#!/usr/bin/env python3
"""
Geocode boutiques from CSV and generate Google Maps JavaScript code.
This script processes the boutiques CSV, removes duplicates, geocodes addresses,
and outputs ready-to-use JavaScript for the map.
"""

import csv
import json
import requests
import time
from typing import List, Dict, Optional

# Your Google Maps API Key
# NOTE: This script is no longer needed - we use manual geocoding instead
# See geocode_boutiques_manual.py
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # Not used

# Category to icon/color mapping
CATEGORY_MAPPING = {
    "Jewelry": {"icon": "💍", "color": "#8b5cf6", "type": "jewelry"},
    "Vintage/Concept": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Fashion": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Designer Fashion": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Couture/Wedding": {"icon": "👰", "color": "#f472b6", "type": "fashion"},
    "Womenswear": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Menswear/Womenswear": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Custom Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Designer Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Premium Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Ethnic Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Wedding Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Ethnic & Western": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Suiting": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Tailoring": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Streetwear": {"icon": "🧢", "color": "#6366f1", "type": "menswear"},
    "Perfume/Lifestyle": {"icon": "🌸", "color": "#a855f7", "type": "perfume"},
    "Perfume": {"icon": "🌸", "color": "#a855f7", "type": "perfume"},
    "Home/Lifestyle": {"icon": "🏠", "color": "#10b981", "type": "home"},
    "Home/Design": {"icon": "🏠", "color": "#10b981", "type": "home"},
    "Home/Furniture": {"icon": "🏠", "color": "#10b981", "type": "home"},
    "Home/Interiors": {"icon": "🏠", "color": "#10b981", "type": "home"},
    "Home/Decor": {"icon": "🏠", "color": "#10b981", "type": "home"},
    "Lifestyle": {"icon": "✨", "color": "#ec4899", "type": "lifestyle"},
    "Concept/Fashion": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Concept/Menswear": {"icon": "👔", "color": "#3b82f6", "type": "menswear"},
    "Concept Store": {"icon": "✨", "color": "#ec4899", "type": "lifestyle"},
    "Accessories": {"icon": "👜", "color": "#f59e0b", "type": "accessories"},
    "Luxury Fashion": {"icon": "💎", "color": "#8b5cf6", "type": "luxury"},
    "Street Shopping": {"icon": "🛍️", "color": "#f59e0b", "type": "shopping"},
    "Mall": {"icon": "🏬", "color": "#64748b", "type": "shopping"},
    "Traditional Market": {"icon": "🏪", "color": "#ef4444", "type": "shopping"},
    "Textile/Lifestyle": {"icon": "🧵", "color": "#10b981", "type": "textile"},
    "Museum/Textile": {"icon": "🏛️", "color": "#6366f1", "type": "museum"},
    "Handicrafts/Textiles": {"icon": "🎨", "color": "#8b5cf6", "type": "handicrafts"},
    "Community Crafts": {"icon": "🎨", "color": "#8b5cf6", "type": "handicrafts"},
    "Traditional Crafts": {"icon": "🎨", "color": "#8b5cf6", "type": "handicrafts"},
    "Local Handicrafts": {"icon": "🎨", "color": "#8b5cf6", "type": "handicrafts"},
    "Eco Crafts": {"icon": "🌿", "color": "#10b981", "type": "handicrafts"},
    "Souvenirs": {"icon": "🎁", "color": "#f59e0b", "type": "souvenirs"},
    "Heritage Market": {"icon": "🏛️", "color": "#ef4444", "type": "shopping"},
    "Antiques Market": {"icon": "⚱️", "color": "#92400e", "type": "shopping"},
    "Royal Crafts": {"icon": "👑", "color": "#9333ea", "type": "handicrafts"},
    "Fashion/Vintage": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Vintage/Thrift": {"icon": "👗", "color": "#ec4899", "type": "fashion"},
    "Multi-brand": {"icon": "🛍️", "color": "#64748b", "type": "shopping"},
    "Textile Market": {"icon": "🧵", "color": "#10b981", "type": "shopping"},
    "Shopping District": {"icon": "🏬", "color": "#64748b", "type": "shopping"},
}

def read_csv_and_deduplicate(filename: str) -> List[Dict]:
    """Read CSV and remove duplicates."""
    seen = set()
    unique_stores = []

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create unique key based on city + store name
            key = (row['City'].strip(), row['Store Name'].strip())

            # Skip empty rows or duplicates
            if not row['City'] or key in seen:
                continue

            seen.add(key)
            unique_stores.append(row)

    return unique_stores

def geocode_address(address: str, city: str) -> Optional[Dict[str, float]]:
    """
    Geocode an address using Google Geocoding API.
    Returns dict with lat/lng or None if failed.
    """
    if not address or address == city:
        # If address is just the city name, geocode the city
        query = f"{city}, India"
    else:
        query = f"{address}, {city}, India"

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data['status'] == 'OK' and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            return {
                "lat": location['lat'],
                "lng": location['lng']
            }
        else:
            print(f"  ⚠️  Geocoding failed for: {query} (Status: {data['status']})")
            return None
    except Exception as e:
        print(f"  ❌ Error geocoding {query}: {e}")
        return None

def process_boutiques(stores: List[Dict]) -> List[Dict]:
    """Process stores and geocode them."""
    processed = []

    for idx, store in enumerate(stores, 1):
        print(f"Processing {idx}/{len(stores)}: {store['Store Name']} in {store['City']}")

        # Get category mapping
        category = store['Category'].strip()
        mapping = CATEGORY_MAPPING.get(category, {"icon": "🏪", "color": "#64748b", "type": "store"})

        # Geocode the address
        position = geocode_address(store['Address'], store['City'])

        if position is None:
            # Try with just neighborhood if full address failed
            position = geocode_address(store['Neighborhood'], store['City'])

        if position is None:
            print(f"  ⚠️  Skipping {store['Store Name']} - could not geocode")
            continue

        # Build details string
        details_parts = []
        if store['Specialty']:
            details_parts.append(store['Specialty'])
        if store['Hours'] and store['Hours'] != 'Not listed (call ahead)':
            details_parts.append(f"Hours: {store['Hours']}")
        if store['Neighborhood']:
            details_parts.append(f"📍 {store['Neighborhood']}")

        details = ' • '.join(details_parts) if details_parts else store['Category']

        processed_store = {
            "name": store['Store Name'],
            "city": store['City'],
            "position": position,
            "type": mapping['type'],
            "category": category,
            "icon": mapping['icon'],
            "color": mapping['color'],
            "details": details,
            "url": store['Website'] if store['Website'] else None,
            "instagram": store['Instagram'] if store['Instagram'] else None,
            "phone": store['Phone'] if store['Phone'] else None,
            "address": store['Address']
        }

        processed.append(processed_store)

        # Rate limiting - Google API allows 50 requests/second
        time.sleep(0.05)

    return processed

def generate_javascript(boutiques: List[Dict], output_file: str):
    """Generate JavaScript code for the map."""

    js_code = """// BOUTIQUES AND SHOPPING - Generated by geocode_boutiques.py
// Copy this array into your index.html file and add to the map

const boutiquesData = [
"""

    for boutique in boutiques:
        url_line = f'url: "{boutique["url"]}",' if boutique['url'] else ''

        js_code += f"""    {{
        name: '{boutique['name'].replace("'", "\\'")}',
        city: '{boutique['city']}',
        position: {{ lat: {boutique['position']['lat']}, lng: {boutique['position']['lng']} }},
        type: '{boutique['type']}',
        category: '{boutique['category']}',
        icon: '{boutique['icon']}',
        color: '{boutique['color']}',
        details: '{boutique['details'].replace("'", "\\'")}',
        {url_line}
    }},
"""

    js_code += """];

// ADD THIS CODE to your initMap() function in index.html:

// Add boutique markers to map
boutiquesData.forEach(boutique => {
    const marker = new google.maps.Marker({
        position: boutique.position,
        map: map,
        title: boutique.name,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 10,
            fillColor: boutique.color,
            fillOpacity: 0.9,
            strokeColor: 'white',
            strokeWeight: 2
        },
        label: {
            text: boutique.icon,
            color: 'white',
            fontSize: '10px'
        }
    });

    // Build info content with optional link
    let infoContent = `
        <div style="font-family: 'Lato', sans-serif; max-width: 280px;">
            <div style="display: flex; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 20px; margin-right: 8px;">${boutique.icon}</span>
                <h3 style="margin: 0; font-size: 15px; font-weight: bold; color: #1f2937;">${boutique.name}</h3>
            </div>
            <p style="margin: 0 0 4px 0; font-size: 12px; color: ${boutique.color}; font-weight: 600; text-transform: uppercase;">${boutique.category} • ${boutique.city}</p>
            <p style="margin: 0; font-size: 13px; color: #6b7280; line-height: 1.4;">${boutique.details}</p>
    `;

    if (boutique.url) {
        infoContent += `<a href="${boutique.url}" target="_blank" style="display: inline-block; margin-top: 8px; font-size: 12px; color: #2563eb; text-decoration: none; font-weight: 600;">Visit Website →</a>`;
    }

    infoContent += `</div>`;

    const infoWindow = new google.maps.InfoWindow({
        content: infoContent
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });

    bounds.extend(boutique.position);
});
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)

    print(f"\n✅ JavaScript code saved to: {output_file}")

def main():
    input_file = "India_Boutiques_Complete_Guide.csv"
    output_file = "boutiques_map_code.js"

    print("🏪 Processing boutiques CSV...")
    stores = read_csv_and_deduplicate(input_file)
    print(f"Found {len(stores)} unique stores")

    print("\n🌍 Geocoding addresses...")
    boutiques = process_boutiques(stores)
    print(f"Successfully geocoded {len(boutiques)}/{len(stores)} stores")

    print("\n📝 Generating JavaScript code...")
    generate_javascript(boutiques, output_file)

    # Save processed data as JSON for reference
    with open('boutiques_processed.json', 'w', encoding='utf-8') as f:
        json.dump(boutiques, f, indent=2, ensure_ascii=False)
    print(f"✅ Processed data saved to: boutiques_processed.json")

    print("\n🎉 Done! Copy the code from boutiques_map_code.js into your index.html file.")

if __name__ == "__main__":
    main()
