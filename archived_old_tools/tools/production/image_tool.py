#!/usr/bin/env python3
"""
Image Validation Tool
====================
Command-line tool for WordPress image validation and optimization.
"""

import sys
import argparse
from pathlib import Path

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))

from wp_client import WordPressClient, print_header, print_section
from image_validator import ImageValidator, validate_post_images, fix_post_images


def main():
    """Main CLI interface for image validation."""
    parser = argparse.ArgumentParser(description='WordPress Image Validation Tool')
    parser.add_argument('--post-id', type=int, help='Validate specific post ID')
    parser.add_argument('--page-id', type=int, help='Validate specific page ID')
    parser.add_argument('--fix', action='store_true', help='Fix image issues automatically')
    parser.add_argument('--add-images', action='store_true', help='Add images to content without images')
    parser.add_argument('--category', type=str, help='Validate posts in specific category')
    parser.add_argument('--report', type=str, help='Save report to file')
    parser.add_argument('--username', type=str, help='WordPress username')
    parser.add_argument('--password', type=str, help='WordPress application password')
    
    args = parser.parse_args()
    
    print_header("IMAGE VALIDATION TOOL")
    
    # Initialize WordPress client
    wp_client = WordPressClient()
    if not wp_client.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    validator = ImageValidator(wp_client)
    results = []
    
    if args.post_id:
        # Validate specific post
        print_section(f"VALIDATING POST ID: {args.post_id}")
        try:
            result = validate_post_images(wp_client, args.post_id)
            results = [result]
            print_image_result(result)
            
            if args.fix:
                print("\n🔧 FIXING IMAGES...")
                success = fix_post_images(wp_client, args.post_id, args.add_images)
                if success:
                    print("✅ Image fixes applied successfully")
                else:
                    print("❌ Failed to apply image fixes")
                    
        except Exception as e:
            print(f"❌ Error validating post {args.post_id}: {e}")
            return 1
    
    elif args.page_id:
        # Validate specific page
        print_section(f"VALIDATING PAGE ID: {args.page_id}")
        try:
            page = wp_client.get_page(args.page_id)
            content = wp_client.get_page_content(page['link'])
            result = validator.validate_content_images(content, page['title']['rendered'])
            result['page_id'] = args.page_id
            results = [result]
            print_image_result(result)
            
        except Exception as e:
            print(f"❌ Error validating page {args.page_id}: {e}")
            return 1
    
    else:
        # Validate all posts or by category
        category_text = f" (Category: {args.category})" if args.category else ""
        print_section(f"VALIDATING ALL POSTS{category_text}")
        
        posts = wp_client.get_posts(per_page=50)
        
        for post in posts:
            # Filter by category if specified
            if args.category:
                categories = []
                for cat_id in post.get('categories', []):
                    try:
                        cat = wp_client.get_category(cat_id)
                        categories.append(cat['name'])
                    except:
                        continue
                
                if args.category not in categories:
                    continue
            
            try:
                result = validate_post_images(wp_client, post['id'])
                result['post_id'] = post['id']
                results.append(result)
                
                # Print summary
                score = result['score']
                issues_count = len(result['issues'])
                status = "✅" if issues_count == 0 else f"⚠️ {issues_count} issues"
                
                print(f"{status} {result['title'][:45]}... - {score['percentage']:.1f}%")
                
                # Fix if requested
                if args.fix and (result['needs_images'] or result['has_broken_images']):
                    success = fix_post_images(wp_client, post['id'], args.add_images)
                    if success:
                        print(f"    🔧 Fixed images for post {post['id']}")
                    
            except Exception as e:
                print(f"⚠️ Error validating post {post['id']}: {e}")
    
    # Generate summary report
    if results:
        print_summary_report(results)
        
        # Save report if requested
        if args.report:
            save_image_report(results, args.report)
    
    return 0


def print_image_result(result: dict):
    """Print detailed image validation result."""
    print(f"\n📄 Title: {result['title']}")
    print(f"🖼️ Total Images: {result['total_images']}")
    
    if result['total_images'] > 0:
        score = result['score']
        print(f"📊 Image Score: {score['percentage']:.1f}% (Grade: {score['grade']})")
        print(f"   Breakdown: Images={score['breakdown']['has_images']:.1f}, Alt={score['breakdown']['alt_text']:.1f}, Access={score['breakdown']['accessibility']:.1f}")
        
        print(f"✅ Images with alt text: {result['images_with_alt']}/{result['total_images']}")
        print(f"🌐 Accessible images: {result['accessible_images']}/{result['total_images']}")
        print(f"🔗 External images: {result['external_images']}/{result['total_images']}")
        
        # Show individual images
        print(f"\n📋 IMAGE DETAILS:")
        for i, img in enumerate(result['images'], 1):
            alt_status = "✅" if img['has_alt'] else "❌"
            access_status = "✅" if img['is_accessible'] else "❌"
            print(f"   {i}. {alt_status} Alt | {access_status} Access")
            print(f"      URL: {img['src'][:60]}...")
            if img['alt']:
                print(f"      Alt: {img['alt'][:50]}...")
    else:
        print("⚠️ No images found in content")
    
    # Show issues
    if result['issues']:
        print(f"\n🚨 ISSUES FOUND ({len(result['issues'])}):")
        for issue in result['issues']:
            print(f"   ⚠️ {issue}")
    
    # Show recommendations
    if result['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in result['recommendations']:
            print(f"   📝 {rec}")


def print_summary_report(results: list):
    """Print summary report for multiple results."""
    if not results:
        return
    
    total_posts = len(results)
    posts_with_images = sum(1 for r in results if r['total_images'] > 0)
    posts_without_images = total_posts - posts_with_images
    total_issues = sum(len(r['issues']) for r in results)
    avg_score = sum(r['score']['percentage'] for r in results) / total_posts
    
    print_section("SUMMARY REPORT")
    print(f"📊 Posts analyzed: {total_posts}")
    print(f"🖼️ Posts with images: {posts_with_images}")
    print(f"❌ Posts without images: {posts_without_images}")
    print(f"🚨 Total issues found: {total_issues}")
    print(f"📈 Average image score: {avg_score:.1f}%")
    
    # Posts needing attention
    problem_posts = [r for r in results if r['issues'] or r['needs_images']]
    if problem_posts:
        print(f"\n⚠️ POSTS NEEDING ATTENTION ({len(problem_posts)}):")
        for result in problem_posts[:10]:  # Show first 10
            print(f"   📄 {result['title'][:50]}...")
            if result['needs_images']:
                print(f"      ❌ No images")
            for issue in result['issues'][:2]:  # Show first 2 issues
                print(f"      ⚠️ {issue}")


def save_image_report(results: list, filename: str):
    """Save image validation report to file."""
    try:
        with open(filename, 'w') as f:
            f.write("IMAGE VALIDATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            total_posts = len(results)
            posts_with_images = sum(1 for r in results if r['total_images'] > 0)
            avg_score = sum(r['score']['percentage'] for r in results) / total_posts
            
            f.write(f"Total posts analyzed: {total_posts}\n")
            f.write(f"Posts with images: {posts_with_images}\n")
            f.write(f"Average image score: {avg_score:.1f}%\n\n")
            
            # Individual results
            for i, result in enumerate(results, 1):
                f.write(f"{i}. {result['title']}\n")
                f.write(f"   Images: {result['total_images']}\n")
                f.write(f"   Score: {result['score']['percentage']:.1f}%\n")
                if result['issues']:
                    f.write(f"   Issues: {len(result['issues'])}\n")
                    for issue in result['issues']:
                        f.write(f"     - {issue}\n")
                f.write("\n")
        
        print(f"💾 Report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving report: {e}")


if __name__ == "__main__":
    sys.exit(main())