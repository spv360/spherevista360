#!/usr/bin/env python3
"""Remove duplicate Contact Us entries from footer menu"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def get_footer_menu():
    """Get footer menu"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menus"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        menus = response.json()
        for menu in menus:
            if 'footer' in menu['name'].lower():
                return menu
    return None

def get_menu_items(menu_id):
    """Get all menu items"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items"
    params = {'menus': menu_id, 'per_page': 100}
    
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        return response.json()
    return []

def delete_menu_item(item_id):
    """Delete a menu item"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items/{item_id}"
    
    response = requests.delete(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD),
        params={'force': True}
    )
    
    return response.status_code == 200

print("=" * 70)
print("Remove Duplicate Contact Us from Footer Menu")
print("=" * 70)
print()

# Get footer menu
menu = get_footer_menu()

if not menu:
    print("❌ No footer menu found!")
    exit(1)

print(f"📋 Found Menu: {menu['name']} (ID: {menu['id']})")
print()

# Get all menu items
items = get_menu_items(menu['id'])

if not items:
    print("⚠️  No menu items found!")
    exit(1)

print(f"Total Menu Items: {len(items)}")
print()

# Show all current items
print("Current menu items:")
for item in sorted(items, key=lambda x: x['menu_order']):
    title = item['title']['rendered'] if isinstance(item['title'], dict) else item['title']
    print(f"   {item['menu_order']}. {title} (ID: {item['id']})")
print()

# Find Contact Us duplicates
contact_items = []
for item in items:
    title = item['title']['rendered'] if isinstance(item['title'], dict) else item['title']
    if 'contact' in title.lower():
        contact_items.append(item)

if len(contact_items) <= 1:
    print("✅ No duplicate Contact Us entries found!")
else:
    print(f"⚠️  Found {len(contact_items)} 'Contact' entries:")
    print()
    
    for item in contact_items:
        title = item['title']['rendered'] if isinstance(item['title'], dict) else item['title']
        print(f"   ID: {item['id']}")
        print(f"   Title: {title}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   Order: {item['menu_order']}")
        print()
    
    # Keep the one with the correct URL, delete others
    contact_page_url = f"{WORDPRESS_BASE_URL}/contact/"
    
    items_to_delete = []
    items_to_keep = []
    
    for item in contact_items:
        item_url = item.get('url', '').rstrip('/')
        if contact_page_url.rstrip('/') in item_url or '/contact' in item_url:
            items_to_keep.append(item)
        else:
            items_to_delete.append(item)
    
    # If we have multiple items pointing to contact, keep only the first one
    if len(items_to_keep) > 1:
        items_to_keep.sort(key=lambda x: x['menu_order'])
        items_to_delete.extend(items_to_keep[1:])
        items_to_keep = [items_to_keep[0]]
    
    if items_to_delete:
        print(f"🗑️  Removing {len(items_to_delete)} duplicate(s):")
        print()
        
        for item in items_to_delete:
            title = item['title']['rendered'] if isinstance(item['title'], dict) else item['title']
            print(f"   Deleting: {title} (ID: {item['id']})")
            if delete_menu_item(item['id']):
                print(f"   ✅ Deleted successfully!")
            else:
                print(f"   ❌ Failed to delete")
            print()
        
        print("✅ Duplicate removal complete!")
        print()
        
        if items_to_keep:
            keep_title = items_to_keep[0]['title']['rendered'] if isinstance(items_to_keep[0]['title'], dict) else items_to_keep[0]['title']
            print(f"✓ Keeping: {keep_title} (ID: {items_to_keep[0]['id']})")
    else:
        print("✅ All Contact entries point to the correct page!")

print()
print("=" * 70)
print("Updated Footer Menu:")
print("=" * 70)

# Get updated menu items
updated_items = get_menu_items(menu['id'])
for item in sorted(updated_items, key=lambda x: x['menu_order']):
    title = item['title']['rendered'] if isinstance(item['title'], dict) else item['title']
    indent = "   " if item.get('parent', 0) == 0 else "      ↳ "
    print(f"{indent}{title}")

print()
print("=" * 70)
print("✅ Footer menu cleanup complete!")
print("=" * 70)
