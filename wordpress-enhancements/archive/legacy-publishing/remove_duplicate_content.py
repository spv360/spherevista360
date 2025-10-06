#!/usr/bin/env python3
'''
WordPress Content Removal Script
IMPORTANT: Review all recommendations before executing!
'''

import requests
import base64
import os
import json

# WordPress credentials (ensure these are set)
WP_SITE = os.environ.get('WP_SITE')
WP_USER = os.environ.get('WP_USER')
WP_APP_PASS = os.environ.get('WP_APP_PASS')

if not all([WP_SITE, WP_USER, WP_APP_PASS]):
    print("❌ WordPress credentials not set!")
    exit(1)

credentials = f"{WP_USER}:{WP_APP_PASS}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json'
}

# Items to remove (review this list carefully!)
ITEMS_TO_REMOVE = [
    {
        'id': 298,
        'title': 'Blog',
        'type': 'page',
        'reason': 'Low quality score: 2/8; Very short content: 0 words; Very short title: 4 characters'
    },
    {
        'id': 904,
        'title': 'Home',
        'type': 'page',
        'reason': 'Very short title: 4 characters'
    },
]

def remove_content_item(item):
    '''Remove a single content item'''
    item_type = item['type']
    item_id = item['id']
    
    if item_type == 'post':
        url = f"{WP_SITE}/wp-json/wp/v2/posts/{item_id}"
    elif item_type == 'page':
        url = f"{WP_SITE}/wp-json/wp/v2/pages/{item_id}"
    else:
        print(f"❌ Unknown content type: {item_type}")
        return False
    
    # Move to trash (safer than permanent deletion)
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Moved to trash: {item['title']}")
        return True
    else:
        print(f"❌ Failed to remove: {item['title']} (Status: {response.status_code})")
        return False

def main():
    print("🗑️ WordPress Content Cleanup")
    print("=" * 30)
    print(f"Items to remove: {len(ITEMS_TO_REMOVE)}")
    print()
    
    # Display items for review
    print("📋 Items scheduled for removal:")
    for i, item in enumerate(ITEMS_TO_REMOVE, 1):
        print(f"{i:2d}. {item['title']} ({item['type']})")
        print(f"    Reason: {item['reason']}")
        print()
    
    # Confirmation
    response = input("Do you want to proceed with removal? (type 'yes' to confirm): ")
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        return
    
    # Remove items
    success_count = 0
    for item in ITEMS_TO_REMOVE:
        if remove_content_item(item):
            success_count += 1
    
    print(f"\n✅ Removal complete: {success_count}/{len(ITEMS_TO_REMOVE)} items moved to trash")
    print("💡 Items are moved to trash and can be restored if needed")

if __name__ == "__main__":
    main()
