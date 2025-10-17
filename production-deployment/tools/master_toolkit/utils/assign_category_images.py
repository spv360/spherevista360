#!/usr/bin/env python3
"""
Assign Category Images Using WordPress Term Meta
Automatically set category featured images via REST API
"""

import requests
import json

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Mapping of category slugs to their uploaded media IDs
CATEGORY_IMAGES = {
    'business': 2967,
    'economy': 2973,
    'entertainment': 2968,
    'finance': 2966,
    'politics': 2970,
    'technology': 2965,
    'top-stories': 2974,
    'travel': 2969,
    'world': 2971,
    'world-news': 2972,
}

def set_category_meta(cat_id, meta_key, meta_value):
    """Set term meta via REST API"""
    # Try to update via category endpoint with meta field
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/categories/{cat_id}',
        json={'meta': {meta_key: meta_value}},
        auth=(USERNAME, PASSWORD)
    )
    return response.ok

def assign_category_image(cat_id, slug, name, media_id):
    """Assign featured image to category"""
    print(f"\n📁 {name}")
    print(f"   Category ID: {cat_id}")
    print(f"   Image Media ID: {media_id}")
    
    # Try different meta keys that WordPress/Kadence might use
    meta_keys_to_try = [
        'thumbnail_id',
        'category_thumbnail_id',
        'term_thumbnail_id',
        'image_id',
        'featured_image'
    ]
    
    success = False
    for meta_key in meta_keys_to_try:
        if set_category_meta(cat_id, meta_key, media_id):
            print(f"   ✅ Set {meta_key} = {media_id}")
            success = True
            break
    
    if not success:
        # Alternative: Update using ACF or custom fields
        response = requests.post(
            f'{WORDPRESS_URL}/wp-json/wp/v2/categories/{cat_id}',
            json={
                'acf': {'category_image': media_id},
                'meta': {'_thumbnail_id': media_id}
            },
            auth=(USERNAME, PASSWORD)
        )
        
        if response.ok:
            print(f"   ✅ Image assigned via ACF/meta")
            success = True
    
    if not success:
        print(f"   ⚠️  REST API assignment not supported - use manual method")
    
    return success

def main():
    """Assign all category images"""
    print("=" * 80)
    print("🖼️  ASSIGNING CATEGORY IMAGES")
    print("=" * 80)
    
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
    assigned = 0
    skipped = 0
    
    for cat in categories:
        slug = cat['slug']
        cat_id = cat['id']
        name = cat['name']
        
        if slug in CATEGORY_IMAGES:
            media_id = CATEGORY_IMAGES[slug]
            if assign_category_image(cat_id, slug, name, media_id):
                assigned += 1
            else:
                skipped += 1
    
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Assigned via API: {assigned} categories")
    print(f"⚠️  Needs manual setup: {skipped} categories")
    print()
    
    if skipped > 0:
        print("=" * 80)
        print("📝 MANUAL SETUP REQUIRED")
        print("=" * 80)
        print()
        print("WordPress core doesn't support category images by default.")
        print("You need to set them manually in WordPress Admin.")
        print()
        print("🔗 STEP-BY-STEP GUIDE:")
        print()
        print("1. Login to WordPress Admin:")
        print(f"   {WORDPRESS_URL}/wp-admin/")
        print()
        print("2. Go to: Posts → Categories")
        print()
        print("3. For EACH category below, click 'Edit':")
        print()
        
        for cat in sorted(categories, key=lambda x: x['name']):
            slug = cat['slug']
            if slug in CATEGORY_IMAGES:
                media_id = CATEGORY_IMAGES[slug]
                print(f"   • {cat['name']}")
                print(f"     - Look for 'Category Image' or 'Featured Image' field")
                print(f"     - Click 'Set image' button")
                print(f"     - Search for media ID: {media_id}")
                print(f"     - Or look for the recently uploaded category image")
                print(f"     - Click 'Update' to save")
                print()
        
        print("4. If you don't see an image upload field:")
        print()
        print("   OPTION A: Install a Plugin")
        print("   - Go to: Plugins → Add New")
        print("   - Search: 'Categories Images' or 'Custom Taxonomy Images'")
        print("   - Install and activate")
        print("   - Return to Posts → Categories")
        print()
        print("   OPTION B: Check Kadence Theme Settings")
        print("   - Go to: Appearance → Customize")
        print("   - Look for 'Category Settings' or 'Archive Settings'")
        print("   - Enable category image support")
        print()
        print("5. Verify: Visit a category page")
        print(f"   {WORDPRESS_URL}/category/finance/")
        print()
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
