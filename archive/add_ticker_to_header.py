#!/usr/bin/env python3
"""
Add stock ticker JavaScript to WordPress header via Kadence theme customizer
"""
import requests
import json
import os

# WordPress credentials
WP_URL = "https://spherevista360.com"
WP_USER = "jkudale93@gmail.com"
WP_APP_PASSWORD = "hC0w vL6R k6T1 TdeL xmLF f4s8"

# Read the ticker code
with open('stock_ticker_code.html', 'r') as f:
    ticker_code = f.read()

# Try to add via theme customizer or custom code
def add_to_header():
    """Add ticker code to WordPress header"""
    
    # Method 1: Try adding via theme mod (Kadence customizer)
    endpoint = f"{WP_URL}/wp-json/wp/v2/settings"
    
    auth = (WP_USER, WP_APP_PASSWORD)
    
    # First, let's check current settings
    response = requests.get(endpoint, auth=auth)
    if response.status_code == 200:
        print("✅ Connected to WordPress API")
        current_settings = response.json()
        print(f"Current site title: {current_settings.get('title', 'N/A')}")
    else:
        print(f"❌ Failed to connect: {response.status_code}")
        print(response.text)
        return
    
    print("\n" + "="*60)
    print("MANUAL INSTALLATION REQUIRED")
    print("="*60)
    print("\nTo add the stock ticker to your header:")
    print("\n1. Go to: WordPress Admin → Appearance → Customize")
    print("2. Look for 'Additional Scripts' or 'Header Scripts' section")
    print("3. Or go to: Appearance → Theme File Editor")
    print("4. Edit header.php and add this code before </head>:")
    print("\n" + "="*60)
    print(ticker_code)
    print("="*60)
    print("\n✅ Code is ready to paste!")
    
    # Save to a simpler file for easy copy-paste
    with open('ticker_for_header.txt', 'w') as f:
        f.write(ticker_code)
    
    print("\n📄 Also saved to: ticker_for_header.txt")

if __name__ == '__main__':
    add_to_header()
