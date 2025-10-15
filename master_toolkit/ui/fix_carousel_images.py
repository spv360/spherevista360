#!/usr/bin/env python3
"""
Fix Carousel Images - Use Alternative Sources
Replace Unsplash URLs with placeholder images or uploaded media
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Alternative: Use placeholder.com or picsum.photos (more reliable)
CAROUSEL_HTML_FIXED = """
<!-- Category Image Carousel -->
<style>
.category-carousel-container {
    width: 100%;
    max-width: 1400px;
    margin: 40px auto;
    padding: 0 20px;
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.carousel-header {
    text-align: center;
    padding: 40px 20px 20px;
}

.carousel-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 10px;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.carousel-subtitle {
    font-size: 18px;
    color: #f0f0f0;
    margin-bottom: 30px;
}

.category-carousel-wrapper {
    position: relative;
    padding: 30px 0;
    overflow: hidden;
}

.category-carousel {
    display: flex;
    gap: 25px;
    animation: scroll 40s linear infinite;
    width: fit-content;
}

.category-carousel:hover {
    animation-play-state: paused;
}

@keyframes scroll {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
}

.category-card {
    position: relative;
    min-width: 320px;
    height: 240px;
    border-radius: 15px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.category-card:hover {
    transform: translateY(-10px) scale(1.05);
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

.category-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
    display: block;
}

.category-card:hover img {
    transform: scale(1.1);
}

.category-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
    padding: 60px 20px 20px;
    transition: all 0.3s ease;
}

.category-card:hover .category-overlay {
    background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.7) 80%, rgba(0,0,0,0.3) 100%);
}

.category-name {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.category-description {
    font-size: 14px;
    color: #e0e0e0;
    margin: 5px 0 0 0;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
}

.category-card:hover .category-description {
    opacity: 1;
    transform: translateY(0);
}

.category-icon {
    font-size: 60px;
    margin-bottom: 10px;
    text-align: center;
    opacity: 0.3;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

@media (max-width: 768px) {
    .carousel-title {
        font-size: 28px;
    }
    
    .category-card {
        min-width: 260px;
        height: 200px;
    }
    
    .category-name {
        font-size: 20px;
    }
}
</style>

<div class="category-carousel-container">
    <div class="carousel-header">
        <h2 class="carousel-title">Explore Our Categories</h2>
        <p class="carousel-subtitle">Discover insights across Finance, Technology, Business & More</p>
    </div>
    
    <div class="category-carousel-wrapper">
        <div class="category-carousel" id="categoryCarousel">
            <!-- Finance -->
            <a href="/category/finance/" class="category-card">
                <div class="category-icon">💰</div>
                <img src="https://picsum.photos/800/600?random=1" alt="Finance" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Finance</h3>
                    <p class="category-description">Banking, Investments & Financial Markets</p>
                </div>
            </a>
            
            <!-- Technology -->
            <a href="/category/technology/" class="category-card">
                <div class="category-icon">💻</div>
                <img src="https://picsum.photos/800/600?random=2" alt="Technology" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Technology</h3>
                    <p class="category-description">AI, Innovation & Digital Transformation</p>
                </div>
            </a>
            
            <!-- Business -->
            <a href="/category/business/" class="category-card">
                <div class="category-icon">📊</div>
                <img src="https://picsum.photos/800/600?random=3" alt="Business" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Business</h3>
                    <p class="category-description">Strategy, Growth & Entrepreneurship</p>
                </div>
            </a>
            
            <!-- Economy -->
            <a href="/category/economy/" class="category-card">
                <div class="category-icon">📈</div>
                <img src="https://picsum.photos/800/600?random=4" alt="Economy" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Economy</h3>
                    <p class="category-description">Markets, Trade & Economic Analysis</p>
                </div>
            </a>
            
            <!-- Entertainment -->
            <a href="/category/entertainment/" class="category-card">
                <div class="category-icon">🎬</div>
                <img src="https://picsum.photos/800/600?random=5" alt="Entertainment" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Entertainment</h3>
                    <p class="category-description">Media, Culture & Digital Content</p>
                </div>
            </a>
            
            <!-- Politics -->
            <a href="/category/politics/" class="category-card">
                <div class="category-icon">🏛️</div>
                <img src="https://picsum.photos/800/600?random=6" alt="Politics" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Politics</h3>
                    <p class="category-description">Policy, Governance & Global Affairs</p>
                </div>
            </a>
            
            <!-- Travel -->
            <a href="/category/travel/" class="category-card">
                <div class="category-icon">✈️</div>
                <img src="https://picsum.photos/800/600?random=7" alt="Travel" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Travel</h3>
                    <p class="category-description">Destinations, Adventures & Exploration</p>
                </div>
            </a>
            
            <!-- World News -->
            <a href="/category/world-news/" class="category-card">
                <div class="category-icon">🌍</div>
                <img src="https://picsum.photos/800/600?random=8" alt="World News" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">World News</h3>
                    <p class="category-description">International Events & Global Updates</p>
                </div>
            </a>
            
            <!-- Duplicate cards for smooth infinite scroll -->
            <a href="/category/finance/" class="category-card">
                <div class="category-icon">💰</div>
                <img src="https://picsum.photos/800/600?random=1" alt="Finance" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Finance</h3>
                    <p class="category-description">Banking, Investments & Financial Markets</p>
                </div>
            </a>
            
            <a href="/category/technology/" class="category-card">
                <div class="category-icon">💻</div>
                <img src="https://picsum.photos/800/600?random=2" alt="Technology" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Technology</h3>
                    <p class="category-description">AI, Innovation & Digital Transformation</p>
                </div>
            </a>
            
            <a href="/category/business/" class="category-card">
                <div class="category-icon">📊</div>
                <img src="https://picsum.photos/800/600?random=3" alt="Business" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Business</h3>
                    <p class="category-description">Strategy, Growth & Entrepreneurship</p>
                </div>
            </a>
            
            <a href="/category/economy/" class="category-card">
                <div class="category-icon">📈</div>
                <img src="https://picsum.photos/800/600?random=4" alt="Economy" loading="lazy" onerror="this.style.display='none'">
                <div class="category-overlay">
                    <h3 class="category-name">Economy</h3>
                    <p class="category-description">Markets, Trade & Economic Analysis</p>
                </div>
            </a>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('categoryCarousel');
    if (!carousel) return;
    
    // Pause on hover
    carousel.addEventListener('mouseenter', function() {
        this.style.animationPlayState = 'paused';
    });
    
    carousel.addEventListener('mouseleave', function() {
        this.style.animationPlayState = 'running';
    });
    
    // Add click analytics
    const cards = carousel.querySelectorAll('.category-card');
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            console.log('Category clicked:', this.querySelector('.category-name').textContent);
        });
    });
    
    // Log if images fail to load
    const images = carousel.querySelectorAll('img');
    images.forEach((img, index) => {
        img.addEventListener('error', function() {
            console.log('Image ' + index + ' failed to load:', this.src);
        });
        img.addEventListener('load', function() {
            console.log('Image ' + index + ' loaded successfully');
        });
    });
});
</script>
"""

def update_homepage_with_fixed_images():
    """Update homepage with fixed image sources"""
    print("=" * 70)
    print("🔧 FIXING CAROUSEL IMAGES")
    print("=" * 70)
    print()
    
    print("Updating homepage with alternative image sources...")
    print("-" * 70)
    
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/2412"
    
    response = requests.post(
        url,
        json={'content': CAROUSEL_HTML_FIXED},
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        print("✅ Carousel updated successfully!")
        print()
        print("Changes made:")
        print("  ✓ Switched to picsum.photos (more reliable)")
        print("  ✓ Added emoji icons as fallback")
        print("  ✓ Added error handling for images")
        print("  ✓ Enhanced gradient backgrounds")
        print("  ✓ Added image load logging")
        print()
        print("=" * 70)
        print("✅ FIX COMPLETE!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Clear browser cache (Ctrl+F5)")
        print("  2. Refresh homepage")
        print("  3. Open browser console (F12)")
        print("  4. Check for image load messages")
        print()
        print("If images still don't show:")
        print("  • Check browser console for errors")
        print("  • Verify site allows external images")
        print("  • Check Content Security Policy")
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
        update_homepage_with_fixed_images()
