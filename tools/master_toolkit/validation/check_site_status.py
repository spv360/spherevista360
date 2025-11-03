#!/usr/bin/env python3
"""
Check WordPress site status and content
"""

import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def check_pages():
    """Check all pages"""
    print("\n📄 Checking Pages...")
    print("-" * 60)
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code == 200:
        pages = response.json()
        print(f"   Total pages: {len(pages)}")
        for page in pages:
            status = page['status']
            print(f"   • {page['title']['rendered']} (ID: {page['id']}, Status: {status})")
    else:
        print(f"   ❌ Failed: {response.status_code}")

def check_posts():
    """Check all posts"""
    print("\n📰 Checking Posts...")
    print("-" * 60)
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code == 200:
        posts = response.json()
        print(f"   Total posts: {len(posts)}")
        for post in posts:
            status = post['status']
            print(f"   • {post['title']['rendered']} (ID: {post['id']}, Status: {status})")
    else:
        print(f"   ❌ Failed: {response.status_code}")

def check_menus():
    """Check navigation menus"""
    print("\n🧭 Checking Menus...")
    print("-" * 60)
    
    # Get all menus
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/menus"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code == 200:
        menus = response.json()
        print(f"   Total menus: {len(menus)}")
        for menu in menus:
            print(f"   • {menu.get('name', 'Unknown')} (ID: {menu.get('id', 'N/A')})")
    elif response.status_code == 404:
        print("   ⚠️  Menu endpoint not available (may need WP REST API Menus plugin)")
    else:
        print(f"   ❌ Failed: {response.status_code}")

def check_settings():
    """Check reading settings"""
    print("\n⚙️  Checking Settings...")
    print("-" * 60)
    
    # Check front page settings
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code == 200:
        settings = response.json()
        print(f"   Show on front: {settings.get('show_on_front', 'Unknown')}")
        print(f"   Front page ID: {settings.get('page_on_front', 'None')}")
        print(f"   Posts page ID: {settings.get('page_for_posts', 'None')}")
        print(f"   Title: {settings.get('title', 'Unknown')}")
        print(f"   Description: {settings.get('description', 'Unknown')}")
    else:
        print(f"   ❌ Failed: {response.status_code}")

def check_active_theme():
    """Check active theme"""
    print("\n🎨 Checking Active Theme...")
    print("-" * 60)
    
    # There's no direct endpoint for active theme, but we can check via site info
    url = f"{WORDPRESS_URL}/wp-json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Site: {data.get('name', 'Unknown')}")
        print(f"   Description: {data.get('description', 'Unknown')}")
        print(f"   URL: {data.get('url', 'Unknown')}")
    
    # Note: Active theme info requires custom endpoint

def main():
    print("=" * 60)
    print("🔍 WordPress Site Status Check")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    check_active_theme()
    check_pages()
    check_posts()
    check_menus()
    check_settings()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS TO FIX:")
    print("=" * 60)
    print("\n1. Set Static Homepage:")
    print(f"   Go to: {WORDPRESS_URL}/wp-admin/options-reading.php")
    print("   • Select 'A static page'")
    print("   • Choose 'Homepage' for Homepage")
    print("   • Choose 'Blog' for Posts page")
    print("\n2. Create Navigation Menu:")
    print(f"   Go to: {WORDPRESS_URL}/wp-admin/nav-menus.php")
    print("   • Create new menu: 'Main Menu'")
    print("   • Add pages: Homepage, About, Services, Contact")
    print("   • Check 'Primary Menu' location")
    print("   • Click 'Save Menu'")
    print("\n3. Check Your Site:")
    print(f"   Visit: {WORDPRESS_URL}")
    print("   • You should see your content")
    print("   • Navigation menu should appear")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
