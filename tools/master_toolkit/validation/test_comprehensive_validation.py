#!/usr/bin/env python3
"""
Comprehensive Validation Test for SphereVista360
===============================================
Test all validation tools with the SphereVista360 website to ensure
proper functionality and comprehensive analysis.
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
    SecurityValidator,
    MobileValidator,
    ContentQualityEnhancer,
    ImageValidator,
    LinkValidator,
    ComprehensiveValidator
)
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def test_wordpress_connection():
    """Test WordPress API connection."""
    print_info("🔗 Testing WordPress API Connection...")
    
    try:
        wp = WordPressClient()
        
        # Test basic connection
        posts = wp.get_posts(per_page=1)
        if posts:
            print_success(f"✅ WordPress API connected successfully")
            print_info(f"   Found {len(posts)} test post(s)")
            return wp, posts[0]['id'] if posts else None
        else:
            print_warning("⚠️  WordPress API connected but no posts found")
            return wp, None
            
    except Exception as e:
        print_error(f"❌ WordPress API connection failed: {str(e)}")
        return None, None


def test_technical_validation(wp, post_id=None):
    """Test technical validation capabilities."""
    print_info("\n🔧 Testing Technical Validation...")
    
    try:
        validator = TechnicalValidator(wp)
        
        # Test site-wide technical validation
        result = validator.validate_site_technical()
        
        print_success("✅ Technical validation completed")
        print_info(f"   Overall Score: {result.get('overall_score', 'N/A')}/100")
        print_info(f"   Issues Found: {len(result.get('issues', []))}")
        
        # Display key findings
        if 'html_validation' in result:
            html_score = result['html_validation'].get('score', 0)
            print_info(f"   HTML Validation Score: {html_score}/100")
        
        if 'css_validation' in result:
            css_score = result['css_validation'].get('score', 0)
            print_info(f"   CSS Validation Score: {css_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Technical validation failed: {str(e)}")
        return None


def test_seo_validation(wp, post_id=None):
    """Test SEO validation capabilities."""
    print_info("\n🎯 Testing SEO Validation...")
    
    try:
        validator = SEOValidator(wp)
        
        if post_id:
            # Test post-specific SEO validation
            result = validator.validate_post_seo(post_id)
            print_success("✅ Post SEO validation completed")
            print_info(f"   Post ID: {post_id}")
        else:
            # Test site-wide SEO validation
            result = validator.validate_site_seo()
            print_success("✅ Site SEO validation completed")
        
        print_info(f"   Overall SEO Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display key SEO metrics
        if 'meta_tags' in result:
            meta_score = result['meta_tags'].get('score', 0)
            print_info(f"   Meta Tags Score: {meta_score}/100")
        
        if 'structured_data' in result:
            schema_score = result['structured_data'].get('score', 0)
            print_info(f"   Structured Data Score: {schema_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ SEO validation failed: {str(e)}")
        return None


def test_performance_validation(wp):
    """Test performance validation capabilities."""
    print_info("\n⚡ Testing Performance Validation...")
    
    try:
        validator = PerformanceValidator(wp)
        
        # Test site performance
        result = validator.validate_site_performance()
        
        print_success("✅ Performance validation completed")
        print_info(f"   Performance Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display key performance metrics
        if 'loading_speed' in result:
            speed_score = result['loading_speed'].get('score', 0)
            print_info(f"   Loading Speed Score: {speed_score}/100")
        
        if 'resource_optimization' in result:
            resource_score = result['resource_optimization'].get('score', 0)
            print_info(f"   Resource Optimization Score: {resource_score}/100")
        
        if 'caching' in result:
            cache_score = result['caching'].get('score', 0)
            print_info(f"   Caching Score: {cache_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Performance validation failed: {str(e)}")
        return None


def test_accessibility_validation(wp, post_id=None):
    """Test accessibility validation capabilities."""
    print_info("\n♿ Testing Accessibility Validation...")
    
    try:
        validator = AccessibilityValidator(wp)
        
        if post_id:
            # Test post accessibility
            result = validator.validate_post_accessibility(post_id)
            print_success("✅ Post accessibility validation completed")
        else:
            # Test site accessibility
            result = validator.validate_site_accessibility()
            print_success("✅ Site accessibility validation completed")
        
        print_info(f"   Accessibility Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display WCAG compliance levels
        if 'wcag_compliance' in result:
            wcag_data = result['wcag_compliance']
            print_info(f"   WCAG AA Compliance: {wcag_data.get('aa_compliant', 'Unknown')}")
            print_info(f"   WCAG AAA Compliance: {wcag_data.get('aaa_compliant', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Accessibility validation failed: {str(e)}")
        return None


def test_security_validation(wp):
    """Test security validation capabilities."""
    print_info("\n🔒 Testing Security Validation...")
    
    try:
        validator = SecurityValidator(wp)
        
        # Test site security
        result = validator.validate_site_security()
        
        print_success("✅ Security validation completed")
        print_info(f"   Security Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display security metrics
        if 'ssl_configuration' in result:
            ssl_score = result['ssl_configuration'].get('score', 0)
            print_info(f"   SSL Configuration Score: {ssl_score}/100")
        
        if 'security_headers' in result:
            headers_score = result['security_headers'].get('score', 0)
            print_info(f"   Security Headers Score: {headers_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Security validation failed: {str(e)}")
        return None


def test_mobile_validation(wp):
    """Test mobile validation capabilities."""
    print_info("\n📱 Testing Mobile Validation...")
    
    try:
        validator = MobileValidator(wp)
        
        # Test mobile responsiveness
        result = validator.validate_site_mobile()
        
        print_success("✅ Mobile validation completed")
        print_info(f"   Mobile Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display mobile metrics
        if 'responsive_design' in result:
            responsive_score = result['responsive_design'].get('score', 0)
            print_info(f"   Responsive Design Score: {responsive_score}/100")
        
        if 'mobile_performance' in result:
            mobile_perf_score = result['mobile_performance'].get('score', 0)
            print_info(f"   Mobile Performance Score: {mobile_perf_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Mobile validation failed: {str(e)}")
        return None


def test_content_quality_validation(wp, post_id=None):
    """Test content quality validation capabilities."""
    print_info("\n📝 Testing Content Quality Validation...")
    
    try:
        validator = ContentQualityEnhancer(wp)
        
        if post_id:
            # Test specific post content quality
            result = validator.enhance_post_content(post_id)
            print_success("✅ Post content quality validation completed")
        else:
            # Test site-wide content quality
            posts = wp.get_posts(per_page=5)
            if posts:
                post_id = posts[0]['id']
                result = validator.enhance_post_content(post_id)
                print_success("✅ Sample post content quality validation completed")
            else:
                print_warning("⚠️  No posts available for content quality testing")
                return None
        
        print_info(f"   Content Quality Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display content metrics
        if 'readability' in result:
            readability_score = result['readability'].get('score', 0)
            print_info(f"   Readability Score: {readability_score}/100")
        
        if 'seo_content' in result:
            seo_content_score = result['seo_content'].get('score', 0)
            print_info(f"   SEO Content Score: {seo_content_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Content quality validation failed: {str(e)}")
        return None


def test_image_validation(wp, post_id=None):
    """Test image validation capabilities."""
    print_info("\n🖼️  Testing Image Validation...")
    
    try:
        validator = ImageValidator(wp)
        
        if post_id:
            # Test post images
            result = validator.validate_post_images(post_id)
            print_success("✅ Post image validation completed")
        else:
            # Test site images
            result = validator.validate_site_images()
            print_success("✅ Site image validation completed")
        
        print_info(f"   Image Quality Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display image metrics
        if 'optimization' in result:
            optimization_score = result['optimization'].get('score', 0)
            print_info(f"   Image Optimization Score: {optimization_score}/100")
        
        if 'accessibility' in result:
            img_a11y_score = result['accessibility'].get('score', 0)
            print_info(f"   Image Accessibility Score: {img_a11y_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Image validation failed: {str(e)}")
        return None


def test_link_validation(wp):
    """Test link validation capabilities."""
    print_info("\n🔗 Testing Link Validation...")
    
    try:
        validator = LinkValidator(wp)
        
        # Test site links
        result = validator.validate_site_links()
        
        print_success("✅ Link validation completed")
        print_info(f"   Link Health Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display link metrics
        if 'internal_links' in result:
            internal_score = result['internal_links'].get('score', 0)
            print_info(f"   Internal Links Score: {internal_score}/100")
        
        if 'external_links' in result:
            external_score = result['external_links'].get('score', 0)
            print_info(f"   External Links Score: {external_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Link validation failed: {str(e)}")
        return None


def test_comprehensive_validation(wp):
    """Test comprehensive validation capabilities."""
    print_info("\n🎯 Testing Comprehensive Validation...")
    
    try:
        validator = ComprehensiveValidator(wp)
        
        # Run comprehensive site validation
        result = validator.validate_site_comprehensive()
        
        print_success("✅ Comprehensive validation completed")
        print_info(f"   Overall Site Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display comprehensive metrics
        print_info(f"   Total Issues Found: {result.get('total_issues', 0)}")
        print_info(f"   Critical Issues: {result.get('critical_issues', 0)}")
        print_info(f"   Validation Categories: {len(result.get('validation_results', {}))}")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Comprehensive validation failed: {str(e)}")
        return None


def generate_test_report(results):
    """Generate comprehensive test report."""
    print_info("\n📊 Generating Test Report...")
    
    report = {
        'test_date': datetime.now().isoformat(),
        'site_url': 'https://spherevista360.com',
        'test_results': results,
        'summary': {
            'total_tests': len([r for r in results.values() if r is not None]),
            'successful_tests': len([r for r in results.values() if r is not None]),
            'failed_tests': len([r for r in results.values() if r is None]),
            'average_scores': {}
        }
    }
    
    # Calculate average scores
    scores = []
    for test_name, result in results.items():
        if result and 'overall_score' in result:
            score = result['overall_score']
            if isinstance(score, (int, float)) and score > 0:
                scores.append(score)
                report['summary']['average_scores'][test_name] = score
    
    if scores:
        report['summary']['overall_average_score'] = round(sum(scores) / len(scores), 2)
    
    # Save report to file
    report_file = f"validation_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_success(f"✅ Test report saved to: {report_file}")
    
    # Display summary
    print_info("\n" + "="*60)
    print_info("VALIDATION TEST SUMMARY")
    print_info("="*60)
    print_info(f"Site: {report['site_url']}")
    print_info(f"Total Tests: {report['summary']['total_tests']}")
    print_info(f"Successful: {report['summary']['successful_tests']}")
    print_info(f"Failed: {report['summary']['failed_tests']}")
    
    if 'overall_average_score' in report['summary']:
        avg_score = report['summary']['overall_average_score']
        print_info(f"Overall Average Score: {avg_score}/100")
        
        if avg_score >= 80:
            print_success("🎉 Excellent! Your site is performing very well!")
        elif avg_score >= 60:
            print_warning("⚠️  Good performance with room for improvement")
        else:
            print_error("❌ Site needs significant optimization")
    
    print_info("="*60)
    
    return report


def main():
    """Main test execution function."""
    print_info("🚀 Starting Comprehensive Validation Test for SphereVista360")
    print_info("=" * 70)
    
    start_time = time.time()
    
    # Test WordPress connection
    wp, test_post_id = test_wordpress_connection()
    
    if not wp:
        print_error("❌ Cannot proceed without WordPress connection")
        return False
    
    # Run all validation tests
    results = {}
    
    # Individual validation tests
    results['technical'] = test_technical_validation(wp, test_post_id)
    results['seo'] = test_seo_validation(wp, test_post_id)
    results['performance'] = test_performance_validation(wp)
    results['accessibility'] = test_accessibility_validation(wp, test_post_id)
    results['security'] = test_security_validation(wp)
    results['mobile'] = test_mobile_validation(wp)
    results['content_quality'] = test_content_quality_validation(wp, test_post_id)
    results['images'] = test_image_validation(wp, test_post_id)
    results['links'] = test_link_validation(wp)
    results['comprehensive'] = test_comprehensive_validation(wp)
    
    # Generate final report
    report = generate_test_report(results)
    
    execution_time = time.time() - start_time
    print_info(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
    
    print_success("🎉 Comprehensive validation testing completed!")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)