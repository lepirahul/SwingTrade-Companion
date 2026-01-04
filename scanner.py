"""
SwingTrade Companion - Momentum Scanner
Phase 1: Volume Shocker Scanner for Nifty Smallcap 250
"""

from nsepython import nsefetch
import pandas as pd
from datetime import datetime, timedelta
import time


class MomentumScanner:
    """Scans Nifty Smallcap 250 for Volume Shocker stocks"""
    
    # Configuration - Adjusted for 5-10% weekly move potential
    VOLUME_MULTIPLIER = 2.5  # Current volume must be 2.5x average (shows interest)
    MIN_PRICE_GAIN_PCT = 1.0  # Minimum 1% price gain (positive momentum, room to grow)
    AVG_VOLUME_DAYS = 20  # Average volume over 20 days
    
    def __init__(self, test_mode=False, max_stocks=None):
        self.results = []
        self.test_mode = test_mode
        self.max_stocks = max_stocks if max_stocks else (10 if test_mode else None)
    
    def get_nifty_smallcap_250_symbols(self):
        """Fetch list of Nifty Smallcap 250 stocks"""
        try:
            # NSE API endpoint for Nifty Smallcap 250 index
            url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20SMALLCAP%20250"
            data = nsefetch(url)
            
            if data and 'data' in data:
                # Filter out the index itself (has priority=1 or contains "NIFTY" in symbol)
                # Only include actual stocks (have 'series' field or priority=0)
                symbols = []
                for stock in data['data']:
                    symbol = stock.get('symbol', '')
                    # Skip the index (contains "NIFTY" or doesn't have series field)
                    if 'NIFTY' not in symbol.upper() and stock.get('series'):
                        symbols.append(symbol)
                
                print(f"Found {len(symbols)} stocks in Nifty Smallcap 250")
                return symbols
            else:
                print("Warning: Could not fetch index data, using fallback method")
                return []
        except Exception as e:
            print(f"Error fetching index symbols: {e}")
            return []
    
    def get_historical_data(self, symbol, days=30):
        """Fetch historical OHLCV data for a symbol"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # NSE historical data endpoint
            url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}&series=[%22EQ%22]&from={start_date.strftime('%d-%m-%Y')}&to={end_date.strftime('%d-%m-%Y')}"
            data = nsefetch(url)
            
            if data and 'data' in data:
                return data['data']
            return []
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return []
    
    def calculate_volume_multiplier(self, historical_data):
        """Calculate volume multiplier (current volume / average volume)"""
        if not historical_data or len(historical_data) < self.AVG_VOLUME_DAYS:
            return 0
        
        # Get volumes (excluding today if it's the last entry)
        volumes = []
        for day in historical_data[-(self.AVG_VOLUME_DAYS + 1):-1]:
            try:
                vol = float(day.get('FH_TOTVOLUME', 0))
                volumes.append(vol)
            except (ValueError, TypeError):
                continue
        
        if not volumes or len(volumes) < self.AVG_VOLUME_DAYS:
            return 0
        
        avg_volume = sum(volumes) / len(volumes)
        current_volume = float(historical_data[-1].get('FH_TOTVOLUME', 0))
        
        if avg_volume == 0:
            return 0
        
        return current_volume / avg_volume
    
    def calculate_price_gain(self, historical_data):
        """Calculate price gain percentage for current session"""
        if not historical_data or len(historical_data) < 2:
            return 0
        
        try:
            prev_close = float(historical_data[-2].get('FH_CLOSEPRICE', 0))
            current_close = float(historical_data[-1].get('FH_CLOSEPRICE', 0))
            
            if prev_close == 0:
                return 0
            
            gain_pct = ((current_close - prev_close) / prev_close) * 100
            return gain_pct
        except (ValueError, TypeError, IndexError):
            return 0
    
    def scan_stock(self, symbol):
        """Scan a single stock for Volume Shocker criteria"""
        historical_data = self.get_historical_data(symbol)
        
        if not historical_data:
            return None
        
        volume_multiplier = self.calculate_volume_multiplier(historical_data)
        price_gain_pct = self.calculate_price_gain(historical_data)
        
        # Check Volume Shocker criteria
        is_volume_shocker = volume_multiplier >= self.VOLUME_MULTIPLIER
        is_price_gainer = price_gain_pct >= self.MIN_PRICE_GAIN_PCT
        
        if is_volume_shocker and is_price_gainer:
            current_price = float(historical_data[-1].get('FH_CLOSEPRICE', 0))
            current_volume = float(historical_data[-1].get('FH_TOTVOLUME', 0))
            
            return {
                'symbol': symbol,
                'price': current_price,
                'price_gain_pct': round(price_gain_pct, 2),
                'volume_multiplier': round(volume_multiplier, 2),
                'current_volume': int(current_volume)
            }
        
        return None
    
    def scan_all(self):
        """Scan Nifty Smallcap 250 stocks"""
        symbols = self.get_nifty_smallcap_250_symbols()
        
        if not symbols:
            print("No symbols found. Exiting.")
            return
        
        # Limit stocks if in test mode or max_stocks specified
        if self.max_stocks:
            symbols = symbols[:self.max_stocks]
            mode_text = f"TEST MODE - Scanning first {len(symbols)} stocks"
        else:
            mode_text = f"FULL SCAN - Scanning all {len(symbols)} stocks"
        
        print(f"\n{mode_text} for Volume Shockers...")
        print(f"Criteria: Volume >= {self.VOLUME_MULTIPLIER}x average, Price gain >= {self.MIN_PRICE_GAIN_PCT}%")
        print("-" * 60)
        
        self.results = []
        start_time = time.time()
        
        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{len(symbols)}] Scanning {symbol}...", end=' ', flush=True)
            
            try:
                result = self.scan_stock(symbol)
                if result:
                    self.results.append(result)
                    print(f"MATCH! (Vol: {result['volume_multiplier']}x, Gain: {result['price_gain_pct']}%)")
                else:
                    print("No match")
            except Exception as e:
                print(f"Error: {str(e)[:30]}")
            
            # Reduced delay for faster scanning (0.2s for test, 0.3s for full scan)
            delay = 0.2 if self.test_mode else 0.3
            time.sleep(delay)
        
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 60)
        print(f"Scan complete! Found {len(self.results)} Volume Shocker stocks in {elapsed_time:.1f}s")
        print("=" * 60)
    
    def save_results(self, filename='volume_shockers.csv'):
        """Save results to CSV file"""
        if not self.results:
            print("No results to save.")
            return
        
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"\nResults saved to {filename}")
    
    def display_results(self):
        """Display results in console"""
        if not self.results:
            print("\nNo Volume Shocker stocks found.")
            return
        
        print("\n" + "=" * 80)
        print("VOLUME SHOCKER STOCKS")
        print("=" * 80)
        print(f"{'Symbol':<15} {'Price':<12} {'Gain %':<10} {'Vol Mult':<12} {'Volume':<15}")
        print("-" * 80)
        
        for result in self.results:
            print(f"{result['symbol']:<15} ₹{result['price']:<11.2f} {result['price_gain_pct']:<10.2f} "
                  f"{result['volume_multiplier']:<12.2f} {result['current_volume']:<15,}")


def main(test_mode=True):
    """Main execution function"""
    print("SwingTrade Companion - Momentum Scanner")
    print("=" * 60)
    
    scanner = MomentumScanner(test_mode=test_mode)
    scanner.scan_all()
    scanner.display_results()
    scanner.save_results()


if __name__ == "__main__":
    import sys
    # Run in test mode by default (first 10 stocks)
    # To run full scan, call: python scanner.py --full
    test_mode = '--full' not in sys.argv
    main(test_mode=test_mode)

