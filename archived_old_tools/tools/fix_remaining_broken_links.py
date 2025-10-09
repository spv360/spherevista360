#!/usr/bin/env python3
"""
Fix Remaining Broken Links - Posts 1838 and 1832
Using working authentication method
"""

import requests
import base64
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def fix_remaining_posts():
    """Fix broken links in posts 1838 and 1832"""
    print("🔧 FIXING REMAINING BROKEN LINKS")
    print("=" * 50)
    
    # Use working credentials
    username = "JK"
    password = getpass.getpass("Enter JK user password: ")
    
    # Create auth headers
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # Posts to fix with their broken links
    posts_to_fix = {
        1838: {
            'broken_links': {
                'https://spherevista360.com/product-analytics-2025/': 
                    'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/'
            }
        },
        1832: {
            'broken_links': {
                'https://spherevista360.com/on-device-vs-cloud-ai-2025/': 
                    'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/'
            }
        }
    }
    
    fixed_count = 0
    
    for post_id, fix_data in posts_to_fix.items():
        print(f"\\n📝 Processing Post {post_id}...")
        
        try:
            # Get post
            post_response = requests.get(f"{WP_BASE_URL}/posts/{post_id}?context=edit", headers=headers)
            
            if post_response.status_code != 200:
                post_response = requests.get(f"{WP_BASE_URL}/posts/{post_id}", headers=headers)
            
            if post_response.status_code != 200:
                print(f"❌ Failed to fetch post {post_id}")
                continue
            
            post_data = post_response.json()
            title = post_data['title']['rendered']
            print(f"Title: {title}")
            
            # Get content
            content = post_data.get('content', {})
            if 'raw' in content and content['raw']:
                current_content = content['raw']
            else:
                current_content = content['rendered']
            
            # Make replacements
            updated_content = current_content
            changes = 0
            
            for old_url, new_url in fix_data['broken_links'].items():
                if old_url in current_content:
                    updated_content = updated_content.replace(old_url, new_url)
                    changes += 1
                    print(f"✅ Will replace: {old_url}")
                    print(f"   With: {new_url}")
            
            if changes == 0:
                print(f"✅ No broken links found in post {post_id}")
                continue
            
            # Update post
            update_data = {'content': updated_content}
            update_response = requests.post(f"{WP_BASE_URL}/posts/{post_id}", 
                                          json=update_data, 
                                          headers=headers)
            
            if update_response.status_code == 200:
                print(f"✅ Post {post_id} updated successfully!")
                fixed_count += 1
            else:
                print(f"❌ Post {post_id} update failed: {update_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error processing post {post_id}: {e}")
    
    return fixed_count

if __name__ == "__main__":
    fixed = fix_remaining_posts()
    print(f"\\n📊 SUMMARY: Fixed {fixed} posts")
    
    if fixed > 0:
        print("✅ Remaining broken links have been fixed!")
    else:
        print("⚠️ No posts were updated")