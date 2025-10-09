#!/usr/bin/env python3
"""
WordPress Image URL Fixer
Fix broken Unsplash URLs in WordPress posts by replacing them with working alternatives
"""

import requests
import re
import json
import html
from urllib.parse import unquote
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Contextual image mappings for different categories
IMAGE_REPLACEMENTS = {
    # Finance-related images
    'finance': [
        'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1600&h=900&q=80',  # Financial charts
        'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1600&h=900&q=80',  # Coins/money
        'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1600&h=900&q=80',  # Business/finance
    ],
    
    # Technology-related images
    'technology': [
        'https://images.unsplash.com/photo-1518709268805-4e9042af2176?auto=format&fit=crop&w=1600&h=900&q=80',  # Tech/code
        'https://images.unsplash.com/photo-1561736778-92e52a7769ef?auto=format&fit=crop&w=1600&h=900&q=80',  # Digital/tech
        'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&h=900&q=80',  # Modern tech
    ],
    
    # Entertainment-related images
    'entertainment': [
        'https://images.unsplash.com/photo-1489599328014-0312ad08c5a4?auto=format&fit=crop&w=1600&h=900&q=80',  # Entertainment/media
        'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?auto=format&fit=crop&w=1600&h=900&q=80',  # Entertainment
        'https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?auto=format&fit=crop&w=1600&h=900&q=80',  # Media/entertainment
    ],
    
    # World/General news images
    'world': [
        'https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?auto=format&fit=crop&w=1600&h=900&q=80',  # World/global
        'https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=1600&h=900&q=80',  # Global perspective
        'https://images.unsplash.com/photo-1597149496772-2ba4b8c5e6e3?auto=format&fit=crop&w=1600&h=900&q=80',  # World view
    ]
}

# Pattern to identify broken Unsplash URLs
BROKEN_URL_PATTERN = r'https://images\.unsplash\.com/[^"\s]*ixlib=rb-4\.0\.3[^"\s]*'

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
    """Replace broken Unsplash URLs with working alternatives"""
    # Find all broken URLs
    broken_urls = re.findall(BROKEN_URL_PATTERN, content)
    
    if not broken_urls:
        return content, 0
    
    # Get replacement images for the category
    replacements = IMAGE_REPLACEMENTS.get(category, IMAGE_REPLACEMENTS['world'])
    
    # Replace each broken URL
    fixed_content = content
    replacements_made = 0
    
    for i, broken_url in enumerate(broken_urls):
        # Use modulo to cycle through available replacements
        replacement_url = replacements[i % len(replacements)]
        
        # Replace the broken URL
        fixed_content = fixed_content.replace(broken_url, replacement_url)
        replacements_made += 1
        
        print(f"  Replaced broken URL {i+1}: {broken_url[:80]}...")
        print(f"  With working URL: {replacement_url}")
    
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
    print("WordPress Broken Image URL Fixer")
    print("=================================")
    
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
            print(f"  No broken URLs found in post {post_id}")
    
    print(f"\n=================================")
    print(f"Total broken URLs fixed: {total_fixes}")
    print("Image URL fixing complete!")

if __name__ == "__main__":
    main()