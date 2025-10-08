#!/usr/bin/env python3
"""
Delete duplicate pages that have -2 suffix
"""

import requests
import json
from datetime import datetime

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def delete_duplicate_pages():
    print("🗑️ DELETING DUPLICATE PAGES")
    print("=" * 40)
    
    # Pages to delete (the -2 versions)
    pages_to_delete = [
        {"id": 1685, "title": "Disclaimer", "slug": "disclaimer-2"},
        {"id": 1684, "title": "Terms of Service", "slug": "terms-of-service-2"},
        {"id": 1683, "title": "Sitemap", "slug": "sitemap-2"},
        {"id": 1682, "title": "Archives", "slug": "archives-2"},
        {"id": 1681, "title": "Subscribe", "slug": "subscribe-2"},
        {"id": 1680, "title": "Newsletter", "slug": "newsletter-2"}
    ]
    
    print("🎯 PAGES TO DELETE (duplicates with -2 suffix):")
    for page in pages_to_delete:
        print(f"   📄 {page['title']} (ID: {page['id']}, Slug: {page['slug']})")
    
    print("\n⚠️  NOTE: This script will show the deletion process but won't actually")
    print("   delete without authentication. You'll need to do this manually in WordPress admin.")
    
    print("\n" + "=" * 50)
    print("🛠️ MANUAL DELETION STEPS:")
    print("=" * 50)
    
    print("1. Go to WordPress Admin → Pages → All Pages")
    print("2. Delete these duplicate pages:")
    
    for page in pages_to_delete:
        print(f"\n   📄 {page['title']} (ID: {page['id']})")
        print(f"      Slug: {page['slug']}")
        print(f"      URL: https://spherevista360.com/{page['slug']}/")
        print(f"      ❌ DELETE THIS ONE (it's the duplicate)")
    
    print("\n3. Keep these original pages:")
    original_pages = [
        {"id": 1663, "title": "Disclaimer", "slug": "disclaimer"},
        {"id": 1662, "title": "Terms of Service", "slug": "terms-of-service"},
        {"id": 1661, "title": "Sitemap", "slug": "sitemap"},
        {"id": 1660, "title": "Archives", "slug": "archives"},
        {"id": 1659, "title": "Subscribe", "slug": "subscribe"},
        {"id": 1658, "title": "Newsletter", "slug": "newsletter"}
    ]
    
    for page in original_pages:
        print(f"\n   📄 {page['title']} (ID: {page['id']})")
        print(f"      Slug: {page['slug']}")
        print(f"      URL: https://spherevista360.com/{page['slug']}/")
        print(f"      ✅ KEEP THIS ONE (original)")

def check_menu_impact():
    print("\n🧭 AFTER DELETION - CHECK NAVIGATION MENUS:")
    print("=" * 50)
    print("1. Go to WordPress Admin → Appearance → Menus")
    print("2. Check all your navigation menus")
    print("3. Remove any broken links to deleted pages")
    print("4. Ensure the original pages are properly linked")
    
    print("\n🔧 COMMON MENU LOCATIONS TO CHECK:")
    print("   • Header Menu")
    print("   • Footer Menu") 
    print("   • Sidebar Widgets")
    print("   • Footer Widgets")

def verify_after_deletion():
    print("\n✅ VERIFICATION AFTER DELETION:")
    print("=" * 40)
    print("1. Visit your website homepage")
    print("2. Check navigation menus work properly")
    print("3. Test these URLs to ensure they work:")
    
    urls_to_test = [
        "https://spherevista360.com/disclaimer/",
        "https://spherevista360.com/terms-of-service/",
        "https://spherevista360.com/sitemap/",
        "https://spherevista360.com/archives/",
        "https://spherevista360.com/subscribe/",
        "https://spherevista360.com/newsletter/"
    ]
    
    for url in urls_to_test:
        print(f"   🔗 {url}")
    
    print("\n4. Ensure these URLs return 404 (deleted duplicates):")
    deleted_urls = [
        "https://spherevista360.com/disclaimer-2/",
        "https://spherevista360.com/terms-of-service-2/",
        "https://spherevista360.com/sitemap-2/",
        "https://spherevista360.com/archives-2/",
        "https://spherevista360.com/subscribe-2/",
        "https://spherevista360.com/newsletter-2/"
    ]
    
    for url in deleted_urls:
        print(f"   ❌ {url} (should be 404)")

def main():
    print("🔧 DUPLICATE PAGES CLEANUP GUIDE")
    print("=" * 50)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    delete_duplicate_pages()
    check_menu_impact()
    verify_after_deletion()
    
    print("\n" + "=" * 50)
    print("🎉 EXPECTED RESULT:")
    print("After deleting the duplicates, you should only see:")
    print("• One Disclaimer page")
    print("• One Terms of Service page") 
    print("• One Sitemap page")
    print("• One Archives page")
    print("• One Subscribe page")
    print("• One Newsletter page")
    print("\nThis will eliminate the duplicate page issue you're seeing!")

if __name__ == "__main__":
    main()