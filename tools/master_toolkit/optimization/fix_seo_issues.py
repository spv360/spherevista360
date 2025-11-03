#!/usr/bin/env python3
"""
Fix SEO Issues:
1. Shorten post URLs to under 90 characters
2. Add internal links to posts
"""

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import time

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def shorten_slug(title, max_length=60):
    """Create a short, SEO-friendly slug from title"""
    # Remove special characters and convert to lowercase
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Split into words and keep most important ones
    words = slug.split('-')
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'how', 'what', 'why'}
    important_words = [w for w in words if w not in stop_words]
    
    # If we removed too many words, add some back
    if len(important_words) < 3:
        important_words = words[:5]
    
    # Build slug up to max length
    slug = ''
    for word in important_words:
        if len(slug + word) + 1 <= max_length:
            slug += word + '-'
        else:
            break
    
    return slug.rstrip('-')

def add_internal_links(content, post_title, all_posts, category_id):
    """Add relevant internal links to post content"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get related posts from same category
    related_posts = [p for p in all_posts if category_id in p.get('categories', []) and p['title']['rendered'] != post_title]
    
    # Get the first paragraph
    paragraphs = soup.find_all('p')
    if len(paragraphs) < 2:
        return content
    
    # Add related posts section at the end
    if related_posts[:3]:  # Add up to 3 related links
        related_section = soup.new_tag('div', **{'class': 'related-posts'})
        related_heading = soup.new_tag('h3')
        related_heading.string = 'Related Articles'
        related_section.append(related_heading)
        
        related_list = soup.new_tag('ul')
        for related in related_posts[:3]:
            li = soup.new_tag('li')
            link = soup.new_tag('a', href=related['link'])
            link.string = related['title']['rendered']
            li.append(link)
            related_list.append(li)
        
        related_section.append(related_list)
        
        # Add before the last paragraph
        if paragraphs:
            paragraphs[-1].insert_before(related_section)
    
    # Add contextual links in content
    link_keywords = {
        'Technology': ['AI', 'cloud computing', 'technology', 'innovation', 'digital transformation'],
        'Finance': ['investment', 'banking', 'finance', 'market', 'trading'],
        'Entertainment': ['streaming', 'movies', 'music', 'entertainment', 'Hollywood'],
        'Travel': ['travel', 'destinations', 'tourism', 'vacation', 'trip'],
        'Politics': ['election', 'policy', 'government', 'politics', 'democracy'],
        'Business': ['business', 'startup', 'entrepreneur', 'strategy', 'growth'],
        'World News': ['global', 'international', 'world', 'news', 'economy']
    }
    
    # Add 1-2 contextual links in first few paragraphs
    links_added = 0
    for p in paragraphs[:3]:
        if links_added >= 2:
            break
            
        text = p.get_text().lower()
        for related in related_posts[:5]:
            if links_added >= 2:
                break
                
            related_title = related['title']['rendered']
            # Check if any keywords from related post appear in this paragraph
            title_words = related_title.lower().split()[:3]
            
            for word in title_words:
                if len(word) > 4 and word in text:
                    # Find the word in the paragraph and make it a link
                    p_text = str(p)
                    # Only link if not already linked
                    if f'>{word}<' in p_text.lower() and '<a' not in p_text:
                        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                        replacement = f'<a href="{related["link"]}">{word}</a>'
                        new_p_text = pattern.sub(replacement, p_text, count=1)
                        if new_p_text != p_text:
                            new_p = BeautifulSoup(new_p_text, 'html.parser').find('p')
                            if new_p:
                                p.replace_with(new_p)
                                links_added += 1
                                break
    
    return str(soup)

def main():
    print("=" * 70)
    print("🔧 FIXING SEO ISSUES")
    print("=" * 70)
    print("1. Optimizing URL lengths (< 90 characters)")
    print("2. Adding internal links to posts\n")
    
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    
    # Get all posts
    print("📥 Fetching all posts...")
    response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100", auth=auth)
    
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = response.json()
    print(f"   Found {len(posts)} posts\n")
    
    # Get categories for context
    cat_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100", auth=auth)
    categories = {c['id']: c['name'] for c in cat_response.json()}
    
    # First pass: Fix long URLs
    print("=" * 70)
    print("PHASE 1: OPTIMIZING POST URLS")
    print("=" * 70)
    
    long_url_posts = []
    for post in posts:
        url = post['link']
        slug = post['slug']
        url_length = len(url)
        
        if url_length > 90 or len(slug) > 60:
            long_url_posts.append(post)
    
    print(f"Found {len(long_url_posts)} posts with long URLs\n")
    
    url_fixes = 0
    for idx, post in enumerate(long_url_posts, 1):
        title = post['title']['rendered']
        old_slug = post['slug']
        new_slug = shorten_slug(title)
        
        print(f"[{idx}/{len(long_url_posts)}] Optimizing URL...")
        print(f"   Title: {title[:60]}")
        print(f"   Old slug: {old_slug[:50]} ({len(old_slug)} chars)")
        print(f"   New slug: {new_slug} ({len(new_slug)} chars)")
        
        # Update post slug
        update_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post['id']}"
        update_data = {'slug': new_slug}
        
        update_response = requests.post(update_url, json=update_data, auth=auth)
        
        if update_response.status_code == 200:
            new_url = update_response.json()['link']
            print(f"   ✅ Updated! New URL: {new_url}")
            print(f"   URL length: {len(new_url)} chars\n")
            url_fixes += 1
            post['slug'] = new_slug  # Update for next phase
            post['link'] = new_url
        else:
            print(f"   ❌ Failed (Status: {update_response.status_code})\n")
        
        time.sleep(0.5)  # Rate limiting
    
    # Refresh posts list with new URLs
    print("\n📥 Refreshing posts list...")
    response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100", auth=auth)
    posts = response.json()
    
    # Second pass: Add internal links
    print("\n" + "=" * 70)
    print("PHASE 2: ADDING INTERNAL LINKS")
    print("=" * 70)
    print()
    
    link_fixes = 0
    for idx, post in enumerate(posts, 1):
        title = post['title']['rendered']
        content = post['content']['rendered']
        category_id = post['categories'][0] if post['categories'] else None
        
        # Check if post already has links
        soup = BeautifulSoup(content, 'html.parser')
        existing_links = soup.find_all('a')
        
        if len(existing_links) >= 3:
            continue  # Already has enough links
        
        print(f"[{idx}/{len(posts)}] Adding links to: {title[:50]}...")
        
        # Add internal links
        updated_content = add_internal_links(content, title, posts, category_id)
        
        # Count new links
        new_soup = BeautifulSoup(updated_content, 'html.parser')
        new_links = new_soup.find_all('a')
        
        if len(new_links) > len(existing_links):
            print(f"   Links: {len(existing_links)} → {len(new_links)}")
            
            # Update post
            update_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post['id']}"
            update_data = {'content': updated_content}
            
            update_response = requests.post(update_url, json=update_data, auth=auth)
            
            if update_response.status_code == 200:
                print(f"   ✅ Updated!\n")
                link_fixes += 1
            else:
                print(f"   ❌ Failed (Status: {update_response.status_code})\n")
            
            time.sleep(0.5)  # Rate limiting
        else:
            print(f"   ⏭️  No suitable links found\n")
    
    # Final summary
    print("=" * 70)
    print("📊 SEO FIXES COMPLETE")
    print("=" * 70)
    print(f"✅ URL optimizations: {url_fixes} posts")
    print(f"✅ Internal links added: {link_fixes} posts")
    print(f"🎯 Total improvements: {url_fixes + link_fixes}")
    print("=" * 70)

if __name__ == "__main__":
    main()
