#!/usr/bin/env python3
"""
Publish content from published_content folder to WordPress
"""

import os
import requests
import frontmatter
from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Category mapping
CATEGORY_MAP = {
    'Finance': 'Finance',
    'Technology': 'Technology',
    'Business': 'Business',
    'Entertainment': 'Entertainment',
    'Travel': 'Travel',
    'Politics': 'Politics',
    'World': 'World News'
}

def get_or_create_category(category_name):
    """Get or create a category"""
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories"
    
    # Check if category exists
    response = requests.get(
        f"{url}?search={category_name}",
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    
    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    
    # Create category
    response = requests.post(
        url,
        json={'name': category_name},
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    
    if response.status_code == 201:
        return response.json()['id']
    
    return None

def publish_post(title, content, category_id, excerpt=""):
    """Publish a post to WordPress"""
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
    
    # Check if post already exists
    check_url = f"{url}?search={title[:50]}"
    response = requests.get(check_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    if response.status_code == 200:
        existing = response.json()
        for post in existing:
            if post['title']['rendered'] == title:
                print(f"   ⏭️  Already exists: {title}")
                return post['id']
    
    # Create new post
    data = {
        'title': title,
        'content': content,
        'status': 'publish',
        'categories': [category_id] if category_id else [],
        'excerpt': excerpt[:150] if excerpt else content[:150]
    }
    
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    
    if response.status_code == 201:
        post_id = response.json()['id']
        print(f"   ✅ Published: {title} (ID: {post_id})")
        return post_id
    else:
        print(f"   ❌ Failed: {title} - {response.status_code}")
        return None

def process_markdown_file(file_path, category):
    """Process a markdown file and extract content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
        title = post.get('title', Path(file_path).stem.replace('-', ' ').title())
        content = post.content
        excerpt = post.get('excerpt', '') or post.get('description', '')
        
        return title, content, excerpt
    except Exception as e:
        print(f"   ⚠️  Error reading {file_path}: {e}")
        return None, None, None

def main():
    print("=" * 60)
    print("📚 Publishing Content from published_content folder")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    content_dir = Path('/home/kddevops/projects/spherevista360/published_content')
    
    if not content_dir.exists():
        print("❌ published_content folder not found!")
        return
    
    total_published = 0
    total_skipped = 0
    
    # Process each category folder
    for category_folder in sorted(content_dir.iterdir()):
        if not category_folder.is_dir():
            continue
        
        category_name = CATEGORY_MAP.get(category_folder.name, category_folder.name)
        
        print(f"\n📁 Processing: {category_name}")
        print("-" * 60)
        
        # Get or create category
        category_id = get_or_create_category(category_name)
        if category_id:
            print(f"   📂 Category ID: {category_id}")
        
        # Process all markdown files in this category
        md_files = sorted(category_folder.glob('*.md'))
        
        for md_file in md_files:
            title, content, excerpt = process_markdown_file(md_file, category_name)
            
            if title and content:
                result = publish_post(title, content, category_id, excerpt)
                if result:
                    if result == "skipped":
                        total_skipped += 1
                    else:
                        total_published += 1
    
    print("\n" + "=" * 60)
    print("✅ PUBLISHING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   ✅ Published: {total_published} posts")
    print(f"   ⏭️  Skipped: {total_skipped} (already exist)")
    
    print(f"\n🌐 Visit your site: {WORDPRESS_URL}")
    print(f"📰 View posts: {WORDPRESS_URL}/blog/")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
