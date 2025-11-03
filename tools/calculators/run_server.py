#!/usr/bin/env python3
"""
SIP Calculator Web Server
Serves the US Stock Market SIP Calculator as a local web application
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class SIPCalculatorHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for SIP Calculator with proper MIME types"""

    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Serve index.html for root requests
        if self.path == '/' or self.path == '/index.html':
            self.path = '/sip_calculator.html'
        return super().do_GET()

def run_server(port=8000, open_browser=True):
    """Run the SIP Calculator web server"""

    # Change to the calculators directory
    calculator_dir = Path(__file__).parent
    os.chdir(calculator_dir)

    # Create server
    with socketserver.TCPServer(("", port), SIPCalculatorHandler) as httpd:
        server_url = f"http://localhost:{port}"

        print("🚀 US Stock Market SIP Calculator")
        print("=" * 50)
        print(f"📊 Server started at: {server_url}")
        print("📈 Open your browser to start calculating!")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)

        # Open browser automatically
        if open_browser:
            try:
                webbrowser.open(server_url)
                print("🌐 Browser opened automatically")
            except:
                print("💡 Please open your browser and navigate to the URL above")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Thank you for using SIP Calculator!")
            httpd.shutdown()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run SIP Calculator Web Server')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Port to run server on (default: 8000)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')

    args = parser.parse_args()

    try:
        run_server(port=args.port, open_browser=not args.no_browser)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {args.port} is already in use. Try a different port:")
            print(f"   python3 {sys.argv[0]} --port {args.port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)