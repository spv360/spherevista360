#!/usr/bin/env python3
"""
Apply Critical CSS Fix via WordPress Customizer
Fixes overlapping images and content with !important rules
"""

import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Comprehensive CSS fix with !important to override any theme styles
CRITICAL_CSS_FIX = """
/* ============================================
   CRITICAL FIX FOR OVERLAPPING CONTENT
   ============================================ */

/* Force all images to respect container width */
img {
    max-width: 100% !important;
    height: auto !important;
}

/* Featured image container */
.post-thumbnail,
.wp-post-image,
.entry-thumbnail {
    display: block !important;
    width: 100% !important;
    margin: 0 0 2rem 0 !important;
    overflow: hidden !important;
}

/* Featured image itself */
.post-thumbnail img,
.wp-post-image {
    width: 100% !important;
    height: auto !important;
    display: block !important;
    object-fit: cover !important;
    max-height: 600px !important;
}

/* Entry content spacing */
.entry-content {
    clear: both !important;
    overflow: hidden !important;
}

/* All content elements clear floats */
.entry-content > *,
.entry-content p,
.entry-content h1,
.entry-content h2,
.entry-content h3,
.entry-content h4,
.entry-content ul,
.entry-content ol,
.entry-content div {
    clear: both !important;
    margin-bottom: 1.5rem !important;
}

/* Images within content */
.entry-content img {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 1.5rem auto !important;
    clear: both !important;
}

/* Fix WordPress alignment classes */
.alignleft {
    float: left !important;
    margin: 0.5rem 1.5rem 1rem 0 !important;
    max-width: 45% !important;
}

.alignright {
    float: right !important;
    margin: 0.5rem 0 1rem 1.5rem !important;
    max-width: 45% !important;
}

.aligncenter {
    display: block !important;
    margin: 1.5rem auto !important;
    clear: both !important;
    float: none !important;
}

.alignnone {
    display: block !important;
    margin: 1.5rem 0 !important;
    clear: both !important;
}

/* Article container */
article {
    overflow: hidden !important;
}

/* Post item in grid */
.post-item {
    overflow: hidden !important;
    display: block !important;
}

/* Clearfix */
.entry-content:after,
.post-content:after,
article:after {
    content: "" !important;
    display: table !important;
    clear: both !important;
}

/* Fix for embedded content */
.entry-content iframe,
.entry-content embed,
.entry-content object,
.entry-content video {
    max-width: 100% !important;
    height: auto !important;
}

/* Gallery fixes */
.gallery {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)) !important;
    gap: 1rem !important;
    clear: both !important;
}

.gallery-item {
    overflow: hidden !important;
}

.gallery-item img {
    width: 100% !important;
    height: auto !important;
}

/* WordPress caption */
.wp-caption {
    max-width: 100% !important;
}

.wp-caption img {
    width: 100% !important;
    height: auto !important;
}

/* Related posts section */
.related-posts {
    clear: both !important;
    margin-top: 3rem !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .alignleft,
    .alignright {
        float: none !important;
        display: block !important;
        margin: 1rem auto !important;
        max-width: 100% !important;
    }
}
"""

def inject_css_to_posts():
    """Inject CSS directly into post content as inline styles"""
    print("=" * 80)
    print("🔧 APPLYING CRITICAL CSS FIX")
    print("=" * 80)
    
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    
    # First, try to add to WordPress Customizer
    print("\n1️⃣  Attempting to add CSS via WordPress Customizer...")
    
    # Get current custom CSS
    try:
        # Try using wp-json REST API
        response = requests.get(f"{WORDPRESS_URL}/wp-json/", auth=auth)
        
        if response.status_code == 200:
            print("   ✅ Connected to WordPress REST API")
            
            # Try to get and update site options
            options_url = f"{WORDPRESS_URL}/wp-json/wp/v2/settings"
            options_response = requests.get(options_url, auth=auth)
            
            if options_response.status_code == 200:
                print("   ✅ Accessed site settings")
                
                # Try to update
                update_data = {}
                update_response = requests.post(options_url, json=update_data, auth=auth)
                print(f"   ℹ️  Settings API available but custom CSS not directly accessible")
            
    except Exception as e:
        print(f"   ⚠️  API method not available: {str(e)[:50]}")
    
    print("\n2️⃣  Creating CSS file for manual upload...")
    
    # Save CSS to file
    css_file_path = "/home/kddevops/downloads/critical-fix.css"
    with open(css_file_path, 'w') as f:
        f.write(CRITICAL_CSS_FIX)
    
    print(f"   ✅ CSS file created: {css_file_path}")
    
    print("\n" + "=" * 80)
    print("📋 MANUAL FIX INSTRUCTIONS")
    print("=" * 80)
    print("\n🎯 METHOD 1: Add to WordPress Customizer (RECOMMENDED)")
    print("-" * 80)
    print("1. Go to: WordPress Admin Dashboard")
    print("2. Navigate to: Appearance → Customize")
    print("3. Click: 'Additional CSS' (in the left sidebar)")
    print("4. Copy and paste the CSS below:")
    print("5. Click: 'Publish'\n")
    print(CRITICAL_CSS_FIX)
    print("\n" + "=" * 80)
    
    print("\n🎯 METHOD 2: Edit Theme Directly")
    print("-" * 80)
    print("1. Go to: WordPress Admin → Appearance → Theme File Editor")
    print("2. Select: style.css")
    print("3. Scroll to bottom and paste the CSS")
    print("4. Click: 'Update File'")
    print("=" * 80)
    
    print("\n🎯 METHOD 3: Use a Custom CSS Plugin")
    print("-" * 80)
    print("1. Install plugin: 'Simple Custom CSS and JS'")
    print("2. Add the CSS through the plugin interface")
    print("3. Save changes")
    print("=" * 80)
    
    # Also create an HTML file with instructions
    html_file = "/home/kddevops/downloads/css-fix-instructions.html"
    with open(html_file, 'w') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>CSS Fix Instructions - SphereVista360</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #667eea;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .step {{
            background: #e3f2fd;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }}
        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .copy-btn:hover {{
            background: #764ba2;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Fix Overlapping Images & Content</h1>
        <p>Follow these steps to fix the overlapping issue on your WordPress site:</p>
        
        <div class="step">
            <h3>Step 1: Copy the CSS Code</h3>
            <button class="copy-btn" onclick="copyCSS()">📋 Copy CSS Code</button>
        </div>
        
        <div class="step">
            <h3>Step 2: Go to WordPress</h3>
            <p>Navigate to: <strong>Appearance → Customize → Additional CSS</strong></p>
        </div>
        
        <div class="step">
            <h3>Step 3: Paste the CSS</h3>
            <p>Paste the copied CSS code in the Additional CSS field</p>
        </div>
        
        <div class="step">
            <h3>Step 4: Publish</h3>
            <p>Click the "Publish" button to apply changes</p>
        </div>
        
        <h2>CSS Code:</h2>
        <pre id="cssCode">{CRITICAL_CSS_FIX}</pre>
        
        <script>
            function copyCSS() {{
                const cssCode = document.getElementById('cssCode').textContent;
                navigator.clipboard.writeText(cssCode).then(() => {{
                    alert('✅ CSS code copied to clipboard!\\n\\nNow go to WordPress → Appearance → Customize → Additional CSS and paste it there.');
                }});
            }}
        </script>
    </div>
</body>
</html>
        """)
    
    print(f"\n📄 Instructions HTML created: {html_file}")
    print(f"   Open this file in a browser for easy copy-paste!")
    
    print("\n" + "=" * 80)
    print("✅ FIX READY - Please apply manually using one of the methods above")
    print("=" * 80)

if __name__ == "__main__":
    inject_css_to_posts()
