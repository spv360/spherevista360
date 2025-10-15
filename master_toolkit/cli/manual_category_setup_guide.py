#!/usr/bin/env python3
"""
Manual Category Image Assignment Guide
Step-by-step instructions for setting images in WordPress admin
"""

WORDPRESS_URL = 'https://spherevista360.com'

# Category images mapping
CATEGORIES = {
    'Finance': {'id': 3, 'media_id': 2744, 'slug': 'finance'},
    'Technology': {'id': 190, 'media_id': 2746, 'slug': 'technology'},
    'Business': {'id': 188, 'media_id': 2741, 'slug': 'business'},
    'Entertainment': {'id': 167, 'media_id': 2743, 'slug': 'entertainment'},
    'Politics': {'id': 5, 'media_id': 2745, 'slug': 'politics'},
    'Travel': {'id': 6, 'media_id': 2748, 'slug': 'travel'},
    'World': {'id': 7, 'media_id': 2749, 'slug': 'world'},
    'World News': {'id': 213, 'media_id': 2750, 'slug': 'world-news'},
    'Economy': {'id': 165, 'media_id': 2742, 'slug': 'economy'},
    'Top Stories': {'id': 177, 'media_id': 2747, 'slug': 'top-stories'},
}

def main():
    print("=" * 80)
    print("📝 MANUAL CATEGORY IMAGE ASSIGNMENT GUIDE")
    print("=" * 80)
    print()
    
    print("The 'Categories Images' plugin requires manual image assignment.")
    print("Follow these steps for EACH category:")
    print()
    
    print("=" * 80)
    print("🎯 STEP-BY-STEP INSTRUCTIONS")
    print("=" * 80)
    print()
    
    for i, (cat_name, cat_info) in enumerate(CATEGORIES.items(), 1):
        print(f"\n{'='*80}")
        print(f"CATEGORY {i}/10: {cat_name}")
        print('='*80)
        
        print(f"\n1. Open this link in your browser:")
        print(f"   {WORDPRESS_URL}/wp-admin/term.php?taxonomy=category&tag_ID={cat_info['id']}&post_type=post")
        print()
        
        print(f"2. Scroll down to find the image upload section")
        print(f"   (Look for 'Image', 'Category Image', or 'Thumbnail' field)")
        print()
        
        print(f"3. Click 'Upload/Add image' or 'Select Image' button")
        print()
        
        print(f"4. In the media library popup:")
        print(f"   - Search for media ID: {cat_info['media_id']}")
        print(f"   - OR look for recently uploaded category images")
        print(f"   - OR search for '{cat_name.lower()}' in the search box")
        print()
        
        print(f"5. Select the image and click 'Select' or 'Set category image'")
        print()
        
        print(f"6. Click 'Update' button to save")
        print()
        
        print(f"7. Verify: Visit {WORDPRESS_URL}/category/{cat_info['slug']}/")
        print()
    
    print("\n" + "=" * 80)
    print("🔍 IF YOU DON'T SEE IMAGE UPLOAD FIELD")
    print("=" * 80)
    print()
    
    print("The plugin might not be configured correctly. Try this:")
    print()
    
    print("1. Check plugin settings:")
    print(f"   {WORDPRESS_URL}/wp-admin/plugins.php")
    print("   Make sure 'Categories Images' is activated")
    print()
    
    print("2. Try deactivating and reactivating the plugin:")
    print("   - Go to Plugins")
    print("   - Deactivate 'Categories Images'")
    print("   - Activate it again")
    print("   - Go back to Posts → Categories")
    print()
    
    print("3. Check if it's a different plugin:")
    print("   Some plugins have different names:")
    print("   - 'Category and Taxonomy Image'")
    print("   - 'Simple Term Meta'")
    print("   - 'Advanced Custom Fields' (ACF)")
    print()
    
    print("4. Install a different plugin if needed:")
    print(f"   {WORDPRESS_URL}/wp-admin/plugin-install.php")
    print("   Search for: 'Category and Taxonomy Image'")
    print("   This plugin is known to work well")
    print()
    
    print("=" * 80)
    print("📸 QUICK REFERENCE - MEDIA IDs")
    print("=" * 80)
    print()
    
    for cat_name, cat_info in sorted(CATEGORIES.items()):
        print(f"   {cat_name:20s} → Media ID: {cat_info['media_id']}")
    
    print()
    print("=" * 80)
    print("🎯 ALTERNATIVE: Use Kadence Theme Features")
    print("=" * 80)
    print()
    
    print("Kadence theme has built-in category customization:")
    print()
    print(f"1. Go to: {WORDPRESS_URL}/wp-admin/customize.php")
    print("2. Navigate to: Content → Archive")
    print("3. Look for category archive settings")
    print("4. Enable category featured images")
    print()
    
    print("OR check Kadence documentation:")
    print("https://www.kadencewp.com/docs/")
    print()
    
    print("=" * 80)
    print()
    
    # Create a simple HTML page with clickable links
    create_html_guide()

def create_html_guide():
    """Create an HTML page with clickable links"""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Category Images Setup Guide</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .category {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .category h2 {
            color: #0073aa;
            margin-top: 0;
        }
        .btn {
            display: inline-block;
            background: #0073aa;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            margin: 10px 10px 10px 0;
        }
        .btn:hover {
            background: #005a87;
        }
        .media-id {
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 4px;
            font-family: monospace;
            font-weight: bold;
        }
        .instructions {
            background: #fffbcc;
            padding: 15px;
            border-left: 4px solid #ffeb3b;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <h1>🖼️ Category Images Setup Guide</h1>
    
    <div class="instructions">
        <strong>Instructions:</strong>
        <ol>
            <li>Click "Edit Category" button below</li>
            <li>Look for image upload field in the category edit page</li>
            <li>Click "Upload/Add image" button</li>
            <li>Search for the Media ID shown below or browse recent uploads</li>
            <li>Select the image and click "Update"</li>
            <li>Click "View Category" to verify the image appears</li>
        </ol>
    </div>
"""
    
    for cat_name, cat_info in CATEGORIES.items():
        html_content += f"""
    <div class="category">
        <h2>{cat_name}</h2>
        <p><strong>Media ID:</strong> <span class="media-id">{cat_info['media_id']}</span></p>
        <a href="{WORDPRESS_URL}/wp-admin/term.php?taxonomy=category&tag_ID={cat_info['id']}&post_type=post" 
           class="btn" target="_blank">
            ✏️ Edit Category
        </a>
        <a href="{WORDPRESS_URL}/category/{cat_info['slug']}/" 
           class="btn" target="_blank">
            👁️ View Category Page
        </a>
    </div>
"""
    
    html_content += """
    <div class="instructions">
        <h3>Troubleshooting</h3>
        <p>If you don't see an image upload field:</p>
        <ul>
            <li>Make sure the "Categories Images" plugin is activated</li>
            <li>Try deactivating and reactivating the plugin</li>
            <li>Install "Category and Taxonomy Image" plugin instead</li>
            <li>Check Kadence theme documentation for built-in category image support</li>
        </ul>
    </div>
    
    <div style="text-align: center; margin-top: 40px; color: #666;">
        <p>Generated: October 13, 2025</p>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    with open('/home/kddevops/downloads/category_images_setup.html', 'w') as f:
        f.write(html_content)
    
    print("💾 Created HTML guide: /home/kddevops/downloads/category_images_setup.html")
    print("   Open this file in your browser for easy access to all edit links!")
    print()

if __name__ == '__main__':
    main()
