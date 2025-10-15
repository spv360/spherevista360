#!/usr/bin/env python3
"""
Upload Fixed Theme CSS to WordPress
Fixes overlapping images and content issues
"""

import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# CSS fixes for overlapping issues
ADDITIONAL_CSS = """
/* OVERLAPPING FIXES - Added by automated fix */

/* Prevent image overflow */
.entry-content img,
.post-thumbnail img,
.wp-post-image {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    clear: both !important;
}

/* Fix content spacing */
.entry-content > * {
    clear: both;
}

/* Better image margins */
.entry-content img {
    margin: 1.5rem auto !important;
}

/* Fix featured images */
.wp-post-image {
    width: 100%;
    max-height: 500px;
    object-fit: cover;
    margin-bottom: 2rem;
}

/* Fix post grid images */
.post-thumbnail {
    width: 100%;
    height: 220px;
    object-fit: cover;
    display: block;
}

.post-item {
    overflow: hidden;
}

/* Prevent text wrapping issues */
.entry-content p,
.entry-content h2,
.entry-content h3,
.entry-content ul,
.entry-content ol {
    clear: both;
}

/* WordPress image alignment fixes */
.alignleft {
    float: left;
    margin: 0.5rem 1.5rem 1rem 0;
    max-width: 50%;
}

.alignright {
    float: right;
    margin: 0.5rem 0 1rem 1.5rem;
    max-width: 50%;
}

.aligncenter {
    display: block;
    margin: 1.5rem auto;
    clear: both;
}

/* Related posts fix */
.related-posts {
    clear: both;
    margin-top: 3rem;
}

/* Gallery fix */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    clear: both;
}

.gallery-item img {
    width: 100%;
    height: auto;
}

/* Fix for any embedded content */
.entry-content iframe,
.entry-content embed,
.entry-content video {
    max-width: 100%;
    height: auto;
}

/* Clearfix for containers */
.entry-content:after,
.post-content:after {
    content: "";
    display: table;
    clear: both;
}
"""

def add_custom_css():
    """Add custom CSS to fix overlapping issues"""
    print("=" * 70)
    print("🎨 FIXING OVERLAPPING IMAGES & CONTENT")
    print("=" * 70)
    
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    
    # Try to update via Customizer API (if available)
    print("\n📝 Adding CSS fixes via WordPress Customizer...")
    
    customizer_url = f"{WORDPRESS_URL}/wp-json/wp/v2/customize/changeset"
    
    # Alternative: Add via Additional CSS setting
    settings_url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
    
    # Get current settings
    response = requests.get(settings_url, auth=auth)
    
    if response.status_code == 200:
        print("✅ Connected to WordPress settings")
        
        # Try to update custom CSS
        update_data = {
            'custom_css': ADDITIONAL_CSS
        }
        
        update_response = requests.post(settings_url, json=update_data, auth=auth)
        
        if update_response.status_code in [200, 201]:
            print("✅ Custom CSS added successfully!")
            print("\n🎉 Overlapping issues should now be fixed!")
        else:
            print(f"⚠️  Could not add via API (Status: {update_response.status_code})")
            print("\n📋 MANUAL FIX REQUIRED:")
            print("=" * 70)
            print("Go to: WordPress Admin → Appearance → Customize → Additional CSS")
            print("And add the following CSS:")
            print("=" * 70)
            print(ADDITIONAL_CSS)
            print("=" * 70)
    else:
        print("⚠️  Could not access settings API")
        print("\n📋 MANUAL FIX - Add this CSS to your theme:")
        print("=" * 70)
        print(ADDITIONAL_CSS)
        print("=" * 70)
    
    print("\n" + "=" * 70)
    print("📦 ALTERNATIVE: Upload Fixed Theme")
    print("=" * 70)
    print("Updated theme package available at:")
    print("  /home/kddevops/projects/spherevista360/spherevista360-fixed.zip")
    print("\nTo upload:")
    print("  1. Go to WordPress Admin → Appearance → Themes")
    print("  2. Click 'Add New' → 'Upload Theme'")
    print("  3. Upload: spherevista360-fixed.zip")
    print("  4. Click 'Activate'")
    print("=" * 70)

if __name__ == "__main__":
    add_custom_css()
