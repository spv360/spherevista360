#!/usr/bin/env python3
"""
Check for duplicate pages in WordPress site
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def get_all_pages():
    print("🔍 CHECKING FOR DUPLICATE PAGES")
    print("=" * 50)
    
    # Get all pages
    try:
        # First, get total count
        response = requests.get(f"{WP_API_BASE}/pages?per_page=1")
        total_pages = int(response.headers.get('X-WP-Total', 0))
        print(f"📊 Total pages found: {total_pages}")
        
        # Get all pages
        all_pages = []
        per_page = 100
        page = 1
        
        while True:
            response = requests.get(f"{WP_API_BASE}/pages?per_page={per_page}&page={page}")
            if response.status_code != 200:
                break
                
            pages = response.json()
            if not pages:
                break
                
            all_pages.extend(pages)
            
            if len(pages) < per_page:
                break
                
            page += 1
        
        return all_pages
        
    except Exception as e:
        print(f"💥 Error getting pages: {e}")
        return []

def analyze_duplicates(pages):
    print(f"\n📋 ANALYZING {len(pages)} PAGES FOR DUPLICATES")
    print("=" * 50)
    
    # Group by title
    titles = defaultdict(list)
    slugs = defaultdict(list)
    
    for page in pages:
        title = page.get('title', {}).get('rendered', '').strip()
        slug = page.get('slug', '').strip()
        
        titles[title.lower()].append(page)
        slugs[slug.lower()].append(page)
    
    # Find duplicates by title
    print("\n🔍 DUPLICATE TITLES:")
    duplicate_titles = {title: pages_list for title, pages_list in titles.items() if len(pages_list) > 1 and title}
    
    if duplicate_titles:
        for title, pages_list in duplicate_titles.items():
            print(f"\n📄 '{title.title()}':")
            for page in pages_list:
                print(f"   ID: {page['id']}")
                print(f"   Slug: {page['slug']}")
                print(f"   URL: {page['link']}")
                print(f"   Status: {page['status']}")
                print(f"   Date: {page['date']}")
                print(f"   Modified: {page['modified']}")
                print()
    else:
        print("   ✅ No duplicate titles found")
    
    # Find duplicates by slug
    print("\n🔍 DUPLICATE SLUGS:")
    duplicate_slugs = {slug: pages_list for slug, pages_list in slugs.items() if len(pages_list) > 1 and slug}
    
    if duplicate_slugs:
        for slug, pages_list in duplicate_slugs.items():
            print(f"\n📄 Slug: '{slug}':")
            for page in pages_list:
                print(f"   ID: {page['id']}")
                print(f"   Title: {page['title']['rendered']}")
                print(f"   URL: {page['link']}")
                print(f"   Status: {page['status']}")
                print()
    else:
        print("   ✅ No duplicate slugs found")
    
    return duplicate_titles, duplicate_slugs

def check_specific_pages():
    print("\n🎯 CHECKING SPECIFIC PAGES (Archive, Disclaimer, etc.)")
    print("=" * 60)
    
    target_keywords = ['archive', 'disclaimer', 'privacy', 'about', 'contact', 'terms']
    
    try:
        # Search for each keyword
        for keyword in target_keywords:
            print(f"\n🔍 Searching for '{keyword}':")
            
            response = requests.get(f"{WP_API_BASE}/pages?search={keyword}")
            if response.status_code == 200:
                pages = response.json()
                
                if pages:
                    print(f"   📊 Found {len(pages)} pages:")
                    for page in pages:
                        title = page.get('title', {}).get('rendered', 'No Title')
                        print(f"   📄 '{title}'")
                        print(f"      ID: {page['id']}")
                        print(f"      Slug: {page['slug']}")
                        print(f"      URL: {page['link']}")
                        print(f"      Status: {page['status']}")
                        print()
                else:
                    print(f"   ✅ No pages found for '{keyword}'")
            else:
                print(f"   ❌ Error searching for '{keyword}': {response.status_code}")
                
    except Exception as e:
        print(f"💥 Error in specific page check: {e}")

def list_all_pages_summary(pages):
    print("\n📜 ALL PAGES SUMMARY")
    print("=" * 30)
    
    # Sort by title
    sorted_pages = sorted(pages, key=lambda x: x.get('title', {}).get('rendered', '').lower())
    
    for page in sorted_pages:
        title = page.get('title', {}).get('rendered', 'No Title')
        status = page.get('status', 'unknown')
        
        status_icon = "✅" if status == "publish" else "🚧" if status == "draft" else "❓"
        
        print(f"{status_icon} {title}")
        print(f"   ID: {page['id']} | Slug: {page['slug']} | Status: {status}")
        print(f"   URL: {page['link']}")
        print()

def check_menu_duplicates():
    print("\n🧭 CHECKING NAVIGATION MENUS")
    print("=" * 40)
    
    try:
        # Try to get menu information
        response = requests.get(f"{WP_API_BASE}/menus")
        if response.status_code == 200:
            menus = response.json()
            print(f"📊 Found {len(menus)} menus")
            
            for menu in menus:
                print(f"\n📋 Menu: {menu.get('name', 'Unknown')}")
                print(f"   ID: {menu.get('term_id')}")
                print(f"   Slug: {menu.get('slug')}")
                
                # Try to get menu items
                menu_items_response = requests.get(f"{WP_API_BASE}/menu-items?menus={menu.get('term_id')}")
                if menu_items_response.status_code == 200:
                    items = menu_items_response.json()
                    print(f"   Items: {len(items)}")
                    
                    # Look for duplicate items
                    item_titles = defaultdict(list)
                    for item in items:
                        title = item.get('title', {}).get('rendered', '')
                        item_titles[title.lower()].append(item)
                    
                    duplicates = {title: items for title, items in item_titles.items() if len(items) > 1 and title}
                    if duplicates:
                        print("   🚨 Duplicate menu items found:")
                        for title, duplicate_items in duplicates.items():
                            print(f"      '{title}' appears {len(duplicate_items)} times")
                    else:
                        print("   ✅ No duplicate menu items")
        else:
            print(f"❌ Could not retrieve menus: {response.status_code}")
            print("   This might be a plugin/theme limitation")
            
    except Exception as e:
        print(f"💥 Error checking menus: {e}")

def main():
    print("🔧 WORDPRESS DUPLICATE PAGES CHECK")
    print("=" * 50)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get all pages
    pages = get_all_pages()
    
    if not pages:
        print("❌ No pages found or error retrieving pages")
        return
    
    # Analyze for duplicates
    duplicate_titles, duplicate_slugs = analyze_duplicates(pages)
    
    # Check specific pages
    check_specific_pages()
    
    # List all pages
    list_all_pages_summary(pages)
    
    # Check menus
    check_menu_duplicates()
    
    print("\n" + "=" * 50)
    print("🎯 RECOMMENDATIONS:")
    
    if duplicate_titles or duplicate_slugs:
        print("🚨 DUPLICATES FOUND:")
        if duplicate_titles:
            print("   - Review pages with identical titles")
            print("   - Consider merging or deleting unnecessary duplicates")
        if duplicate_slugs:
            print("   - Fix pages with identical slugs (this can cause URL conflicts)")
        
        print("\n💡 TO FIX DUPLICATES:")
        print("   1. Go to WordPress Admin → Pages")
        print("   2. Review the duplicate pages listed above")
        print("   3. Delete unnecessary duplicates or rename them")
        print("   4. Check if duplicates appear in menus and remove extras")
    else:
        print("✅ No obvious page duplicates found")
        print("💡 If you still see duplicates in navigation:")
        print("   1. Check WordPress Admin → Appearance → Menus")
        print("   2. Look for duplicate menu items")
        print("   3. Check widgets that might display page lists")
        print("   4. Review theme customizer for page display settings")

if __name__ == "__main__":
    main()