#!/usr/bin/env python3
"""
Complete Site Content Validation
================================
Test all posts and pages on SphereVista360 for comprehensive validation.
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
        
        print_success(f"✅ WordPress connected successfully")
        print_info(f"   Base URL: {config.get('base_url')}")
        
        return wp
        
    except Exception as e:
        print_error(f"❌ WordPress setup failed: {str(e)}")
        return None


def get_all_content(wp):
    """Get all posts and pages from the site."""
    print_info("\n📋 Fetching all site content...")
    
    all_content = {
        'posts': [],
        'pages': []
    }
    
    try:
        # Get all published posts (with pagination)
        page = 1
        while True:
            try:
                posts = wp.get_posts(per_page=50, page=page)
                if not posts:
                    break
                all_content['posts'].extend(posts)
                page += 1
                if page > 10:  # Safety limit
                    break
            except Exception as e:
                print_warning(f"⚠️  Error fetching posts page {page}: {str(e)}")
                break
            
        print_success(f"✅ Found {len(all_content['posts'])} published posts")
        
        # Get all published pages
        try:
            # Try to get pages - might not be available on all WordPress installations
            pages = wp.get_pages(per_page=50)
            all_content['pages'].extend(pages or [])
            print_success(f"✅ Found {len(all_content['pages'])} published pages")
        except Exception as e:
            print_warning(f"⚠️  Could not fetch pages: {str(e)}")
            print_info("   Continuing with posts only...")
        
        # Display content summary
        print_info(f"\n📊 Content Summary:")
        print_info(f"   Total Posts: {len(all_content['posts'])}")
        print_info(f"   Total Pages: {len(all_content['pages'])}")
        print_info(f"   Total Content Items: {len(all_content['posts']) + len(all_content['pages'])}")
        
        return all_content
        
    except Exception as e:
        print_error(f"❌ Failed to fetch content: {str(e)}")
        return None


def validate_content_item(wp, item, item_type, validators):
    """Validate a single content item (post or page)."""
    item_id = item['id']
    title = item.get('title', {}).get('rendered', 'Untitled')
    url = item.get('link', 'N/A')
    
    print_info(f"\n🎯 Validating {item_type}: {title}")
    print_info(f"   ID: {item_id}")
    print_info(f"   URL: {url}")
    
    results = {
        'id': item_id,
        'title': title,
        'url': url,
        'type': item_type,
        'validation_results': {}
    }
    
    # Run each validator
    for validator_name, validator in validators.items():
        try:
            if validator_name == 'seo':
                result = validator.validate_post(item_id)
            elif validator_name == 'technical':
                sitemap_result = validator.validate_sitemap_inclusion(item_id)
                result = {'sitemap_inclusion': sitemap_result, 'overall_score': 50}
            elif validator_name == 'performance':
                result = validator.validate_page_speed(item_id)
            elif validator_name == 'accessibility':
                result = validator.validate_accessibility(item_id)
            elif validator_name == 'links':
                result = validator.validate_post_links(item_id)
            elif validator_name == 'images':
                result = validator.validate_post_images(item_id)
            elif validator_name == 'comprehensive':
                result = validator.validate_post_comprehensive(item_id)
            
            results['validation_results'][validator_name] = result
            score = result.get('overall_score', 'N/A')
            print_info(f"   ✅ {validator_name.upper()}: {score}/100" if score != 'N/A' else f"   ✅ {validator_name.upper()}: COMPLETED")
            
        except Exception as e:
            print_error(f"   ❌ {validator_name.upper()}: {str(e)}")
            results['validation_results'][validator_name] = None
    
    return results


def test_all_content(wp, all_content):
    """Test all posts and pages on the site."""
    print_info("\n" + "="*80)
    print_info("🔍 COMPREHENSIVE SITE VALIDATION")
    print_info("="*80)
    
    # Initialize validators
    validators = {
        'seo': SEOValidator(wp),
        'technical': TechnicalValidator(wp),
        'performance': PerformanceValidator(wp),
        'accessibility': AccessibilityValidator(wp),
        'links': LinkValidator(wp),
        'images': ImageValidator(wp),
        'comprehensive': ComprehensiveValidator(wp)
    }
    
    all_results = {
        'posts': [],
        'pages': [],
        'summary': {
            'total_items': 0,
            'total_posts': 0,
            'total_pages': 0,
            'validation_scores': {},
            'average_scores': {}
        }
    }
    
    # Test all posts
    print_info(f"\n📝 VALIDATING {len(all_content['posts'])} POSTS")
    print_info("-" * 60)
    
    for i, post in enumerate(all_content['posts'], 1):
        print_info(f"\n[{i}/{len(all_content['posts'])}] Testing Post...")
        result = validate_content_item(wp, post, 'post', validators)
        all_results['posts'].append(result)
        
        # Add small delay to avoid overwhelming the server
        time.sleep(1)
    
    # Test all pages
    print_info(f"\n📄 VALIDATING {len(all_content['pages'])} PAGES")
    print_info("-" * 60)
    
    for i, page in enumerate(all_content['pages'], 1):
        print_info(f"\n[{i}/{len(all_content['pages'])}] Testing Page...")
        result = validate_content_item(wp, page, 'page', validators)
        all_results['pages'].append(result)
        
        # Add small delay to avoid overwhelming the server
        time.sleep(1)
    
    return all_results


def generate_comprehensive_report(all_results):
    """Generate comprehensive report for all content."""
    print_info("\n" + "="*80)
    print_info("📊 COMPREHENSIVE SITE VALIDATION REPORT")
    print_info("="*80)
    
    total_posts = len(all_results['posts'])
    total_pages = len(all_results['pages'])
    total_items = total_posts + total_pages
    
    print_info(f"\n📋 Content Summary:")
    print_info(f"   Total Posts Tested: {total_posts}")
    print_info(f"   Total Pages Tested: {total_pages}")
    print_info(f"   Total Items Tested: {total_items}")
    
    # Calculate average scores for each validator
    validator_scores = {
        'seo': [],
        'technical': [],
        'performance': [],
        'accessibility': [],
        'links': [],
        'images': [],
        'comprehensive': []
    }
    
    # Collect scores from all items
    for item_list in [all_results['posts'], all_results['pages']]:
        for item in item_list:
            for validator_name, result in item['validation_results'].items():
                if result and 'overall_score' in result and result['overall_score']:
                    validator_scores[validator_name].append(result['overall_score'])
    
    print_info(f"\n🔍 Validation Results Summary:")
    print_info("-" * 50)
    
    overall_scores = []
    for validator_name, scores in validator_scores.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            overall_scores.extend(scores)
            status = ""
            if avg_score >= 80:
                status = "(EXCELLENT)"
            elif avg_score >= 60:
                status = "(GOOD)"
            elif avg_score >= 40:
                status = "(FAIR)"
            else:
                status = "(NEEDS WORK)"
            
            print_info(f"   {validator_name.upper():15} Average: {avg_score:.1f}/100 {status}")
            print_info(f"   {'':<15} Items tested: {len(scores)}")
        else:
            print_info(f"   {validator_name.upper():15} No valid scores")
    
    # Overall site assessment
    print_info(f"\n📈 OVERALL SITE ASSESSMENT:")
    print_info("-" * 50)
    
    if overall_scores:
        site_average = sum(overall_scores) / len(overall_scores)
        print_info(f"   OVERALL SITE SCORE: {site_average:.1f}/100")
        
        if site_average >= 85:
            print_success("🏆 OUTSTANDING! Your entire site is exceptionally well optimized!")
        elif site_average >= 70:
            print_success("🎉 EXCELLENT! Your site is performing very well across all content!")
        elif site_average >= 55:
            print_warning("👍 GOOD! Your site is solid with room for improvement")
        elif site_average >= 40:
            print_warning("⚠️  FAIR! Your site needs optimization")
        else:
            print_error("🚨 CRITICAL! Your site requires immediate attention")
    
    # Identify top performing and problematic content
    print_info(f"\n🏆 TOP PERFORMING CONTENT:")
    print_info("-" * 50)
    
    top_items = []
    for item_list in [all_results['posts'], all_results['pages']]:
        for item in item_list:
            comp_result = item['validation_results'].get('comprehensive')
            if comp_result and comp_result.get('overall_score'):
                top_items.append((item, comp_result['overall_score']))
    
    # Sort by score and show top 5
    top_items.sort(key=lambda x: x[1], reverse=True)
    for i, (item, score) in enumerate(top_items[:5], 1):
        print_info(f"   {i}. {item['title']} ({item['type']}) - {score}/100")
    
    print_info(f"\n⚠️  CONTENT NEEDING ATTENTION:")
    print_info("-" * 50)
    
    # Show bottom 5
    bottom_items = top_items[-5:] if len(top_items) > 5 else []
    for i, (item, score) in enumerate(bottom_items, 1):
        print_info(f"   {i}. {item['title']} ({item['type']}) - {score}/100")
    
    # Save comprehensive report
    report_file = f"complete_site_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump({
            'test_date': datetime.now().isoformat(),
            'site_url': config.get('base_url'),
            'summary': {
                'total_posts': total_posts,
                'total_pages': total_pages,
                'total_items': total_items,
                'overall_score': sum(overall_scores) / len(overall_scores) if overall_scores else 0,
                'validator_averages': {name: sum(scores)/len(scores) if scores else 0 
                                     for name, scores in validator_scores.items()}
            },
            'detailed_results': all_results
        }, f, indent=2)
    
    print_success(f"📄 Complete site report saved: {report_file}")
    print_info("="*80)
    
    return report_file


def main():
    """Main execution for complete site validation."""
    print_info("🚀 COMPLETE SITE VALIDATION")
    print_info("SphereVista360 - All Posts & Pages Analysis")
    print_info("=" * 60)
    
    start_time = time.time()
    
    # Setup WordPress connection
    wp = setup_wordpress_client()
    if not wp:
        print_error("❌ Cannot proceed without WordPress connection")
        return False
    
    # Get all content
    all_content = get_all_content(wp)
    if not all_content:
        print_error("❌ Cannot proceed without content")
        return False
    
    total_items = len(all_content['posts']) + len(all_content['pages'])
    if total_items == 0:
        print_warning("⚠️  No content found to validate")
        return True
    
    print_info(f"\n⏰ Estimated time: ~{total_items * 2} seconds ({total_items} items × 2s each)")
    
    # Ask for confirmation for large sites
    if total_items > 20:
        print_warning(f"⚠️  This will test {total_items} content items. This may take a while.")
        response = input("Continue? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print_info("🚫 Testing cancelled by user")
            return False
    
    # Run comprehensive validation
    all_results = test_all_content(wp, all_content)
    
    # Generate comprehensive report
    report_file = generate_comprehensive_report(all_results)
    
    execution_time = time.time() - start_time
    print_info(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
    
    print_success("🎉 Complete site validation finished!")
    print_info(f"📄 Full results available in: {report_file}")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)