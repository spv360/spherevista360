#!/usr/bin/env python3
"""
Quick Validation Test for SphereVista360
========================================
Test key validation tools with proper authentication setup.
"""

import sys
import os
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
    LinkValidator
)
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def setup_wordpress_client():
    """Set up WordPress client with proper authentication."""
    print_info("🔧 Setting up WordPress client...")
    
    try:
        # Set up credentials - update these with your actual values
        wp_config = {
            'base_url': 'https://spherevista360.com',
            'username': 'spv360',  # Your WordPress username
            'password': 'TWhW QCT5 9XaY u5eJ bMpu aNWj'  # Your application password
        }
        
        # Create client
        wp = WordPressClient()
        wp.base_url = wp_config['base_url']
        wp.username = wp_config['username']
        wp.password = wp_config['password']
        
        # Authenticate
        wp.authenticate()
        
        # Test connection
        posts = wp.get_posts(per_page=1)
        
        print_success(f"✅ WordPress connected to {wp_config['base_url']}")
        print_info(f"   Username: {wp_config['username']}")
        print_info(f"   Test posts found: {len(posts)}")
        
        return wp, posts[0]['id'] if posts else None
        
    except Exception as e:
        print_error(f"❌ WordPress setup failed: {str(e)}")
        return None, None


def test_seo_validator(wp, post_id=None):
    """Test SEO validation with actual site data."""
    print_info("\n🎯 Testing SEO Validator...")
    
    try:
        validator = SEOValidator(wp)
        
        # Test site-wide SEO
        result = validator.validate_site_seo()
        
        print_success("✅ SEO validation completed")
        print_info(f"   Overall SEO Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display key findings
        if 'meta_tags' in result:
            meta_issues = len(result['meta_tags'].get('issues', []))
            print_info(f"   Meta tag issues: {meta_issues}")
        
        if 'structured_data' in result:
            schema_score = result['structured_data'].get('score', 0)
            print_info(f"   Schema markup score: {schema_score}/100")
        
        if 'content_optimization' in result:
            content_score = result['content_optimization'].get('score', 0)
            print_info(f"   Content optimization score: {content_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ SEO validation failed: {str(e)}")
        return None


def test_technical_validator(wp):
    """Test technical validation."""
    print_info("\n🔧 Testing Technical Validator...")
    
    try:
        validator = TechnicalValidator(wp)
        
        # Test site technical aspects
        result = validator.validate_site_technical()
        
        print_success("✅ Technical validation completed")
        print_info(f"   Overall Technical Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display findings
        if 'html_validation' in result:
            html_score = result['html_validation'].get('score', 0)
            html_errors = len(result['html_validation'].get('errors', []))
            print_info(f"   HTML validation score: {html_score}/100 ({html_errors} errors)")
        
        if 'css_validation' in result:
            css_score = result['css_validation'].get('score', 0)
            print_info(f"   CSS validation score: {css_score}/100")
        
        if 'javascript_validation' in result:
            js_score = result['javascript_validation'].get('score', 0)
            print_info(f"   JavaScript validation score: {js_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Technical validation failed: {str(e)}")
        return None


def test_performance_validator(wp):
    """Test performance validation."""
    print_info("\n⚡ Testing Performance Validator...")
    
    try:
        validator = PerformanceValidator(wp)
        
        # Test site performance
        result = validator.validate_site_performance()
        
        print_success("✅ Performance validation completed")
        print_info(f"   Overall Performance Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display performance metrics
        if 'loading_speed' in result:
            speed_score = result['loading_speed'].get('score', 0)
            load_time = result['loading_speed'].get('load_time', 'N/A')
            print_info(f"   Loading speed score: {speed_score}/100 (Load time: {load_time}s)")
        
        if 'resource_optimization' in result:
            resource_score = result['resource_optimization'].get('score', 0)
            print_info(f"   Resource optimization score: {resource_score}/100")
        
        if 'caching' in result:
            cache_score = result['caching'].get('score', 0)
            print_info(f"   Caching score: {cache_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Performance validation failed: {str(e)}")
        return None


def test_accessibility_validator(wp):
    """Test accessibility validation."""
    print_info("\n♿ Testing Accessibility Validator...")
    
    try:
        validator = AccessibilityValidator(wp)
        
        # Test site accessibility
        result = validator.validate_site_accessibility()
        
        print_success("✅ Accessibility validation completed")
        print_info(f"   Overall Accessibility Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display accessibility metrics
        if 'wcag_compliance' in result:
            wcag_data = result['wcag_compliance']
            aa_compliant = wcag_data.get('aa_compliant', 'Unknown')
            aaa_compliant = wcag_data.get('aaa_compliant', 'Unknown')
            print_info(f"   WCAG AA compliance: {aa_compliant}")
            print_info(f"   WCAG AAA compliance: {aaa_compliant}")
        
        if 'color_contrast' in result:
            contrast_score = result['color_contrast'].get('score', 0)
            print_info(f"   Color contrast score: {contrast_score}/100")
        
        if 'keyboard_navigation' in result:
            keyboard_score = result['keyboard_navigation'].get('score', 0)
            print_info(f"   Keyboard navigation score: {keyboard_score}/100")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Accessibility validation failed: {str(e)}")
        return None


def test_link_validator(wp):
    """Test link validation."""
    print_info("\n🔗 Testing Link Validator...")
    
    try:
        validator = LinkValidator(wp)
        
        # Test site links
        result = validator.validate_site_links()
        
        print_success("✅ Link validation completed")
        print_info(f"   Overall Link Score: {result.get('overall_score', 'N/A')}/100")
        
        # Display link metrics
        if 'internal_links' in result:
            internal_score = result['internal_links'].get('score', 0)
            internal_broken = len(result['internal_links'].get('broken_links', []))
            print_info(f"   Internal links score: {internal_score}/100 ({internal_broken} broken)")
        
        if 'external_links' in result:
            external_score = result['external_links'].get('score', 0)
            external_broken = len(result['external_links'].get('broken_links', []))
            print_info(f"   External links score: {external_score}/100 ({external_broken} broken)")
        
        return result
        
    except Exception as e:
        print_error(f"❌ Link validation failed: {str(e)}")
        return None


def generate_summary_report(results):
    """Generate summary report of all tests."""
    print_info("\n📊 VALIDATION TEST SUMMARY")
    print_info("=" * 50)
    
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
    print_info("🚀 Quick Validation Test for SphereVista360")
    print_info("=" * 45)
    
    start_time = time.time()
    
    # Setup WordPress connection
    wp, test_post_id = setup_wordpress_client()
    
    if not wp:
        print_error("❌ Cannot proceed without WordPress connection")
        return False
    
    # Run key validation tests
    results = {}
    
    print_info(f"\n🎯 Running validation tests with post ID: {test_post_id}")
    
    # Test key validators
    results['seo'] = test_seo_validator(wp, test_post_id)
    results['technical'] = test_technical_validator(wp)
    results['performance'] = test_performance_validator(wp)
    results['accessibility'] = test_accessibility_validator(wp)
    results['links'] = test_link_validator(wp)
    
    # Generate summary
    generate_summary_report(results)
    
    execution_time = time.time() - start_time
    print_info(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
    
    print_success("🎉 Validation testing completed!")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)