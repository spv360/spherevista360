#!/usr/bin/env python3
"""
Link Validation Tool
===================
Command-line tool for WordPress link validation and menu checking.
"""

import sys
import argparse
from pathlib import Path

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))

from wp_client import WordPressClient, print_header, print_section
from link_validator import LinkValidator, validate_post_links, validate_site_menu


def main():
    """Main CLI interface for link validation."""
    parser = argparse.ArgumentParser(description='WordPress Link Validation Tool')
    parser.add_argument('--post-id', type=int, help='Validate links in specific post')
    parser.add_argument('--page-id', type=int, help='Validate links in specific page')
    parser.add_argument('--menu', action='store_true', help='Validate menu structure')
    parser.add_argument('--site-scan', action='store_true', help='Scan entire site for broken links')
    parser.add_argument('--max-pages', type=int, default=10, help='Max pages to scan for site-scan')
    parser.add_argument('--report', type=str, help='Save report to file')
    parser.add_argument('--username', type=str, help='WordPress username')
    parser.add_argument('--password', type=str, help='WordPress application password')
    
    args = parser.parse_args()
    
    print_header("LINK VALIDATION TOOL")
    
    # Initialize WordPress client
    wp_client = WordPressClient()
    if not wp_client.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    validator = LinkValidator(wp_client)
    
    if args.post_id:
        # Validate specific post
        print_section(f"VALIDATING POST ID: {args.post_id}")
        try:
            result = validate_post_links(wp_client, args.post_id)
            print_link_result(result)
            
            if args.report:
                save_link_report([result], args.report, 'post')
                
        except Exception as e:
            print(f"❌ Error validating post {args.post_id}: {e}")
            return 1
    
    elif args.page_id:
        # Validate specific page
        print_section(f"VALIDATING PAGE ID: {args.page_id}")
        try:
            page = wp_client.get_page(args.page_id)
            content = wp_client.get_page_content(page['link'])
            result = validator.validate_page_links(content, page['link'])
            result['page_title'] = page['title']['rendered']
            result['page_url'] = page['link']
            print_link_result(result)
            
            if args.report:
                save_link_report([result], args.report, 'page')
                
        except Exception as e:
            print(f"❌ Error validating page {args.page_id}: {e}")
            return 1
    
    elif args.menu:
        # Validate menu structure
        print_section("VALIDATING MENU STRUCTURE")
        result = validate_site_menu(wp_client)
        
        if 'error' in result:
            print(f"❌ {result['error']}")
            return 1
        
        print_menu_result(result)
        
        if args.report:
            save_menu_report(result, args.report)
    
    elif args.site_scan:
        # Scan entire site
        print_section(f"SCANNING SITE FOR BROKEN LINKS (Max {args.max_pages} pages)")
        result = validator.scan_site_for_broken_links(args.max_pages)
        
        if 'error' in result:
            print(f"❌ {result['error']}")
            return 1
        
        print_site_scan_result(result)
        
        if args.report:
            save_site_scan_report(result, args.report)
    
    else:
        print("❌ Please specify --post-id, --page-id, --menu, or --site-scan")
        return 1
    
    return 0


def print_link_result(result: dict):
    """Print detailed link validation result."""
    title = result.get('post_title') or result.get('page_title', 'Unknown')
    url = result.get('post_url') or result.get('page_url', '')
    
    print(f"\n📄 Title: {title}")
    print(f"🌐 URL: {url}")
    
    summary = result['validation_summary']
    print(f"\n📊 Link Summary:")
    print(f"   Total links: {result['total_links']}")
    print(f"   Tested links: {summary['total_tested']}")
    print(f"   Working: {summary['working_count']} ✅")
    print(f"   Broken: {summary['broken_count']} ❌")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    
    print(f"\n🔗 Link Types:")
    print(f"   Internal: {summary['internal_count']}")
    print(f"   External: {summary['external_count']}")
    print(f"   Email: {summary['email_count']}")
    print(f"   Anchor: {summary['anchor_count']}")
    
    # Show broken links
    if result['broken_links']:
        print(f"\n🚨 BROKEN LINKS ({len(result['broken_links'])}):")
        for i, link in enumerate(result['broken_links'], 1):
            print(f"   {i}. {link['text'][:30]}...")
            print(f"      URL: {link['url']}")
            print(f"      Error: {link['error']} (Status: {link['status_code']})")
    else:
        print("\n✅ No broken links found!")


def print_menu_result(result: dict):
    """Print menu validation result."""
    print(f"\n🍔 Menu Analysis:")
    print(f"   Menus found: {result['menus_found']}")
    
    summary = result['menu_summary']
    print(f"   Total menu links: {summary['total_menu_links']}")
    print(f"   Working links: {summary['working_menu_links']} ✅")
    print(f"   Broken links: {summary['broken_menu_links']} ❌")
    print(f"   Success rate: {summary['menu_success_rate']:.1f}%")
    
    # Show duplicates
    if result['duplicate_links']:
        print(f"\n🔄 DUPLICATE MENU LINKS ({len(result['duplicate_links'])}):")
        for dup in result['duplicate_links']:
            print(f"   🔗 {dup['url']} (appears {dup['count']} times)")
    
    # Show broken menu links
    if result['broken_menu_links']:
        print(f"\n🚨 BROKEN MENU LINKS ({len(result['broken_menu_links'])}):")
        for link in result['broken_menu_links']:
            print(f"   ❌ {link['text']} → {link['url']}")
            print(f"      Menu: {link['menu_index']}, Error: {link['error']}")
    else:
        print("\n✅ All menu links are working!")
    
    # Show menu details
    print(f"\n📋 MENU DETAILS:")
    for menu in result['menu_data']:
        working = sum(1 for link in menu['links'] if link['is_working'])
        print(f"   Menu {menu['menu_index']}: {working}/{menu['link_count']} links working")


def print_site_scan_result(result: dict):
    """Print site scan result."""
    summary = result['summary']
    
    print(f"\n🔍 Site Scan Results:")
    print(f"   Pages scanned: {summary['pages_scanned']}")
    print(f"   Pages with issues: {summary['pages_with_issues']}")
    print(f"   Total broken links: {summary['total_broken_links']}")
    print(f"   Site health score: {summary['health_score']:.1f}%")
    
    # Show pages with issues
    if result['pages_with_issues']:
        print(f"\n⚠️ PAGES WITH BROKEN LINKS:")
        for page in result['pages_with_issues']:
            print(f"   📄 {page['title'][:40]}...")
            print(f"      Type: {page['type']}, Broken links: {page['broken_count']}")
            print(f"      URL: {page['url']}")
    
    # Show broken links summary
    if result['broken_links']:
        print(f"\n🚨 BROKEN LINKS SUMMARY (First 10):")
        for i, link in enumerate(result['broken_links'][:10], 1):
            print(f"   {i}. {link['text'][:30]}...")
            print(f"      URL: {link['url']}")
            print(f"      Source: {link['source_page'][:30]}...")
            print(f"      Error: {link['error']}")
    else:
        print("\n✅ No broken links found on scanned pages!")


def save_link_report(results: list, filename: str, content_type: str):
    """Save link validation report to file."""
    try:
        with open(filename, 'w') as f:
            f.write(f"LINK VALIDATION REPORT - {content_type.upper()}\n")
            f.write("=" * 50 + "\n\n")
            
            for result in results:
                title = result.get(f'{content_type}_title', 'Unknown')
                url = result.get(f'{content_type}_url', '')
                
                f.write(f"Title: {title}\n")
                f.write(f"URL: {url}\n")
                
                summary = result['validation_summary']
                f.write(f"Total links: {result['total_links']}\n")
                f.write(f"Working: {summary['working_count']}\n")
                f.write(f"Broken: {summary['broken_count']}\n")
                f.write(f"Success rate: {summary['success_rate']:.1f}%\n\n")
                
                if result['broken_links']:
                    f.write("BROKEN LINKS:\n")
                    for link in result['broken_links']:
                        f.write(f"  - {link['text']} → {link['url']}\n")
                        f.write(f"    Error: {link['error']} (Status: {link['status_code']})\n")
                f.write("\n" + "-" * 50 + "\n\n")
        
        print(f"💾 Report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving report: {e}")


def save_menu_report(result: dict, filename: str):
    """Save menu validation report to file."""
    try:
        with open(filename, 'w') as f:
            f.write("MENU VALIDATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            summary = result['menu_summary']
            f.write(f"Menus found: {result['menus_found']}\n")
            f.write(f"Total menu links: {summary['total_menu_links']}\n")
            f.write(f"Working links: {summary['working_menu_links']}\n")
            f.write(f"Broken links: {summary['broken_menu_links']}\n")
            f.write(f"Success rate: {summary['menu_success_rate']:.1f}%\n\n")
            
            if result['duplicate_links']:
                f.write("DUPLICATE LINKS:\n")
                for dup in result['duplicate_links']:
                    f.write(f"  - {dup['url']} (appears {dup['count']} times)\n")
                f.write("\n")
            
            if result['broken_menu_links']:
                f.write("BROKEN MENU LINKS:\n")
                for link in result['broken_menu_links']:
                    f.write(f"  - {link['text']} → {link['url']}\n")
                    f.write(f"    Menu: {link['menu_index']}, Error: {link['error']}\n")
        
        print(f"💾 Menu report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving menu report: {e}")


def save_site_scan_report(result: dict, filename: str):
    """Save site scan report to file."""
    try:
        with open(filename, 'w') as f:
            f.write("SITE SCAN REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            summary = result['summary']
            f.write(f"Pages scanned: {summary['pages_scanned']}\n")
            f.write(f"Pages with issues: {summary['pages_with_issues']}\n")
            f.write(f"Total broken links: {summary['total_broken_links']}\n")
            f.write(f"Site health score: {summary['health_score']:.1f}%\n\n")
            
            if result['pages_with_issues']:
                f.write("PAGES WITH ISSUES:\n")
                for page in result['pages_with_issues']:
                    f.write(f"  - {page['title']}\n")
                    f.write(f"    URL: {page['url']}\n")
                    f.write(f"    Type: {page['type']}, Broken links: {page['broken_count']}\n\n")
            
            if result['broken_links']:
                f.write("ALL BROKEN LINKS:\n")
                for link in result['broken_links']:
                    f.write(f"  - {link['text']} → {link['url']}\n")
                    f.write(f"    Source: {link['source_page']}\n")
                    f.write(f"    Error: {link['error']}\n\n")
        
        print(f"💾 Site scan report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving site scan report: {e}")


if __name__ == "__main__":
    sys.exit(main())