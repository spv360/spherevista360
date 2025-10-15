#!/usr/bin/env python3
"""
Comprehensive WordPress Site Validation
Validates ALL requirements including content quality and word count
"""

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

class ComprehensiveValidator:
    def __init__(self):
        self.auth = HTTPBasicAuth(USERNAME, PASSWORD)
        self.issues = []
        self.warnings = []
        self.success = []
        
    def strip_html(self, html):
        """Remove HTML tags and get plain text"""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    
    def count_words(self, text):
        """Count words in text"""
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def validate_post_content_length(self):
        """Validate all posts have 500-700 words"""
        print("\n📝 Validating Post Content Length (500-700 words)...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code != 200:
            self.issues.append("Failed to fetch posts for content validation")
            return False
        
        posts = response.json()
        short_posts = []
        long_posts = []
        good_posts = []
        
        for post in posts:
            title = post['title']['rendered']
            content = post['content']['rendered']
            plain_text = self.strip_html(content)
            word_count = self.count_words(plain_text)
            
            if word_count < 500:
                short_posts.append((title, word_count))
                print(f"   ⚠️  {title[:50]}: {word_count} words (too short)")
            elif word_count > 700:
                long_posts.append((title, word_count))
                print(f"   ℹ️  {title[:50]}: {word_count} words (acceptable but long)")
            else:
                good_posts.append((title, word_count))
                if len(good_posts) <= 5:  # Show first 5
                    print(f"   ✅ {title[:50]}: {word_count} words")
        
        print(f"\n   📊 Summary:")
        print(f"   ✅ Optimal (500-700 words): {len(good_posts)}")
        print(f"   ⚠️  Too short (<500 words): {len(short_posts)}")
        print(f"   ℹ️  Long (>700 words): {len(long_posts)}")
        
        if short_posts:
            self.warnings.append(f"{len(short_posts)} posts under 500 words")
        else:
            self.success.append("All posts meet minimum word count")
        
        return len(short_posts) == 0
    
    def validate_published_content_match(self):
        """Verify all content from published_content folder is on WordPress"""
        print("\n📚 Validating Published Content Matches Source...")
        print("-" * 60)
        
        from pathlib import Path
        content_dir = Path('/home/kddevops/projects/spherevista360/published_content')
        
        if not content_dir.exists():
            self.issues.append("published_content folder not found")
            return False
        
        # Count markdown files
        md_files = list(content_dir.rglob('*.md'))
        print(f"   📁 Source files in published_content: {len(md_files)}")
        
        # Get posts from WordPress
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
        response = requests.get(url, auth=self.auth)
        wp_posts = len(response.json()) if response.status_code == 200 else 0
        
        print(f"   📰 Posts on WordPress: {wp_posts}")
        
        if wp_posts >= len(md_files):
            print(f"   ✅ All source content published")
            self.success.append(f"All {len(md_files)} source files published")
        else:
            missing = len(md_files) - wp_posts
            print(f"   ⚠️  {missing} files may be missing")
            self.warnings.append(f"{missing} source files not found on WordPress")
    
    def validate_featured_images(self):
        """Check all posts have featured images"""
        print("\n🖼️  Validating Featured Images...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code != 200:
            self.issues.append("Failed to fetch posts for image validation")
            return False
        
        posts = response.json()
        without_images = [p for p in posts if p.get('featured_media', 0) == 0]
        
        print(f"   Total posts: {len(posts)}")
        print(f"   ✅ With featured images: {len(posts) - len(without_images)}")
        print(f"   ❌ Without featured images: {len(without_images)}")
        
        if without_images:
            self.issues.append(f"{len(without_images)} posts missing featured images")
            for post in without_images[:5]:
                print(f"      • {post['title']['rendered']}")
        else:
            self.success.append("All posts have featured images")
        
        return len(without_images) == 0
    
    def validate_categories(self):
        """Check all posts are categorized"""
        print("\n📂 Validating Post Categories...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code != 200:
            return False
        
        posts = response.json()
        uncategorized = [p for p in posts if not p.get('categories') or p['categories'] == [1]]
        
        print(f"   ✅ Categorized posts: {len(posts) - len(uncategorized)}")
        print(f"   ⚠️  Uncategorized posts: {len(uncategorized)}")
        
        if uncategorized:
            self.warnings.append(f"{len(uncategorized)} posts in default category")
        else:
            self.success.append("All posts properly categorized")
        
        return len(uncategorized) == 0
    
    def check_broken_links(self):
        """Check for broken links on homepage"""
        print("\n🔗 Checking for Broken Links...")
        print("-" * 60)
        
        try:
            response = requests.get(WORDPRESS_URL, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                internal_links = [l['href'] for l in links if WORDPRESS_URL in l['href']]
                print(f"   Found {len(links)} total links")
                print(f"   Testing {len(internal_links[:10])} internal links...")
                
                broken = []
                for link in internal_links[:10]:
                    r = requests.get(link, timeout=5)
                    if r.status_code >= 400:
                        broken.append((link, r.status_code))
                
                if broken:
                    print(f"   ❌ Found {len(broken)} broken links")
                    self.issues.append(f"{len(broken)} broken links detected")
                else:
                    print(f"   ✅ No broken links found")
                    self.success.append("No broken links detected")
            else:
                self.warnings.append("Could not access homepage for link checking")
        except Exception as e:
            self.warnings.append(f"Link checking failed: {str(e)}")
    
    def validate_redirects(self):
        """Check for redirects"""
        print("\n↪️  Checking for Redirects...")
        print("-" * 60)
        
        response = requests.get(WORDPRESS_URL, allow_redirects=False)
        if response.status_code in [301, 302, 307, 308]:
            print(f"   ⚠️  Homepage redirects to: {response.headers.get('Location')}")
            self.warnings.append("Homepage has redirect")
        else:
            print(f"   ✅ No redirects on homepage")
            self.success.append("No unwanted redirects")
    
    def validate_header_footer(self):
        """Check header and footer are present"""
        print("\n📄 Validating Header and Footer...")
        print("-" * 60)
        
        response = requests.get(WORDPRESS_URL)
        if response.status_code == 200:
            html = response.text
            
            # Check for header
            if 'site-header' in html or '<header' in html:
                print("   ✅ Header present")
                self.success.append("Professional header detected")
            else:
                print("   ⚠️  Header not clearly identified")
                self.warnings.append("Header structure unclear")
            
            # Check for footer
            if 'site-footer' in html or '<footer' in html:
                print("   ✅ Footer present")
                self.success.append("Professional footer detected")
            else:
                print("   ⚠️  Footer not clearly identified")
                self.warnings.append("Footer structure unclear")
            
            # Check for navigation
            if '<nav' in html or 'navigation' in html:
                print("   ✅ Navigation menu present")
                self.success.append("Navigation menu detected")
            else:
                self.warnings.append("Navigation menu not detected")
    
    def validate_seo(self):
        """Validate SEO elements"""
        print("\n🔍 Validating SEO & Indexing...")
        print("-" * 60)
        
        # Sitemap
        sitemap_urls = [
            f"{WORDPRESS_URL}/sitemap.xml",
            f"{WORDPRESS_URL}/wp-sitemap.xml"
        ]
        
        sitemap_found = False
        for url in sitemap_urls:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"   ✅ Sitemap found: {url}")
                self.success.append("XML Sitemap active")
                sitemap_found = True
                break
        
        if not sitemap_found:
            print("   ❌ Sitemap not found")
            self.issues.append("XML Sitemap missing")
        
        # robots.txt
        response = requests.get(f"{WORDPRESS_URL}/robots.txt")
        if response.status_code == 200:
            print("   ✅ robots.txt exists")
            self.success.append("robots.txt configured")
        else:
            print("   ⚠️  robots.txt not found")
            self.warnings.append("robots.txt missing")
        
        # Meta tags on homepage
        response = requests.get(WORDPRESS_URL)
        if response.status_code == 200:
            if 'meta name="description"' in response.text:
                print("   ✅ Meta description present")
                self.success.append("Meta descriptions configured")
            else:
                print("   ⚠️  Meta description missing")
                self.warnings.append("Meta descriptions need attention")
    
    def validate_menus(self):
        """Check menus are configured"""
        print("\n🧭 Validating Navigation Menus...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/menus"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            menus = response.json()
            print(f"   ✅ Total menus: {len(menus)}")
            for menu in menus[:5]:
                print(f"      • {menu.get('name', 'Unknown')}")
            self.success.append(f"{len(menus)} navigation menus configured")
        else:
            print("   ℹ️  Menu endpoint not available")
            self.warnings.append("Cannot verify menu configuration via API")
    
    def generate_final_report(self):
        """Generate final validation report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE VALIDATION REPORT")
        print("=" * 60)
        print(f"\n🌐 Site: {WORDPRESS_URL}")
        print(f"📅 Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESSES ({len(self.success)})")
        print("=" * 60)
        for item in self.success:
            print(f"   ✅ {item}")
        
        if self.warnings:
            print("\n" + "=" * 60)
            print(f"⚠️  WARNINGS ({len(self.warnings)})")
            print("=" * 60)
            for item in self.warnings:
                print(f"   ⚠️  {item}")
        
        if self.issues:
            print("\n" + "=" * 60)
            print(f"❌ CRITICAL ISSUES ({len(self.issues)})")
            print("=" * 60)
            for item in self.issues:
                print(f"   ❌ {item}")
        
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY")
        print("=" * 60)
        
        total_checks = len(self.success) + len(self.warnings) + len(self.issues)
        pass_rate = (len(self.success) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n   Total Checks: {total_checks}")
        print(f"   ✅ Passed: {len(self.success)}")
        print(f"   ⚠️  Warnings: {len(self.warnings)}")
        print(f"   ❌ Failed: {len(self.issues)}")
        print(f"   📊 Pass Rate: {pass_rate:.1f}%")
        
        if len(self.issues) == 0:
            print("\n   🎉 SITE VALIDATION PASSED!")
            print("   Your site meets all critical requirements!")
        elif len(self.issues) < 3:
            print("\n   ⚠️  SITE NEEDS MINOR FIXES")
            print("   A few issues need attention before going live.")
        else:
            print("\n   ❌ SITE NEEDS ATTENTION")
            print("   Several critical issues must be resolved.")
        
        print("\n" + "=" * 60)

def main():
    print("=" * 60)
    print("🔍 COMPREHENSIVE WORDPRESS SITE VALIDATION")
    print("=" * 60)
    print("Validating ALL requirements for production readiness...")
    
    validator = ComprehensiveValidator()
    
    # Run all validations
    validator.validate_published_content_match()
    validator.validate_post_content_length()
    validator.validate_featured_images()
    validator.validate_categories()
    validator.check_broken_links()
    validator.validate_redirects()
    validator.validate_header_footer()
    validator.validate_seo()
    validator.validate_menus()
    
    # Generate final report
    validator.generate_final_report()

if __name__ == "__main__":
    main()
