#!/usr/bin/env python3
"""
Remove old footer HTML from post/page content
This removes the footer that was embedded in content
"""

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def remove_footer_from_content(content):
    """Remove footer HTML from content"""
    if not content:
        return content
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove footer by id
    footer = soup.find('footer', id='sv360-bottom-footer')
    if footer:
        footer.decompose()
    
    # Remove any footer tags
    for footer in soup.find_all('footer'):
        footer.decompose()
    
    # Remove script tags related to footer
    for script in soup.find_all('script'):
        script_text = script.get_text()
        if 'footer' in script_text.lower() or 'sv360-bottom-footer' in script_text:
            script.decompose()
    
    return str(soup)

def clean_all_posts():
    """Remove footer from all posts"""
    print("=" * 80)
    print("🧹 REMOVING OLD FOOTER FROM POSTS")
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
    
    print(f"📊 Found {len(all_posts)} posts to check")
    print()
    
    cleaned_count = 0
    skipped_count = 0
    
    for post in all_posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        # Check if content has footer
        has_footer = 'sv360-bottom-footer' in content or '<footer' in content
        
        if not has_footer:
            skipped_count += 1
            continue
        
        print(f"🧹 Cleaning: {title[:60]}...")
        
        # Remove footer
        cleaned_content = remove_footer_from_content(content)
        
        # Update the post
        update_data = {
            'content': cleaned_content
        }
        
        response = requests.post(
            f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
            json=update_data,
            auth=(USERNAME, PASSWORD)
        )
        
        if response.ok:
            print(f"   ✅ Removed footer")
            cleaned_count += 1
        else:
            print(f"   ❌ Failed: {response.status_code}")
    
    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Posts cleaned: {cleaned_count}")
    print(f"⏭️  Posts skipped: {skipped_count}")
    print(f"📝 Total posts: {len(all_posts)}")
    print()

def clean_all_pages():
    """Remove footer from all pages"""
    print("=" * 80)
    print("🧹 REMOVING OLD FOOTER FROM PAGES")
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
    
    print(f"📊 Found {len(all_pages)} pages to check")
    print()
    
    cleaned_count = 0
    skipped_count = 0
    
    for pg in all_pages:
        page_id = pg['id']
        title = pg['title']['rendered']
        content = pg['content']['rendered']
        
        # Check if content has footer
        has_footer = 'sv360-bottom-footer' in content or '<footer' in content
        
        if not has_footer:
            skipped_count += 1
            continue
        
        print(f"🧹 Cleaning: {title[:60]}...")
        
        # Remove footer
        cleaned_content = remove_footer_from_content(content)
        
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
            print(f"   ✅ Removed footer")
            cleaned_count += 1
        else:
            print(f"   ❌ Failed: {response.status_code}")
    
    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Pages cleaned: {cleaned_count}")
    print(f"⏭️  Pages skipped: {skipped_count}")
    print(f"📝 Total pages: {len(all_pages)}")
    print()

if __name__ == '__main__':
    clean_all_posts()
    print()
    clean_all_pages()
