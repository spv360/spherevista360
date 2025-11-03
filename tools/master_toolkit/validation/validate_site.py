#!/usr/bin/env python3
"""
Comprehensive WordPress Site Validator
Validates all aspects of the SphereVista360 WordPress site
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from collections import defaultdict

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

class SiteValidator:
    def __init__(self):
        self.auth = HTTPBasicAuth(USERNAME, PASSWORD)
        self.results = {
            'posts': {},
            'pages': {},
            'categories': {},
            'menus': {},
            'images': {},
            'seo': {},
            'links': {},
            'errors': []
        }
    
    def validate_posts(self):
        """Validate all posts"""
        print("\n📰 Validating Posts...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            posts = response.json()
            self.results['posts']['total'] = len(posts)
            self.results['posts']['with_featured_image'] = sum(1 for p in posts if p.get('featured_media', 0) > 0)
            self.results['posts']['without_featured_image'] = len(posts) - self.results['posts']['with_featured_image']
            self.results['posts']['with_categories'] = sum(1 for p in posts if p.get('categories'))
            self.results['posts']['with_excerpt'] = sum(1 for p in posts if p.get('excerpt', {}).get('rendered'))
            
            print(f"   Total Posts: {self.results['posts']['total']}")
            print(f"   ✅ With Featured Images: {self.results['posts']['with_featured_image']}")
            print(f"   ⚠️  Without Featured Images: {self.results['posts']['without_featured_image']}")
            print(f"   ✅ With Categories: {self.results['posts']['with_categories']}")
            print(f"   ✅ With Excerpts: {self.results['posts']['with_excerpt']}")
            
            # Check for empty content
            empty_content = []
            for post in posts:
                content = post.get('content', {}).get('rendered', '')
                if len(content.strip()) < 100:
                    empty_content.append(post['title']['rendered'])
            
            if empty_content:
                self.results['posts']['empty_content'] = empty_content
                print(f"   ⚠️  Posts with short/empty content: {len(empty_content)}")
            
            return True
        else:
            error = f"Failed to fetch posts: {response.status_code}"
            self.results['errors'].append(error)
            print(f"   ❌ {error}")
            return False
    
    def validate_pages(self):
        """Validate all pages"""
        print("\n📄 Validating Pages...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            pages = response.json()
            self.results['pages']['total'] = len(pages)
            
            required_pages = ['Homepage', 'About', 'Services', 'Contact', 'Blog']
            found_pages = [p['title']['rendered'] for p in pages]
            
            self.results['pages']['found'] = []
            self.results['pages']['missing'] = []
            
            for page_name in required_pages:
                if any(page_name.lower() in p.lower() for p in found_pages):
                    self.results['pages']['found'].append(page_name)
                    print(f"   ✅ {page_name}: Found")
                else:
                    self.results['pages']['missing'].append(page_name)
                    print(f"   ❌ {page_name}: Missing")
            
            # Check page content
            for page in pages:
                content = page.get('content', {}).get('rendered', '')
                if len(content.strip()) < 50:
                    print(f"   ⚠️  '{page['title']['rendered']}' has minimal content")
            
            return True
        else:
            error = f"Failed to fetch pages: {response.status_code}"
            self.results['errors'].append(error)
            print(f"   ❌ {error}")
            return False
    
    def validate_categories(self):
        """Validate categories"""
        print("\n📂 Validating Categories...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            categories = response.json()
            self.results['categories']['total'] = len(categories)
            
            for cat in categories:
                print(f"   ✅ {cat['name']} ({cat['count']} posts)")
            
            return True
        else:
            error = f"Failed to fetch categories: {response.status_code}"
            self.results['errors'].append(error)
            print(f"   ❌ {error}")
            return False
    
    def validate_menus(self):
        """Validate menus"""
        print("\n🧭 Validating Menus...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/menus"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            menus = response.json()
            self.results['menus']['total'] = len(menus)
            
            for menu in menus:
                print(f"   ✅ Menu: {menu.get('name', 'Unknown')}")
            
            return True
        elif response.status_code == 404:
            print("   ℹ️  Menu endpoint not available (requires plugin)")
            return True
        else:
            print(f"   ⚠️  Could not verify menus: {response.status_code}")
            return True
    
    def validate_homepage_setting(self):
        """Validate homepage configuration"""
        print("\n🏠 Validating Homepage Settings...")
        print("-" * 60)
        
        # Try to get settings (may fail with 403 for non-admin)
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            settings = response.json()
            print(f"   Show on front: {settings.get('show_on_front', 'Unknown')}")
            print(f"   Front page ID: {settings.get('page_on_front', 'None')}")
            print(f"   Posts page ID: {settings.get('page_for_posts', 'None')}")
        else:
            print(f"   ℹ️  Settings check requires admin permissions")
        
        # Check actual homepage
        response = requests.get(WORDPRESS_URL)
        if response.status_code == 200:
            if '<title>Homepage' in response.text or 'SphereVista360' in response.text:
                print(f"   ✅ Homepage is accessible")
            else:
                print(f"   ⚠️  Homepage may not be configured correctly")
    
    def check_sitemap(self):
        """Check for sitemap"""
        print("\n🗺️  Validating Sitemap...")
        print("-" * 60)
        
        sitemap_urls = [
            f"{WORDPRESS_URL}/sitemap.xml",
            f"{WORDPRESS_URL}/wp-sitemap.xml",
            f"{WORDPRESS_URL}/sitemap_index.xml"
        ]
        
        for sitemap_url in sitemap_urls:
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                print(f"   ✅ Sitemap found: {sitemap_url}")
                self.results['seo']['sitemap'] = sitemap_url
                return True
        
        print(f"   ⚠️  No sitemap found")
        self.results['seo']['sitemap'] = None
        return False
    
    def check_robots_txt(self):
        """Check robots.txt"""
        print("\n🤖 Validating robots.txt...")
        print("-" * 60)
        
        response = requests.get(f"{WORDPRESS_URL}/robots.txt")
        if response.status_code == 200:
            print(f"   ✅ robots.txt exists")
            self.results['seo']['robots_txt'] = True
        else:
            print(f"   ⚠️  robots.txt not found")
            self.results['seo']['robots_txt'] = False
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE SITE VALIDATION REPORT")
        print("=" * 60)
        
        print(f"\n🌐 Site: {WORDPRESS_URL}")
        print(f"📅 Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "=" * 60)
        print("✅ CONTENT SUMMARY")
        print("=" * 60)
        print(f"📰 Posts: {self.results['posts'].get('total', 0)}")
        print(f"📄 Pages: {self.results['pages'].get('total', 0)}")
        print(f"📂 Categories: {self.results['categories'].get('total', 0)}")
        print(f"🧭 Menus: {self.results['menus'].get('total', 0)}")
        
        print("\n" + "=" * 60)
        print("⚠️  ISSUES TO FIX")
        print("=" * 60)
        
        issues = []
        
        if self.results['posts'].get('without_featured_image', 0) > 0:
            issues.append(f"❌ {self.results['posts']['without_featured_image']} posts need featured images")
        
        if self.results['pages'].get('missing'):
            issues.append(f"❌ Missing pages: {', '.join(self.results['pages']['missing'])}")
        
        if not self.results['seo'].get('sitemap'):
            issues.append("❌ Sitemap not found - install SEO plugin")
        
        if not self.results['seo'].get('robots_txt'):
            issues.append("❌ robots.txt not configured")
        
        if self.results['errors']:
            for error in self.results['errors']:
                issues.append(f"❌ {error}")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print("   ✅ No critical issues found!")
        
        print("\n" + "=" * 60)
        print("📋 NEXT STEPS")
        print("=" * 60)
        print("\n1. 🎨 Install Safe Theme:")
        print(f"   Download: https://spherevista360.com/wp-content/uploads/2025/10/spherevista360-safe.zip")
        print(f"   Or from: /home/kddevops/downloads/spherevista360-safe.zip")
        print(f"   Upload at: {WORDPRESS_URL}/wp-admin/themes.php")
        
        if self.results['posts'].get('without_featured_image', 0) > 0:
            print("\n2. 📸 Add Featured Images:")
            print("   Run script to add placeholder images to posts")
        
        if not self.results['seo'].get('sitemap'):
            print("\n3. 🗺️  Install SEO Plugin:")
            print("   Install Rank Math or Yoast SEO for sitemap generation")
        
        print("\n" + "=" * 60)
        
        return self.results

def main():
    print("=" * 60)
    print("🔍 WordPress Site Validator")
    print("=" * 60)
    
    validator = SiteValidator()
    
    validator.validate_posts()
    validator.validate_pages()
    validator.validate_categories()
    validator.validate_menus()
    validator.validate_homepage_setting()
    validator.check_sitemap()
    validator.check_robots_txt()
    
    results = validator.generate_report()
    
    # Save report
    import json
    with open('site_validation_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full report saved to: site_validation_report.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
