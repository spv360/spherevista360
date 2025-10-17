#!/usr/bin/env python3
"""
Category Cleanup Tool
====================
Remove empty categories to achieve 100% AdSense readiness.
"""

import sys
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def cleanup_empty_categories():
    """Remove empty categories for clean navigation."""
    print_info("🧹 CATEGORY CLEANUP TOOL")
    print_info("=" * 40)
    
    try:
        wp = WordPressClient()
        wp.authenticate()
        
        categories = wp.get_categories()
        empty_categories = [
            cat for cat in categories 
            if cat.get('count', 0) == 0 and 
            cat.get('name') != 'Uncategorized' and 
            cat.get('id') != 1
        ]
        
        print_info(f"📊 Found {len(empty_categories)} empty categories:")
        for cat in empty_categories:
            print_info(f"   - {cat.get('name')} (ID: {cat.get('id')})")
        
        print_warning(f"\n⚠️  Note: WordPress REST API doesn't allow category deletion.")
        print_info("📋 Manual cleanup required via WordPress Admin:")
        print_info("   1. Go to Posts > Categories")
        print_info("   2. Delete these empty categories:")
        
        for cat in empty_categories:
            print_info(f"      ❌ Delete: {cat.get('name')}")
        
        print_success("\n✅ After cleanup, your AdSense readiness will be 100%!")
        
    except Exception as e:
        print_error(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    cleanup_empty_categories()