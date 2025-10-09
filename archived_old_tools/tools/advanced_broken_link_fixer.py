#!/usr/bin/env python3
"""
Fix Broken Links with Application Password Authentication
"""

import requests
import json
import base64

# WordPress configuration with Application Password
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
WP_USERNAME = "admin"
# Application password format: username:password
WP_APP_PASSWORD = "DTYzFB6dZS9sHNY7QM73w&@F"

# Broken links mapping
BROKEN_LINKS_MAP = {
    "https://spherevista360.com/product-analytics-2025/": "https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/",
    "https://spherevista360.com/on-device-vs-cloud-ai-2025/": "https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/"
}

POSTS_TO_FIX = [1838, 1833, 1832]

def get_auth_header():
    """Generate Basic Auth header"""
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

def fix_broken_links_advanced():
    """Fix broken links with multiple authentication attempts"""
    print("🔧 ADVANCED BROKEN LINK FIXER")
    print("=" * 40)
    
    headers = {
        "Content-Type": "application/json",
        **get_auth_header()
    }
    
    fixed_count = 0
    
    for post_id in POSTS_TO_FIX:
        print(f"📝 Processing Post {post_id}")
        
        try:
            # Get current post
            response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
            if response.status_code != 200:
                print(f"   ❌ Failed to fetch post: {response.status_code}")
                continue
                
            post_data = response.json()
            title = post_data['title']['rendered']
            current_content = post_data['content']['raw']  # Get raw content
            
            print(f"   Title: {title}")
            
            # Check for broken links and replace
            updated_content = current_content
            replacements_made = 0
            
            for broken_link, correct_link in BROKEN_LINKS_MAP.items():
                if broken_link in updated_content:
                    updated_content = updated_content.replace(broken_link, correct_link)
                    replacements_made += 1
                    print(f"   🔗 Replaced: {broken_link}")
                    print(f"   ✅ With: {correct_link}")
            
            if replacements_made > 0:
                # Update the post
                update_data = {"content": updated_content}
                
                # Try multiple update methods
                methods = [
                    ("POST", f"{WP_BASE_URL}/posts/{post_id}"),
                    ("PUT", f"{WP_BASE_URL}/posts/{post_id}"),
                ]
                
                success = False
                for method, url in methods:
                    try:
                        if method == "POST":
                            update_response = requests.post(url, json=update_data, headers=headers, timeout=10)
                        else:
                            update_response = requests.put(url, json=update_data, headers=headers, timeout=10)
                        
                        if update_response.status_code in [200, 201]:
                            print(f"   ✅ Successfully updated with {method}!")
                            fixed_count += 1
                            success = True
                            break
                        else:
                            print(f"   ⚠️ {method} failed: {update_response.status_code}")
                            
                    except Exception as e:
                        print(f"   ⚠️ {method} error: {e}")
                
                if not success:
                    print(f"   ❌ All update methods failed")
                    # Show last response for debugging
                    print(f"   Last response: {update_response.text[:200]}")
            else:
                print(f"   ℹ️ No broken links found in this post")
                
        except Exception as e:
            print(f"   ❌ Error processing post: {e}")
        
        print()
    
    print(f"📊 FINAL SUMMARY:")
    print(f"Successfully fixed {fixed_count} out of {len(POSTS_TO_FIX)} posts")
    
    return fixed_count

if __name__ == "__main__":
    fixed = fix_broken_links_advanced()
    
    if fixed > 0:
        print(f"\n🎉 {fixed} posts updated successfully!")
        print("✅ Broken links have been replaced with working URLs")
    else:
        print("\n⚠️ No posts were updated")
        print("This might be due to authentication issues or the links may have already been fixed")