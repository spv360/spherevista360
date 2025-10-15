#!/usr/bin/env python3
"""
Configure WordPress using direct database approach
This uses WordPress REST API with admin credentials
"""

import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = 'SphereVista360'  # Admin username
ADMIN_PASSWORD = os.getenv('WORDPRESS_ADMIN_PASSWORD', 'SphereV360@2024')

def test_admin_auth():
    """Test admin authentication"""
    print("🔐 Testing admin authentication...")
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/users/me"
    
    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, ADMIN_PASSWORD)
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Authenticated as: {data.get('name', 'Unknown')}")
        print(f"   Capabilities: {list(data.get('capabilities', {}).keys())[:5]}...")
        return True
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def update_settings_with_admin():
    """Update WordPress settings using admin credentials"""
    print("\n⚙️  Updating WordPress settings...")
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
    
    # Get Homepage and Blog page IDs
    pages_url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages?search=Homepage"
    response = requests.get(pages_url, auth=HTTPBasicAuth(USERNAME, ADMIN_PASSWORD))
    homepage_id = response.json()[0]['id'] if response.status_code == 200 and response.json() else None
    
    pages_url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages?search=Blog"
    response = requests.get(pages_url, auth=HTTPBasicAuth(USERNAME, ADMIN_PASSWORD))
    blog_id = response.json()[0]['id'] if response.status_code == 200 and response.json() else None
    
    if not homepage_id:
        print("❌ Could not find Homepage")
        return False
    
    print(f"   Found Homepage (ID: {homepage_id})")
    print(f"   Found Blog (ID: {blog_id})")
    
    # Update settings
    data = {
        'title': 'SphereVista360',
        'description': 'Your 360° View on Global Insights - Finance, Technology & Innovation',
        'show_on_front': 'page',
        'page_on_front': homepage_id,
    }
    
    if blog_id:
        data['page_for_posts'] = blog_id
    
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, ADMIN_PASSWORD)
    )
    
    if response.status_code == 200:
        print("✅ Settings updated successfully!")
        return True
    else:
        print(f"❌ Failed to update settings: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    print("=" * 60)
    print("🔧 WordPress Configuration with Admin Credentials")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 Admin User: {USERNAME}")
    print("=" * 60)
    
    # Test authentication
    if not test_admin_auth():
        print("\n❌ Admin authentication failed!")
        print("   Make sure WORDPRESS_ADMIN_PASSWORD is correct in .env")
        return
    
    # Update settings
    update_settings_with_admin()
    
    print("\n" + "=" * 60)
    print("📋 Manual Menu Configuration Needed")
    print("=" * 60)
    print(f"\n🧭 Configure Navigation Menu (2 minutes):")
    print(f"   1. Go to: {WORDPRESS_URL}/wp-admin/nav-menus.php")
    print(f"   2. Login with:")
    print(f"      Username: {USERNAME}")
    print(f"      Password: {ADMIN_PASSWORD}")
    print(f"   3. Select 'Main Menu' (or create new)")
    print(f"   4. Add pages: Homepage, About, Services, Contact")
    print(f"   5. Check 'Primary Menu' location")
    print(f"   6. Click 'Save Menu'")
    print("\n" + "=" * 60)
    print(f"\n🌐 Then visit: {WORDPRESS_URL}")
    print("=" * 60)

if __name__ == "__main__":
    main()
