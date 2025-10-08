#!/usr/bin/env python3
"""
WordPress Link and Image Fixer
Fixes broken internal links and images identified by verification
"""

import os
import requests
import base64
import json
import re
from urllib.parse import urlparse

class WordPressFixer:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
        
        # URL mapping for broken internal links
        self.url_mappings = {
            'ai-in-politics': 'ai-influencing-politics',
            'us-india-trade-2025': 'us-india-trade-relations-new-era-cooperation',
            'global-inflation-2025': 'rising-inflation-impact-emerging-markets',
            'digital-banking-2025': 'digital-banking-revolution-future-fintech',
            'visa-free-destinations-2025': 'top-visa-free-destinations-2025-travelers',
            'budget-travel-tips-2025': 'digital-nomad-visas-2025-work-anywhere',  # Alternative link
            'ai-cybersecurity-automation': 'cybersecurity-age-ai-automation',
            'cloud-wars-2025': 'cloud-wars-2025-aws-vs-azure-vs-google-cloud',
            'startup-funding-2025': 'startup-funding-trends-investor-sentiment-2025',
            'ai-investing-2025': 'ai-transforming-global-investing-2025',
            'generative-ai-tools-2025': 'generative-ai-tools-shaping-tech-2025'
        }
        
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def get_post(self, post_id):
        """Get a specific post"""
        response = requests.get(f"{self.api}/posts/{post_id}", headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def update_post(self, post_id, content):
        """Update post content"""
        data = {'content': content}
        response = requests.post(f"{self.api}/posts/{post_id}", headers=self.headers, json=data)
        return response.status_code == 200
    
    def fix_broken_image(self, post_id, old_url, new_url):
        """Fix a broken image in a post"""
        post = self.get_post(post_id)
        if not post:
            return False
            
        content = post['content']['rendered']
        
        # Replace the broken image URL
        content = content.replace(old_url, new_url)
        
        return self.update_post(post_id, content)
    
    def fix_internal_links(self, post_id):
        """Fix broken internal links in a post"""
        post = self.get_post(post_id)
        if not post:
            return False
            
        content = post['content']['rendered']
        original_content = content
        
        # Fix internal links using URL mappings
        for old_slug, new_slug in self.url_mappings.items():
            old_url = f"{self.site}/{old_slug}/"
            new_url = f"{self.site}/{new_slug}/"
            content = content.replace(old_url, new_url)
        
        # Update if content changed
        if content != original_content:
            return self.update_post(post_id, content)
        
        return True
    
    def fix_politics_image(self):
        """Fix the broken politics image with a working alternative"""
        # Working alternative image for politics/AI theme
        new_image_url = "https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80"
        
        # Posts with broken politics images
        posts_with_broken_image = [1700, 1649]  # Both "How AI Is Influencing Modern Politics" posts
        
        for post_id in posts_with_broken_image:
            post = self.get_post(post_id)
            if post:
                content = post['content']['rendered']
                
                # Replace broken image URL
                broken_url = "https://images.unsplash.com/photo-1528747045269-390fe33c19d4?auto=format&#038;fit=crop&#038;w=800&#038;h=500&#038;q=80"
                content = content.replace(broken_url, new_image_url)
                
                if self.update_post(post_id, content):
                    print(f"✅ Fixed image in post {post_id}")
                else:
                    print(f"❌ Failed to fix image in post {post_id}")
    
    def add_missing_images_to_entertainment(self):
        """Add images to Entertainment posts that are missing them"""
        entertainment_images = {
            1689: "https://images.unsplash.com/photo-1517180102446-f3ece451e9d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80",  # AI Hollywood VFX
            1691: "https://images.unsplash.com/photo-1560472355-536de3962603?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80",  # Cloud Gaming
            1693: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80",  # Spotify AI DJ
            1694: "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80",  # Streaming Wars
            1695: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80"   # YouTube Automation
        }
        
        for post_id, image_url in entertainment_images.items():
            post = self.get_post(post_id)
            if post:
                content = post['content']['rendered']
                title = post['title']['rendered']
                
                # Add image after the first H1 if no images exist
                if '<img' not in content and '![' not in content:
                    # Find first H2 or add after title
                    h2_match = re.search(r'<h2[^>]*>', content)
                    if h2_match:
                        # Insert image before first H2
                        insert_pos = h2_match.start()
                        image_html = f'\n\n<img src="{image_url}" alt="{title}" style="width: 100%; height: auto; margin: 20px 0;">\n\n'
                        content = content[:insert_pos] + image_html + content[insert_pos:]
                    else:
                        # Add image at the beginning
                        image_html = f'<img src="{image_url}" alt="{title}" style="width: 100%; height: auto; margin: 20px 0;">\n\n'
                        content = image_html + content
                    
                    if self.update_post(post_id, content):
                        print(f"✅ Added image to post {post_id}: {title}")
                    else:
                        print(f"❌ Failed to add image to post {post_id}: {title}")
    
    def fix_all_issues(self):
        """Fix all identified issues"""
        print("🔧 Starting WordPress Fixes")
        
        # Fix broken politics images
        print("\n1. Fixing broken politics images...")
        self.fix_politics_image()
        
        # Add missing images to Entertainment posts
        print("\n2. Adding missing images to Entertainment posts...")
        self.add_missing_images_to_entertainment()
        
        # Fix internal links in all posts with issues
        print("\n3. Fixing broken internal links...")
        posts_with_link_issues = [
            1707, 1706, 1705, 1704, 1700, 1699, 1698, 1697, 1696,
            1657, 1656, 1655, 1654, 1653, 1652, 1651, 1650, 1649, 1648, 1647, 1646
        ]
        
        for post_id in posts_with_link_issues:
            post = self.get_post(post_id)
            if post:
                title = post['title']['rendered']
                if self.fix_internal_links(post_id):
                    print(f"✅ Fixed links in post {post_id}: {title}")
                else:
                    print(f"❌ Failed to fix links in post {post_id}: {title}")
        
        print("\n🎉 Fix process completed!")
        print("Run verification script again to check if issues are resolved.")

if __name__ == "__main__":
    fixer = WordPressFixer()
    fixer.fix_all_issues()