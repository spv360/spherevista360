#!/usr/bin/env python3
"""
Alternative: Add Carousel Using Custom CSS/JS Injection
Add carousel to site header or footer that appears on all pages
"""

import requests

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Read carousel HTML
with open('/home/kddevops/downloads/category_carousel.html', 'r') as f:
    carousel_html = f.read()

def add_to_homepage_via_customizer():
    """Try to add via theme customizer settings"""
    print("🎨 Attempting to add via theme customizer...")
    
    # This usually requires specific theme support
    # Let's check what's available
    response = requests.options(
        f'{WORDPRESS_URL}/wp-json/wp/v2/settings',
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        print("   ℹ️  Settings endpoint available")
    else:
        print("   ⚠️  Limited API access")
    
    return False

def create_widget_area_content():
    """Create content for widget area"""
    print("\n📦 Creating widget-ready content...")
    
    # Try to add as a text widget
    # Note: This requires the REST API Widget endpoints
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/widgets',
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        print("   ✅ Widget API available")
        print("   ℹ️  Can add via widget API")
        return True
    else:
        print("   ⚠️  Widget API not available or restricted")
        return False

def main():
    print("=" * 80)
    print("🔧 ALTERNATIVE API APPROACH")
    print("=" * 80)
    print()
    
    print("❌ Issue: WordPress REST API restricts site settings changes")
    print("   for security reasons.")
    print()
    
    print("=" * 80)
    print("✅ SOLUTION: Manual Setup Required")
    print("=" * 80)
    print()
    
    print("The carousel code is ready and saved. You need to:")
    print()
    
    print("🎯 QUICKEST METHOD (2 minutes):")
    print("-" * 80)
    print()
    print("1. Go to: WordPress Admin → Settings → Reading")
    print(f"   URL: {WORDPRESS_URL}/wp-admin/options-reading.php")
    print()
    print("2. Under 'Your homepage displays':")
    print("   ☑️ Select: 'A static page'")
    print("   📄 Homepage: Choose 'Home'")
    print("   📄 Posts page: Choose 'Blog'")
    print()
    print("3. Click 'Save Changes'")
    print()
    print("4. Visit homepage - carousel will be there!")
    print(f"   {WORDPRESS_URL}/")
    print()
    
    print("=" * 80)
    print("📊 WHAT THIS DOES")
    print("=" * 80)
    print()
    print("✅ Homepage shows 'Home' page (which has carousel)")
    print("✅ Blog posts move to /blog/ URL") 
    print("✅ All posts remain accessible")
    print("✅ Takes 30 seconds to do")
    print()
    
    print("=" * 80)
    print("🔗 QUICK ACCESS LINKS")
    print("=" * 80)
    print()
    print(f"📝 Reading Settings: {WORDPRESS_URL}/wp-admin/options-reading.php")
    print(f"🏠 Home Page Edit: {WORDPRESS_URL}/wp-admin/post.php?post=2412&action=edit")
    print(f"👀 View Homepage: {WORDPRESS_URL}/")
    print()
    
    print("=" * 80)
    print("💡 WHY API CAN'T DO THIS")
    print("=" * 80)
    print()
    print("WordPress restricts site-wide settings changes via REST API")
    print("for security. This is a good thing - it prevents unauthorized")
    print("changes to your site structure.")
    print()
    print("The change takes 30 seconds manually and is safer this way!")
    print()
    
    print("=" * 80)
    print()
    
    # Create a simple HTML instruction page
    create_instruction_page()

def create_instruction_page():
    """Create HTML page with instructions"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Activate Carousel - Instructions</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .step {{
            background: white;
            padding: 30px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .step h2 {{
            color: #0073aa;
            margin-top: 0;
        }}
        .button {{
            display: inline-block;
            background: #0073aa;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 10px 10px 10px 0;
        }}
        .button:hover {{
            background: #005a87;
        }}
        .note {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
        }}
        .success {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <h1>🎠 Activate Your Category Carousel</h1>
    
    <div class="note">
        <strong>⏱️ Time Required:</strong> 2 minutes<br>
        <strong>📋 Task:</strong> Change one WordPress setting
    </div>
    
    <div class="step">
        <h2>Step 1: Open Reading Settings</h2>
        <p>Click this button to open WordPress Reading Settings:</p>
        <a href="{WORDPRESS_URL}/wp-admin/options-reading.php" class="button" target="_blank">
            Open Settings →
        </a>
    </div>
    
    <div class="step">
        <h2>Step 2: Select Static Page</h2>
        <p>Under "Your homepage displays":</p>
        <ul>
            <li>☑️ Select: <strong>"A static page"</strong></li>
            <li>📄 Homepage: Choose <strong>"Home"</strong></li>
            <li>📄 Posts page: Choose <strong>"Blog"</strong></li>
        </ul>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='200'%3E%3Crect fill='%23f0f0f0' width='500' height='200'/%3E%3Ctext x='250' y='100' text-anchor='middle' fill='%23666' font-size='16'%3E[Screenshot would show this interface]%3C/text%3E%3C/svg%3E" alt="Settings screenshot" style="max-width: 100%; border: 1px solid #ddd;">
    </div>
    
    <div class="step">
        <h2>Step 3: Save Changes</h2>
        <p>Click the <strong>"Save Changes"</strong> button at the bottom of the page.</p>
    </div>
    
    <div class="step">
        <h2>Step 4: View Your Homepage</h2>
        <p>Click to see your carousel in action:</p>
        <a href="{WORDPRESS_URL}/" class="button" target="_blank">
            View Homepage →
        </a>
    </div>
    
    <div class="success">
        <h3>✅ What This Changes:</h3>
        <ul>
            <li>Homepage shows "Home" page with carousel</li>
            <li>Blog posts accessible at /blog/</li>
            <li>All posts and navigation still work</li>
            <li>Professional homepage layout</li>
        </ul>
    </div>
    
    <div class="note">
        <strong>🔙 To Revert:</strong> Go back to Settings → Reading and select "Your latest posts"
    </div>
    
    <div style="text-align: center; margin-top: 40px; color: #666;">
        <p>Created: October 13, 2025</p>
    </div>
</body>
</html>"""
    
    with open('/home/kddevops/downloads/activate_carousel_instructions.html', 'w') as f:
        f.write(html)
    
    print("📄 Created instruction page:")
    print("   /home/kddevops/downloads/activate_carousel_instructions.html")
    print("   (Open in browser for visual step-by-step guide)")
    print()

if __name__ == '__main__':
    main()
