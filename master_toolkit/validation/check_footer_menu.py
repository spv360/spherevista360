#!/usr/bin/env python3
"""Check footer menu items"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Get all menus
url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menus"
response = requests.get(
    url,
    auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
)

print("=" * 70)
print("Footer Menu Check")
print("=" * 70)
print()

if response.status_code == 200:
    menus = response.json()
    
    for menu in menus:
        if 'footer' in menu['name'].lower():
            print(f"Found Menu: {menu['name']} (ID: {menu['id']})")
            print("-" * 70)
            
            # Get menu items
            items_url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items"
            params = {'menus': menu['id'], 'per_page': 100}
            
            items_response = requests.get(
                items_url,
                params=params,
                auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
            )
            
            if items_response.status_code == 200:
                items = items_response.json()
                
                print(f"\nTotal Items: {len(items)}\n")
                
                for item in sorted(items, key=lambda x: x['menu_order']):
                    indent = "   " if item.get('parent', 0) == 0 else "      ↳ "
                    print(f"{indent}[ID: {item['id']}] {item['title']}")
                    print(f"{indent}     URL: {item.get('url', 'N/A')}")
                    
                # Check for duplicates
                titles = [item['title'] for item in items]
                duplicates = [title for title in set(titles) if titles.count(title) > 1]
                
                if duplicates:
                    print("\n⚠️  DUPLICATES FOUND:")
                    for dup in duplicates:
                        matching_items = [item for item in items if item['title'] == dup]
                        print(f"\n   '{dup}' appears {len(matching_items)} times:")
                        for item in matching_items:
                            print(f"      - ID: {item['id']}, Order: {item['menu_order']}")
            else:
                print(f"Failed to get menu items: {items_response.status_code}")
else:
    print(f"Failed to get menus: {response.status_code}")

print("\n" + "=" * 70)
