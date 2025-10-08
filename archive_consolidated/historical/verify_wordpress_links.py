#!/usr/bin/env python3
"""
WordPress Image and Link Verification Tool
Comprehensive check for all images and internal links
"""

import os
import requests
import base64
import json
import re
from urllib.parse import urlparse, urljoin
from datetime import datetime

class WordPressVerifier:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
        self.issues = {
            'broken_images': [],
            'missing_images': [],
            'broken_internal_links': [],
            'broken_external_links': [],
            'seo_issues': []
        }
        
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def get_all_posts(self):
        """Get all published posts"""
        all_posts = []
        page = 1
        per_page = 100
        
        while True:
            response = requests.get(
                f"{self.api}/posts",
                headers=self.headers,
                params={'per_page': per_page, 'page': page, 'status': 'publish'}
            )
            
            if response.status_code != 200:
                break
                
            posts = response.json()
            if not posts:
                break
                
            all_posts.extend(posts)
            page += 1
            
        return all_posts
    
    def get_all_categories(self):
        """Get all categories"""
        response = requests.get(f"{self.api}/categories", headers=self.headers, params={'per_page': 100})
        return response.json() if response.status_code == 200 else []
    
    def check_image_url(self, url, context=""):
        """Check if an image URL is accessible"""
        try:
            # Clean up the URL
            url = url.strip()
            if not url:
                return False, "Empty URL"
            
            # Handle relative URLs
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                url = self.site + url
            
            # Verify URL format
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format"
            
            # Make request with timeout
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                if 'image' in content_type:
                    return True, "OK"
                else:
                    return False, f"Not an image (content-type: {content_type})"
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def check_internal_link(self, url):
        """Check if an internal link is accessible"""
        try:
            if not url.startswith(self.site):
                return True, "External link"
            
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200, f"HTTP {response.status_code}"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def extract_images_from_content(self, content):
        """Extract all image URLs from post content"""
        # Find img tags
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        images = re.findall(img_pattern, content, re.IGNORECASE)
        
        # Find markdown images
        md_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        md_images = re.findall(md_pattern, content)
        images.extend([img[1] for img in md_images])
        
        # Find background images in style attributes
        bg_pattern = r'background-image:\s*url\(["\']?([^"\']+)["\']?\)'
        bg_images = re.findall(bg_pattern, content, re.IGNORECASE)
        images.extend(bg_images)
        
        return list(set(images))  # Remove duplicates
    
    def extract_links_from_content(self, content):
        """Extract all links from post content"""
        # Find anchor tags
        link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>'
        links = re.findall(link_pattern, content, re.IGNORECASE)
        
        # Find markdown links
        md_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        md_links = re.findall(md_pattern, content)
        links.extend([link[1] for link in md_links])
        
        return list(set(links))  # Remove duplicates
    
    def verify_post(self, post):
        """Verify all images and links in a single post"""
        post_id = post['id']
        post_title = post['title']['rendered']
        content = post['content']['rendered']
        
        print(f"\n🔍 Verifying: {post_title} (ID: {post_id})")
        
        # Check images
        images = self.extract_images_from_content(content)
        print(f"   Found {len(images)} images")
        
        for img_url in images:
            is_valid, error = self.check_image_url(img_url, f"Post: {post_title}")
            if not is_valid:
                self.issues['broken_images'].append({
                    'post_id': post_id,
                    'post_title': post_title,
                    'image_url': img_url,
                    'error': error
                })
                print(f"   ❌ Image: {img_url[:50]}... - {error}")
            else:
                print(f"   ✅ Image: {img_url[:50]}...")
        
        # Check links
        links = self.extract_links_from_content(content)
        internal_links = [link for link in links if link.startswith(self.site) or link.startswith('/')]
        external_links = [link for link in links if not link.startswith(self.site) and not link.startswith('/') and '://' in link]
        
        print(f"   Found {len(internal_links)} internal links, {len(external_links)} external links")
        
        # Verify internal links
        for link in internal_links:
            if link.startswith('/'):
                full_link = self.site + link
            else:
                full_link = link
                
            is_valid, error = self.check_internal_link(full_link)
            if not is_valid:
                self.issues['broken_internal_links'].append({
                    'post_id': post_id,
                    'post_title': post_title,
                    'link_url': full_link,
                    'error': error
                })
                print(f"   ❌ Internal link: {full_link[:50]}... - {error}")
            else:
                print(f"   ✅ Internal link: {full_link[:50]}...")
        
        # Check featured image
        if post.get('featured_media') and post['featured_media'] > 0:
            media_response = requests.get(f"{self.api}/media/{post['featured_media']}", headers=self.headers)
            if media_response.status_code == 200:
                media = media_response.json()
                featured_image_url = media.get('source_url', '')
                if featured_image_url:
                    is_valid, error = self.check_image_url(featured_image_url, f"Featured image: {post_title}")
                    if not is_valid:
                        self.issues['broken_images'].append({
                            'post_id': post_id,
                            'post_title': post_title,
                            'image_url': featured_image_url,
                            'error': f"Featured image: {error}",
                            'type': 'featured'
                        })
                        print(f"   ❌ Featured image: {featured_image_url[:50]}... - {error}")
                    else:
                        print(f"   ✅ Featured image: {featured_image_url[:50]}...")
    
    def verify_categories(self):
        """Verify category links and structure"""
        print(f"\n🏷️  Verifying Categories")
        categories = self.get_all_categories()
        
        for category in categories:
            if category['count'] > 0:  # Only check categories with posts
                category_url = f"{self.site}/category/{category['slug']}/"
                is_valid, error = self.check_internal_link(category_url)
                
                if not is_valid:
                    self.issues['broken_internal_links'].append({
                        'type': 'category',
                        'category_name': category['name'],
                        'category_url': category_url,
                        'error': error
                    })
                    print(f"   ❌ Category: {category['name']} - {error}")
                else:
                    print(f"   ✅ Category: {category['name']} ({category['count']} posts)")
    
    def generate_report(self):
        """Generate comprehensive verification report"""
        print(f"\n{'='*60}")
        print(f"🔍 WORDPRESS VERIFICATION REPORT")
        print(f"{'='*60}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Site: {self.site}")
        
        # Summary
        total_issues = sum(len(issues) for issues in self.issues.values())
        print(f"\n📊 SUMMARY")
        print(f"Total Issues Found: {total_issues}")
        
        for issue_type, issues in self.issues.items():
            if issues:
                print(f"  {issue_type.replace('_', ' ').title()}: {len(issues)}")
        
        # Detailed issues
        if self.issues['broken_images']:
            print(f"\n❌ BROKEN IMAGES ({len(self.issues['broken_images'])})")
            for issue in self.issues['broken_images']:
                print(f"  Post: {issue['post_title']} (ID: {issue['post_id']})")
                print(f"  Image: {issue['image_url']}")
                print(f"  Error: {issue['error']}")
                print()
        
        if self.issues['broken_internal_links']:
            print(f"\n❌ BROKEN INTERNAL LINKS ({len(self.issues['broken_internal_links'])})")
            for issue in self.issues['broken_internal_links']:
                if 'post_title' in issue:
                    print(f"  Post: {issue['post_title']} (ID: {issue['post_id']})")
                elif 'category_name' in issue:
                    print(f"  Category: {issue['category_name']}")
                print(f"  Link: {issue['link_url'] if 'link_url' in issue else issue['category_url']}")
                print(f"  Error: {issue['error']}")
                print()
        
        if total_issues == 0:
            print(f"\n✅ ALL IMAGES AND LINKS ARE WORKING CORRECTLY!")
            print(f"No issues found during verification.")
        
        return total_issues
    
    def run_verification(self):
        """Run complete verification"""
        print(f"🚀 Starting WordPress Verification")
        print(f"Site: {self.site}")
        
        # Get all posts
        posts = self.get_all_posts()
        print(f"Found {len(posts)} published posts to verify")
        
        # Verify each post
        for post in posts:
            self.verify_post(post)
        
        # Verify categories
        self.verify_categories()
        
        # Generate report
        return self.generate_report()

if __name__ == "__main__":
    verifier = WordPressVerifier()
    issues_found = verifier.run_verification()
    
    # Exit with error code if issues found
    import sys
    sys.exit(1 if issues_found > 0 else 0)