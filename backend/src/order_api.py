"""
Simple HTTP server to serve latest order to frontend
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from pathlib import Path
import threading

ORDERS_FILE = Path(__file__).parent.parent / "orders.json"

class OrderHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/latest-order':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                if ORDERS_FILE.exists():
                    with open(ORDERS_FILE, 'r') as f:
                        orders = json.load(f)
                        if orders and len(orders) > 0:
                            latest_order = orders[-1]
                            # Remove timestamp for frontend
                            if 'timestamp' in latest_order:
                                del latest_order['timestamp']
                            self.wfile.write(json.dumps(latest_order).encode())
                        else:
                            self.wfile.write(json.dumps({}).encode())
                else:
                    self.wfile.write(json.dumps({}).encode())
            except Exception as e:
                print(f"Error reading orders: {e}")
                self.wfile.write(json.dumps({}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress logging
        pass

def start_order_server(port=8082):
    """Start HTTP server in background thread"""
    server = HTTPServer(('localhost', port), OrderHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Order API server started on http://localhost:{port}")
    return server
