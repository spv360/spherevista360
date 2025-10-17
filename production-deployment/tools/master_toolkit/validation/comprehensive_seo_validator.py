#!/usr/bin/env python3
"""
Comprehensive SEO & Site Validation Tool
Uses master toolkit approach for SphereVista360
"""

import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

class ComprehensiveSiteValidator:
    def __init__(self):
        self.auth = HTTPBasicAuth(USERNAME, PASSWORD)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'site_url': WORDPRESS_URL,
            'seo': {},
            'content': {},
            'technical': {},
            'performance': {},
            'issues': [],
            'recommendations': []
        }
    
    def check_seo_titles(self):
        """Validate SEO titles"""
        print("\n📝 Checking SEO Titles & Meta Descriptions...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=20"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            posts = response.json()
            
            title_issues = []
            missing_excerpt = []
            
            for post in posts:
                title = post['title']['rendered']
                excerpt = post.get('excerpt', {}).get('rendered', '').strip()
                
                # Check title length (ideal: 50-60 chars)
                if len(title) > 70:
                    title_issues.append(f"{title[:50]}... (too long: {len(title)} chars)")
                elif len(title) < 30:
                    title_issues.append(f"{title} (too short: {len(title)} chars)")
                
                if not excerpt or len(excerpt) < 50:
                    missing_excerpt.append(title[:50])
            
            self.results['seo']['total_posts_checked'] = len(posts)
            self.results['seo']['title_issues'] = len(title_issues)
            self.results['seo']['missing_excerpts'] = len(missing_excerpt)
            
            if title_issues:
                print(f"   ⚠️  {len(title_issues)} posts with title length issues")
            else:
                print(f"   ✅ All post titles are well-optimized")
            
            if missing_excerpt:
                print(f"   ⚠️  {len(missing_excerpt)} posts with short/missing excerpts")
            else:
                print(f"   ✅ All posts have proper excerpts")
            
            return True
        return False
    
    def check_featured_images(self):
        """Check featured images status"""
        print("\n🖼️  Checking Featured Images...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            posts = response.json()
            
            with_images = sum(1 for p in posts if p.get('featured_media', 0) > 0)
            without_images = len(posts) - with_images
            
            self.results['content']['total_posts'] = len(posts)
            self.results['content']['posts_with_images'] = with_images
            self.results['content']['posts_without_images'] = without_images
            
            print(f"   📊 Total Posts: {len(posts)}")
            print(f"   ✅ With Featured Images: {with_images}")
            
            if without_images > 0:
                print(f"   ❌ Without Featured Images: {without_images}")
                self.results['issues'].append(f"{without_images} posts missing featured images")
            else:
                print(f"   ✅ All posts have featured images!")
            
            return True
        return False
    
    def check_categories(self):
        """Validate categories and taxonomies"""
        print("\n📂 Checking Categories & Taxonomies...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            categories = response.json()
            
            active_cats = [c for c in categories if c['count'] > 0]
            empty_cats = [c for c in categories if c['count'] == 0]
            
            self.results['content']['total_categories'] = len(categories)
            self.results['content']['active_categories'] = len(active_cats)
            self.results['content']['empty_categories'] = len(empty_cats)
            
            print(f"   📊 Total Categories: {len(categories)}")
            print(f"   ✅ Active Categories: {len(active_cats)}")
            
            if empty_cats:
                print(f"   ⚠️  Empty Categories: {len(empty_cats)}")
                for cat in empty_cats:
                    print(f"      - {cat['name']}")
            
            # Check for uncategorized posts
            url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?categories=1&per_page=1"
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                uncategorized = len(response.json())
                if uncategorized > 0:
                    self.results['issues'].append(f"{uncategorized} posts in Uncategorized")
            
            return True
        return False
    
    def check_internal_links(self):
        """Check for internal linking"""
        print("\n🔗 Checking Internal Links...")
        print("-" * 60)
        
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=10"
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            posts = response.json()
            
            posts_with_links = 0
            for post in posts:
                content = post['content']['rendered']
                if f'href="{WORDPRESS_URL}' in content or 'href="/' in content:
                    posts_with_links += 1
            
            self.results['seo']['posts_with_internal_links'] = posts_with_links
            self.results['seo']['posts_checked_for_links'] = len(posts)
            
            print(f"   ✅ {posts_with_links}/{len(posts)} posts have internal links")
            
            if posts_with_links < len(posts) / 2:
                self.results['recommendations'].append("Add more internal links between related posts")
            
            return True
        return False
    
    def check_sitemap(self):
        """Validate sitemap"""
        print("\n🗺️  Checking XML Sitemap...")
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
                self.results['seo']['sitemap_url'] = sitemap_url
                self.results['seo']['sitemap_exists'] = True
                
                # Check if it contains URLs
                if '<url>' in response.text or '<sitemap>' in response.text:
                    print(f"   ✅ Sitemap contains valid entries")
                return True
        
        print(f"   ❌ No sitemap found")
        self.results['seo']['sitemap_exists'] = False
        self.results['issues'].append("Sitemap not found or not accessible")
        return False
    
    def check_robots_txt(self):
        """Check robots.txt"""
        print("\n🤖 Checking robots.txt...")
        print("-" * 60)
        
        response = requests.get(f"{WORDPRESS_URL}/robots.txt")
        if response.status_code == 200:
            print(f"   ✅ robots.txt exists")
            
            content = response.text
            if 'Sitemap:' in content:
                print(f"   ✅ Sitemap referenced in robots.txt")
            else:
                print(f"   ⚠️  Sitemap not referenced in robots.txt")
                self.results['recommendations'].append("Add sitemap reference to robots.txt")
            
            if 'Disallow: /wp-admin/' in content:
                print(f"   ✅ Admin area properly blocked")
            
            self.results['seo']['robots_txt_exists'] = True
            return True
        else:
            print(f"   ❌ robots.txt not found")
            self.results['seo']['robots_txt_exists'] = False
            self.results['issues'].append("robots.txt not configured")
            return False
    
    def check_page_speed(self):
        """Basic page speed check"""
        print("\n⚡ Checking Page Speed...")
        print("-" * 60)
        
        import time
        start = time.time()
        response = requests.get(WORDPRESS_URL)
        load_time = time.time() - start
        
        self.results['performance']['homepage_load_time'] = round(load_time, 2)
        
        print(f"   📊 Homepage Load Time: {load_time:.2f}s")
        
        if load_time < 2:
            print(f"   ✅ Excellent load time!")
        elif load_time < 3:
            print(f"   ✅ Good load time")
        elif load_time < 5:
            print(f"   ⚠️  Moderate load time - room for improvement")
        else:
            print(f"   ❌ Slow load time - needs optimization")
            self.results['issues'].append(f"Slow page load time: {load_time:.2f}s")
        
        return True
    
    def check_mobile_responsive(self):
        """Check mobile viewport meta tag"""
        print("\n📱 Checking Mobile Responsiveness...")
        print("-" * 60)
        
        response = requests.get(WORDPRESS_URL)
        if response.status_code == 200:
            content = response.text
            
            if 'viewport' in content.lower():
                print(f"   ✅ Mobile viewport meta tag present")
                self.results['technical']['mobile_viewport'] = True
            else:
                print(f"   ❌ Mobile viewport meta tag missing")
                self.results['technical']['mobile_viewport'] = False
                self.results['issues'].append("Mobile viewport meta tag missing")
            
            return True
        return False
    
    def check_ssl(self):
        """Check SSL/HTTPS"""
        print("\n🔒 Checking SSL/HTTPS...")
        print("-" * 60)
        
        if WORDPRESS_URL.startswith('https://'):
            print(f"   ✅ Site uses HTTPS")
            self.results['technical']['uses_https'] = True
        else:
            print(f"   ❌ Site not using HTTPS")
            self.results['technical']['uses_https'] = False
            self.results['issues'].append("Site not using HTTPS - security risk")
        
        return True
    
    def check_schema_markup(self):
        """Check for Schema.org markup"""
        print("\n📊 Checking Schema Markup...")
        print("-" * 60)
        
        response = requests.get(WORDPRESS_URL)
        if response.status_code == 200:
            content = response.text
            
            if 'schema.org' in content.lower() or 'application/ld+json' in content.lower():
                print(f"   ✅ Schema markup found")
                self.results['seo']['schema_markup'] = True
            else:
                print(f"   ⚠️  No Schema markup detected")
                self.results['seo']['schema_markup'] = False
                self.results['recommendations'].append("Add Schema.org structured data")
            
            return True
        return False
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE SEO & VALIDATION REPORT")
        print("=" * 60)
        
        print(f"\n🌐 Site: {WORDPRESS_URL}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Calculate SEO Score
        total_checks = 0
        passed_checks = 0
        
        if self.results['seo'].get('sitemap_exists'):
            passed_checks += 1
        total_checks += 1
        
        if self.results['seo'].get('robots_txt_exists'):
            passed_checks += 1
        total_checks += 1
        
        if self.results['content'].get('posts_without_images', 1) == 0:
            passed_checks += 1
        total_checks += 1
        
        if self.results['technical'].get('uses_https'):
            passed_checks += 1
        total_checks += 1
        
        if self.results['technical'].get('mobile_viewport'):
            passed_checks += 1
        total_checks += 1
        
        if self.results['performance'].get('homepage_load_time', 10) < 3:
            passed_checks += 1
        total_checks += 1
        
        seo_score = int((passed_checks / total_checks) * 100)
        self.results['seo_score'] = seo_score
        
        print(f"\n🎯 SEO SCORE: {seo_score}/100")
        
        if seo_score >= 90:
            print("   ✅ Excellent!")
        elif seo_score >= 70:
            print("   ✅ Good")
        elif seo_score >= 50:
            print("   ⚠️  Needs Improvement")
        else:
            print("   ❌ Poor - Requires Immediate Attention")
        
        # Issues Summary
        print("\n" + "=" * 60)
        print("⚠️  ISSUES FOUND")
        print("=" * 60)
        
        if self.results['issues']:
            for i, issue in enumerate(self.results['issues'], 1):
                print(f"   {i}. {issue}")
        else:
            print("   ✅ No critical issues found!")
        
        # Recommendations
        print("\n" + "=" * 60)
        print("💡 RECOMMENDATIONS")
        print("=" * 60)
        
        if self.results['recommendations']:
            for i, rec in enumerate(self.results['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print("   ✅ Site is well-optimized!")
        
        # Content Summary
        print("\n" + "=" * 60)
        print("📊 CONTENT SUMMARY")
        print("=" * 60)
        print(f"   📰 Total Posts: {self.results['content'].get('total_posts', 0)}")
        print(f"   🖼️  Posts with Images: {self.results['content'].get('posts_with_images', 0)}")
        print(f"   📂 Active Categories: {self.results['content'].get('active_categories', 0)}")
        
        # Technical Summary
        print("\n" + "=" * 60)
        print("🔧 TECHNICAL SUMMARY")
        print("=" * 60)
        print(f"   🔒 HTTPS: {'✅ Yes' if self.results['technical'].get('uses_https') else '❌ No'}")
        print(f"   📱 Mobile Viewport: {'✅ Yes' if self.results['technical'].get('mobile_viewport') else '❌ No'}")
        print(f"   ⚡ Load Time: {self.results['performance'].get('homepage_load_time', 'N/A')}s")
        
        return self.results

def main():
    print("=" * 60)
    print("🔍 COMPREHENSIVE SEO & SITE VALIDATION")
    print("=" * 60)
    
    validator = ComprehensiveSiteValidator()
    
    # Run all checks
    validator.check_seo_titles()
    validator.check_featured_images()
    validator.check_categories()
    validator.check_internal_links()
    validator.check_sitemap()
    validator.check_robots_txt()
    validator.check_page_speed()
    validator.check_mobile_responsive()
    validator.check_ssl()
    validator.check_schema_markup()
    
    # Generate report
    results = validator.generate_report()
    
    # Save detailed report
    with open('comprehensive_seo_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed report saved: comprehensive_seo_report.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
