#!/usr/bin/env python3
"""
Final WordPress Internal Link Fix
Uses exact URL mappings to fix all broken internal links
"""

import os
import requests
import base64
import re

class FinalLinkFixer:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
        
        # Exact URL mappings based on current posts
        self.url_fixes = {
            'digital-banking-revolution-future-fintech': 'digital-banking-revolution-the-future-of-fintech',
            'cloud-wars-2025-aws-vs-azure-vs-google-cloud': 'the-cloud-wars-of-2025-aws-vs-azure-vs-google-cloud',
            'top-visa-free-destinations-2025-travelers': 'top-visa-free-destinations-for-2025-travelers',
            'digital-nomad-visas-2025-work-anywhere': 'digital-nomad-visas-2025-work-from-anywhere',
            'generative-ai-tools-shaping-tech-2025': 'generative-ai-tools-shaping-tech-in-2025',
            'ai-transforming-global-investing-2025': 'how-ai-is-transforming-global-investing-in-2025',
            'cybersecurity-age-ai-automation': 'cybersecurity-in-the-age-of-ai-automation',
            'us-india-trade-relations-new-era-cooperation': 'us-india-trade-relations-a-new-era-of-cooperation',
            'ai-influencing-politics': 'how-ai-is-influencing-modern-politics',
            'rising-inflation-impact-emerging-markets': 'rising-inflation-and-its-impact-on-emerging-markets',
            'startup-funding-trends-investor-sentiment-2025': 'startup-funding-trends-and-investor-sentiment-in-2025'
        }
        
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def fix_post_links(self, post_id):
        """Fix internal links in a specific post"""
        post_response = requests.get(f"{self.api}/posts/{post_id}", headers=self.headers)
        if post_response.status_code != 200:
            return False
            
        post = post_response.json()
        content = post['content']['rendered']
        original_content = content
        fixed_count = 0
        
        # Fix each broken URL pattern
        for broken_slug, correct_slug in self.url_fixes.items():
            broken_url = f"{self.site}/{broken_slug}/"
            correct_url = f"{self.site}/{correct_slug}/"
            
            if broken_url in content:
                content = content.replace(broken_url, correct_url)
                fixed_count += 1
                print(f"    Fixed: {broken_slug} → {correct_slug}")
        
        # Update post if content changed
        if content != original_content:
            update_data = {'content': content}
            update_response = requests.post(f"{self.api}/posts/{post_id}", headers=self.headers, json=update_data)
            if update_response.status_code == 200:
                print(f"    ✅ Updated post with {fixed_count} link fixes")
                return True
            else:
                print(f"    ❌ Failed to update post")
                return False
        else:
            print(f"    ℹ️  No broken links found")
            return True
    
    def fix_all_links(self):
        """Fix all internal links across all posts"""
        print("🔧 Final Internal Link Fix")
        print("=" * 50)
        
        # Get all posts
        posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
        posts = posts_response.json()
        
        print(f"Found {len(posts)} posts to check")
        
        total_fixed = 0
        for post in posts:
            post_id = post['id']
            title = post['title']['rendered']
            print(f"\n🔍 Checking: {title} (ID: {post_id})")
            
            if self.fix_post_links(post_id):
                total_fixed += 1
        
        print(f"\n🎉 Link fixing completed!")
        print(f"📊 Processed {len(posts)} posts successfully")
        
        return total_fixed

if __name__ == "__main__":
    fixer = FinalLinkFixer()
    fixer.fix_all_links()