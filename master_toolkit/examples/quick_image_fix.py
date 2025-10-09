#!/usr/bin/env python3
"""
Quick Image Fix Script
=====================
Simple script using our existing enhanced master-toolkit tools.
"""

import sys
sys.path.append('/home/kddevops/projects/spherevista360')

from master_toolkit.core import WordPressClient
from master_toolkit.utils.auto_fixer import AutoFixer

def quick_fix_images():
    """Quick image fix using existing enhanced tools."""
    print("🖼️  Quick Image Fix Using Enhanced Tools")
    print("=" * 45)
    
    try:
        # Setup (you'll need to configure authentication)
        wp = WordPressClient()
        # wp.authenticate('username', 'password')  # Configure as needed
        
        # Use our AutoFixer that we already built
        auto_fixer = AutoFixer(wp)
        
        print("🔍 Step 1: Analyzing image issues...")
        analysis = auto_fixer.analyze_all_issues(per_page=10)
        
        missing_images = len(analysis['issue_summary'].get('missing_featured_image', []))
        print(f"   Found {missing_images} posts missing featured images")
        
        if missing_images > 0:
            print("🔧 Step 2: Fixing missing featured images (DRY RUN)...")
            # Use the fix_specific_issues method we built
            result = auto_fixer.fix_specific_issues(
                issue_types=['missing_featured_image'],
                dry_run=True  # Safe dry run first
            )
            
            print(f"   {result.get('message', 'Fix completed')}")
            
            # To apply actual fixes:
            # result = auto_fixer.fix_specific_issues(
            #     issue_types=['missing_featured_image'],
            #     dry_run=False
            # )
        
        print("✅ All done using existing enhanced tools!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Configure WordPress authentication first")

if __name__ == "__main__":
    quick_fix_images()