#!/usr/bin/env python3
"""
Corrected Validation Test for SphereVista360
===========================================
Test validation tools with actual available methods.
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.validation import (
    TechnicalValidator,
    SEOValidator, 
    PerformanceValidator,
    AccessibilityValidator,
    LinkValidator,
    ImageValidator,
    ComprehensiveValidator
)
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def setup_wordpress_client():
    """Set up WordPress client with proper authentication."""
    print_info("🔧 Setting up WordPress client...")
    
    try:
        wp = WordPressClient()
        wp.authenticate()
        
        # Test connection
        posts = wp.get_posts(per_page=3)
        
        print_success(f"✅ WordPress connected successfully")
        print_info(f"   Test posts found: {len(posts)}")
        
        return wp, posts
        
    except Exception as e:
        print_error(f"❌ WordPress setup failed: {str(e)}")
        return None, None


def test_seo_validation(wp, posts):
    """Test SEO validation with actual methods."""
    print_info("\n🎯 Testing SEO Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for SEO testing")
        return None
    
    try:
        validator = SEOValidator(wp)
        post_id = posts[0]['id']
        
        # Test individual post SEO validation
        result = validator.validate_post(post_id)
        
        print_success("✅ SEO validation completed")
        print_info(f"   Post ID: {post_id}")
        print_info(f"   Post Title: {posts[0].get('title', {}).get('rendered', 'Untitled')}")
        print_info(f"   Overall SEO Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display key findings
        if 'title_validation' in result:
            title_score = result['title_validation'].get('score', 0)
            print_info(f"   Title validation score: {title_score}/100")
        
        if 'meta_description' in result:
            meta_score = result['meta_description'].get('score', 0)
            print_info(f"   Meta description score: {meta_score}/100")
        
        if 'content_analysis' in result:
            content_score = result['content_analysis'].get('score', 0)
            print_info(f"   Content analysis score: {content_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ SEO validation failed: {str(e)}")
        return None


def test_technical_validation(wp, posts):
    """Test technical validation."""
    print_info("\n🔧 Testing Technical Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for technical testing")
        return None
    
    try:
        validator = TechnicalValidator(wp)
        post_id = posts[0]['id']
        
        # Test sitemap inclusion
        sitemap_result = validator.validate_sitemap_inclusion(post_id)
        
        # Test robots.txt
        robots_result = validator.validate_robots_txt()
        
        # Test duplicate content
        duplicate_result = validator.check_duplicate_content(post_id)
        
        print_success("✅ Technical validation completed")
        print_info(f"   Post ID: {post_id}")
        
        # Display findings
        if 'in_sitemap' in sitemap_result:
            sitemap_status = sitemap_result['in_sitemap']
            print_info(f"   Sitemap inclusion: {'✅ Found' if sitemap_status else '❌ Not found'}")
        
        if 'score' in robots_result:
            robots_score = robots_result['score']
            print_info(f"   Robots.txt score: {robots_score}/100")
        
        if 'is_duplicate' in duplicate_result:
            is_duplicate = duplicate_result['is_duplicate']
            print_info(f"   Duplicate content: {'❌ Found' if is_duplicate else '✅ Unique'}")
        
        # Combine results
        result = {
            'sitemap_validation': sitemap_result,
            'robots_validation': robots_result,
            'duplicate_content': duplicate_result,
            'overall_score': robots_result.get('score', 50)  # Use robots score as overall
        }
        
        return result
        
    except Exception as e:
        print_error(f"❌ Technical validation failed: {str(e)}")
        return None


def test_performance_validation(wp, posts):
    """Test performance validation."""
    print_info("\n⚡ Testing Performance Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for performance testing")
        return None
    
    try:
        validator = PerformanceValidator(wp)
        post_id = posts[0]['id']
        
        # Test page speed
        result = validator.validate_page_speed(post_id)
        
        print_success("✅ Performance validation completed")
        print_info(f"   Post ID: {post_id}")
        print_info(f"   Overall Performance Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display performance metrics
        if 'loading_time' in result:
            load_time = result['loading_time']
            print_info(f"   Loading time: {load_time}s")
        
        if 'resource_analysis' in result:
            resource_data = result['resource_analysis']
            total_resources = resource_data.get('total_resources', 0)
            print_info(f"   Total resources: {total_resources}")
        
        if 'optimization_suggestions' in result:
            suggestions = result['optimization_suggestions']
            print_info(f"   Optimization suggestions: {len(suggestions)}")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Performance validation failed: {str(e)}")
        return None


def test_accessibility_validation(wp, posts):
    """Test accessibility validation."""
    print_info("\n♿ Testing Accessibility Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for accessibility testing")
        return None
    
    try:
        validator = AccessibilityValidator(wp)
        post_id = posts[0]['id']
        
        # Test post accessibility
        result = validator.validate_post_accessibility(post_id)
        
        print_success("✅ Accessibility validation completed")
        print_info(f"   Post ID: {post_id}")
        print_info(f"   Overall Accessibility Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display accessibility metrics
        if 'color_contrast' in result:
            contrast_score = result['color_contrast'].get('score', 0)
            print_info(f"   Color contrast score: {contrast_score}/100")
        
        if 'alt_text_analysis' in result:
            alt_score = result['alt_text_analysis'].get('score', 0)
            print_info(f"   Alt text score: {alt_score}/100")
        
        if 'heading_structure' in result:
            heading_score = result['heading_structure'].get('score', 0)
            print_info(f"   Heading structure score: {heading_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Accessibility validation failed: {str(e)}")
        return None


def test_link_validation(wp, posts):
    """Test link validation."""
    print_info("\n🔗 Testing Link Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for link testing")
        return None
    
    try:
        validator = LinkValidator(wp)
        post_id = posts[0]['id']
        
        # Test post links
        result = validator.validate_post_links(post_id)
        
        print_success("✅ Link validation completed")
        print_info(f"   Post ID: {post_id}")
        print_info(f"   Overall Link Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display link metrics
        if 'internal_links' in result:
            internal_data = result['internal_links']
            internal_count = len(internal_data.get('links', []))
            internal_broken = len(internal_data.get('broken_links', []))
            print_info(f"   Internal links: {internal_count} total, {internal_broken} broken")
        
        if 'external_links' in result:
            external_data = result['external_links']
            external_count = len(external_data.get('links', []))
            external_broken = len(external_data.get('broken_links', []))
            print_info(f"   External links: {external_count} total, {external_broken} broken")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Link validation failed: {str(e)}")
        return None


def test_image_validation(wp, posts):
    """Test image validation."""
    print_info("\n🖼️  Testing Image Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for image testing")
        return None
    
    try:
        validator = ImageValidator(wp)
        post_id = posts[0]['id']
        
        # Test post images
        result = validator.validate_post_images(post_id)
        
        print_success("✅ Image validation completed")
        print_info(f"   Post ID: {post_id}")
        print_info(f"   Overall Image Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display image metrics
        if 'image_analysis' in result:
            image_data = result['image_analysis']
            total_images = image_data.get('total_images', 0)
            optimized_images = image_data.get('optimized_images', 0)
            print_info(f"   Total images: {total_images}")
            print_info(f"   Optimized images: {optimized_images}")
        
        if 'accessibility_analysis' in result:
            a11y_data = result['accessibility_analysis']
            images_with_alt = a11y_data.get('images_with_alt', 0)
            print_info(f"   Images with alt text: {images_with_alt}")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Image validation failed: {str(e)}")
        return None


def test_comprehensive_validation(wp, posts):
    """Test comprehensive validation."""
    print_info("\n🎯 Testing Comprehensive Validation...")
    
    if not posts:
        print_warning("⚠️  No posts available for comprehensive testing")
        return None
    
    try:
        validator = ComprehensiveValidator(wp)
        post_id = posts[0]['id']
        
        # Test comprehensive post validation
        result = validator.validate_post_comprehensive(post_id)
        
        print_success("✅ Comprehensive validation completed")
        print_info(f"   Post ID: {post_id}")
        print_info(f"   Overall Comprehensive Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display comprehensive metrics
        if 'validation_results' in result:
            validations = result['validation_results']
            print_info(f"   Validation categories completed: {len(validations)}")
        
        if 'issues' in result:
            issues = result['issues']
            print_info(f"   Total issues found: {len(issues)}")
        
        if 'recommendations' in result:
            recommendations = result['recommendations']
            print_info(f"   Recommendations: {len(recommendations)}")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Comprehensive validation failed: {str(e)}")
        return None


def generate_summary_report(results, posts):
    """Generate summary report of all tests."""
    print_info("\n📊 VALIDATION TEST SUMMARY")
    print_info("=" * 50)
    
    if posts:
        test_post = posts[0]
        print_info(f"Test Post: {test_post.get('title', {}).get('rendered', 'Untitled')}")
        print_info(f"Post ID: {test_post['id']}")
        print_info(f"Post URL: {test_post.get('link', 'N/A')}")
        print_info("-" * 50)
    
    successful_tests = 0
    total_tests = len(results)
    scores = []
    
    for test_name, result in results.items():
        if result:
            successful_tests += 1
            score = result.get('overall_score', 0)
            if score and score > 0:
                scores.append(score)
            
            status = "✅ PASSED"
            if score:
                if score >= 80:
                    quality = "EXCELLENT"
                elif score >= 60:
                    quality = "GOOD"
                elif score >= 40:
                    quality = "FAIR"
                else:
                    quality = "NEEDS WORK"
                status += f" - {score}/100 ({quality})"
        else:
            status = "❌ FAILED"
        
        print_info(f"{test_name.upper():20} {status}")
    
    print_info("-" * 50)
    print_info(f"Tests Completed: {successful_tests}/{total_tests}")
    
    if scores:
        avg_score = sum(scores) / len(scores)
        print_info(f"Average Score: {avg_score:.1f}/100")
        
        if avg_score >= 80:
            print_success("🎉 EXCELLENT! Your site is performing very well!")
        elif avg_score >= 60:
            print_warning("👍 GOOD! Your site is performing well with some areas for improvement")
        elif avg_score >= 40:
            print_warning("⚠️  FAIR! Your site needs optimization in several areas")
        else:
            print_error("🚨 NEEDS WORK! Your site requires significant improvements")
    
    print_info("=" * 50)
    
    # Save detailed results
    report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump({
            'test_date': datetime.now().isoformat(),
            'site_url': 'https://spherevista360.com',
            'test_post': posts[0] if posts else None,
            'results': results,
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'average_score': sum(scores) / len(scores) if scores else 0
            }
        }, f, indent=2)
    
    print_success(f"📄 Detailed report saved: {report_file}")


def main():
    """Main test execution."""
    print_info("🚀 Validation Test for SphereVista360")
    print_info("=" * 40)
    
    start_time = time.time()
    
    # Setup WordPress connection
    wp, posts = setup_wordpress_client()
    
    if not wp:
        print_error("❌ Cannot proceed without WordPress connection")
        return False
    
    if not posts:
        print_warning("⚠️  No posts found, some tests may be limited")
    else:
        print_info(f"\n🎯 Testing with {len(posts)} available posts")
    
    # Run validation tests
    results = {}
    
    results['seo'] = test_seo_validation(wp, posts)
    results['technical'] = test_technical_validation(wp, posts)
    results['performance'] = test_performance_validation(wp, posts)
    results['accessibility'] = test_accessibility_validation(wp, posts)
    results['links'] = test_link_validation(wp, posts)
    results['images'] = test_image_validation(wp, posts)
    results['comprehensive'] = test_comprehensive_validation(wp, posts)
    
    # Generate summary
    generate_summary_report(results, posts)
    
    execution_time = time.time() - start_time
    print_info(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
    
    print_success("🎉 Validation testing completed!")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)