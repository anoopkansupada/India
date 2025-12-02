#!/usr/bin/env python3
"""
Process boutiques CSV with manual neighborhood geocoding.
Uses approximate coordinates for major neighborhoods in each city.
"""

import csv
import json
from typing import List, Dict, Optional

# Manual coordinates for major neighborhoods in each city
NEIGHBORHOOD_COORDS = {
    # MUMBAI
    ("Mumbai", "Bandra West"): {"lat": 19.0596, "lng": 72.8295},
    ("Mumbai", "Bandra"): {"lat": 19.0596, "lng": 72.8295},
    ("Mumbai", "Lower Parel"): {"lat": 19.0008, "lng": 72.8304},
    ("Mumbai", "Girgaon"): {"lat": 18.9510, "lng": 72.8144},
    ("Mumbai", "Kala Ghoda"): {"lat": 18.9278, "lng": 72.8319},
    ("Mumbai", "Fort"): {"lat": 18.9320, "lng": 72.8347},
    ("Mumbai", "Colaba"): {"lat": 18.9067, "lng": 72.8147},
    ("Mumbai", "Juhu"): {"lat": 19.0990, "lng": 72.8268},
    ("Mumbai", "Andheri West"): {"lat": 19.1355, "lng": 72.8262},
    ("Mumbai", "Khar"): {"lat": 19.0708, "lng": 72.8357},
    ("Mumbai", "Borivali West"): {"lat": 19.2307, "lng": 72.8567},
    ("Mumbai", "Goregaon"): {"lat": 19.1653, "lng": 72.8494},
    ("Mumbai", "Ghatkopar West"): {"lat": 19.0866, "lng": 72.9081},
    ("Mumbai", "Kandivali"): {"lat": 19.2042, "lng": 72.8546},
    ("Mumbai", "Mumbai"): {"lat": 19.0760, "lng": 72.8777},  # Central Mumbai

    # JAIPUR
    ("Jaipur", "Ashok Nagar"): {"lat": 26.8871, "lng": 75.8076},
    ("Jaipur", "Malviya Nagar"): {"lat": 26.8544, "lng": 75.8205},
    ("Jaipur", "C-Scheme"): {"lat": 26.9024, "lng": 75.7878},
    ("Jaipur", "C Scheme"): {"lat": 26.9024, "lng": 75.7878},
    ("Jaipur", "Amer"): {"lat": 26.9855, "lng": 75.8513},
    ("Jaipur", "Old City"): {"lat": 26.9248, "lng": 75.8246},
    ("Jaipur", "Jaipur"): {"lat": 26.9124, "lng": 75.7873},  # Central Jaipur

    # UDAIPUR
    ("Udaipur", "Bapu Bazar"): {"lat": 24.5800, "lng": 73.6820},
    ("Udaipur", "Old City"): {"lat": 24.5794, "lng": 73.6833},
    ("Udaipur", "City Palace"): {"lat": 24.5760, "lng": 73.6832},
    ("Udaipur", "Panchwati"): {"lat": 24.5854, "lng": 73.6872},
    ("Udaipur", "Court Chowaraha"): {"lat": 24.5858, "lng": 73.6854},
    ("Udaipur", "Udaipur"): {"lat": 24.5854, "lng": 73.7125},  # Central Udaipur

    # AGRA
    ("Agra", "Kamla Nagar"): {"lat": 27.2046, "lng": 78.0131},
    ("Agra", "Sikandra"): {"lat": 27.2152, "lng": 77.9753},
    ("Agra", "Sanjay Place"): {"lat": 27.1767, "lng": 78.0081},
    ("Agra", "Sadar"): {"lat": 27.1903, "lng": 78.0022},
    ("Agra", "Old City"): {"lat": 27.1751, "lng": 78.0421},
    ("Agra", "Agra"): {"lat": 27.1767, "lng": 78.0081},  # Central Agra

    # RANTHAMBORE / SAWAI MADHOPUR
    ("Ranthambore", "Sawai Madhopur"): {"lat": 26.0173, "lng": 76.3426},
    ("Ranthambore", "Ranthambore"): {"lat": 26.0173, "lng": 76.5026},
}

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

            # Skip empty rows, header rows, or duplicates
            if not row['City'] or row['City'] == 'City' or key in seen:
                continue

            seen.add(key)
            unique_stores.append(row)

    return unique_stores

def get_coordinates(city: str, neighborhood: str) -> Optional[Dict[str, float]]:
    """Get coordinates from manual mapping."""
    # Try exact match first
    key = (city, neighborhood)
    if key in NEIGHBORHOOD_COORDS:
        return NEIGHBORHOOD_COORDS[key]

    # Try city-level coordinates
    city_key = (city, city)
    if city_key in NEIGHBORHOOD_COORDS:
        return NEIGHBORHOOD_COORDS[city_key]

    return None

def process_boutiques(stores: List[Dict]) -> List[Dict]:
    """Process stores with manual coordinates."""
    processed = []

    for idx, store in enumerate(stores, 1):
        city = store['City'].strip()
        neighborhood = store['Neighborhood'].strip()

        print(f"Processing {idx}/{len(stores)}: {store['Store Name']} in {city}")

        # Get category mapping
        category = store['Category'].strip()
        mapping = CATEGORY_MAPPING.get(category, {"icon": "🏪", "color": "#64748b", "type": "store"})

        # Get coordinates
        position = get_coordinates(city, neighborhood)

        if position is None:
            print(f"  ⚠️  Skipping {store['Store Name']} - no coordinates for {city}/{neighborhood}")
            continue

        # Build details string
        details_parts = []
        if store['Specialty']:
            details_parts.append(store['Specialty'])
        if store['Hours'] and store['Hours'] not in ['Not listed (call ahead)', '']:
            details_parts.append(f"Hours: {store['Hours']}")
        if store['Address'] and store['Address'] != neighborhood:
            details_parts.append(f"📍 {store['Address']}")
        elif neighborhood:
            details_parts.append(f"📍 {neighborhood}")

        details = ' • '.join(details_parts) if details_parts else store['Category']

        processed_store = {
            "name": store['Store Name'],
            "city": city,
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

    return processed

def generate_javascript(boutiques: List[Dict], output_file: str):
    """Generate JavaScript code for the map."""

    js_code = """// BOUTIQUES AND SHOPPING - Generated automatically
// Add this to your index.html inside the initMap() function

const boutiquesData = [
"""

    for boutique in boutiques:
        url_line = f'        url: "{boutique["url"]}",' if boutique['url'] else '        url: null,'

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

// ADD THIS CODE to your initMap() function in index.html (after the existing pointsOfInterest markers):

boutiquesData.forEach(boutique => {
    const marker = new google.maps.Marker({
        position: boutique.position,
        map: map,
        title: boutique.name,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillColor: boutique.color,
            fillOpacity: 0.85,
            strokeColor: 'white',
            strokeWeight: 2
        },
        label: {
            text: boutique.icon,
            color: 'white',
            fontSize: '9px'
        }
    });

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

// After adding all markers, re-fit the bounds
map.fitBounds(bounds);
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)

    print(f"\n✅ JavaScript code saved to: {output_file}")

def main():
    input_file = "India_Boutiques_Complete_Guide.csv"
    output_file = "boutiques_map_code.js"

    print("🏪 Processing boutiques CSV...")
    stores = read_csv_and_deduplicate(input_file)
    print(f"Found {len(stores)} unique stores\n")

    print("📍 Using manual neighborhood coordinates...")
    boutiques = process_boutiques(stores)
    print(f"\n✅ Successfully processed {len(boutiques)}/{len(stores)} stores")

    print("\n📝 Generating JavaScript code...")
    generate_javascript(boutiques, output_file)

    # Save processed data as JSON for reference
    with open('boutiques_processed.json', 'w', encoding='utf-8') as f:
        json.dump(boutiques, f, indent=2, ensure_ascii=False)
    print(f"✅ Processed data saved to: boutiques_processed.json")

    print("\n" + "="*60)
    print("🎉 DONE! Next steps:")
    print("="*60)
    print("1. Open: boutiques_map_code.js")
    print("2. Copy all the code")
    print("3. Paste it into your index.html inside the initMap() function")
    print("4. The boutiques will appear on your map with colored icons!")
    print("="*60)

if __name__ == "__main__":
    main()
