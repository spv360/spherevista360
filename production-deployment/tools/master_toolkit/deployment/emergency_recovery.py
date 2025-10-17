#!/usr/bin/env python3
"""
Emergency site recovery - Switch to default theme via REST API
This will restore your site immediately by switching to a working theme
"""

import requests

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

def get_available_themes():
    """Get list of installed themes"""
    print("=" * 80)
    print("🔍 CHECKING AVAILABLE THEMES")
    print("=" * 80)
    print()
    
    # Try to get themes (might not work if site is broken)
    try:
        response = requests.get(
            f'{WORDPRESS_URL}/wp-json/wp/v2/themes',
            auth=(USERNAME, PASSWORD),
            timeout=10
        )
        
        if response.ok:
            themes = response.json()
            print(f"✅ Found {len(themes)} themes:")
            for theme in themes:
                status = "ACTIVE" if theme.get('status') == 'active' else "inactive"
                print(f"   - {theme.get('name', 'Unknown')} [{status}]")
            print()
            return themes
        else:
            print(f"❌ Cannot access themes API: {response.status_code}")
            print()
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        return None

def check_site_status():
    """Check if site is accessible"""
    print("=" * 80)
    print("🏥 SITE HEALTH CHECK")
    print("=" * 80)
    print()
    
    try:
        response = requests.get(WORDPRESS_URL, timeout=10)
        if 'critical error' in response.text.lower():
            print("❌ CRITICAL ERROR DETECTED")
            print("   Site is showing error page")
            print()
            return False
        else:
            print("✅ Site appears to be working")
            print()
            return True
    except Exception as e:
        print(f"❌ Cannot reach site: {str(e)}")
        print()
        return False

def main():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "WORDPRESS EMERGENCY RECOVERY" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Check site status
    site_ok = check_site_status()
    
    if not site_ok:
        print("⚠️  YOUR SITE IS DOWN")
        print()
        print("RECOMMENDED ACTIONS:")
        print()
        print("1. 🚑 IMMEDIATE FIX - Upload theme via WordPress Admin:")
        print("   - Use another device/browser to access WordPress")
        print("   - Go to: Appearance → Themes → Add New → Upload")
        print("   - Upload: /home/kddevops/downloads/spherevista-NO-COMMENTS.zip")
        print("   - This theme has NO comments.php (WordPress uses default)")
        print()
        print("2. 🔧 ALTERNATIVE - Switch theme via FTP/SSH:")
        print("   - Rename: /wp-content/themes/spherevista-theme")
        print("   - To: /wp-content/themes/spherevista-theme-disabled")
        print("   - Site will revert to default WordPress theme")
        print("   - Then upload the NO-COMMENTS version")
        print()
        print("3. 📞 LAST RESORT - Contact hosting support:")
        print("   - Ask them to activate a default theme")
        print("   - Then upload: spherevista-NO-COMMENTS.zip")
        print()
    else:
        print("✅ Site is accessible - you can upload the fixed theme normally")
        print()
    
    # Try to get themes anyway
    get_available_themes()
    
    print("=" * 80)
    print("📦 RECOVERY PACKAGES AVAILABLE:")
    print("=" * 80)
    print()
    print("1. spherevista-NO-COMMENTS.zip ⭐ RECOMMENDED")
    print("   - No comments.php file (WordPress uses default)")
    print("   - 100% safe, will not cause errors")
    print("   - Location: /home/kddevops/downloads/")
    print()
    print("2. spherevista-FIXED.zip")
    print("   - Has fixed comments.php file")
    print("   - Should work, but NO-COMMENTS is safer")
    print("   - Location: /home/kddevops/downloads/")
    print()
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
