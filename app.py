"""
SwingTrade Companion - Web Interface
Simple Flask web app for mobile access to the momentum scanner
"""

from flask import Flask, render_template, jsonify, request
from scanner import MomentumScanner
import threading
import time

app = Flask(__name__)

# Global variables for scan status
scan_status = {
    'running': False,
    'progress': 0,
    'total': 0,
    'results': [],
    'error': None,
    'start_time': None,
    'end_time': None
}

scanner_instance = None
scan_thread = None


def run_scan(max_stocks=None):
    """Run scan in background thread"""
    global scan_status, scanner_instance
    
    try:
        scan_status['running'] = True
        scan_status['error'] = None
        scan_status['results'] = []
        scan_status['start_time'] = time.time()
        
        scanner = MomentumScanner(test_mode=False, max_stocks=max_stocks)
        scanner_instance = scanner
        
        symbols = scanner.get_nifty_smallcap_250_symbols()
        if not symbols:
            scan_status['error'] = "No symbols found"
            scan_status['running'] = False
            return
        
        if max_stocks:
            symbols = symbols[:max_stocks]
        
        scan_status['total'] = len(symbols)
        scan_status['progress'] = 0
        
        scanner.results = []
        
        for i, symbol in enumerate(symbols, 1):
            if not scan_status['running']:  # Allow cancellation
                break
            
            scan_status['progress'] = i
            result = scanner.scan_stock(symbol)
            if result:
                scanner.results.append(result)
            
            time.sleep(0.3)  # Delay between requests
        
        scan_status['results'] = scanner.results
        scan_status['end_time'] = time.time()
        
    except Exception as e:
        scan_status['error'] = str(e)
    finally:
        scan_status['running'] = False


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/scan', methods=['POST'])
def start_scan():
    """Start a new scan"""
    global scan_thread, scan_status
    
    if scan_status['running']:
        return jsonify({'error': 'Scan already running'}), 400
    
    data = request.get_json() or {}
    scan_type = data.get('type', 'test')  # test, medium, full
    
    max_stocks = None
    if scan_type == 'test':
        max_stocks = 10
    elif scan_type == 'medium':
        max_stocks = 50
    elif scan_type == 'full':
        max_stocks = None  # All stocks
    
    # Reset status
    scan_status = {
        'running': False,
        'progress': 0,
        'total': 0,
        'results': [],
        'error': None,
        'start_time': None,
        'end_time': None
    }
    
    # Start scan in background thread
    scan_thread = threading.Thread(target=run_scan, args=(max_stocks,))
    scan_thread.daemon = True
    scan_thread.start()
    
    return jsonify({'message': 'Scan started', 'type': scan_type})


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current scan status"""
    elapsed = None
    if scan_status['start_time']:
        end = scan_status['end_time'] or time.time()
        elapsed = round(end - scan_status['start_time'], 1)
    
    return jsonify({
        'running': scan_status['running'],
        'progress': scan_status['progress'],
        'total': scan_status['total'],
        'results': scan_status['results'],
        'error': scan_status['error'],
        'elapsed': elapsed
    })


@app.route('/api/stop', methods=['POST'])
def stop_scan():
    """Stop current scan"""
    global scan_status
    scan_status['running'] = False
    return jsonify({'message': 'Scan stopped'})


if __name__ == '__main__':
    import os
    
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("SwingTrade Companion - Web Interface")
    print("=" * 60)
    print(f"\nServer starting on port {port}")
    print(f"Access at: http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)

