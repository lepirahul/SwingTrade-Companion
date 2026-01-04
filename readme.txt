# Project Description: SwingTrade Companion (STC) - High Momentum Edition

## 1. Project Overview
The **SwingTrade Companion** is a Python-based desktop application designed to identify high-volatility, high-momentum swing trades. It specifically targets **Small-Cap stocks** capable of significant short-term moves (target 5-10% weekly) by combining broad NSE market scans with deep technical validation via the Zerodha Kite API.

## 2. Core Objectives
* **Momentum Discovery:** Identify stocks with sudden "Volume Shocks" indicating institutional interest.
* **Small-Cap Focus:** Specifically scan the Nifty Smallcap 250 universe.
* **Explosive Setups:** Detect "VCP" (Volatility Contraction) and 52-Week High breakouts.
* **Risk Management:** Automated stop-loss and position sizing to protect against small-cap volatility.

---

## 3. The "Explosive Move" Funnel



### A. Stage 1: The Volume Shocker (nsepython)
* **Universe:** Nifty Smallcap 250.
* **Logic:** Identify stocks where `Current Volume > (5x Average 20-Day Volume)`.
* **Price Action:** Filter for stocks with a >3% gain in a single session to confirm "active" momentum.

### B. Stage 2: Technical Confirmation (Kite API)
* **Breakout Detection:** Check if the stock is within 2% of its 52-Week High.
* **Relative Strength (RS):** Compare stock performance against Nifty 50. If Nifty is sideways and the Small-cap is rising, it has high RS.
* **Support/Resistance:** Automate the detection of "Tight Bases" where price has consolidated before a move.

### C. Stage 3: Fundamental & News Safety
* **Quality Check:** Screen for `Promoter Pledging < 10%` and `Positive Quarterly Profit`.
* **News Sentiment:** Scrape for contract wins, earnings surprises, or sector-specific tailwinds.

---

## 4. Ranking & Selection Logic (The "10% Target" Score)
The app calculates a **Momentum Score ($M$):**

$$M = (0.5 \times Vol\_Multiplier) + (0.3 \times Dist\_From\_52W\_High) + (0.2 \times Relative\_Strength)$$

**Criteria for Top Picks:**
1. **Vol_Multiplier:** Higher is better (indicates "Smart Money" entry).
2. **Dist_From_52W_High:** Stocks breaking new highs have no "overhead supply" (sellers).
3. **Relative Strength:** Must be outperforming the benchmark index.

---

## 5. Feature Roadmap

| Phase | Milestone | Key Deliverables |
| :--- | :--- | :--- |
| **Phase 1** | Momentum Scraper | `nsepython` script to find daily volume/price gainers. |
| **Phase 2** | Kite Validation | Download 15-min and Daily OHLC to verify "Tightness" of price. |
| **Phase 3** | Sentiment Engine | News scraper focused on Small-cap corporate announcements. |
| **Phase 4** | Dashboard | PyQt6 UI showing a "Heatmap" of trending small-cap sectors. |
| **Phase 5** | Risk Module | Fixed 3% Stop-Loss and Target 10% Profit calculator. |

---

## 6. Technical Requirements
* **Libraries:** `nsepython`, `kiteconnect`, `pandas_ta`, `PyQt6`, `vaderSentiment`.
* **Data Sources:** NSE (Bhavcopy), Zerodha (Live Tick/Historical).