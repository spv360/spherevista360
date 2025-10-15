import requests
import json

# WordPress credentials
wp_url = "https://spherevista360.com"
username = "JK"
app_password = "BT1I iKXv 6bYv EUuS P2vk K9hV"

# Update homepage with stronger CSS
page_id = 2412

new_content = """[category_carousel]

<style>
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
</div>"""

# Update the page
endpoint = f"{wp_url}/wp-json/wp/v2/pages/{page_id}"

response = requests.post(
    endpoint,
    auth=(username, app_password),
    json={
        'content': new_content
    }
)

if response.status_code == 200:
    print("✅ Homepage layout fixed with stronger CSS!")
    print("🎯 Grid layout enforced with !important declarations")
    print("\nLayout structure:")
    print("  📱 Grid Column 1: Article list (main content)")
    print("  🔥 Grid Column 2: Trending sidebar (right side)")
    print("\n" + "="*60)
    print("⚠️ CRITICAL: You MUST copy WORKING-functions.php to WordPress!")
    print("="*60)
    print("\nWithout this, the [trending_topics] shortcode won't work.")
    print("\nSteps:")
    print("1. Open WORKING-functions.php")
    print("2. Select All (Ctrl+A) and Copy (Ctrl+C)")
    print("3. Go to: https://spherevista360.com/wp-admin/")
    print("4. Navigate: Appearance → Theme File Editor")
    print("5. Select: 'Theme Functions (functions.php)'")
    print("6. Delete ALL content and Paste (Ctrl+V)")
    print("7. Click 'Update File'")
    print("\n✨ Then the sidebar will appear on the right!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

