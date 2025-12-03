# 🚨 URGENT: API Key Rotation Required

## ⚠️ What Happened

Your Google Maps API key `AIzaSyBSRrd-sjbtPbT8BSd4f4icQJTWQNJHpwE` was exposed in the file `SECURITY_SETUP.md` which was committed to your public GitHub repository.

**Status**: The key has been removed from the documentation, but it remains in Git history. Anyone who accessed your repository may have copied it.

---

## 🔴 IMMEDIATE ACTION REQUIRED (Do This Now!)

### Step 1: Delete the Exposed API Key

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/google/maps-apis/credentials)
2. Find the key: `AIzaSyBSRrd-sjbtPbT8BSd4f4icQJTWQNJHpwE`
3. Click the **trash icon** to DELETE it
4. Confirm deletion

**This immediately invalidates the key so no one can use it.**

---

### Step 2: Create a New API Key

1. Still in [Google Cloud Console - Credentials](https://console.cloud.google.com/google/maps-apis/credentials)
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"API key"**
4. A new key will be created (copy it somewhere safe temporarily)

---

### Step 3: Restrict the New API Key (CRITICAL!)

**Do NOT skip this step!** This prevents unauthorized use:

1. Click **"EDIT API KEY"** (pencil icon) next to your new key
2. Give it a name: `India Trip Map - Restricted`

#### Set Application Restrictions:
- Select **"HTTP referrers (web sites)"**
- Click **"ADD AN ITEM"** and add (for GitHub Pages):
  ```
  https://anoopkansupada.github.io/India/*
  ```
- Click **"ADD AN ITEM"** again and add (for local testing):
  ```
  http://localhost/*
  ```
- Click **"ADD AN ITEM"** again and add (for local testing on any port):
  ```
  http://localhost:*/*
  ```

**Note:** For local file testing (opening HTML directly), restrictions won't work. You have two options:
- **Option A:** Temporarily select "None" for Application restrictions while testing locally
- **Option B:** Use a local web server (recommended):
  ```bash
  cd /Users/anoopkansupada/India/India
  python3 -m http.server 8000
  # Then open: http://localhost:8000/index.html
  ```

#### Set API Restrictions:
- Select **"Restrict key"**
- Check ONLY these APIs:
  - ✅ Maps JavaScript API
  - ✅ Places API
  - ✅ Geocoding API (if needed)
- Leave everything else unchecked

3. Click **"SAVE"**

---

### Step 4: Update Your Local config.js

1. Open the file: `config.js` in your India project folder
2. Replace the old key with your NEW key:

```javascript
// Configuration file for API keys and sensitive data
// WARNING: This file contains your actual API key and should NOT be committed to Git!

const CONFIG = {
    GOOGLE_MAPS_API_KEY: 'YOUR_NEW_KEY_HERE'
};
```

3. Save the file

---

### Step 5: Test the Map

1. Open `index.html` in your browser
2. The map should load successfully
3. If you see errors, check:
   - Did you save config.js with the new key?
   - Did you add all the HTTP referrer restrictions (including `file:///*`)?

---

### Step 6: Set Up Billing Protection

**Prevent surprise charges:**

1. Go to [Google Cloud Billing](https://console.cloud.google.com/billing)
2. Click **"Budgets & alerts"**
3. Click **"CREATE BUDGET"**
4. Set budget amount: **$20/month** (Google gives $200 free credit)
5. Set alert thresholds at: **50%, 90%, 100%**
6. Add your email for notifications

#### Set Quota Limits:
1. Go to [Maps API Quotas](https://console.cloud.google.com/google/maps-apis/quotas)
2. Find **"Maps JavaScript API"**
3. Set daily quota: **10,000 requests/day** (more than enough for your trip)

---

## 📊 Verification Checklist

After completing all steps, verify:

- [ ] Old API key is DELETED from Google Cloud Console
- [ ] New API key is created
- [ ] HTTP referrer restrictions are set (github.io, localhost, file://)
- [ ] API restrictions are set (only Maps JavaScript, Places, Geocoding)
- [ ] config.js is updated with new key
- [ ] Map loads successfully in browser
- [ ] Billing budget alerts are configured ($20/month)
- [ ] Daily quota limits are set (10,000 requests/day)

---

## 🔒 Security Best Practices Going Forward

### ✅ DO:
- Keep `config.js` in .gitignore (already done)
- Monitor API usage monthly: [Usage Metrics](https://console.cloud.google.com/google/maps-apis/metrics)
- Use domain restrictions for all API keys
- Set up billing alerts

### ❌ DON'T:
- Never commit `config.js` to Git
- Never share API keys in documentation
- Never disable restrictions to "fix" issues
- Never ignore billing alert emails

---

## 🆘 If You See Suspicious Usage

If you see unexpected API calls in [Usage Metrics](https://console.cloud.google.com/google/maps-apis/metrics):

1. **Immediately delete the key** (even if it's the new one)
2. Create another new key with even stricter restrictions
3. Check the referrer logs to see where calls are coming from
4. Consider adding more specific domain restrictions

---

## 📞 Need Help?

If you have issues:

1. Check the browser console for error messages (F12 → Console tab)
2. Verify the key works: [Test in Google Maps Platform](https://developers.google.com/maps/documentation/javascript/get-api-key#test-key)
3. Review restrictions: Make sure you added `file:///*` for local testing

---

## 🎯 Summary

**Priority**: 🔴 HIGH - Do this within the next hour

**Time Required**: ~10 minutes

**Steps**:
1. Delete old key (1 min)
2. Create new key (1 min)
3. Set restrictions (3 min)
4. Update config.js (1 min)
5. Test (2 min)
6. Set billing protection (2 min)

**Result**: Your map will work securely without risk of unauthorized use or surprise charges.

---

**🛡️ After following these steps, your API key will be properly secured!**

Questions? Check the [Google Maps Platform Documentation](https://developers.google.com/maps/documentation/javascript/get-api-key)
