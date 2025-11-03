#!/usr/bin/env python3
"""
Update WordPress footer menu with professional layout
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def get_menus():
    """Get all menus"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menus"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        return response.json()
    return []

def get_page_id_by_slug(slug):
    """Get page ID by slug"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages"
    params = {'slug': slug, 'per_page': 1}
    
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        pages = response.json()
        return pages[0]['id'] if pages else None
    return None

def get_or_create_footer_menu():
    """Get or create footer menu"""
    menus = get_menus()
    
    # Check if footer menu exists
    for menu in menus:
        if 'footer' in menu['name'].lower():
            print(f"   Found existing footer menu: {menu['name']} (ID: {menu['id']})")
            return menu['id']
    
    # Create new footer menu
    print("   Creating new footer menu...")
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menus"
    data = {
        'name': 'Footer Menu',
        'slug': 'footer-menu',
        'description': 'Professional footer navigation menu',
        'locations': ['footer']
    }
    
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 201:
        menu = response.json()
        print(f"   ✅ Created footer menu (ID: {menu['id']})")
        return menu['id']
    else:
        print(f"   ❌ Failed to create menu: {response.status_code}")
        return None

def clear_menu_items(menu_id):
    """Clear all items from a menu"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items"
    params = {'menus': menu_id, 'per_page': 100}
    
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        items = response.json()
        for item in items:
            delete_url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items/{item['id']}"
            requests.delete(
                delete_url,
                auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
            )
        print(f"   Cleared {len(items)} existing menu items")

def add_menu_item(menu_id, title, object_id=None, url=None, parent=0, menu_order=0):
    """Add a menu item"""
    api_url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items"
    
    data = {
        'title': title,
        'menu_order': menu_order,
        'menus': menu_id,
        'parent': parent,
        'status': 'publish'
    }
    
    if object_id:
        data['object_id'] = object_id
        data['object'] = 'page'
        data['type'] = 'post_type'
    elif url:
        data['url'] = url
        data['type'] = 'custom'
    
    response = requests.post(
        api_url,
        json=data,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 201:
        return response.json()
    else:
        print(f"   ❌ Failed to add menu item '{title}': {response.status_code}")
        return None

def create_professional_footer_menu():
    """Create a professional footer menu structure"""
    
    print("\n🔍 Getting page IDs...")
    print("-" * 70)
    
    # Get page IDs
    pages = {
        'about': get_page_id_by_slug('about-us'),
        'contact': get_page_id_by_slug('contact'),
        'privacy': get_page_id_by_slug('privacy-policy'),
        'terms': get_page_id_by_slug('terms-of-service'),
        'disclaimer': get_page_id_by_slug('disclaimer')
    }
    
    for key, page_id in pages.items():
        if page_id:
            print(f"   ✅ {key.title()}: ID {page_id}")
        else:
            print(f"   ⚠️  {key.title()}: Not found")
    
    print("\n📋 Setting up footer menu...")
    print("-" * 70)
    
    # Get or create footer menu
    menu_id = get_or_create_footer_menu()
    if not menu_id:
        return False
    
    # Clear existing items
    clear_menu_items(menu_id)
    
    print("\n➕ Adding menu items...")
    print("-" * 70)
    
    # Define professional menu structure
    menu_structure = []
    
    # Company Section
    menu_structure.append({
        'title': 'Company',
        'menu_order': 1,
        'children': [
            {'title': 'About Us', 'page_id': pages['about'], 'order': 2},
            {'title': 'Contact', 'page_id': pages['contact'], 'order': 3}
        ]
    })
    
    # Legal Section
    menu_structure.append({
        'title': 'Legal',
        'menu_order': 4,
        'children': [
            {'title': 'Privacy Policy', 'page_id': pages['privacy'], 'order': 5},
            {'title': 'Terms of Service', 'page_id': pages['terms'], 'order': 6},
            {'title': 'Disclaimer', 'page_id': pages['disclaimer'], 'order': 7}
        ]
    })
    
    # Add menu items
    created_items = []
    
    for section in menu_structure:
        # Add parent item (section header)
        parent_item = add_menu_item(
            menu_id,
            section['title'],
            url='#',
            menu_order=section['menu_order']
        )
        
        if parent_item:
            print(f"   ✅ Added section: {section['title']}")
            created_items.append(parent_item)
            
            # Add child items
            for child in section.get('children', []):
                if child['page_id']:
                    child_item = add_menu_item(
                        menu_id,
                        child['title'],
                        object_id=child['page_id'],
                        parent=parent_item['id'],
                        menu_order=child['order']
                    )
                    if child_item:
                        print(f"      ↳ {child['title']}")
                        created_items.append(child_item)
    
    return len(created_items) > 0

def create_simple_footer_menu():
    """Create a simple flat footer menu if hierarchical fails"""
    
    print("\n📋 Creating simple footer menu...")
    print("-" * 70)
    
    # Get or create footer menu
    menu_id = get_or_create_footer_menu()
    if not menu_id:
        return False
    
    # Clear existing items
    clear_menu_items(menu_id)
    
    # Get page IDs
    pages = {
        'About Us': get_page_id_by_slug('about-us'),
        'Contact': get_page_id_by_slug('contact'),
        'Privacy Policy': get_page_id_by_slug('privacy-policy'),
        'Terms of Service': get_page_id_by_slug('terms-of-service'),
        'Disclaimer': get_page_id_by_slug('disclaimer')
    }
    
    print("\n➕ Adding menu items...")
    print("-" * 70)
    
    menu_order = 1
    created_items = 0
    
    for title, page_id in pages.items():
        if page_id:
            item = add_menu_item(menu_id, title, object_id=page_id, menu_order=menu_order)
            if item:
                print(f"   ✅ {title}")
                created_items += 1
                menu_order += 1
        else:
            print(f"   ⚠️  Skipped {title} (page not found)")
    
    return created_items > 0

def verify_footer_menu():
    """Verify the footer menu was created"""
    menus = get_menus()
    
    for menu in menus:
        if 'footer' in menu['name'].lower():
            # Get menu items
            url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/menu-items"
            params = {'menus': menu['id'], 'per_page': 100}
            
            response = requests.get(
                url,
                params=params,
                auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
            )
            
            if response.status_code == 200:
                items = response.json()
                return menu, items
    
    return None, []

def main():
    print("=" * 70)
    print("SphereVista360 - Footer Menu Setup")
    print("Professional Navigation Structure")
    print("=" * 70)
    
    if not all([WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("\n❌ Error: Missing WordPress credentials in .env file")
        return
    
    print(f"\n🌐 WordPress Site: {WORDPRESS_BASE_URL}")
    
    # Try professional hierarchical menu first
    success = create_professional_footer_menu()
    
    # If that fails, create simple flat menu
    if not success:
        print("\n⚠️  Hierarchical menu failed, creating simple menu...")
        success = create_simple_footer_menu()
    
    # Verify the menu
    if success:
        print("\n🔍 Verifying footer menu...")
        print("-" * 70)
        
        menu, items = verify_footer_menu()
        
        if menu and items:
            print(f"   ✅ Footer menu verified")
            print(f"   Menu ID: {menu['id']}")
            print(f"   Menu Name: {menu['name']}")
            print(f"   Total Items: {len(items)}")
        
        print("\n" + "=" * 70)
        print("✅ Footer menu setup complete!")
        print("=" * 70)
        print("\n📝 Menu Items:")
        
        if items:
            for item in sorted(items, key=lambda x: x['menu_order']):
                indent = "   " if item.get('parent', 0) == 0 else "      ↳ "
                print(f"{indent}{item['title']}")
        
        print("\n🎯 Next Steps:")
        print("   1. Go to WordPress Admin → Appearance → Menus")
        print("   2. Assign the 'Footer Menu' to your footer location")
        print("   3. Verify the menu displays correctly on your site")
        print("   4. Test all links to ensure they work")
        print("\n" + "=" * 70)
    else:
        print("\n❌ Footer menu setup failed!")
        print("=" * 70)

if __name__ == "__main__":
    main()
