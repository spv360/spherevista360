#!/usr/bin/env python3
"""
WordPress API Fix with Direct Password
Fix broken links using provided password
"""

import requests
import base64
import sys

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
WP_USERNAME = "admin"

def fix_with_password(password):
    """Fix broken links using provided password"""
    print("🔧 FIXING BROKEN LINKS WITH API AUTH")
    print("=" * 50)
    
    # Create authentication headers
    credentials = f"{WP_USERNAME}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # Test authentication first
    print("🔐 Testing authentication...")
    try:
        auth_test = requests.get(f"{WP_BASE_URL}/users/me", headers=headers)
        if auth_test.status_code == 200:
            user_data = auth_test.json()
            print(f"✅ Authenticated as: {user_data.get('username')}")
        else:
            print(f"❌ Authentication failed: {auth_test.status_code}")
            print(f"Error: {auth_test.text}")
            return False
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return False
    
    # Get post 1833
    print(f"\\n📝 Getting post 1833...")
    try:
        post_response = requests.get(f"{WP_BASE_URL}/posts/1833?context=edit", headers=headers)
        if post_response.status_code != 200:
            print(f"❌ Failed to get post: {post_response.status_code}")
            return False
        
        post_data = post_response.json()
        title = post_data['title']['rendered']
        print(f"Post title: {title}")
        
        # Get content
        content = post_data.get('content', {})
        if 'raw' in content:
            current_content = content['raw']
        else:
            current_content = content['rendered']
        
        print(f"Content length: {len(current_content)} characters")
        
    except Exception as e:
        print(f"❌ Error getting post: {e}")
        return False
    
    # Make replacements
    print(f"\\n🔄 Making replacements...")
    updated_content = current_content
    
    # Replace broken links
    replacements = [
        ('https://spherevista360.com/product-analytics-2025/', 
         'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/'),
        ('https://spherevista360.com/on-device-vs-cloud-ai-2025/', 
         'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/')
    ]
    
    changes = 0
    for old_url, new_url in replacements:
        if old_url in updated_content:
            updated_content = updated_content.replace(old_url, new_url)
            changes += 1
            print(f"✅ Replaced: {old_url}")
    
    if changes == 0:
        print("ℹ️ No broken links found")
        return True
    
    # Update the post
    print(f"\\n💾 Updating post...")
    try:
        update_data = {'content': updated_content}
        update_response = requests.post(f"{WP_BASE_URL}/posts/1833", 
                                      json=update_data, 
                                      headers=headers)
        
        if update_response.status_code == 200:
            print(f"✅ Post updated successfully! ({changes} links fixed)")
            
            # Quick verification
            print(f"\\n🔍 Quick verification...")
            verify_response = requests.get(f"{WP_BASE_URL}/posts/1833")
            if verify_response.status_code == 200:
                verify_content = verify_response.json()['content']['rendered']
                broken_still = sum(1 for old_url, _ in replacements if old_url in verify_content)
                if broken_still == 0:
                    print("✅ Verification passed - no broken links found!")
                else:
                    print(f"⚠️ Verification: {broken_still} broken links still exist")
            
            return True
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(f"Error: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Update error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 auth_fix_broken_links_direct.py <password>")
        print("Example: python3 auth_fix_broken_links_direct.py 'your_password_here'")
        sys.exit(1)
    
    password = sys.argv[1]
    success = fix_with_password(password)
    
    if success:
        print("\\n🎉 SUCCESS! Broken links have been fixed!")
    else:
        print("\\n❌ FAILED! Manual intervention may be required.")