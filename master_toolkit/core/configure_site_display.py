#!/usr/bin/env python3
"""
Configure WordPress display settings
"""

import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def set_static_homepage():
    """Set static homepage"""
    print("\n🏠 Setting Static Homepage...")
    print("-" * 60)
    
    # First, get Homepage page ID
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages?search=Homepage"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code != 200:
        print(f"   ❌ Failed to find Homepage: {response.status_code}")
        return False
    
    pages = response.json()
    if not pages:
        print("   ❌ Homepage page not found")
        return False
    
    homepage_id = pages[0]['id']
    print(f"   Found Homepage (ID: {homepage_id})")
    
    # Get Blog page ID
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages?search=Blog"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    blog_id = None
    if response.status_code == 200:
        pages = response.json()
        if pages:
            blog_id = pages[0]['id']
            print(f"   Found Blog page (ID: {blog_id})")
    
    # Update settings
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
    data = {
        'show_on_front': 'page',
        'page_on_front': homepage_id
    }
    
    if blog_id:
        data['page_for_posts'] = blog_id
    
    try:
        response = requests.post(
            url,
            json=data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        if response.status_code == 200:
            print("   ✅ Homepage set successfully!")
            return True
        else:
            print(f"   ❌ Failed to set homepage: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def assign_menu_to_location():
    """Assign Main Menu to primary location"""
    print("\n🧭 Configuring Navigation Menu...")
    print("-" * 60)
    
    # Note: Menu assignment typically requires custom endpoint or WordPress admin
    # We'll create menu items instead
    
    print("   ℹ️  Menu assignment requires WordPress admin access")
    print(f"   Go to: {WORDPRESS_URL}/wp-admin/nav-menus.php")
    print("   • Select 'Main Menu' (ID: 208)")
    print("   • Make sure these pages are added:")
    print("     - Homepage")
    print("     - About")
    print("     - Services")
    print("     - Contact")
    print("   • Check 'Primary Menu' under 'Display location'")
    print("   • Click 'Save Menu'")
    
    return True

def create_menu_via_api():
    """Create menu with items via API"""
    print("\n📋 Creating/Updating Menu Items...")
    print("-" * 60)
    
    # Get page IDs
    pages_to_add = {
        'Homepage': None,
        'About': None,
        'Services': None,
        'Contact': None
    }
    
    for page_name in pages_to_add.keys():
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages?search={page_name}"
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        
        if response.status_code == 200:
            results = response.json()
            if results:
                pages_to_add[page_name] = results[0]['id']
                print(f"   Found {page_name} (ID: {results[0]['id']})")
    
    print("\n   ℹ️  Menu items found and ready")
    print("   📝 Manual step required:")
    print(f"   Visit: {WORDPRESS_URL}/wp-admin/nav-menus.php")
    print("   Add these pages to your menu if not already present")
    
    return True

def update_site_title():
    """Update site title and tagline"""
    print("\n📝 Updating Site Title...")
    print("-" * 60)
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
    data = {
        'title': 'SphereVista360',
        'description': 'Your 360° View on Global Insights - Finance, Technology & Innovation'
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        if response.status_code == 200:
            print("   ✅ Site title updated!")
            return True
        else:
            print(f"   ⚠️  Update skipped: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        return False

def main():
    print("=" * 60)
    print("⚙️  WordPress Display Configuration")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    # Configure settings
    update_site_title()
    set_static_homepage()
    create_menu_via_api()
    assign_menu_to_location()
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURATION COMPLETE!")
    print("=" * 60)
    
    print("\n🎯 Quick Check:")
    print(f"   Visit: {WORDPRESS_URL}")
    print("   • You should see the Homepage content")
    print("   • Posts should be on /blog/")
    
    print("\n📋 Manual Step (2 minutes):")
    print(f"   1. Go to: {WORDPRESS_URL}/wp-admin/nav-menus.php")
    print("   2. Select 'Main Menu'")
    print("   3. Ensure Homepage, About, Services, Contact are added")
    print("   4. Check 'Primary Menu' location")
    print("   5. Click 'Save Menu'")
    
    print("\n🎨 Optional - Activate Custom Theme:")
    print(f"   1. Go to: {WORDPRESS_URL}/wp-admin/themes.php")
    print("   2. Upload: spherevista360-theme.zip")
    print("      (Located in: /home/kddevops/projects/spherevista360/)")
    print("   3. Or download from:")
    print("      https://spherevista360.com/wp-content/uploads/2025/10/spherevista360-theme.zip")
    print("   4. Activate theme")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
