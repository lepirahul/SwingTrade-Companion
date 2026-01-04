# SwingTrade Companion - High Momentum Edition

A Python-based scanner for identifying high-volatility, high-momentum swing trades in NSE Small-Cap stocks.

## Phase 1: Momentum Scanner (Current)

Scans Nifty Smallcap 250 stocks to identify "Volume Shocker" candidates:
- **Volume Criterion:** Current volume >= 2.5x average 20-day volume
- **Price Criterion:** Price gain >= 1.0% in current session
- **Target:** Stocks with 5-10% weekly move potential

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Command Line Scanner

Run the scanner from command line:
```bash
python scanner.py          # Test mode (10 stocks)
python scanner.py --full   # Full scan (249 stocks)
```

Results are displayed in console and saved to `volume_shockers.csv`

### Option 2: Web Interface (Mobile-Friendly)

#### Local Deployment:

Run the web server locally:
```bash
python app.py
```

Then access at: http://localhost:5000

#### Cloud Deployment (Recommended for Mobile Access):

Deploy to cloud for access from anywhere on any device.

**Option A: Railway (Recommended - Free Tier Available)**

1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI (optional, or use web interface):
   ```bash
   npm i -g @railway/cli
   ```
3. Deploy:
   ```bash
   railway login
   railway init
   railway up
   ```
4. Or use Railway's GitHub integration:
   - Push code to GitHub
   - Connect GitHub repo in Railway dashboard
   - Railway auto-deploys

**Option B: Render (Free Tier Available)**

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new "Web Service"
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Deploy

**Option C: Heroku (Requires Credit Card for Free Tier)**

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

After deployment, you'll get a public URL like:
- `https://your-app.railway.app`
- `https://your-app.onrender.com`

Access this URL from any device, anywhere!

#### Web Interface Features:
- 🧪 Test Scan: Quick scan of 10 stocks
- ⚡ Medium Scan: Scan 50 stocks
- 🚀 Full Scan: Complete scan of all 249 stocks
- Real-time progress tracking
- Mobile-optimized responsive design
- Access from anywhere (cloud deployment)

## Configuration

Edit `scanner.py` to modify:
- `VOLUME_MULTIPLIER`: Volume threshold (default: 2.5)
- `MIN_PRICE_GAIN_PCT`: Minimum price gain % (default: 1.0)
- `AVG_VOLUME_DAYS`: Days for average volume calculation (default: 20)

