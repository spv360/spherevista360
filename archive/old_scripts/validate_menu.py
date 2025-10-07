#!/usr/bin/env python3
"""
Validate and analyze WordPress main menu structure
"""

import requests
import json
import base64
from datetime import datetime
import getpass

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def get_auth_headers():
    print("🔐 AUTHENTICATION SETUP")
    print("=" * 30)
    
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    
    credentials = f"{username}:{app_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    return {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

def check_menu_locations(headers):
    print("\n🧭 CHECKING MENU LOCATIONS")
    print("=" * 35)
    
    try:
        # Try to get menu locations
        response = requests.get(f"{WP_API_BASE}/menu-locations", headers=headers)
        if response.status_code == 200:
            locations = response.json()
            print(f"📍 Menu locations found: {len(locations)}")
            
            for location_name, menu_id in locations.items():
                print(f"   📋 {location_name}: Menu ID {menu_id}")
                
            return locations
        else:
            print(f"❌ Could not get menu locations: {response.status_code}")
            return {}
    except Exception as e:
        print(f"💥 Error checking menu locations: {e}")
        return {}

def get_all_menus(headers):
    print("\n📋 GETTING ALL MENUS")
    print("=" * 25)
    
    try:
        # Get all menus
        response = requests.get(f"{WP_API_BASE}/menus", headers=headers)
        if response.status_code == 200:
            menus = response.json()
            print(f"📊 Total menus found: {len(menus)}")
            
            menu_info = []
            for menu in menus:
                menu_data = {
                    'id': menu.get('id'),
                    'name': menu.get('name'),
                    'slug': menu.get('slug'),
                    'count': menu.get('count', 0)
                }
                menu_info.append(menu_data)
                print(f"   📋 Menu: {menu_data['name']} (ID: {menu_data['id']}, Items: {menu_data['count']})")
                
            return menu_info
        else:
            print(f"❌ Could not get menus: {response.status_code}")
            return []
    except Exception as e:
        print(f"💥 Error getting menus: {e}")
        return []

def analyze_menu_items(headers, menu_id, menu_name):
    print(f"\n🔍 ANALYZING MENU: {menu_name}")
    print("=" * 40)
    
    try:
        response = requests.get(f"{WP_API_BASE}/menu-items?menus={menu_id}", headers=headers)
        if response.status_code == 200:
            items = response.json()
            print(f"📊 Menu items: {len(items)}")
            
            # Group items by parent
            top_level = []
            sub_items = {}
            
            for item in items:
                item_data = {
                    'id': item.get('id'),
                    'title': item.get('title', {}).get('rendered', 'Unknown'),
                    'url': item.get('url', ''),
                    'parent': item.get('menu_order', 0),
                    'type': item.get('type', 'unknown'),
                    'object': item.get('object', 'unknown'),
                    'object_id': item.get('object_id', 0)
                }
                
                if item.get('menu_item_parent', 0) == 0:
                    top_level.append(item_data)
                else:
                    parent_id = item.get('menu_item_parent', 0)
                    if parent_id not in sub_items:
                        sub_items[parent_id] = []
                    sub_items[parent_id].append(item_data)
            
            # Display menu structure
            print(f"\n📋 MENU STRUCTURE:")
            for item in sorted(top_level, key=lambda x: x['parent']):
                print(f"   📄 {item['title']}")
                print(f"      URL: {item['url']}")
                print(f"      Type: {item['type']} ({item['object']})")
                if item['object_id']:
                    print(f"      Object ID: {item['object_id']}")
                
                # Show sub-items if any
                if item['id'] in sub_items:
                    for sub_item in sub_items[item['id']]:
                        print(f"      └── {sub_item['title']}")
                        print(f"          URL: {sub_item['url']}")
                print()
                
            return items
        else:
            print(f"❌ Could not get menu items: {response.status_code}")
            return []
    except Exception as e:
        print(f"💥 Error analyzing menu: {e}")
        return []

def check_page_references(headers, menu_items):
    print("\n🔗 CHECKING PAGE REFERENCES")
    print("=" * 35)
    
    # Get all pages
    try:
        response = requests.get(f"{WP_API_BASE}/pages?per_page=100", headers=headers)
        if response.status_code == 200:
            pages = response.json()
            page_lookup = {page['id']: page for page in pages}
            
            print(f"📊 Total pages available: {len(pages)}")
            
            # Check menu items against actual pages
            issues = []
            
            for item in menu_items:
                if item.get('type') == 'post_type' and item.get('object') == 'page':
                    page_id = item.get('object_id')
                    if page_id in page_lookup:
                        page = page_lookup[page_id]
                        print(f"   ✅ {item.get('title', {}).get('rendered', 'Unknown')}")
                        print(f"      Links to: {page.get('title', {}).get('rendered', 'Unknown')} (ID: {page_id})")
                        print(f"      Status: {page.get('status', 'unknown')}")
                    else:
                        issues.append({
                            'menu_item': item.get('title', {}).get('rendered', 'Unknown'),
                            'page_id': page_id,
                            'issue': 'Page not found'
                        })
                        print(f"   ❌ {item.get('title', {}).get('rendered', 'Unknown')}")
                        print(f"      Links to missing page ID: {page_id}")
                elif item.get('type') == 'custom':
                    print(f"   🔗 {item.get('title', {}).get('rendered', 'Unknown')}")
                    print(f"      Custom URL: {item.get('url', 'Unknown')}")
                print()
                
            return issues
        else:
            print(f"❌ Could not get pages: {response.status_code}")
            return []
    except Exception as e:
        print(f"💥 Error checking page references: {e}")
        return []

def check_for_duplicate_references(menu_items):
    print("\n🔍 CHECKING FOR DUPLICATE REFERENCES")
    print("=" * 45)
    
    # Check for duplicate page references
    page_refs = {}
    url_refs = {}
    
    for item in menu_items:
        title = item.get('title', {}).get('rendered', 'Unknown')
        
        if item.get('type') == 'post_type' and item.get('object') == 'page':
            page_id = item.get('object_id')
            if page_id in page_refs:
                page_refs[page_id].append(title)
            else:
                page_refs[page_id] = [title]
                
        url = item.get('url', '')
        if url:
            if url in url_refs:
                url_refs[url].append(title)
            else:
                url_refs[url] = [title]
    
    # Report duplicates
    duplicates_found = False
    
    print("📋 Duplicate page references:")
    for page_id, titles in page_refs.items():
        if len(titles) > 1:
            duplicates_found = True
            print(f"   🚨 Page ID {page_id} referenced by:")
            for title in titles:
                print(f"      - {title}")
    
    print("\n📋 Duplicate URL references:")
    for url, titles in url_refs.items():
        if len(titles) > 1:
            duplicates_found = True
            print(f"   🚨 URL {url} referenced by:")
            for title in titles:
                print(f"      - {title}")
    
    if not duplicates_found:
        print("   ✅ No duplicates found")

def suggest_menu_updates():
    print("\n💡 MENU UPDATE SUGGESTIONS")
    print("=" * 35)
    
    print("📋 Based on recent changes, consider updating menu to include:")
    print("   ✅ Newsletter page (optimized)")
    print("   ✅ Homepage (optimized)")
    print("   ❌ Remove any links to deleted duplicate pages:")
    print("      - Disclaimer-2")
    print("      - Terms of Service-2")
    print("      - Sitemap-2") 
    print("      - Archives-2")
    print("      - Subscribe-2")
    
    print("\n🔧 Recommended menu structure:")
    print("   📄 Home")
    print("   📄 Newsletter")
    print("   📄 Archives")
    print("   📄 About/Disclaimer")
    print("   📄 Terms of Service")
    print("   📄 Contact/Subscribe")

def main():
    print("🧭 WORDPRESS MENU VALIDATION")
    print("=" * 40)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Checking if main menu is up-to-date")
    print()
    
    # Get authentication
    headers = get_auth_headers()
    
    # Check menu locations
    menu_locations = check_menu_locations(headers)
    
    # Get all menus
    menus = get_all_menus(headers)
    
    # Analyze each menu
    all_menu_items = []
    for menu in menus:
        items = analyze_menu_items(headers, menu['id'], menu['name'])
        all_menu_items.extend(items)
    
    if all_menu_items:
        # Check page references
        issues = check_page_references(headers, all_menu_items)
        
        # Check for duplicates
        check_for_duplicate_references(all_menu_items)
        
        # Suggestions
        suggest_menu_updates()
        
        print("\n" + "=" * 50)
        print("📊 MENU VALIDATION SUMMARY")
        print("=" * 50)
        
        if issues:
            print("🚨 ISSUES FOUND:")
            for issue in issues:
                print(f"   ❌ {issue['menu_item']}: {issue['issue']}")
            print("\n💡 Recommendation: Update menu in WordPress Admin → Appearance → Menus")
        else:
            print("✅ No broken menu links found")
            print("💡 Menu appears to be functional")
    else:
        print("❌ Could not analyze menu items")

if __name__ == "__main__":
    main()