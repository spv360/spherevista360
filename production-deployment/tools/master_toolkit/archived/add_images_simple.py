#!/usr/bin/env python3
"""
Add Featured Images by URL
==========================
Add featured images to posts using direct image URLs (WordPress supports this).
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

# High-quality stock images from reliable sources
STOCK_IMAGES = {
    'travel': [
        'https://images.pexels.com/photos/346885/pexels-photo-346885.jpeg',  # Travel
        'https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg',  # World map
        'https://images.pexels.com/photos/2467287/pexels-photo-2467287.jpeg',  # Passport
    ],
    'business': [
        'https://images.pexels.com/photos/3184360/pexels-photo-3184360.jpeg',  # Business meeting
        'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg',  # Office work
        'https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg',  # Handshake
    ],
    'technology': [
        'https://images.pexels.com/photos/2004161/pexels-photo-2004161.jpeg',  # Code
        'https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg',  # Computer
        'https://images.pexels.com/photos/325229/pexels-photo-325229.jpeg',  # Cloud
    ],
    'finance': [
        'https://images.pexels.com/photos/590022/pexels-photo-590022.jpeg',  # Charts
        'https://images.pexels.com/photos/159888/pexels-photo-159888.jpeg',  # Money
        'https://images.pexels.com/photos/3760067/pexels-photo-3760067.jpeg',  # Financial graph
    ],
    'politics': [
        'https://images.pexels.com/photos/1550337/pexels-photo-1550337.jpeg',  # Government building
        'https://images.pexels.com/photos/6896086/pexels-photo-6896086.jpeg',  # Voting
        'https://images.pexels.com/photos/8837687/pexels-photo-8837687.jpeg',  # Democracy
    ],
    'general': [
        'https://images.pexels.com/photos/261949/pexels-photo-261949.jpeg',  # Writing
        'https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg',  # Laptop
        'https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg',  # Professional
    ]
}

def categorize_post(title, content=""):
    """Categorize post based on title and content to choose appropriate image."""
    title_lower = title.lower()
    content_lower = content.lower()
    text = f"{title_lower} {content_lower}"
    
    if any(word in text for word in ['travel', 'visa', 'destination', 'tourism', 'trip', 'nomad']):
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

def add_image_to_post_content(wp_client, post_id, post_title, category='general'):
    """Add an image to post content by embedding the URL directly."""
    try:
        # Choose appropriate image based on category
        images = STOCK_IMAGES.get(category, STOCK_IMAGES['general'])
        image_url = random.choice(images)
        
        print(f"   🖼️  Selected {category} image: {image_url}")
        
        # Get current post content
        post = wp_client.get_post(post_id, context='edit')
        current_content = post.get('content', {}).get('raw', '')
        
        # Create image HTML with proper attributes
        image_html = f'''<div class="wp-block-image">
<figure class="aligncenter size-large">
<img src="{image_url}" alt="{post_title}" />
<figcaption>{post_title}</figcaption>
</figure>
</div>

'''
        
        # Add image to the beginning of the content
        new_content = image_html + current_content
        
        # Update post with new content
        print(f"   ✏️  Adding image to post content...")
        wp_client.update_post(post_id, {
            'content': new_content
        })
        
        return {
            'success': True,
            'image_url': image_url,
            'category': category
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def add_images_simple():
    """Add images to posts using simple URL embedding."""
    print("🖼️  Adding Images to Posts (Simple Method)")
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
        print("\n🔍 Finding posts without images...")
        posts = wp.get_posts(per_page=20)
        
        # Check which posts actually have no images in content
        posts_needing_images = []
        for post in posts:
            # Get full post content to check for images
            full_post = wp.get_post(post['id'], context='edit')
            content = full_post.get('content', {}).get('raw', '')
            
            # Check if post has any images
            if '<img' not in content and not post.get('featured_media'):
                posts_needing_images.append(post)
        
        print(f"📊 Found {len(posts_needing_images)} posts without any images")
        
        if not posts_needing_images:
            print("✅ All posts already have images!")
            return
        
        # Show posts and ask for confirmation
        print("\n📋 Posts that will get images added:")
        for i, post in enumerate(posts_needing_images[:5], 1):  # Show 5 for confirmation
            title = post.get('title', {}).get('rendered', 'Untitled')
            category = categorize_post(title)
            print(f"   {i}. {title[:40]}... → {category.title()} image")
        
        # Ask for confirmation
        confirm = input(f"\n🔧 Add images to these {min(len(posts_needing_images), 5)} posts? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Cancelled")
            return
        
        # Process posts
        print(f"\n🚀 Adding images to posts...")
        successful_count = 0
        
        for post in posts_needing_images[:5]:  # Limit to 5 for safety
            post_id = post['id']
            title = post.get('title', {}).get('rendered', 'Untitled')
            category = categorize_post(title)
            
            print(f"\n   Processing: {title[:30]}... (Category: {category})")
            
            result = add_image_to_post_content(wp, post_id, title, category)
            
            if result.get('success'):
                print(f"   ✅ Successfully added {category} image!")
                successful_count += 1
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        print(f"\n🎉 Results:")
        print(f"   • Posts processed: {min(len(posts_needing_images), 5)}")
        print(f"   • Successfully enhanced: {successful_count}")
        print(f"   • Images added from Pexels stock photos")
        
        if successful_count > 0:
            print(f"\n✅ Successfully added relevant images to posts!")
            print(f"💡 Each post now has:")
            print(f"   • A relevant image in the content")
            print(f"   • Proper alt text for SEO")
            print(f"   • Professional appearance")
            
            print(f"\n🔄 Next steps:")
            print(f"   • Run our enhanced ImageValidator to set featured images")
            print(f"   • Continue with remaining posts if needed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🏁 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    add_images_simple()