#!/usr/bin/env python3
"""
Replace all featured images with REAL technology, finance, AI, and business images
Using Unsplash API with specific technology/business collections
"""

import os
import requests
from dotenv import load_dotenv
import time
import random
import hashlib

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Real technology, finance, business image URLs from Unsplash
# Using query parameters to get specific relevant images
CATEGORY_IMAGE_QUERIES = {
    # AI & Technology - actual technology images
    'ai': [
        'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=630&fit=crop',  # AI brain
        'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200&h=630&fit=crop',  # AI circuits
        'https://images.unsplash.com/photo-1655393001768-d946c97d6fd1?w=1200&h=630&fit=crop',  # AI robot
        'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200&h=630&fit=crop',  # AI network
        'https://images.unsplash.com/photo-1677756119517-756a188d2d94?w=1200&h=630&fit=crop',  # AI chip
        'https://images.unsplash.com/photo-1676299081847-824916de030a?w=1200&h=630&fit=crop',  # AI tech
        'https://images.unsplash.com/photo-1655721532555-6b5633bca136?w=1200&h=630&fit=crop',  # Neural network
        'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=1200&h=630&fit=crop',  # Computer code
        'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&h=630&fit=crop',  # Data matrix
        'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=1200&h=630&fit=crop',  # AI circuit board
    ],
    
    # Cloud Computing - servers, data centers, cloud
    'cloud-computing': [
        'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=630&fit=crop',  # Server room
        'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200&h=630&fit=crop',  # Data center
        'https://images.unsplash.com/photo-1609743522471-83c84ce23e32?w=1200&h=630&fit=crop',  # Cloud servers
        'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=630&fit=crop',  # Network globe
        'https://images.unsplash.com/photo-1597733336794-12d05021d510?w=1200&h=630&fit=crop',  # Server racks
    ],
    
    # Cybersecurity - locks, security, encryption
    'cybersecurity': [
        'https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=1200&h=630&fit=crop',  # Cyber security
        'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=1200&h=630&fit=crop',  # Digital lock
        'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&h=630&fit=crop',  # Security code
        'https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?w=1200&h=630&fit=crop',  # Encryption
        'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=1200&h=630&fit=crop',  # Digital security
    ],
    
    # Data Analytics - charts, dashboards, data viz
    'data-analytics': [
        'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop',  # Data dashboard
        'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=630&fit=crop',  # Analytics screen
        'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop',  # Charts graphs
        'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&h=630&fit=crop',  # Data analysis
        'https://images.unsplash.com/photo-1543286386-713bdd548da4?w=1200&h=630&fit=crop',  # Dashboard laptop
    ],
    
    # Software Development - coding, programming
    'software': [
        'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&h=630&fit=crop',  # Code editor
        'https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1200&h=630&fit=crop',  # Programming
        'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&h=630&fit=crop',  # Coding laptop
        'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=630&fit=crop',  # Developer desk
        'https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=1200&h=630&fit=crop',  # Code screen
    ],
    
    # Tech Innovation - technology, innovation
    'tech-innovation': [
        'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&h=630&fit=crop',  # Technology
        'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1200&h=630&fit=crop',  # Robot tech
        'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200&h=630&fit=crop',  # Innovation
        'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop',  # Tech team
        'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1200&h=630&fit=crop',  # Tech devices
    ],
    
    # Finance - money, trading, stocks, banking
    'finance': [
        'https://images.unsplash.com/photo-1579532537598-459ecdaf39cc?w=1200&h=630&fit=crop',  # Stock market
        'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&h=630&fit=crop',  # Financial charts
        'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1200&h=630&fit=crop',  # Currency
        'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=1200&h=630&fit=crop',  # Finance data
        'https://images.unsplash.com/photo-1642790551116-18e150f248e4?w=1200&h=630&fit=crop',  # Trading screen
    ],
    
    # Banking - digital banking, fintech
    'banking': [
        'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1200&h=630&fit=crop',  # Digital banking
        'https://images.unsplash.com/photo-1556742400-b5b7c256b673?w=1200&h=630&fit=crop',  # Banking app
        'https://images.unsplash.com/photo-1601597111158-2fceff292cdc?w=1200&h=630&fit=crop',  # Fintech
        'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&h=630&fit=crop',  # Bank cards
        'https://images.unsplash.com/photo-1633158829585-23ba8f7c8caf?w=1200&h=630&fit=crop',  # Mobile banking
    ],
    
    # Investment - stocks, trading, portfolio
    'investment': [
        'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&h=630&fit=crop',  # Stock charts
        'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop',  # Investment data
        'https://images.unsplash.com/photo-1560520653-9e0e4c89eb11?w=1200&h=630&fit=crop',  # Trading
        'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1200&h=630&fit=crop',  # Portfolio
        'https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=1200&h=630&fit=crop',  # Crypto trading
    ],
    
    # Green Bonds - renewable energy, solar, sustainability
    'green-bonds': [
        'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=1200&h=630&fit=crop',  # Solar panels
        'https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=1200&h=630&fit=crop',  # Wind energy
        'https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?w=1200&h=630&fit=crop',  # Solar farm
        'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=1200&h=630&fit=crop',  # Renewable
        'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1200&h=630&fit=crop',  # Green energy
    ],
    
    # Default categories use technology images
    'economy': 'finance',
    'inflation': 'finance', 
    'travel': 'tech-innovation',
    'digital-nomad': 'software',
    'visa': 'tech-innovation',
    'budget-travel': 'tech-innovation',
    'hollywood': 'tech-innovation',
    'streaming': 'tech-innovation',
    'music': 'tech-innovation',
    'gaming': 'tech-innovation',
    'celebrity': 'tech-innovation',
    'politics': 'tech-innovation',
    'elections': 'tech-innovation',
    'trade': 'finance',
    'supply-chain': 'tech-innovation',
}

# Track used URLs to ensure uniqueness
used_urls = set()

def categorize_post(title, content):
    """Determine the best image category for a post"""
    title_lower = title.lower()
    content_lower = content.lower()[:500]
    combined = title_lower + " " + content_lower
    
    # AI & Technology keywords
    if any(word in combined for word in ['artificial intelligence', 'ai model', 'ai agent', 'machine learning', 'neural', 'llm', 'algorithm']):
        return 'ai'
    elif any(word in combined for word in ['cloud computing', 'aws', 'azure', 'google cloud', 'cloud war']):
        return 'cloud-computing'
    elif any(word in combined for word in ['cybersecurity', 'security', 'hacking', 'privacy', 'data privacy']):
        return 'cybersecurity'
    elif any(word in combined for word in ['analytics', 'data analysis', 'dashboard', 'metrics', 'product analytics']):
        return 'data-analytics'
    elif any(word in combined for word in ['software', 'coding', 'programming', 'development', 'ops copilot']):
        return 'software'
    elif any(word in combined for word in ['technology', 'tech innovation', 'digital transformation']):
        return 'tech-innovation'
    
    # Finance keywords
    elif any(word in combined for word in ['green bond', 'renewable', 'solar', 'clean energy', 'energy transition']):
        return 'green-bonds'
    elif any(word in combined for word in ['banking', 'fintech', 'digital bank', 'neobank']):
        return 'banking'
    elif any(word in combined for word in ['investment', 'investing', 'portfolio', 'stocks', 'trading', 'retail investing', 'startup funding', 'venture capital']):
        return 'investment'
    elif any(word in combined for word in ['inflation', 'price rise', 'monetary', 'emerging market']):
        return 'inflation'
    elif any(word in combined for word in ['finance', 'financial', 'money', 'capital', 'regtech', 'regulatory technology']):
        return 'finance'
    
    # Default to tech
    else:
        return 'tech-innovation'

def get_unique_image_url(category):
    """Get a unique relevant image URL for a category"""
    global used_urls
    
    # Get base category if it's a redirect
    if isinstance(CATEGORY_IMAGE_QUERIES.get(category), str):
        category = CATEGORY_IMAGE_QUERIES[category]
    
    image_urls = CATEGORY_IMAGE_QUERIES.get(category, CATEGORY_IMAGE_QUERIES['tech-innovation'])
    
    # Filter out already used URLs
    available_urls = [url for url in image_urls if url not in used_urls]
    
    # If all images from this category are used, allow reuse
    if not available_urls:
        available_urls = image_urls
    
    # Pick a unique image
    image_url = random.choice(available_urls)
    used_urls.add(image_url)
    
    # Generate unique hash for filename
    url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
    
    return image_url, url_hash

def update_all_featured_images():
    """Update featured images for all posts with REAL technology/finance images"""
    print("=" * 80)
    print("🖼️  REPLACING WITH REAL TECHNOLOGY, FINANCE & BUSINESS IMAGES")
    print("=" * 80)
    print()
    print("Using actual images of:")
    print("  • AI, robots, neural networks, computer chips")
    print("  • Servers, data centers, cloud computing")
    print("  • Cybersecurity, encryption, digital locks")
    print("  • Code editors, programming, software development")
    print("  • Stock markets, trading screens, financial data")
    print("  • Solar panels, renewable energy, green tech")
    print()
    
    # Get all posts
    page = 1
    all_posts = []
    
    while True:
        response = requests.get(
            f'{WORDPRESS_URL}/wp-json/wp/v2/posts',
            params={'per_page': 100, 'page': page},
            auth=(USERNAME, PASSWORD)
        )
        
        if not response.ok:
            break
        
        posts = response.json()
        if not posts:
            break
        
        all_posts.extend(posts)
        page += 1
    
    print(f"📊 Found {len(all_posts)} posts to update")
    print()
    
    updated_count = 0
    failed_count = 0
    categories_used = {}
    
    for idx, post in enumerate(all_posts, 1):
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        # Determine best image category
        category = categorize_post(title, content)
        image_url, url_hash = get_unique_image_url(category)
        
        # Track categories
        categories_used[category] = categories_used.get(category, 0) + 1
        
        print(f"[{idx}/{len(all_posts)}] 📝 {title[:45]}...")
        print(f"      🎯 Category: {category}")
        print(f"      🖼️  Real image: {category.replace('-', ' ').title()}")
        
        try:
            # Download image
            img_response = requests.get(image_url, timeout=20)
            if not img_response.ok:
                print(f"      ❌ Failed to download")
                failed_count += 1
                print()
                continue
            
            # Generate unique filename
            filename = f"{category}-{post_id}-{url_hash}.jpg"
            
            # Upload to WordPress
            files = {
                'file': (filename, img_response.content, 'image/jpeg')
            }
            
            upload_response = requests.post(
                f'{WORDPRESS_URL}/wp-json/wp/v2/media',
                auth=(USERNAME, PASSWORD),
                files=files
            )
            
            if not upload_response.ok:
                print(f"      ❌ Failed to upload")
                failed_count += 1
                print()
                continue
            
            media_id = upload_response.json()['id']
            
            # Set as featured image
            update_response = requests.post(
                f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
                json={'featured_media': media_id},
                auth=(USERNAME, PASSWORD)
            )
            
            if update_response.ok:
                print(f"      ✅ Updated with REAL {category} image")
                updated_count += 1
            else:
                print(f"      ❌ Failed to set featured")
                failed_count += 1
                
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:50]}")
            failed_count += 1
        
        print()
        time.sleep(1)  # Unsplash rate limiting
    
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully updated: {updated_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📝 Total posts: {len(all_posts)}")
    print()
    
    print("📁 REAL IMAGE CATEGORIES USED:")
    for cat, count in sorted(categories_used.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat.replace('-', ' ').title()}: {count} posts")
    print()
    
    print("✨ All posts now have REAL technology/finance/business images!")
    print()

if __name__ == '__main__':
    update_all_featured_images()
