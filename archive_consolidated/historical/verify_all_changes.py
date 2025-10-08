#!/usr/bin/env python3
"""
Comprehensive verification of WordPress site changes
"""

import requests
import json
from datetime import datetime
import re

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def check_duplicate_pages_deleted():
    print("🗑️ CHECKING DUPLICATE PAGES DELETION")
    print("=" * 45)
    
    # Pages that should be deleted (the -2 versions)
    deleted_pages = [
        {"id": 1685, "name": "Disclaimer-2", "url": "/disclaimer-2/"},
        {"id": 1684, "name": "Terms of Service-2", "url": "/terms-of-service-2/"},
        {"id": 1683, "name": "Sitemap-2", "url": "/sitemap-2/"},
        {"id": 1682, "name": "Archives-2", "url": "/archives-2/"},
        {"id": 1681, "name": "Subscribe-2", "url": "/subscribe-2/"}
    ]
    
    all_deleted = True
    
    for page in deleted_pages:
        print(f"\n📄 Checking {page['name']} (ID: {page['id']})")
        
        try:
            # Check via API
            response = requests.get(f"{WP_API_BASE}/pages/{page['id']}")
            if response.status_code == 404:
                print(f"   ✅ API: Page deleted (404)")
            else:
                print(f"   ❌ API: Page still exists ({response.status_code})")
                all_deleted = False
            
            # Check via direct URL
            response = requests.get(f"{SITE_URL}{page['url']}")
            if response.status_code == 404:
                print(f"   ✅ URL: Returns 404 (deleted)")
            else:
                print(f"   ❌ URL: Still accessible ({response.status_code})")
                all_deleted = False
                
        except Exception as e:
            print(f"   💥 Error checking {page['name']}: {e}")
    
    return all_deleted

def check_remaining_pages():
    print("\n✅ CHECKING REMAINING PAGES")
    print("=" * 35)
    
    # Pages that should still exist
    remaining_pages = [
        {"id": 1663, "name": "Disclaimer", "url": "/disclaimer/"},
        {"id": 1662, "name": "Terms of Service", "url": "/terms-of-service/"},
        {"id": 1661, "name": "Sitemap", "url": "/sitemap/"},
        {"id": 1660, "name": "Archives", "url": "/archives/"},
        {"id": 1659, "name": "Subscribe", "url": "/subscribe/"},
        {"id": 1658, "name": "Newsletter", "url": "/newsletter/"},
        {"id": 1686, "name": "Homepage", "url": "/homepage/"}
    ]
    
    all_exist = True
    
    for page in remaining_pages:
        print(f"\n📄 Checking {page['name']} (ID: {page['id']})")
        
        try:
            response = requests.get(f"{WP_API_BASE}/pages/{page['id']}")
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', {}).get('rendered', 'No Title')
                print(f"   ✅ Exists: {title}")
                print(f"   🔗 URL: {data.get('link', 'Unknown')}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                all_exist = False
                
        except Exception as e:
            print(f"   💥 Error: {e}")
            all_exist = False
    
    return all_exist

def check_newsletter_seo():
    print("\n📧 CHECKING NEWSLETTER PAGE SEO")
    print("=" * 40)
    
    try:
        response = requests.get(f"{WP_API_BASE}/pages/1658")
        if response.status_code == 200:
            data = response.json()
            
            title = data.get('title', {}).get('rendered', '')
            content = data.get('content', {}).get('rendered', '')
            excerpt = data.get('excerpt', {}).get('rendered', '')
            
            print(f"📝 Title: {title}")
            print(f"📊 Content length: {len(content)} characters")
            print(f"📋 Excerpt length: {len(excerpt)} characters")
            
            # Check for SEO improvements
            seo_checks = {
                "Has optimized title": "Stay Updated with SphereVista360 Insights" in title,
                "Has H2 headings": "<h2>" in content,
                "Has internal links": "<a href=" in content,
                "Has excerpt": len(excerpt.strip()) > 0,
                "Content substantial": len(content) > 2000
            }
            
            print(f"\n🔍 SEO Analysis:")
            for check, passed in seo_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            # Count internal links
            link_count = content.count('<a href=')
            print(f"   🔗 Internal links found: {link_count}")
            
            return all(seo_checks.values())
        else:
            print(f"❌ Could not access Newsletter page: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Error checking Newsletter: {e}")
        return False

def check_homepage_seo():
    print("\n🏠 CHECKING HOMEPAGE SEO")
    print("=" * 30)
    
    try:
        response = requests.get(f"{WP_API_BASE}/pages/1686")
        if response.status_code == 200:
            data = response.json()
            
            title = data.get('title', {}).get('rendered', '')
            content = data.get('content', {}).get('rendered', '')
            excerpt = data.get('excerpt', {}).get('rendered', '')
            
            print(f"📝 Title: {title}")
            print(f"📊 Content length: {len(content)} characters")
            print(f"📋 Excerpt length: {len(excerpt)} characters")
            
            # Check for SEO improvements
            seo_checks = {
                "Has optimized title": "Global Perspectives" in title,
                "Has H2 headings": "<h2>" in content,
                "Has internal links": "<a href=" in content,
                "Has excerpt": len(excerpt.strip()) > 0,
                "Content substantial": len(content) > 2000
            }
            
            print(f"\n🔍 SEO Analysis:")
            for check, passed in seo_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            # Count internal links
            link_count = content.count('<a href=')
            print(f"   🔗 Internal links found: {link_count}")
            
            return all(seo_checks.values())
        else:
            print(f"❌ Could not access Homepage: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Error checking Homepage: {e}")
        return False

def check_site_accessibility():
    print("\n🌐 CHECKING SITE ACCESSIBILITY")
    print("=" * 35)
    
    # Test main pages
    pages_to_test = [
        {"url": "/", "name": "Homepage"},
        {"url": "/newsletter/", "name": "Newsletter"},
        {"url": "/disclaimer/", "name": "Disclaimer"},
        {"url": "/archives/", "name": "Archives"}
    ]
    
    all_accessible = True
    
    for page in pages_to_test:
        print(f"\n🔗 Testing {page['name']}: {SITE_URL}{page['url']}")
        
        try:
            response = requests.get(f"{SITE_URL}{page['url']}")
            if response.status_code == 200:
                print(f"   ✅ Accessible ({response.status_code})")
                
                # Check if page loads properly
                content_length = len(response.text)
                print(f"   📊 Content size: {content_length} bytes")
                
                if content_length < 1000:
                    print(f"   ⚠️  Content seems short - possible error page")
                    all_accessible = False
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                all_accessible = False
                
        except Exception as e:
            print(f"   💥 Error: {e}")
            all_accessible = False
    
    return all_accessible

def check_comments_status():
    print("\n💬 CHECKING COMMENTS STATUS")
    print("=" * 35)
    
    # Check if the comment issue was resolved
    try:
        response = requests.get(f"{WP_API_BASE}/comments")
        if response.status_code == 200:
            comments = response.json()
            print(f"📊 Public comments accessible: {len(comments)}")
            
            if len(comments) == 0:
                print("📋 Still no public comments visible via API")
                print("   This might be normal if comments require authentication")
            else:
                print("✅ Comments are now accessible")
                
        else:
            print(f"❌ Comments API error: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Error checking comments: {e}")

def overall_health_check():
    print("\n🏥 OVERALL SITE HEALTH CHECK")
    print("=" * 40)
    
    health_checks = []
    
    # Run all checks
    duplicates_deleted = check_duplicate_pages_deleted()
    remaining_exist = check_remaining_pages()
    newsletter_seo = check_newsletter_seo()
    homepage_seo = check_homepage_seo()
    site_accessible = check_site_accessibility()
    
    health_checks = [
        ("Duplicate pages deleted", duplicates_deleted),
        ("Remaining pages exist", remaining_exist),
        ("Newsletter SEO optimized", newsletter_seo),
        ("Homepage SEO optimized", homepage_seo),
        ("Site accessibility", site_accessible)
    ]
    
    print(f"\n📊 HEALTH SUMMARY:")
    total_checks = len(health_checks)
    passed_checks = sum(1 for _, passed in health_checks if passed)
    
    for check_name, passed in health_checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
    
    print(f"\n🎯 OVERALL SCORE: {passed_checks}/{total_checks} ({(passed_checks/total_checks)*100:.1f}%)")
    
    if passed_checks == total_checks:
        print("🎉 ALL CHECKS PASSED - Site is fully optimized!")
    elif passed_checks >= total_checks * 0.8:
        print("👍 Most checks passed - Site is in good shape!")
    else:
        print("⚠️  Some issues need attention")

def main():
    print("🔍 WORDPRESS SITE VERIFICATION")
    print("=" * 40)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Checking all recent changes and optimizations")
    print()
    
    overall_health_check()
    check_comments_status()
    
    print("\n" + "=" * 50)
    print("📋 VERIFICATION COMPLETE")
    print("=" * 50)
    print("Check the results above to see what's working and what needs attention.")

if __name__ == "__main__":
    main()