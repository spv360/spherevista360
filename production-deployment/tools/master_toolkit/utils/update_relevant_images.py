#!/usr/bin/env python3
"""
Replace all featured images with topic-relevant images from Unsplash
Categories: Technology, Finance, AI, Travel, Entertainment, Politics
"""

import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Unsplash image topics - using specific high-quality keywords
TOPIC_IMAGES = {
    # Technology & AI
    'ai': 'https://source.unsplash.com/1200x630/?artificial-intelligence,technology',
    'cloud-computing': 'https://source.unsplash.com/1200x630/?cloud-computing,server',
    'cybersecurity': 'https://source.unsplash.com/1200x630/?cybersecurity,network',
    'data-analytics': 'https://source.unsplash.com/1200x630/?data-analytics,dashboard',
    'software': 'https://source.unsplash.com/1200x630/?software-development,coding',
    'tech-innovation': 'https://source.unsplash.com/1200x630/?technology,innovation',
    
    # Finance & Investment
    'finance': 'https://source.unsplash.com/1200x630/?finance,trading',
    'banking': 'https://source.unsplash.com/1200x630/?banking,fintech',
    'investment': 'https://source.unsplash.com/1200x630/?investment,stocks',
    'cryptocurrency': 'https://source.unsplash.com/1200x630/?cryptocurrency,blockchain',
    'economy': 'https://source.unsplash.com/1200x630/?economy,business',
    'green-bonds': 'https://source.unsplash.com/1200x630/?renewable-energy,solar',
    
    # Travel
    'travel': 'https://source.unsplash.com/1200x630/?travel,destination',
    'digital-nomad': 'https://source.unsplash.com/1200x630/?remote-work,laptop',
    'visa': 'https://source.unsplash.com/1200x630/?passport,travel',
    'budget-travel': 'https://source.unsplash.com/1200x630/?backpacking,adventure',
    
    # Entertainment
    'hollywood': 'https://source.unsplash.com/1200x630/?cinema,movie',
    'streaming': 'https://source.unsplash.com/1200x630/?streaming,entertainment',
    'music': 'https://source.unsplash.com/1200x630/?music,headphones',
    'gaming': 'https://source.unsplash.com/1200x630/?gaming,esports',
    'celebrity': 'https://source.unsplash.com/1200x630/?red-carpet,celebrity',
    
    # Politics & Global
    'politics': 'https://source.unsplash.com/1200x630/?politics,government',
    'elections': 'https://source.unsplash.com/1200x630/?voting,democracy',
    'trade': 'https://source.unsplash.com/1200x630/?global-trade,shipping',
    'inflation': 'https://source.unsplash.com/1200x630/?economy,inflation',
    'supply-chain': 'https://source.unsplash.com/1200x630/?logistics,warehouse',
}

def categorize_post(title, content):
    """Determine the best image category for a post"""
    title_lower = title.lower()
    content_lower = content.lower()
    combined = title_lower + " " + content_lower
    
    # AI & Technology keywords
    if any(word in combined for word in ['artificial intelligence', 'ai ', 'machine learning', 'neural', 'algorithm']):
        return 'ai'
    elif any(word in combined for word in ['cloud computing', 'aws', 'azure', 'google cloud']):
        return 'cloud-computing'
    elif any(word in combined for word in ['cybersecurity', 'security', 'hacking', 'privacy']):
        return 'cybersecurity'
    elif any(word in combined for word in ['analytics', 'data', 'dashboard', 'metrics']):
        return 'data-analytics'
    elif any(word in combined for word in ['software', 'coding', 'programming', 'development']):
        return 'software'
    elif any(word in combined for word in ['technology', 'tech', 'innovation', 'digital']):
        return 'tech-innovation'
    
    # Finance keywords
    elif any(word in combined for word in ['green bond', 'renewable', 'solar', 'clean energy']):
        return 'green-bonds'
    elif any(word in combined for word in ['banking', 'fintech', 'digital bank']):
        return 'banking'
    elif any(word in combined for word in ['investment', 'investing', 'portfolio', 'stocks']):
        return 'investment'
    elif any(word in combined for word in ['cryptocurrency', 'crypto', 'blockchain', 'bitcoin']):
        return 'cryptocurrency'
    elif any(word in combined for word in ['inflation', 'price', 'monetary']):
        return 'inflation'
    elif any(word in combined for word in ['finance', 'financial', 'money', 'capital']):
        return 'finance'
    
    # Travel keywords
    elif any(word in combined for word in ['digital nomad', 'remote work', 'work from anywhere']):
        return 'digital-nomad'
    elif any(word in combined for word in ['visa', 'passport']):
        return 'visa'
    elif any(word in combined for word in ['budget travel', 'cheap travel', 'backpack']):
        return 'budget-travel'
    elif any(word in combined for word in ['travel', 'destination', 'tourism']):
        return 'travel'
    
    # Entertainment keywords
    elif any(word in combined for word in ['hollywood', 'movie', 'blockbuster', 'cinema', 'film']):
        return 'hollywood'
    elif any(word in combined for word in ['streaming', 'netflix', 'spotify', 'platform']):
        return 'streaming'
    elif any(word in combined for word in ['music', 'spotify', 'dj', 'playlist']):
        return 'music'
    elif any(word in combined for word in ['gaming', 'game', 'esports']):
        return 'gaming'
    elif any(word in combined for word in ['celebrity', 'star', 'famous']):
        return 'celebrity'
    
    # Politics keywords
    elif any(word in combined for word in ['election', 'voting', 'democracy']):
        return 'elections'
    elif any(word in combined for word in ['trade', 'import', 'export', 'tariff']):
        return 'trade'
    elif any(word in combined for word in ['supply chain', 'logistics', 'reshoring']):
        return 'supply-chain'
    elif any(word in combined for word in ['politics', 'political', 'government']):
        return 'politics'
    
    # Default
    else:
        return 'tech-innovation'

def upload_image_from_url(image_url, post_title):
    """Upload image from URL to WordPress media library"""
    try:
        # Download image
        img_response = requests.get(image_url, timeout=10)
        if not img_response.ok:
            return None
        
        # Generate filename
        filename = f"{post_title[:30].replace(' ', '-').lower()}-featured.jpg"
        
        # Upload to WordPress
        files = {
            'file': (filename, img_response.content, 'image/jpeg')
        }
        
        upload_response = requests.post(
            f'{WORDPRESS_URL}/wp-json/wp/v2/media',
            auth=(USERNAME, PASSWORD),
            files=files
        )
        
        if upload_response.ok:
            return upload_response.json()['id']
        else:
            return None
            
    except Exception as e:
        print(f"      Error uploading image: {str(e)}")
        return None

def update_all_featured_images():
    """Update featured images for all posts"""
    print("=" * 80)
    print("🖼️  REPLACING ALL FEATURED IMAGES WITH RELEVANT CONTENT")
    print("=" * 80)
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
    
    for idx, post in enumerate(all_posts, 1):
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        # Determine best image category
        category = categorize_post(title, content)
        image_url = TOPIC_IMAGES[category]
        
        print(f"[{idx}/{len(all_posts)}] 📝 {title[:50]}...")
        print(f"      Category: {category}")
        
        # Upload new image
        media_id = upload_image_from_url(image_url, title)
        
        if media_id:
            # Set as featured image
            update_response = requests.post(
                f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
                json={'featured_media': media_id},
                auth=(USERNAME, PASSWORD)
            )
            
            if update_response.ok:
                print(f"      ✅ Updated with relevant {category} image")
                updated_count += 1
            else:
                print(f"      ❌ Failed to set featured image")
                failed_count += 1
        else:
            print(f"      ⚠️  Failed to upload image")
            failed_count += 1
        
        print()
        
        # Rate limiting - small delay between uploads
        time.sleep(1)
    
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully updated: {updated_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📝 Total posts: {len(all_posts)}")
    print()
    print("✨ All posts now have topic-relevant featured images!")
    print()

if __name__ == '__main__':
    update_all_featured_images()
