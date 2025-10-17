#!/usr/bin/env python3
"""
Display Category Images Guide
How to show category images on your WordPress site
"""

import requests

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

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

def main():
    print("=" * 80)
    print("🖼️  CATEGORY IMAGES - DISPLAY GUIDE")
    print("=" * 80)
    print()
    
    print("✅ Category images have been assigned!")
    print()
    print("📍 Image assignments:")
    print("-" * 80)
    
    for slug, media_id in CATEGORY_IMAGES.items():
        cat_name = slug.replace('-', ' ').title()
        print(f"   • {cat_name}: Image ID {media_id}")
    
    print()
    print("=" * 80)
    print("🎨 HOW TO DISPLAY CATEGORY IMAGES")
    print("=" * 80)
    print()
    
    print("METHOD 1: Install 'Categories Images' Plugin (Recommended)")
    print("-" * 80)
    print("1. Go to: WordPress Admin → Plugins → Add New")
    print("2. Search for: 'Categories Images'")
    print("3. Install plugin by 'Muhammad Elhady'")
    print("4. Activate the plugin")
    print("5. Go to: Posts → Categories")
    print("6. You'll see category images are already assigned!")
    print("7. The plugin will automatically display them on:")
    print("   - Category archive pages")
    print("   - Category widgets")
    print("   - Category lists")
    print()
    
    print("METHOD 2: Kadence Theme Category Settings")
    print("-" * 80)
    print("1. Go to: Appearance → Customize")
    print("2. Navigate to: 'Content' or 'Archive Settings'")
    print("3. Look for 'Category Archive' or 'Taxonomy Settings'")
    print("4. Enable 'Show Category Image' or similar option")
    print("5. Save and check category pages")
    print()
    
    print("METHOD 3: Add Custom Code to Theme")
    print("-" * 80)
    print("Add this to your category.php or archive.php template:")
    print()
    print("```php")
    print("<?php")
    print("// Display category image")
    print("$category = get_queried_object();")
    print("$thumbnail_id = get_term_meta($category->term_id, 'thumbnail_id', true);")
    print("if ($thumbnail_id) {")
    print("    echo wp_get_attachment_image($thumbnail_id, 'large', false, array('class' => 'category-image'));")
    print("}")
    print("?>")
    print("```")
    print()
    
    print("METHOD 4: Check Category Pages")
    print("-" * 80)
    print("Visit these URLs to see if images display automatically:")
    print()
    for slug in ['finance', 'technology', 'business', 'entertainment']:
        print(f"   • {WORDPRESS_URL}/category/{slug}/")
    print()
    
    print("=" * 80)
    print("📝 VERIFICATION CHECKLIST")
    print("=" * 80)
    print()
    print("✅ Category descriptions updated (professional, relevant)")
    print("✅ Category images uploaded to media library (10 images)")
    print("✅ Images assigned to categories via term meta")
    print("⏳ Display images on frontend (requires plugin or theme support)")
    print()
    
    print("=" * 80)
    print("🎯 RECOMMENDED NEXT STEP")
    print("=" * 80)
    print()
    print("Install 'Categories Images' plugin for automatic display:")
    print(f"   {WORDPRESS_URL}/wp-admin/plugin-install.php?s=categories+images&tab=search")
    print()
    print("Or visit the category pages to check if Kadence displays them:")
    print(f"   {WORDPRESS_URL}/category/finance/")
    print()
    
    print("=" * 80)
    
if __name__ == '__main__':
    main()
