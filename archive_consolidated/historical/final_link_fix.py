#!/usr/bin/env python3
"""
WordPress Link Fixer - Final Version
Uses actual post URLs from WordPress to fix internal links
"""

import os
import requests
import base64
import re

class WordPressLinkFixer:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
        self.post_url_map = self.build_post_url_map()
        
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def build_post_url_map(self):
        """Build a mapping of post titles/keywords to actual URLs"""
        posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
        posts = posts_response.json()
        
        url_map = {}
        keyword_map = {
            'ai-in-politics': 'how-ai-is-influencing-modern-politics',
            'us-india-trade-2025': 'us-india-trade-relations-a-new-era-of-cooperation',
            'global-inflation-2025': 'rising-inflation-and-its-impact-on-emerging-markets',
            'digital-banking-2025': 'digital-banking-revolution-the-future-of-fintech',
            'visa-free-destinations-2025': 'top-visa-free-destinations-for-2025-travelers',
            'budget-travel-tips-2025': 'digital-nomad-visas-2025-work-from-anywhere',
            'ai-cybersecurity-automation': 'cybersecurity-in-the-age-of-ai-automation',
            'cloud-wars-2025': 'the-cloud-wars-of-2025-aws-vs-azure-vs-google-cloud',
            'startup-funding-2025': 'startup-funding-trends-and-investor-sentiment-in-2025',
            'ai-investing-2025': 'how-ai-is-transforming-global-investing-in-2025',
            'generative-ai-tools-2025': 'generative-ai-tools-shaping-tech-in-2025'
        }
        
        # Map keywords to actual URLs
        for post in posts:
            slug = post['slug']
            actual_url = post['link']
            
            # Map direct slugs
            url_map[slug] = actual_url
            
            # Map keyword variants
            for keyword, target_slug in keyword_map.items():
                if target_slug in slug:
                    url_map[keyword] = actual_url
        
        return url_map
    
    def fix_links_in_post(self, post_id):
        """Fix internal links in a specific post"""
        post_response = requests.get(f"{self.api}/posts/{post_id}", headers=self.headers)
        if post_response.status_code != 200:
            return False
            
        post = post_response.json()
        content = post['content']['rendered']
        original_content = content
        
        # Find all internal links that are broken
        broken_patterns = [
            r'https://spherevista360\.com/([^/]+)/',
        ]
        
        for pattern in broken_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                full_url = match.group(0)
                slug = match.group(1)
                
                # Check if we have a mapping for this slug
                if slug in self.post_url_map:
                    new_url = self.post_url_map[slug]
                    content = content.replace(full_url, new_url)
                    print(f"  Replaced: {full_url} → {new_url}")
        
        # Update post if content changed
        if content != original_content:
            update_data = {'content': content}
            update_response = requests.post(f"{self.api}/posts/{post_id}", headers=self.headers, json=update_data)
            return update_response.status_code == 200
        
        return True
    
    def remove_duplicate_posts(self):
        """Remove duplicate posts (those with -2 suffix)"""
        posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
        posts = posts_response.json()
        
        duplicate_posts = [post for post in posts if post['slug'].endswith('-2')]
        
        print(f"Found {len(duplicate_posts)} duplicate posts to remove:")
        for post in duplicate_posts:
            print(f"  - {post['title']['rendered']} (ID: {post['id']})")
        
        print(f"\nRemoving duplicates...")
        for post in duplicate_posts:
            delete_response = requests.delete(f"{self.api}/posts/{post['id']}", headers=self.headers, params={'force': True})
            if delete_response.status_code == 200:
                print(f"  ✅ Deleted: {post['title']['rendered']}")
            else:
                print(f"  ❌ Failed to delete: {post['title']['rendered']}")
    
    def fix_all_links(self):
        """Fix all internal links across all posts"""
        print("🔧 Starting Final Link Fix Process")
        
        # First, remove duplicate posts
        print("\n1. Removing duplicate posts...")
        self.remove_duplicate_posts()
        
        # Rebuild URL map after removing duplicates
        print("\n2. Rebuilding URL map...")
        self.post_url_map = self.build_post_url_map()
        
        # Fix links in all remaining posts
        print("\n3. Fixing internal links...")
        posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
        posts = posts_response.json()
        
        for post in posts:
            post_id = post['id']
            title = post['title']['rendered']
            print(f"Fixing links in: {title}")
            
            if self.fix_links_in_post(post_id):
                print(f"  ✅ Fixed")
            else:
                print(f"  ❌ Failed")
        
        print("\n🎉 Link fixing completed!")

if __name__ == "__main__":
    fixer = WordPressLinkFixer()
    fixer.fix_all_links()