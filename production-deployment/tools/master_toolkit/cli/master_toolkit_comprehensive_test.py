#!/usr/bin/env python3
"""
Complete Master Toolkit Test for SphereVista360
==============================================
Test both validation and optimization tools comprehensively.
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.core.config import config
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
        print_info(f"   Base URL: {config.get('base_url')}")
        print_info(f"   Test posts found: {len(posts)}")
        
        return wp, posts
        
    except Exception as e:
        print_error(f"❌ WordPress setup failed: {str(e)}")
        return None, None


def test_validation_suite(wp, posts):
    """Test all validation tools."""
    print_info("\n" + "="*60)
    print_info("🔍 VALIDATION SUITE TESTING")
    print_info("="*60)
    
    results = {}
    
    if not posts:
        print_warning("⚠️  No posts available for detailed testing")
        return results
    
    test_post = posts[0]
    post_id = test_post['id']
    post_title = test_post.get('title', {}).get('rendered', 'Untitled')
    
    print_info(f"🎯 Testing with post: {post_title}")
    print_info(f"   Post ID: {post_id}")
    print_info(f"   Post URL: {test_post.get('link', 'N/A')}")
    
    # 1. SEO Validation
    print_info("\n📈 Testing SEO Validation...")
    try:
        seo_validator = SEOValidator(wp)
        seo_result = seo_validator.validate_post(post_id)
        results['seo'] = seo_result
        print_success(f"✅ SEO Score: {seo_result.get('overall_score', 'N/A')}/100")
    except Exception as e:
        print_error(f"❌ SEO validation failed: {str(e)}")
        results['seo'] = None
    
    # 2. Technical Validation
    print_info("\n🔧 Testing Technical Validation...")
    try:
        tech_validator = TechnicalValidator(wp)
        
        # Test multiple technical aspects
        sitemap_result = tech_validator.validate_sitemap_inclusion(post_id)
        robots_result = tech_validator.validate_robots_txt()
        
        tech_result = {
            'sitemap_inclusion': sitemap_result,
            'robots_txt': robots_result,
            'overall_score': robots_result.get('score', 50)
        }
        results['technical'] = tech_result
        print_success(f"✅ Technical Score: {tech_result['overall_score']}/100")
    except Exception as e:
        print_error(f"❌ Technical validation failed: {str(e)}")
        results['technical'] = None
    
    # 3. Performance Validation
    print_info("\n⚡ Testing Performance Validation...")
    try:
        perf_validator = PerformanceValidator(wp)
        perf_result = perf_validator.validate_page_speed(post_id)
        results['performance'] = perf_result
        print_success(f"✅ Performance Score: {perf_result.get('overall_score', 'N/A')}/100")
        
        if 'loading_time' in perf_result:
            print_info(f"   Loading time: {perf_result['loading_time']:.2f}s")
    except Exception as e:
        print_error(f"❌ Performance validation failed: {str(e)}")
        results['performance'] = None
    
    # 4. Accessibility Validation
    print_info("\n♿ Testing Accessibility Validation...")
    try:
        a11y_validator = AccessibilityValidator(wp)
        a11y_result = a11y_validator.validate_accessibility(post_id)
        results['accessibility'] = a11y_result
        print_success(f"✅ Accessibility Score: {a11y_result.get('overall_score', 'N/A')}/100")
        
        if 'wcag_compliance' in a11y_result:
            wcag_data = a11y_result['wcag_compliance']
            print_info(f"   WCAG AA Compliance: {wcag_data.get('aa_compliant', 'Unknown')}")
    except Exception as e:
        print_error(f"❌ Accessibility validation failed: {str(e)}")
        results['accessibility'] = None
    
    # 5. Link Validation
    print_info("\n🔗 Testing Link Validation...")
    try:
        link_validator = LinkValidator(wp)
        link_result = link_validator.validate_post_links(post_id)
        results['links'] = link_result
        print_success(f"✅ Link Score: {link_result.get('overall_score', 'N/A')}/100")
        
        if 'internal_links' in link_result:
            internal_count = len(link_result['internal_links'].get('links', []))
            print_info(f"   Internal links found: {internal_count}")
    except Exception as e:
        print_error(f"❌ Link validation failed: {str(e)}")
        results['links'] = None
    
    # 6. Image Validation
    print_info("\n🖼️  Testing Image Validation...")
    try:
        img_validator = ImageValidator(wp)
        img_result = img_validator.validate_post_images(post_id)
        results['images'] = img_result
        print_success(f"✅ Image Score: {img_result.get('overall_score', 'N/A')}/100")
        
        if 'image_analysis' in img_result:
            total_images = img_result['image_analysis'].get('total_images', 0)
            print_info(f"   Total images: {total_images}")
    except Exception as e:
        print_error(f"❌ Image validation failed: {str(e)}")
        results['images'] = None
    
    # 7. Comprehensive Validation
    print_info("\n🎯 Testing Comprehensive Validation...")
    try:
        comp_validator = ComprehensiveValidator(wp)
        comp_result = comp_validator.validate_post_comprehensive(post_id)
        results['comprehensive'] = comp_result
        print_success(f"✅ Comprehensive Score: {comp_result.get('overall_score', 'N/A')}/100")
        
        if 'issues' in comp_result:
            total_issues = len(comp_result['issues'])
            print_info(f"   Total issues found: {total_issues}")
    except Exception as e:
        print_error(f"❌ Comprehensive validation failed: {str(e)}")
        results['comprehensive'] = None
    
    return results


def test_optimization_suite(wp, posts):
    """Test optimization tools if available."""
    print_info("\n" + "="*60)
    print_info("🚀 OPTIMIZATION SUITE TESTING")
    print_info("="*60)
    
    optimization_results = {}
    
    try:
        # Check if optimization module is available
        from master_toolkit.optimization import (
            ContentOptimizer,
            SEOOptimizer,
            PerformanceOptimizer,
            AccessibilityOptimizer,
            ImageOptimizer
        )
        
        if not posts:
            print_warning("⚠️  No posts available for optimization testing")
            return optimization_results
        
        test_post = posts[0]
        post_id = test_post['id']
        post_title = test_post.get('title', {}).get('rendered', 'Untitled')
        
        print_info(f"🎯 Testing optimization with post: {post_title}")
        print_info(f"   Post ID: {post_id}")
        
        # 1. Content Optimization
        print_info("\n📝 Testing Content Optimization...")
        try:
            content_optimizer = ContentOptimizer(wp)
            content_result = content_optimizer.optimize_post_content(
                post_id, 
                target_keywords=['travel', 'visa'],
                auto_apply=False  # Don't actually apply changes
            )
            optimization_results['content'] = content_result
            print_success(f"✅ Content Optimization Score: {content_result.get('score', 'N/A')}/100")
        except Exception as e:
            print_error(f"❌ Content optimization failed: {str(e)}")
            optimization_results['content'] = None
        
        # 2. SEO Optimization
        print_info("\n📈 Testing SEO Optimization...")
        try:
            seo_optimizer = SEOOptimizer(wp)
            seo_opt_result = seo_optimizer.optimize_post_seo(
                post_id,
                target_keywords=['travel', 'visa'],
                auto_apply=False
            )
            optimization_results['seo'] = seo_opt_result
            print_success(f"✅ SEO Optimization Score: {seo_opt_result.get('score', 'N/A')}/100")
        except Exception as e:
            print_error(f"❌ SEO optimization failed: {str(e)}")
            optimization_results['seo'] = None
        
        # 3. Performance Optimization
        print_info("\n⚡ Testing Performance Optimization...")
        try:
            perf_optimizer = PerformanceOptimizer(wp)
            perf_opt_result = perf_optimizer.optimize_post_performance(
                post_id,
                auto_apply=False
            )
            optimization_results['performance'] = perf_opt_result
            print_success(f"✅ Performance Optimization Score: {perf_opt_result.get('score', 'N/A')}/100")
        except Exception as e:
            print_error(f"❌ Performance optimization failed: {str(e)}")
            optimization_results['performance'] = None
        
        # 4. Accessibility Optimization
        print_info("\n♿ Testing Accessibility Optimization...")
        try:
            a11y_optimizer = AccessibilityOptimizer(wp)
            a11y_opt_result = a11y_optimizer.optimize_post_accessibility(
                post_id,
                auto_apply=False
            )
            optimization_results['accessibility'] = a11y_opt_result
            print_success(f"✅ Accessibility Optimization Score: {a11y_opt_result.get('score', 'N/A')}/100")
        except Exception as e:
            print_error(f"❌ Accessibility optimization failed: {str(e)}")
            optimization_results['accessibility'] = None
        
        # 5. Image Optimization
        print_info("\n🖼️  Testing Image Optimization...")
        try:
            img_optimizer = ImageOptimizer(wp)
            img_opt_result = img_optimizer.optimize_post_images(
                post_id,
                auto_apply=False
            )
            optimization_results['images'] = img_opt_result
            print_success(f"✅ Image Optimization Score: {img_opt_result.get('score', 'N/A')}/100")
        except Exception as e:
            print_error(f"❌ Image optimization failed: {str(e)}")
            optimization_results['images'] = None
    
    except ImportError:
        print_warning("⚠️  Optimization module not available - skipping optimization tests")
    except Exception as e:
        print_error(f"❌ Optimization suite failed: {str(e)}")
    
    return optimization_results


def generate_comprehensive_report(validation_results, optimization_results, posts):
    """Generate comprehensive report of all tests."""
    print_info("\n" + "="*70)
    print_info("📊 COMPREHENSIVE MASTER TOOLKIT TEST REPORT")
    print_info("="*70)
    
    if posts:
        test_post = posts[0]
        print_info(f"🎯 Test Subject:")
        print_info(f"   Post: {test_post.get('title', {}).get('rendered', 'Untitled')}")
        print_info(f"   ID: {test_post['id']}")
        print_info(f"   URL: {test_post.get('link', 'N/A')}")
        print_info(f"   Date: {test_post.get('date', 'N/A')}")
    
    print_info("\n🔍 VALIDATION RESULTS:")
    print_info("-" * 50)
    
    validation_scores = []
    for test_name, result in validation_results.items():
        if result:
            score = result.get('overall_score', 0)
            if score and score > 0:
                validation_scores.append(score)
                status = f"✅ {score}/100"
                if score >= 80:
                    status += " (EXCELLENT)"
                elif score >= 60:
                    status += " (GOOD)"
                elif score >= 40:
                    status += " (FAIR)"
                else:
                    status += " (NEEDS WORK)"
            else:
                status = "✅ COMPLETED"
        else:
            status = "❌ FAILED"
        
        print_info(f"   {test_name.upper():15} {status}")
    
    if optimization_results:
        print_info("\n🚀 OPTIMIZATION RESULTS:")
        print_info("-" * 50)
        
        optimization_scores = []
        for test_name, result in optimization_results.items():
            if result:
                score = result.get('score', 0)
                if score and score > 0:
                    optimization_scores.append(score)
                    status = f"✅ {score}/100"
                    if score >= 80:
                        status += " (EXCELLENT)"
                    elif score >= 60:
                        status += " (GOOD)"
                    elif score >= 40:
                        status += " (FAIR)"
                    else:
                        status += " (NEEDS WORK)"
                else:
                    status = "✅ COMPLETED"
            else:
                status = "❌ FAILED"
            
            print_info(f"   {test_name.upper():15} {status}")
    
    # Calculate overall scores
    print_info("\n📈 OVERALL ASSESSMENT:")
    print_info("-" * 50)
    
    if validation_scores:
        avg_validation = sum(validation_scores) / len(validation_scores)
        print_info(f"   Average Validation Score: {avg_validation:.1f}/100")
    
    if optimization_results and any(optimization_results.values()):
        optimization_scores = [
            r.get('score', 0) for r in optimization_results.values() 
            if r and r.get('score', 0) > 0
        ]
        if optimization_scores:
            avg_optimization = sum(optimization_scores) / len(optimization_scores)
            print_info(f"   Average Optimization Score: {avg_optimization:.1f}/100")
    
    all_scores = validation_scores + (optimization_scores if 'optimization_scores' in locals() else [])
    if all_scores:
        overall_avg = sum(all_scores) / len(all_scores)
        print_info(f"   OVERALL SITE SCORE: {overall_avg:.1f}/100")
        
        if overall_avg >= 85:
            print_success("🏆 OUTSTANDING! Your site is exceptionally well optimized!")
        elif overall_avg >= 70:
            print_success("🎉 EXCELLENT! Your site is performing very well!")
        elif overall_avg >= 55:
            print_warning("👍 GOOD! Your site is solid with room for improvement")
        elif overall_avg >= 40:
            print_warning("⚠️  FAIR! Your site needs optimization")
        else:
            print_error("🚨 CRITICAL! Your site requires immediate attention")
    
    print_info("="*70)
    
    # Save comprehensive report
    report_file = f"master_toolkit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump({
            'test_date': datetime.now().isoformat(),
            'site_url': config.get('base_url'),
            'test_post': posts[0] if posts else None,
            'validation_results': validation_results,
            'optimization_results': optimization_results,
            'summary': {
                'validation_tests': len(validation_results),
                'optimization_tests': len(optimization_results) if optimization_results else 0,
                'average_validation_score': sum(validation_scores) / len(validation_scores) if validation_scores else 0,
                'overall_score': sum(all_scores) / len(all_scores) if all_scores else 0
            }
        }, f, indent=2)
    
    print_success(f"📄 Comprehensive report saved: {report_file}")
    
    return report_file


def main():
    """Main test execution."""
    print_info("🚀 MASTER TOOLKIT COMPREHENSIVE TEST")
    print_info("SphereVista360 - Complete Validation & Optimization Suite")
    print_info("=" * 60)
    
    start_time = time.time()
    
    # Setup WordPress connection
    wp, posts = setup_wordpress_client()
    
    if not wp:
        print_error("❌ Cannot proceed without WordPress connection")
        return False
    
    # Run validation suite
    validation_results = test_validation_suite(wp, posts)
    
    # Run optimization suite
    optimization_results = test_optimization_suite(wp, posts)
    
    # Generate comprehensive report
    report_file = generate_comprehensive_report(validation_results, optimization_results, posts)
    
    execution_time = time.time() - start_time
    print_info(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
    
    print_success("🎉 Master Toolkit testing completed!")
    print_info(f"📄 Full results available in: {report_file}")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)