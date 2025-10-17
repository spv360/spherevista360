#!/usr/bin/env python3
"""
Rollback Carousel Changes
Remove the enhanced carousel and restore a simple working version or remove entirely
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Simple working carousel or remove entirely
SIMPLE_CAROUSEL_HTML = """
<!-- Simple Category Carousel - Working Version -->
<style>
.category-carousel-container {
    width: 100%;
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.carousel-header {
    text-align: center;
    padding: 20px;
}

.carousel-title {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.carousel-subtitle {
    font-size: 16px;
    color: #f0f0f0;
    margin-bottom: 20px;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px;
}

.category-card {
    position: relative;
    height: 180px;
    border-radius: 10px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s ease;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

.category-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 100%);
    padding: 40px 15px 15px;
    color: white;
}

.category-name {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.category-description {
    font-size: 12px;
    margin: 5px 0 0 0;
    opacity: 0.9;
}

.category-emoji {
    font-size: 48px;
    text-align: center;
    line-height: 180px;
    opacity: 0.7;
}

@media (max-width: 768px) {
    .category-grid {
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }

    .category-card {
        height: 150px;
    }

    .category-emoji {
        font-size: 36px;
        line-height: 150px;
    }

    .carousel-title {
        font-size: 24px;
    }
}
</style>

<div class="category-carousel-container">
    <div class="carousel-header">
        <h2 class="carousel-title">Explore Categories</h2>
        <p class="carousel-subtitle">Click any category to explore our content</p>
    </div>

    <div class="category-grid">
        <a href="/category/finance/" class="category-card">
            <div class="category-emoji">💰</div>
            <div class="category-overlay">
                <h3 class="category-name">Finance</h3>
                <p class="category-description">Banking & Investments</p>
            </div>
        </a>

        <a href="/category/technology/" class="category-card">
            <div class="category-emoji">💻</div>
            <div class="category-overlay">
                <h3 class="category-name">Technology</h3>
                <p class="category-description">AI & Innovation</p>
            </div>
        </a>

        <a href="/category/business/" class="category-card">
            <div class="category-emoji">📊</div>
            <div class="category-overlay">
                <h3 class="category-name">Business</h3>
                <p class="category-description">Strategy & Growth</p>
            </div>
        </a>

        <a href="/category/economy/" class="category-card">
            <div class="category-emoji">📈</div>
            <div class="category-overlay">
                <h3 class="category-name">Economy</h3>
                <p class="category-description">Markets & Trade</p>
            </div>
        </a>

        <a href="/category/entertainment/" class="category-card">
            <div class="category-emoji">🎬</div>
            <div class="category-overlay">
                <h3 class="category-name">Entertainment</h3>
                <p class="category-description">Media & Culture</p>
            </div>
        </a>

        <a href="/category/politics/" class="category-card">
            <div class="category-emoji">🏛️</div>
            <div class="category-overlay">
                <h3 class="category-name">Politics</h3>
                <p class="category-description">Policy & Governance</p>
            </div>
        </a>

        <a href="/category/travel/" class="category-card">
            <div class="category-emoji">✈️</div>
            <div class="category-overlay">
                <h3 class="category-name">Travel</h3>
                <p class="category-description">Destinations & Adventures</p>
            </div>
        </a>

        <a href="/category/world-news/" class="category-card">
            <div class="category-emoji">🌍</div>
            <div class="category-overlay">
                <h3 class="category-name">World News</h3>
                <p class="category-description">Global Updates</p>
            </div>
        </a>
    </div>
</div>
"""

# Option 2: Remove carousel entirely
EMPTY_CONTENT = """
<!-- Carousel removed - homepage content -->
<div style="text-align: center; padding: 40px;">
    <h1>Welcome to Sphere Vista 360</h1>
    <p>Your source for global news and insights</p>
</div>
"""

def rollback_carousel():
    """Rollback carousel changes to a simple working version"""
    print("=" * 70)
    print("🔄 ROLLING BACK CAROUSEL CHANGES")
    print("=" * 70)
    print()

    print("Options:")
    print("1. Replace with simple static grid (recommended)")
    print("2. Remove carousel entirely")
    print()

    # Default to option 1 - simple working version
    choice = "1"
    print(f"Using option {choice}: Simple static grid")

    if choice == "1":
        content = SIMPLE_CAROUSEL_HTML
        description = "simple static category grid"
    else:
        content = EMPTY_CONTENT
        description = "empty homepage"

    print(f"Rolling back to {description}...")
    print("-" * 70)

    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/2412"

    response = requests.post(
        url,
        json={'content': content},
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )

    if response.status_code == 200:
        print("✅ Carousel rolled back successfully!")
        print()
        if choice == "1":
            print("📋 What was restored:")
            print("   ✅ Simple category grid with emojis")
            print("   ✅ Clickable category navigation")
            print("   ✅ Mobile-responsive design")
            print("   ✅ Clean, professional appearance")
            print("   ❌ Removed: Auto-scrolling, complex animations")
        else:
            print("🗑️ Carousel completely removed")
        print()
        print("=" * 70)
        print("✅ ROLLBACK COMPLETE!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Clear browser cache (Ctrl+F5)")
        print("  2. Refresh homepage")
        print("  3. Verify simple grid is working")
        print()
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response: {response.text[:300]}")
        return False

if __name__ == "__main__":
    if not all([WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("❌ Error: Missing WordPress credentials")
    else:
        rollback_carousel()