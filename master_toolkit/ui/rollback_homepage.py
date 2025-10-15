#!/usr/bin/env python3
"""
Rollback Homepage - Remove Carousel
Restore to clean state
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Simple, clean homepage content
CLEAN_HOMEPAGE = """
<div style="max-width: 1200px; margin: 0 auto; padding: 40px 20px;">
    <h1 style="text-align: center; font-size: 48px; margin-bottom: 20px; color: #1a1a1a;">
        Welcome to SphereVista360
    </h1>
    
    <p style="text-align: center; font-size: 20px; color: #666; margin-bottom: 40px;">
        Your Premier Source for Financial Technology Insights
    </p>
    
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 40px; border-radius: 15px; color: white; text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 36px; margin-bottom: 20px;">Explore Our Content</h2>
        <p style="font-size: 18px; opacity: 0.95; line-height: 1.6;">
            Discover in-depth analysis and insights into financial technology, blockchain, artificial intelligence, and digital innovation.
        </p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; margin-bottom: 40px;">
        <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #667eea; margin-bottom: 15px;">💰 Finance</h3>
            <p style="color: #666; line-height: 1.6;">Banking, investments, and financial markets analysis</p>
            <a href="/category/finance/" style="display: inline-block; margin-top: 15px; color: #667eea; text-decoration: none; font-weight: 600;">Explore Finance →</a>
        </div>
        
        <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #764ba2; margin-bottom: 15px;">💻 Technology</h3>
            <p style="color: #666; line-height: 1.6;">AI, innovation, and digital transformation insights</p>
            <a href="/category/technology/" style="display: inline-block; margin-top: 15px; color: #764ba2; text-decoration: none; font-weight: 600;">Explore Technology →</a>
        </div>
        
        <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #667eea; margin-bottom: 15px;">💼 Business</h3>
            <p style="color: #666; line-height: 1.6;">Strategy, growth, and entrepreneurship coverage</p>
            <a href="/category/business/" style="display: inline-block; margin-top: 15px; color: #667eea; text-decoration: none; font-weight: 600;">Explore Business →</a>
        </div>
    </div>
</div>
"""

print("=" * 70)
print("🔄 ROLLING BACK HOMEPAGE CHANGES")
print("=" * 70)
print()

print("Restoring homepage to clean state...")
print("-" * 70)

# Update homepage
url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/2412"

response = requests.post(
    url,
    json={'content': CLEAN_HOMEPAGE},
    auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
)

if response.status_code == 200:
    print("✅ Homepage restored successfully!")
    print()
    print("Changes made:")
    print("  • Removed carousel HTML/CSS/JavaScript")
    print("  • Added clean, simple homepage")
    print("  • Kept category links working")
    print("  • Professional gradient header")
    print("  • Simple category cards (no images)")
    print()
    print("=" * 70)
    print("✅ ROLLBACK COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Clear browser cache (Ctrl+F5)")
    print("  2. Visit: https://spherevista360.com")
    print("  3. Site should now load properly")
    print()
    print("The carousel has been removed and replaced")
    print("with a clean, working homepage.")
else:
    print(f"❌ Failed to update: {response.status_code}")
    print(f"Response: {response.text[:500]}")

print()
print("=" * 70)

