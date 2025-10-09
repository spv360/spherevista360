#!/usr/bin/env python3
"""
Website Health Checker (No Auth Required)
=========================================
Check website health without requiring WordPress authentication.
"""

import requests
import re
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Any


class WebsiteHealthChecker:
    """Website health checker that doesn't require WordPress auth."""
    
    def __init__(self, base_url="https://spherevista360.com"):
        """Initialize the health checker."""
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (WebsiteHealthChecker/1.0)'
        })
        
        # Known broken links from previous analysis
        self.known_broken_links = {
            'https://spherevista360.com/product-analytics-2025/': 
                'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/',
            'https://spherevista360.com/on-device-vs-cloud-ai-2025/': 
                'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/',
            'https://spherevista360.com/tech-innovation-2025/':
                'https://spherevista360.com/tech-innovations-that-will-transform-2025/',
            'https://spherevista360.com/data-privacy-future/':
                'https://spherevista360.com/the-future-of-data-privacy-new-laws-and-technologies/',
            'https://spherevista360.com/cloud-computing-evolution/':
                'https://spherevista360.com/cloud-computing-evolution-trends-and-predictions/'
        }
    
    def check_url_status(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Check the status of a URL."""
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            return {
                'url': url,
                'status_code': response.status_code,
                'accessible': response.status_code < 400,
                'final_url': response.url,
                'redirected': response.url != url,
                'error': None
            }
        except requests.RequestException as e:
            return {
                'url': url,
                'status_code': None,
                'accessible': False,
                'final_url': None,
                'redirected': False,
                'error': str(e)
            }
    
    def check_known_broken_links(self) -> Dict[str, Any]:
        """Check the status of known broken links."""
        print("🔗 CHECKING KNOWN BROKEN LINKS")
        print("=" * 50)
        
        results = {
            'broken_links_checked': len(self.known_broken_links),
            'still_broken': [],
            'now_working': [],
            'correct_links_status': []
        }
        
        for broken_url, correct_url in self.known_broken_links.items():
            print(f"\n🔍 Checking: {broken_url}")
            
            # Check broken link
            broken_status = self.check_url_status(broken_url)
            print(f"  Status: {broken_status['status_code']} ({'✅' if broken_status['accessible'] else '❌'})")
            
            if not broken_status['accessible']:
                results['still_broken'].append(broken_url)
            else:
                results['now_working'].append(broken_url)
            
            # Check correct link
            print(f"🎯 Checking correct: {correct_url}")
            correct_status = self.check_url_status(correct_url)
            print(f"  Status: {correct_status['status_code']} ({'✅' if correct_status['accessible'] else '❌'})")
            
            results['correct_links_status'].append({
                'broken_url': broken_url,
                'correct_url': correct_url,
                'broken_accessible': broken_status['accessible'],
                'correct_accessible': correct_status['accessible']
            })
            
            time.sleep(1)  # Be nice to the server
        
        return results
    
    def check_homepage_health(self) -> Dict[str, Any]:
        """Check homepage health and extract links."""
        print("\n🏠 CHECKING HOMEPAGE HEALTH")
        print("=" * 50)
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            
            results = {
                'homepage_accessible': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content),
                'internal_links': [],
                'external_links': [],
                'images': []
            }
            
            if response.status_code == 200:
                print(f"✅ Homepage accessible ({response.status_code})")
                print(f"⏱️ Response time: {results['response_time']:.2f}s")
                print(f"📄 Content length: {results['content_length']} bytes")
                
                # Extract links and images
                content = response.text
                
                # Find internal links
                internal_pattern = rf'href=["\']({re.escape(self.base_url)}[^"\']*)["\']'
                internal_links = re.findall(internal_pattern, content)
                results['internal_links'] = list(set(internal_links))
                
                # Find external links  
                external_pattern = r'href=["\'](?:https?://(?!spherevista360\.com)[^"\']*)["\']'
                external_links = re.findall(external_pattern, content)
                results['external_links'] = list(set(external_links))
                
                # Find images
                img_pattern = r'<img[^>]*src=["\']([^"\']*)["\']'
                images = re.findall(img_pattern, content)
                results['images'] = list(set(images))
                
                print(f"🔗 Internal links found: {len(results['internal_links'])}")
                print(f"🌐 External links found: {len(results['external_links'])}")
                print(f"🖼️ Images found: {len(results['images'])}")
                
            else:
                print(f"❌ Homepage not accessible ({response.status_code})")
            
            return results
            
        except Exception as e:
            print(f"❌ Error checking homepage: {e}")
            return {
                'homepage_accessible': False,
                'error': str(e)
            }
    
    def check_sample_internal_links(self, homepage_results: Dict[str, Any], sample_size: int = 10) -> Dict[str, Any]:
        """Check a sample of internal links."""
        print(f"\n🔗 CHECKING SAMPLE INTERNAL LINKS")
        print("=" * 50)
        
        if 'internal_links' not in homepage_results:
            print("❌ No internal links data available")
            return {}
        
        internal_links = homepage_results['internal_links'][:sample_size]
        
        results = {
            'links_checked': len(internal_links),
            'accessible': 0,
            'broken': 0,
            'results': []
        }
        
        for link in internal_links:
            print(f"🔍 Checking: {link}")
            status = self.check_url_status(link)
            
            if status['accessible']:
                results['accessible'] += 1
                print(f"  ✅ {status['status_code']}")
            else:
                results['broken'] += 1
                print(f"  ❌ {status['status_code']} - {status.get('error', 'Not accessible')}")
            
            results['results'].append(status)
            time.sleep(1)  # Be nice to the server
        
        success_rate = (results['accessible'] / results['links_checked']) * 100 if results['links_checked'] > 0 else 0
        print(f"\n📊 Link Health: {results['accessible']}/{results['links_checked']} working ({success_rate:.1f}%)")
        
        return results
    
    def check_sample_images(self, homepage_results: Dict[str, Any], sample_size: int = 5) -> Dict[str, Any]:
        """Check a sample of images."""
        print(f"\n🖼️ CHECKING SAMPLE IMAGES")
        print("=" * 50)
        
        if 'images' not in homepage_results:
            print("❌ No images data available")
            return {}
        
        images = homepage_results['images'][:sample_size]
        
        results = {
            'images_checked': len(images),
            'accessible': 0,
            'broken': 0,
            'results': []
        }
        
        for img_src in images:
            # Handle relative URLs
            if img_src.startswith('/'):
                img_url = urljoin(self.base_url, img_src)
            elif img_src.startswith('http'):
                img_url = img_src
            else:
                img_url = urljoin(self.base_url, img_src)
            
            print(f"🔍 Checking: {img_url}")
            status = self.check_url_status(img_url)
            
            if status['accessible']:
                results['accessible'] += 1
                print(f"  ✅ {status['status_code']}")
            else:
                results['broken'] += 1
                print(f"  ❌ {status['status_code']} - {status.get('error', 'Not accessible')}")
            
            results['results'].append(status)
            time.sleep(1)  # Be nice to the server
        
        success_rate = (results['accessible'] / results['images_checked']) * 100 if results['images_checked'] > 0 else 0
        print(f"\n📊 Image Health: {results['accessible']}/{results['images_checked']} working ({success_rate:.1f}%)")
        
        return results
    
    def generate_health_report(self, all_results: Dict[str, Any]) -> str:
        """Generate a comprehensive health report."""
        report = []
        report.append("WEBSITE HEALTH REPORT")
        report.append("=" * 50)
        report.append(f"Website: {self.base_url}")
        report.append(f"Checked on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Homepage health
        if 'homepage' in all_results:
            homepage = all_results['homepage']
            report.append("🏠 HOMEPAGE HEALTH")
            report.append("-" * 30)
            report.append(f"Status: {'✅ Accessible' if homepage.get('homepage_accessible') else '❌ Not accessible'}")
            if homepage.get('status_code'):
                report.append(f"Status Code: {homepage['status_code']}")
            if homepage.get('response_time'):
                report.append(f"Response Time: {homepage['response_time']:.2f}s")
            report.append("")
        
        # Known broken links
        if 'broken_links' in all_results:
            broken = all_results['broken_links']
            report.append("🔗 KNOWN BROKEN LINKS")
            report.append("-" * 30)
            report.append(f"Links checked: {broken.get('broken_links_checked', 0)}")
            report.append(f"Still broken: {len(broken.get('still_broken', []))}")
            report.append(f"Now working: {len(broken.get('now_working', []))}")
            
            if broken.get('still_broken'):
                report.append("\nStill broken:")
                for link in broken['still_broken']:
                    report.append(f"  ❌ {link}")
            
            if broken.get('now_working'):
                report.append("\nNow working:")
                for link in broken['now_working']:
                    report.append(f"  ✅ {link}")
            report.append("")
        
        # Internal links
        if 'internal_links' in all_results:
            links = all_results['internal_links']
            report.append("🔗 INTERNAL LINKS SAMPLE")
            report.append("-" * 30)
            report.append(f"Links checked: {links.get('links_checked', 0)}")
            report.append(f"Accessible: {links.get('accessible', 0)}")
            report.append(f"Broken: {links.get('broken', 0)}")
            if links.get('links_checked', 0) > 0:
                success_rate = (links.get('accessible', 0) / links['links_checked']) * 100
                report.append(f"Success rate: {success_rate:.1f}%")
            report.append("")
        
        # Images
        if 'images' in all_results:
            images = all_results['images']
            report.append("🖼️ IMAGES SAMPLE")
            report.append("-" * 30)
            report.append(f"Images checked: {images.get('images_checked', 0)}")
            report.append(f"Accessible: {images.get('accessible', 0)}")
            report.append(f"Broken: {images.get('broken', 0)}")
            if images.get('images_checked', 0) > 0:
                success_rate = (images.get('accessible', 0) / images['images_checked']) * 100
                report.append(f"Success rate: {success_rate:.1f}%")
            report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 30)
        
        if 'broken_links' in all_results and all_results['broken_links'].get('still_broken'):
            report.append("• Fix remaining broken links using the master_toolkit")
        
        if 'internal_links' in all_results:
            links = all_results['internal_links']
            if links.get('broken', 0) > 0:
                report.append("• Check and fix broken internal links")
        
        if 'images' in all_results:
            images = all_results['images']
            if images.get('broken', 0) > 0:
                report.append("• Check and fix broken images")
        
        report.append("• Run comprehensive test with authentication for full analysis")
        report.append("• Use master_toolkit/cli/validate.py for detailed validation")
        
        return "\n".join(report)


def main():
    """Main function."""
    print("🌐 WEBSITE HEALTH CHECKER (No Auth Required)")
    print("=" * 60)
    print("This tool checks website health without requiring WordPress authentication.")
    print()
    
    checker = WebsiteHealthChecker()
    all_results = {}
    
    try:
        # Check homepage
        homepage_results = checker.check_homepage_health()
        all_results['homepage'] = homepage_results
        
        # Check known broken links
        broken_links_results = checker.check_known_broken_links()
        all_results['broken_links'] = broken_links_results
        
        # Check sample internal links
        if homepage_results.get('homepage_accessible'):
            internal_links_results = checker.check_sample_internal_links(homepage_results)
            all_results['internal_links'] = internal_links_results
            
            # Check sample images
            images_results = checker.check_sample_images(homepage_results)
            all_results['images'] = images_results
        
        # Generate report
        print("\n📄 GENERATING HEALTH REPORT")
        print("=" * 50)
        
        report = checker.generate_health_report(all_results)
        
        # Save report
        report_file = f"website_health_report_{int(time.time())}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✅ Report saved: {report_file}")
        
        # Show summary
        print("\n📊 HEALTH CHECK SUMMARY")
        print("=" * 50)
        
        if homepage_results.get('homepage_accessible'):
            print("✅ Homepage is accessible")
        else:
            print("❌ Homepage has issues")
        
        if 'broken_links' in all_results:
            broken = all_results['broken_links']
            still_broken = len(broken.get('still_broken', []))
            if still_broken == 0:
                print("✅ No known broken links found")
            else:
                print(f"❌ {still_broken} known broken links still exist")
        
        if 'internal_links' in all_results:
            links = all_results['internal_links']
            if links.get('broken', 0) == 0:
                print("✅ Sample internal links are working")
            else:
                print(f"⚠️ {links.get('broken', 0)} sample internal links are broken")
        
        if 'images' in all_results:
            images = all_results['images']
            if images.get('broken', 0) == 0:
                print("✅ Sample images are working")
            else:
                print(f"⚠️ {images.get('broken', 0)} sample images are broken")
        
        print(f"\n📄 Detailed report: {report_file}")
        print("\n🔧 Next Steps:")
        print("1. For comprehensive testing: python3 comprehensive_website_tester.py")
        print("2. To fix issues: python3 master_toolkit/cli/validate.py audit")
        print("3. For content management: python3 master_toolkit/cli/publish.py --help")
        
        return 0
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())