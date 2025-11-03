#!/usr/bin/env python3
"""
WordPress API - Update Retirement Planner Page
Automatically updates the retirement planner page (ID 3173) with fixed content
"""

import requests
import json
import getpass
from requests.auth import HTTPBasicAuth

def load_fixed_content():
    """Load the fixed retirement planner content"""
    try:
        with open('retirement-planner-fixed.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract content between <body> tags
        import re
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if body_match:
            return body_match.group(1).strip()

        return content
    except Exception as e:
        print(f"❌ Error loading fixed content: {e}")
        return None

def update_retirement_planner(auth, base_url="https://spherevista360.com"):
    """Update the retirement planner page using WordPress REST API"""

    page_id = 3173  # Retirement Planner page ID
    url = f"{base_url}/wp-json/wp/v2/pages/{page_id}"

    # Load the fixed content
    content = load_fixed_content()
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
            print(f"🔗 View at: {base_url}/retirement-planner-estimator/")
            return True
        else:
            print(f"❌ Failed to update page {page_id}: {response.status_code}")
            print(f"   Response: {response.text[:500]}...")
            return False

    except Exception as e:
        print(f"❌ Error updating page {page_id}: {e}")
        return False

def main():
    print("🏖️ WORDPRESS API - UPDATE RETIREMENT PLANNER")
    print("=" * 50)
    print()

    # Check if fixed content exists
    content = load_fixed_content()
    if not content:
        print("❌ Fixed content not found!")
        return

    print("✅ Fixed content loaded successfully")
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
    print("🔄 Updating retirement planner page (ID 3173)...")
    print()

    # Confirm before proceeding
    confirm = input("Update retirement planner page? (yes/no): ").lower().strip()
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return

    print()

    # Update the page
    if update_retirement_planner(auth):
        print()
        print("🎉 RETIREMENT PLANNER UPDATED SUCCESSFULLY!")
        print()
        print("🎯 EXPECTED IMPROVEMENTS:")
        print("• ✅ Aligned form labels with icons")
        print("• ✅ Horizontal button layout")
        print("• ✅ Interactive data displays")
        print("• ✅ Progress bars and charts")
        print("• ✅ No JavaScript console errors")
        print("• ✅ Mobile responsive design")
        print()
        print("🔄 NEXT STEPS:")
        print("1. Visit: https://spherevista360.com/retirement-planner-estimator/")
        print("2. Test the calculator functionality")
        print("3. Clear WordPress cache")
        print("4. Verify all other calculators still work")
    else:
        print()
        print("❌ UPDATE FAILED")
        print("You may need to update the page manually:")
        print("• Run: python3 update_retirement_planner.py (for manual instructions)")
        print("• Or update via WordPress Admin → Pages → Edit page 3173")

if __name__ == "__main__":
    main()