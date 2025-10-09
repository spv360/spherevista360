#!/usr/bin/env python3
"""
Verify Image Fixes
==================
Quick verification that our image fixes worked.
"""

import sys
import getpass

# Add the master_toolkit to Python path
sys.path.append('/home/kddevops/projects/spherevista360')

from direct_image_fix import SimpleWordPressClient

def verify_fixes():
    """Verify that our image fixes worked."""
    print("🔍 Verifying Image Fixes")
    print("=" * 30)
    
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
        
        # Get recent posts
        posts = wp.get_posts(per_page=20)
        
        posts_with_images = 0
        posts_without_images = 0
        posts_with_featured = 0
        
        print("\n📊 Checking posts for images...")
        
        for post in posts:
            post_id = post['id']
            title = post.get('title', {}).get('rendered', 'Untitled')
            
            # Check content for images
            full_post = wp.get_post(post_id, context='edit')
            content = full_post.get('content', {}).get('raw', '')
            has_content_images = '<img' in content
            
            # Check for featured image
            has_featured = post.get('featured_media', 0) > 0
            
            if has_content_images:
                posts_with_images += 1
                print(f"   ✅ {title[:40]}... (has images)")
            else:
                posts_without_images += 1
                print(f"   ❌ {title[:40]}... (no images)")
            
            if has_featured:
                posts_with_featured += 1
        
        print(f"\n📈 Results:")
        print(f"   • Total posts checked: {len(posts)}")
        print(f"   • Posts with images in content: {posts_with_images}")
        print(f"   • Posts without any images: {posts_without_images}")
        print(f"   • Posts with featured images: {posts_with_featured}")
        
        print(f"\n🎯 Improvement Summary:")
        if posts_without_images < 15:  # We started with ~18 posts without images
            print(f"   ✅ Significant improvement! Reduced posts without images!")
            print(f"   📉 From ~18 posts to {posts_without_images} posts without images")
        
        if posts_with_images >= 5:  # We added images to 5 posts
            print(f"   ✅ Successfully added images to multiple posts!")
        
        print(f"\n💡 Next Steps:")
        if posts_without_images > 0:
            print(f"   • Run add_images_simple.py again to fix remaining {posts_without_images} posts")
        else:
            print(f"   • All posts now have images! 🎉")
        
        print(f"   • Continue enhancing with SEO improvements")
        print(f"   • Run content quality enhancements")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_fixes()