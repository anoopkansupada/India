// BOUTIQUES AND SHOPPING - With Google Places API Integration
// This version searches for actual Google Places listings and falls back to manual coordinates

// Add this to your index.html inside the initMap() function (after the existing markers)

const boutiquesData = [
    {
        name: 'Lune',
        city: 'Mumbai',
        address: 'Shop 1 & 2, Labbaik House, 39, Chimbai Road, Bandra West, 400050',
        fallbackPosition: { lat: 19.0596, lng: 72.8295 },
        type: 'jewelry',
        category: 'Jewelry',
        icon: '💍',
        color: '#8b5cf6',
        details: 'Cult jewelry, celestial designs • Hours: Mon-Sat 11am–7:30pm, Sun closed',
        url: "shoplune.com",
    },
    {
        name: 'Two Extra Lives',
        city: 'Mumbai',
        address: 'Bungalow 111, 562 Dr Ambedkar Road, Pali Village, Bandra West, 400050',
        fallbackPosition: { lat: 19.0596, lng: 72.8295 },
        type: 'fashion',
        category: 'Vintage/Concept',
        icon: '👗',
        color: '#ec4899',
        details: 'Upcycled, vintage, conscious fashion • Hours: Daily 11am–8pm',
        url: "twoextralives.com",
    },
    {
        name: 'Call of the Valley',
        city: 'Mumbai',
        address: 'Shop 3, Aruna Niwas, Pali Village, Bandra West, 400050',
        fallbackPosition: { lat: 19.0596, lng: 72.8295 },
        type: 'perfume',
        category: 'Perfume/Lifestyle',
        icon: '🌸',
        color: '#a855f7',
        details: 'Artisanal Indian perfume oils',
        url: "callofthevalley.com",
    },
    {
        name: 'Good Earth',
        city: 'Mumbai',
        address: '11-12 Raghuvanshi Mills Compound, Senapati Bapat Marg, Lower Parel',
        fallbackPosition: { lat: 19.0008, lng: 72.8304 },
        type: 'home',
        category: 'Home/Lifestyle',
        icon: '🪴',
        color: '#10b981',
        details: 'Handcrafted luxury homeware, Indian crafts',
        url: "goodearth.in",
    },
    {
        name: 'Hatsu',
        city: 'Mumbai',
        address: '25, Laxmi Mill Compound, Shakti Mills Lane, Mahalakshmi',
        fallbackPosition: { lat: 19.0008, lng: 72.8304 },
        type: 'home',
        category: 'Home/Design',
        icon: '🪴',
        color: '#10b981',
        details: 'Modern lighting, furniture, quirky décor',
        url: "hatsu.in",
    },
    {
        name: 'James Ferreira',
        city: 'Mumbai',
        address: 'Studio 47-G Khotachiwadi Trail, 1st Lane, Khotachiwadi, Girgaon',
        fallbackPosition: { lat: 18.951, lng: 72.8144 },
        type: 'fashion',
        category: 'Fashion',
        icon: '👗',
        color: '#ec4899',
        details: 'Contemporary clothing from heritage bungalow',
        url: "jamesferreira.in",
    },
    {
        name: 'Nicobar',
        city: 'Mumbai',
        address: '10 Ropewalk Lane, Above Kala Ghoda Café, Kala Ghoda, Fort',
        fallbackPosition: { lat: 18.9278, lng: 72.8319 },
        type: 'lifestyle',
        category: 'Lifestyle',
        icon: '✨',
        color: '#ec4899',
        details: 'Tropical-accented homeware, bohemian clothing',
        url: "nicobar.com",
    },
    {
        name: 'Ogaan',
        city: 'Mumbai',
        address: '6/8, Navbharat House, Burjorji S Bharucha Marg, Kala Ghoda',
        fallbackPosition: { lat: 18.9278, lng: 72.8319 },
        type: 'fashion',
        category: 'Designer Fashion',
        icon: '👗',
        color: '#ec4899',
        details: 'Indian designer clothing (men\'s and women\'s)',
        url: "ogaan.com",
    },
    {
        name: 'Sabyasachi',
        city: 'Mumbai',
        address: 'IGP Fort, Veer Nariman Road, near Horniman Circle, Fort',
        fallbackPosition: { lat: 18.932, lng: 72.8347 },
        type: 'fashion',
        category: 'Couture/Wedding',
        icon: '👰',
        color: '#f472b6',
        details: 'Bridalwear flagship/living museum',
        url: "sabyasachiofficial.com",
    },
    {
        name: 'Valliyan',
        city: 'Mumbai',
        address: 'First Floor, Rhythm House Building, 59 Forbes Street, Fort',
        fallbackPosition: { lat: 18.9278, lng: 72.8319 },
        type: 'jewelry',
        category: 'Jewelry',
        icon: '💍',
        color: '#8b5cf6',
        details: 'Statement jewelry, retro-futurist designs',
        url: "valliyan.com",
    },
    {
        name: 'Moonray',
        city: 'Mumbai',
        address: 'Ground floor, Mittal Avenue, Kala Ghoda, Fort',
        fallbackPosition: { lat: 18.9278, lng: 72.8319 },
        type: 'fashion',
        category: 'Womenswear',
        icon: '👗',
        color: '#ec4899',
        details: 'Sophisticated tailored womenswear & accessories',
        url: "moonray.in",
    },
    {
        name: 'Jodi',
        city: 'Mumbai',
        address: 'Shop no. 1, Lentin Chambers, Dalal Street, Fort',
        fallbackPosition: { lat: 18.932, lng: 72.8347 },
        type: 'fashion',
        category: 'Menswear/Womenswear',
        icon: '👗',
        color: '#ec4899',
        details: 'Hand-block print, colorful menswear',
        url: "thejodilife.com",
    },
    {
        name: 'Obataimu',
        city: 'Mumbai',
        address: 'Ground Floor, Machinery House, 3, S Bharucha Marg, Kala Ghoda, Fort',
        fallbackPosition: { lat: 18.9278, lng: 72.8319 },
        type: 'menswear',
        category: 'Concept/Menswear',
        icon: '👔',
        color: '#3b82f6',
        details: 'Limited-edition, innovative contemporary clothing',
        url: "obataimu.com",
    },
    {
        name: 'Nappa Dori',
        city: 'Mumbai',
        address: '2, Sunny House, Mereweather Road, Colaba',
        fallbackPosition: { lat: 18.9067, lng: 72.8147 },
        type: 'accessories',
        category: 'Accessories',
        icon: '👜',
        color: '#f59e0b',
        details: 'Luggage and leather accessories',
        url: "nappadori.com",
    },
    {
        name: 'Le Mill',
        city: 'Mumbai',
        address: '1st Floor, Pheroze Building, Chhatrapati Shivaji Maharaj Marg, Colaba',
        fallbackPosition: { lat: 18.9067, lng: 72.8147 },
        type: 'luxury',
        category: 'Luxury Fashion',
        icon: '💎',
        color: '#8b5cf6',
        details: 'Global luxury brands, top international labels',
        url: "lemillindia.com",
    },
    {
        name: 'Linking Road',
        city: 'Mumbai',
        address: 'Linking Road, Bandra West',
        fallbackPosition: { lat: 19.0596, lng: 72.8295 },
        type: 'shopping',
        category: 'Street Shopping',
        icon: '🛍️',
        color: '#f59e0b',
        details: 'Trendy street fashion, accessible prices',
        url: null,
    },
    {
        name: 'Colaba Causeway',
        city: 'Mumbai',
        address: 'Colaba Causeway, Colaba',
        fallbackPosition: { lat: 18.9067, lng: 72.8147 },
        type: 'shopping',
        category: 'Street Shopping',
        icon: '🛍️',
        color: '#f59e0b',
        details: 'Eclectic finds, vintage-inspired',
        url: null,
    },
    {
        name: 'Phoenix Palladium',
        city: 'Mumbai',
        address: 'Phoenix Palladium, Lower Parel',
        fallbackPosition: { lat: 19.0008, lng: 72.8304 },
        type: 'shopping',
        category: 'Mall',
        icon: '🏬',
        color: '#64748b',
        details: 'Luxury brands, flagship stores',
        url: null,
    },
    // JAIPUR
    {
        name: 'ANOKHI',
        city: 'Jaipur',
        address: 'C-Scheme, Jaipur',
        fallbackPosition: { lat: 26.9024, lng: 75.7878 },
        type: 'fashion',
        category: 'Concept/Fashion',
        icon: '👗',
        color: '#ec4899',
        details: 'Block-printed clothing, eco-conscious, 50+ years heritage',
        url: "anokhi.com",
    },
    {
        name: 'Nila House',
        city: 'Jaipur',
        address: 'C-86, Prithviraj Road, C Scheme, Jaipur',
        fallbackPosition: { lat: 26.9024, lng: 75.7878 },
        type: 'textile',
        category: 'Textile/Lifestyle',
        icon: '🧵',
        color: '#10b981',
        details: 'Natural dyeing, modern Rajasthani tradition',
        url: "nilahouse.com",
    },
    {
        name: 'Anokhi Museum',
        city: 'Jaipur',
        address: 'Kheri Gate, Amer, Jaipur',
        fallbackPosition: { lat: 26.9855, lng: 75.8513 },
        type: 'museum',
        category: 'Museum/Textile',
        icon: '🏛️',
        color: '#6366f1',
        details: 'Hand-block printing heritage techniques',
        url: "anokhi.com",
    },
    {
        name: 'Johri Bazaar',
        city: 'Jaipur',
        address: 'Johri Bazaar, Jaipur',
        fallbackPosition: { lat: 26.9248, lng: 75.8246 },
        type: 'shopping',
        category: 'Traditional Market',
        icon: '🏪',
        color: '#ef4444',
        details: 'Oldest pink market, jewelry, textiles, lehariya',
        url: null,
    },
    {
        name: 'Bapu Bazaar',
        city: 'Jaipur',
        address: 'Bapu Bazaar, Jaipur',
        fallbackPosition: { lat: 26.9248, lng: 75.8246 },
        type: 'shopping',
        category: 'Street Shopping',
        icon: '🛍️',
        color: '#f59e0b',
        details: 'Men\'s suits, boots, ethnic wear',
        url: null,
    },
    // UDAIPUR
    {
        name: 'Bapu Bazaar Udaipur',
        city: 'Udaipur',
        address: 'Bapu Bazaar, Udaipur',
        fallbackPosition: { lat: 24.58, lng: 73.682 },
        type: 'shopping',
        category: 'Traditional Market',
        icon: '🏪',
        color: '#ef4444',
        details: 'Bandhani sarees, embroidered textiles',
        url: null,
    },
    {
        name: 'Jagdish Chowk',
        city: 'Udaipur',
        address: 'Jagdish Chowk, Udaipur',
        fallbackPosition: { lat: 24.5794, lng: 73.6833 },
        type: 'shopping',
        category: 'Heritage Market',
        icon: '🏛️',
        color: '#ef4444',
        details: 'Antique jewelry, hand-carved items',
        url: null,
    },
    {
        name: 'City Palace Boutiques',
        city: 'Udaipur',
        address: 'City Palace Complex, Udaipur',
        fallbackPosition: { lat: 24.576, lng: 73.6832 },
        type: 'handicrafts',
        category: 'Royal Crafts',
        icon: '👑',
        color: '#9333ea',
        details: 'High-quality Mewar handicrafts',
        url: null,
    },
    // AGRA
    {
        name: 'Sadar Bazaar',
        city: 'Agra',
        address: 'Sadar Bazaar, Agra',
        fallbackPosition: { lat: 27.1903, lng: 78.0022 },
        type: 'shopping',
        category: 'Traditional Market',
        icon: '🏪',
        color: '#ef4444',
        details: 'Traditional shopping, textiles',
        url: null,
    },
    {
        name: 'Kinari Bazaar',
        city: 'Agra',
        address: 'Kinari Bazaar, Agra',
        fallbackPosition: { lat: 27.1751, lng: 78.0421 },
        type: 'shopping',
        category: 'Textile Market',
        icon: '🧵',
        color: '#10b981',
        details: 'Textiles, embroidery, traditional crafts',
        url: null,
    },
    // RANTHAMBORE
    {
        name: 'Dastkar Ranthambore',
        city: 'Ranthambore',
        address: 'Sawai Madhopur, near Ranthambore',
        fallbackPosition: { lat: 26.0173, lng: 76.3426 },
        type: 'handicrafts',
        category: 'Handicrafts/Textiles',
        icon: '🎨',
        color: '#8b5cf6',
        details: 'Community coop, handmade textiles, village crafts',
        url: "dastkar.org",
    },
];

// ============================================
// PLACES API INTEGRATION
// ============================================

async function addBoutiquesWithPlacesAPI(map, bounds) {
    const placesService = new google.maps.places.PlacesService(map);
    let processedCount = 0;
    const totalBoutiques = boutiquesData.length;

    // Process boutiques in batches to avoid rate limits
    for (const boutique of boutiquesData) {
        await new Promise((resolve) => {
            // Try to find the actual place using Text Search
            const searchQuery = `${boutique.name} ${boutique.address || boutique.city}`;

            const request = {
                query: searchQuery,
                fields: ['name', 'geometry', 'place_id', 'formatted_address', 'rating', 'user_ratings_total', 'business_status']
            };

            placesService.textSearch(request, (results, status) => {
                let finalPosition = boutique.fallbackPosition;
                let placeId = null;
                let actualName = boutique.name;
                let rating = null;
                let userRatingsTotal = null;

                // If we found a valid place, use its location
                if (status === google.maps.places.PlacesServiceStatus.OK && results && results.length > 0) {
                    const place = results[0];
                    finalPosition = place.geometry.location;
                    placeId = place.place_id;
                    actualName = place.name || boutique.name;
                    rating = place.rating;
                    userRatingsTotal = place.user_ratings_total;

                    console.log(`✓ Found: ${boutique.name} → ${place.name} (${place.formatted_address})`);
                } else {
                    console.log(`⚠ Using fallback for: ${boutique.name} (Status: ${status})`);
                }

                // Create marker with actual or fallback position
                createBoutiqueMarker(map, boutique, finalPosition, placeId, actualName, rating, userRatingsTotal);

                // Extend bounds
                if (finalPosition.lat && finalPosition.lng) {
                    bounds.extend(finalPosition);
                } else {
                    bounds.extend(new google.maps.LatLng(finalPosition.lat(), finalPosition.lng()));
                }

                processedCount++;

                // Small delay to respect API rate limits
                setTimeout(resolve, 100);
            });
        });
    }

    console.log(`Processed ${processedCount} of ${totalBoutiques} boutiques`);

    // Re-fit the map after all markers are added
    map.fitBounds(bounds);
}

function createBoutiqueMarker(map, boutique, position, placeId, actualName, rating, userRatingsTotal) {
    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: actualName,
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

    // Build info window content
    let infoContent = `
        <div style="font-family: 'Lato', sans-serif; max-width: 300px;">
            <div style="display: flex; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 20px; margin-right: 8px;">${boutique.icon}</span>
                <h3 style="margin: 0; font-size: 15px; font-weight: bold; color: #1f2937;">${actualName}</h3>
            </div>
            <p style="margin: 0 0 4px 0; font-size: 12px; color: ${boutique.color}; font-weight: 600; text-transform: uppercase;">${boutique.category} • ${boutique.city}</p>
    `;

    // Add Google rating if available
    if (rating && userRatingsTotal) {
        const stars = '⭐'.repeat(Math.round(rating));
        infoContent += `<p style="margin: 0 0 4px 0; font-size: 11px; color: #6b7280;">${stars} ${rating.toFixed(1)} (${userRatingsTotal} reviews)</p>`;
    }

    infoContent += `<p style="margin: 0; font-size: 13px; color: #6b7280; line-height: 1.4;">${boutique.details}</p>`;

    // Add website link if available
    if (boutique.url) {
        const fullUrl = boutique.url.startsWith('http') ? boutique.url : `https://${boutique.url}`;
        infoContent += `<a href="${fullUrl}" target="_blank" style="display: inline-block; margin-top: 8px; font-size: 12px; color: #2563eb; text-decoration: none; font-weight: 600;">Visit Website →</a>`;
    }

    // Add Google Maps link if we have a place ID
    if (placeId) {
        infoContent += `<br><a href="https://www.google.com/maps/place/?q=place_id:${placeId}" target="_blank" style="display: inline-block; margin-top: 4px; font-size: 12px; color: #059669; text-decoration: none; font-weight: 600;">View on Google Maps →</a>`;
    }

    infoContent += `</div>`;

    const infoWindow = new google.maps.InfoWindow({
        content: infoContent
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });
}

// ============================================
// USAGE INSTRUCTIONS
// ============================================
/*
ADD THIS CODE TO YOUR initMap() function in index.html:

// After creating your map and bounds objects:
const map = new google.maps.Map(document.getElementById('map'), {...});
const bounds = new google.maps.LatLngBounds();

// ... your existing markers ...

// Add boutiques with Places API
addBoutiquesWithPlacesAPI(map, bounds);

NOTE: Make sure your Google Maps API includes the Places library:
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=initMap&libraries=places&v=weekly"></script>
*/
