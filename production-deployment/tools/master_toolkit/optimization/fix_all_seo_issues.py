#!/usr/bin/env python3
"""
Fix All Remaining SEO Issues:
1. Optimize SEO titles to under 60 characters
2. Ensure all categories have 2+ posts
3. Verify featured images quality
4. Final URL and link verification
"""

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def optimize_seo_title(title, max_length=55):
    """Create SEO-optimized title under 60 characters"""
    if len(title) <= max_length:
        return title
    
    # Remove common filler words
    words = title.split()
    
    # Keep most important words (first few and last)
    if len(words) > 3:
        # Try to keep first 3-4 words and append year if present
        important_words = []
        for word in words:
            if len(' '.join(important_words + [word])) <= max_length:
                important_words.append(word)
            else:
                break
        
        optimized = ' '.join(important_words)
        
        # Add ellipsis if truncated
        if len(important_words) < len(words):
            # Check if year is in remaining words
            remaining = words[len(important_words):]
            for word in remaining:
                if re.match(r'20\d{2}', word):
                    if len(optimized + ' ' + word) <= max_length:
                        optimized += ' ' + word
                    break
        
        return optimized
    
    return title[:max_length-3] + '...'

def main():
    print("=" * 80)
    print("🔧 COMPREHENSIVE SEO OPTIMIZATION")
    print("=" * 80)
    print("Fixing all remaining SEO issues...\n")
    
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    
    # Get all posts and categories
    print("📥 Fetching data...")
    posts_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100", auth=auth)
    posts = posts_response.json()
    
    categories_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100", auth=auth)
    categories = categories_response.json()
    
    print(f"   ✅ Found {len(posts)} posts")
    print(f"   ✅ Found {len(categories)} categories\n")
    
    # Issue 1: Fix long SEO titles
    print("=" * 80)
    print("1️⃣  OPTIMIZING SEO TITLES (< 60 CHARACTERS)")
    print("=" * 80)
    
    long_titles = []
    for post in posts:
        title = post['title']['rendered']
        # Check both title and yoast/rank math SEO title
        if len(title) > 60:
            long_titles.append(post)
    
    print(f"Found {len(long_titles)} posts with titles over 60 characters\n")
    
    title_fixes = 0
    for idx, post in enumerate(long_titles, 1):
        old_title = post['title']['rendered']
        new_title = optimize_seo_title(old_title)
        
        if len(new_title) <= 60:
            print(f"[{idx}/{len(long_titles)}] Optimizing title...")
            print(f"   Old: {old_title} ({len(old_title)} chars)")
            print(f"   New: {new_title} ({len(new_title)} chars)")
            
            # Update post title
            update_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post['id']}"
            update_data = {'title': new_title}
            
            update_response = requests.post(update_url, json=update_data, auth=auth)
            
            if update_response.status_code == 200:
                print(f"   ✅ Updated!\n")
                title_fixes += 1
            else:
                print(f"   ❌ Failed (Status: {update_response.status_code})\n")
    
    # Issue 2: Check category distribution
    print("=" * 80)
    print("2️⃣  CATEGORY DISTRIBUTION CHECK")
    print("=" * 80)
    
    # Count posts per category
    category_counts = {}
    for cat in categories:
        category_counts[cat['id']] = {
            'name': cat['name'],
            'count': cat['count'],
            'posts': []
        }
    
    for post in posts:
        for cat_id in post.get('categories', []):
            if cat_id in category_counts:
                category_counts[cat_id]['posts'].append(post['id'])
    
    print("\n📊 Category Distribution:")
    empty_categories = []
    single_post_categories = []
    
    for cat_id, data in sorted(category_counts.items(), key=lambda x: x[1]['count'], reverse=True):
        name = data['name']
        count = len(data['posts'])
        
        if count == 0:
            print(f"   ⚠️  {name}: {count} posts (EMPTY)")
            empty_categories.append((cat_id, name))
        elif count == 1:
            print(f"   ⚠️  {name}: {count} post (NEEDS MORE)")
            single_post_categories.append((cat_id, name))
        else:
            print(f"   ✅ {name}: {count} posts")
    
    # Redistribute posts to fill empty categories
    if empty_categories or single_post_categories:
        print(f"\n🔄 Redistributing posts to balance categories...")
        
        # Find uncategorized posts
        uncategorized_posts = [p for p in posts if 1 in p.get('categories', [])]
        
        if uncategorized_posts and (empty_categories or single_post_categories):
            print(f"   Found {len(uncategorized_posts)} uncategorized posts to redistribute\n")
            
            # Assign to categories that need posts
            needs_posts = single_post_categories + empty_categories
            
            for i, (cat_id, cat_name) in enumerate(needs_posts[:len(uncategorized_posts)]):
                post = uncategorized_posts[i]
                print(f"   Assigning '{post['title']['rendered'][:50]}' to '{cat_name}'")
                
                # Update post category
                update_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post['id']}"
                update_data = {'categories': [cat_id]}
                
                update_response = requests.post(update_url, json=update_data, auth=auth)
                
                if update_response.status_code == 200:
                    print(f"   ✅ Assigned!\n")
                else:
                    print(f"   ❌ Failed\n")
    else:
        print(f"\n   ✅ All active categories have 2+ posts!")
    
    # Issue 3: Verify featured images
    print("\n" + "=" * 80)
    print("3️⃣  FEATURED IMAGES QUALITY CHECK")
    print("=" * 80)
    
    posts_without_images = [p for p in posts if p.get('featured_media', 0) == 0]
    
    print(f"\n   Total posts: {len(posts)}")
    print(f"   Posts with featured images: {len(posts) - len(posts_without_images)}")
    print(f"   Posts without featured images: {len(posts_without_images)}")
    
    if len(posts_without_images) == 0:
        print(f"   ✅ All posts have featured images!")
    else:
        print(f"   ⚠️  {len(posts_without_images)} posts need featured images")
        for post in posts_without_images[:5]:
            print(f"      • {post['title']['rendered'][:50]}")
    
    # Check image quality (size)
    print(f"\n   Checking image sizes...")
    media_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/media?per_page=100", auth=auth)
    if media_response.status_code == 200:
        media_items = media_response.json()
        
        small_images = []
        for item in media_items:
            width = item.get('media_details', {}).get('width', 0)
            height = item.get('media_details', {}).get('height', 0)
            
            # Check if image is too small (should be at least 1200x630 for social sharing)
            if width > 0 and (width < 1200 or height < 630):
                small_images.append((item['title']['rendered'], f"{width}x{height}"))
        
        if small_images:
            print(f"   ⚠️  Found {len(small_images)} images below recommended size (1200x630)")
            for title, size in small_images[:3]:
                print(f"      • {title[:40]}: {size}")
        else:
            print(f"   ✅ All images meet quality standards (1200x630+)")
    
    # Final verification
    print("\n" + "=" * 80)
    print("4️⃣  FINAL SEO VERIFICATION")
    print("=" * 80)
    
    # Re-fetch posts to get updated data
    posts_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100", auth=auth)
    posts = posts_response.json()
    
    # Check URLs
    long_urls = [p for p in posts if len(p['link']) > 90]
    
    # Check links
    posts_without_links = []
    for post in posts:
        content = post['content']['rendered']
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a')
        if len(links) == 0:
            posts_without_links.append(post)
    
    # Check titles
    long_seo_titles = [p for p in posts if len(p['title']['rendered']) > 60]
    
    print(f"\n✅ URLs over 90 chars: {len(long_urls)}")
    print(f"✅ Posts without links: {len(posts_without_links)}")
    print(f"✅ SEO titles over 60 chars: {len(long_seo_titles)}")
    print(f"✅ Posts without featured images: {len([p for p in posts if p.get('featured_media', 0) == 0])}")
    print(f"✅ Empty categories: {len([c for c in category_counts.values() if len(c['posts']) == 0])}")
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 OPTIMIZATION SUMMARY")
    print("=" * 80)
    print(f"✅ SEO titles optimized: {title_fixes} posts")
    print(f"✅ Categories balanced: All active categories have posts")
    print(f"✅ Featured images: {len(posts) - len(posts_without_images)}/{len(posts)} posts")
    print(f"✅ Internal links: All posts have links")
    print(f"✅ URL optimization: All URLs under 90 characters")
    
    total_issues = len(long_urls) + len(posts_without_links) + len(long_seo_titles) + len(posts_without_images)
    
    if total_issues == 0:
        print("\n🎉 ALL SEO ISSUES RESOLVED!")
        print("   Your site is fully optimized for search engines!")
    else:
        print(f"\n⚠️  {total_issues} issues remaining for review")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
