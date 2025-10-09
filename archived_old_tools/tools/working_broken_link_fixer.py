#!/usr/bin/env python3
"""
Working Broken Link Fixer
Fix broken links using rendered content
"""

import requests
import json

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
WP_USERNAME = "admin"
WP_PASSWORD = "DTYzFB6dZS9sHNY7QM73w&@F"

# Broken links mapping
BROKEN_LINKS_MAP = {
    "https://spherevista360.com/product-analytics-2025/": "https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/",
    "https://spherevista360.com/on-device-vs-cloud-ai-2025/": "https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/"
}

def fix_broken_links_working():
    """Fix broken links using the working approach"""
    print("🔧 WORKING BROKEN LINK FIXER")
    print("=" * 40)
    
    auth = (WP_USERNAME, WP_PASSWORD)
    headers = {'Content-Type': 'application/json'}
    
    # Get all posts that might contain broken links
    response = requests.get(f"{WP_BASE_URL}/posts?per_page=50")
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = response.json()
    fixed_count = 0
    
    for post in posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        # Check if this post contains broken links
        needs_update = False
        updated_content = content
        
        for broken_link, correct_link in BROKEN_LINKS_MAP.items():
            if broken_link in content:
                updated_content = updated_content.replace(broken_link, correct_link)
                needs_update = True
                print(f"📝 Post {post_id}: {title}")
                print(f"   🔗 Replacing: {broken_link}")
                print(f"   ✅ With: {correct_link}")
        
        if needs_update:
            # Use the classic REST API approach
            update_data = {'content': updated_content}
            
            # Try the update
            try:
                update_response = requests.post(
                    f"{WP_BASE_URL}/posts/{post_id}",
                    json=update_data,
                    auth=auth,
                    headers=headers,
                    timeout=15
                )
                
                if update_response.status_code == 200:
                    print(f"   ✅ Successfully updated!")
                    fixed_count += 1
                else:
                    print(f"   ❌ Update failed: {update_response.status_code}")
                    # Try alternative method with different data structure
                    alt_data = {'content': {'raw': updated_content}}
                    alt_response = requests.post(
                        f"{WP_BASE_URL}/posts/{post_id}",
                        json=alt_data,
                        auth=auth,
                        headers=headers,
                        timeout=15
                    )
                    
                    if alt_response.status_code == 200:
                        print(f"   ✅ Successfully updated with alternative method!")
                        fixed_count += 1
                    else:
                        print(f"   ❌ Alternative method also failed: {alt_response.status_code}")
                        
            except Exception as e:
                print(f"   ❌ Error updating post: {e}")
            
            print()
    
    print(f"📊 SUMMARY:")
    print(f"Fixed {fixed_count} posts with broken links")
    
    return fixed_count

def verify_links_are_fixed():
    """Verify that the broken links have been replaced"""
    print("🔍 VERIFICATION CHECK")
    print("=" * 30)
    
    response = requests.get(f"{WP_BASE_URL}/posts?per_page=50")
    if response.status_code != 200:
        print("❌ Failed to fetch posts for verification")
        return
    
    posts = response.json()
    still_broken = 0
    
    for post in posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        for broken_link in BROKEN_LINKS_MAP.keys():
            if broken_link in content:
                still_broken += 1
                print(f"❌ Post {post_id} still contains: {broken_link}")
    
    if still_broken == 0:
        print("✅ All broken links have been fixed!")
    else:
        print(f"⚠️ {still_broken} broken links still exist")

if __name__ == "__main__":
    fixed = fix_broken_links_working()
    print()
    verify_links_are_fixed()
    
    if fixed > 0:
        print(f"\n🎉 Successfully fixed {fixed} broken links!")
    else:
        print(f"\n⚠️ No broken links were fixed - may need manual intervention")