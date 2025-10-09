#!/usr/bin/env python3
"""
Broken Links Verification Tool
Check if broken links have been fixed
"""

import requests

# URLs to check
BROKEN_URLS = [
    "https://spherevista360.com/product-analytics-2025/",
    "https://spherevista360.com/on-device-vs-cloud-ai-2025/"
]

CORRECT_URLS = [
    "https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/",
    "https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/"
]

POSTS_TO_CHECK = [1838, 1833, 1832]

def verify_broken_links_status():
    """Check if the broken links have been fixed"""
    print("🔍 BROKEN LINKS VERIFICATION")
    print("=" * 40)
    
    WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
    
    broken_links_found = 0
    posts_checked = 0
    
    for post_id in POSTS_TO_CHECK:
        try:
            response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
            if response.status_code == 200:
                post = response.json()
                title = post['title']['rendered']
                content = post['content']['rendered']
                posts_checked += 1
                
                print(f"📝 Post {post_id}: {title}")
                
                # Check for broken links
                post_has_broken = False
                for broken_url in BROKEN_URLS:
                    if broken_url in content:
                        print(f"   ❌ Still contains: {broken_url}")
                        broken_links_found += 1
                        post_has_broken = True
                
                # Check for correct links
                for correct_url in CORRECT_URLS:
                    if correct_url in content:
                        print(f"   ✅ Contains correct link: {correct_url}")
                
                if not post_has_broken:
                    print(f"   ✅ No broken links found")
                
                print()
                
        except Exception as e:
            print(f"❌ Error checking post {post_id}: {e}")
    
    print("📊 VERIFICATION SUMMARY:")
    print(f"Posts checked: {posts_checked}")
    print(f"Broken links found: {broken_links_found}")
    
    if broken_links_found == 0:
        print("\n🎉 SUCCESS! All broken links have been fixed!")
        print("✅ No broken URLs found in any posts")
    else:
        print(f"\n⚠️ {broken_links_found} broken links still need to be fixed")
        print("Please complete the manual fixes as described in the report")

def verify_target_urls():
    """Verify that target URLs are working"""
    print("\n🌐 TARGET URL VERIFICATION:")
    print("-" * 30)
    
    for url in CORRECT_URLS:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url}")
            else:
                print(f"⚠️ {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

if __name__ == "__main__":
    verify_broken_links_status()
    verify_target_urls()