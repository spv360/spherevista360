#!/usr/bin/env python3
"""
WordPress API Authentication Analysis and Testing
"""

import requests
import json
import base64
from datetime import datetime

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def check_wp_api_status():
    print("🔍 CHECKING WORDPRESS API STATUS")
    print("=" * 45)
    
    endpoints_to_check = [
        "/wp-json/",
        "/wp-json/wp/v2/",
        "/wp-json/wp/v2/posts",
        "/wp-json/wp/v2/pages",
        "/wp-json/wp/v2/users"
    ]
    
    for endpoint in endpoints_to_check:
        url = f"{SITE_URL}{endpoint}"
        print(f"\n🌐 Testing: {endpoint}")
        
        try:
            response = requests.get(url)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                if endpoint == "/wp-json/":
                    data = response.json()
                    print(f"   ✅ WordPress API is accessible")
                    print(f"   📋 Available routes: {len(data.get('routes', {}))}")
                    
                    # Check authentication info
                    auth_info = data.get('authentication', {})
                    if auth_info:
                        print(f"   🔐 Authentication methods: {auth_info}")
                    
                elif endpoint in ["/wp-json/wp/v2/posts", "/wp-json/wp/v2/pages"]:
                    data = response.json()
                    print(f"   ✅ Accessible, found {len(data)} items")
                    
            elif response.status_code == 401:
                print(f"   🔐 Requires authentication")
            elif response.status_code == 403:
                print(f"   🚫 Forbidden - permissions issue")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")

def check_authentication_methods():
    print("\n🔐 CHECKING AUTHENTICATION METHODS")
    print("=" * 45)
    
    # Check what authentication the site supports
    try:
        response = requests.get(f"{SITE_URL}/wp-json/")
        if response.status_code == 200:
            data = response.json()
            
            print("📋 WordPress API Info:")
            print(f"   Name: {data.get('name', 'Unknown')}")
            print(f"   Description: {data.get('description', 'Unknown')}")
            print(f"   URL: {data.get('url', 'Unknown')}")
            print(f"   Home: {data.get('home', 'Unknown')}")
            
            # Check routes that might give us auth info
            routes = data.get('routes', {})
            auth_routes = [route for route in routes.keys() if 'auth' in route.lower() or 'jwt' in route.lower()]
            
            if auth_routes:
                print(f"\n🔐 Authentication routes found:")
                for route in auth_routes:
                    print(f"   {route}")
            else:
                print(f"\n❌ No specific authentication routes found")
                
    except Exception as e:
        print(f"💥 Error checking authentication: {e}")

def test_different_auth_methods():
    print("\n🧪 TESTING DIFFERENT AUTHENTICATION METHODS")
    print("=" * 55)
    
    # Test endpoint for updates
    test_page_id = 1658  # Newsletter page
    test_url = f"{WP_API_BASE}/pages/{test_page_id}"
    
    # Method 1: No authentication (public read)
    print("1️⃣ Testing without authentication:")
    try:
        response = requests.get(test_url)
        print(f"   GET Status: {response.status_code}")
        
        # Try POST without auth
        response = requests.post(test_url, json={"title": "Test"})
        print(f"   POST Status: {response.status_code}")
        if response.status_code == 401:
            print("   🔐 POST requires authentication (expected)")
        
    except Exception as e:
        print(f"   💥 Error: {e}")
    
    # Method 2: Basic Authentication (would need credentials)
    print("\n2️⃣ Basic Authentication requirements:")
    print("   📋 Requires: WordPress username and password")
    print("   ⚠️  Not recommended for production")
    print("   🔧 Format: Authorization: Basic base64(username:password)")
    
    # Method 3: Application Passwords
    print("\n3️⃣ Application Passwords (Recommended):")
    print("   📋 WordPress 5.6+ feature")
    print("   🔧 Go to: WordPress Admin → Users → Your Profile")
    print("   🔑 Create new Application Password")
    print("   📝 Use format: username:application_password")
    
    # Method 4: JWT Authentication
    print("\n4️⃣ JWT Authentication:")
    print("   📋 Requires JWT plugin installation")
    print("   🔧 Plugin: JWT Authentication for WP-API")
    print("   🔑 Uses tokens instead of passwords")
    
    # Method 5: Custom API key
    print("\n5️⃣ Custom API Key:")
    print("   📋 Requires plugin like WP REST API Authentication")
    print("   🔧 Generates API keys for authentication")

def check_wp_permissions():
    print("\n🛡️ CHECKING WORDPRESS PERMISSIONS")
    print("=" * 40)
    
    # Check what we can access without auth
    public_endpoints = [
        "/posts",
        "/pages", 
        "/categories",
        "/tags",
        "/media"
    ]
    
    for endpoint in public_endpoints:
        url = f"{WP_API_BASE}{endpoint}"
        print(f"\n📄 Testing {endpoint}:")
        
        try:
            # GET request (should work)
            response = requests.get(url)
            print(f"   GET: {response.status_code}")
            
            # POST request (should fail)
            response = requests.post(url, json={"test": "data"})
            print(f"   POST: {response.status_code}")
            
            # Check response headers for auth info
            auth_header = response.headers.get('WWW-Authenticate')
            if auth_header:
                print(f"   🔐 Auth required: {auth_header}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")

def why_auth_failing():
    print("\n❓ WHY AUTHENTICATION IS FAILING")
    print("=" * 40)
    
    reasons = [
        "🔐 WordPress REST API requires authentication for write operations",
        "🛡️ This is a security feature to prevent unauthorized content changes",
        "📝 Reading content (GET) is usually public",
        "✏️ Writing/updating content (POST/PUT/PATCH) requires authentication",
        "🔑 We need valid WordPress credentials or API keys",
        "⚙️ WordPress settings might restrict API access"
    ]
    
    for reason in reasons:
        print(f"   {reason}")

def solutions_to_fix_auth():
    print("\n💡 SOLUTIONS TO FIX AUTHENTICATION")
    print("=" * 45)
    
    print("🎯 OPTION 1: Application Passwords (Easiest)")
    print("   1. Login to WordPress Admin")
    print("   2. Go to Users → Your Profile")
    print("   3. Scroll to 'Application Passwords' section")
    print("   4. Enter name like 'API Access' and click 'Add New'")
    print("   5. Copy the generated password")
    print("   6. Use username:app_password for authentication")
    
    print("\n🎯 OPTION 2: Manual Update (Fastest)")
    print("   1. Copy the enhanced content from previous script")
    print("   2. Login to WordPress Admin → Pages")
    print("   3. Edit Newsletter page manually")
    print("   4. Paste the new content")
    print("   5. Update the page")
    
    print("\n🎯 OPTION 3: JWT Plugin")
    print("   1. Install 'JWT Authentication for WP-API' plugin")
    print("   2. Configure JWT settings")
    print("   3. Use token-based authentication")
    
    print("\n🎯 OPTION 4: Check WordPress Settings")
    print("   1. WordPress Admin → Settings → Permalinks")
    print("   2. Ensure permalinks are set to 'Post name' or custom")
    print("   3. Check if REST API is disabled by security plugin")

def main():
    print("🔧 WORDPRESS API AUTHENTICATION ANALYSIS")
    print("=" * 50)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Investigating why authentication is failing")
    print()
    
    check_wp_api_status()
    check_authentication_methods()
    test_different_auth_methods()
    check_wp_permissions()
    why_auth_failing()
    solutions_to_fix_auth()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    print("✅ WordPress REST API is accessible for reading")
    print("❌ Authentication required for writing/updating")
    print("🔧 This is normal WordPress security behavior")
    print("💡 Use Application Passwords or manual update")
    
    print("\n🎯 RECOMMENDED ACTION:")
    print("   Use manual update method - it's faster than setting up auth")
    print("   Copy content from previous script and paste in WordPress admin")

if __name__ == "__main__":
    main()