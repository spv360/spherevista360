#!/usr/bin/env python3
"""
Fix WordPress menu issues - remove broken links and duplicates
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

def get_main_menu_items(headers):
    print("\n📋 GETTING MAIN MENU ITEMS")
    print("=" * 35)
    
    try:
        # Get Main Menu (ID: 208 from previous analysis)
        main_menu_id = 208
        response = requests.get(f"{WP_API_BASE}/menu-items?menus={main_menu_id}", headers=headers)
        
        if response.status_code == 200:
            items = response.json()
            print(f"📊 Found {len(items)} menu items")
            
            # Organize items with details
            menu_items = []
            for item in items:
                item_data = {
                    'id': item.get('id'),
                    'title': item.get('title', {}).get('rendered', 'Unknown'),
                    'url': item.get('url', ''),
                    'type': item.get('type', 'unknown'),
                    'object': item.get('object', 'unknown'),
                    'object_id': item.get('object_id', 0),
                    'menu_order': item.get('menu_order', 0),
                    'parent': item.get('menu_item_parent', 0)
                }
                menu_items.append(item_data)
                
                print(f"   📄 {item_data['title']} (ID: {item_data['id']})")
                print(f"      URL: {item_data['url']}")
                print(f"      Type: {item_data['type']} | Object: {item_data['object']}")
                
            return menu_items, main_menu_id
        else:
            print(f"❌ Could not get menu items: {response.status_code}")
            return [], None
    except Exception as e:
        print(f"💥 Error getting menu items: {e}")
        return [], None

def identify_broken_items(headers, menu_items):
    print("\n🔍 IDENTIFYING BROKEN MENU ITEMS")
    print("=" * 40)
    
    broken_items = []
    duplicate_items = []
    outdated_items = []
    
    # Check for broken page references
    page_ids_to_check = []
    for item in menu_items:
        if item['type'] == 'post_type' and item['object'] == 'page':
            page_ids_to_check.append(item['object_id'])
    
    # Get actual pages to verify
    try:
        response = requests.get(f"{WP_API_BASE}/pages?per_page=100", headers=headers)
        if response.status_code == 200:
            existing_pages = response.json()
            existing_page_ids = [page['id'] for page in existing_pages]
            
            print(f"📊 Existing pages: {len(existing_pages)}")
            
            # Identify broken items
            url_count = {}
            title_count = {}
            
            for item in menu_items:
                # Check for broken page links
                if item['type'] == 'post_type' and item['object'] == 'page':
                    if item['object_id'] not in existing_page_ids:
                        broken_items.append(item)
                        print(f"❌ BROKEN: {item['title']} (Page ID {item['object_id']} not found)")
                
                # Check for duplicates by URL
                url = item['url']
                if url in url_count:
                    url_count[url].append(item)
                else:
                    url_count[url] = [item]
                
                # Check for duplicates by title
                title = item['title'].lower()
                if title in title_count:
                    title_count[title].append(item)
                else:
                    title_count[title] = [item]
                
                # Check for outdated category links
                if '/category/tech/' in item['url']:
                    outdated_items.append(item)
                    print(f"⚠️  OUTDATED: {item['title']} (Tech category deleted)")
                elif '/category/finance/' in item['url'] or '/category/world/' in item['url']:
                    outdated_items.append(item)
                    print(f"⚠️  QUESTIONABLE: {item['title']} (Category may not exist)")
            
            # Find duplicates
            for url, items in url_count.items():
                if len(items) > 1:
                    # Keep the first one, mark others as duplicates
                    for item in items[1:]:
                        duplicate_items.append(item)
                        print(f"🔄 DUPLICATE: {item['title']} (Duplicate URL: {url})")
                        
    except Exception as e:
        print(f"💥 Error checking pages: {e}")
    
    return broken_items, duplicate_items, outdated_items

def delete_menu_items(headers, items_to_delete, reason):
    print(f"\n🗑️ DELETING {reason.upper()} ITEMS")
    print("=" * 50)
    
    success_count = 0
    
    for item in items_to_delete:
        try:
            print(f"🗑️ Deleting: {item['title']} (ID: {item['id']})")
            
            response = requests.delete(f"{WP_API_BASE}/menu-items/{item['id']}", headers=headers)
            
            if response.status_code in [200, 204]:
                print(f"   ✅ Successfully deleted")
                success_count += 1
            else:
                print(f"   ❌ Failed to delete: {response.status_code}")
                if response.text:
                    print(f"      Error: {response.text}")
                    
        except Exception as e:
            print(f"   💥 Error deleting {item['title']}: {e}")
    
    print(f"\n📊 {reason} cleanup: {success_count}/{len(items_to_delete)} items deleted")
    return success_count

def create_clean_menu_structure(headers, menu_id):
    print("\n🔧 CREATING CLEAN MENU STRUCTURE")
    print("=" * 40)
    
    # Define the clean menu structure we want
    clean_menu_items = [
        {"title": "Home", "url": "https://spherevista360.com/", "type": "custom", "order": 1},
        {"title": "Newsletter", "url": "https://spherevista360.com/newsletter/", "type": "custom", "order": 2},
        {"title": "Archives", "url": "https://spherevista360.com/archives/", "type": "custom", "order": 3},
        {"title": "Disclaimer", "url": "https://spherevista360.com/disclaimer/", "type": "custom", "order": 4},
        {"title": "Terms of Service", "url": "https://spherevista360.com/terms-of-service/", "type": "custom", "order": 5},
        {"title": "Subscribe", "url": "https://spherevista360.com/subscribe/", "type": "custom", "order": 6}
    ]
    
    print("📋 Proposed clean menu structure:")
    for item in clean_menu_items:
        print(f"   {item['order']}. {item['title']} → {item['url']}")
    
    return clean_menu_items

def verify_menu_cleanup(headers, menu_id):
    print("\n✅ VERIFYING MENU CLEANUP")
    print("=" * 35)
    
    try:
        response = requests.get(f"{WP_API_BASE}/menu-items?menus={menu_id}", headers=headers)
        
        if response.status_code == 200:
            items = response.json()
            print(f"📊 Remaining menu items: {len(items)}")
            
            # Check for any remaining issues
            working_items = 0
            for item in items:
                title = item.get('title', {}).get('rendered', 'Unknown')
                url = item.get('url', '')
                
                print(f"   📄 {title}")
                print(f"      URL: {url}")
                
                # Quick URL validation
                try:
                    url_response = requests.head(url, timeout=5)
                    if url_response.status_code == 200:
                        print(f"      ✅ URL accessible")
                        working_items += 1
                    else:
                        print(f"      ⚠️  URL returns {url_response.status_code}")
                except:
                    print(f"      ❌ URL not accessible")
                print()
            
            print(f"📊 Working menu items: {working_items}/{len(items)}")
            return len(items), working_items
        else:
            print(f"❌ Could not verify menu: {response.status_code}")
            return 0, 0
    except Exception as e:
        print(f"💥 Error verifying menu: {e}")
        return 0, 0

def main():
    print("🛠️ WORDPRESS MENU CLEANUP TOOL")
    print("=" * 40)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Fixing broken links, duplicates, and outdated items")
    print()
    
    # Get authentication
    headers = get_auth_headers()
    
    # Get menu items
    menu_items, menu_id = get_main_menu_items(headers)
    
    if not menu_items:
        print("❌ Could not retrieve menu items. Exiting.")
        return
    
    # Identify problematic items
    broken_items, duplicate_items, outdated_items = identify_broken_items(headers, menu_items)
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"   🚨 Broken items: {len(broken_items)}")
    print(f"   🔄 Duplicate items: {len(duplicate_items)}")
    print(f"   ⚠️  Outdated items: {len(outdated_items)}")
    
    if broken_items or duplicate_items or outdated_items:
        print("\n🔧 PROCEEDING WITH CLEANUP...")
        
        # Delete broken items
        if broken_items:
            delete_menu_items(headers, broken_items, "broken")
        
        # Delete duplicates
        if duplicate_items:
            delete_menu_items(headers, duplicate_items, "duplicate")
        
        # Delete outdated items
        if outdated_items:
            delete_menu_items(headers, outdated_items, "outdated")
        
        # Verify cleanup
        remaining_items, working_items = verify_menu_cleanup(headers, menu_id)
        
        print("\n" + "=" * 50)
        print("🎉 MENU CLEANUP COMPLETE!")
        print("=" * 50)
        print(f"✅ Broken links removed: {len(broken_items)}")
        print(f"✅ Duplicates removed: {len(duplicate_items)}")
        print(f"✅ Outdated items removed: {len(outdated_items)}")
        print(f"📊 Final menu status: {working_items}/{remaining_items} items working")
        
        if working_items == remaining_items and remaining_items > 0:
            print("🎉 All remaining menu items are functional!")
        else:
            print("⚠️  Some items may still need manual review")
            
    else:
        print("✅ No cleanup needed - menu is already clean!")
    
    # Show recommended structure
    create_clean_menu_structure(headers, menu_id)

if __name__ == "__main__":
    main()