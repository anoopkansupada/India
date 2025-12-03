# 🔒 Securing Your Google Maps API Key

Your Google Maps API key is currently public in the HTML file. Here's how to properly secure it:

## Option 1: Restrict the API Key (RECOMMENDED - Quick & Easy)

1. **Go to Google Cloud Console**:
   - Visit: https://console.cloud.google.com/google/maps-apis/credentials
   - Sign in with your Google account

2. **Find your API key** (it should be listed in the credentials page)

3. **Click "Edit API key" (pencil icon)**

4. **Set Application Restrictions**:
   - Choose "HTTP referrers (web sites)"
   - Add your allowed websites:
     ```
     https://anoopkansupada.github.io/India/*
     http://localhost/*
     http://localhost:*/*
     ```
   - This prevents unauthorized use from other domains

   **Note:** To test locally by opening HTML files directly (file:///...), you'll need to temporarily set "Application restrictions" to "None". For production, use the referrers above.

5. **Set API Restrictions**:
   - Choose "Restrict key"
   - Select only these APIs:
     - Maps JavaScript API
     - Geocoding API (if needed)
     - Places API (if needed)

6. **Save**

**This is the easiest solution and works immediately!**

---

## Option 2: Use a Backend Proxy (Most Secure)

For production sites, hide the API key completely using a backend server:

### Setup:

1. Create a simple backend endpoint (Node.js example):

```javascript
// server.js
const express = require('express');
const app = express();

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY; // Store in env variable

app.get('/api/maps-config', (req, res) => {
    res.json({ apiKey: GOOGLE_MAPS_API_KEY });
});

app.listen(3000);
```

2. Update your HTML to fetch the key:

```html
<script>
async function initMap() {
    // Fetch API key from your backend
    const response = await fetch('/api/maps-config');
    const config = await response.json();

    // Load Google Maps dynamically
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${config.apiKey}&callback=loadMap`;
    document.head.appendChild(script);
}

function loadMap() {
    // Your existing map initialization code
}
</script>
```

---

## Option 3: Environment Variables (For Development)

If you're deploying via a hosting service (Vercel, Netlify, etc.):

1. **Store the key in your hosting platform's environment variables**

2. **Use build-time replacement**:

```javascript
// In your build process, replace the placeholder
const MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY;
```

---

## ⚠️ Current Risk Level

**Medium Risk**: Your key is public but can only be used for Maps JavaScript API calls.

**Potential Issues**:
- Someone could copy your key and use it on their website
- This could exhaust your API quota
- Could lead to unexpected charges if quota is exceeded

**Immediate Actions**:
1. Set up billing alerts in Google Cloud Console
2. Set a daily quota limit (e.g., 10,000 requests/day)
3. Enable API restrictions (Option 1 above)

---

## 💰 Billing Protection

1. **Set up a budget alert**:
   - Go to: https://console.cloud.google.com/billing
   - Create budget alert at $50, $100, $200

2. **Set quota limits**:
   - Go to: https://console.cloud.google.com/google/maps-apis/quotas
   - Set daily limits for each API

---

## ✅ Recommended Immediate Action

**Do this right now** (takes 2 minutes):

1. Go to: https://console.cloud.google.com/google/maps-apis/credentials
2. Click on your API key
3. Under "Application restrictions" → Choose "HTTP referrers"
4. Add: `https://yourdomain.com/*` (or your actual domain)
5. Add: `http://localhost:*` (for local testing)
6. Click "Save"

This will immediately prevent unauthorized use while keeping your site working!

---

## 🔍 Check for Unauthorized Usage

Monitor your API usage:
- Visit: https://console.cloud.google.com/google/maps-apis/metrics
- Check for unusual spikes or unknown referrers
