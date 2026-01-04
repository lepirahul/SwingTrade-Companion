# Deployment Guide - SwingTrade Companion

## Platform Comparison

| Feature | Railway | Render |
|---------|---------|--------|
| Free Tier | ✅ Yes ($5 credit/month) | ✅ Yes (Limited hours) |
| Auto-Deploy | ✅ From GitHub | ✅ From GitHub |
| HTTPS/SSL | ✅ Automatic | ✅ Automatic |
| Setup Time | ~5 minutes | ~5 minutes |
| Credit Card Required | ❌ No | ❌ No |
| Data Security | ✅ Excellent | ✅ Excellent |

**Recommendation:** Railway (easier setup, better free tier)

---

## Option 1: Railway Deployment (Recommended)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended - easier integration)

### Step 2: Deploy from GitHub
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Authorize Railway to access your GitHub
4. Select repository: `lepirahul/SwingTrade-Companion`
5. Railway automatically detects Python and starts deploying

### Step 3: Configure (Optional)
Railway auto-detects:
- ✅ Python runtime
- ✅ Dependencies (from requirements.txt)
- ✅ Start command (from Procfile)

**No configuration needed** - it should work automatically!

### Step 4: Get Your URL
1. After deployment completes (2-3 minutes)
2. Click on your service
3. Click "Settings" tab
4. Under "Domains" section, you'll see your URL
   - Example: `https://swingtrade-companion-production.up.railway.app`
5. Click "Generate Domain" for a custom subdomain (optional)

### Step 5: Access Your App
- Open the URL in any browser (desktop or mobile)
- No restrictions - works from anywhere!

---

## Option 2: Render Deployment

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub account (if not already)
3. Select repository: `SwingTrade-Companion`
4. Click "Connect"

### Step 3: Configure Settings
- **Name:** `swingtrade-companion` (or your choice)
- **Region:** Choose closest to you (e.g., Singapore for India)
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`
- **Plan:** Free (or paid if needed)

### Step 4: Deploy
1. Click "Create Web Service"
2. Render will build and deploy (3-5 minutes)
3. Watch the logs for progress

### Step 5: Get Your URL
- Your app URL will be: `https://swingtrade-companion.onrender.com`
- Or custom domain if you configure one

---

## Verification Checklist

After deployment, verify:

- [ ] App loads at the URL
- [ ] Test scan button works
- [ ] Progress bar shows during scan
- [ ] Results display correctly
- [ ] Mobile browser works (test on phone)
- [ ] HTTPS is enabled (URL starts with https://)

---

## Troubleshooting

### Deployment Fails

**Error: "Build failed"**
- Check that `requirements.txt` has all dependencies
- Check build logs for specific error

**Error: "Application error"**
- Check that `Procfile` exists and is correct
- Verify `app.py` runs locally first
- Check application logs in platform dashboard

### App Works But Scans Fail

**No results found:**
- This is normal if markets are closed or no stocks meet criteria
- Test on a trading day during market hours
- Verify NSE APIs are accessible

### Connection Timeout

**Render free tier:**
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- Consider paid plan for always-on service

**Railway free tier:**
- More reliable, less sleeping
- Better for always-available service

---

## Updating Your App

After making code changes:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

2. **Platform auto-deploys:**
   - Railway: Auto-deploys within 1-2 minutes
   - Render: Auto-deploys within 2-3 minutes

3. **Check deployment status:**
   - Railway: Check "Deployments" tab
   - Render: Check "Events" tab

---

## Environment Variables (Future Use)

If you need to add API keys later:

### Railway:
1. Go to Service → Variables tab
2. Add key-value pairs
3. Access in code: `os.environ.get('YOUR_KEY')`

### Render:
1. Go to Service → Environment tab
2. Add key-value pairs
3. Access in code: `os.environ.get('YOUR_KEY')`

**Note:** Currently not needed - your app uses public APIs only.

---

## Security Notes

✅ **Safe to Deploy:**
- No sensitive credentials in code
- Only public stock data
- HTTPS enabled automatically
- No user data stored

See `SECURITY.md` for detailed security analysis.

---

## Support

- **Railway Docs:** https://docs.railway.app
- **Render Docs:** https://render.com/docs
- **GitHub Issues:** Create issue in your repository

