#!/usr/bin/env python3
"""
Direct WordPress API Image URL Fixer
Updates post content directly through REST API
"""

import requests
import base64
import os
import re

def fix_post_images():
    """Fix images using direct WordPress REST API calls"""
    
    # WordPress credentials
    wp_site = os.environ.get('WP_SITE', 'https://spherevista360.com').rstrip('/')
    wp_user = input("Enter WordPress username: ")
    wp_pass = input("Enter application password: ")
    
    # Authentication
    credentials = f"{wp_user}:{wp_pass}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    # URL mappings for broken to working images
    url_fixes = {
        "photo-1559589688-f26e20a6c987?ixlib=rb-4.0.3&": "photo-1559126961-cc431cc43e55?",
        "photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&": "photo-1555949963-aa79dcee981c?",
        "photo-1489599904335-1f69ba4d43da?ixlib=rb-4.0.3&": "photo-1594736797933-d0401ba2fe65?"
    }
    
    # Posts to fix
    posts_to_fix = [1827, 1828, 1829, 1830, 1831, 1832, 1833]
    
    print("🔧 FIXING IMAGES VIA DIRECT API")
    print("=" * 50)
    
    fixed_count = 0
    
    for post_id in posts_to_fix:
        try:
            # Get current post
            url = f"{wp_site}/wp-json/wp/v2/posts/{post_id}"
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"❌ Failed to get post {post_id}: {response.status_code}")
                continue
                
            post_data = response.json()
            original_content = post_data['content']['raw']
            updated_content = original_content
            
            print(f"🔍 Processing post {post_id}: {post_data['title']['raw'][:50]}...")
            
            # Apply fixes
            changes_made = False
            for broken_pattern, fixed_pattern in url_fixes.items():
                if broken_pattern in updated_content:
                    # Replace the broken URL pattern
                    updated_content = re.sub(
                        r'auto=format&fit=crop&w=1600&h=900&q=80',
                        'auto=format&fit=crop&w=800&h=500&q=80',
                        updated_content.replace(broken_pattern, fixed_pattern)
                    )
                    changes_made = True
                    print(f"   ✅ Fixed image URL pattern")
            
            # Update post if changes were made
            if changes_made:
                update_data = {
                    'content': updated_content
                }
                
                update_response = requests.post(url, headers=headers, json=update_data)
                
                if update_response.status_code == 200:
                    print(f"   ✅ Post {post_id} updated successfully")
                    fixed_count += 1
                else:
                    print(f"   ❌ Failed to update post {post_id}: {update_response.status_code}")
            else:
                print(f"   ℹ️ No broken images found in post {post_id}")
                
        except Exception as e:
            print(f"❌ Error processing post {post_id}: {e}")
    
    print(f"\n📊 SUMMARY: Successfully fixed {fixed_count} posts")
    return fixed_count

if __name__ == "__main__":
    fix_post_images()