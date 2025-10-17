#!/usr/bin/env python3
"""
WordPress Authentication Setup & Image Fixing
==============================================
Configure WordPress authentication and run image fixes using enhanced tools.
"""

import sys
import os
import getpass
from datetime import datetime

# Add the master_toolkit to Python path
sys.path.append('/home/kddevops/projects/spherevista360')

from master_toolkit.core.client import WordPressClient
from master_toolkit.utils.auto_fixer import AutoFixer


def setup_wordpress_auth():
    """Setup WordPress authentication interactively."""
    print("🔐 WordPress Authentication Setup")
    print("=" * 40)
    
    # You can either set these manually or input them interactively
    username = input("Enter WordPress username: ") if len(sys.argv) < 2 else sys.argv[1]
    password = getpass.getpass("Enter WordPress password: ") if len(sys.argv) < 3 else sys.argv[2]
    
    if not username or not password:
        print("❌ Username and password required")
        return None
    
    try:
        # Create WordPress client with credentials
        wp = WordPressClient()
        
        # Authenticate explicitly
        auth_success = wp.authenticate(username, password)
        if not auth_success:
            print("❌ Authentication failed - invalid credentials")
            return None
        
        # Test connection
        print("🔍 Testing connection...")
        posts = wp.get_posts(per_page=1)
        
        if posts:
            print(f"✅ Connected successfully! Found {len(posts)} post(s)")
            return wp
        else:
            print("❌ Connected but no posts found")
            return None
            
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Make sure you're using correct credentials and the site is accessible")
        
        # Try alternative authentication approach
        try:
            print("🔄 Trying alternative authentication...")
            from master_toolkit.core.client import create_client
            wp = create_client(username, password)
            
            posts = wp.get_posts(per_page=1)
            if posts:
                print(f"✅ Alternative auth successful! Found {len(posts)} post(s)")
                return wp
        except Exception as e2:
            print(f"❌ Alternative auth also failed: {e2}")
        
        return None


def analyze_and_fix_images(wp_client, dry_run=True):
    """Use our enhanced tools to analyze and fix image issues."""
    print(f"\n🖼️  Image Analysis & Fixing {'(DRY RUN)' if dry_run else '(LIVE)'}")
    print("=" * 50)
    
    try:
        # Create AutoFixer instance using our enhanced tools
        auto_fixer = AutoFixer(wp_client)
        
        # Step 1: Analyze all issues (focus on images)
        print("🔍 Step 1: Analyzing image issues...")
        analysis = auto_fixer.analyze_all_issues(per_page=20)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return False
        
        # Show image-specific issues
        image_issues = analysis.get('issue_summary', {})
        missing_featured = len(image_issues.get('missing_featured_image', []))
        broken_images = len(image_issues.get('broken_images', []))
        missing_alt = len(image_issues.get('missing_alt_text', []))
        
        print(f"📊 Image Issues Found:")
        print(f"   • Posts missing featured images: {missing_featured}")
        print(f"   • Posts with broken images: {broken_images}")
        print(f"   • Posts missing alt text: {missing_alt}")
        print(f"   • Total posts analyzed: {analysis['total_posts']}")
        
        if missing_featured == 0 and broken_images == 0 and missing_alt == 0:
            print("✅ No image issues found! Your images are already optimized.")
            return True
        
        # Step 2: Fix image issues
        print(f"\n🔧 Step 2: Fixing image issues...")
        
        # Fix specifically image-related issues using our enhanced tools
        image_fix_types = []
        if missing_featured > 0:
            image_fix_types.append('missing_featured_image')
        if broken_images > 0:
            image_fix_types.append('broken_images')
        if missing_alt > 0:
            image_fix_types.append('missing_alt_text')
        
        if image_fix_types:
            fix_result = auto_fixer.fix_specific_issues(
                issue_types=image_fix_types,
                per_page=15,  # Process 15 posts at a time
                dry_run=dry_run
            )
            
            if 'error' in fix_result:
                print(f"❌ Fixing failed: {fix_result['error']}")
                return False
            
            print(f"📊 Fix Results:")
            print(f"   • Posts processed: {fix_result['posts_processed']}")
            print(f"   • Posts fixed: {fix_result['posts_fixed_count']}")
            print(f"   • Total fixes applied: {fix_result['total_fixes']}")
            
            # Show breakdown
            fixes_applied = fix_result.get('fixes_applied', {})
            for fix_type, count in fixes_applied.items():
                if count > 0:
                    print(f"   • {fix_type.replace('_', ' ').title()}: {count}")
            
            if dry_run:
                print(f"\n💡 This was a dry run - no actual changes made")
                print(f"🚀 To apply these fixes, run: python3 {sys.argv[0]} --live")
            else:
                print(f"\n🎉 Live fixes applied successfully!")
                print(f"💡 Re-run site audit to see improvements")
        
        return True
        
    except Exception as e:
        print(f"❌ Image fixing failed: {e}")
        return False


def main():
    """Main function."""
    print("🚀 Enhanced Image Fixing Tool")
    print("=" * 35)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check for live mode
    dry_run = '--live' not in sys.argv
    if not dry_run:
        print("⚠️  LIVE MODE: Will make actual changes to your website!")
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Cancelled")
            return
    
    # Step 1: Setup WordPress authentication
    wp_client = setup_wordpress_auth()
    if not wp_client:
        print("\n❌ Cannot proceed without WordPress authentication")
        print("\n💡 Usage:")
        print(f"   python3 {sys.argv[0]} [username] [password]")
        print(f"   python3 {sys.argv[0]} [username] [password] --live")
        return
    
    # Step 2: Analyze and fix images using our enhanced tools
    success = analyze_and_fix_images(wp_client, dry_run=dry_run)
    
    if success:
        print(f"\n✅ Image fixing completed successfully!")
        if dry_run:
            print(f"🔄 Run with --live flag to apply actual fixes")
    else:
        print(f"\n❌ Image fixing encountered errors")
    
    print(f"\n🏁 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()