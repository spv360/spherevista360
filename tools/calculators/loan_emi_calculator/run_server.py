#!/usr/bin/env python3
"""
Simple HTTP server to serve the Loan EMI Calculator web interface.
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import unquote
import json
from loan_emi_calculator import LoanEMICalculator


class LoanEMICalculatorHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for the Loan EMI Calculator"""

    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        self.calculator = LoanEMICalculator()
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Serve the main HTML file
            self.path = '/loan_emi_calculator.html'
            return super().do_GET()
        elif self.path.startswith('/api/'):
            # Handle API requests
            self.handle_api_request()
        else:
            # Serve static files normally
            return super().do_GET()

    def do_POST(self):
        """Handle POST requests for API calls"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404, "Not Found")

    def handle_api_request(self):
        """Handle API requests for calculations"""
        try:
            if self.path == '/api/calculate-emi':
                self.handle_calculate_emi()
            elif self.path == '/api/calculate-eligibility':
                self.handle_calculate_eligibility()
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def handle_calculate_emi(self):
        """Handle EMI calculation API request"""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract parameters
            loan_amount = float(data.get('loan_amount', 0))
            interest_rate = float(data.get('interest_rate', 0)) / 100  # Convert to decimal
            tenure_years = int(data.get('tenure_years', 0))
            tenure_months = int(data.get('tenure_months', 0))

            # Validate inputs
            if loan_amount <= 0 or interest_rate <= 0 or tenure_years < 0:
                self.send_json_response({'error': 'Invalid input parameters'}, 400)
                return

            # Calculate EMI
            results = self.calculator.calculate_emi(loan_amount, interest_rate, tenure_years, tenure_months)

            # Convert to JSON-serializable format
            response_data = {
                'loan_amount': results['loan_amount'],
                'annual_rate': results['annual_rate'] * 100,  # Convert back to percentage
                'tenure_years': results['tenure_years'],
                'tenure_months': results['tenure_months'],
                'total_months': results['total_months'],
                'monthly_emi': round(results['monthly_emi'], 2),
                'total_amount': round(results['total_amount'], 2),
                'total_interest': round(results['total_interest'], 2),
                'interest_percentage': round(results['interest_percentage'], 2),
                'amortization_schedule': [
                    {
                        'month': payment['month'],
                        'emi': round(payment['emi'], 2),
                        'interest_payment': round(payment['interest_payment'], 2),
                        'principal_payment': round(payment['principal_payment'], 2),
                        'remaining_balance': round(payment['remaining_balance'], 2)
                    }
                    for payment in results['amortization_schedule']
                ]
            }

            self.send_json_response(response_data)

        except (ValueError, KeyError) as e:
            self.send_json_response({'error': f'Invalid input: {str(e)}'}, 400)
        except Exception as e:
            self.send_json_response({'error': f'Calculation error: {str(e)}'}, 500)

    def handle_calculate_eligibility(self):
        """Handle loan eligibility calculation API request"""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract parameters
            monthly_income = float(data.get('monthly_income', 0))
            existing_obligations = float(data.get('existing_obligations', 0))
            max_emi_percentage = float(data.get('max_emi_percentage', 50)) / 100  # Convert to decimal

            # Validate inputs
            if monthly_income <= 0:
                self.send_json_response({'error': 'Invalid monthly income'}, 400)
                return

            # Calculate eligibility
            results = self.calculator.calculate_loan_eligibility(
                monthly_income, existing_obligations, max_emi_percentage
            )

            # Convert to JSON-serializable format
            response_data = {
                'monthly_income': results['monthly_income'],
                'existing_obligations': results['existing_obligations'],
                'max_emi_percentage': results['max_emi_percentage'] * 100,  # Convert back to percentage
                'max_monthly_emi': round(results['max_monthly_emi'], 2),
                'available_emi': round(results['available_emi'], 2),
                'scenarios': [
                    {
                        'rate': round(scenario['rate'] * 100, 1),  # Convert back to percentage
                        'tenure': scenario['tenure'],
                        'max_loan': round(scenario['max_loan'], 2),
                        'monthly_emi': round(scenario['monthly_emi'], 2)
                    }
                    for scenario in results['scenarios']
                ]
            }

            self.send_json_response(response_data)

        except (ValueError, KeyError) as e:
            self.send_json_response({'error': f'Invalid input: {str(e)}'}, 400)
        except Exception as e:
            self.send_json_response({'error': f'Calculation error: {str(e)}'}, 500)

    def send_json_response(self, data, status_code=200):
        """Send a JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        json_response = json.dumps(data, indent=2)
        self.wfile.write(json_response.encode('utf-8'))

    def log_message(self, format, *args):
        """Override logging to be less verbose"""
        if "GET /api/" in format or "POST /api/" in format:
            # Log API requests
            super().log_message(format, *args)
        # Suppress favicon and other static file requests


def run_server(port=8000, open_browser=True):
    """Run the web server"""
    try:
        with socketserver.TCPServer(("", port), LoanEMICalculatorHandler) as httpd:
            print(f"🚀 Loan EMI Calculator server started!")
            print(f"📱 Open your browser to: http://localhost:{port}")
            print(f"🔄 Server running... Press Ctrl+C to stop")

            if open_browser:
                try:
                    webbrowser.open(f"http://localhost:{port}")
                except Exception as e:
                    print(f"Could not open browser automatically: {e}")

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Loan EMI Calculator Web Server")
    parser.add_argument('--port', type=int, default=8000, help='Port to run server on (default: 8000)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')

    args = parser.parse_args()

    run_server(port=args.port, open_browser=not args.no_browser)