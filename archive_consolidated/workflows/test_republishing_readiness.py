#!/usr/bin/env python3
"""
Basic Content Validation Workflow
=================================
Test and validate content using available tools (no external dependencies).
"""

import os
import sys
from pathlib import Path

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent / 'wp_tools'))

from wp_client import WordPressClient, print_header, print_section


def run_duplicate_check():
    """Run comprehensive duplicate checking."""
    print_section("DUPLICATE CONTENT CHECK")
    
    print("🔍 Running duplicate checker...")
    result = os.system("python3 wp_tools/duplicate_checker.py --all")
    
    if result == 0:
        print("✅ Duplicate check completed successfully")
        return True
    else:
        print("❌ Duplicate check failed")
        return False


def check_content_inventory():
    """Check available content for publishing."""
    print_section("CONTENT INVENTORY CHECK")
    
    content_dir = "content_to_publish"
    
    if not os.path.exists(content_dir):
        print(f"❌ Content directory '{content_dir}' not found!")
        return False
    
    categories = {}
    total_files = 0
    
    for item in os.listdir(content_dir):
        item_path = os.path.join(content_dir, item)
        
        if os.path.isdir(item_path):
            md_files = [f for f in os.listdir(item_path) if f.endswith('.md')]
            if md_files:
                categories[item] = len(md_files)
                total_files += len(md_files)
    
    print(f"📊 CONTENT SUMMARY:")
    print(f"   📁 Categories: {len(categories)}")
    print(f"   📄 Total files: {total_files}")
    
    print(f"\n📋 CATEGORY BREAKDOWN:")
    for category, count in sorted(categories.items()):
        print(f"   📂 {category}: {count} posts")
    
    return True


def test_wordpress_connection():
    """Test WordPress connection and basic functionality."""
    print_section("WORDPRESS CONNECTION TEST")
    
    try:
        wp_client = WordPressClient()
        
        if not wp_client.authenticate():
            print("❌ WordPress authentication failed")
            return False
        
        print("✅ WordPress authentication successful")
        
        # Test basic API calls
        try:
            posts = wp_client.get_posts(per_page=5)
            print(f"✅ Successfully retrieved {len(posts)} posts")
            
            pages = wp_client.get_pages(per_page=5)
            print(f"✅ Successfully retrieved {len(pages)} pages")
            
            categories = wp_client.get_categories()
            print(f"✅ Successfully retrieved {len(categories)} categories")
            
            return True
            
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


def analyze_current_site_state():
    """Analyze current state of the website."""
    print_section("CURRENT SITE STATE ANALYSIS")
    
    try:
        wp_client = WordPressClient()
        
        if not wp_client.authenticate():
            print("❌ Cannot analyze site - authentication failed")
            return False
        
        # Get content overview
        posts = wp_client.get_posts(per_page=50)
        pages = wp_client.get_pages()
        categories = wp_client.get_categories()
        
        print(f"📊 CURRENT SITE INVENTORY:")
        print(f"   📄 Posts: {len(posts)}")
        print(f"   📃 Pages: {len(pages)}")
        print(f"   📂 Categories: {len(categories)}")
        
        # Analyze categories
        category_counts = {}
        for post in posts:
            for cat_id in post.get('categories', []):
                for cat in categories:
                    if cat['id'] == cat_id:
                        cat_name = cat['name']
                        category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
        
        print(f"\n📋 POSTS BY CATEGORY:")
        for cat_name, count in sorted(category_counts.items()):
            print(f"   📂 {cat_name}: {count} posts")
        
        # Check for Entertainment category specifically
        if 'Entertainment' in category_counts:
            ent_count = category_counts['Entertainment']
            print(f"\n🎭 ENTERTAINMENT CATEGORY STATUS:")
            print(f"   📄 Current posts: {ent_count}")
            print(f"   🎯 This category was previously optimized to 100% SEO")
        
        return True
        
    except Exception as e:
        print(f"❌ Site analysis failed: {e}")
        return False


def generate_publishing_recommendations():
    """Generate recommendations for content publishing."""
    print_section("PUBLISHING RECOMMENDATIONS")
    
    print("📋 RECOMMENDED PUBLISHING WORKFLOW:")
    print()
    
    # Check if dependencies are available
    dependencies_available = False
    try:
        import requests
        import yaml
        import markdown
        dependencies_available = True
    except ImportError:
        pass
    
    if dependencies_available:
        print("✅ OPTION 1: Use new content_publisher.py (Recommended)")
        print("   # Install dependencies first:")
        print("   pip install -r requirements.txt")
        print()
        print("   # Test with dry run:")
        print("   python3 wp_tools/content_publisher.py content_to_publish/Entertainment --dry-run")
        print()
        print("   # Publish Entertainment category:")
        print("   python3 wp_tools/content_publisher.py content_to_publish/Entertainment --category Entertainment")
        print()
    else:
        print("⚠️ OPTION 1: Install dependencies for modern tools")
        print("   pip install -r requirements.txt")
        print()
    
    print("✅ OPTION 2: Use legacy bulk publisher")
    print("   # Use existing wp_agent_bulk.py from archive:")
    print("   python3 archive/old_scripts/wp_agent_bulk.py content_to_publish/Entertainment")
    print()
    
    print("📊 TESTING WORKFLOW:")
    print("   1. Run duplicate checker: python3 wp_tools/duplicate_checker.py --all")
    print("   2. Publish content using preferred method above")
    print("   3. Re-run duplicate checker to ensure no duplicates created")
    print("   4. Install dependencies and run SEO/image validation")


def main():
    """Main testing workflow."""
    
    print_header("CONTENT VALIDATION & PUBLISHING READINESS TEST")
    print("🎯 This test will verify:")
    print("   ✅ WordPress connection and authentication")
    print("   ✅ Current site state and content inventory")
    print("   ✅ Available content for publishing")
    print("   ✅ Duplicate detection functionality")
    print("   📋 Publishing recommendations")
    print()
    
    # Run all tests
    tests = [
        ("WordPress Connection", test_wordpress_connection),
        ("Content Inventory", check_content_inventory),
        ("Site State Analysis", analyze_current_site_state),
        ("Duplicate Check", run_duplicate_check)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Generate recommendations
    generate_publishing_recommendations()
    
    # Final summary
    print_section("TEST RESULTS SUMMARY")
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"📊 OVERALL RESULTS: {passed}/{total} tests passed")
    print()
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ Your setup is ready for content republishing")
        print(f"📋 Follow the publishing recommendations above")
    else:
        print(f"\n⚠️ Some tests failed - review errors above")
        print(f"🔧 Fix issues before proceeding with republishing")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())