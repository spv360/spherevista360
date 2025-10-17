#!/usr/bin/env python3
"""
Add Featured Images to WordPress Posts using Lorem Picsum
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

def download_placeholder_image(post_id):
    """Download placeholder image from Lorem Picsum"""
    # Use Lorem Picsum for placeholder images
    # Size: 1200x630 (optimal for social sharing)
    url = f"https://picsum.photos/1200/630?random={post_id}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = f"/tmp/featured_{post_id}.jpg"
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print(f"Error: {e}")
    return None

def upload_to_wordpress(image_path, post_title):
    """Upload image to WordPress"""
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/media"
    
    try:
        with open(image_path, 'rb') as f:
            files = {
                'file': (f'featured-{os.path.basename(image_path)}', f, 'image/jpeg')
            }
            response = requests.post(
                url,
                files=files,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                headers={'Content-Disposition': f'attachment; filename="featured.jpg"'}
            )
            
            if response.status_code == 201:
                return response.json()['id']
    except Exception as e:
        print(f"Upload error: {e}")
    return None

def set_featured_image(post_id, media_id):
    """Set featured image for post"""
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}"
    
    response = requests.post(
        url,
        json={'featured_media': media_id},
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    
    return response.status_code == 200

def main():
    print("=" * 60)
    print("📸 Adding Placeholder Featured Images")
    print("=" * 60)
    
    # Get posts without featured images
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = [p for p in response.json() if p.get('featured_media', 0) == 0]
    
    print(f"\nProcessing {min(len(posts), 30)} posts...")
    print("=" * 60)
    
    success = 0
    
    for i, post in enumerate(posts[:30], 1):
        title = post['title']['rendered'][:40]
        print(f"\n[{i}/30] {title}...")
        
        # Download placeholder
        image_path = download_placeholder_image(post['id'])
        if not image_path:
            print("   ❌ Download failed")
            continue
        
        # Upload to WordPress
        media_id = upload_to_wordpress(image_path, title)
        if not media_id:
            print("   ❌ Upload failed")
            os.remove(image_path)
            continue
        
        # Set as featured image
        if set_featured_image(post['id'], media_id):
            print(f"   ✅ Featured image set (Media ID: {media_id})")
            success += 1
        else:
            print("   ❌ Failed to set featured image")
        
        # Cleanup
        try:
            os.remove(image_path)
        except:
            pass
        
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully added {success} featured images!")
    print("=" * 60)

if __name__ == "__main__":
    main()
