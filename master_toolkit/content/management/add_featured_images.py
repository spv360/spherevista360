#!/usr/bin/env python3
"""
Add Featured Images to WordPress Posts
Uses Unsplash API for relevant stock photos
"""

import os
import requests
import time
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Category to search query mapping for Unsplash
CATEGORY_IMAGES = {
    'Finance': 'finance business money',
    'Technology': 'technology computer innovation',
    'Business': 'business meeting office',
    'Entertainment': 'entertainment media cinema',
    'Travel': 'travel destination adventure',
    'Politics': 'politics government leadership',
    'World': 'world globe international',
    'World News': 'news journalism media'
}

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"   ❌ Download error: {e}")
    return False

def upload_image_to_wordpress(image_path, title):
    """Upload image to WordPress media library"""
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/media"
    
    with open(image_path, 'rb') as f:
        files = {
            'file': (os.path.basename(image_path), f, 'image/jpeg')
        }
        headers = {
            'Content-Disposition': f'attachment; filename="{os.path.basename(image_path)}"'
        }
        
        response = requests.post(
            url,
            files=files,
            headers=headers,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        if response.status_code == 201:
            return response.json()['id']
    
    return None

def set_featured_image(post_id, media_id):
    """Set featured image for a post"""
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}"
    
    data = {
        'featured_media': media_id
    }
    
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    
    return response.status_code == 200

def get_placeholder_image_url(category, index):
    """Get placeholder image URL from Unsplash Source"""
    query = CATEGORY_IMAGES.get(category, 'business technology')
    # Using Unsplash Source for random images
    # Size: 1200x630 (optimal for featured images and social sharing)
    return f"https://source.unsplash.com/1200x630/?{query.replace(' ', ',')}&sig={index}"

def add_featured_images():
    """Add featured images to all posts without them"""
    print("=" * 60)
    print("📸 Adding Featured Images to Posts")
    print("=" * 60)
    
    # Get all posts
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = response.json()
    posts_without_images = [p for p in posts if p.get('featured_media', 0) == 0]
    
    print(f"\nFound {len(posts_without_images)} posts without featured images")
    print("=" * 60)
    
    success_count = 0
    temp_dir = '/tmp/wp_images'
    os.makedirs(temp_dir, exist_ok=True)
    
    for index, post in enumerate(posts_without_images[:20], 1):  # Limit to 20 for now
        print(f"\n[{index}/{len(posts_without_images)}] {post['title']['rendered'][:50]}...")
        
        # Get category for relevant image
        categories = post.get('categories', [])
        category_name = 'Business'  # Default
        
        if categories:
            cat_url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories/{categories[0]}"
            cat_response = requests.get(cat_url)
            if cat_response.status_code == 200:
                category_name = cat_response.json()['name']
        
        # Get image
        image_url = get_placeholder_image_url(category_name, index)
        image_path = os.path.join(temp_dir, f"featured_{post['id']}.jpg")
        
        print(f"   📥 Downloading image... ", end='')
        if download_image(image_url, image_path):
            print("✅")
            
            print(f"   📤 Uploading to WordPress... ", end='')
            media_id = upload_image_to_wordpress(image_path, post['title']['rendered'])
            
            if media_id:
                print(f"✅ (ID: {media_id})")
                
                print(f"   🖼️  Setting as featured image... ", end='')
                if set_featured_image(post['id'], media_id):
                    print("✅")
                    success_count += 1
                else:
                    print("❌")
            else:
                print("❌")
            
            # Clean up
            try:
                os.remove(image_path)
            except:
                pass
        else:
            print("❌")
        
        # Be nice to Unsplash
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"✅ Added featured images to {success_count} posts")
    print("=" * 60)

def main():
    add_featured_images()
    
    print("\n🎉 Done! Visit your site to see the featured images.")
    print(f"🌐 {WORDPRESS_URL}")

if __name__ == "__main__":
    main()
