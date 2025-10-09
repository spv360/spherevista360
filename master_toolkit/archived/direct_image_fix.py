#!/usr/bin/env python3
"""
Direct Image Fix Using Enhanced Tools
====================================
Directly use our enhanced tools with simple authentication setup.
"""

import sys
import os
import getpass
import requests
from datetime import datetime

# Add the master_toolkit to Python path
sys.path.append('/home/kddevops/projects/spherevista360')

class SimpleWordPressClient:
    """Simple WordPress API client with direct authentication."""
    
    def __init__(self, base_url="https://spherevista360.com"):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/wp-json/wp/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SphereVista360-Enhanced-Tools/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.authenticated = False
        
    def authenticate(self, username, password):
        """Authenticate with WordPress using application passwords."""
        try:
            # Test authentication with a simple API call
            auth = (username, password)
            response = self.session.get(f"{self.api_base}/posts", auth=auth, params={'per_page': 1})
            
            if response.status_code == 200:
                self.session.auth = auth
                self.authenticated = True
                print(f"✅ Authenticated successfully as {username}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_posts(self, per_page=10, **kwargs):
        """Get posts from WordPress."""
        if not self.authenticated:
            raise Exception("Not authenticated")
        
        params = {'per_page': per_page}
        params.update(kwargs)
        
        response = self.session.get(f"{self.api_base}/posts", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_post(self, post_id, context='view'):
        """Get a single post."""
        if not self.authenticated:
            raise Exception("Not authenticated")
        
        params = {'context': context} if context else {}
        response = self.session.get(f"{self.api_base}/posts/{post_id}", params=params)
        response.raise_for_status()
        return response.json()
    
    def update_post(self, post_id, data):
        """Update a post."""
        if not self.authenticated:
            raise Exception("Not authenticated")
        
        response = self.session.post(f"{self.api_base}/posts/{post_id}", json=data)
        response.raise_for_status()
        return response.json()
    
    def upload_media(self, file_content, filename, alt_text="", caption=""):
        """Upload media to WordPress."""
        if not self.authenticated:
            raise Exception("Not authenticated")
        
        files = {
            'file': (filename, file_content, 'image/jpeg')
        }
        data = {
            'alt_text': alt_text,
            'caption': caption
        }
        
        response = self.session.post(f"{self.api_base}/media", files=files, data=data)
        response.raise_for_status()
        return response.json()
    
    def get_media(self, media_id):
        """Get media details."""
        if not self.authenticated:
            raise Exception("Not authenticated")
        
        response = self.session.get(f"{self.api_base}/media/{media_id}")
        response.raise_for_status()
        return response.json()


def fix_images_directly():
    """Fix images using our enhanced tools with direct authentication."""
    print("🖼️  Direct Image Fixing with Enhanced Tools")
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
        # Create simple client
        wp = SimpleWordPressClient()
        
        # Authenticate
        if not wp.authenticate(username, password):
            print("❌ Authentication failed")
            return
        
        # Test: get posts missing featured images
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
        
        # Show which posts need fixing
        print("\n📋 Posts that need featured images:")
        for i, post in enumerate(posts_without_featured[:10], 1):
            title = post.get('title', {}).get('rendered', 'Untitled')
            print(f"   {i}. {title[:50]}... (ID: {post['id']})")
        
        # Ask for confirmation
        confirm = input(f"\n🔧 Fix featured images for these {len(posts_without_featured)} posts? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Cancelled")
            return
        
        # Use our enhanced ImageValidator
        print("\n🚀 Using Enhanced ImageValidator...")
        from master_toolkit.validation.images import ImageValidator
        
        # Create ImageValidator with our simple client
        image_validator = ImageValidator(wp)
        
        # Fix each post
        fixed_count = 0
        for post in posts_without_featured[:10]:  # Limit to 10 for safety
            post_id = post['id']
            title = post.get('title', {}).get('rendered', 'Untitled')
            
            print(f"\n   Processing: {title[:30]}... (ID: {post_id})")
            
            try:
                # Use our enhanced method to set featured image from content
                result = image_validator.set_featured_image_from_content(post_id, dry_run=False)
                
                if result.get('success'):
                    print(f"   ✅ {result.get('message', 'Success')}")
                    fixed_count += 1
                elif 'No images found' in result.get('message', ''):
                    print(f"   ⚠️  No images in content to use as featured image")
                else:
                    print(f"   ❌ {result.get('message', 'Failed')}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n🎉 Results:")
        print(f"   • Posts processed: {min(len(posts_without_featured), 10)}")
        print(f"   • Successfully fixed: {fixed_count}")
        print(f"   • Remaining posts without featured images: {len(posts_without_featured) - fixed_count}")
        
        if fixed_count > 0:
            print(f"\n✅ Successfully fixed featured images using enhanced tools!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🏁 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    fix_images_directly()