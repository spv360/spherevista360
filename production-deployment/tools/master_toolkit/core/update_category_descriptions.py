#!/usr/bin/env python3
"""
Update Category Descriptions and Images
Add relevant descriptions and featured images for all categories
"""

import requests
import time

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Category descriptions aligned with finance/tech focus
CATEGORY_DATA = {
    'finance': {
        'description': 'Expert insights on personal finance, investment strategies, market analysis, and wealth management. Stay informed about financial trends, banking innovations, and smart money management techniques.',
        'image_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&q=80',  # Stock charts
    },
    'technology': {
        'description': 'Cutting-edge technology news covering artificial intelligence, cloud computing, cybersecurity, software development, and digital innovation. Explore the latest tech trends shaping our digital future.',
        'image_url': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&q=80',  # Tech background
    },
    'business': {
        'description': 'Business strategy, entrepreneurship, startup insights, and corporate innovation. Discover actionable business intelligence, market trends, and leadership perspectives for modern enterprises.',
        'image_url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80',  # Business meeting
    },
    'entertainment': {
        'description': 'Technology and innovation in entertainment, streaming platforms, digital media, gaming industry trends, and the intersection of tech with creative content production.',
        'image_url': 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=1200&q=80',  # Digital entertainment
    },
    'politics': {
        'description': 'Political analysis, policy insights, election coverage, and the impact of technology on governance. Understanding how political decisions shape economic and technological landscapes.',
        'image_url': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1200&q=80',  # Government buildings
    },
    'travel': {
        'description': 'Smart travel strategies, digital nomad insights, visa regulations, travel technology, and the future of remote work. Explore how technology is transforming modern travel experiences.',
        'image_url': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&q=80',  # Travel
    },
    'world': {
        'description': 'Global affairs, international trade, geopolitical analysis, and cross-border technology trends. Stay informed about worldwide economic shifts and their impact on markets.',
        'image_url': 'https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=1200&q=80',  # Globe
    },
    'world-news': {
        'description': 'Breaking international news, global economic developments, and worldwide technology adoption. Comprehensive coverage of events shaping the global financial and tech landscape.',
        'image_url': 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1200&q=80',  # News
    },
    'economy': {
        'description': 'Economic trends, market forecasts, monetary policy analysis, and financial indicators. Expert perspectives on inflation, interest rates, GDP growth, and economic sustainability.',
        'image_url': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1200&q=80',  # Economy/finance
    },
    'top-stories': {
        'description': 'Curated selection of the most important finance, technology, and business stories. Essential reading for staying ahead in the fast-paced world of innovation and markets.',
        'image_url': 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&q=80',  # Featured content
    },
}

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        if response.ok:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"   ⚠️  Failed to download image: {e}")
    return False

def upload_image_to_media_library(image_path, title):
    """Upload image to WordPress media library"""
    try:
        with open(image_path, 'rb') as img:
            files = {'file': (image_path, img, 'image/jpeg')}
            headers = {'Content-Disposition': f'attachment; filename="{image_path}"'}
            
            response = requests.post(
                f'{WORDPRESS_URL}/wp-json/wp/v2/media',
                files=files,
                headers=headers,
                auth=(USERNAME, PASSWORD)
            )
            
            if response.ok:
                return response.json()['id']
    except Exception as e:
        print(f"   ⚠️  Failed to upload image: {e}")
    return None

def update_category(cat_id, slug, name, description, image_url):
    """Update category with description and image"""
    print(f"\n📁 Updating: {name}")
    print(f"   Slug: {slug}")
    
    # Update description
    update_data = {'description': description}
    
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/categories/{cat_id}',
        json=update_data,
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        print(f"   ✅ Description updated")
    else:
        print(f"   ❌ Failed to update description: {response.status_code}")
        return False
    
    # Download and upload category image
    print(f"   📥 Downloading category image...")
    image_filename = f'/tmp/category_{slug}.jpg'
    
    if download_image(image_url, image_filename):
        print(f"   📤 Uploading to media library...")
        media_id = upload_image_to_media_library(image_filename, f'{name} Category')
        
        if media_id:
            print(f"   ✅ Image uploaded (ID: {media_id})")
            
            # Note: Category images need to be set via theme options or ACF
            # WordPress core doesn't support category featured images by default
            # The Kadence theme may support this via customizer
            print(f"   ℹ️  Image uploaded to media library - can be set in category settings")
        else:
            print(f"   ⚠️  Failed to upload image")
    
    time.sleep(1)  # Rate limiting
    return True

def main():
    """Update all categories"""
    print("=" * 80)
    print("🔄 UPDATING CATEGORY DESCRIPTIONS AND IMAGES")
    print("=" * 80)
    
    # Get all categories
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/categories',
        params={'per_page': 100},
        auth=(USERNAME, PASSWORD)
    )
    
    if not response.ok:
        print("❌ Failed to fetch categories")
        return
    
    categories = response.json()
    updated_count = 0
    skipped_count = 0
    
    for cat in categories:
        slug = cat['slug']
        cat_id = cat['id']
        name = cat['name']
        
        # Skip Uncategorized
        if slug == 'uncategorized':
            print(f"\n⏭️  Skipping: {name}")
            skipped_count += 1
            continue
        
        # Get data for this category
        if slug in CATEGORY_DATA:
            data = CATEGORY_DATA[slug]
            if update_category(cat_id, slug, name, data['description'], data['image_url']):
                updated_count += 1
            else:
                skipped_count += 1
        else:
            print(f"\n⚠️  No data defined for: {name} ({slug})")
            skipped_count += 1
    
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Updated: {updated_count} categories")
    print(f"⏭️  Skipped: {skipped_count} categories")
    print(f"📁 Total: {len(categories)} categories")
    print()
    print("=" * 80)
    print()
    
    print("💡 NEXT STEPS:")
    print("   1. Category images are uploaded to media library")
    print("   2. To set category images in Kadence theme:")
    print("      - Go to WordPress Admin → Posts → Categories")
    print("      - Edit each category")
    print("      - Look for 'Category Image' field")
    print("      - Select the uploaded image from media library")
    print()

if __name__ == '__main__':
    main()
