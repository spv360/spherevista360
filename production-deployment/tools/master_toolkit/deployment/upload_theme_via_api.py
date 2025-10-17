#!/usr/bin/env python3
"""
Upload and activate WordPress theme directly
Uses WordPress REST API with file upload
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def upload_theme_zip():
    """Upload theme ZIP via WordPress media API"""
    print("📤 Uploading theme ZIP file...")
    
    zip_path = Path('spherevista360-theme.zip')
    
    if not zip_path.exists():
        print("❌ Theme ZIP not found. Run deploy_and_configure_theme.py first.")
        return None
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/media"
    
    with open(zip_path, 'rb') as f:
        files = {
            'file': (zip_path.name, f, 'application/zip')
        }
        
        try:
            response = requests.post(
                url,
                files=files,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                headers={
                    'Content-Disposition': f'attachment; filename="{zip_path.name}"'
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Theme ZIP uploaded!")
                print(f"   Media ID: {data['id']}")
                print(f"   URL: {data['source_url']}")
                return data['source_url']
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def main():
    print("=" * 60)
    print("📦 Theme ZIP Uploader")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    # Upload theme ZIP to media library
    zip_url = upload_theme_zip()
    
    if zip_url:
        print("\n" + "=" * 60)
        print("✅ NEXT STEPS:")
        print("=" * 60)
        print("\n1. The theme ZIP is now in your Media Library")
        print(f"   URL: {zip_url}")
        print("\n2. You can now:")
        print("   Option A: Download it from Media Library and upload via Appearance > Themes")
        print("   Option B: Use the pre-generated ZIP file:")
        print(f"   File: /home/kddevops/projects/spherevista360/spherevista360-theme.zip")
        print("\n3. Go to WordPress Admin:")
        print(f"   {WORDPRESS_URL}/wp-admin/theme-install.php")
        print("   • Click 'Upload Theme'")
        print("   • Choose the ZIP file")
        print("   • Click 'Install Now'")
        print("   • Click 'Activate'")
        print("\n4. Theme will auto-configure:")
        print("   ✓ Set Homepage as front page")
        print("   ✓ Create main navigation menu")
        print("   ✓ Set Blog page for posts")
        print("   ✓ Configure permalinks")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
