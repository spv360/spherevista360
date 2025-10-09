#!/usr/bin/env python3
"""
Broken Links Verification
Verify that the broken links have been successfully fixed
"""

import requests
import re

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Previously broken URLs that should now be fixed
PREVIOUSLY_BROKEN = [
    "https://spherevista360.com/visa-free-destinations-2025/",
    "https://spherevista360.com/digital-banking-2025/"
]

# Replacement URLs that should now be used
REPLACEMENT_URLS = [
    "https://spherevista360.com/top-visa-free-destinations-for-2025-travelers/",
    "https://spherevista360.com/digital-banking-revolution-the-future-of-fintech/"
]

# Posts that were updated
UPDATED_POSTS = [1836, 1834, 1827]

def check_url_status(url):
    """Check if a URL is working"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code == 200, response.status_code
    except Exception as e:
        return False, str(e)

def check_post_for_broken_links(post_id):
    """Check if a post still contains broken links"""
    try:
        response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
        if response.status_code == 200:
            post_data = response.json()
            content = post_data.get('content', {}).get('rendered', '')
            title = post_data.get('title', {}).get('rendered', '')
            
            # Check for previously broken URLs
            broken_links_found = []
            for broken_url in PREVIOUSLY_BROKEN:
                if broken_url in content:
                    broken_links_found.append(broken_url)
            
            # Check for replacement URLs
            replacement_links_found = []
            for replacement_url in REPLACEMENT_URLS:
                if replacement_url in content:
                    replacement_links_found.append(replacement_url)
            
            return {
                'post_id': post_id,
                'title': title,
                'broken_links': broken_links_found,
                'replacement_links': replacement_links_found,
                'success': len(broken_links_found) == 0
            }
    except Exception as e:
        return {'error': f'Error checking post {post_id}: {e}'}
    
    return None

def main():
    """Verify broken links fixes"""
    print("Broken Links Verification")
    print("=" * 40)
    print("Verifying that broken links have been fixed...")
    print()
    
    # First, verify the replacement URLs are working
    print("1. CHECKING REPLACEMENT URLs:")
    print("-" * 30)
    
    all_replacements_working = True
    for url in REPLACEMENT_URLS:
        is_working, status = check_url_status(url)
        status_icon = "✅" if is_working else "❌"
        print(f"{status_icon} {url} - Status: {status}")
        if not is_working:
            all_replacements_working = False
    
    print()
    
    # Check that posts no longer contain broken links
    print("2. CHECKING UPDATED POSTS:")
    print("-" * 30)
    
    all_posts_fixed = True
    total_broken_remaining = 0
    total_replacements_found = 0
    
    for post_id in UPDATED_POSTS:
        result = check_post_for_broken_links(post_id)
        
        if result and 'error' not in result:
            broken_count = len(result['broken_links'])
            replacement_count = len(result['replacement_links'])
            
            total_broken_remaining += broken_count
            total_replacements_found += replacement_count
            
            status_icon = "✅" if result['success'] else "❌"
            print(f"{status_icon} Post {post_id}: {result['title'][:50]}...")
            
            if broken_count > 0:
                print(f"    ❌ Still contains {broken_count} broken links:")
                for broken in result['broken_links']:
                    print(f"      - {broken}")
                all_posts_fixed = False
            
            if replacement_count > 0:
                print(f"    ✅ Contains {replacement_count} replacement links:")
                for replacement in result['replacement_links']:
                    print(f"      - {replacement}")
            
            if broken_count == 0 and replacement_count == 0:
                print(f"    ℹ️ No links from our fix list found in this post")
        else:
            print(f"❌ Could not check post {post_id}: {result.get('error', 'Unknown error')}")
            all_posts_fixed = False
        
        print()
    
    # Summary
    print("=" * 40)
    print("VERIFICATION SUMMARY")
    print("=" * 40)
    
    if all_replacements_working and all_posts_fixed and total_broken_remaining == 0:
        print("🎉 ALL BROKEN LINKS SUCCESSFULLY FIXED!")
        print(f"✅ All {len(REPLACEMENT_URLS)} replacement URLs are working")
        print(f"✅ {len(UPDATED_POSTS)} posts updated successfully")
        print(f"✅ {total_replacements_found} working replacement links found")
        print(f"✅ 0 broken links remaining")
    else:
        print("⚠️ VERIFICATION RESULTS:")
        print(f"Replacement URLs working: {all_replacements_working}")
        print(f"Posts successfully fixed: {all_posts_fixed}")
        print(f"Broken links remaining: {total_broken_remaining}")
        print(f"Replacement links found: {total_replacements_found}")
    
    print(f"\nRECOMMENDATIONS:")
    if total_broken_remaining == 0:
        print("✅ No further action needed for these specific broken links")
        print("✅ Consider running a full site link audit to check for other issues")
    else:
        print("❌ Some broken links may still exist - manual review required")
    
    print("✅ Set up 301 redirects for the broken URLs to prevent future issues")

if __name__ == "__main__":
    main()