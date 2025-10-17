#!/usr/bin/env python3
"""
Restore homepage with robust grid/flex layout using WordPress API
"""
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
HOME_PAGE_ID = 2412

def get_homepage_content():
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
    font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: #0a2540;
    margin: 0 0 18px 0;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    line-height: 1.1;
    text-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.home-subtitle {
    font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
    font-size: 21px;
         return """
    <style>
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
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        font-size: 48px;
        font-weight: 800;
        color: #0a2540;
        margin: 0 0 18px 0;
        letter-spacing: -0.02em;
        text-transform: uppercase;
        line-height: 1.1;
        text-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .home-subtitle {
        font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
        font-size: 21px;
        color: #3b4757;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.7;
        font-weight: 500;
        letter-spacing: 0.01em;
        text-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .home-content-wrapper {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 0 20px !important;
        display: grid !important;
        grid-template-columns: minmax(0,1fr) 370px !important;
        gap: 50px !important;
        align-items: start !important;
        grid-auto-flow: column !important;
        /* Fallback for grid issues: */
        display: -webkit-box !important;
        display: -ms-flexbox !important;
        display: flex !important;
        -webkit-box-orient: horizontal !important;
        -webkit-box-direction: normal !important;
        -ms-flex-direction: row !important;
        flex-direction: row !important;
    }
    .main-content-area {
        min-width: 0 !important;
        grid-column: 1 !important;
        grid-row: 1 !important;
        -webkit-box-flex: 1 !important;
        -ms-flex: 1 1 0%;
        flex: 1 1 0%;
    }
    .sidebar-area {
        grid-column: 2 !important;
        grid-row: 1 !important;
        position: relative !important;
        width: 370px !important;
        max-width: 100% !important;
        -webkit-box-flex: 0 !important;
        -ms-flex: 0 0 370px;
        flex: 0 0 370px;
    }
    @media (max-width: 1024px) {
        .home-content-wrapper {
            grid-template-columns: 1fr !important;
            grid-auto-flow: row !important;
            gap: 40px !important;
            display: block !important;
        }
        .main-content-area,
        .sidebar-area {
            grid-column: 1 !important;
            grid-row: auto !important;
            width: 100% !important;
            max-width: 100% !important;
        }
    }
    </style>

    [category_carousel]

    <div class="home-header-section">
        <h1 class="home-main-title">SphereVista360: Insights That Drive Success</h1>
        <p class="home-subtitle">Expert analysis and trusted perspectives on finance, technology, business, and global affairs. Empower your decisions with our professional coverage and actionable intelligence.</p>
    </div>

    <div class="home-content-wrapper">
        <div class="main-content-area">[latest_posts posts_per_page="12"]</div><aside class="sidebar-area">[trending_topics count="5"]</aside>
        </div>
    """
                line-height: 1.1;
                text-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            .home-subtitle {
                font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
                font-size: 21px;
                color: #3b4757;
                max-width: 800px;
                margin: 0 auto;
                line-height: 1.7;
                font-weight: 500;
                letter-spacing: 0.01em;
                text-shadow: 0 1px 4px rgba(0,0,0,0.04);
            }
            .home-content-wrapper {
                max-width: 1400px !important;
                margin: 0 auto !important;
                padding: 0 20px !important;
                display: grid !important;
                grid-template-columns: minmax(0,1fr) 370px !important;
                gap: 50px !important;
                align-items: start !important;
                grid-auto-flow: column !important;
                /* Fallback for grid issues: */
                display: -webkit-box !important;
                display: -ms-flexbox !important;
                display: flex !important;
                -webkit-box-orient: horizontal !important;
                -webkit-box-direction: normal !important;
                -ms-flex-direction: row !important;
                flex-direction: row !important;
            }
            .main-content-area {
                min-width: 0 !important;
                grid-column: 1 !important;
                grid-row: 1 !important;
                -webkit-box-flex: 1 !important;
                -ms-flex: 1 1 0%;
                flex: 1 1 0%;
            }
            .sidebar-area {
                grid-column: 2 !important;
                grid-row: 1 !important;
                position: relative !important;
                width: 370px !important;
                max-width: 100% !important;
                -webkit-box-flex: 0 !important;
                -ms-flex: 0 0 370px;
                flex: 0 0 370px;
            }
            @media (max-width: 1024px) {
                .home-content-wrapper {
                    grid-template-columns: 1fr !important;
                    grid-auto-flow: row !important;
                    gap: 40px !important;
                    display: block !important;
                }
                .main-content-area,
                .sidebar-area {
                    grid-column: 1 !important;
                    grid-row: auto !important;
                    width: 100% !important;
                    max-width: 100% !important;
                }
            }
            </style>

            [category_carousel]

            <div class="home-header-section">
                <h1 class="home-main-title">SphereVista360: Insights That Drive Success</h1>
                <p class="home-subtitle">Expert analysis and trusted perspectives on finance, technology, business, and global affairs. Empower your decisions with our professional coverage and actionable intelligence.</p>
            </div>

            <div class="home-content-wrapper">
                <div class="main-content-area">[latest_posts posts_per_page="12"]</div><aside class="sidebar-area">[trending_topics count="5"]</aside>
            </div>
            """
<div class="home-header-section">
    <h1 class="home-main-title">Latest Articles</h1>
    <p class="home-subtitle">Stay informed with comprehensive coverage of finance, technology, business, and global affairs</p>
</div>

<div class="home-content-wrapper">
    <div class="main-content-area">[latest_posts posts_per_page=\"12\"]</div><aside class="sidebar-area">[trending_topics count=\"5\"]</aside>
</div>'''

def restore_homepage():
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{HOME_PAGE_ID}"
    data = {
        'content': get_homepage_content(),
        'status': 'publish'
    }
    print(f"Restoring homepage (ID: {HOME_PAGE_ID}) with robust grid/flex layout...")
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    if response.status_code == 200:
        result = response.json()
        print("✅ Homepage successfully restored!")
        print(f"   Page URL: {result.get('link', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        print(f"   Content length: {len(data['content'])} characters")
        return True
    else:
        print(f"❌ Failed to restore homepage!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    restore_homepage()
