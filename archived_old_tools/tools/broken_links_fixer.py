#!/usr/bin/env python3
"""
Broken Links Fixer
Fix the identified broken links by replacing them with correct URLs
"""

import requests
import json
import getpass
import re

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Link fixes to apply
LINK_FIXES = {
    # visa-free-destinations-2025 -> existing post about visa-free destinations
    "https://spherevista360.com/visa-free-destinations-2025/": 
        "https://spherevista360.com/top-visa-free-destinations-for-2025-travelers/",
    
    # digital-banking-2025 -> existing post about digital banking
    "https://spherevista360.com/digital-banking-2025/": 
        "https://spherevista360.com/digital-banking-revolution-the-future-of-fintech/"
}

# Posts that need fixing based on our analysis
POSTS_TO_FIX = [1836, 1834, 1827]  # Posts that contain the broken links

def authenticate():
    """Get WordPress credentials"""
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    return username, app_password

def get_post_content(post_id, auth):
    """Get post content from WordPress"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    response = requests.get(url, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching post {post_id}: {response.status_code}")
        return None

def update_post_content(post_id, new_content, auth):
    """Update post content in WordPress"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {
        'content': new_content
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=data, auth=auth, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print(f"Error updating post {post_id}: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def fix_broken_links_in_content(content):
    """Replace broken links with correct links in content"""
    updated_content = content
    fixes_made = []
    
    for broken_link, correct_link in LINK_FIXES.items():
        if broken_link in content:
            updated_content = updated_content.replace(broken_link, correct_link)
            fixes_made.append((broken_link, correct_link))
    
    return updated_content, fixes_made

def main():
    """Main function to fix broken links"""
    print("Broken Links Fixer")
    print("=" * 40)
    print("Fixing broken internal links in posts...")
    print()
    
    # Show planned fixes
    print("PLANNED LINK FIXES:")
    print("-" * 30)
    for broken, correct in LINK_FIXES.items():
        print(f"❌ {broken}")
        print(f"✅ {correct}")
        print()
    
    # Get authentication
    auth = authenticate()
    
    total_fixes = 0
    total_posts_updated = 0
    
    for post_id in POSTS_TO_FIX:
        print(f"\nChecking Post {post_id}...")
        
        # Get post data
        post_data = get_post_content(post_id, auth)
        if not post_data:
            continue
        
        title = post_data.get('title', {}).get('rendered', '')
        content = post_data.get('content', {}).get('rendered', '')
        
        print(f"  Title: {title}")
        
        # Fix broken links
        updated_content, fixes_made = fix_broken_links_in_content(content)
        
        if fixes_made:
            print(f"  Found {len(fixes_made)} broken links to fix:")
            for broken, correct in fixes_made:
                print(f"    ❌ {broken}")
                print(f"    ✅ {correct}")
            
            # Update the post
            if update_post_content(post_id, updated_content, auth):
                print(f"  ✅ Successfully updated post {post_id}")
                total_fixes += len(fixes_made)
                total_posts_updated += 1
            else:
                print(f"  ❌ Failed to update post {post_id}")
        else:
            print(f"  ℹ️ No broken links found in post {post_id}")
    
    # Summary
    print(f"\n" + "=" * 40)
    print("BROKEN LINKS FIX SUMMARY")
    print("=" * 40)
    print(f"Posts updated: {total_posts_updated}")
    print(f"Total link fixes: {total_fixes}")
    
    if total_fixes > 0:
        print(f"\n🎉 Successfully fixed {total_fixes} broken links!")
        print("The reported broken links should now be resolved.")
    else:
        print(f"\n⚠️ No broken links were found to fix.")
    
    print(f"\nNext steps:")
    print("1. Test the fixed links to ensure they work")
    print("2. Run a site-wide link check to find any other broken links")
    print("3. Consider setting up 301 redirects for the original broken URLs")

if __name__ == "__main__":
    main()