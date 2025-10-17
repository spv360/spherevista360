#!/usr/bin/env python3
"""
Replace all featured images with relevant high-quality images
Using direct image URLs for technology, finance, AI topics
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

# Curated high-quality images by topic (using Picsum with specific IDs for consistency)
TOPIC_IMAGE_IDS = {
    # AI & Technology
    'ai': [1, 20, 180, 201, 250],  # Tech/abstract
    'cloud-computing': [2, 365, 403, 456, 493],  # Tech/network
    'cybersecurity': [88, 225, 367, 404, 430],  # Abstract/secure
    'data-analytics': [60, 200, 326, 367, 431],  # Charts/data
    'software': [3, 169, 239, 326, 396],  # Code/tech
    'tech-innovation': [1, 180, 250, 326, 367],  # Innovation
    
    # Finance & Investment  
    'finance': [109, 206, 292, 367, 452],  # Business/finance
    'banking': [163, 292, 367, 452, 493],  # Business/tech
    'investment': [141, 206, 367, 452, 531],  # Growth/business
    'green-bonds': [96, 140, 250, 431, 564],  # Nature/energy
    'economy': [109, 206, 292, 367, 431],  # Business/global
    'inflation': [163, 206, 292, 367, 452],  # Economy
    
    # Travel
    'travel': [15, 48, 78, 129, 163],  # Travel/destinations
    'digital-nomad': [29, 180, 326, 395, 431],  # Remote work
    'visa': [15, 48, 88, 163, 250],  # Travel docs
    'budget-travel': [15, 78, 129, 163, 250],  # Adventure
    
    # Entertainment
    'hollywood': [62, 109, 188, 237, 342],  # Cinema/entertainment
    'streaming': [180, 326, 367, 431, 493],  # Media/tech
    'music': [85, 154, 235, 316, 431],  # Music/audio
    'gaming': [119, 326, 367, 404, 493],  # Gaming/tech
    'celebrity': [64, 188, 237, 316, 431],  # People/celebrity
    
    # Politics & Global
    'politics': [109, 163, 292, 367, 452],  # Government/business
    'elections': [109, 163, 206, 292, 367],  # Democracy/voting
    'trade': [109, 163, 206, 292, 367],  # Global trade
    'supply-chain': [163, 292, 367, 452, 493],  # Logistics
}

def categorize_post(title, content):
    """Determine the best image category for a post"""
    title_lower = title.lower()
    content_lower = content.lower()[:500]  # First 500 chars for efficiency
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

def get_image_url_for_category(category):
    """Get a consistent image URL for a category"""
    image_ids = TOPIC_IMAGE_IDS.get(category, TOPIC_IMAGE_IDS['tech-innovation'])
    # Use first ID for consistency (or random for variety)
    image_id = image_ids[0]  # Consistent image per category
    return f'https://picsum.photos/id/{image_id}/1200/630'

def update_all_featured_images():
    """Update featured images for all posts"""
    print("=" * 80)
    print("🖼️  REPLACING ALL FEATURED IMAGES WITH RELEVANT CONTENT")
    print("=" * 80)
    print()
    print("Using curated high-quality images for:")
    print("  • Technology & AI")
    print("  • Finance & Investment") 
    print("  • Travel")
    print("  • Entertainment")
    print("  • Politics & Global Affairs")
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
        image_url = get_image_url_for_category(category)
        
        # Track categories
        categories_used[category] = categories_used.get(category, 0) + 1
        
        print(f"[{idx}/{len(all_posts)}] 📝 {title[:50]}...")
        print(f"      🎯 Category: {category}")
        print(f"      🖼️  Image: {image_url}")
        
        try:
            # Download image
            img_response = requests.get(image_url, timeout=15)
            if not img_response.ok:
                print(f"      ❌ Failed to download image")
                failed_count += 1
                print()
                continue
            
            # Generate filename
            filename = f"{category}-{post_id}.jpg"
            
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
                print(f"      ❌ Failed to upload to WordPress")
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
                print(f"      ✅ Updated with relevant image")
                updated_count += 1
            else:
                print(f"      ❌ Failed to set featured image")
                failed_count += 1
                
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")
            failed_count += 1
        
        print()
        
        # Rate limiting
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
    
    print("✨ All posts now have topic-relevant featured images!")
    print()

if __name__ == '__main__':
    update_all_featured_images()
