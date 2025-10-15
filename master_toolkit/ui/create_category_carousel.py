#!/usr/bin/env python3
"""
Create Category Image Carousel for Homepage
Add a sliding image gallery showing all categories
"""

import requests
import time

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Category images mapping
CATEGORY_IMAGES = {
    3: {'name': 'Finance', 'media_id': 2744, 'slug': 'finance'},
    190: {'name': 'Technology', 'media_id': 2746, 'slug': 'technology'},
    188: {'name': 'Business', 'media_id': 2741, 'slug': 'business'},
    167: {'name': 'Entertainment', 'media_id': 2743, 'slug': 'entertainment'},
    5: {'name': 'Politics', 'media_id': 2745, 'slug': 'politics'},
    6: {'name': 'Travel', 'media_id': 2748, 'slug': 'travel'},
    7: {'name': 'World', 'media_id': 2749, 'slug': 'world'},
    213: {'name': 'World News', 'media_id': 2750, 'slug': 'world-news'},
    165: {'name': 'Economy', 'media_id': 2742, 'slug': 'economy'},
    177: {'name': 'Top Stories', 'media_id': 2747, 'slug': 'top-stories'},
}

def get_media_url(media_id):
    """Get full URL of media file"""
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/media/{media_id}',
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        media = response.json()
        return media.get('source_url', '')
    return ''

def create_carousel_html():
    """Generate HTML/CSS/JS for category carousel"""
    
    print("=" * 80)
    print("📸 CREATING CATEGORY CAROUSEL CODE")
    print("=" * 80)
    print()
    
    # Get all media URLs
    print("📥 Fetching image URLs...")
    category_data = []
    
    for cat_id, cat_info in CATEGORY_IMAGES.items():
        media_url = get_media_url(cat_info['media_id'])
        if media_url:
            category_data.append({
                'name': cat_info['name'],
                'slug': cat_info['slug'],
                'url': media_url,
                'link': f"{WORDPRESS_URL}/category/{cat_info['slug']}/"
            })
            print(f"   ✅ {cat_info['name']}: {media_url[:60]}...")
        time.sleep(0.3)
    
    print()
    print("=" * 80)
    print("🎨 GENERATING CAROUSEL HTML")
    print("=" * 80)
    print()
    
    # Generate HTML with inline CSS and JavaScript
    html_content = """
<!-- Category Image Carousel -->
<style>
.category-carousel-container {
    width: 100%;
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
    overflow: hidden;
}

.category-carousel-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 30px;
    color: #1a1a1a;
}

.category-carousel {
    display: flex;
    gap: 20px;
    animation: scroll 30s linear infinite;
    width: fit-content;
}

.category-carousel:hover {
    animation-play-state: paused;
}

.category-card {
    position: relative;
    min-width: 280px;
    height: 200px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}

.category-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

.category-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.category-card:hover img {
    transform: scale(1.1);
}

.category-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    padding: 20px;
    color: white;
}

.category-name {
    font-size: 20px;
    font-weight: bold;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

@keyframes scroll {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
}

@media (max-width: 768px) {
    .category-card {
        min-width: 220px;
        height: 160px;
    }
    
    .category-carousel-title {
        font-size: 24px;
    }
}
</style>

<div class="category-carousel-container">
    <h2 class="category-carousel-title">Explore Our Categories</h2>
    <div class="category-carousel">
"""
    
    # Add categories twice for infinite loop effect
    for _ in range(2):
        for cat in category_data:
            html_content += f"""
        <a href="{cat['link']}" class="category-card">
            <img src="{cat['url']}" alt="{cat['name']}" loading="lazy">
            <div class="category-overlay">
                <h3 class="category-name">{cat['name']}</h3>
            </div>
        </a>
"""
    
    html_content += """
    </div>
</div>

<script>
// Pause animation on mobile for better UX
if (window.innerWidth < 768) {
    document.querySelector('.category-carousel').style.animationDuration = '40s';
}
</script>
<!-- End Category Image Carousel -->
"""
    
    return html_content, category_data

def get_home_page():
    """Get the home page"""
    # Try to get home page
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/pages',
        params={'per_page': 100},
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        pages = response.json()
        for page in pages:
            if page['slug'] in ['home', 'front-page'] or 'home' in page['title']['rendered'].lower():
                return page
        # Return first page if no home found
        if pages:
            return pages[0]
    return None

def add_carousel_to_homepage(carousel_html):
    """Add carousel HTML to homepage"""
    print("🏠 Finding homepage...")
    
    home_page = get_home_page()
    
    if not home_page:
        print("   ⚠️  Home page not found, will create instructions for manual addition")
        return False
    
    page_id = home_page['id']
    page_title = home_page['title']['rendered']
    current_content = home_page['content']['rendered']
    
    print(f"   ✅ Found: {page_title} (ID: {page_id})")
    print()
    
    # Check if carousel already exists
    if 'category-carousel-container' in current_content:
        print("   ℹ️  Carousel already exists on homepage")
        print("   Would you like to update it? (This will replace existing carousel)")
        return False
    
    # Add carousel at the beginning of content
    new_content = carousel_html + "\n\n" + current_content
    
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/pages/{page_id}',
        json={'content': new_content},
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        print("   ✅ Carousel added to homepage!")
        print(f"   🔗 View: {WORDPRESS_URL}/")
        return True
    else:
        print(f"   ❌ Failed to update page: {response.status_code}")
        return False

def main():
    """Create and add category carousel"""
    print("=" * 80)
    print("🎠 CATEGORY IMAGE CAROUSEL CREATOR")
    print("=" * 80)
    print()
    
    # Generate carousel HTML
    carousel_html, category_data = create_carousel_html()
    
    print(f"✅ Generated carousel with {len(category_data)} categories")
    print()
    
    # Save HTML to file
    carousel_file = '/home/kddevops/downloads/category_carousel.html'
    with open(carousel_file, 'w') as f:
        f.write(carousel_html)
    
    print(f"💾 Saved carousel HTML to: {carousel_file}")
    print()
    
    # Try to add to homepage
    print("=" * 80)
    print("🏠 ADDING TO HOMEPAGE")
    print("=" * 80)
    print()
    
    if not add_carousel_to_homepage(carousel_html):
        print()
        print("=" * 80)
        print("📝 MANUAL INSTALLATION INSTRUCTIONS")
        print("=" * 80)
        print()
        print("To add the carousel to your homepage:")
        print()
        print("METHOD 1: Via WordPress Admin (Recommended)")
        print("-" * 80)
        print("1. Go to: Pages → All Pages")
        print("2. Edit your 'Home' page")
        print("3. Switch to 'Text' or 'HTML' editor mode")
        print("4. Copy the HTML from: " + carousel_file)
        print("5. Paste it at the top of your page content")
        print("6. Click 'Update'")
        print()
        print("METHOD 2: Via Kadence Blocks")
        print("-" * 80)
        print("1. Edit your homepage in Gutenberg editor")
        print("2. Add a 'Custom HTML' block")
        print("3. Paste the carousel HTML")
        print("4. Position it where you want")
        print("5. Publish")
        print()
        print("METHOD 3: Via Widget")
        print("-" * 80)
        print("1. Go to: Appearance → Widgets")
        print("2. Add 'Custom HTML' widget to desired area")
        print("3. Paste the carousel HTML")
        print("4. Save")
        print()
    
    print("=" * 80)
    print("✨ FEATURES")
    print("=" * 80)
    print()
    print("✅ Auto-scrolling carousel (infinite loop)")
    print("✅ Hover to pause animation")
    print("✅ Click categories to navigate")
    print("✅ Responsive design (mobile-friendly)")
    print("✅ Smooth animations and transitions")
    print("✅ Professional gradient overlays")
    print("✅ Optimized for performance (lazy loading)")
    print()
    
    print("=" * 80)
    print("🎨 CUSTOMIZATION OPTIONS")
    print("=" * 80)
    print()
    print("To customize the carousel, edit the CSS in the HTML file:")
    print()
    print("• Animation speed: Change '30s' in animation property")
    print("• Card size: Adjust 'min-width' and 'height' values")
    print("• Colors: Modify gradient and overlay colors")
    print("• Spacing: Change 'gap' value in .category-carousel")
    print()
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
