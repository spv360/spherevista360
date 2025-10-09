#!/usr/bin/env python3
"""
WordPress API Authentication with User Password
Fix broken links using proper authentication
"""

import requests
import base64
import json
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
WP_USERNAME = "admin"

def get_auth_credentials():
    """Get authentication credentials"""
    print("🔐 WordPress Authentication Setup")
    print("=" * 40)
    
    # Use provided username
    username = WP_USERNAME
    
    # Get password from user
    print(f"Username: {username}")
    password = getpass.getpass("Enter WordPress password: ")
    
    return username, password

def test_authentication(username, password):
    """Test if authentication works"""
    print("\n🧪 Testing Authentication...")
    
    # Create Basic Auth header
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test with /users/me endpoint
        response = requests.get(f"{WP_BASE_URL}/users/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Authentication successful!")
            print(f"   User ID: {user_data.get('id')}")
            print(f"   Username: {user_data.get('username')}")
            print(f"   Display Name: {user_data.get('name')}")
            
            # Check capabilities
            capabilities = user_data.get('capabilities', {})
            if 'edit_posts' in capabilities:
                print("✅ User has edit_posts capability")
                return headers
            else:
                print("⚠️ User may not have edit_posts capability")
                return headers  # Try anyway
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def fix_post_1833(auth_headers):
    """Fix the broken links in post 1833"""
    print("\n🔧 Fixing Post 1833 Broken Links")
    print("=" * 40)
    
    post_id = 1833
    
    # Get current post with edit context
    try:
        response = requests.get(f"{WP_BASE_URL}/posts/{post_id}?context=edit", 
                              headers=auth_headers)
        
        if response.status_code != 200:
            print(f"❌ Failed to get post: {response.status_code}")
            print(f"Error: {response.text}")
            return False
        
        post_data = response.json()
        title = post_data['title']['rendered']
        print(f"📝 Post: {title}")
        
        # Get content - try 'raw' first, then 'rendered'
        content = post_data.get('content', {})
        if 'raw' in content:
            current_content = content['raw']
            content_type = 'raw'
        else:
            current_content = content['rendered']
            content_type = 'rendered'
        
        print(f"Using content type: {content_type}")
        print(f"Content length: {len(current_content)} characters")
        
        # Make the replacements
        updated_content = current_content
        
        # Define replacements
        replacements = [
            {
                'old': 'https://spherevista360.com/product-analytics-2025/',
                'new': 'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/'
            },
            {
                'old': 'https://spherevista360.com/on-device-vs-cloud-ai-2025/',
                'new': 'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/'
            }
        ]
        
        changes_made = 0
        for replacement in replacements:
            if replacement['old'] in updated_content:
                updated_content = updated_content.replace(replacement['old'], replacement['new'])
                changes_made += 1
                print(f"✅ Replaced: {replacement['old']}")
                print(f"   With: {replacement['new']}")
        
        if changes_made == 0:
            print("ℹ️ No broken links found - may already be fixed")
            return True
        
        # Update the post
        update_data = {'content': updated_content}
        
        update_response = requests.post(f"{WP_BASE_URL}/posts/{post_id}", 
                                      json=update_data, 
                                      headers=auth_headers)
        
        if update_response.status_code == 200:
            print(f"✅ Post updated successfully! ({changes_made} links fixed)")
            return True
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(f"Error: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing post: {e}")
        return False

def verify_fix():
    """Verify that the links have been fixed"""
    print("\n🔍 Verifying Fix...")
    print("=" * 30)
    
    try:
        response = requests.get(f"{WP_BASE_URL}/posts/1833")
        if response.status_code == 200:
            post = response.json()
            content = post['content']['rendered']
            
            broken_links = [
                'https://spherevista360.com/product-analytics-2025/',
                'https://spherevista360.com/on-device-vs-cloud-ai-2025/'
            ]
            
            correct_links = [
                'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/',
                'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/'
            ]
            
            broken_count = 0
            fixed_count = 0
            
            for broken_link in broken_links:
                if broken_link in content:
                    broken_count += 1
                    print(f"❌ Still contains: {broken_link}")
            
            for correct_link in correct_links:
                if correct_link in content:
                    fixed_count += 1
                    print(f"✅ Now contains: {correct_link}")
            
            if broken_count == 0 and fixed_count > 0:
                print("\n🎉 SUCCESS! All broken links have been fixed!")
                return True
            elif broken_count == 0:
                print("\n✅ No broken links found")
                return True
            else:
                print(f"\n⚠️ Still {broken_count} broken links remaining")
                return False
                
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 WordPress Broken Links Fixer with Authentication")
    print("=" * 60)
    
    # Get credentials
    username, password = get_auth_credentials()
    
    # Test authentication
    auth_headers = test_authentication(username, password)
    
    if not auth_headers:
        print("\n❌ Authentication failed. Please check your credentials.")
        return
    
    # Fix the post
    success = fix_post_1833(auth_headers)
    
    if success:
        # Verify the fix
        verify_fix()
    else:
        print("\n❌ Failed to fix the post")

if __name__ == "__main__":
    main()