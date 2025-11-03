#!/usr/bin/env python3
"""
Update a single WordPress category description
"""

import requests
import sys

# WordPress credentials
wp_url = "https://spherevista360.com"
username = "JK"
app_password = "BT1I iKXv 6bYv EUuS P2vk K9hV"

def update_category_description(category_id, new_description):
    """Update category description"""
    endpoint = f"{wp_url}/wp-json/wp/v2/categories/{category_id}"
    
    print("=" * 80)
    print(f"🔄 UPDATING CATEGORY {category_id}")
    print("=" * 80)
    
    # Get current category info
    response = requests.get(endpoint, auth=(username, app_password))
    
    if response.status_code == 200:
        current_cat = response.json()
        print(f"\nCategory Name: {current_cat['name']}")
        print(f"Current Description: {current_cat.get('description', 'None')}")
        print(f"\nNew Description: {new_description}")
        print("\n" + "-" * 80)
        
        # Update the description
        update_response = requests.post(
            endpoint,
            auth=(username, app_password),
            json={'description': new_description}
        )
        
        if update_response.status_code == 200:
            print("✅ Category description updated successfully!")
            updated_cat = update_response.json()
            print(f"\nVerified new description:")
            print(f"{updated_cat.get('description')}")
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(update_response.text)
    else:
        print(f"❌ Category not found: {response.status_code}")
        print(response.text)
    
    print("=" * 80)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        category_id = int(sys.argv[1])
        new_description = sys.argv[2]
        update_category_description(category_id, new_description)
    else:
        print("=" * 80)
        print("📝 UPDATE CATEGORY DESCRIPTION")
        print("=" * 80)
        print("\nUsage:")
        print("  python3 update_category.py <category_id> <description>")
        print("\nExample:")
        print('  python3 update_category.py 3 "Your new description here"')
        print("\nOr edit this script to update specific categories:")
        print("\n# Example updates:")
        print('update_category_description(3, "New Finance description")')
        print('update_category_description(4, "New Technology description")')
        print("\n" + "=" * 80)
        print("\n💡 TIP: Run list_categories.py first to see all category IDs")
        print("=" * 80)
        
        # Uncomment and modify these lines to update categories:
        # update_category_description(3, "Your new Finance description")
        # update_category_description(4, "Your new Technology description")
