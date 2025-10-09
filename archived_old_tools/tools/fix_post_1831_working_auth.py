#!/usr/bin/env python3
"""
Fix Post 1831 with Working Auth Method
Use the same method that successfully fixed post 1833
"""

import requests
import base64

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def fix_post_1831_same_auth():
    """Fix post 1831 using the same auth that worked for 1833"""
    print("🔧 FIXING POST 1831 BROKEN LINKS")
    print("=" * 50)
    print("Using the same authentication method that worked for post 1833...")
    
    # Use the working credentials (JK user that worked before)
    username = "JK"
    
    # Get password
    import getpass
    password = getpass.getpass("Enter JK user password: ")
    
    # Create authentication headers
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # Test auth first
    print("\\n🔐 Testing authentication...")
    try:
        auth_test = requests.get(f"{WP_BASE_URL}/users/me", headers=headers)
        if auth_test.status_code == 200:
            print("✅ Authentication successful")
        else:
            print(f"❌ Auth failed: {auth_test.status_code}")
            return False
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return False
    
    # Get post 1831
    print("\\n📝 Fetching post 1831...")
    try:
        post_response = requests.get(f"{WP_BASE_URL}/posts/1831?context=edit", headers=headers)
        
        if post_response.status_code != 200:
            post_response = requests.get(f"{WP_BASE_URL}/posts/1831", headers=headers)
        
        if post_response.status_code != 200:
            print(f"❌ Failed to fetch post: {post_response.status_code}")
            return False
        
        post_data = post_response.json()
        title = post_data['title']['rendered']
        print(f"✅ Got post: {title}")
        
        # Get content - same way as post 1833
        content = post_data.get('content', {})
        if 'raw' in content and content['raw']:
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
    
    # Check and replace broken links
    print("\\n🔍 Checking for broken links...")
    
    broken_links_map = {
        'https://spherevista360.com/open-source-models-2025/': 
            'https://spherevista360.com/open-source-ai-models-in-the-enterprise-build-buy-or-blend/',
        'https://spherevista360.com/startup-funding-2025/': 
            'https://spherevista360.com/startup-funding-trends-and-investor-sentiment-in-2025/'
    }
    
    updated_content = current_content
    changes_made = 0
    
    for old_url, new_url in broken_links_map.items():
        if old_url in current_content:
            print(f"❌ Found: {old_url}")
            updated_content = updated_content.replace(old_url, new_url)
            changes_made += 1
            print(f"✅ Replace with: {new_url}")
    
    if changes_made == 0:
        print("✅ No broken links found!")
        return True
    
    # Update the post
    print(f"\\n💾 Updating post with {changes_made} changes...")
    try:
        update_data = {'content': updated_content}
        
        update_response = requests.post(f"{WP_BASE_URL}/posts/1831", 
                                      json=update_data, 
                                      headers=headers,
                                      timeout=30)
        
        print(f"Update status: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print("✅ POST 1831 UPDATED SUCCESSFULLY!")
            return True
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(f"Error: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Update error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Fix Post 1831 - Same Auth Method")
    print("=" * 50)
    
    success = fix_post_1831_same_auth()
    
    if success:
        print("\\n🎉 SUCCESS! Post 1831 fixed!")
        print("\\nReplaced broken links:")
        print("• open-source-models-2025 → Enterprise AI Models")
        print("• startup-funding-2025 → Startup Funding Trends")
    else:
        print("\\n❌ Fix failed")