#!/usr/bin/env python3
"""
Fix Broken Links in Post 1831
Replace broken links with correct working URLs
"""

import requests
import base64

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def fix_post_1831(username, password):
    """Fix broken links in post 1831"""
    print("🔧 FIXING POST 1831 BROKEN LINKS")
    print("=" * 50)
    
    # Create authentication headers
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # Get post 1831
    print("📝 Fetching post 1831...")
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
    
    # Define broken links and their replacements
    broken_links_map = {
        'https://spherevista360.com/open-source-models-2025/': 
            'https://spherevista360.com/open-source-ai-models-in-the-enterprise-build-buy-or-blend/',
        'https://spherevista360.com/startup-funding-2025/': 
            'https://spherevista360.com/startup-funding-trends-and-investor-sentiment-in-2025/'
    }
    
    # Check for broken links and make replacements
    print("\\n🔍 Checking for broken links...")
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
        
        update_response = requests.post(f"{WP_BASE_URL}/posts/1831", 
                                      json=update_data, 
                                      headers=headers,
                                      timeout=30)
        
        print(f"Update response: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print("✅ POST 1831 UPDATED SUCCESSFULLY!")
            
            # Verify the fix
            print("\\n🔍 Verifying fix...")
            verify_response = requests.get(f"{WP_BASE_URL}/posts/1831")
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

if __name__ == "__main__":
    print("🚀 Post 1831 Broken Links Fixer")
    print("=" * 40)
    
    # Use the same credentials that worked for post 1833
    print("Enter your editor credentials (same as used for post 1833):")
    import getpass
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    
    success = fix_post_1831(username, password)
    
    if success:
        print("\\n🎉 SUCCESS! Post 1831 broken links have been fixed!")
        print("\\nFixed links:")
        print("• Enterprise AI Models: Build, Buy, or Blend Strategy")
        print("• Startup Funding Trends and Investor Sentiment in 2025")
    else:
        print("\\n❌ FAILED! Check credentials and permissions.")