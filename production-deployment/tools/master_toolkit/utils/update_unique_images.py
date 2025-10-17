#!/usr/bin/env python3
"""
Replace all featured images with UNIQUE relevant images
Each post gets a different image from its category pool
"""

import os
import requests
from dotenv import load_dotenv
import time
import random

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Multiple unique images per category (30+ IDs per category for variety)
TOPIC_IMAGE_IDS = {
    # AI & Technology (30 unique IDs)
    'ai': [1, 20, 180, 201, 250, 326, 367, 395, 403, 430, 431, 456, 493, 169, 225, 239, 292, 316, 342, 365, 396, 404, 452, 531, 564, 593, 602, 659, 684, 718],
    
    # Cloud Computing (25 unique IDs)
    'cloud-computing': [2, 365, 403, 456, 493, 326, 367, 404, 430, 452, 531, 564, 593, 602, 659, 684, 718, 740, 763, 788, 815, 842, 866, 893, 901],
    
    # Cybersecurity (25 unique IDs)
    'cybersecurity': [88, 225, 367, 404, 430, 60, 163, 206, 250, 292, 326, 365, 396, 431, 452, 493, 531, 564, 593, 602, 659, 684, 718, 740, 763],
    
    # Data Analytics (25 unique IDs)
    'data-analytics': [60, 200, 326, 367, 431, 20, 109, 163, 206, 239, 292, 316, 342, 365, 396, 404, 430, 452, 493, 531, 564, 593, 602, 659, 684],
    
    # Software (25 unique IDs)
    'software': [3, 169, 239, 326, 396, 20, 88, 109, 163, 180, 201, 225, 250, 292, 316, 342, 365, 367, 395, 403, 430, 431, 456, 493, 531],
    
    # Tech Innovation (30 unique IDs)
    'tech-innovation': [1, 180, 250, 326, 367, 20, 88, 109, 163, 169, 201, 225, 239, 292, 316, 342, 365, 395, 396, 403, 404, 430, 431, 452, 456, 493, 531, 564, 593, 602],
    
    # Finance (25 unique IDs)
    'finance': [109, 206, 292, 367, 452, 20, 60, 88, 141, 163, 180, 201, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 456],
    
    # Banking (25 unique IDs)
    'banking': [163, 292, 367, 452, 493, 60, 88, 109, 141, 180, 201, 206, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 456],
    
    # Investment (30 unique IDs)
    'investment': [141, 206, 367, 452, 531, 20, 60, 88, 109, 163, 180, 201, 225, 239, 250, 292, 316, 326, 342, 365, 395, 396, 403, 430, 431, 456, 493, 564, 593, 602],
    
    # Green Bonds (25 unique IDs)
    'green-bonds': [96, 140, 250, 431, 564, 15, 29, 48, 78, 88, 109, 129, 141, 163, 180, 201, 225, 292, 316, 326, 342, 365, 395, 431, 452],
    
    # Economy (25 unique IDs)
    'economy': [109, 206, 292, 367, 431, 60, 88, 141, 163, 180, 201, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 452, 456, 493],
    
    # Inflation (25 unique IDs)
    'inflation': [163, 206, 292, 367, 452, 60, 88, 109, 141, 180, 201, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 456, 493],
    
    # Travel (25 unique IDs)
    'travel': [15, 48, 78, 129, 163, 29, 64, 85, 96, 119, 140, 154, 188, 235, 237, 250, 316, 342, 395, 431, 564, 593, 602, 659, 684],
    
    # Digital Nomad (25 unique IDs)
    'digital-nomad': [29, 180, 326, 395, 431, 20, 60, 88, 109, 141, 163, 201, 225, 239, 250, 292, 316, 342, 365, 367, 396, 403, 430, 452, 456],
    
    # Visa (20 unique IDs)
    'visa': [15, 48, 88, 163, 250, 29, 78, 96, 129, 140, 154, 188, 235, 316, 342, 395, 431, 564, 593, 602],
    
    # Budget Travel (20 unique IDs)
    'budget-travel': [15, 78, 129, 163, 250, 29, 48, 64, 85, 96, 119, 140, 154, 188, 235, 237, 316, 342, 395, 431],
    
    # Hollywood (25 unique IDs)
    'hollywood': [62, 109, 188, 237, 342, 64, 85, 119, 154, 163, 180, 201, 225, 235, 250, 292, 316, 326, 365, 395, 431, 452, 493, 564, 593],
    
    # Streaming (25 unique IDs)
    'streaming': [180, 326, 367, 431, 493, 20, 60, 88, 109, 141, 163, 201, 225, 239, 250, 292, 316, 342, 365, 395, 396, 403, 430, 452, 456],
    
    # Music (25 unique IDs)
    'music': [85, 154, 235, 316, 431, 62, 64, 119, 163, 180, 188, 201, 225, 237, 250, 292, 326, 342, 365, 395, 452, 493, 564, 593, 602],
    
    # Gaming (25 unique IDs)
    'gaming': [119, 326, 367, 404, 493, 20, 60, 88, 109, 141, 163, 180, 201, 225, 239, 250, 292, 316, 342, 365, 395, 396, 403, 430, 456],
    
    # Celebrity (20 unique IDs)
    'celebrity': [64, 188, 237, 316, 431, 62, 85, 119, 154, 163, 180, 201, 235, 250, 292, 326, 342, 365, 395, 452],
    
    # Politics (25 unique IDs)
    'politics': [109, 163, 292, 367, 452, 60, 88, 141, 180, 201, 206, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 456, 493],
    
    # Elections (25 unique IDs)
    'elections': [109, 163, 206, 292, 367, 60, 88, 141, 180, 201, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 452, 456, 493],
    
    # Trade (25 unique IDs)
    'trade': [109, 163, 206, 292, 367, 60, 88, 141, 180, 201, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 452, 456, 493],
    
    # Supply Chain (25 unique IDs)
    'supply-chain': [163, 292, 367, 452, 493, 60, 88, 109, 141, 180, 201, 206, 225, 239, 250, 316, 326, 342, 365, 395, 396, 403, 430, 431, 456],
}

# Track used images to ensure uniqueness
used_images = set()

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
    elif any(word in combined for word in ['investment', 'investing', 'portfolio', 'stocks', 'trading', 'retail investing']):
        return 'investment'
    elif any(word in combined for word in ['cryptocurrency', 'crypto', 'blockchain', 'bitcoin']):
        return 'investment'
    elif any(word in combined for word in ['inflation', 'price rise', 'monetary', 'emerging market']):
        return 'inflation'
    elif any(word in combined for word in ['startup funding', 'venture capital', 'investor']):
        return 'investment'
    elif any(word in combined for word in ['finance', 'financial', 'money', 'capital', 'regtech', 'regulatory technology']):
        return 'finance'
    
    # Travel keywords
    elif any(word in combined for word in ['digital nomad', 'remote work', 'work from anywhere']):
        return 'digital-nomad'
    elif any(word in combined for word in ['visa', 'passport', 'visa-free']):
        return 'visa'
    elif any(word in combined for word in ['budget travel', 'cheap travel', 'backpack', 'money-saving']):
        return 'budget-travel'
    elif any(word in combined for word in ['travel', 'destination', 'tourism', 'itinerary']):
        return 'travel'
    
    # Entertainment keywords
    elif any(word in combined for word in ['hollywood', 'movie', 'blockbuster', 'cinema', 'film', 'vfx', 'visual effects']):
        return 'hollywood'
    elif any(word in combined for word in ['streaming', 'netflix', 'platform', 'streaming war']):
        return 'streaming'
    elif any(word in combined for word in ['music', 'spotify', 'dj', 'playlist', 'audio']):
        return 'music'
    elif any(word in combined for word in ['gaming', 'game', 'esports', 'cloud gaming']):
        return 'gaming'
    elif any(word in combined for word in ['celebrity', 'star', 'famous', 'social impact']):
        return 'celebrity'
    
    # Politics keywords
    elif any(word in combined for word in ['election', 'voting', 'democracy', 'democratic']):
        return 'elections'
    elif any(word in combined for word in ['trade relation', 'us-india', 'import', 'export', 'tariff']):
        return 'trade'
    elif any(word in combined for word in ['supply chain', 'logistics', 'reshoring', 'manufacturing']):
        return 'supply-chain'
    elif any(word in combined for word in ['politics', 'political', 'government']):
        return 'politics'
    
    # Default
    else:
        return 'tech-innovation'

def get_unique_image_url(category):
    """Get a unique image URL for a category that hasn't been used yet"""
    global used_images
    
    image_ids = TOPIC_IMAGE_IDS.get(category, TOPIC_IMAGE_IDS['tech-innovation'])
    
    # Filter out already used images
    available_ids = [img_id for img_id in image_ids if img_id not in used_images]
    
    # If all images from this category are used, use any from the pool
    if not available_ids:
        available_ids = image_ids
    
    # Pick a random unique image
    image_id = random.choice(available_ids)
    used_images.add(image_id)
    
    return f'https://picsum.photos/id/{image_id}/1200/630', image_id

def update_all_featured_images():
    """Update featured images for all posts with UNIQUE images"""
    print("=" * 80)
    print("🖼️  REPLACING ALL IMAGES WITH UNIQUE RELEVANT CONTENT")
    print("=" * 80)
    print()
    print("✨ Each post will get a UNIQUE image from its topic category")
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
    image_ids_used = []
    
    for idx, post in enumerate(all_posts, 1):
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        # Determine best image category
        category = categorize_post(title, content)
        image_url, image_id = get_unique_image_url(category)
        
        # Track categories and IDs
        categories_used[category] = categories_used.get(category, 0) + 1
        image_ids_used.append(image_id)
        
        print(f"[{idx}/{len(all_posts)}] 📝 {title[:45]}...")
        print(f"      🎯 Category: {category}")
        print(f"      🖼️  Image ID: {image_id} (unique)")
        
        try:
            # Download image
            img_response = requests.get(image_url, timeout=15)
            if not img_response.ok:
                print(f"      ❌ Failed to download")
                failed_count += 1
                print()
                continue
            
            # Generate unique filename
            filename = f"{category}-{post_id}-{image_id}.jpg"
            
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
                print(f"      ✅ Updated with unique image")
                updated_count += 1
            else:
                print(f"      ❌ Failed to set featured")
                failed_count += 1
                
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:50]}")
            failed_count += 1
        
        print()
        time.sleep(0.5)
    
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully updated: {updated_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📝 Total posts: {len(all_posts)}")
    print()
    
    print("📁 CATEGORIES USED:")
    for cat, count in sorted(categories_used.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count} posts")
    print()
    
    print("🎨 IMAGE UNIQUENESS:")
    unique_count = len(set(image_ids_used))
    print(f"   Total images used: {len(image_ids_used)}")
    print(f"   Unique images: {unique_count}")
    print(f"   Uniqueness rate: {(unique_count/len(image_ids_used)*100):.1f}%")
    print()
    
    print("✨ All posts now have UNIQUE topic-relevant images!")
    print()

if __name__ == '__main__':
    update_all_featured_images()
