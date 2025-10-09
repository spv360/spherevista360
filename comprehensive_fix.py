#!/usr/bin/env python3
"""
Comprehensive Link Fixer
========================
Fix broken links using the comprehensive validation system
"""

import sys
sys.path.append('.')
sys.path.append('./master_toolkit')

from master_toolkit.validation.comprehensive import ComprehensiveValidator
from master_toolkit.core.client import WordPressClient

def comprehensive_fix():
    """Fix all issues including broken links."""
    
    print("🔧 COMPREHENSIVE WEBSITE FIXER")
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
    
    # Create comprehensive validator
    validator = ComprehensiveValidator(wp_client)
    
    print("\n🔍 Running comprehensive validation and fixes...")
    
    # Choose fix mode
    print("\nChoose fixing mode:")
    print("1. Fix all issues (SEO + Links + Images)")
    print("2. Dry run (see what would be fixed)")
    print("3. Fix specific posts")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        # Fix all issues
        print("\n🔧 Fixing all issues...")
        result = validator.fix_all_issues(dry_run=False)
        
    elif choice == "2":
        # Dry run
        print("\n👀 Dry run - showing what would be fixed...")
        result = validator.fix_all_issues(dry_run=True)
        
    elif choice == "3":
        # Fix specific posts
        post_ids_str = input("Enter post IDs (comma-separated): ")
        try:
            post_ids = [int(x.strip()) for x in post_ids_str.split(',')]
            print(f"\n🔧 Fixing posts: {post_ids}")
            result = validator.fix_all_issues(post_ids=post_ids, dry_run=False)
        except ValueError:
            print("❌ Invalid post IDs")
            return
    else:
        print("❌ Invalid choice")
        return
    
    # Show results
    print("\n" + "=" * 50)
    print("📊 COMPREHENSIVE FIXING RESULTS")
    print("=" * 50)
    print(f"Posts fixed: {result.get('posts_fixed', 0)}")
    print(f"Total fixes: {result.get('total_fixes', 0)}")
    
    if result.get('total_fixes', 0) > 0:
        print("\n✅ All issues have been fixed!")
    else:
        print("\n ℹ️ No issues found to fix")

if __name__ == "__main__":
    comprehensive_fix()