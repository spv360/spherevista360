#!/usr/bin/env python3
"""
WordPress API Fix with Editor Role Credentials
Fix broken links using editor user credentials
"""

import requests
import base64
import sys
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def get_editor_credentials():
    """Get editor user credentials"""
    print("🔐 Editor Authentication Setup")
    print("=" * 40)
    
    # Get username and password
    username = input("Enter editor username: ")
    password = getpass.getpass("Enter editor password: ")
    
    return username, password

def fix_with_editor_auth(username, password):
    """Fix broken links using editor credentials"""
    print("🔧 FIXING BROKEN LINKS WITH EDITOR AUTH")
    print("=" * 50)
    
    # Create authentication headers
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # Test authentication first
    print("🔐 Testing editor authentication...")
    try:
        auth_test = requests.get(f"{WP_BASE_URL}/users/me", headers=headers)
        if auth_test.status_code == 200:
            user_data = auth_test.json()
            print(f"✅ Authenticated as: {user_data.get('username')}")
            print(f"   Display name: {user_data.get('name')}")
            
            # Check user capabilities
            capabilities = user_data.get('capabilities', {})
            if 'edit_posts' in capabilities:
                print("✅ User has edit_posts capability")
            else:
                print("⚠️ User may not have edit_posts capability")
                print(f"   Available capabilities: {list(capabilities.keys())[:5]}...")
                
        else:
            print(f"❌ Authentication failed: {auth_test.status_code}")
            print(f"Error: {auth_test.text}")
            return False
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return False
    
    # Get post 1833 with edit context
    print(f"\\n📝 Getting post 1833 for editing...")
    try:
        post_response = requests.get(f"{WP_BASE_URL}/posts/1833?context=edit", headers=headers)
        
        print(f"   Post fetch status: {post_response.status_code}")
        
        if post_response.status_code != 200:
            print(f"❌ Failed to get post with edit context: {post_response.status_code}")
            print(f"Error: {post_response.text}")
            
            # Try without edit context
            print("\\n🔄 Trying without edit context...")
            post_response = requests.get(f"{WP_BASE_URL}/posts/1833", headers=headers)
            if post_response.status_code != 200:
                print(f"❌ Failed to get post: {post_response.status_code}")
                return False
        
        post_data = post_response.json()
        title = post_data['title']['rendered']
        print(f"   Post title: {title}")
        
        # Get content - check what's available
        content = post_data.get('content', {})
        content_keys = list(content.keys())
        print(f"   Available content fields: {content_keys}")
        
        # Use the best available content field
        if 'raw' in content:
            current_content = content['raw']
            content_type = 'raw'
        elif 'rendered' in content:
            current_content = content['rendered']
            content_type = 'rendered'
        else:
            print("❌ No suitable content field found")
            return False
        
        print(f"   Using content type: {content_type}")
        print(f"   Content length: {len(current_content)} characters")
        
    except Exception as e:
        print(f"❌ Error getting post: {e}")
        return False
    
    # Check for broken links
    print(f"\\n🔍 Checking for broken links...")
    broken_links = [
        'https://spherevista360.com/product-analytics-2025/',
        'https://spherevista360.com/on-device-vs-cloud-ai-2025/'
    ]
    
    found_broken = []
    for broken_link in broken_links:
        if broken_link in current_content:
            found_broken.append(broken_link)
            print(f"   ❌ Found: {broken_link}")
    
    if not found_broken:
        print("✅ No broken links found - may already be fixed!")
        return True
    
    # Make replacements
    print(f"\\n🔄 Making replacements...")
    updated_content = current_content
    
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
            print(f"✅ Will replace: {old_url}")
            print(f"   With: {new_url}")
    
    if changes == 0:
        print("ℹ️ No changes needed")
        return True
    
    # Update the post
    print(f"\\n💾 Updating post with {changes} changes...")
    try:
        update_data = {'content': updated_content}
        
        update_response = requests.post(f"{WP_BASE_URL}/posts/1833", 
                                      json=update_data, 
                                      headers=headers)
        
        print(f"   Update status: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print(f"✅ Post updated successfully!")
            
            # Verify the update
            print(f"\\n🔍 Verifying update...")
            verify_response = requests.get(f"{WP_BASE_URL}/posts/1833")
            if verify_response.status_code == 200:
                verify_content = verify_response.json()['content']['rendered']
                
                still_broken = 0
                for old_url, _ in replacements:
                    if old_url in verify_content:
                        still_broken += 1
                        print(f"   ❌ Still contains: {old_url}")
                
                if still_broken == 0:
                    print("✅ Verification passed - all broken links fixed!")
                else:
                    print(f"⚠️ Verification: {still_broken} broken links remain")
            
            return True
            
        elif update_response.status_code == 401:
            print(f"❌ Update failed: Insufficient permissions (401)")
            print("   Editor role may not have permission to edit this specific post")
            return False
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(f"Error: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Update error: {e}")
        return False

def main():
    """Main function for editor authentication"""
    print("🚀 WordPress Broken Links Fixer - Editor Authentication")
    print("=" * 60)
    
    # Get editor credentials
    username, password = get_editor_credentials()
    
    # Fix with editor credentials
    success = fix_with_editor_auth(username, password)
    
    if success:
        print("\\n🎉 SUCCESS! Broken links have been fixed!")
        print("\\nPost 1833 now has working internal links:")
        print("✅ Product Analytics in 2025: From Dashboards to Decisions")
        print("✅ On-Device AI vs Cloud AI: Where Each Wins in 2025")
    else:
        print("\\n❌ FAILED! Manual intervention may be required.")
        print("\\nIf editor permissions are insufficient, you may need:")
        print("• Administrator access")
        print("• Manual edit through WordPress dashboard")

if __name__ == "__main__":
    main()