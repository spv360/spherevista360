#!/usr/bin/env python3
"""
WordPress API - Update Homepage with Stock Tracker Header
Automatically updates the homepage (ID 2412) with the new stock tracker header
"""

import requests
import json
import getpass
from requests.auth import HTTPBasicAuth

def load_homepage_content():
    """Load the updated homepage content with stock tracker header"""
    try:
        with open('professional_homepage.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract content between <body> tags if present, otherwise use as-is
        import re
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if body_match:
            return body_match.group(1).strip()

        return content
    except Exception as e:
        print(f"❌ Error loading homepage content: {e}")
        return None

def update_homepage(auth, base_url="https://spherevista360.com"):
    """Update the homepage using WordPress REST API"""

    page_id = 2412  # Homepage ID
    url = f"{base_url}/wp-json/wp/v2/pages/{page_id}"

    # Load the updated content
    content = load_homepage_content()
    if not content:
        return False

    # Prepare the update data
    data = {
        'content': content,
        'status': 'publish'  # Keep it published
    }

    try:
        response = requests.post(url, json=data, auth=auth)

        if response.status_code == 200:
            page_data = response.json()
            title = page_data.get('title', {}).get('rendered', 'Unknown')
            print(f"✅ Successfully updated: {title}")
            print(f"🔗 View at: {base_url}/")
            return True
        else:
            print(f"❌ Failed to update homepage {page_id}: {response.status_code}")
            print(f"   Response: {response.text[:500]}...")
            return False

    except Exception as e:
        print(f"❌ Error updating homepage {page_id}: {e}")
        return False

def main():
    print("🏠 WORDPRESS API - UPDATE HOMEPAGE WITH STOCK TRACKER HEADER")
    print("=" * 60)
    print()

    # Check if updated content exists
    content = load_homepage_content()
    if not content:
        print("❌ Updated homepage content not found!")
        return

    print("✅ Updated homepage content loaded successfully")
    print(f"   Size: {len(content)} characters")
    print()

    # Get WordPress credentials
    username = input("WordPress Username: ").strip()
    if not username:
        username = "JK"  # From previous successful auth

    password = getpass.getpass("WordPress Password: ")

    if not password:
        print("❌ Password is required!")
        return

    # Setup authentication
    auth = HTTPBasicAuth(username, password)

    print()
    print("🔄 Updating homepage (ID 2412) with stock tracker header...")
    print()

    # Confirm before proceeding
    confirm = "yes"  # Auto-confirm for testing
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return

    print()

    # Update the page
    if update_homepage(auth):
        print()
        print("🎉 HOMEPAGE UPDATED SUCCESSFULLY WITH STOCK TRACKER HEADER!")
        print()
        print("🎯 NEW FEATURES ADDED:")
        print("• 📈 Live Stock Tracker Header at the top")
        print("• 🏢 Professional blue gradient design")
        print("• 📊 Real-time stock prices (SPY, QQQ, AAPL, MSFT)")
        print("• 🟢/🔴 Market status indicator")
        print("• 📱 Responsive design for all devices")
        print("• 🔄 Auto-updates every 5 minutes")
        print()
        print("🔄 NEXT STEPS:")
        print("1. Visit: https://spherevista360.com/")
        print("2. Verify stock tracker header is visible at the top")
        print("3. Clear WordPress cache if needed")
        print("4. Test on mobile devices")
        print()
        print("💡 STOCK TRACKER FEATURES:")
        print("• Shows live prices for major stocks and ETFs")
        print("• Color-coded gains/losses (green/red)")
        print("• Market open/closed status")
        print("• Fallback to mock data if API unavailable")
        print("• Updates automatically every 5 minutes")
    else:
        print()
        print("❌ UPDATE FAILED")
        print("You may need to update the homepage manually:")
        print("• Go to WordPress Admin → Pages → Edit page 2412")
        print("• Replace content with professional_homepage.html")
        print("• Save and publish the page")

if __name__ == "__main__":
    main()