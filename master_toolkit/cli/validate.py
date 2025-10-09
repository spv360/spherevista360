#!/usr/bin/env python3
"""
WordPress Validation CLI
========================
Command-line interface for WordPress content validation and fixing.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from wordpress_toolkit.core import create_client, WordPressAPIError
from wordpress_toolkit.validation import ComprehensiveValidator, LinkValidator, SEOValidator, ImageValidator
from wordpress_toolkit.utils import print_header, print_error, print_success


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='WordPress Content Validation Tool')
    parser.add_argument('--username', '-u', help='WordPress username')
    parser.add_argument('--password', '-p', help='WordPress application password')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate post(s)')
    validate_parser.add_argument('--post-id', type=int, help='Specific post ID to validate')
    validate_parser.add_argument('--all', action='store_true', help='Validate all posts')
    validate_parser.add_argument('--limit', type=int, default=10, help='Number of posts to validate')
    
    # Fix command
    fix_parser = subparsers.add_parser('fix', help='Fix issues in post(s)')
    fix_parser.add_argument('--post-id', type=int, help='Specific post ID to fix')
    fix_parser.add_argument('--all', action='store_true', help='Fix all posts with issues')
    fix_parser.add_argument('--links-only', action='store_true', help='Fix only broken links')
    fix_parser.add_argument('--seo-only', action='store_true', help='Fix only SEO issues')
    fix_parser.add_argument('--images-only', action='store_true', help='Fix only image issues')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Complete quality audit')
    audit_parser.add_argument('--limit', type=int, default=20, help='Number of posts to audit')
    audit_parser.add_argument('--report', action='store_true', help='Generate detailed report')
    
    # Links command
    links_parser = subparsers.add_parser('links', help='Link-specific operations')
    links_parser.add_argument('--check', action='store_true', help='Check for broken links')
    links_parser.add_argument('--fix', action='store_true', help='Fix broken links')
    links_parser.add_argument('--verify', action='store_true', help='Verify previous fixes')
    links_parser.add_argument('--post-id', type=int, help='Specific post ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Create and authenticate client
        client = create_client()
        
        if not client.authenticate(args.username, args.password):
            print_error("Authentication failed. Please check credentials.")
            return 1
        
        # Execute command
        if args.command == 'validate':
            return validate_content(client, args)
        elif args.command == 'fix':
            return fix_content(client, args)
        elif args.command == 'audit':
            return audit_content(client, args)
        elif args.command == 'links':
            return handle_links(client, args)
        
    except WordPressAPIError as e:
        print_error(f"WordPress API error: {e}")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


def validate_content(client, args):
    """Validate content."""
    validator = ComprehensiveValidator(client)
    
    if args.post_id:
        # Validate single post
        result = validator.validate_post_comprehensive(args.post_id)
        
        if 'error' in result:
            print_error(f"Validation failed: {result['error']}")
            return 1
        
        print_header(f"Validation Result for Post {args.post_id}")
        print(f"📊 Overall Score: {result['overall_score']}%")
        print(f"📝 SEO Score: {result['summary']['seo_score']}%")
        print(f"🔗 Links Score: {result['summary']['link_score']}%")
        print(f"🖼️ Images Score: {result['summary']['image_score']}%")
        
        if result['summary']['total_issues'] > 0:
            print(f"⚠️ Issues found: {result['summary']['total_issues']}")
        else:
            print_success("No issues found!")
        
    else:
        # Validate multiple posts
        limit = args.limit if not args.all else 100
        result = validator.validate_multiple_posts(per_page=limit)
        
        if 'error' in result:
            print_error(f"Validation failed: {result['error']}")
            return 1
        
        print_header("Validation Summary")
        print(f"📊 Posts validated: {result['validated_posts']}")
        print(f"📈 Average score: {result['average_score']}%")
        print(f"⚠️ Posts needing attention: {result['posts_needing_attention']}")
    
    return 0


def fix_content(client, args):
    """Fix content issues."""
    validator = ComprehensiveValidator(client)
    
    if args.post_id:
        post_ids = [args.post_id]
    else:
        post_ids = None  # Will auto-detect problematic posts
    
    # Apply specific fixes
    if args.links_only:
        link_validator = LinkValidator(client)
        result = link_validator.fix_all_broken_links(post_ids, args.dry_run)
    elif args.seo_only:
        seo_validator = SEOValidator(client)
        if args.post_id:
            result = seo_validator.optimize_post_seo(args.post_id, args.dry_run)
        else:
            print_error("SEO-only fixes require a specific post ID")
            return 1
    elif args.images_only:
        image_validator = ImageValidator(client)
        if args.post_id:
            result = image_validator.optimize_post_images(args.post_id, dry_run=args.dry_run)
        else:
            print_error("Image-only fixes require a specific post ID")
            return 1
    else:
        # Comprehensive fixes
        result = validator.fix_all_issues(post_ids, args.dry_run)
    
    if 'error' in result:
        print_error(f"Fixing failed: {result['error']}")
        return 1
    
    mode = "DRY RUN" if args.dry_run else "APPLIED"
    fixes = result.get('total_fixes', 0)
    print_success(f"{mode}: {fixes} fixes processed")
    
    return 0


def audit_content(client, args):
    """Perform quality audit."""
    validator = ComprehensiveValidator(client)
    
    print_header("Quality Audit")
    result = validator.quality_audit_workflow()
    
    if not result['success']:
        print_error(f"Audit failed: {result.get('error', 'Unknown error')}")
        return 1
    
    # Show improvement
    if 'improvement' in result:
        improvement = result['improvement']
        print_success(f"Audit completed!")
        print(f"📈 Score improvement: {improvement['initial_score']}% → {improvement['final_score']}%")
        print(f"🔧 Posts fixed: {improvement['posts_fixed']}")
        print(f"✅ Total fixes: {improvement['total_fixes']}")
    
    # Generate report if requested
    if args.report:
        report = validator.generate_quality_report()
        report_file = f"quality_report_{validator._get_timestamp().replace(':', '-')}.txt"
        
        with open(report_file, 'w') as f:
            f.write(report)
        
        print_success(f"Report saved: {report_file}")
    
    return 0


def handle_links(client, args):
    """Handle link operations."""
    link_validator = LinkValidator(client)
    
    if args.verify:
        result = link_validator.verify_fixes()
        
        print_header("Link Fix Verification")
        print(f"📊 Posts checked: {result['posts_checked']}")
        print(f"✅ Posts clean: {result['posts_clean']}")
        print(f"⚠️ Remaining broken links: {result['remaining_broken_links']}")
        
        if result['remaining_broken_links'] == 0:
            print_success("All broken links have been fixed!")
        
    elif args.check:
        if args.post_id:
            result = link_validator.validate_post_links(args.post_id)
            
            if 'error' in result:
                print_error(f"Check failed: {result['error']}")
                return 1
            
            print_header(f"Link Check for Post {args.post_id}")
            print(f"🔗 Total links: {result['total_links']}")
            print(f"✅ Valid links: {len(result['valid_links'])}")
            print(f"❌ Broken links: {len(result['broken_links'])}")
            
            if result['broken_links']:
                print("\nBroken links found:")
                for link in result['broken_links']:
                    print(f"  • {link}")
        else:
            print_error("Link check requires a post ID")
            return 1
    
    elif args.fix:
        post_ids = [args.post_id] if args.post_id else None
        result = link_validator.fix_all_broken_links(post_ids, dry_run=False)
        
        print_success(f"Fixed {result.get('total_fixes', 0)} broken links")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())