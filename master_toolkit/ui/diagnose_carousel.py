#!/usr/bin/env python3
"""
Diagnose Carousel Issues
Check homepage setup, carousel HTML, and category images
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def check_homepage_settings():
    """Check what page is set as homepage"""
    print("1️⃣  HOMEPAGE SETTINGS")
    print("-" * 70)
    
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/settings"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        settings = response.json()
        show_on_front = settings.get('show_on_front', 'posts')
        page_on_front = settings.get('page_on_front', 0)
        page_for_posts = settings.get('page_for_posts', 0)
        
        print(f"   Show on front: {show_on_front}")
        print(f"   Page on front ID: {page_on_front}")
        print(f"   Page for posts ID: {page_for_posts}")
        
        if show_on_front == 'posts':
            print("   ⚠️  Homepage is set to show LATEST POSTS (blog mode)")
            print("   ⚠️  This means no static homepage with carousel!")
            return False, None
        else:
            print("   ✅ Homepage is set to STATIC PAGE")
            return True, page_on_front
    else:
        print(f"   ❌ Failed to get settings: {response.status_code}")
        return False, None

def check_homepage_content(page_id):
    """Check the content of the homepage"""
    print("\n2️⃣  HOMEPAGE CONTENT")
    print("-" * 70)
    
    if not page_id:
        print("   ⚠️  No homepage ID provided")
        return False
    
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{page_id}"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        page = response.json()
        title = page['title']['rendered']
        content = page['content']['rendered']
        
        print(f"   Page Title: {title}")
        print(f"   Page ID: {page_id}")
        print(f"   Content Length: {len(content)} characters")
        
        # Check for carousel-related code
        has_carousel_container = 'category-carousel-container' in content
        has_carousel_class = 'category-carousel' in content
        has_carousel_style = '<style>' in content and 'carousel' in content
        has_carousel_script = '<script>' in content and 'carousel' in content
        
        print(f"\n   Carousel Elements:")
        print(f"      Container div: {'✅ Found' if has_carousel_container else '❌ Missing'}")
        print(f"      Carousel class: {'✅ Found' if has_carousel_class else '❌ Missing'}")
        print(f"      CSS styles: {'✅ Found' if has_carousel_style else '❌ Missing'}")
        print(f"      JavaScript: {'✅ Found' if has_carousel_script else '❌ Missing'}")
        
        # Check for images
        img_count = content.count('<img')
        print(f"\n   Image Count: {img_count} images")
        
        if img_count == 0:
            print("   ❌ NO IMAGES FOUND IN CAROUSEL!")
            print("   Problem: Carousel has no category images")
            return False
        else:
            print(f"   ✅ Found {img_count} images")
        
        # Show sample content
        if len(content) > 0:
            print(f"\n   Content Preview (first 300 chars):")
            print(f"   {content[:300]}...")
        
        return has_carousel_container and img_count > 0
    else:
        print(f"   ❌ Failed to get page: {response.status_code}")
        return False

def check_category_images():
    """Check if categories have images assigned"""
    print("\n3️⃣  CATEGORY IMAGES")
    print("-" * 70)
    
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/categories"
    params = {'per_page': 20}
    
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        categories = response.json()
        
        categories_with_images = 0
        categories_without_images = 0
        
        for cat in categories:
            cat_id = cat['id']
            cat_name = cat['name']
            
            # Check for category image in meta
            meta_url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/categories/{cat_id}"
            meta_response = requests.get(
                meta_url,
                auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
            )
            
            if meta_response.status_code == 200:
                cat_data = meta_response.json()
                has_image = 'image' in cat_data or 'category_image' in str(cat_data)
                
                if has_image:
                    categories_with_images += 1
                    print(f"   ✅ {cat_name} (ID: {cat_id})")
                else:
                    categories_without_images += 1
                    print(f"   ⚠️  {cat_name} (ID: {cat_id}) - No image")
        
        print(f"\n   Summary:")
        print(f"      With images: {categories_with_images}")
        print(f"      Without images: {categories_without_images}")
        
        return categories_with_images > 0
    else:
        print(f"   ❌ Failed to get categories: {response.status_code}")
        return False

def check_theme_support():
    """Check if theme supports carousel/homepage customization"""
    print("\n4️⃣  THEME CONFIGURATION")
    print("-" * 70)
    
    # Check active theme
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/themes"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        themes = response.json()
        for theme in themes:
            if theme.get('status') == 'active':
                print(f"   Active Theme: {theme.get('name', {}).get('rendered', 'Unknown')}")
                print(f"   Theme Slug: {theme.get('stylesheet', 'Unknown')}")
                return True
    
    print("   ⚠️  Could not determine active theme")
    return False

def provide_solutions(has_static_homepage, homepage_has_carousel, categories_have_images):
    """Provide solutions based on diagnostic results"""
    print("\n" + "=" * 70)
    print("💡 DIAGNOSIS & SOLUTIONS")
    print("=" * 70)
    
    issues = []
    solutions = []
    
    if not has_static_homepage:
        issues.append("Homepage is showing latest posts instead of static page")
        solutions.append("""
    SOLUTION 1: Set Static Homepage
    
    Run this command:
    python3 activate_carousel_via_api.py
    
    Or manually in WordPress:
    1. Go to Settings → Reading
    2. Select "A static page" for "Your homepage displays"
    3. Choose "Home" or create a new "Home" page
    4. Save changes
        """)
    
    if not homepage_has_carousel:
        issues.append("Homepage doesn't have carousel HTML/images")
        solutions.append("""
    SOLUTION 2: Add Carousel to Homepage
    
    Run this command:
    python3 create_category_carousel.py
    
    This will generate carousel HTML. Then:
    1. Copy the generated HTML
    2. Go to Pages → Home → Edit
    3. Paste the HTML in the content area
    4. Update the page
        """)
    
    if not categories_have_images:
        issues.append("Categories don't have images assigned")
        solutions.append("""
    SOLUTION 3: Assign Category Images
    
    Run this command:
    python3 assign_category_images.py
    
    Or manually:
    1. Upload images to Media Library
    2. Use a plugin like "Categories Images" or "Category Icon"
    3. Assign images to each category
        """)
    
    if not issues:
        print("\n✅ NO MAJOR ISSUES FOUND!")
        print("\nIf carousel still not showing, check:")
        print("   • Clear browser cache (Ctrl+F5)")
        print("   • Clear WordPress cache plugin")
        print("   • Check browser console for JavaScript errors (F12)")
        print("   • Verify images are loading (check image URLs)")
    else:
        print("\n⚠️  ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n📋 RECOMMENDED SOLUTIONS:")
        for solution in solutions:
            print(solution)

def main():
    print("=" * 70)
    print("🔍 CAROUSEL DIAGNOSTIC TOOL")
    print("=" * 70)
    print()
    
    if not all([WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("❌ Error: Missing WordPress credentials in .env file")
        return
    
    print(f"🌐 Site: {WORDPRESS_BASE_URL}")
    print()
    
    # Run diagnostics
    has_static_homepage, homepage_id = check_homepage_settings()
    homepage_has_carousel = False
    
    if homepage_id:
        homepage_has_carousel = check_homepage_content(homepage_id)
    
    categories_have_images = check_category_images()
    check_theme_support()
    
    # Provide solutions
    provide_solutions(has_static_homepage, homepage_has_carousel, categories_have_images)
    
    print("\n" + "=" * 70)
    print("✅ Diagnostic complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
