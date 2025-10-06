#!/usr/bin/env python3
"""
WordPress Authentication Tester
Diagnoses and fixes WordPress API authentication issues
"""

import os
import requests
import base64
import json
from urllib.parse import urlparse

class WordPressAuthTester:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', '').rstrip('/')
        self.wp_user = os.environ.get('WP_USER', '')
        self.wp_pass = os.environ.get('WP_APP_PASS', '')
        
    def test_basic_connection(self):
        """Test if the WordPress site is accessible"""
        print("🌐 Testing basic site connection...")
        
        if not self.wp_site:
            print("❌ WP_SITE not set")
            return False
            
        try:
            # Test basic site access
            response = requests.get(f"{self.wp_site}", timeout=10)
            if response.status_code == 200:
                print(f"✅ Site accessible: {self.wp_site}")
                return True
            else:
                print(f"❌ Site not accessible (Status: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_rest_api_availability(self):
        """Test if WordPress REST API is available"""
        print("🔌 Testing WordPress REST API...")
        
        try:
            # Test REST API root
            response = requests.get(f"{self.wp_site}/wp-json/wp/v2/", timeout=10)
            if response.status_code == 200:
                print("✅ WordPress REST API is available")
                return True
            else:
                print(f"❌ WordPress REST API not available (Status: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ REST API test failed: {e}")
            return False
    
    def test_authentication(self):
        """Test WordPress authentication"""
        print("🔐 Testing WordPress authentication...")
        
        if not all([self.wp_user, self.wp_pass]):
            missing = []
            if not self.wp_user:
                missing.append("WP_USER")
            if not self.wp_pass:
                missing.append("WP_APP_PASS")
            print(f"❌ Missing credentials: {', '.join(missing)}")
            return False
        
        try:
            # Create authentication header
            credentials = f"{self.wp_user}:{self.wp_pass}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            # Test authentication with a simple GET request
            response = requests.get(
                f"{self.wp_site}/wp-json/wp/v2/users/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Authentication successful")
                print(f"   User: {user_data.get('name', 'Unknown')}")
                print(f"   Roles: {', '.join(user_data.get('roles', []))}")
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed (401 Unauthorized)")
                print("   Possible issues:")
                print("   • Incorrect username or application password")
                print("   • Application password not enabled")
                print("   • User doesn't have API access")
                return False
            else:
                print(f"❌ Authentication test failed (Status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Authentication test error: {e}")
            return False
    
    def test_content_permissions(self):
        """Test if user can read and modify content"""
        print("📝 Testing content permissions...")
        
        if not all([self.wp_user, self.wp_pass]):
            print("❌ Cannot test permissions without credentials")
            return False
        
        try:
            credentials = f"{self.wp_user}:{self.wp_pass}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            # Test reading posts
            posts_response = requests.get(
                f"{self.wp_site}/wp-json/wp/v2/posts?per_page=1",
                headers=headers,
                timeout=10
            )
            
            if posts_response.status_code == 200:
                print("✅ Can read posts")
                posts_data = posts_response.json()
                
                if posts_data and len(posts_data) > 0:
                    # Test if we can modify a post (just update without changes)
                    post_id = posts_data[0]['id']
                    post_data = {
                        'title': posts_data[0]['title']['rendered']  # Same title, no actual change
                    }
                    
                    update_response = requests.post(
                        f"{self.wp_site}/wp-json/wp/v2/posts/{post_id}",
                        headers=headers,
                        json=post_data,
                        timeout=10
                    )
                    
                    if update_response.status_code == 200:
                        print("✅ Can modify posts")
                        return True
                    elif update_response.status_code == 401:
                        print("❌ Cannot modify posts (401 Unauthorized)")
                        print("   User may not have 'edit_posts' capability")
                        return False
                    else:
                        print(f"❌ Cannot modify posts (Status: {update_response.status_code})")
                        return False
                else:
                    print("⚠️  No posts found to test modification")
                    return True
            else:
                print(f"❌ Cannot read posts (Status: {posts_response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Permission test error: {e}")
            return False
    
    def provide_troubleshooting_guide(self):
        """Provide troubleshooting guide based on test results"""
        print("\n🔧 TROUBLESHOOTING GUIDE")
        print("=" * 25)
        
        print("\n1. APPLICATION PASSWORD SETUP:")
        print("   a) Login to WordPress admin")
        print("   b) Go to Users > Profile")
        print("   c) Scroll to 'Application Passwords'")
        print("   d) Enter name: 'Content Audit Tool'")
        print("   e) Click 'Add New Application Password'")
        print("   f) Copy the generated password (not your login password!)")
        
        print("\n2. CORRECT ENVIRONMENT VARIABLES:")
        print("   export WP_SITE='https://yourdomain.com'  # No trailing slash")
        print("   export WP_USER='your_admin_username'      # WordPress username")
        print("   export WP_APP_PASS='xxxx xxxx xxxx xxxx'  # Application password")
        
        print("\n3. USER PERMISSIONS REQUIRED:")
        print("   • Administrator role (recommended)")
        print("   • OR at minimum: edit_posts, delete_posts, edit_pages, delete_pages")
        
        print("\n4. WORDPRESS SETTINGS:")
        print("   • REST API must be enabled (usually enabled by default)")
        print("   • No security plugins blocking API access")
        print("   • SSL certificate valid (for https sites)")
        
        print("\n5. COMMON ISSUES:")
        print("   • Using login password instead of application password")
        print("   • Extra spaces in environment variables")
        print("   • Wrong username (use WordPress username, not email)")
        print("   • Security plugins blocking REST API")
        
        print("\n6. TEST MANUALLY:")
        print("   curl -u 'username:app_password' \\")
        print(f"        '{self.wp_site}/wp-json/wp/v2/users/me'")
    
    def run_full_diagnosis(self):
        """Run complete authentication diagnosis"""
        print("🩺 WordPress Authentication Diagnosis")
        print("=" * 40)
        print(f"Site: {self.wp_site or 'NOT SET'}")
        print(f"User: {self.wp_user or 'NOT SET'}")
        print(f"Pass: {'SET' if self.wp_pass else 'NOT SET'}")
        print()
        
        # Run all tests
        tests_passed = 0
        total_tests = 4
        
        if self.test_basic_connection():
            tests_passed += 1
        
        if self.test_rest_api_availability():
            tests_passed += 1
        
        if self.test_authentication():
            tests_passed += 1
        
        if self.test_content_permissions():
            tests_passed += 1
        
        print(f"\n📊 DIAGNOSIS RESULTS")
        print("=" * 20)
        print(f"Tests passed: {tests_passed}/{total_tests}")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! Your WordPress authentication is working correctly.")
            print("\nYou can now run the content audit:")
            print("   python wordpress-enhancements/scripts/content_auditor.py")
        else:
            print("❌ Some tests failed. Authentication needs to be fixed.")
            self.provide_troubleshooting_guide()
        
        return tests_passed == total_tests

def main():
    """Main execution function"""
    tester = WordPressAuthTester()
    return tester.run_full_diagnosis()

if __name__ == "__main__":
    main()