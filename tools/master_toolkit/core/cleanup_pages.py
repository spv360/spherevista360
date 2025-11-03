#!/usr/bin/env python3
"""
Clean up pages - remove all images (keep only featured images)
"""

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def remove_images_from_content(content):
    """Remove all images from content"""
    if not content:
        return content
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove all img tags
    for img in soup.find_all('img'):
        img.decompose()
    
    # Remove all figure tags
    for figure in soup.find_all('figure'):
        figure.decompose()
    
    # Remove all picture tags
    for picture in soup.find_all('picture'):
        picture.decompose()
    
    # Remove WordPress image blocks
    content_str = str(soup)
    content_str = re.sub(r'<!-- wp:image.*?<!-- /wp:image -->', '', content_str, flags=re.DOTALL)
    
    return content_str.strip()

def cleanup_all_pages():
    """Remove images from all page content"""
    print("=" * 80)
    print("🧹 CLEANING UP PAGES")
    print("=" * 80)
    print()
    
    # Get all pages
    page = 1
    all_pages = []
    
    while True:
        response = requests.get(
            f'{WORDPRESS_URL}/wp-json/wp/v2/pages',
            params={'per_page': 100, 'page': page},
            auth=(USERNAME, PASSWORD)
        )
        
        if not response.ok:
            break
        
        pages = response.json()
        if not pages:
            break
        
        all_pages.extend(pages)
        page += 1
    
    print(f"📊 Found {len(all_pages)} pages to clean")
    print()
    
    cleaned_count = 0
    skipped_count = 0
    
    for pg in all_pages:
        page_id = pg['id']
        title = pg['title']['rendered']
        content = pg['content']['rendered']
        
        # Check if content has images
        has_images = '<img' in content or '<figure' in content or 'wp:image' in content
        
        if not has_images:
            print(f"⏭️  Skipping: {title[:50]}... (no images in content)")
            skipped_count += 1
            continue
        
        # Remove images from content
        cleaned_content = remove_images_from_content(content)
        
        # Update the page
        update_data = {
            'content': cleaned_content
        }
        
        response = requests.post(
            f'{WORDPRESS_URL}/wp-json/wp/v2/pages/{page_id}',
            json=update_data,
            auth=(USERNAME, PASSWORD)
        )
        
        if response.ok:
            print(f"✅ Cleaned: {title[:60]}...")
            cleaned_count += 1
        else:
            print(f"❌ Failed: {title[:60]}... - {response.status_code}")
    
    print()
    print("=" * 80)
    print("📊 CLEANUP SUMMARY")
    print("=" * 80)
    print(f"✅ Pages cleaned: {cleaned_count}")
    print(f"⏭️  Pages skipped: {skipped_count}")
    print(f"📝 Total pages: {len(all_pages)}")
    print()
    print("✨ All pages now have ONLY featured images (no inline images)")
    print()

if __name__ == '__main__':
    cleanup_all_pages()
