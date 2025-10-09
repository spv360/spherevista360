#!/usr/bin/env python3
"""
WordPress Image URL Fixer - Final Fix
Fix broken Unsplash URLs with verified working alternatives
"""

import requests
import re
import json
import html
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# VERIFIED working image replacements for different categories
IMAGE_REPLACEMENTS = {
    # Finance-related images (VERIFIED WORKING)
    'finance': [
        'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1600&h=900&q=80',  # Financial charts - WORKING
        'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1600&h=900&q=80',  # Coins/money - WORKING
        'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1600&h=900&q=80',  # Business/finance - WORKING
    ],
    
    # Technology-related images (VERIFIED WORKING)
    'technology': [
        'https://images.unsplash.com/photo-1561736778-92e52a7769ef?auto=format&fit=crop&w=1600&h=900&q=80',  # Digital/tech - WORKING
        'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&h=900&q=80',  # Modern tech - WORKING
        'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1600&h=900&q=80',  # Tech workspace - WORKING
    ],
    
    # Entertainment-related images (VERIFIED WORKING)
    'entertainment': [
        'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?auto=format&fit=crop&w=1600&h=900&q=80',  # Entertainment - WORKING
        'https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?auto=format&fit=crop&w=1600&h=900&q=80',  # Media/entertainment - WORKING
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1600&h=900&q=80',  # Entertainment/media - WORKING
    ],
    
    # World/General news images (VERIFIED WORKING)
    'world': [
        'https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?auto=format&fit=crop&w=1600&h=900&q=80',  # World/global - WORKING
        'https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=1600&h=900&q=80',  # Global perspective - WORKING
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1600&h=900&q=80',  # World view - WORKING
    ]
}

def authenticate():
    """Get WordPress credentials"""
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    return username, app_password

def test_url(url):
    """Test if a URL is working"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def get_post_content(post_id, auth):
    """Get post content from WordPress"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    response = requests.get(url, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching post {post_id}: {response.status_code}")
        return None

def detect_category(content):
    """Detect the category of content based on keywords"""
    content_lower = content.lower()
    
    # Finance keywords
    if any(word in content_lower for word in ['finance', 'money', 'investment', 'financial', 'economy', 'market', 'trading', 'business']):
        return 'finance'
    
    # Technology keywords
    elif any(word in content_lower for word in ['technology', 'tech', 'digital', 'software', 'ai', 'artificial intelligence', 'computer', 'innovation']):
        return 'technology'
    
    # Entertainment keywords
    elif any(word in content_lower for word in ['entertainment', 'movie', 'film', 'music', 'celebrity', 'hollywood', 'show', 'media']):
        return 'entertainment'
    
    # Default to world category
    else:
        return 'world'

def fix_broken_urls(content, category='world'):
    """Replace ALL problematic Unsplash URLs with verified working alternatives"""
    # Pattern to find ANY Unsplash URL that might be problematic
    all_unsplash_pattern = r'https://images\.unsplash\.com/[^"\s]*'
    
    # Find all Unsplash URLs
    all_urls = re.findall(all_unsplash_pattern, content)
    
    if not all_urls:
        return content, 0
    
    # Get replacement images for the category
    replacements = IMAGE_REPLACEMENTS.get(category, IMAGE_REPLACEMENTS['world'])
    
    # Replace each URL
    fixed_content = content
    replacements_made = 0
    
    for i, url in enumerate(all_urls):
        # Check if URL is working
        if not test_url(url):
            # Use modulo to cycle through available replacements
            replacement_url = replacements[i % len(replacements)]
            
            # Replace the broken URL
            # Handle both regular and HTML-encoded URLs
            encoded_url = url.replace('&', '&#038;')
            
            fixed_content = fixed_content.replace(url, replacement_url)
            fixed_content = fixed_content.replace(encoded_url, replacement_url)
            replacements_made += 1
            
            print(f"  Replaced broken URL {i+1}: {url[:60]}...")
            print(f"  With working URL: {replacement_url}")
        else:
            print(f"  URL {i+1} is working: {url[:60]}...")
    
    return fixed_content, replacements_made

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

def main():
    """Main function to fix broken image URLs"""
    print("WordPress Broken Image URL Fixer - Final Fix")
    print("============================================")
    
    # Test our replacement URLs first
    print("Testing replacement URLs...")
    all_replacements = []
    for category, urls in IMAGE_REPLACEMENTS.items():
        all_replacements.extend(urls)
    
    working_urls = 0
    for url in all_replacements:
        if test_url(url):
            working_urls += 1
            print(f"✅ {url}")
        else:
            print(f"❌ {url}")
    
    print(f"\n{working_urls}/{len(all_replacements)} replacement URLs are working")
    
    if working_urls < len(all_replacements):
        print("Some replacement URLs are broken. Please fix them first.")
        return
    
    # Get authentication
    auth = authenticate()
    
    # Post IDs to check (from recent publishing)
    post_ids = [1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838]
    
    total_fixes = 0
    
    for post_id in post_ids:
        print(f"\nChecking post {post_id}...")
        
        # Get post data
        post_data = get_post_content(post_id, auth)
        if not post_data:
            continue
        
        # Get the rendered content
        content = post_data.get('content', {}).get('rendered', '')
        if not content:
            print(f"  No content found for post {post_id}")
            continue
        
        # Decode HTML entities
        content = html.unescape(content)
        
        # Detect category
        category = detect_category(content)
        print(f"  Detected category: {category}")
        
        # Fix broken URLs
        fixed_content, fixes_made = fix_broken_urls(content, category)
        
        if fixes_made > 0:
            print(f"  Found and fixed {fixes_made} broken URLs")
            
            # Update the post
            if update_post_content(post_id, fixed_content, auth):
                print(f"  ✓ Successfully updated post {post_id}")
                total_fixes += fixes_made
            else:
                print(f"  ✗ Failed to update post {post_id}")
        else:
            print(f"  All URLs in post {post_id} are working")
    
    print(f"\n============================================")
    print(f"Total broken URLs fixed: {total_fixes}")
    print("Final image URL fixing complete!")

if __name__ == "__main__":
    main()