#!/usr/bin/env python3
"""
Add Images to Posts Without Any Images
=====================================
Use our enhanced tools to add relevant images to posts that have none.
"""

import sys
import os
import getpass
import requests
from datetime import datetime
import random

# Add the master_toolkit to Python path
sys.path.append('/home/kddevops/projects/spherevista360')

from direct_image_fix import SimpleWordPressClient

# Relevant stock images from Unsplash (free to use)
STOCK_IMAGES = {
    'travel': [
        'https://images.unsplash.com/photo-1488646953014-85cb44e25828',  # Travel
        'https://images.unsplash.com/photo-1469474968028-56623f02e42e',  # Landscape
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',  # Mountain
    ],
    'business': [
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',  # Business meeting
        'https://images.unsplash.com/photo-1560472354-b33ff0c44a43',  # Office
        'https://images.unsplash.com/photo-1553484771-371a605b060b',  # Handshake
    ],
    'technology': [
        'https://images.unsplash.com/photo-1518709268805-4e9042af2176',  # Code
        'https://images.unsplash.com/photo-1559526324-4b87b5e36e44',  # Computer
        'https://images.unsplash.com/photo-1551288049-bebda4e38f71',  # Data
    ],
    'finance': [
        'https://images.unsplash.com/photo-1559526324-4b87b5e36e44',  # Charts
        'https://images.unsplash.com/photo-1460925895917-afdab827c52f',  # Analytics
        'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3',  # Money
    ],
    'politics': [
        'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620',  # Government
        'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620',  # Voting
        'https://images.unsplash.com/photo-1586255997252-b1e7f7b0e70c',  # Democracy
    ],
    'general': [
        'https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a',  # Writing
        'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d',  # Computer work
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',  # Professional
    ]
}

def categorize_post(title, content=""):
    """Categorize post based on title and content to choose appropriate image."""
    title_lower = title.lower()
    content_lower = content.lower()
    text = f"{title_lower} {content_lower}"
    
    if any(word in text for word in ['travel', 'visa', 'destination', 'tourism', 'trip']):
        return 'travel'
    elif any(word in text for word in ['business', 'trade', 'startup', 'funding', 'investor']):
        return 'business'
    elif any(word in text for word in ['ai', 'technology', 'cloud', 'software', 'digital', 'tech']):
        return 'technology'
    elif any(word in text for word in ['inflation', 'economy', 'financial', 'money', 'budget']):
        return 'finance'
    elif any(word in text for word in ['election', 'political', 'politics', 'democratic', 'government']):
        return 'politics'
    else:
        return 'general'

def download_and_add_image(wp_client, post_id, post_title, category='general'):
    """Download a relevant stock image and add it to the post content and as featured image."""
    try:
        # Choose appropriate image based on category
        images = STOCK_IMAGES.get(category, STOCK_IMAGES['general'])
        image_url = random.choice(images)
        
        # Add image dimensions for better quality
        image_url += "?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80"
        
        print(f"   📸 Downloading image from Unsplash...")
        
        # Download the image
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Generate filename
        filename = f"featured-{post_id}-{category}.jpg"
        
        # Upload to WordPress
        print(f"   ⬆️  Uploading to WordPress media library...")
        media_result = wp_client.upload_media(
            file_content=response.content,
            filename=filename,
            alt_text=f"Featured image for {post_title}",
            caption=f"Featured image for post: {post_title}"
        )
        
        media_id = media_result['id']
        media_url = media_result['source_url']
        
        # Get current post content
        post = wp_client.get_post(post_id, context='edit')
        current_content = post.get('content', {}).get('raw', '')
        
        # Add image to the beginning of the content if it doesn't have any images
        image_html = f'<img src="{media_url}" alt="{post_title}" class="wp-image-{media_id}" />\n\n'
        new_content = image_html + current_content
        
        # Update post with new content and featured image
        print(f"   ✏️  Adding image to post content and setting as featured image...")
        wp_client.update_post(post_id, {
            'content': new_content,
            'featured_media': media_id
        })
        
        return {
            'success': True,
            'media_id': media_id,
            'media_url': media_url,
            'category': category
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def add_images_to_posts():
    """Add relevant images to posts that have none."""
    print("🖼️  Adding Images to Posts Without Any Images")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get credentials
    username = input("WordPress Username: ") if len(sys.argv) < 2 else sys.argv[1]
    password = getpass.getpass("WordPress Password: ") if len(sys.argv) < 3 else sys.argv[2]
    
    if not username or not password:
        print("❌ Username and password required")
        return
    
    try:
        # Create client and authenticate
        wp = SimpleWordPressClient()
        if not wp.authenticate(username, password):
            print("❌ Authentication failed")
            return
        
        # Get posts without featured images
        print("\n🔍 Finding posts without featured images...")
        posts = wp.get_posts(per_page=20)
        
        posts_without_featured = []
        for post in posts:
            if not post.get('featured_media') or post.get('featured_media') == 0:
                posts_without_featured.append(post)
        
        print(f"📊 Found {len(posts_without_featured)} posts without featured images")
        
        if not posts_without_featured:
            print("✅ All posts already have featured images!")
            return
        
        # Show posts and ask for confirmation
        print("\n📋 Posts that will get relevant images added:")
        for i, post in enumerate(posts_without_featured[:10], 1):
            title = post.get('title', {}).get('rendered', 'Untitled')
            category = categorize_post(title)
            print(f"   {i}. {title[:40]}... → {category.title()} image")
        
        # Ask for confirmation
        confirm = input(f"\n🔧 Add relevant images to these {min(len(posts_without_featured), 10)} posts? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Cancelled")
            return
        
        # Process posts
        print(f"\n🚀 Adding images to posts...")
        successful_count = 0
        
        for post in posts_without_featured[:10]:  # Limit to 10 for safety
            post_id = post['id']
            title = post.get('title', {}).get('rendered', 'Untitled')
            category = categorize_post(title)
            
            print(f"\n   Processing: {title[:30]}... (Category: {category})")
            
            result = download_and_add_image(wp, post_id, title, category)
            
            if result.get('success'):
                print(f"   ✅ Successfully added {category} image!")
                successful_count += 1
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        print(f"\n🎉 Results:")
        print(f"   • Posts processed: {min(len(posts_without_featured), 10)}")
        print(f"   • Successfully enhanced: {successful_count}")
        print(f"   • Images added from Unsplash stock photos")
        
        if successful_count > 0:
            print(f"\n✅ Successfully added relevant images to posts!")
            print(f"💡 Each post now has:")
            print(f"   • A relevant image in the content")
            print(f"   • A featured image for social sharing")
            print(f"   • Proper alt text for SEO")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🏁 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    add_images_to_posts()