import requests
import json

# WordPress credentials
wp_url = "https://spherevista360.com"
username = "JK"
app_password = "BT1I iKXv 6bYv EUuS P2vk K9hV"

# Update homepage content with full layout including carousel, latest posts, and trending topics
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
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 1fr 370px;
    gap: 50px;
    align-items: start;
}

.main-content-area {
    min-width: 0;
}

.sidebar-area {
    position: relative;
}

@media (max-width: 1024px) {
    .home-content-wrapper {
        grid-template-columns: 1fr;
        gap: 40px;
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

print("🔧 RESTORING FULL HOMEPAGE LAYOUT")
print("=" * 50)

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
    print("✅ Homepage fully restored!")
    print("\n📋 What's been added:")
    print("  🎠 Category carousel (top)")
    print("  📝 Latest articles section (left)")
    print("  🔥 Trending topics sidebar (right)")
    print("\n🎯 Layout structure:")
    print("  📱 Top: Animated category carousel")
    print("  📄 Middle: 'Latest Articles' header")
    print("  📝 Left: Article list (12 posts)")
    print("  🔥 Right: Trending topics sidebar")
    print("\n⚠️ REMINDER: Ensure WORKING-functions.php is active in theme")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)