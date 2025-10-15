#!/usr/bin/env python3
"""
Comprehensive Website Testing Tool
=================================
Test the complete website for broken links, images, and SEO optimization needs.
"""

import sys
import os
from pathlib import Path

# Add the master toolkit to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from master_toolkit.core import create_client, WordPressAPIError
    from master_toolkit.validation import ComprehensiveValidator, LinkValidator, ImageValidator, SEOValidator
    from master_toolkit.utils import print_header, print_success, print_error, print_section, ResultFormatter
except ImportError as e:
    print(f"Error importing toolkit: {e}")
    sys.exit(1)


class WebsiteTester:
    """Comprehensive website testing utility."""
    
    def __init__(self):
        """Initialize the tester."""
        self.client = None
        self.link_validator = None
        self.image_validator = None
        self.seo_validator = None
        self.comprehensive_validator = None
    
    def authenticate(self, username=None, password=None):
        """Authenticate with WordPress."""
        try:
            self.client = create_client()
            
            if username and password:
                success = self.client.authenticate(username, password)
            else:
                success = self.client.authenticate()
            
            if success:
                # Initialize validators
                self.link_validator = LinkValidator(self.client)
                self.image_validator = ImageValidator(self.client)
                self.seo_validator = SEOValidator(self.client)
                self.comprehensive_validator = ComprehensiveValidator(self.client)
                return True
            return False
            
        except Exception as e:
            print_error(f"Authentication failed: {e}")
            return False
    
    def test_all_posts(self, limit=50):
        """Test all posts for issues."""
        print_header("COMPREHENSIVE WEBSITE TESTING")
        
        if not self.client:
            print_error("Not authenticated. Please authenticate first.")
            return
        
        try:
            # Get all posts
            posts = self.client.get_posts(per_page=limit)
            total_posts = len(posts)
            
            print(f"📊 Testing {total_posts} posts...")
            
            # Run comprehensive validation
            validation_results = self.comprehensive_validator.validate_multiple_posts(per_page=limit)
            
            # Detailed breakdown
            self._print_test_results(validation_results)
            
            return validation_results
            
        except Exception as e:
            print_error(f"Testing failed: {e}")
            return None
    
    def test_broken_links(self):
        """Test for broken links across the site."""
        print_header("BROKEN LINKS TESTING")
        
        if not self.link_validator:
            print_error("Link validator not initialized")
            return
        
        try:
            # Known problematic posts
            post_ids = [1833, 1832, 1831, 1838, 1829, 1828]
            
            print("🔗 Checking known problematic posts...")
            
            all_broken_links = []
            posts_with_issues = []
            
            for post_id in post_ids:
                try:
                    result = self.link_validator.validate_post_links(post_id)
                    if 'broken_links' in result and result['broken_links']:
                        posts_with_issues.append({
                            'post_id': post_id,
                            'title': result.get('post_title', 'Unknown'),
                            'broken_links': result['broken_links']
                        })
                        all_broken_links.extend(result['broken_links'])
                        print_error(f"Post {post_id}: {len(result['broken_links'])} broken links")
                    else:
                        print_success(f"Post {post_id}: No broken links")
                except Exception as e:
                    print_error(f"Error checking post {post_id}: {e}")
            
            # Summary
            print_section("Broken Links Summary")
            print(f"📊 Posts checked: {len(post_ids)}")
            print(f"❌ Posts with broken links: {len(posts_with_issues)}")
            print(f"🔗 Total broken links: {len(all_broken_links)}")
            
            if all_broken_links:
                print("\n🔍 Unique broken links found:")
                for link in set(all_broken_links):
                    print(f"  • {link}")
            
            return {
                'posts_checked': len(post_ids),
                'posts_with_issues': len(posts_with_issues),
                'total_broken_links': len(all_broken_links),
                'broken_links': list(set(all_broken_links)),
                'posts_details': posts_with_issues
            }
            
        except Exception as e:
            print_error(f"Link testing failed: {e}")
            return None
    
    def test_images(self):
        """Test images across the site."""
        print_header("IMAGE TESTING")
        
        if not self.image_validator:
            print_error("Image validator not initialized")
            return
        
        try:
            # Get recent posts to test images
            posts = self.client.get_posts(per_page=20)
            
            total_images = 0
            broken_images = 0
            missing_alt = 0
            posts_with_image_issues = []
            
            for post in posts:
                post_id = post['id']
                try:
                    result = self.image_validator.validate_post_images(post_id)
                    
                    if 'total_images' in result:
                        total_images += result['total_images']
                        broken_images += result.get('broken_images', 0)
                        missing_alt += result.get('images_without_alt', 0)
                        
                        if result.get('broken_images', 0) > 0 or result.get('images_without_alt', 0) > 0:
                            posts_with_image_issues.append({
                                'post_id': post_id,
                                'title': result.get('post_title', 'Unknown'),
                                'broken_images': result.get('broken_images', 0),
                                'missing_alt': result.get('images_without_alt', 0)
                            })
                            
                except Exception as e:
                    print_error(f"Error checking images in post {post_id}: {e}")
            
            # Summary
            print_section("Image Testing Summary")
            print(f"📊 Posts checked: {len(posts)}")
            print(f"🖼️ Total images: {total_images}")
            print(f"❌ Broken images: {broken_images}")
            print(f"📝 Missing alt text: {missing_alt}")
            print(f"⚠️ Posts with issues: {len(posts_with_image_issues)}")
            
            if total_images > 0:
                success_rate = ((total_images - broken_images) / total_images) * 100
                print(f"✅ Image success rate: {success_rate:.1f}%")
            
            return {
                'posts_checked': len(posts),
                'total_images': total_images,
                'broken_images': broken_images,
                'missing_alt': missing_alt,
                'posts_with_issues': len(posts_with_image_issues),
                'issue_details': posts_with_image_issues
            }
            
        except Exception as e:
            print_error(f"Image testing failed: {e}")
            return None
    
    def test_seo(self):
        """Test SEO across the site."""
        print_header("SEO TESTING")
        
        if not self.seo_validator:
            print_error("SEO validator not initialized")
            return
        
        try:
            # Test recent posts
            posts = self.client.get_posts(per_page=20)
            
            seo_results = self.seo_validator.scan_posts_seo([post['id'] for post in posts])
            
            # Summary
            print_section("SEO Testing Summary")
            print(f"📊 Posts scanned: {seo_results['posts_scanned']}")
            print(f"📈 Average SEO score: {seo_results['average_score']:.1f}%")
            print(f"⚠️ Posts with issues: {seo_results['posts_with_issues']}")
            print(f"🔧 Total issues: {seo_results['total_issues']}")
            
            # Grade distribution
            grades = {}
            for result in seo_results.get('post_results', []):
                grade = result.get('grade', 'F')
                grades[grade] = grades.get(grade, 0) + 1
            
            if grades:
                print("\n📊 SEO Grade Distribution:")
                for grade in ['A', 'B', 'C', 'D', 'F']:
                    count = grades.get(grade, 0)
                    if count > 0:
                        print(f"  {grade}: {count} posts")
            
            return seo_results
            
        except Exception as e:
            print_error(f"SEO testing failed: {e}")
            return None
    
    def fix_all_issues(self, dry_run=False):
        """Fix all detected issues."""
        print_header("FIXING ALL DETECTED ISSUES")
        
        if not self.comprehensive_validator:
            print_error("Comprehensive validator not initialized")
            return
        
        try:
            mode = "DRY RUN" if dry_run else "LIVE FIXING"
            print(f"🔧 Mode: {mode}")
            
            # Run comprehensive fix
            fix_results = self.comprehensive_validator.fix_all_issues(dry_run=dry_run)
            
            print_section("Fix Results")
            print(f"📊 Posts processed: {fix_results.get('total_posts', 0)}")
            print(f"✅ Posts fixed: {fix_results.get('posts_fixed', 0)}")
            print(f"❌ Posts failed: {fix_results.get('posts_failed', 0)}")
            print(f"🔧 Total fixes applied: {fix_results.get('total_fixes', 0)}")
            
            return fix_results
            
        except Exception as e:
            print_error(f"Fixing failed: {e}")
            return None
    
    def generate_full_report(self):
        """Generate a comprehensive website health report."""
        print_header("GENERATING COMPREHENSIVE REPORT")
        
        if not self.comprehensive_validator:
            print_error("Comprehensive validator not initialized")
            return
        
        try:
            report = self.comprehensive_validator.generate_quality_report()
            
            # Save report
            report_file = f"website_health_report_{self._get_timestamp()}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            
            print_success(f"Report saved: {report_file}")
            
            # Also show summary
            print_section("Report Summary")
            lines = report.split('\n')
            for line in lines[:20]:  # Show first 20 lines
                print(line)
            
            return report_file
            
        except Exception as e:
            print_error(f"Report generation failed: {e}")
            return None
    
    def _print_test_results(self, results):
        """Print comprehensive test results."""
        if not results or 'error' in results:
            print_error("No valid test results to display")
            return
        
        print_section("Test Results Summary")
        print(f"📊 Posts tested: {results.get('validated_posts', 0)}")
        print(f"📈 Average quality score: {results.get('average_score', 0)}%")
        print(f"⚠️ Posts needing attention: {results.get('posts_needing_attention', 0)}")
        
        # Quality distribution
        if 'validation_results' in results:
            scores = [r['overall_score'] for r in results['validation_results']]
            if scores:
                excellent = len([s for s in scores if s >= 90])
                good = len([s for s in scores if 70 <= s < 90])
                poor = len([s for s in scores if s < 70])
                
                print("\n📊 Quality Distribution:")
                print(f"  🟢 Excellent (90%+): {excellent} posts")
                print(f"  🟡 Good (70-89%): {good} posts")
                print(f"  🔴 Needs work (<70%): {poor} posts")
    
    def _get_timestamp(self):
        """Get timestamp for filenames."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")


def main():
    """Main function."""
    print("🚀 COMPREHENSIVE WEBSITE TESTING")
    print("=" * 60)
    
    tester = WebsiteTester()
    
    # Try to authenticate
    print("🔐 Authenticating...")
    if not tester.authenticate():
        print_error("Authentication failed. Exiting.")
        return 1
    
    print_success("Authentication successful!")
    
    # Run all tests
    try:
        # Test 1: Comprehensive validation
        print("\n" + "="*60)
        comprehensive_results = tester.test_all_posts(limit=30)
        
        # Test 2: Broken links
        print("\n" + "="*60)
        link_results = tester.test_broken_links()
        
        # Test 3: Images
        print("\n" + "="*60)
        image_results = tester.test_images()
        
        # Test 4: SEO
        print("\n" + "="*60)
        seo_results = tester.test_seo()
        
        # Generate report
        print("\n" + "="*60)
        report_file = tester.generate_full_report()
        
        # Ask about fixing
        print("\n" + "="*60)
        print("🔧 AUTOMATIC FIXING AVAILABLE")
        print("Would you like to automatically fix detected issues?")
        print("1. Dry run (preview fixes)")
        print("2. Apply fixes")
        print("3. Skip fixing")
        
        # For now, let's do a dry run
        print("Running dry run to preview fixes...")
        fix_results = tester.fix_all_issues(dry_run=True)
        
        # Final summary
        print_header("FINAL TESTING SUMMARY")
        print("✅ Comprehensive website testing completed!")
        
        if comprehensive_results:
            print(f"📊 Overall quality score: {comprehensive_results.get('average_score', 0)}%")
        
        if link_results:
            print(f"🔗 Broken links found: {link_results.get('total_broken_links', 0)}")
        
        if image_results:
            print(f"🖼️ Image issues: {image_results.get('broken_images', 0)} broken, {image_results.get('missing_alt', 0)} missing alt")
        
        if seo_results:
            print(f"📈 SEO average: {seo_results.get('average_score', 0)}%")
        
        if fix_results:
            print(f"🔧 Fixes available: {fix_results.get('total_fixes', 0)}")
        
        if report_file:
            print(f"📄 Detailed report: {report_file}")
        
        return 0
        
    except Exception as e:
        print_error(f"Testing failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())