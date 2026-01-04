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

**Quick Start - Railway (Recommended):**

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `lepirahul/SwingTrade-Companion`
4. Railway auto-deploys (takes 2-3 minutes)
5. Get your URL from the dashboard

**Quick Start - Render:**

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect repository: `SwingTrade-Companion`
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Click "Create Web Service"

After deployment, you'll get a public URL like:
- `https://your-app.railway.app` (Railway)
- `https://your-app.onrender.com` (Render)

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

