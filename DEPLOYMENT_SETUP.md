# GitHub Pages Deployment Setup

This guide will help you deploy your India trip website to GitHub Pages with the Google Maps API key securely stored in GitHub Secrets.

## 🎯 What We've Set Up

1. **GitHub Actions Workflow** ([.github/workflows/deploy.yml](.github/workflows/deploy.yml))
   - Automatically deploys your site when you push to the `main` branch
   - Injects the API key during deployment (never stored in the repo)
   - Keeps `config.js` out of version control

2. **Updated index.html** ([index.html](index.html))
   - Better error handling for missing API keys
   - Works both locally (with your local config.js) and on GitHub Pages (with injected config.js)

## 📋 Setup Steps (Do Once)

### Step 1: Add Your API Key to GitHub Secrets

1. Go to your GitHub repository: https://github.com/anoopkansupada/India
2. Click **Settings** (top navigation)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click the **New repository secret** button
5. Enter:
   - **Name**: `GOOGLE_MAPS_API_KEY`
   - **Secret**: `YOUR_GOOGLE_MAPS_API_KEY_HERE` (get this from your local config.js file)
6. Click **Add secret**

### Step 2: Enable GitHub Pages with GitHub Actions

1. In your repository, go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions** (NOT the old "Deploy from a branch" option)
3. Click **Save**

### Step 3: Commit and Push These Changes

```bash
cd /Users/anoopkansupada/India/India
git add .github/workflows/deploy.yml index.html DEPLOYMENT_SETUP.md
git commit -m "Add GitHub Actions deployment with secure API key handling"
git push origin main
```

### Step 4: Verify Deployment

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see a workflow running called "Deploy to GitHub Pages"
4. Wait for it to complete (usually 1-2 minutes)
5. Visit https://anoopkansupada.github.io/India/index.html
6. The map should now load!

## 🔍 Troubleshooting

### If the workflow fails:

1. **Check the Actions tab** for error messages
2. **Verify the secret name** is exactly `GOOGLE_MAPS_API_KEY` (case-sensitive)
3. **Check Pages settings** ensure Source is set to "GitHub Actions"

### If the map still doesn't load:

1. Open browser console (F12 → Console)
2. Look for errors:
   - `CONFIG is undefined` → Secret wasn't injected correctly
   - `RefererNotAllowedMapError` → Update API key restrictions (see below)

### Update API Key Restrictions

Make sure your Google Maps API key allows requests from GitHub Pages:

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/google/maps-apis/credentials)
2. Find your API key
3. Click Edit
4. Under **Application restrictions**:
   - Select **HTTP referrers (web sites)**
   - Add: `https://anoopkansupada.github.io/India/*`
   - Keep: `http://localhost/*` (for local testing)
5. Click **Save**

## 🚀 How It Works

### Local Development
- You have `config.js` on your machine (in .gitignore)
- Opening index.html locally loads your local config.js
- Map works perfectly

### GitHub Pages Deployment
- Push to main → GitHub Actions runs
- Workflow creates config.js with API key from Secrets
- Deploys everything to GitHub Pages
- config.js is NOT in your repo history (secure!)

## 🔐 Security Benefits

✅ API key never appears in Git history
✅ API key is encrypted in GitHub Secrets
✅ Only authorized workflows can access the secret
✅ Domain restrictions prevent unauthorized use
✅ Local config.js stays out of version control

## 📝 Future Updates

### To Update the API Key

If you need to rotate the API key:

1. Create new API key in Google Cloud Console
2. Go to GitHub repository → Settings → Secrets and variables → Actions
3. Click on `GOOGLE_MAPS_API_KEY`
4. Click **Update secret**
5. Paste new key and save
6. Next deployment will automatically use the new key

### To Deploy Changes

Just commit and push to main:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

The deployment happens automatically!

## ✅ Verification Checklist

After setup, verify:

- [ ] GitHub Secret `GOOGLE_MAPS_API_KEY` is created
- [ ] GitHub Pages Source is set to "GitHub Actions"
- [ ] Workflow completed successfully (green checkmark in Actions tab)
- [ ] Site is accessible at https://anoopkansupada.github.io/India/index.html
- [ ] Map loads without errors
- [ ] Browser console shows no API key errors
- [ ] Local development still works (opening index.html from disk)

## 🆘 Need Help?

- **GitHub Actions Logs**: Repository → Actions → Click on the workflow run
- **GitHub Pages Status**: Settings → Pages (shows deployment status)
- **Browser Console**: F12 → Console (shows JavaScript errors)

---

**Status**: Ready to deploy! Follow Steps 1-4 above to activate the deployment.
