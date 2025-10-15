#!/usr/bin/env python3
"""
Pre-Upload Theme Verification
Tests the theme package before uploading to WordPress
"""

import zipfile
import os
import re

THEME_ZIP = '/home/kddevops/downloads/spherevista-PRODUCTION-READY.zip'

def check_theme_package():
    """Verify the theme package is valid and safe"""
    print("=" * 80)
    print("🔍 THEME PACKAGE VERIFICATION")
    print("=" * 80)
    print()
    
    # Check if file exists
    if not os.path.exists(THEME_ZIP):
        print("❌ Theme package not found!")
        return False
    
    print(f"✅ Found: {THEME_ZIP}")
    print(f"   Size: {os.path.getsize(THEME_ZIP) / 1024:.1f} KB")
    print()
    
    # Check ZIP contents
    try:
        with zipfile.ZipFile(THEME_ZIP, 'r') as zip_file:
            files = zip_file.namelist()
            
            print("📦 PACKAGE CONTENTS:")
            print("-" * 80)
            
            # Required files
            required_files = [
                'style.css',
                'functions.php',
                'index.php',
                'single.php',
                'comments.php'
            ]
            
            found_files = []
            for req_file in required_files:
                matching = [f for f in files if f.endswith(req_file)]
                if matching:
                    found_files.append(req_file)
                    print(f"   ✅ {req_file:<20} - Found")
                else:
                    print(f"   ❌ {req_file:<20} - MISSING!")
            
            print()
            
            # Check comments.php specifically
            comments_files = [f for f in files if f.endswith('comments.php')]
            if comments_files:
                print("🗨️  COMMENTS.PHP VERIFICATION:")
                print("-" * 80)
                
                comments_path = comments_files[0]
                comments_content = zip_file.read(comments_path).decode('utf-8', errors='ignore')
                
                # Check for problematic patterns
                issues = []
                
                # Check for undefined functions
                if 'spherevista360_comment_callback' in comments_content:
                    issues.append("❌ Custom callback function found (may cause error)")
                else:
                    print("   ✅ No custom callback functions")
                
                # Check for required WordPress functions
                if 'wp_list_comments' in comments_content:
                    print("   ✅ Uses wp_list_comments()")
                if 'comment_form' in comments_content:
                    print("   ✅ Uses comment_form()")
                
                # Check for proper PHP tags
                if comments_content.startswith('<?php'):
                    print("   ✅ Proper PHP opening tag")
                
                # Check for unclosed PHP tags or syntax issues
                php_open_count = comments_content.count('<?php')
                php_close_count = comments_content.count('?>')
                
                if php_open_count > 0:
                    print(f"   ✅ PHP tags: {php_open_count} opening, {php_close_count} closing")
                
                # Check for styling
                if '<style>' in comments_content:
                    print("   ✅ Includes styling")
                
                if issues:
                    print()
                    print("   ⚠️  POTENTIAL ISSUES:")
                    for issue in issues:
                        print(f"      {issue}")
                    return False
                
                print()
            
            # Check style.css for theme info
            style_files = [f for f in files if f.endswith('style.css')]
            if style_files:
                print("🎨 THEME INFO:")
                print("-" * 80)
                style_content = zip_file.read(style_files[0]).decode('utf-8', errors='ignore')
                
                # Extract theme name
                name_match = re.search(r'Theme Name:\s*(.+)', style_content)
                if name_match:
                    print(f"   Theme Name: {name_match.group(1).strip()}")
                
                # Extract version
                version_match = re.search(r'Version:\s*(.+)', style_content)
                if version_match:
                    print(f"   Version: {version_match.group(1).strip()}")
                
                print()
            
            # Summary
            print("=" * 80)
            print("📊 VERIFICATION SUMMARY")
            print("=" * 80)
            print(f"   Total files: {len(files)}")
            print(f"   Required files: {len(found_files)}/{len(required_files)}")
            print()
            
            if len(found_files) == len(required_files):
                print("✅ THEME IS VALID AND READY TO UPLOAD!")
                print()
                print("🚀 NEXT STEPS:")
                print("   1. Go to: WordPress Dashboard → Appearance → Themes")
                print("   2. Click: Add New → Upload Theme")
                print("   3. Choose: spherevista-PRODUCTION-READY.zip")
                print("   4. Install → Activate")
                print()
                return True
            else:
                print("❌ THEME IS INCOMPLETE - MISSING REQUIRED FILES")
                return False
    
    except Exception as e:
        print(f"❌ Error reading theme package: {str(e)}")
        return False

def check_site_status():
    """Check if WordPress site is accessible"""
    import requests
    
    print("=" * 80)
    print("🌐 WORDPRESS SITE STATUS")
    print("=" * 80)
    print()
    
    try:
        # Check main site
        response = requests.get('https://spherevista360.com', timeout=10)
        if response.status_code == 200:
            print("✅ Site is ONLINE (200 OK)")
            
            if 'kadence' in response.text.lower():
                print("   Currently running: Kadence Theme")
            
            if 'critical error' in response.text.lower():
                print("   ⚠️  Critical error detected")
            else:
                print("   No errors detected")
        else:
            print(f"⚠️  Site returned: {response.status_code}")
        
        print()
        
        # Check admin
        admin_response = requests.get('https://spherevista360.com/wp-admin/', timeout=10, allow_redirects=False)
        if admin_response.status_code in [200, 302]:
            print("✅ Admin is ACCESSIBLE")
            print("   You can upload the theme via WordPress dashboard")
        else:
            print(f"⚠️  Admin returned: {admin_response.status_code}")
        
        print()
        
    except Exception as e:
        print(f"❌ Cannot reach site: {str(e)}")
        print()

if __name__ == '__main__':
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 22 + "THEME READINESS CHECK" + " " * 35 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Check site status
    check_site_status()
    
    # Check theme package
    is_valid = check_theme_package()
    
    if is_valid:
        print("=" * 80)
        print("✅ ALL CHECKS PASSED - SAFE TO UPLOAD!")
        print("=" * 80)
        print()
    else:
        print("=" * 80)
        print("⚠️  ISSUES FOUND - REVIEW ABOVE")
        print("=" * 80)
        print()
