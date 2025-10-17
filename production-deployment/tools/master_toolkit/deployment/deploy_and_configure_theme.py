#!/usr/bin/env python3
"""
Deploy SphereVista360 Theme and Auto-Configure
"""

import os
import requests
import zipfile
from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def create_theme_zip():
    """Create a ZIP file of the theme"""
    print("📦 Creating theme package...")
    
    theme_dir = Path('spherevista-theme')
    zip_path = Path('spherevista360-theme.zip')
    
    # Remove old zip if exists
    if zip_path.exists():
        zip_path.unlink()
    
    # Create new zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in theme_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(theme_dir.parent)
                zipf.write(file_path, arcname)
                print(f"   Added: {arcname}")
    
    print(f"✅ Theme packaged: {zip_path}")
    return zip_path

def upload_theme(zip_path):
    """Upload theme via WordPress REST API"""
    print(f"\n📤 Uploading theme to {WORDPRESS_URL}...")
    
    # WordPress doesn't have a direct REST API endpoint for theme upload
    # We'll use the admin-ajax.php approach or WP-CLI
    print("⚠️  Theme upload requires WP-CLI or FTP access")
    print("   Alternative: Upload manually via WordPress admin")
    print(f"   File ready: {zip_path.absolute()}")
    
    return True

def activate_theme():
    """Activate theme via REST API"""
    print(f"\n🎨 Activating theme...")
    
    # Note: WordPress REST API doesn't have direct theme activation
    # This would require a custom endpoint or WP-CLI
    print("⚠️  Theme activation requires WP-CLI or manual activation")
    print("   Go to: Appearance > Themes > Activate 'SphereVista360'")
    
    return True

def configure_theme():
    """Configure theme via custom REST API endpoint"""
    print(f"\n⚙️  Configuring theme...")
    
    url = f"{WORDPRESS_URL}/wp-json/spherevista360/v1/configure"
    
    try:
        response = requests.post(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Theme configured successfully!")
            data = response.json()
            print(f"   {data.get('message', 'Configuration complete')}")
            return True
        else:
            print(f"❌ Configuration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_blog_page():
    """Create Blog page for posts"""
    print(f"\n📄 Creating Blog page...")
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/pages"
    
    # Check if Blog page already exists
    check_url = f"{url}?search=Blog"
    response = requests.get(
        check_url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    
    if response.status_code == 200 and len(response.json()) > 0:
        print("   ℹ️  Blog page already exists")
        return response.json()[0]['id']
    
    # Create Blog page
    data = {
        'title': 'Blog',
        'content': '<p>Welcome to our blog. Here you\'ll find the latest insights and updates.</p>',
        'status': 'publish',
        'type': 'page'
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        if response.status_code == 201:
            page_id = response.json()['id']
            print(f"   ✅ Created Blog page (ID: {page_id})")
            return page_id
        else:
            print(f"   ❌ Failed to create Blog page: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    """Main deployment function"""
    print("=" * 60)
    print("🚀 SphereVista360 Theme Deployment & Configuration")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    # Step 1: Create theme package
    zip_path = create_theme_zip()
    
    # Step 2: Upload theme (manual step for now)
    upload_theme(zip_path)
    
    # Step 3: Create Blog page
    create_blog_page()
    
    # Step 4: Manual instructions for theme activation
    print("\n" + "=" * 60)
    print("📋 MANUAL STEPS REQUIRED:")
    print("=" * 60)
    print("\n1. 📤 Upload Theme:")
    print(f"   • Go to: {WORDPRESS_URL}/wp-admin/theme-install.php")
    print("   • Click 'Upload Theme'")
    print(f"   • Upload: {zip_path.absolute()}")
    print("   • Click 'Install Now'")
    print("\n2. 🎨 Activate Theme:")
    print("   • After installation, click 'Activate'")
    print("   • Or go to: Appearance > Themes")
    print("   • Activate 'SphereVista360 Professional Theme'")
    print("\n3. ⚙️  Auto-Configuration:")
    print("   • Theme will auto-configure on activation!")
    print("   • It will set up:")
    print("     - Static homepage (Homepage)")
    print("     - Main navigation menu")
    print("     - Blog page for posts")
    print("     - Pretty permalinks")
    
    # Step 5: Offer to run configuration if theme is already active
    print("\n" + "=" * 60)
    print("🔧 If theme is already active, run configuration now?")
    print("=" * 60)
    
    user_input = input("\nRun configuration? (y/n): ").lower()
    
    if user_input == 'y':
        configure_theme()
    
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT PACKAGE READY!")
    print("=" * 60)
    print(f"\n📦 Package: {zip_path.absolute()}")
    print(f"🌐 Your site: {WORDPRESS_URL}")
    print("\n🎉 Follow the manual steps above to complete deployment!")
    print("=" * 60)

if __name__ == "__main__":
    main()
