#!/usr/bin/env python3
"""
Fix Specific Broken Links
Fix the identified broken links with correct URLs
"""

import requests
import json

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
WP_USERNAME = "admin"
WP_PASSWORD = "DTYzFB6dZS9sHNY7QM73w&@F"

# Broken links mapping to correct URLs
BROKEN_LINKS_MAP = {
    "https://spherevista360.com/product-analytics-2025/": "https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/",
    "https://spherevista360.com/on-device-vs-cloud-ai-2025/": "https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/"
}

# Posts that need fixing based on our search
POSTS_TO_FIX = [
    {
        'post_id': 1838,
        'title': 'Ops Copilots: Automating Work That Scales Businesses',
        'broken_link': 'https://spherevista360.com/product-analytics-2025/'
    },
    {
        'post_id': 1833,
        'title': 'How AI Recommenders Shape Your Streaming Experience',
        'broken_link': 'https://spherevista360.com/product-analytics-2025/'
    },
    {
        'post_id': 1832,
        'title': 'Hollywood\'s AI Moment: How VFX Pipelines Are Changing',
        'broken_link': 'https://spherevista360.com/on-device-vs-cloud-ai-2025/'
    }
]

def fix_broken_links():
    """Fix broken links in identified posts"""
    auth = (WP_USERNAME, WP_PASSWORD)
    headers = {'Content-Type': 'application/json'}
    
    print("🔧 FIXING BROKEN LINKS")
    print("=" * 40)
    
    fixed_count = 0
    
    for post_info in POSTS_TO_FIX:
        post_id = post_info['post_id']
        title = post_info['title']
        broken_link = post_info['broken_link']
        correct_link = BROKEN_LINKS_MAP[broken_link]
        
        print(f"📝 Fixing Post {post_id}: {title}")
        print(f"   🔗 Replacing: {broken_link}")
        print(f"   ✅ With: {correct_link}")
        
        # Get current post content
        try:
            response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
            if response.status_code == 200:
                post_data = response.json()
                current_content = post_data['content']['rendered']
                
                # Replace the broken link
                if broken_link in current_content:
                    updated_content = current_content.replace(broken_link, correct_link)
                    
                    # Update the post
                    update_data = {
                        'content': updated_content
                    }
                    
                    update_response = requests.post(
                        f"{WP_BASE_URL}/posts/{post_id}",
                        json=update_data,
                        auth=auth,
                        headers=headers
                    )
                    
                    if update_response.status_code == 200:
                        print(f"   ✅ Successfully updated!")
                        fixed_count += 1
                    else:
                        print(f"   ❌ Failed to update: {update_response.status_code}")
                        print(f"   Error: {update_response.text[:200]}")
                else:
                    print(f"   ⚠️ Broken link not found in current content")
                    
            else:
                print(f"   ❌ Failed to fetch post: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print(f"📊 SUMMARY:")
    print(f"Fixed {fixed_count} out of {len(POSTS_TO_FIX)} posts")
    
    if fixed_count == len(POSTS_TO_FIX):
        print("✅ ALL BROKEN LINKS SUCCESSFULLY FIXED!")
    else:
        print(f"⚠️ {len(POSTS_TO_FIX) - fixed_count} posts still need attention")

def verify_fixes():
    """Verify that the links have been fixed"""
    print("\n🔍 VERIFYING FIXES")
    print("=" * 30)
    
    for post_info in POSTS_TO_FIX:
        post_id = post_info['post_id']
        broken_link = post_info['broken_link']
        correct_link = BROKEN_LINKS_MAP[broken_link]
        
        try:
            response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
            if response.status_code == 200:
                post_data = response.json()
                content = post_data['content']['rendered']
                
                has_broken = broken_link in content
                has_correct = correct_link in content
                
                print(f"Post {post_id}:")
                if not has_broken and has_correct:
                    print(f"   ✅ Fixed successfully")
                elif has_broken:
                    print(f"   ❌ Still contains broken link")
                else:
                    print(f"   ⚠️ Neither old nor new link found")
                    
        except Exception as e:
            print(f"Post {post_id}: ❌ Error verifying - {e}")

if __name__ == "__main__":
    fix_broken_links()
    verify_fixes()