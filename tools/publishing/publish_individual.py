#!/usr/bin/env python3
"""
Individual Post Publishing CLI
==============================
Command-line interface for publishing individual posts with comprehensive validation.
"""

import argparse
import sys
import os
import json
import getpass
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from master_toolkit.content.individual_publisher import IndividualPostPublisher
from master_toolkit.core import create_client, WordPressAPIError
from master_toolkit.utils import print_header, print_success, print_error


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Individual Post Publishing & Validation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Publish a single post with validation
  python -m master_toolkit.cli.individual_publish publish_content/cli/publish_individual.py published_content/week3/entertainment/ai-virtual-influencers-2025.md --category entertainment --focus-keyword "AI virtual influencers"

  # Validate an existing post
  python -m master_toolkit.cli.individual_publish validate 3019 --focus-keyword "AI virtual influencers"

  # Dry run publishing
  python -m master_toolkit.cli.individual_publish publish_content/cli/publish_individual.py published_content/week3/entertainment/ai-virtual-influencers-2025.md --dry-run
        """
    )

    parser.add_argument('--username', '-u', help='WordPress username')
    parser.add_argument('--password', '-p', help='WordPress application password')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Publish command
    publish_parser = subparsers.add_parser(
        'publish',
        help='Publish a single markdown file with comprehensive validation'
    )
    publish_parser.add_argument('file', help='Path to markdown file')
    publish_parser.add_argument('--category', '-c', help='Post category')
    publish_parser.add_argument('--status', '-s', default='publish', help='Post status')
    publish_parser.add_argument('--apply-fixes', action='store_true', help='Apply SEO fixes after publishing')
    publish_parser.add_argument('--focus-keyword', '-k', help='Focus keyword for SEO analysis')

    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate an existing post'
    )
    validate_parser.add_argument('post_id', type=int, help='Post ID to validate')
    validate_parser.add_argument('--focus-keyword', '-k', help='Focus keyword for SEO analysis')

    # SEO audit command
    seo_parser = subparsers.add_parser(
        'seo_audit',
        help='Run SEO audit on a markdown file, directory of files, or an existing post ID'
    )
    group = seo_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', help='Path to a markdown file to audit')
    group.add_argument('--dir', '-d', help='Directory containing markdown files to audit')
    group.add_argument('--post', '-p', type=int, help='Existing WordPress post ID to audit')
    seo_parser.add_argument('--focus-keyword', '-k', help='Focus keyword for SEO analysis')
    seo_parser.add_argument('--out', '-o', help='Write JSON report to file (defaults to stdout)')
    seo_parser.add_argument('--apply-fixes', action='store_true', help='Apply safe SEO fixes (use with care)')

    args = parser.parse_args()

    # Always prompt interactively when running publish (force interactive)
    if args.command == 'publish':
        try:
            args.username = input('WordPress username: ').strip()
            args.password = getpass.getpass('WordPress application password (application password — not primary login password): ')
            args.status = input(f'Post status [publish/draft] (default: {getattr(args, "status", "publish")}): ').strip() or getattr(args, 'status', 'publish')
            resp = input('Apply SEO fixes after publishing? (y/N): ').strip().lower()
            args.apply_fixes = resp in ('y', 'yes')
        except KeyboardInterrupt:
            print('\nOperation cancelled by user')
            return 1

    if not args.command:
        parser.print_help()
        return 1

    try:
        # Create and authenticate client
        client = create_client()
        if not client.authenticate(args.username, args.password):
            print_error("Authentication failed. Please check credentials.")
            return 1

        # Initialize publisher
        publisher = IndividualPostPublisher(client)

        # Execute command
        if args.command == 'publish':
            return publish_post(publisher, args)
        elif args.command == 'validate':
            return validate_post(publisher, args)
        elif args.command == 'seo_audit':
            return seo_audit_cmd(publisher, args)

    except WordPressAPIError as e:
        print_error(f"WordPress API error: {e}")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


def publish_post(publisher, args):
    """Publish a single post with validation."""
    result = publisher.publish_and_validate(
        file_path=args.file,
        category=args.category,
        status=args.status,
        focus_keyword=args.focus_keyword,
        dry_run=args.dry_run
    )

    if result['success']:
        if args.dry_run:
            print_success("✅ Dry run completed successfully!")
        else:
            print_success("✅ Post published and validated successfully!")

            # Show validation summary
            if 'post_validation' in result['steps']:
                validation = result['steps']['post_validation']
                score = validation.get('percentage', 0)
                print(f"📊 Final Quality Score: {score}%")

                issues_count = len(validation.get('issues', []))
                warnings_count = len(validation.get('warnings', []))

                if issues_count > 0:
                    print(f"❌ Issues: {issues_count}")
                if warnings_count > 0:
                    print(f"⚠️ Warnings: {warnings_count}")

        return 0
    else:
        print_error(f"❌ Publishing failed: {result.get('error', 'Unknown error')}")
        return 1


def validate_post(publisher, args):
    """Validate an existing post."""
    result = publisher.validate_existing_post(
        post_id=args.post_id,
        focus_keyword=args.focus_keyword
    )

    if result['success']:
        validation = result['validation']
        score = validation.get('percentage', 0)

        if score >= 90:
            print_success("🎉 Excellent quality post!")
        elif score >= 80:
            print_success("✅ Very good quality post!")
        elif score >= 70:
            print("👍 Good quality with minor improvements possible")
        else:
            print_error("⚠️ Quality improvements needed")

        return 0
    else:
        print_error(f"❌ Validation failed: {result.get('error', 'Unknown error')}")
        return 1


def _audit_markdown_file(publisher, file_path: str, focus_keyword: str = None) -> dict:
    """Run an SEO-style audit on a markdown file (no WP publish)."""
    # Parse file into HTML using ContentPublisher
    parsed = publisher.publisher.parse_markdown_file(file_path)
    front = parsed.get('front_matter', {})
    html = parsed.get('html_content', '')

    report = {
        'file': file_path,
        'title': front.get('title') or '',
        'slug': front.get('slug') or publisher._slugify(front.get('title', Path(file_path).stem)),
        'seo': {},
        'content_checks': {},
        'link_checks': {},
        'image_checks': {}
    }

    # Use the SEOValidator for title/slug/content checks
    seo_validator = publisher.validator.seo_validator
    report['seo']['title'] = seo_validator.validate_title(report['title'])
    report['seo']['slug'] = seo_validator.validate_slug(report['slug'])
    report['seo']['content'] = seo_validator.validate_content(html)

    # Use IndividualPostValidator methods for link/image checks
    ipv = publisher.validator
    try:
        report['link_checks']['internal_links'] = ipv._validate_internal_links(html, '')
        report['link_checks']['broken_links'] = ipv._validate_broken_links(html)
    except Exception as e:
        report['link_checks']['error'] = str(e)

    try:
        report['image_checks']['missing_images'] = ipv._validate_missing_images(html)
    except Exception as e:
        report['image_checks']['error'] = str(e)

    # Content quality
    try:
        report['content_checks']['quality'] = ipv._validate_content_quality(html)
    except Exception as e:
        report['content_checks']['error'] = str(e)

    # Featured image candidate and quick validation
    try:
        candidate = publisher.publisher._get_featured_image(front.get('category', None) or front.get('category', ''), front)
        report['image_checks']['candidate'] = candidate

        # Quick dimension check
        try:
            import requests
            from io import BytesIO
            from PIL import Image
            resp = requests.get(candidate, timeout=6)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content))
                report['image_checks']['dimensions'] = img.size
            else:
                report['image_checks']['dimensions'] = None
        except Exception as e:
            report['image_checks']['dimensions_error'] = str(e)
    except Exception as e:
        report['image_checks']['candidate_error'] = str(e)

    # Focus keyword checks (optional)
    if focus_keyword:
        try:
            fk = ipv._validate_focus_keyword(report['title'], html, '', focus_keyword)
            report['seo']['focus_keyword'] = fk
        except Exception as e:
            report['seo']['focus_keyword_error'] = str(e)

    return report


def seo_audit_cmd(publisher, args):
    """Handler for seo_audit subcommand."""
    out_path = args.out
    focus_keyword = args.focus_keyword
    apply_fixes = getattr(args, 'apply_fixes', False)
    apply_fixes = getattr(args, 'apply_fixes', False)

    results = None

    # Audit existing post by ID
    if getattr(args, 'post', None):
        post_id = args.post
        val = publisher.validate_existing_post(post_id, focus_keyword)
        if not val.get('success'):
            print_error(f"SEO audit failed for post {post_id}: {val.get('error')}")
            return 1
        results = {'type': 'post', 'post_id': post_id, 'validation': val['validation']}

        # Plan fixes using SEOValidator methods (dry-run), then apply if requested
        seo = publisher.validator.seo_validator
        fix_plan = {}
        try:
            # Plan: meta description
            plan_meta = seo.add_meta_description(post_id, dry_run=True)
            fix_plan['meta_description'] = plan_meta

            # Plan: social meta
            plan_social = seo.add_social_meta_tags(post_id, dry_run=True)
            fix_plan['social_meta'] = plan_social

            # Plan: schema
            plan_schema = seo.add_schema_markup(post_id, dry_run=True)
            fix_plan['schema'] = plan_schema

            # Plan: optimize title/slug
            plan_opt = seo.optimize_post_seo(post_id, dry_run=True)
            fix_plan['optimize'] = plan_opt

        except Exception as e:
            fix_plan['error'] = str(e)

        results['fix_plan'] = fix_plan

        if apply_fixes:
            apply_results = {}
            try:
                apply_results['meta_description'] = seo.add_meta_description(post_id, dry_run=False)
                apply_results['social_meta'] = seo.add_social_meta_tags(post_id, dry_run=False)
                apply_results['schema'] = seo.add_schema_markup(post_id, dry_run=False)
                apply_results['optimize'] = seo.optimize_post_seo(post_id, dry_run=False)
            except Exception as e:
                apply_results['error'] = str(e)

            results['applied_fixes'] = apply_results

        # Optionally apply safe fixes to the existing post
        if apply_fixes:
            seo = publisher.validator.seo_validator
            fixes = {}
            try:
                # Add/normalize meta description
                fixes['meta_description'] = seo.add_meta_description(post_id, dry_run=not apply_fixes)
            except Exception as e:
                fixes['meta_description'] = {'error': str(e)}

            try:
                fixes['social_meta'] = seo.add_social_meta_tags(post_id, dry_run=not apply_fixes)
            except Exception as e:
                fixes['social_meta'] = {'error': str(e)}

            try:
                fixes['schema'] = seo.add_schema_markup(post_id, dry_run=not apply_fixes)
            except Exception as e:
                fixes['schema'] = {'error': str(e)}

            try:
                fixes['optimize_seo'] = seo.optimize_post_seo(post_id, dry_run=not apply_fixes)
            except Exception as e:
                fixes['optimize_seo'] = {'error': str(e)}

            results['fixes'] = fixes

    # Audit single markdown file
    elif getattr(args, 'file', None):
        file_path = args.file
        if not Path(file_path).exists():
            print_error(f"File not found: {file_path}")
            return 1
        report = _audit_markdown_file(publisher, file_path, focus_keyword)
        results = {'type': 'file', 'file': file_path, 'report': report}

        # Generate proposed fixes for front-matter (title, slug, meta description)
        try:
            seo = publisher.validator.seo_validator
            pub = publisher.publisher

            current_title = report['title'] or ''
            current_slug = report['slug'] or ''
            optimized_title = seo._optimize_title(current_title)
            optimized_slug = seo._optimize_slug(current_slug)
            generated_meta = pub._generate_meta_description(report.get('report', {}).get('html_content', report.get('file', '')) if False else pub._generate_meta_description(report.get('report', {}).get('html_content', '')))
            # The above line attempts to be defensive; we'll derive meta from parsed file instead
        except Exception:
            # Fallback: compute using available helpers
            optimized_title = publisher.validator.seo_validator._optimize_title(report['title'])
            optimized_slug = publisher.validator.seo_validator._optimize_slug(report['slug'])
            generated_meta = publisher.publisher._generate_meta_description(publisher.publisher.parse_markdown_file(file_path)['html_content'])

        fix_plan = {
            'optimized_title': optimized_title,
            'optimized_slug': optimized_slug,
            'generated_meta_description': generated_meta
        }

        results['fix_plan'] = fix_plan

        # Apply fixes to markdown front-matter if requested
        if apply_fixes:
            try:
                import yaml
                from datetime import datetime

                # Read original file and parse front matter
                with open(file_path, 'r', encoding='utf-8') as fh:
                    content = fh.read()

                fm = {}
                md = content
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        import yaml
                        fm = yaml.safe_load(parts[1]) or {}
                        md = parts[2]

                # Update front matter keys
                if optimized_title:
                    fm['title'] = optimized_title
                if optimized_slug:
                    fm['slug'] = optimized_slug
                if generated_meta:
                    # store as excerpt or meta field
                    fm['excerpt'] = fm.get('excerpt') or generated_meta

                # Backup original file
                backup_path = file_path + f'.bak.{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
                with open(backup_path, 'w', encoding='utf-8') as bf:
                    bf.write(content)

                # Write updated file
                with open(file_path, 'w', encoding='utf-8') as fh:
                    fh.write('---\n')
                    yaml.safe_dump(fm, fh, sort_keys=False, allow_unicode=True)
                    fh.write('---\n')
                    fh.write(md.lstrip('\n'))

                results['applied_fixes'] = {'backup': backup_path, 'updated_file': file_path}
            except Exception as e:
                results.setdefault('applied_fixes', {})
                results['applied_fixes']['error'] = str(e)

        # Optionally apply fixes to the markdown file (update front matter)
        if apply_fixes:
            try:
                import yaml
                parsed = publisher.publisher.parse_markdown_file(file_path)
                front = parsed.get('front_matter', {}) or {}
                raw = parsed.get('raw_content', '')

                seo = publisher.validator.seo_validator
                # Compute optimized values
                optimized_title = seo._optimize_title(report.get('title', ''))
                optimized_slug = seo._optimize_slug(report.get('slug', publisher._slugify(report.get('title', Path(file_path).stem))))
                optimized_excerpt = publisher.publisher._generate_meta_description(parsed.get('html_content', ''))

                # Apply to front matter
                if optimized_title:
                    front['title'] = optimized_title
                if optimized_slug:
                    front['slug'] = optimized_slug
                if optimized_excerpt:
                    front['excerpt'] = optimized_excerpt

                # Write back front matter + raw markdown
                fm = yaml.safe_dump(front, sort_keys=False, allow_unicode=True)
                new_content = '---\n' + fm + '---\n\n' + raw
                with open(file_path, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)

                results['file_fix'] = {
                    'applied': True,
                    'changes': {
                        'title': optimized_title,
                        'slug': optimized_slug,
                        'excerpt': optimized_excerpt
                    }
                }
            except Exception as e:
                results['file_fix'] = {'applied': False, 'error': str(e)}

    # Audit directory of markdown files
    elif getattr(args, 'dir', None):
        dir_path = Path(args.dir)
        if not dir_path.exists() or not dir_path.is_dir():
            print_error(f"Directory not found: {dir_path}")
            return 1

        reports = []
        for md in sorted(dir_path.glob('*.md')):
            try:
                reports.append(_audit_markdown_file(publisher, str(md), focus_keyword))
            except Exception as e:
                reports.append({'file': str(md), 'error': str(e)})

        results = {'type': 'directory', 'directory': str(dir_path), 'reports': reports}

    # Output results
    if out_path:
        try:
            with open(out_path, 'w', encoding='utf-8') as fh:
                json.dump(results, fh, indent=2)
            print_success(f"SEO audit written to {out_path}")
            return 0
        except Exception as e:
            print_error(f"Failed to write output: {e}")
            return 1
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0


if __name__ == '__main__':
    sys.exit(main())