#!/usr/bin/env python3
"""
Complete Carousel Fix
1. Check/Create homepage
2. Add carousel HTML with images
3. Set as static homepage
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Category images from Unsplash (free, high-quality images)
CAROUSEL_HTML = """
<!-- Category Image Carousel -->
<style>
.category-carousel-container {
    width: 100%;
    max-width: 1400px;
    margin: 40px auto;
    padding: 0 20px;
    overflow: hidden;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
    color: #1a1a1a;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.carousel-subtitle {
    font-size: 18px;
    color: #666;
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
                <img src="https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&h=600&fit=crop" alt="Finance" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Finance</h3>
                    <p class="category-description">Banking, Investments & Financial Markets</p>
                </div>
            </a>
            
            <!-- Technology -->
            <a href="/category/technology/" class="category-card">
                <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=600&fit=crop" alt="Technology" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Technology</h3>
                    <p class="category-description">AI, Innovation & Digital Transformation</p>
                </div>
            </a>
            
            <!-- Business -->
            <a href="/category/business/" class="category-card">
                <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=600&fit=crop" alt="Business" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Business</h3>
                    <p class="category-description">Strategy, Growth & Entrepreneurship</p>
                </div>
            </a>
            
            <!-- Economy -->
            <a href="/category/economy/" class="category-card">
                <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop" alt="Economy" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Economy</h3>
                    <p class="category-description">Markets, Trade & Economic Analysis</p>
                </div>
            </a>
            
            <!-- Entertainment -->
            <a href="/category/entertainment/" class="category-card">
                <img src="https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=800&h=600&fit=crop" alt="Entertainment" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Entertainment</h3>
                    <p class="category-description">Media, Culture & Digital Content</p>
                </div>
            </a>
            
            <!-- Politics -->
            <a href="/category/politics/" class="category-card">
                <img src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&h=600&fit=crop" alt="Politics" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Politics</h3>
                    <p class="category-description">Policy, Governance & Global Affairs</p>
                </div>
            </a>
            
            <!-- Travel -->
            <a href="/category/travel/" class="category-card">
                <img src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=600&fit=crop" alt="Travel" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Travel</h3>
                    <p class="category-description">Destinations, Adventures & Exploration</p>
                </div>
            </a>
            
            <!-- World News -->
            <a href="/category/world-news/" class="category-card">
                <img src="https://images.unsplash.com/photo-1526666923127-b2970f64b422?w=800&h=600&fit=crop" alt="World News" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">World News</h3>
                    <p class="category-description">International Events & Global Updates</p>
                </div>
            </a>
            
            <!-- Duplicate cards for smooth infinite scroll -->
            <a href="/category/finance/" class="category-card">
                <img src="https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&h=600&fit=crop" alt="Finance" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Finance</h3>
                    <p class="category-description">Banking, Investments & Financial Markets</p>
                </div>
            </a>
            
            <a href="/category/technology/" class="category-card">
                <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=600&fit=crop" alt="Technology" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Technology</h3>
                    <p class="category-description">AI, Innovation & Digital Transformation</p>
                </div>
            </a>
            
            <a href="/category/business/" class="category-card">
                <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=600&fit=crop" alt="Business" loading="lazy">
                <div class="category-overlay">
                    <h3 class="category-name">Business</h3>
                    <p class="category-description">Strategy, Growth & Entrepreneurship</p>
                </div>
            </a>
            
            <a href="/category/economy/" class="category-card">
                <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop" alt="Economy" loading="lazy">
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
    
    // Add click analytics (optional)
    const cards = carousel.querySelectorAll('.category-card');
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            console.log('Category clicked:', this.querySelector('.category-name').textContent);
        });
    });
});
</script>
"""

def get_or_create_homepage():
    """Get existing Home page or create one"""
    print("1️⃣  Checking for Homepage...")
    print("-" * 70)
    
    # Check for existing Home page
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages"
    params = {'search': 'home', 'per_page': 50}
    
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        pages = response.json()
        for page in pages:
            title = page['title']['rendered'].lower()
            if title == 'home' or title == 'homepage':
                print(f"   ✅ Found existing page: {page['title']['rendered']} (ID: {page['id']})")
                return page['id']
    
    # Create new Home page
    print("   📝 Creating new Home page...")
    
    response = requests.post(
        url,
        json={
            'title': 'Home',
            'content': CAROUSEL_HTML,
            'status': 'publish',
            'slug': 'home'
        },
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 201:
        page = response.json()
        print(f"   ✅ Created Home page (ID: {page['id']})")
        return page['id']
    else:
        print(f"   ❌ Failed to create page: {response.status_code}")
        return None

def update_homepage_content(page_id):
    """Update homepage with carousel HTML"""
    print("\n2️⃣  Adding Carousel to Homepage...")
    print("-" * 70)
    
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{page_id}"
    
    response = requests.post(
        url,
        json={'content': CAROUSEL_HTML},
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        print("   ✅ Carousel HTML added successfully!")
        print(f"   📊 Content: {len(CAROUSEL_HTML)} characters")
        print(f"   🖼️  Images: 8 category cards with images")
        return True
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False

def set_static_homepage(page_id):
    """Set page as static homepage"""
    print("\n3️⃣  Setting as Static Homepage...")
    print("-" * 70)
    
    # Note: This requires admin access which might be restricted
    # Manual method will be provided as fallback
    
    print(f"   Page ID to set: {page_id}")
    print("   ⚠️  Note: API may restrict this operation")
    print()
    print("   Manual Setup Required:")
    print("   1. Go to: https://spherevista360.com/wp-admin/options-reading.php")
    print("   2. Under 'Your homepage displays', select 'A static page'")
    print(f"   3. Choose 'Home' (ID: {page_id}) as 'Homepage'")
    print("   4. Click 'Save Changes'")
    
    return True

def verify_setup(page_id):
    """Verify the carousel setup"""
    print("\n4️⃣  Verification...")
    print("-" * 70)
    
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{page_id}"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        page = response.json()
        content = page['content']['rendered']
        
        has_carousel = 'category-carousel' in content
        has_images = content.count('<img') > 0
        image_count = content.count('<img')
        
        print(f"   Page URL: {page['link']}")
        print(f"   Carousel code: {'✅ Present' if has_carousel else '❌ Missing'}")
        print(f"   Images: {'✅ ' + str(image_count) + ' images' if has_images else '❌ No images'}")
        
        return has_carousel and has_images
    
    return False

def main():
    print("=" * 70)
    print("🎨 COMPLETE CAROUSEL FIX")
    print("=" * 70)
    print()
    
    if not all([WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("❌ Error: Missing WordPress credentials")
        return
    
    print(f"🌐 Site: {WORDPRESS_BASE_URL}")
    print()
    
    # Get or create homepage
    page_id = get_or_create_homepage()
    
    if not page_id:
        print("\n❌ Failed to get/create homepage")
        return
    
    # Update with carousel
    if update_homepage_content(page_id):
        # Set as static homepage (manual step required)
        set_static_homepage(page_id)
        
        # Verify
        if verify_setup(page_id):
            print("\n" + "=" * 70)
            print("✅ CAROUSEL SETUP COMPLETE!")
            print("=" * 70)
            print()
            print("📋 NEXT STEPS:")
            print("   1. Clear your browser cache (Ctrl+F5)")
            print("   2. Set page as static homepage in WordPress admin")
            print("   3. Visit: https://spherevista360.com")
            print()
            print("🎉 Your carousel should now be visible!")
        else:
            print("\n⚠️  Setup completed but verification failed")
    else:
        print("\n❌ Failed to add carousel content")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
