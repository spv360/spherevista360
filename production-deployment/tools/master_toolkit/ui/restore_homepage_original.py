#!/usr/bin/env python3
"""
Restore homepage to original content
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WordPress credentials from .env
WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Page ID
HOME_PAGE_ID = 2412

def restore_homepage():
    """Restore the homepage to original content"""
    
    # Original homepage content
    original_content = '''<style>
/* Hide page title on homepage */
.page .entry-header,
.page-title,
h1.entry-title,
.content-title-style,
header.entry-header {
    display: none !important;
}

/* Hide breadcrumbs on homepage */
.kadence-breadcrumbs,
.breadcrumb,
.breadcrumbs {
    display: none !important;
}

.home-header-section {
    max-width: 1400px;
    margin: 60px auto 40px;
    padding: 0 20px;
    text-align: center;
}

.home-main-title {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 42px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 16px 0;
    letter-spacing: -0.03em;
}

.home-subtitle {
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 17px;
    color: #6b7280;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

.home-content-wrapper {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
    display: grid !important;
    grid-template-columns: 1fr 370px !important;
    gap: 50px !important;
    align-items: start !important;
}

.main-content-area {
    min-width: 0 !important;
    grid-column: 1 !important;
}

.sidebar-area {
    grid-column: 2 !important;
    position: relative !important;
}

@media (max-width: 1024px) {
    .home-content-wrapper {
        grid-template-columns: 1fr !important;
        gap: 40px !important;
    }
    
    .main-content-area,
    .sidebar-area {
        grid-column: 1 !important;
    }
}
</style>

[category_carousel]

<div class="home-header-section">
    <h1 class="home-main-title">Latest Articles</h1>
    <p class="home-subtitle">Stay informed with comprehensive coverage of finance, technology, business, and global affairs</p>
</div>

<div class="home-content-wrapper">
    <div class="main-content-area">
        [latest_posts posts_per_page="12"]
    </div>
    <aside class="sidebar-area">
        [trending_topics count="5"]
    </aside>
</div>'''

    # WordPress API endpoint
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{HOME_PAGE_ID}"
    
    # Prepare the update data
    data = {
        'content': original_content,
        'status': 'publish'
    }
    
    # Make the API request
    print(f"Restoring homepage (ID: {HOME_PAGE_ID}) to original content...")
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Homepage successfully restored to original!")
        print(f"   Page URL: {result.get('link', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        print(f"   Content length: {len(original_content)} characters")
        return True
    else:
        print(f"❌ Failed to restore homepage!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HOMEPAGE RESTORATION")
    print("=" * 60)
    restore_homepage()
    print("=" * 60)
