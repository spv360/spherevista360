#!/usr/bin/env python3
"""
Configure Categories Images Plugin
Set images using the plugin's meta key
"""

import requests
import time

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Category slug to media ID mapping
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

def get_category_current_meta(cat_id):
    """Get current category metadata"""
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/categories/{cat_id}',
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        cat_data = response.json()
        return cat_data.get('meta', {})
    return {}

def update_category_with_image(cat_id, slug, name, media_id):
    """Update category with image using different meta keys"""
    print(f"\n📁 Configuring: {name}")
    print(f"   Category ID: {cat_id}")
    print(f"   Image Media ID: {media_id}")
    
    # Get current meta
    current_meta = get_category_current_meta(cat_id)
    print(f"   Current meta keys: {list(current_meta.keys()) if current_meta else 'None'}")
    
    # Try different meta keys that the Categories Images plugin might use
    meta_keys_to_set = {
        'z_taxonomy_image_url': f'{WORDPRESS_URL}/wp-content/uploads/category_{slug}.jpg',
        'z_taxonomy_image': media_id,
        'category-image-id': media_id,
        'thumbnail_id': media_id,
        '_thumbnail_id': media_id,
        'category_thumbnail_id': media_id,
    }
    
    # Update with all possible meta keys
    for meta_key, meta_value in meta_keys_to_set.items():
        response = requests.post(
            f'{WORDPRESS_URL}/wp-json/wp/v2/categories/{cat_id}',
            json={'meta': {meta_key: str(meta_value)}},
            auth=(USERNAME, PASSWORD)
        )
        
        if response.ok:
            print(f"   ✅ Set {meta_key}")
        else:
            print(f"   ⚠️  Failed to set {meta_key}: {response.status_code}")
    
    time.sleep(0.5)
    return True

def check_plugin_settings():
    """Check what meta keys the plugin is using"""
    print("=" * 80)
    print("🔍 CHECKING CATEGORIES IMAGES PLUGIN CONFIGURATION")
    print("=" * 80)
    print()
    
    # Check a sample category to see what meta fields exist
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/categories/3',  # Finance category
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        cat_data = response.json()
        print("📊 Sample Category (Finance) Current State:")
        print(f"   Name: {cat_data.get('name')}")
        print(f"   ID: {cat_data.get('id')}")
        print(f"   Slug: {cat_data.get('slug')}")
        print()
        print("   Meta fields:")
        meta = cat_data.get('meta', {})
        if meta:
            for key, value in meta.items():
                print(f"      {key}: {value}")
        else:
            print("      No meta fields found")
        print()
    
    print("=" * 80)
    print()

def main():
    """Configure all category images for the plugin"""
    print("=" * 80)
    print("🖼️  CONFIGURING CATEGORIES IMAGES PLUGIN")
    print("=" * 80)
    print()
    
    # First check current state
    check_plugin_settings()
    
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
    updated = 0
    
    print("🔧 Updating category meta with multiple keys...")
    print("=" * 80)
    
    for cat in categories:
        slug = cat['slug']
        cat_id = cat['id']
        name = cat['name']
        
        if slug in CATEGORY_IMAGES:
            media_id = CATEGORY_IMAGES[slug]
            if update_category_with_image(cat_id, slug, name, media_id):
                updated += 1
    
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Updated: {updated} categories")
    print()
    
    print("=" * 80)
    print("🔍 TROUBLESHOOTING STEPS")
    print("=" * 80)
    print()
    print("If images still don't show, try these steps:")
    print()
    print("1. CHECK PLUGIN SETTINGS:")
    print(f"   Go to: {WORDPRESS_URL}/wp-admin/options-general.php?page=categories-images")
    print("   Or: Settings → Categories Images")
    print("   Check if there are any configuration options")
    print()
    print("2. MANUALLY SET ONE IMAGE AS TEST:")
    print(f"   Go to: {WORDPRESS_URL}/wp-admin/edit-tags.php?taxonomy=category")
    print("   Edit 'Finance' category")
    print("   Look for image upload field")
    print("   Select image ID 2744 from media library")
    print("   Save and check if it appears")
    print()
    print("3. CHECK PLUGIN DOCUMENTATION:")
    print("   The plugin might use a custom upload field")
    print("   You may need to re-upload images through the plugin interface")
    print()
    print("4. TRY ALTERNATIVE PLUGIN:")
    print("   If this plugin doesn't work, try:")
    print("   - 'Enhanced Category Pages' plugin")
    print("   - 'Category Thumbnail Images' plugin")
    print("   - Or use Kadence theme's built-in category features")
    print()
    print("5. CHECK THEME COMPATIBILITY:")
    print(f"   Go to: {WORDPRESS_URL}/category/finance/")
    print("   View page source and search for 'category' or 'thumbnail'")
    print("   Check if theme is calling category image functions")
    print()
    
    print("=" * 80)
    print("📸 MEDIA LIBRARY IDs")
    print("=" * 80)
    print()
    print("Use these IDs when manually setting images:")
    for slug, media_id in sorted(CATEGORY_IMAGES.items()):
        cat_name = slug.replace('-', ' ').title()
        print(f"   {cat_name}: {media_id}")
    print()
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
