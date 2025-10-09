#!/usr/bin/env python3
"""
Fix Broken Links Script
======================
Script to fix the 5 known broken links on spherevista360.com
"""

import sys
import os
sys.path.append('.')
sys.path.append('./master_toolkit')

from master_toolkit.validation.links import LinkValidator
from master_toolkit.core.client import WordPressClient

def fix_broken_links():
    """Fix all broken links with authentication."""
    
    print("🔧 BROKEN LINKS FIXER")
    print("=" * 50)
    
    # Initialize WordPress client
    wp_client = WordPressClient("https://spherevista360.com")
    
    # Get credentials
    username = input("Enter WordPress username: ")
    password = input("Enter WordPress password: ")
    
    # Authenticate
    try:
        wp_client.authenticate(username, password)
        print("✅ Authentication successful!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    # Create link validator
    link_validator = LinkValidator(wp_client)
    
    print("\n🔍 Scanning for broken links...")
    
    # Option 1: Fix all posts
    print("\nChoose fixing option:")
    print("1. Fix all posts (recommended)")
    print("2. Test run (dry run)")
    print("3. Fix specific posts")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        # Fix all broken links
        print("\n🔧 Fixing all broken links...")
        result = link_validator.fix_all_broken_links(dry_run=False)
        
    elif choice == "2":
        # Dry run - see what would be fixed
        print("\n👀 Dry run - showing what would be fixed...")
        result = link_validator.fix_all_broken_links(dry_run=True)
        
    elif choice == "3":
        # Fix specific posts
        post_ids_str = input("Enter post IDs (comma-separated): ")
        try:
            post_ids = [int(x.strip()) for x in post_ids_str.split(',')]
            print(f"\n🔧 Fixing posts: {post_ids}")
            result = link_validator.fix_all_broken_links(post_ids=post_ids, dry_run=False)
        except ValueError:
            print("❌ Invalid post IDs")
            return
    else:
        print("❌ Invalid choice")
        return
    
    # Show results
    print("\n" + "=" * 50)
    print("📊 FIXING RESULTS")
    print("=" * 50)
    print(f"Posts processed: {result.get('posts_processed', 0)}")
    print(f"Posts fixed: {result.get('fixed_posts', 0)}")
    print(f"Total fixes: {result.get('total_fixes', 0)}")
    
    if result.get('total_fixes', 0) > 0:
        print("\n✅ Broken links have been fixed!")
        print("\n🔍 Verifying fixes...")
        
        # Verify the fixes worked
        verify_result = link_validator.verify_fixes()
        print(f"Verification: {verify_result.get('message', 'Complete')}")
    else:
        print("\n ℹ️ No broken links found to fix")

if __name__ == "__main__":
    fix_broken_links()