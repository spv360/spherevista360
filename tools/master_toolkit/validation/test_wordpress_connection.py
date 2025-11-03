#!/usr/bin/env python3
"""
WordPress Application Password Setup Guide and Tester
"""

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

def print_setup_guide():
    """Print detailed setup instructions"""
    print("=" * 70)
    print("🔐 WordPress Application Password Setup Guide")
    print("=" * 70)
    print()
    print("WordPress REST API requires an Application Password for security.")
    print("Follow these steps to create one:")
    print()
    print("📝 STEP-BY-STEP INSTRUCTIONS:")
    print("-" * 70)
    print()
    print("1. 🔑 Login to WordPress Admin")
    print("   Go to: https://spherevista360.com/wp-admin")
    print()
    print("2. 👤 Go to Your Profile")
    print("   Navigate to: Users > Profile")
    print("   Or click your name in the top-right corner")
    print()
    print("3. 📱 Find Application Passwords Section")
    print("   Scroll down to 'Application Passwords' section")
    print("   (If you don't see it, your WordPress might need updating)")
    print()
    print("4. ✍️  Create New Application Password")
    print("   - Application Name: 'SphereVista360 API'")
    print("   - Click 'Add New Application Password'")
    print()
    print("5. 📋 Copy the Generated Password")
    print("   - WordPress will show a password like: 'xxxx xxxx xxxx xxxx xxxx xxxx'")
    print("   - IMPORTANT: Copy this immediately (you won't see it again!)")
    print("   - Save it somewhere secure")
    print()
    print("6. 🔧 Update Your .env File")
    print("   Replace the password in your .env file with the new one")
    print("   Keep the spaces between the characters")
    print()
    print("=" * 70)
    print()

def test_credentials():
    """Test WordPress credentials"""
    load_dotenv()
    
    base_url = os.getenv('WORDPRESS_BASE_URL', '').rstrip('/')
    username = os.getenv('WORDPRESS_USERNAME', '')
    password = os.getenv('WORDPRESS_PASSWORD', '')
    
    if not all([base_url, username, password]):
        print("❌ Missing credentials in .env file")
        return False
    
    print("🔍 Testing WordPress Connection...")
    print(f"   Site: {base_url}")
    print(f"   User: {username}")
    print(f"   Pass: {'*' * len(password)}")
    print()
    
    try:
        # Test REST API endpoint
        api_url = f"{base_url}/wp-json/wp/v2/users/me"
        
        print(f"   Connecting to: {api_url}")
        
        auth = HTTPBasicAuth(username, password)
        response = requests.get(api_url, auth=auth, timeout=10)
        
        print(f"   HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"\n✅ SUCCESS! Connection established")
            print(f"   User: {user_data.get('name', 'Unknown')}")
            print(f"   Email: {user_data.get('email', 'Unknown')}")
            print(f"   Roles: {', '.join(user_data.get('roles', []))}")
            print(f"\n🎉 You're ready to run the automated setup!")
            return True
            
        elif response.status_code == 401:
            print(f"\n❌ AUTHENTICATION FAILED")
            print(f"   The username or password is incorrect")
            print(f"\n💡 Solutions:")
            print(f"   1. Double-check your username (case-sensitive)")
            print(f"   2. Create an Application Password (see guide below)")
            print(f"   3. Make sure you copied the entire password with spaces")
            return False
            
        elif response.status_code == 404:
            print(f"\n❌ REST API NOT FOUND")
            print(f"   The WordPress REST API might be disabled")
            print(f"\n💡 Solutions:")
            print(f"   1. Check if WordPress is installed at: {base_url}")
            print(f"   2. Make sure REST API is enabled (should be by default)")
            print(f"   3. Check for plugins that might block the REST API")
            return False
            
        else:
            print(f"\n❌ UNEXPECTED ERROR: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR")
        print(f"   Cannot connect to: {base_url}")
        print(f"\n💡 Solutions:")
        print(f"   1. Check if the URL is correct")
        print(f"   2. Make sure the site is online")
        print(f"   3. Check your internet connection")
        return False
        
    except requests.exceptions.Timeout:
        print(f"\n❌ CONNECTION TIMEOUT")
        print(f"   The server took too long to respond")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def main():
    """Main function"""
    print()
    print_setup_guide()
    
    # Test current credentials
    print("🧪 Testing Current Credentials...")
    print("=" * 70)
    print()
    
    success = test_credentials()
    
    print()
    print("=" * 70)
    
    if success:
        print("\n✅ Your credentials are working!")
        print("\n🚀 Next Step: Run the automated setup")
        print("   Command: python3 wordpress_api_setup.py")
    else:
        print("\n❌ Credentials not working yet")
        print("\n📝 Action Required:")
        print("   1. Follow the setup guide above to create an Application Password")
        print("   2. Update your .env file with the new password")
        print("   3. Run this test again: python3 test_wordpress_connection.py")
        print("\n💡 Or manually add content using the text files we created")
    
    print()

if __name__ == "__main__":
    main()