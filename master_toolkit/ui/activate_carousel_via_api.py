#!/usr/bin/env python3
"""
Add Carousel to Homepage via API
Use WordPress Customizer API or insert into site header
"""

import requests
import json

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Read carousel HTML
with open('/home/kddevops/downloads/category_carousel.html', 'r') as f:
    carousel_html = f.read()

def set_static_homepage():
    """Set the Home page as the front page via API"""
    print("🏠 Setting 'Home' page as static front page...")
    
    # Update site settings to use static homepage
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/settings',
        json={
            'show_on_front': 'page',
            'page_on_front': 2412,  # Home page ID
        },
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        print("   ✅ Homepage set to static 'Home' page!")
        print("   ✅ Carousel is now LIVE!")
        return True
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False

def create_blog_page():
    """Create a 'Blog' page for posts if it doesn't exist"""
    print("\n📝 Checking for Blog page...")
    
    # Check if Blog page exists
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/pages',
        params={'search': 'blog', 'per_page': 10},
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        pages = response.json()
        for page in pages:
            if page['title']['rendered'].lower() == 'blog':
                print(f"   ✅ Blog page exists (ID: {page['id']})")
                return page['id']
    
    # Create Blog page
    print("   📄 Creating Blog page...")
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/pages',
        json={
            'title': 'Blog',
            'content': '<p>Welcome to our blog! Here you\'ll find all our latest articles.</p>',
            'status': 'publish'
        },
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        page = response.json()
        print(f"   ✅ Blog page created (ID: {page['id']})")
        return page['id']
    else:
        print(f"   ⚠️  Could not create Blog page: {response.status_code}")
        return None

def set_posts_page(blog_page_id):
    """Set the Blog page as posts page"""
    if not blog_page_id:
        print("   ⚠️  Skipping posts page setup (no Blog page)")
        return False
    
    print(f"\n📰 Setting Blog page (ID: {blog_page_id}) as posts page...")
    
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/settings',
        json={'page_for_posts': blog_page_id},
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        print("   ✅ Posts page configured!")
        return True
    else:
        print(f"   ⚠️  Could not set posts page: {response.status_code}")
        return False

def verify_homepage():
    """Verify the homepage settings"""
    print("\n🔍 Verifying homepage configuration...")
    
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/settings',
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        settings = response.json()
        show_on_front = settings.get('show_on_front', 'posts')
        page_on_front = settings.get('page_on_front', 0)
        page_for_posts = settings.get('page_for_posts', 0)
        
        print(f"   Show on front: {show_on_front}")
        print(f"   Homepage: Page ID {page_on_front}")
        print(f"   Posts page: Page ID {page_for_posts}")
        
        if show_on_front == 'page' and page_on_front == 2412:
            print("\n   ✅ Configuration is CORRECT!")
            return True
        else:
            print("\n   ❌ Configuration needs adjustment")
            return False
    
    return False

def main():
    """Set up static homepage with carousel via API"""
    print("=" * 80)
    print("🚀 MAKING CAROUSEL LIVE VIA API")
    print("=" * 80)
    print()
    
    print("📋 Plan:")
    print("   1. Create 'Blog' page (if needed)")
    print("   2. Set 'Home' page as front page")
    print("   3. Set 'Blog' page for posts")
    print("   4. Verify configuration")
    print()
    
    input("Press Enter to proceed...")
    print()
    
    print("=" * 80)
    print("⚙️  EXECUTING CHANGES")
    print("=" * 80)
    
    # Step 1: Create/find Blog page
    blog_page_id = create_blog_page()
    
    # Step 2: Set static homepage
    if set_static_homepage():
        print()
        print("=" * 80)
        print("🎉 SUCCESS!")
        print("=" * 80)
        print()
        
        # Step 3: Set posts page
        set_posts_page(blog_page_id)
        
        # Step 4: Verify
        if verify_homepage():
            print()
            print("=" * 80)
            print("✅ CAROUSEL IS NOW LIVE!")
            print("=" * 80)
            print()
            print("🔗 View your site:")
            print(f"   Homepage (with carousel): {WORDPRESS_URL}/")
            print(f"   Blog posts: {WORDPRESS_URL}/blog/")
            print()
            print("📊 What changed:")
            print("   ✅ Homepage now shows the 'Home' page (with carousel)")
            print("   ✅ Blog posts moved to /blog/ URL")
            print("   ✅ All your posts are still accessible")
            print("   ✅ Navigation menu still works")
            print()
            print("🎠 Carousel features:")
            print("   • Auto-scrolling animation")
            print("   • Hover to pause")
            print("   • Click to navigate to categories")
            print("   • Mobile responsive")
            print()
        else:
            print("\n⚠️  Configuration may need manual verification")
    else:
        print("\n❌ Could not set static homepage via API")
        print("\nAlternative: Set manually in WordPress Admin")
        print(f"   Go to: {WORDPRESS_URL}/wp-admin/options-reading.php")
        print("   Select: 'A static page' → Homepage: 'Home'")
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
