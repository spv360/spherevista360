#!/usr/bin/env python3
"""
List all WordPress categories with their IDs, names, and descriptions
"""

import requests
import json

# WordPress credentials
wp_url = "https://spherevista360.com"
username = "JK"
app_password = "BT1I iKXv 6bYv EUuS P2vk K9hV"

print("=" * 100)
print("📋 FETCHING ALL CATEGORIES FROM SPHEREVISTA360.COM")
print("=" * 100)

endpoint = f"{wp_url}/wp-json/wp/v2/categories?per_page=100"

try:
    response = requests.get(endpoint, auth=(username, app_password))
    
    if response.status_code == 200:
        categories = response.json()
        
        print(f"\n✅ Found {len(categories)} categories\n")
        print("-" * 100)
        print(f"{'ID':<6} {'Name':<20} {'Slug':<20} {'Posts':<8} {'Description':<40}")
        print("-" * 100)
        
        for cat in sorted(categories, key=lambda x: x['id']):
            description = cat.get('description', '')
            # Truncate long descriptions
            if len(description) > 40:
                description = description[:37] + "..."
            
            print(f"{cat['id']:<6} {cat['name']:<20} {cat['slug']:<20} {cat['count']:<8} {description:<40}")
        
        print("-" * 100)
        
        # Show full details for each category
        print("\n" + "=" * 100)
        print("📝 FULL CATEGORY DETAILS:")
        print("=" * 100)
        
        for cat in sorted(categories, key=lambda x: x['id']):
            print(f"\n{'='*100}")
            print(f"Category ID: {cat['id']}")
            print(f"Name: {cat['name']}")
            print(f"Slug: {cat['slug']}")
            print(f"Post Count: {cat['count']}")
            print(f"URL: {cat['link']}")
            print(f"\nDescription:")
            print(f"{cat.get('description', 'No description')}")
            
            # Check for category image
            if 'meta' in cat and 'thumbnail_id' in cat['meta']:
                print(f"\nThumbnail ID: {cat['meta']['thumbnail_id']}")
        
        print("\n" + "=" * 100)
        print("✅ DONE!")
        print("=" * 100)
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
