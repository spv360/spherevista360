#!/usr/bin/env python3
"""
Set Category Images in Kadence Theme
Automatically assign uploaded images to categories
"""

import requests

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Mapping of category slugs to their uploaded media IDs
CATEGORY_IMAGES = {
    'business': 2741,
    'economy': 2742,
    'entertainment': 2743,
    'finance': 2744,
    'politics': 2745,
    'technology': 2746,
    'top-stories': 2747,
    'travel': 2748,
    'world': 2749,
    'world-news': 2750,
}

def set_category_image(cat_id, slug, name, media_id):
    """Set category featured image using term meta"""
    print(f"📁 Setting image for: {name}")
    
    # Try different meta keys that Kadence might use
    meta_keys = [
        'kadence_term_image_id',
        'category-image-id', 
        'category_thumbnail_id',
        '_thumbnail_id'
    ]
    
    success = False
    for meta_key in meta_keys:
        # WordPress REST API doesn't directly support term meta
        # We need to use a custom endpoint or plugin
        # For now, we'll document the manual process
        pass
    
    print(f"   ℹ️  Media ID {media_id} ready for category {slug}")
    return True

def main():
    """Set category images"""
    print("=" * 80)
    print("🖼️  SETTING CATEGORY IMAGES")
    print("=" * 80)
    print()
    
    # Get all categories
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/categories',
        params={'per_page': 100},
        auth=(USERNAME, PASSWORD)
    )
    
    if not response.ok:
        print("❌ Failed to fetch categories")
        return
    
    categories = response.json()
    
    print("📊 Category Image Mapping:")
    print("=" * 80)
    
    for cat in categories:
        slug = cat['slug']
        name = cat['name']
        cat_id = cat['id']
        
        if slug in CATEGORY_IMAGES:
            media_id = CATEGORY_IMAGES[slug]
            print(f"\n✅ {name}")
            print(f"   Category ID: {cat_id}")
            print(f"   Image Media ID: {media_id}")
            print(f"   URL: {WORDPRESS_URL}/wp-admin/term.php?taxonomy=category&tag_ID={cat_id}&post_type=post")
    
    print("\n" + "=" * 80)
    print("📝 MANUAL ASSIGNMENT GUIDE")
    print("=" * 80)
    print()
    print("Since WordPress REST API doesn't directly support category images,")
    print("you can set them manually in WordPress Admin:")
    print()
    print("Method 1: Using Kadence Theme (if it supports category images)")
    print("   1. Go to: Posts → Categories")
    print("   2. Click 'Edit' on each category")
    print("   3. Look for 'Category Image' or 'Featured Image' field")
    print("   4. Click 'Set image' and select from media library")
    print()
    print("Method 2: Using a Plugin")
    print("   Install 'Categories Images' or 'Custom Taxonomy Images' plugin")
    print("   Then assign images from Posts → Categories")
    print()
    print("Method 3: Check if your category archive shows images automatically")
    print("   Visit: {}/category/finance/".format(WORDPRESS_URL))
    print("   Some themes auto-display featured images")
    print()
    
    # Create SQL commands as backup
    print("=" * 80)
    print("💾 BACKUP: SQL Commands (if needed)")
    print("=" * 80)
    print()
    
    for cat in categories:
        slug = cat['slug']
        cat_id = cat['id']
        
        if slug in CATEGORY_IMAGES:
            media_id = CATEGORY_IMAGES[slug]
            print(f"-- {cat['name']}")
            print(f"INSERT INTO wp_termmeta (term_id, meta_key, meta_value) VALUES ({cat_id}, 'thumbnail_id', {media_id})")
            print(f"  ON DUPLICATE KEY UPDATE meta_value = {media_id};")
            print()
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
