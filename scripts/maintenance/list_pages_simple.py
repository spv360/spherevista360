#!/usr/bin/env python3
"""
List WordPress Pages - Using shared credentials
"""
import sys
import os

# Add wordpress_core to path
script_dir = os.path.dirname(os.path.abspath(__file__))
wordpress_core_path = os.path.join(os.path.dirname(script_dir), 'wordpress_core')
sys.path.insert(0, wordpress_core_path)

from wordpress_utils import WordPressAPI, print_success, print_info

def main():
    print_info("Fetching WordPress pages...")
    api = WordPressAPI()
    
    # Get all pages
    pages = api.list_pages(per_page=100)
    
    if not pages:
        print("❌ No pages found or connection failed")
        return
    
    print_success(f"Found {len(pages)} pages:\n")
    
    # Sort by ID
    pages.sort(key=lambda p: p['id'])
    
    # Print formatted list
    for page in pages:
        page_id = page['id']
        title = page['title']['rendered']
        slug = page['slug']
        url = page['link']
        status = page['status']
        
        status_icon = "✅" if status == "publish" else "📝" if status == "draft" else "🗑️"
        
        print(f"{status_icon} ID: {page_id:5d} | {title:40s} | /{slug}")
        print(f"   {url}")
        print()

if __name__ == "__main__":
    main()
