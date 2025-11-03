#!/usr/bin/env python3
"""
Quick SEO & Google AdSense Compliance Checker
No external dependencies - uses only standard library
"""

import requests
import json
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse

class QuickSEOValidator:
    def __init__(self, site_url="https://spherevista360.com"):
        self.site_url = site_url.rstrip('/')
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'site_url': self.site_url,
            'seo_score': 0,
            'adsense_compliance': True,
            'issues': [],
            'passed': []
        }
    
    def check_homepage(self):
        """Check homepage SEO and AdSense compliance"""
        print(f"\n🔍 Checking Homepage: {self.site_url}")
        print("=" * 70)
        
        try:
            response = requests.get(self.site_url, timeout=10)
            html = response.text
            
            # SEO Checks
            self._check_title(html)
            self._check_meta_description(html)
            self._check_h1_tags(html)
            self._check_images(html)
            self._check_internal_links(html)
            
            # AdSense Compliance Checks
            self._check_content_quality(html)
            self._check_navigation(html)
            self._check_footer_links(html)
            self._check_contact_info(html)
            
            # Calculate score
            total_checks = len(self.results['passed']) + len(self.results['issues'])
            if total_checks > 0:
                self.results['seo_score'] = int((len(self.results['passed']) / total_checks) * 100)
            
        except Exception as e:
            self.results['issues'].append(f"❌ Failed to fetch homepage: {e}")
            self.results['adsense_compliance'] = False
    
    def _check_title(self, html):
        """Check page title"""
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            if len(title) > 0 and len(title) <= 60:
                self.results['passed'].append(f"✅ Page title present and optimal length: '{title}'")
            elif len(title) > 60:
                self.results['issues'].append(f"⚠️ Page title too long ({len(title)} chars): '{title[:60]}...'")
            else:
                self.results['issues'].append("❌ Page title is empty")
        else:
            self.results['issues'].append("❌ No page title found")
            self.results['adsense_compliance'] = False
    
    def _check_meta_description(self, html):
        """Check meta description"""
        meta_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        if meta_match:
            desc = meta_match.group(1)
            if 120 <= len(desc) <= 160:
                self.results['passed'].append(f"✅ Meta description optimal: {len(desc)} chars")
            elif len(desc) < 120:
                self.results['issues'].append(f"⚠️ Meta description too short: {len(desc)} chars (recommend 120-160)")
            else:
                self.results['issues'].append(f"⚠️ Meta description too long: {len(desc)} chars")
        else:
            self.results['issues'].append("❌ No meta description found")
    
    def _check_h1_tags(self, html):
        """Check H1 tags"""
        h1_tags = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
        if len(h1_tags) == 1:
            h1_text = re.sub(r'<[^>]+>', '', h1_tags[0]).strip()
            self.results['passed'].append(f"✅ Single H1 tag found: '{h1_text[:50]}...'")
        elif len(h1_tags) > 1:
            self.results['issues'].append(f"⚠️ Multiple H1 tags found: {len(h1_tags)} (should have only 1)")
        else:
            self.results['issues'].append("❌ No H1 tag found")
    
    def _check_images(self, html):
        """Check images have alt text"""
        img_tags = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
        imgs_without_alt = [img for img in img_tags if 'alt=' not in img.lower()]
        
        if len(img_tags) > 0:
            if len(imgs_without_alt) == 0:
                self.results['passed'].append(f"✅ All {len(img_tags)} images have alt text")
            else:
                self.results['issues'].append(f"⚠️ {len(imgs_without_alt)} of {len(img_tags)} images missing alt text")
        else:
            self.results['passed'].append("✅ No images found (or page is text-based)")
    
    def _check_internal_links(self, html):
        """Check internal links"""
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        internal_links = [link for link in links if self.site_url in link or link.startswith('/')]
        
        if len(internal_links) >= 5:
            self.results['passed'].append(f"✅ Good internal linking: {len(internal_links)} internal links")
        elif len(internal_links) > 0:
            self.results['issues'].append(f"⚠️ Limited internal linking: only {len(internal_links)} links (recommend 5+)")
        else:
            self.results['issues'].append("❌ No internal links found")
    
    def _check_content_quality(self, html):
        """Check content quality for AdSense"""
        # Remove HTML tags and count words
        text = re.sub(r'<[^>]+>', ' ', html)
        words = text.split()
        word_count = len(words)
        
        if word_count >= 300:
            self.results['passed'].append(f"✅ Sufficient content: ~{word_count} words (AdSense requires 300+)")
        else:
            self.results['issues'].append(f"❌ Insufficient content: ~{word_count} words (AdSense requires 300+)")
            self.results['adsense_compliance'] = False
    
    def _check_navigation(self, html):
        """Check navigation menu for AdSense"""
        nav_found = '<nav' in html.lower() or 'menu' in html.lower()
        
        if nav_found:
            self.results['passed'].append("✅ Navigation menu detected (AdSense requirement)")
        else:
            self.results['issues'].append("❌ Navigation menu not clearly detected (AdSense requirement)")
            self.results['adsense_compliance'] = False
    
    def _check_footer_links(self, html):
        """Check essential footer links for AdSense"""
        essential_pages = ['privacy', 'contact', 'about', 'terms', 'disclaimer']
        found_pages = [page for page in essential_pages if page in html.lower()]
        
        if len(found_pages) >= 3:
            self.results['passed'].append(f"✅ Essential pages found: {', '.join(found_pages)} (AdSense requirement)")
        else:
            self.results['issues'].append(f"⚠️ Missing essential pages. Found: {', '.join(found_pages) if found_pages else 'none'}")
            self.results['issues'].append("   Required for AdSense: Privacy Policy, Contact, About")
            self.results['adsense_compliance'] = False
    
    def _check_contact_info(self, html):
        """Check contact information"""
        contact_indicators = ['email', 'contact', '@', 'mailto']
        has_contact = any(indicator in html.lower() for indicator in contact_indicators)
        
        if has_contact:
            self.results['passed'].append("✅ Contact information found (AdSense requirement)")
        else:
            self.results['issues'].append("❌ No contact information found (AdSense requirement)")
            self.results['adsense_compliance'] = False
    
    def check_essential_pages(self):
        """Check AdSense required pages"""
        print(f"\n📄 Checking Essential Pages (AdSense Requirements)")
        print("=" * 70)
        
        essential_pages = {
            'privacy-policy': 'Privacy Policy',
            'contact': 'Contact',
            'about': 'About',
            'disclaimer': 'Disclaimer',
            'terms-of-service': 'Terms of Service'
        }
        
        for slug, name in essential_pages.items():
            url = f"{self.site_url}/{slug}/"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    # Check if page has content
                    text = re.sub(r'<[^>]+>', ' ', response.text)
                    word_count = len(text.split())
                    if word_count >= 100:
                        self.results['passed'].append(f"✅ {name} page exists with sufficient content")
                    else:
                        self.results['issues'].append(f"⚠️ {name} page exists but has minimal content ({word_count} words)")
                else:
                    self.results['issues'].append(f"❌ {name} page not found (HTTP {response.status_code})")
                    self.results['adsense_compliance'] = False
            except Exception as e:
                self.results['issues'].append(f"❌ Failed to check {name} page: {e}")
                self.results['adsense_compliance'] = False
    
    def check_robots_txt(self):
        """Check robots.txt"""
        print(f"\n🤖 Checking robots.txt")
        print("=" * 70)
        
        url = f"{self.site_url}/robots.txt"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.results['passed'].append("✅ robots.txt file exists")
                
                # Check for AdSense bot
                if 'adsbot-google' not in response.text.lower():
                    self.results['passed'].append("✅ No blocks on AdSense bot (good)")
                else:
                    self.results['issues'].append("⚠️ Check robots.txt - may be blocking AdSense bot")
            else:
                self.results['issues'].append("⚠️ robots.txt not found (optional but recommended)")
        except Exception as e:
            self.results['issues'].append(f"⚠️ Could not check robots.txt: {e}")
    
    def check_mobile_friendly(self):
        """Check mobile viewport tag"""
        print(f"\n📱 Checking Mobile-Friendliness")
        print("=" * 70)
        
        try:
            response = requests.get(self.site_url, timeout=10)
            html = response.text
            
            viewport_match = re.search(r'<meta\s+name=["\']viewport["\']', html, re.IGNORECASE)
            if viewport_match:
                self.results['passed'].append("✅ Mobile viewport meta tag present")
            else:
                self.results['issues'].append("❌ Missing viewport meta tag (critical for mobile and AdSense)")
                self.results['adsense_compliance'] = False
            
            # Check for responsive design indicators
            responsive_indicators = ['@media', 'max-width', 'min-width', 'responsive']
            has_responsive = any(indicator in html for indicator in responsive_indicators)
            
            if has_responsive:
                self.results['passed'].append("✅ Responsive design detected")
            else:
                self.results['issues'].append("⚠️ Responsive design not clearly detected")
                
        except Exception as e:
            self.results['issues'].append(f"❌ Failed to check mobile-friendliness: {e}")
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "=" * 70)
        print("📊 VALIDATION REPORT SUMMARY")
        print("=" * 70)
        
        print(f"\n🎯 SEO Score: {self.results['seo_score']}%")
        
        if self.results['adsense_compliance']:
            print("✅ Google AdSense Compliance: PASSED")
        else:
            print("❌ Google AdSense Compliance: NEEDS ATTENTION")
        
        print(f"\n✅ Passed Checks: {len(self.results['passed'])}")
        print(f"❌ Issues Found: {len(self.results['issues'])}")
        
        if self.results['passed']:
            print("\n" + "=" * 70)
            print("✅ PASSED CHECKS:")
            print("=" * 70)
            for item in self.results['passed']:
                print(f"  {item}")
        
        if self.results['issues']:
            print("\n" + "=" * 70)
            print("❌ ISSUES & WARNINGS:")
            print("=" * 70)
            for item in self.results['issues']:
                print(f"  {item}")
        
        # AdSense specific recommendations
        if not self.results['adsense_compliance']:
            print("\n" + "=" * 70)
            print("📋 ADSENSE COMPLIANCE RECOMMENDATIONS:")
            print("=" * 70)
            print("  1. Ensure all required pages exist: Privacy Policy, Contact, About")
            print("  2. Add minimum 300 words of original content per page")
            print("  3. Include clear navigation menu")
            print("  4. Provide contact information")
            print("  5. Ensure mobile-responsive design")
            print("  6. Add all images alt text")
        
        print("\n" + "=" * 70)
        print(f"Report completed at: {self.results['timestamp']}")
        print("=" * 70)
    
    def run_full_validation(self):
        """Run all validation checks"""
        print("\n🚀 Starting Comprehensive SEO & AdSense Validation")
        print("=" * 70)
        
        self.check_homepage()
        self.check_essential_pages()
        self.check_robots_txt()
        self.check_mobile_friendly()
        self.print_report()
        
        return self.results

def main():
    validator = QuickSEOValidator()
    results = validator.run_full_validation()
    
    # Exit code based on compliance
    exit(0 if results['adsense_compliance'] else 1)

if __name__ == "__main__":
    main()
