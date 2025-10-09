#!/usr/bin/env python3
"""
Test Enhanced Master-Toolkit Tools
==================================
Test script to verify the enhanced validation tools work correctly.
"""

import sys
import os
import json
from datetime import datetime

# Add the master_toolkit to Python path
sys.path.append('/home/kddevops/projects/spherevista360')

from master_toolkit.core import WordPressClient
from master_toolkit.utils.auto_fixer import AutoFixer
from master_toolkit.validation.images import ImageValidator
from master_toolkit.validation.seo import SEOValidator
from master_toolkit.validation.content_quality import ContentQualityEnhancer


def test_wordpress_connection():
    """Test WordPress API connection."""
    print("🔍 Testing WordPress connection...")
    
    try:
        wp = WordPressClient()
        
        # Test basic connection
        posts = wp.get_posts(per_page=1)
        if posts:
            print(f"✅ Connected to WordPress - Found {len(posts)} posts")
            return wp
        else:
            print("❌ No posts found")
            return None
            
    except Exception as e:
        print(f"❌ WordPress connection failed: {e}")
        return None


def test_enhanced_tools(wp_client, test_post_id=None):
    """Test the enhanced validation tools."""
    print("\n🧪 Testing Enhanced Validation Tools...")
    
    # Get a test post ID if not provided
    if not test_post_id:
        try:
            posts = wp_client.get_posts(per_page=5)
            if posts:
                test_post_id = posts[0]['id']
                print(f"📝 Using test post ID: {test_post_id}")
            else:
                print("❌ No posts available for testing")
                return False
        except Exception as e:
            print(f"❌ Failed to get test post: {e}")
            return False
    
    # Test ImageValidator enhancements
    print("\n🖼️  Testing ImageValidator enhancements...")
    try:
        image_validator = ImageValidator(wp_client)
        
        # Test featured image check
        featured_check = image_validator.check_featured_image(test_post_id)
        print(f"   Featured image check: {'✅' if not featured_check.get('error') else '❌'}")
        print(f"   Has featured image: {featured_check.get('has_featured_image', False)}")
        
        # Test featured image setting (dry run)
        if not featured_check.get('has_featured_image', False):
            featured_set = image_validator.set_featured_image_from_content(test_post_id, dry_run=True)
            print(f"   Featured image setting: {'✅' if not featured_set.get('error') else '❌'}")
            print(f"   Message: {featured_set.get('message', 'No message')}")
        
    except Exception as e:
        print(f"❌ ImageValidator test failed: {e}")
        return False
    
    # Test SEOValidator enhancements
    print("\n🎯 Testing SEOValidator enhancements...")
    try:
        seo_validator = SEOValidator(wp_client)
        
        # Test meta description addition (dry run)
        meta_result = seo_validator.add_meta_description(test_post_id, dry_run=True)
        print(f"   Meta description: {'✅' if not meta_result.get('error') else '❌'}")
        print(f"   Message: {meta_result.get('message', 'No message')}")
        
        # Test social meta tags (dry run)
        social_result = seo_validator.add_social_meta_tags(test_post_id, dry_run=True)
        print(f"   Social meta tags: {'✅' if not social_result.get('error') else '❌'}")
        
        # Test schema markup (dry run)
        schema_result = seo_validator.add_schema_markup(test_post_id, dry_run=True)
        print(f"   Schema markup: {'✅' if not schema_result.get('error') else '❌'}")
        
    except Exception as e:
        print(f"❌ SEOValidator test failed: {e}")
        return False
    
    # Test ContentQualityEnhancer
    print("\n📝 Testing ContentQualityEnhancer...")
    try:
        content_enhancer = ContentQualityEnhancer(wp_client)
        
        # Test content quality analysis
        quality_analysis = content_enhancer.analyze_content_quality(test_post_id)
        print(f"   Quality analysis: {'✅' if not quality_analysis.get('error') else '❌'}")
        
        if 'overall_score' in quality_analysis:
            score = quality_analysis['overall_score']
            grade = quality_analysis['grade']
            print(f"   Content score: {score}/100 (Grade: {grade})")
            
            # Show metrics
            metrics = quality_analysis.get('metrics', {})
            print(f"   Word count: {metrics.get('word_count', 0)}")
            print(f"   Headings: {metrics.get('headings_count', 0)}")
            print(f"   Internal links: {metrics.get('internal_links_count', 0)}")
        
        # Test content enhancement (dry run)
        enhancement_result = content_enhancer.enhance_content_structure(test_post_id, dry_run=True)
        print(f"   Content enhancement: {'✅' if not enhancement_result.get('error') else '❌'}")
        
        # Test internal linking (dry run)
        linking_result = content_enhancer.add_internal_links(test_post_id, dry_run=True)
        print(f"   Internal linking: {'✅' if not linking_result.get('error') else '❌'}")
        
    except Exception as e:
        print(f"❌ ContentQualityEnhancer test failed: {e}")
        return False
    
    print("✅ All enhanced tools tested successfully!")
    return True


def test_auto_fixer(wp_client):
    """Test the AutoFixer workflow."""
    print("\n🤖 Testing AutoFixer workflow...")
    
    try:
        auto_fixer = AutoFixer(wp_client)
        
        # Test analysis of issues (small sample)
        print("   Running issue analysis...")
        analysis = auto_fixer.analyze_all_issues(per_page=3)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return False
        
        print(f"✅ Analysis completed:")
        print(f"   Posts analyzed: {analysis['total_posts']}")
        print(f"   Total issues: {analysis['total_issues']}")
        print(f"   Posts with issues: {analysis['posts_with_issues']}")
        
        # Show issue breakdown
        issue_summary = analysis.get('issue_summary', {})
        for issue_type, post_ids in issue_summary.items():
            if post_ids:
                print(f"   {issue_type}: {len(post_ids)} posts")
        
        # Test fix recommendations
        recommendations = auto_fixer.get_fix_recommendations(analysis)
        if 'error' not in recommendations:
            print(f"✅ Fix recommendations generated")
            print(f"   Estimated total time: {recommendations['total_estimated_time']} minutes")
        
        # Test dry run of fixes
        if analysis['posts_with_issues'] > 0:
            print("   Testing dry run fixes...")
            fix_results = auto_fixer.fix_all_issues(per_page=2, dry_run=True, priority_only=True)
            
            if 'error' not in fix_results:
                print(f"✅ Dry run completed successfully")
                print(f"   {fix_results.get('message', 'No message')}")
            else:
                print(f"❌ Dry run failed: {fix_results['error']}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ AutoFixer test failed: {e}")
        return False


def generate_test_report(results):
    """Generate a test report."""
    print("\n📊 Test Report")
    print("=" * 50)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Test completed: {timestamp}")
    print()
    
    if results['connection']:
        print("✅ WordPress Connection: PASS")
    else:
        print("❌ WordPress Connection: FAIL")
        return
    
    if results['tools']:
        print("✅ Enhanced Tools: PASS")
    else:
        print("❌ Enhanced Tools: FAIL")
    
    if results['auto_fixer']:
        print("✅ AutoFixer Workflow: PASS")
    else:
        print("❌ AutoFixer Workflow: FAIL")
    
    print()
    
    if all(results.values()):
        print("🎉 All tests passed! Enhanced tools are ready to use.")
        print()
        print("Next steps:")
        print("1. Run auto_fixer.analyze_all_issues() to get full site analysis")
        print("2. Use auto_fixer.fix_all_issues(dry_run=False) to apply fixes")
        print("3. Re-run site health audit to verify improvements")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")


def main():
    """Main test function."""
    print("🧪 Enhanced Master-Toolkit Test Suite")
    print("=" * 50)
    
    results = {
        'connection': False,
        'tools': False,
        'auto_fixer': False
    }
    
    # Test WordPress connection
    wp_client = test_wordpress_connection()
    if wp_client:
        results['connection'] = True
        
        # Test enhanced tools
        if test_enhanced_tools(wp_client):
            results['tools'] = True
            
            # Test auto-fixer
            if test_auto_fixer(wp_client):
                results['auto_fixer'] = True
    
    # Generate report
    generate_test_report(results)


if __name__ == "__main__":
    main()