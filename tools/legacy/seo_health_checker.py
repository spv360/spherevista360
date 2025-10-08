#!/usr/bin/env python3
"""
SEO Health Checker - Comprehensive WordPress SEO Analysis
Analyzes website SEO health across multiple factors
"""

import os
import sys
import requests
import base64
from typing import Dict, List, Optional
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse

class SEOHealthChecker:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', '').rstrip('/')
        self.wp_user = os.environ.get('WP_USER', '')
        self.wp_pass = os.environ.get('WP_APP_PASS', '')
        
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            # Try alternative environment variable names
            self.wp_site = os.environ.get('WP_URL', 'https://spherevista360.com').rstrip('/')
            self.wp_user = os.environ.get('WP_USERNAME', '')
            self.wp_pass = os.environ.get('WP_APP_PASSWORD', '')
            
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            raise ValueError("WordPress credentials not set")
        
        # Set up authentication
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'User-Agent': 'SphereVista360-SEO-Checker/1.0'
        }
        
        self.base_url = f"{self.wp_site}/wp-json/wp/v2"
        self.seo_score = 0
        self.max_score = 0
        self.issues = []
        self.recommendations = []
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected as {user_data.get('name')} with roles: {user_data.get('roles')}")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def check_site_accessibility(self) -> Dict:
        """Check if the website is accessible and loading properly"""
        print("🌐 Checking Site Accessibility...")
        
        try:
            response = requests.get(self.wp_site, timeout=10)
            load_time = response.elapsed.total_seconds()
            
            accessibility = {
                'status_code': response.status_code,
                'load_time': load_time,
                'accessible': response.status_code == 200,
                'ssl_enabled': self.wp_site.startswith('https://'),
                'content_length': len(response.content)
            }
            
            if accessibility['accessible']:
                self.seo_score += 20
                print(f"   ✅ Site accessible (Status: {response.status_code})")
            else:
                self.issues.append(f"Site not accessible (Status: {response.status_code})")
                print(f"   ❌ Site not accessible (Status: {response.status_code})")
            
            if accessibility['ssl_enabled']:
                self.seo_score += 10
                print(f"   ✅ SSL/HTTPS enabled")
            else:
                self.issues.append("SSL/HTTPS not enabled")
                print(f"   ❌ SSL/HTTPS not enabled")
            
            if load_time < 3.0:
                self.seo_score += 10
                print(f"   ✅ Good load time: {load_time:.2f}s")
            else:
                self.issues.append(f"Slow load time: {load_time:.2f}s")
                print(f"   ⚠️ Slow load time: {load_time:.2f}s")
            
            self.max_score += 40
            return accessibility
            
        except Exception as e:
            self.issues.append(f"Site accessibility check failed: {e}")
            print(f"   ❌ Error checking accessibility: {e}")
            self.max_score += 40
            return {'accessible': False, 'error': str(e)}
    
    def check_meta_tags(self) -> Dict:
        """Check essential meta tags"""
        print("🏷️ Checking Meta Tags...")
        
        try:
            response = requests.get(self.wp_site, timeout=10)
            content = response.text
            
            meta_checks = {
                'title': bool(re.search(r'<title[^>]*>(.+?)</title>', content, re.IGNORECASE)),
                'description': bool(re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)),
                'keywords': bool(re.search(r'<meta[^>]*name=["\']keywords["\']', content, re.IGNORECASE)),
                'robots': bool(re.search(r'<meta[^>]*name=["\']robots["\']', content, re.IGNORECASE)),
                'viewport': bool(re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE)),
                'og_title': bool(re.search(r'<meta[^>]*property=["\']og:title["\']', content, re.IGNORECASE)),
                'og_description': bool(re.search(r'<meta[^>]*property=["\']og:description["\']', content, re.IGNORECASE)),
                'canonical': bool(re.search(r'<link[^>]*rel=["\']canonical["\']', content, re.IGNORECASE))
            }
            
            # Score meta tags
            for tag, present in meta_checks.items():
                if present:
                    self.seo_score += 5
                    print(f"   ✅ {tag.replace('_', ' ').title()} tag present")
                else:
                    self.issues.append(f"Missing {tag.replace('_', ' ')} meta tag")
                    print(f"   ❌ Missing {tag.replace('_', ' ')} meta tag")
            
            self.max_score += len(meta_checks) * 5
            return meta_checks
            
        except Exception as e:
            self.issues.append(f"Meta tags check failed: {e}")
            print(f"   ❌ Error checking meta tags: {e}")
            self.max_score += 40
            return {}
    
    def check_content_structure(self) -> Dict:
        """Check content structure and headings"""
        print("📝 Checking Content Structure...")
        
        try:
            response = requests.get(self.wp_site, timeout=10)
            content = response.text
            
            structure = {
                'h1_count': len(re.findall(r'<h1[^>]*>', content, re.IGNORECASE)),
                'h2_count': len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE)),
                'h3_count': len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE)),
                'img_count': len(re.findall(r'<img[^>]*>', content, re.IGNORECASE)),
                'alt_tags': len(re.findall(r'<img[^>]*alt=["\']([^"\']+)["\']', content, re.IGNORECASE)),
                'internal_links': len(re.findall(rf'<a[^>]*href=["\'][^"\']*{urlparse(self.wp_site).netloc}[^"\']*["\']', content, re.IGNORECASE)),
                'word_count': len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', '', content)))
            }
            
            # Analyze structure quality
            if structure['h1_count'] == 1:
                self.seo_score += 10
                print(f"   ✅ Proper H1 usage (1 H1 tag)")
            elif structure['h1_count'] == 0:
                self.issues.append("No H1 tag found")
                print(f"   ❌ No H1 tag found")
            else:
                self.issues.append(f"Multiple H1 tags ({structure['h1_count']})")
                print(f"   ⚠️ Multiple H1 tags ({structure['h1_count']})")
            
            if structure['h2_count'] > 0:
                self.seo_score += 5
                print(f"   ✅ H2 tags present ({structure['h2_count']})")
            else:
                self.issues.append("No H2 tags found")
                print(f"   ❌ No H2 tags found")
            
            if structure['img_count'] > 0:
                self.seo_score += 5
                print(f"   ✅ Images present ({structure['img_count']})")
                
                alt_ratio = structure['alt_tags'] / structure['img_count'] if structure['img_count'] > 0 else 0
                if alt_ratio >= 0.8:
                    self.seo_score += 10
                    print(f"   ✅ Good alt tag coverage ({alt_ratio:.1%})")
                else:
                    self.issues.append(f"Poor alt tag coverage ({alt_ratio:.1%})")
                    print(f"   ⚠️ Poor alt tag coverage ({alt_ratio:.1%})")
            else:
                self.issues.append("No images found")
                print(f"   ❌ No images found")
            
            if structure['word_count'] > 300:
                self.seo_score += 10
                print(f"   ✅ Sufficient content ({structure['word_count']} words)")
            else:
                self.issues.append(f"Insufficient content ({structure['word_count']} words)")
                print(f"   ⚠️ Insufficient content ({structure['word_count']} words)")
            
            self.max_score += 40
            return structure
            
        except Exception as e:
            self.issues.append(f"Content structure check failed: {e}")
            print(f"   ❌ Error checking content structure: {e}")
            self.max_score += 40
            return {}
    
    def check_sitemap_and_robots(self) -> Dict:
        """Check sitemap.xml and robots.txt"""
        print("🗺️ Checking Sitemap and Robots...")
        
        sitemap_robots = {
            'sitemap_xml': False,
            'robots_txt': False,
            'sitemap_in_robots': False
        }
        
        try:
            # Check sitemap.xml
            sitemap_response = requests.get(f"{self.wp_site}/sitemap.xml", timeout=10)
            if sitemap_response.status_code == 200:
                sitemap_robots['sitemap_xml'] = True
                self.seo_score += 15
                print(f"   ✅ sitemap.xml accessible")
            else:
                self.issues.append("sitemap.xml not found")
                print(f"   ❌ sitemap.xml not found")
            
            # Check robots.txt
            robots_response = requests.get(f"{self.wp_site}/robots.txt", timeout=10)
            if robots_response.status_code == 200:
                sitemap_robots['robots_txt'] = True
                self.seo_score += 10
                print(f"   ✅ robots.txt accessible")
                
                # Check if sitemap is referenced in robots.txt
                if 'sitemap' in robots_response.text.lower():
                    sitemap_robots['sitemap_in_robots'] = True
                    self.seo_score += 5
                    print(f"   ✅ Sitemap referenced in robots.txt")
                else:
                    self.recommendations.append("Add sitemap reference to robots.txt")
                    print(f"   ⚠️ Sitemap not referenced in robots.txt")
            else:
                self.issues.append("robots.txt not found")
                print(f"   ❌ robots.txt not found")
            
            self.max_score += 30
            return sitemap_robots
            
        except Exception as e:
            self.issues.append(f"Sitemap/robots check failed: {e}")
            print(f"   ❌ Error checking sitemap/robots: {e}")
            self.max_score += 30
            return sitemap_robots
    
    def check_social_media_integration(self) -> Dict:
        """Check social media meta tags and integration"""
        print("📱 Checking Social Media Integration...")
        
        try:
            response = requests.get(self.wp_site, timeout=10)
            content = response.text
            
            social_checks = {
                'og_title': bool(re.search(r'<meta[^>]*property=["\']og:title["\']', content, re.IGNORECASE)),
                'og_description': bool(re.search(r'<meta[^>]*property=["\']og:description["\']', content, re.IGNORECASE)),
                'og_image': bool(re.search(r'<meta[^>]*property=["\']og:image["\']', content, re.IGNORECASE)),
                'og_url': bool(re.search(r'<meta[^>]*property=["\']og:url["\']', content, re.IGNORECASE)),
                'twitter_card': bool(re.search(r'<meta[^>]*name=["\']twitter:card["\']', content, re.IGNORECASE)),
                'twitter_title': bool(re.search(r'<meta[^>]*name=["\']twitter:title["\']', content, re.IGNORECASE)),
                'twitter_description': bool(re.search(r'<meta[^>]*name=["\']twitter:description["\']', content, re.IGNORECASE))
            }
            
            social_score = sum(social_checks.values())
            if social_score >= 5:
                self.seo_score += 15
                print(f"   ✅ Good social media integration ({social_score}/7)")
            elif social_score >= 3:
                self.seo_score += 10
                print(f"   ⚠️ Basic social media integration ({social_score}/7)")
            else:
                self.issues.append(f"Poor social media integration ({social_score}/7)")
                print(f"   ❌ Poor social media integration ({social_score}/7)")
            
            for tag, present in social_checks.items():
                if not present:
                    self.recommendations.append(f"Add {tag.replace('_', ':')} meta tag")
            
            self.max_score += 15
            return social_checks
            
        except Exception as e:
            self.issues.append(f"Social media check failed: {e}")
            print(f"   ❌ Error checking social media integration: {e}")
            self.max_score += 15
            return {}
    
    def check_posts_seo(self) -> Dict:
        """Check SEO quality of recent posts"""
        print("📰 Checking Posts SEO...")
        
        try:
            response = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={'per_page': 10, 'status': 'publish'},
                timeout=10
            )
            
            if response.status_code != 200:
                self.issues.append(f"Failed to fetch posts: {response.status_code}")
                self.max_score += 20
                return {}
            
            posts = response.json()
            
            seo_stats = {
                'total_posts': len(posts),
                'posts_with_excerpts': 0,
                'posts_with_featured_images': 0,
                'avg_title_length': 0,
                'avg_content_length': 0
            }
            
            if not posts:
                self.issues.append("No published posts found")
                print(f"   ❌ No published posts found")
                self.max_score += 20
                return seo_stats
            
            title_lengths = []
            content_lengths = []
            
            for post in posts:
                # Check excerpts
                if post.get('excerpt', {}).get('rendered', '').strip():
                    seo_stats['posts_with_excerpts'] += 1
                
                # Check featured images
                if post.get('featured_media', 0) > 0:
                    seo_stats['posts_with_featured_images'] += 1
                
                # Analyze titles
                title = post.get('title', {}).get('rendered', '')
                title_length = len(title)
                title_lengths.append(title_length)
                
                # Analyze content
                content = post.get('content', {}).get('rendered', '')
                content_length = len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', '', content)))
                content_lengths.append(content_length)
            
            seo_stats['avg_title_length'] = sum(title_lengths) / len(title_lengths) if title_lengths else 0
            seo_stats['avg_content_length'] = sum(content_lengths) / len(content_lengths) if content_lengths else 0
            
            # Score posts SEO
            excerpt_ratio = seo_stats['posts_with_excerpts'] / seo_stats['total_posts']
            if excerpt_ratio >= 0.8:
                self.seo_score += 5
                print(f"   ✅ Good excerpt usage ({excerpt_ratio:.1%})")
            else:
                self.recommendations.append(f"Add excerpts to more posts ({excerpt_ratio:.1%})")
                print(f"   ⚠️ Poor excerpt usage ({excerpt_ratio:.1%})")
            
            image_ratio = seo_stats['posts_with_featured_images'] / seo_stats['total_posts']
            if image_ratio >= 0.8:
                self.seo_score += 5
                print(f"   ✅ Good featured image usage ({image_ratio:.1%})")
            else:
                self.recommendations.append(f"Add featured images to more posts ({image_ratio:.1%})")
                print(f"   ⚠️ Poor featured image usage ({image_ratio:.1%})")
            
            if 30 <= seo_stats['avg_title_length'] <= 60:
                self.seo_score += 5
                print(f"   ✅ Good average title length ({seo_stats['avg_title_length']:.1f} chars)")
            else:
                self.recommendations.append(f"Optimize title lengths (avg: {seo_stats['avg_title_length']:.1f} chars)")
                print(f"   ⚠️ Suboptimal title length ({seo_stats['avg_title_length']:.1f} chars)")
            
            if seo_stats['avg_content_length'] >= 300:
                self.seo_score += 5
                print(f"   ✅ Sufficient content length ({seo_stats['avg_content_length']:.0f} words avg)")
            else:
                self.recommendations.append(f"Increase content length (avg: {seo_stats['avg_content_length']:.0f} words)")
                print(f"   ⚠️ Short content length ({seo_stats['avg_content_length']:.0f} words avg)")
            
            self.max_score += 20
            return seo_stats
            
        except Exception as e:
            self.issues.append(f"Posts SEO check failed: {e}")
            print(f"   ❌ Error checking posts SEO: {e}")
            self.max_score += 20
            return {}
    
    def generate_seo_report(self) -> Dict:
        """Generate comprehensive SEO report"""
        final_score = (self.seo_score / self.max_score * 100) if self.max_score > 0 else 0
        
        print(f"\n📊 SEO HEALTH REPORT")
        print("=" * 50)
        print(f"🎯 Overall SEO Score: {final_score:.1f}% ({self.seo_score}/{self.max_score})")
        
        if final_score >= 80:
            grade = "A"
            status = "Excellent"
            emoji = "🟢"
        elif final_score >= 70:
            grade = "B"
            status = "Good"
            emoji = "🟡"
        elif final_score >= 60:
            grade = "C"
            status = "Fair"
            emoji = "🟠"
        else:
            grade = "D"
            status = "Needs Improvement"
            emoji = "🔴"
        
        print(f"{emoji} SEO Grade: {grade} ({status})")
        
        if self.issues:
            print(f"\n❌ Issues Found ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        
        if self.recommendations:
            print(f"\n💡 Recommendations ({len(self.recommendations)}):")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"   {i}. {rec}")
        
        print(f"\n🎯 Priority Actions:")
        if final_score < 60:
            print("   1. Fix critical issues listed above")
            print("   2. Add missing meta tags")
            print("   3. Improve content structure")
            print("   4. Optimize page loading speed")
        elif final_score < 80:
            print("   1. Implement recommendations above")
            print("   2. Enhance social media integration")
            print("   3. Optimize post SEO")
            print("   4. Add structured data markup")
        else:
            print("   1. Monitor and maintain current SEO health")
            print("   2. Continue publishing quality content")
            print("   3. Build quality backlinks")
            print("   4. Track keyword rankings")
        
        return {
            'score': final_score,
            'grade': grade,
            'status': status,
            'issues_count': len(self.issues),
            'recommendations_count': len(self.recommendations),
            'issues': self.issues,
            'recommendations': self.recommendations
        }
    
    def run_seo_audit(self) -> Dict:
        """Run complete SEO audit"""
        print(f"🌐 Site: {self.wp_site}")
        print("🔍 SEO Health Audit - Comprehensive Analysis")
        print("=" * 55)
        
        if not self.test_connection():
            return {'error': 'Connection failed'}
        
        # Run all SEO checks
        accessibility = self.check_site_accessibility()
        meta_tags = self.check_meta_tags()
        content_structure = self.check_content_structure()
        sitemap_robots = self.check_sitemap_and_robots()
        social_media = self.check_social_media_integration()
        posts_seo = self.check_posts_seo()
        
        # Generate final report
        report = self.generate_seo_report()
        
        return {
            'report': report,
            'accessibility': accessibility,
            'meta_tags': meta_tags,
            'content_structure': content_structure,
            'sitemap_robots': sitemap_robots,
            'social_media': social_media,
            'posts_seo': posts_seo
        }

def main():
    """Main function"""
    try:
        checker = SEOHealthChecker()
        results = checker.run_seo_audit()
        
        if 'error' in results:
            print(f"❌ Audit failed: {results['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()