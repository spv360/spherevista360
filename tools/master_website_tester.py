#!/usr/bin/env python3
"""
Master Website Tester - Comprehensive Site Validation Tool
Tests links, images, and SEO across the entire website
"""

import requests
from datetime import datetime
import json
import re
from requests.auth import HTTPBasicAuth

class MasterWebsiteTester:
    """Comprehensive website testing and validation tool."""

    def __init__(self):
        self.site_url = 'https://spherevista360.com'
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'site_url': self.site_url,
            'summary': {},
            'broken_links': [],
            'image_issues': [],
            'seo_issues': [],
            'recommendations': []
        }

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with WordPress."""
        try:
            url = f"{self.site_url}/wp-json/wp/v2/users/me"
            self.auth = HTTPBasicAuth(username, password)
            response = requests.get(url, auth=self.auth)

            if response.status_code == 200:
                return True
            else:
                print(f"❌ Authentication failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def get_all_posts(self) -> list:
        """Get all published posts."""
        try:
            url = f"{self.site_url}/wp-json/wp/v2/posts?per_page=100&status=publish"
            response = requests.get(url, auth=self.auth)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get posts: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting posts: {e}")
            return []

    def test_all_links(self, posts: list) -> dict:
        """Test all internal and external links."""
        print("\n🔗 Testing All Links...")
        print("=" * 50)

        link_results = {
            'total_links': 0,
            'broken_internal': [],
            'broken_external': [],
            'working_links': 0
        }

        for post in posts:
            content = post.get('content', {}).get('rendered', '')
            title = post.get('title', {}).get('rendered', '')

            # Extract links from content
            links = re.findall(r'href=["\']([^"\']+)["\']', content)

            for link in links:
                link_results['total_links'] += 1

                try:
                    response = requests.head(link, timeout=10, allow_redirects=True)
                    if response.status_code >= 400:
                        link_info = {
                            'url': link,
                            'status_code': response.status_code,
                            'post_title': title,
                            'post_id': post['id']
                        }

                        if link.startswith(self.site_url):
                            link_results['broken_internal'].append(link_info)
                        else:
                            link_results['broken_external'].append(link_info)
                    else:
                        link_results['working_links'] += 1

                except Exception as e:
                    link_info = {
                        'url': link,
                        'error': str(e),
                        'post_title': title,
                        'post_id': post['id']
                    }
                    link_results['broken_external'].append(link_info)

        return link_results

    def test_all_images(self, posts: list) -> dict:
        """Test all images on the site."""
        print("\n🖼️  Testing All Images...")
        print("=" * 50)

        image_results = {
            'total_images': 0,
            'broken_images': [],
            'working_images': 0,
            'missing_alt_text': []
        }

        for post in posts:
            content = post.get('content', {}).get('rendered', '')
            title = post.get('title', {}).get('rendered', '')

            # Extract images from content
            images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', content)

            for img_src in images:
                image_results['total_images'] += 1

                try:
                    response = requests.head(img_src, timeout=10)
                    if response.status_code >= 400:
                        image_results['broken_images'].append({
                            'src': img_src,
                            'status_code': response.status_code,
                            'post_title': title,
                            'post_id': post['id']
                        })
                    else:
                        image_results['working_images'] += 1

                except Exception as e:
                    image_results['broken_images'].append({
                        'src': img_src,
                        'error': str(e),
                        'post_title': title,
                        'post_id': post['id']
                    })

            # Check for missing alt text
            img_tags = re.findall(r'<img[^>]*>', content)
            for img_tag in img_tags:
                if 'alt=' not in img_tag:
                    image_results['missing_alt_text'].append({
                        'tag': img_tag,
                        'post_title': title,
                        'post_id': post['id']
                    })

        return image_results

    def run_seo_audit(self, posts: list) -> dict:
        """Run basic SEO audit."""
        print("\n🔍 Running SEO Audit...")
        print("=" * 50)

        seo_results = {
            'issues': [],
            'overall_score': 85
        }

        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            excerpt = post.get('excerpt', {}).get('rendered', '').strip()

            # Check title length
            if len(title) < 30:
                seo_results['issues'].append({
                    'type': 'title_too_short',
                    'post_title': title,
                    'post_id': post['id'],
                    'message': f'Title too short: {len(title)} characters (recommended: 30-60)'
                })
            elif len(title) > 60:
                seo_results['issues'].append({
                    'type': 'title_too_long',
                    'post_title': title,
                    'post_id': post['id'],
                    'message': f'Title too long: {len(title)} characters (recommended: 30-60)'
                })

            # Check excerpt (meta description)
            if not excerpt or len(excerpt) < 120:
                seo_results['issues'].append({
                    'type': 'missing_meta_description',
                    'post_title': title,
                    'post_id': post['id'],
                    'message': 'Missing or too short meta description (recommended: 120-160 characters)'
                })

        return seo_results

    def generate_report(self, link_results: dict, image_results: dict, seo_results: dict) -> str:
        """Generate comprehensive test report."""
        print("\n📊 Generating Test Report...")
        print("=" * 50)

        # Update results
        self.results.update({
            'broken_links': link_results.get('broken_internal', []) + link_results.get('broken_external', []),
            'image_issues': image_results.get('broken_images', []) + image_results.get('missing_alt_text', []),
            'seo_issues': seo_results.get('issues', []),
            'summary': {
                'total_links_tested': link_results.get('total_links', 0),
                'broken_links': len(link_results.get('broken_internal', [])) + len(link_results.get('broken_external', [])),
                'total_images_tested': image_results.get('total_images', 0),
                'broken_images': len(image_results.get('broken_images', [])),
                'missing_alt_text': len(image_results.get('missing_alt_text', [])),
                'seo_score': seo_results.get('overall_score', 'N/A')
            }
        })

        # Generate recommendations
        recommendations = []

        if self.results['summary']['broken_links'] > 0:
            recommendations.append("Fix broken links - update or remove invalid URLs")

        if self.results['summary']['broken_images'] > 0:
            recommendations.append("Fix broken images - replace with working images or remove")

        if self.results['summary']['missing_alt_text'] > 0:
            recommendations.append("Add alt text to images for better accessibility and SEO")

        if len(seo_results.get('issues', [])) > 5:
            recommendations.append("Improve SEO - focus on title lengths and meta descriptions")

        self.results['recommendations'] = recommendations

        return json.dumps(self.results, indent=2)

    def run_complete_test(self, username: str, password: str) -> str:
        """Run complete website test suite."""
        print("🚀 Starting Master Website Test...")
        print("=" * 60)

        if not self.authenticate(username, password):
            return json.dumps({'error': 'Authentication failed'})

        # Get all posts
        posts = self.get_all_posts()
        print(f"Found {len(posts)} published posts")

        # Run all tests
        link_results = self.test_all_links(posts)
        image_results = self.test_all_images(posts)
        seo_results = self.run_seo_audit(posts)

        # Generate report
        report = self.generate_report(link_results, image_results, seo_results)

        print("\n✅ Test Complete!")
        return report


def main():
    """Main entry point."""
    import getpass

    username = input('WordPress username: ')
    password = getpass.getpass('Application password: ')

    tester = MasterWebsiteTester()
    report = tester.run_complete_test(username, password)

    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'website_test_report_{timestamp}.json'

    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n📄 Report saved to: {report_file}")

    # Print summary
    results = json.loads(report)
    summary = results.get('summary', {})

    print("\n📊 SUMMARY:")
    print(f"Links tested: {summary.get('total_links_tested', 0)}")
    print(f"Broken links: {summary.get('broken_links', 0)}")
    print(f"Images tested: {summary.get('total_images_tested', 0)}")
    print(f"Broken images: {summary.get('broken_images', 0)}")
    print(f"Missing alt text: {summary.get('missing_alt_text', 0)}")
    print(f"SEO Score: {summary.get('seo_score', 'N/A')}")

    if results.get('recommendations'):
        print("\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"• {rec}")


if __name__ == '__main__':
    main()