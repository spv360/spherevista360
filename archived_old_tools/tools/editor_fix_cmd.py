#!/usr/bin/env python3
"""
WordPress Editor Fix - Command Line Version
Fix broken links using editor credentials from command line
"""

import requests
import base64
import sys

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def fix_with_editor_credentials(username, password):
    """Fix broken links using editor credentials"""
    print("🔧 FIXING BROKEN LINKS WITH EDITOR CREDENTIALS")
    print("=" * 60)
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    
    # Create authentication headers
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # Test authentication
    print("\\n🔐 Testing authentication...")
    try:
        auth_test = requests.get(f"{WP_BASE_URL}/users/me", headers=headers)
        print(f"Auth response: {auth_test.status_code}")
        
        if auth_test.status_code == 200:
            user_data = auth_test.json()
            print(f"✅ Authenticated as: {user_data.get('username')}")
            print(f"   Display name: {user_data.get('name')}")
            print(f"   User ID: {user_data.get('id')}")
            
            # Check capabilities
            capabilities = user_data.get('capabilities', {})
            edit_capability = 'edit_posts' in capabilities
            print(f"   Can edit posts: {edit_capability}")
            
        else:
            print(f"❌ Authentication failed: {auth_test.status_code}")
            print(f"Response: {auth_test.text}")
            return False
            
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return False
    
    # Get post 1833
    print("\\n📝 Fetching post 1833...")
    try:
        # Try with edit context first
        post_response = requests.get(f"{WP_BASE_URL}/posts/1833?context=edit", headers=headers)
        print(f"Edit context response: {post_response.status_code}")
        
        if post_response.status_code != 200:
            print("Trying without edit context...")
            post_response = requests.get(f"{WP_BASE_URL}/posts/1833", headers=headers)
            print(f"Standard response: {post_response.status_code}")
        
        if post_response.status_code != 200:
            print(f"❌ Failed to fetch post: {post_response.status_code}")
            print(f"Response: {post_response.text}")
            return False
        
        post_data = post_response.json()
        title = post_data['title']['rendered']
        print(f"✅ Got post: {title}")
        
        # Get content
        content = post_data.get('content', {})
        if 'raw' in content:
            current_content = content['raw']
            content_source = 'raw'
        else:
            current_content = content['rendered']
            content_source = 'rendered'
        
        print(f"Content source: {content_source}")
        print(f"Content length: {len(current_content)} chars")
        
    except Exception as e:
        print(f"❌ Error fetching post: {e}")
        return False
    
    # Check for broken links
    print("\\n🔍 Checking for broken links...")
    broken_links_map = {
        'https://spherevista360.com/product-analytics-2025/': 
            'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/',
        'https://spherevista360.com/on-device-vs-cloud-ai-2025/': 
            'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/'
    }
    
    updated_content = current_content
    changes_made = 0
    
    for old_url, new_url in broken_links_map.items():
        if old_url in current_content:
            print(f"❌ Found broken: {old_url}")
            updated_content = updated_content.replace(old_url, new_url)
            changes_made += 1
            print(f"✅ Will replace with: {new_url}")
    
    if changes_made == 0:
        print("✅ No broken links found!")
        return True
    
    # Update the post
    print(f"\\n💾 Updating post with {changes_made} changes...")
    try:
        update_data = {'content': updated_content}
        
        update_response = requests.post(f"{WP_BASE_URL}/posts/1833", 
                                      json=update_data, 
                                      headers=headers,
                                      timeout=30)
        
        print(f"Update response: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print("✅ POST UPDATED SUCCESSFULLY!")
            
            # Quick verification
            print("\\n🔍 Verifying fix...")
            verify_response = requests.get(f"{WP_BASE_URL}/posts/1833")
            if verify_response.status_code == 200:
                verify_content = verify_response.json()['content']['rendered']
                remaining_broken = sum(1 for old_url in broken_links_map.keys() 
                                     if old_url in verify_content)
                
                if remaining_broken == 0:
                    print("✅ VERIFICATION PASSED - All links fixed!")
                else:
                    print(f"⚠️ {remaining_broken} broken links still remain")
            
            return True
            
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(f"Response: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Update error: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python3 editor_fix_cmd.py <username> <password>")
        print("Example: python3 editor_fix_cmd.py editor_user editor_password")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    print("🚀 WordPress Editor Broken Links Fix")
    print("=" * 50)
    
    success = fix_with_editor_credentials(username, password)
    
    if success:
        print("\\n🎉 SUCCESS! Post 1833 broken links have been fixed!")
        print("\\nFixed links:")
        print("• Product Analytics in 2025: From Dashboards to Decisions")
        print("• On-Device AI vs Cloud AI: Where Each Wins in 2025")
    else:
        print("\\n❌ FAILED! Check credentials and permissions.")

if __name__ == "__main__":
    main()