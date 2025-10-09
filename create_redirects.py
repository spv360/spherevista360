#!/usr/bin/env python3
"""
WordPress Redirect Manager
==========================
Creates redirects for broken URLs using available WordPress methods
"""

import sys
sys.path.append('./master_toolkit')

from master_toolkit.core.client import WordPressClient
import requests

def create_wordpress_redirects():
    """Create WordPress redirects programmatically where possible."""
    
    print("🔧 WORDPRESS REDIRECT CREATOR")
    print("=" * 50)
    
    # Get credentials
    username = input("Enter WordPress username: ")
    password = input("Enter WordPress password: ")
    
    # Initialize and authenticate
    wp = WordPressClient("https://spherevista360.com")
    try:
        wp.authenticate(username, password)
        print("✅ Authentication successful!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    # Define redirects
    redirects = {
        'product-analytics-2025': 'product-analytics-in-2025-from-dashboards-to-decisions',
        'on-device-vs-cloud-ai-2025': 'on-device-ai-vs-cloud-ai-where-each-wins-in-2025',
        'tech-innovation-2025': 'generative-ai-tools-shaping-tech-in-2025',
        'data-privacy-future': 'digital-banking-revolution-the-future-of-fintech',
        'cloud-computing-evolution': 'on-device-ai-vs-cloud-ai-where-each-wins-in-2025'
    }
    
    print(f"\n📋 Creating {len(redirects)} redirects...")
    
    # Method 1: Try to create redirect posts (if supported)
    print("\n🔧 Method 1: Creating redirect posts...")
    for old_slug, new_slug in redirects.items():
        try:
            # Create a post with redirect meta
            redirect_post = {
                'title': f'Redirect: {old_slug}',
                'slug': old_slug,
                'status': 'publish',
                'content': f'<script>window.location.href="/{new_slug}/";</script>',
                'meta': {
                    '_redirect_url': f'/{new_slug}/',
                    '_redirect_type': '301'
                }
            }
            
            result = wp.create_post(redirect_post)
            print(f"  ✅ Created redirect post for {old_slug} (ID: {result['id']})")
            
        except Exception as e:
            print(f"  ❌ Failed to create redirect post for {old_slug}: {e}")
    
    print("\n📄 Alternative Solutions:")
    print("1. Add .htaccess rules (see redirect_rules.htaccess)")
    print("2. Install WordPress Redirection plugin")
    print("3. Use server-level redirects")
    
    # Test the redirects
    print("\n🔍 Testing redirect effectiveness...")
    for old_slug, new_slug in redirects.items():
        old_url = f"https://spherevista360.com/{old_slug}/"
        try:
            response = requests.head(old_url, allow_redirects=False, timeout=10)
            if response.status_code in [301, 302]:
                print(f"  ✅ {old_slug} redirects properly")
            else:
                print(f"  ❌ {old_slug} still returns {response.status_code}")
        except:
            print(f"  ❌ {old_slug} still broken")

if __name__ == "__main__":
    create_wordpress_redirects()