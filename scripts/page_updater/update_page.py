#!/usr/bin/env python3
"""
WordPress Page Updater Tool
Generic tool to update any WordPress page with content from HTML file

Usage:
    python update_page.py <page_id> <content_file>
    python update_page.py --slug <page_slug> <content_file>
    python update_page.py --create <title> <content_file> [--slug <slug>]

Examples:
    python update_page.py 2412 ../content/homepage.html
    python update_page.py --slug newsletter ../content/newsletter.html
    python update_page.py --create "New Page" ../content/new_page.html --slug new-page
"""
import sys
import os
import argparse

# Add wordpress_core directory to path to import wordpress_utils
script_dir = os.path.dirname(os.path.abspath(__file__))
wordpress_core_path = os.path.join(os.path.dirname(script_dir), 'wordpress_core')
sys.path.insert(0, wordpress_core_path)
from wordpress_utils import WordPressAPI, read_content_file, print_success, print_error, print_info


def update_page_by_id(page_id: int, content_file: str, title: str = None):
    """Update page by ID"""
    print_info(f"Reading content from: {content_file}")
    content = read_content_file(content_file)
    
    if not content:
        print_error("No content to update")
        return False
    
    api = WordPressAPI()
    print_info(f"Updating page ID: {page_id}")
    
    if api.update_page(page_id, content, title):
        print_success(f"Page updated successfully!")
        page = api.get_page(page_id)
        if page:
            print_info(f"View at: {page['link']}")
        return True
    else:
        print_error("Failed to update page")
        return False


def update_page_by_slug(slug: str, content_file: str, title: str = None):
    """Update page by slug"""
    api = WordPressAPI()
    print_info(f"Searching for page with slug: {slug}")
    
    page = api.find_page_by_slug(slug)
    if not page:
        print_error(f"Page not found with slug: {slug}")
        return False
    
    print_info(f"Found page: {page['title']['rendered']} (ID: {page['id']})")
    return update_page_by_id(page['id'], content_file, title)


def create_page(title: str, content_file: str, slug: str = None):
    """Create new page"""
    print_info(f"Reading content from: {content_file}")
    content = read_content_file(content_file)
    
    if not content:
        print_error("No content to create page")
        return False
    
    api = WordPressAPI()
    print_info(f"Creating new page: {title}")
    
    page_id = api.create_page(title, content, slug)
    if page_id:
        print_success(f"Page created successfully! (ID: {page_id})")
        page = api.get_page(page_id)
        if page:
            print_info(f"View at: {page['link']}")
        return True
    else:
        print_error("Failed to create page")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Update or create WordPress pages from HTML content files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Update page by ID:
    %(prog)s 2412 ../content/homepage.html
  
  Update page by slug:
    %(prog)s --slug newsletter ../content/newsletter.html
  
  Create new page:
    %(prog)s --create "New Page" ../content/new_page.html --slug new-page
  
  Update with new title:
    %(prog)s 2412 ../content/homepage.html --title "New Homepage Title"
        """
    )
    
    parser.add_argument('page_id_or_content', nargs='?', help='Page ID or content file (depends on mode)')
    parser.add_argument('content_file', nargs='?', help='Content file path')
    parser.add_argument('--slug', help='Page slug (for finding or creating pages)')
    parser.add_argument('--create', metavar='TITLE', help='Create new page with this title')
    parser.add_argument('--title', help='Update page title')
    
    args = parser.parse_args()
    
    # Handle different modes
    if args.create:
        # Create mode: --create "Title" content_file.html --slug slug
        if not args.page_id_or_content:
            parser.error("Content file required when using --create")
        success = create_page(args.create, args.page_id_or_content, args.slug)
    
    elif args.slug:
        # Slug mode: --slug page-slug content_file.html
        if not args.page_id_or_content:
            parser.error("Content file required when using --slug")
        success = update_page_by_slug(args.slug, args.page_id_or_content, args.title)
    
    else:
        # ID mode: page_id content_file.html
        if not args.page_id_or_content or not args.content_file:
            parser.error("Both page_id and content_file are required")
        try:
            page_id = int(args.page_id_or_content)
            success = update_page_by_id(page_id, args.content_file, args.title)
        except ValueError:
            parser.error(f"Invalid page ID: {args.page_id_or_content}")
            success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
