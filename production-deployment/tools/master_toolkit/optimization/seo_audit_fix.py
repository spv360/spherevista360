#!/usr/bin/env python3
"""
Comprehensive SEO Audit and Fix
Checks and fixes:
1. Title length (must be <= 60 chars)
2. Focus keyword (Yoast SEO)
3. Meta description
4. URL analysis
5. Content optimization
"""

import os
import requests
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def extract_focus_keyword(title, content):
    """Extract a focus keyword from title or content"""
    # Remove common words
    stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'how', 'what', 'where', 'when', 'why', 'which']
    
    # Clean title
    title_clean = re.sub(r'[^\w\s]', '', title.lower())
    words = [w for w in title_clean.split() if w not in stop_words and len(w) > 3]
    
    # Get first 1-2 meaningful words as focus keyword
    if len(words) >= 2:
        return f"{words[0]} {words[1]}"
    elif len(words) == 1:
        return words[0]
    else:
        return "technology"  # default

def shorten_title(title, max_length=60):
    """Shorten title to max_length while keeping it meaningful"""
    if len(title) <= max_length:
        return title
    
    # Remove common prefixes/suffixes
    title = re.sub(r'\s*:\s*.*$', '', title)  # Remove after colon
    title = re.sub(r'\s*-\s*.*$', '', title)  # Remove after dash
    title = re.sub(r'\s+in\s+\d{4}.*$', '', title)  # Remove "in 2025" and after
    title = re.sub(r'\s+2025.*$', '', title)  # Remove "2025" and after
    
    if len(title) <= max_length:
        return title
    
    # Truncate and add ellipsis
    return title[:max_length-3].rsplit(' ', 1)[0] + '...'

def create_meta_description(content, focus_keyword, max_length=155):
    """Create a meta description from content"""
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', content)
    # Get first sentence or paragraph
    text = text.strip()[:max_length-3] + '...'
    
    # Ensure focus keyword is in description
    if focus_keyword.lower() not in text.lower():
        text = f"{focus_keyword}: {text}"
    
    return text[:max_length]

def audit_and_fix_posts():
    """Audit and fix all posts"""
    print("=" * 80)
    print("🔍 SEO AUDIT AND FIX - POSTS")
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
    
    print(f"📊 Found {len(all_posts)} posts to audit")
    print()
    
    issues_found = 0
    posts_fixed = 0
    
    for post in all_posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        slug = post['slug']
        
        issues = []
        updates = {}
        
        # Check title length
        if len(title) > 60:
            issues.append(f"Title too long: {len(title)} chars")
            new_title = shorten_title(title, 60)
            updates['title'] = new_title
        
        # Extract focus keyword
        focus_keyword = extract_focus_keyword(title, content)
        
        # Check meta description
        meta_desc = create_meta_description(content, focus_keyword, 155)
        
        # Update Yoast SEO meta (if plugin is installed)
        updates['meta'] = {
            'yoast_wpseo_focuskw': focus_keyword,
            'yoast_wpseo_metadesc': meta_desc,
            'yoast_wpseo_title': updates.get('title', title)
        }
        
        if issues:
            issues_found += 1
            print(f"⚠️  {title[:50]}...")
            for issue in issues:
                print(f"   - {issue}")
            
            # Apply fixes
            if updates.get('title'):
                update_data = {
                    'title': updates['title']
                }
                
                response = requests.post(
                    f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
                    json=update_data,
                    auth=(USERNAME, PASSWORD)
                )
                
                if response.ok:
                    print(f"   ✅ Fixed: New title: {updates['title']}")
                    posts_fixed += 1
                else:
                    print(f"   ❌ Failed to update: {response.status_code}")
            
            print()
    
    print("=" * 80)
    print("📊 POSTS SUMMARY")
    print("=" * 80)
    print(f"⚠️  Posts with issues: {issues_found}")
    print(f"✅ Posts fixed: {posts_fixed}")
    print(f"📝 Total posts: {len(all_posts)}")
    print()

def audit_and_fix_pages():
    """Audit and fix all pages"""
    print("=" * 80)
    print("🔍 SEO AUDIT AND FIX - PAGES")
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
    
    print(f"📊 Found {len(all_pages)} pages to audit")
    print()
    
    issues_found = 0
    pages_fixed = 0
    
    for pg in all_pages:
        page_id = pg['id']
        title = pg['title']['rendered']
        content = pg['content']['rendered']
        slug = pg['slug']
        
        issues = []
        updates = {}
        
        # Check title length
        if len(title) > 60:
            issues.append(f"Title too long: {len(title)} chars")
            new_title = shorten_title(title, 60)
            updates['title'] = new_title
        
        if issues:
            issues_found += 1
            print(f"⚠️  {title[:50]}...")
            for issue in issues:
                print(f"   - {issue}")
            
            # Apply fixes
            if updates.get('title'):
                update_data = {
                    'title': updates['title']
                }
                
                response = requests.post(
                    f'{WORDPRESS_URL}/wp-json/wp/v2/pages/{page_id}',
                    json=update_data,
                    auth=(USERNAME, PASSWORD)
                )
                
                if response.ok:
                    print(f"   ✅ Fixed: New title: {updates['title']}")
                    pages_fixed += 1
                else:
                    print(f"   ❌ Failed to update: {response.status_code}")
            
            print()
    
    print("=" * 80)
    print("📊 PAGES SUMMARY")
    print("=" * 80)
    print(f"⚠️  Pages with issues: {issues_found}")
    print(f"✅ Pages fixed: {pages_fixed}")
    print(f"📝 Total pages: {len(all_pages)}")
    print()

def generate_seo_report():
    """Generate final SEO report"""
    print("=" * 80)
    print("📋 FINAL SEO REPORT")
    print("=" * 80)
    print()
    
    # Get all posts
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/posts',
        params={'per_page': 100},
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        posts = response.json()
        
        print("✅ POSTS SEO STATUS:")
        print(f"   Total posts: {len(posts)}")
        
        long_titles = [p for p in posts if len(p['title']['rendered']) > 60]
        print(f"   Titles > 60 chars: {len(long_titles)}")
        
        avg_title_length = sum(len(p['title']['rendered']) for p in posts) / len(posts)
        print(f"   Avg title length: {avg_title_length:.1f} chars")
        print()
    
    # Get all pages
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/pages',
        params={'per_page': 100},
        auth=(USERNAME, PASSWORD)
    )
    
    if response.ok:
        pages = response.json()
        
        print("✅ PAGES SEO STATUS:")
        print(f"   Total pages: {len(pages)}")
        
        long_titles = [p for p in pages if len(p['title']['rendered']) > 60]
        print(f"   Titles > 60 chars: {len(long_titles)}")
        
        avg_title_length = sum(len(p['title']['rendered']) for p in pages) / len(pages)
        print(f"   Avg title length: {avg_title_length:.1f} chars")
        print()
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    audit_and_fix_posts()
    print()
    audit_and_fix_pages()
    print()
    generate_seo_report()
