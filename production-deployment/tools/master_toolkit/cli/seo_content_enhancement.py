#!/usr/bin/env python3
"""
SEO and Content Quality Enhancement Script
==========================================
Apply SEO improvements and content quality enhancements to all posts.
"""

import requests
import json
import re
from getpass import getpass
from datetime import datetime
from urllib.parse import quote

class SimpleWordPressClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://spherevista360.com"
        self.auth_token = None
        
    def authenticate(self):
        """Authenticate with WordPress"""
        auth_url = f"{self.base_url}/wp-json/jwt-auth/v1/token"
        
        try:
            response = requests.post(auth_url, json={
                'username': self.username,
                'password': self.password
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                return True
            else:
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def get_posts(self, per_page=100):
        """Get all posts"""
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        headers = {'Authorization': f'Bearer {self.auth_token}'} if self.auth_token else {}
        
        try:
            response = requests.get(url, headers=headers, params={'per_page': per_page}, timeout=30)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting posts: {e}")
            return []
    
    def update_post(self, post_id, data):
        """Update a post"""
        url = f"{self.base_url}/wp-json/wp/v2/posts/{post_id}"
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating post {post_id}: {e}")
            return False

class SEOEnhancer:
    def __init__(self, wordpress_client):
        self.wordpress = wordpress_client
        
    def analyze_seo_issues(self, posts):
        """Analyze SEO issues across all posts"""
        issues = {
            'missing_meta_descriptions': [],
            'short_titles': [],
            'long_titles': [],
            'missing_keywords': [],
            'poor_readability': []
        }
        
        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            content = post.get('content', {}).get('rendered', '')
            excerpt = post.get('excerpt', {}).get('rendered', '')
            
            # Check title length
            if len(title) < 30:
                issues['short_titles'].append(f"{title[:50]}... (ID: {post['id']})")
            elif len(title) > 60:
                issues['long_titles'].append(f"{title[:50]}... (ID: {post['id']})")
            
            # Check meta description (excerpt)
            if not excerpt or len(excerpt.strip()) < 120:
                issues['missing_meta_descriptions'].append(f"{title[:50]}... (ID: {post['id']})")
            
            # Check for keywords in content
            if content and len(content.strip()) < 300:
                issues['poor_readability'].append(f"{title[:50]}... (ID: {post['id']})")
        
        return issues
    
    def enhance_meta_descriptions(self, posts):
        """Generate and add meta descriptions"""
        enhanced_count = 0
        
        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            content = post.get('content', {}).get('rendered', '')
            excerpt = post.get('excerpt', {}).get('rendered', '')
            
            # Skip if already has good excerpt
            if excerpt and len(excerpt.strip()) >= 120:
                continue
            
            # Generate meta description from content
            clean_content = re.sub(r'<[^>]+>', '', content)
            sentences = clean_content.split('.')[:3]
            meta_description = '. '.join(sentences).strip()[:155] + '...'
            
            if len(meta_description) > 50:
                update_data = {'excerpt': meta_description}
                
                if self.wordpress.update_post(post['id'], update_data):
                    print(f"   ✅ Enhanced meta description for: {title[:50]}...")
                    enhanced_count += 1
                else:
                    print(f"   ❌ Failed to update: {title[:50]}...")
        
        return enhanced_count

class ContentQualityEnhancer:
    def __init__(self, wordpress_client):
        self.wordpress = wordpress_client
        
    def analyze_content_quality(self, posts):
        """Analyze content quality issues"""
        issues = {
            'short_content': [],
            'missing_headings': [],
            'no_internal_links': [],
            'poor_formatting': []
        }
        
        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            content = post.get('content', {}).get('rendered', '')
            
            # Check content length
            clean_content = re.sub(r'<[^>]+>', '', content)
            if len(clean_content.strip()) < 500:
                issues['short_content'].append(f"{title[:50]}... (ID: {post['id']})")
            
            # Check for headings
            if not re.search(r'<h[2-6]', content):
                issues['missing_headings'].append(f"{title[:50]}... (ID: {post['id']})")
            
            # Check for internal links
            if 'spherevista360.com' not in content:
                issues['no_internal_links'].append(f"{title[:50]}... (ID: {post['id']})")
        
        return issues
    
    def enhance_content_structure(self, posts):
        """Enhance content structure and formatting"""
        enhanced_count = 0
        
        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            content = post.get('content', {}).get('rendered', '')
            
            # Skip if content is already well structured
            if re.search(r'<h[2-6]', content):
                continue
            
            # Add basic structure to content
            paragraphs = content.split('</p>')
            if len(paragraphs) > 3:
                # Add a subheading after the first paragraph
                enhanced_content = paragraphs[0] + '</p>'
                enhanced_content += '<h2>Key Insights</h2>'
                enhanced_content += '</p>'.join(paragraphs[1:])
                
                update_data = {'content': enhanced_content}
                
                if self.wordpress.update_post(post['id'], update_data):
                    print(f"   ✅ Enhanced content structure for: {title[:50]}...")
                    enhanced_count += 1
                else:
                    print(f"   ❌ Failed to update: {title[:50]}...")
        
        return enhanced_count

def main():
    """Main execution function"""
    print("🚀 SEO and Content Quality Enhancement")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authenticate
    print("\n🔐 WordPress Authentication")
    username = input("WordPress Username: ")
    password = getpass("WordPress Password: ")
    
    wordpress = SimpleWordPressClient(username, password)
    
    if not wordpress.authenticate():
        print("❌ Authentication failed")
        return
    
    print(f"✅ Authenticated successfully as {username}")
    
    # Get posts
    print("\n📊 Fetching posts...")
    posts = wordpress.get_posts()
    print(f"Found {len(posts)} posts to analyze")
    
    # Initialize enhancers
    seo_enhancer = SEOEnhancer(wordpress)
    content_enhancer = ContentQualityEnhancer(wordpress)
    
    # Analyze SEO issues
    print("\n🔍 Analyzing SEO Issues...")
    seo_issues = seo_enhancer.analyze_seo_issues(posts)
    
    for category, issues in seo_issues.items():
        if issues:
            print(f"   {category.replace('_', ' ').title()}: {len(issues)} issues")
    
    # Analyze content quality
    print("\n🔍 Analyzing Content Quality...")
    content_issues = content_enhancer.analyze_content_quality(posts)
    
    for category, issues in content_issues.items():
        if issues:
            print(f"   {category.replace('_', ' ').title()}: {len(issues)} issues")
    
    # Apply enhancements
    apply_fixes = input("\n🔧 Apply enhancements? (yes/no): ").lower().strip()
    
    if apply_fixes == 'yes':
        print("\n🛠️  Applying SEO Enhancements...")
        meta_desc_count = seo_enhancer.enhance_meta_descriptions(posts)
        
        print(f"\n🛠️  Applying Content Quality Enhancements...")
        structure_count = content_enhancer.enhance_content_structure(posts)
        
        print(f"\n🎉 Enhancement Results:")
        print(f"   • Meta descriptions enhanced: {meta_desc_count}")
        print(f"   • Content structures improved: {structure_count}")
        print(f"   • Total posts enhanced: {meta_desc_count + structure_count}")
    
    print(f"\n🏁 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()