#!/usr/bin/env python3
"""
SEO Validation Tool
==================
Command-line tool for comprehensive WordPress SEO validation.
"""

import sys
import argparse
from pathlib import Path

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))

from wp_client import WordPressClient, print_header, print_section
from seo_validator import SEOValidator, validate_all_posts, validate_single_post


def main():
    """Main CLI interface for SEO validation."""
    parser = argparse.ArgumentParser(description='WordPress SEO Validation Tool')
    parser.add_argument('--post-id', type=int, help='Validate specific post ID')
    parser.add_argument('--category', type=str, help='Filter by category name')
    parser.add_argument('--pages', action='store_true', help='Validate pages instead of posts')
    parser.add_argument('--report', type=str, help='Save report to file')
    parser.add_argument('--username', type=str, help='WordPress username')
    parser.add_argument('--password', type=str, help='WordPress application password')
    
    args = parser.parse_args()
    
    print_header("SEO VALIDATION TOOL")
    
    # Initialize WordPress client
    wp_client = WordPressClient()
    if not wp_client.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    validator = SEOValidator()
    results = []
    
    if args.post_id:
        # Validate single post
        print_section(f"VALIDATING POST ID: {args.post_id}")
        try:
            result = validate_single_post(wp_client, args.post_id)
            results = [result]
            print_seo_result(result)
        except Exception as e:
            print(f"❌ Error validating post {args.post_id}: {e}")
            return 1
            
    elif args.pages:
        # Validate pages
        print_section("VALIDATING ALL PAGES")
        pages = wp_client.get_pages()
        
        for page in pages:
            try:
                content = wp_client.get_page_content(page['link'])
                result = validator.validate_content(
                    content, page['title']['rendered'], page['link']
                )
                result['page_id'] = page['id']
                results.append(result)
                print(f"✅ {page['title']['rendered'][:50]}... - {result['seo_score']['core_percentage']:.1f}%")
            except Exception as e:
                print(f"⚠️ Error validating page {page['id']}: {e}")
    
    else:
        # Validate posts
        category_text = f" (Category: {args.category})" if args.category else ""
        print_section(f"VALIDATING ALL POSTS{category_text}")
        results = validate_all_posts(wp_client, args.category)
        
        # Print summary
        if results:
            avg_score = sum(r['seo_score']['core_percentage'] for r in results) / len(results)
            perfect_count = sum(1 for r in results if r['seo_score']['core_percentage'] == 100)
            
            print(f"\n📊 VALIDATION SUMMARY:")
            print(f"   📄 Posts analyzed: {len(results)}")
            print(f"   📈 Average score: {avg_score:.1f}%")
            print(f"   🎯 Perfect scores: {perfect_count}/{len(results)}")
            
            print(f"\n📋 INDIVIDUAL RESULTS:")
            for i, result in enumerate(results, 1):
                score = result['seo_score']
                print(f"   {i}. {result['title'][:45]}...")
                print(f"      📊 {score['core_percentage']:.1f}% ({score['breakdown']})")
    
    # Generate and save report
    if results:
        report = validator.generate_report(results)
        
        if args.report:
            try:
                with open(args.report, 'w') as f:
                    f.write(report)
                print(f"\n💾 Report saved to: {args.report}")
            except Exception as e:
                print(f"⚠️ Error saving report: {e}")
        else:
            print("\n" + "="*50)
            print(report)
    
    return 0


def print_seo_result(result: dict):
    """Print detailed SEO result."""
    print(f"\n📄 Title: {result['title']}")
    print(f"🌐 URL: {result['url']}")
    
    score = result['seo_score']
    print(f"\n📊 SEO Score: {score['core_percentage']:.1f}% (Grade: {score['grade']})")
    print(f"   Core: {score['core_score']}/{score['core_max']}")
    print(f"   Bonus: {score['bonus_score']}/{score['bonus_max']}")
    
    # H2 Headings
    h2 = result['h2_headings']
    status = "✅" if h2['meets_requirement'] else "❌"
    print(f"\n📝 H2 Headings: {status} {h2['count']} found")
    if h2['headings']:
        for i, heading in enumerate(h2['headings'][:3], 1):
            print(f"   {i}. {heading}")
        if len(h2['headings']) > 3:
            print(f"   ... and {len(h2['headings']) - 3} more")
    print(f"   💡 {h2['recommendation']}")
    
    # Images
    img = result['images']
    status = "✅" if img['meets_requirement'] else "❌"
    print(f"\n🖼️ Images: {status} {img['count']} found")
    print(f"   Alt text: {img['images_with_alt']}/{img['count']} ({img['alt_percentage']:.1f}%)")
    print(f"   💡 {img['recommendation']}")
    
    # Title
    title = result['title_validation']
    status = "✅" if title['meets_requirement'] else "❌"
    print(f"\n📏 Title Length: {status} {title['length']}/60 characters")
    print(f"   💡 {title['recommendation']}")
    
    # Internal Links
    links = result['internal_links']
    status = "✅" if links['meets_requirement'] else "❌"
    print(f"\n🔗 Internal Links: {status} {links['internal_count']} found")
    print(f"   External: {links['external_count']}")
    print(f"   💡 {links['recommendation']}")
    
    # Meta Description
    meta = result['meta_description']
    status = "✅" if meta['meets_requirement'] else "❌"
    print(f"\n📋 Meta Description: {status}")
    if meta['description']:
        print(f"   Length: {meta['length']}/160 characters")
        print(f"   Text: {meta['description'][:100]}...")
    print(f"   💡 {meta['recommendation']}")


if __name__ == "__main__":
    sys.exit(main())