#!/usr/bin/env python3
"""
Broken Links Checker and Fixer
Find and fix broken internal links on the website
"""

import requests
import re
from bs4 import BeautifulSoup

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
SITE_URL = "https://spherevista360.com"

# Broken URLs reported
BROKEN_URLS = [
    "https://spherevista360.com/visa-free-destinations-2025/",
    "https://spherevista360.com/digital-banking-2025/"
]

def check_url_status(url):
    """Check if a URL returns 200 status"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code, response.headers.get('content-type', '')
    except Exception as e:
        return None, str(e)

def find_posts_with_links(broken_url):
    """Find posts that contain links to the broken URL"""
    posts_with_links = []
    
    # Get all posts
    try:
        response = requests.get(f"{WP_BASE_URL}/posts", params={'per_page': 50})
        if response.status_code == 200:
            posts = response.json()
            
            for post in posts:
                post_id = post.get('id')
                title = post.get('title', {}).get('rendered', '')
                content = post.get('content', {}).get('rendered', '')
                
                # Check if this post contains the broken link
                if broken_url in content:
                    posts_with_links.append({
                        'post_id': post_id,
                        'title': title,
                        'url': post.get('link', ''),
                        'content_snippet': content[:200] + '...'
                    })
    except Exception as e:
        print(f"Error fetching posts: {e}")
    
    return posts_with_links

def suggest_alternative_urls(broken_url):
    """Suggest possible alternative URLs for broken links"""
    # Extract the slug from the broken URL
    slug = broken_url.rstrip('/').split('/')[-1]
    
    # Search for similar posts
    try:
        # Search by slug keywords
        keywords = slug.replace('-', ' ')
        response = requests.get(f"{WP_BASE_URL}/posts", params={
            'search': keywords,
            'per_page': 10
        })
        
        if response.status_code == 200:
            posts = response.json()
            alternatives = []
            
            for post in posts:
                post_url = post.get('link', '')
                post_title = post.get('title', {}).get('rendered', '')
                alternatives.append({
                    'url': post_url,
                    'title': post_title,
                    'similarity_score': calculate_similarity(slug, post_url)
                })
            
            # Sort by similarity
            alternatives.sort(key=lambda x: x['similarity_score'], reverse=True)
            return alternatives[:5]  # Top 5 suggestions
    except Exception as e:
        print(f"Error searching for alternatives: {e}")
    
    return []

def calculate_similarity(broken_slug, post_url):
    """Calculate similarity between broken slug and post URL"""
    post_slug = post_url.rstrip('/').split('/')[-1]
    
    broken_words = set(broken_slug.split('-'))
    post_words = set(post_slug.split('-'))
    
    # Calculate Jaccard similarity
    intersection = len(broken_words.intersection(post_words))
    union = len(broken_words.union(post_words))
    
    return intersection / union if union > 0 else 0

def main():
    """Check broken links and suggest fixes"""
    print("Broken Links Checker and Fixer")
    print("=" * 50)
    print("Analyzing reported broken links...")
    print()
    
    for broken_url in BROKEN_URLS:
        print(f"Checking: {broken_url}")
        
        # Check URL status
        status, content_type = check_url_status(broken_url)
        
        if status == 200:
            print(f"  ✅ URL is actually working (status: {status})")
            continue
        elif status:
            print(f"  ❌ URL returns error status: {status}")
        else:
            print(f"  ❌ URL unreachable: {content_type}")
        
        # Find posts that link to this broken URL
        print(f"  🔍 Searching for posts that link to this URL...")
        linking_posts = find_posts_with_links(broken_url)
        
        if linking_posts:
            print(f"  📝 Found {len(linking_posts)} posts with this link:")
            for post in linking_posts:
                print(f"    - Post {post['post_id']}: {post['title']}")
                print(f"      URL: {post['url']}")
        else:
            print(f"  ℹ️ No posts found linking to this URL")
        
        # Suggest alternatives
        print(f"  💡 Suggesting alternative URLs...")
        alternatives = suggest_alternative_urls(broken_url)
        
        if alternatives:
            print(f"  📋 Top alternative suggestions:")
            for i, alt in enumerate(alternatives, 1):
                print(f"    {i}. {alt['title']}")
                print(f"       URL: {alt['url']}")
                print(f"       Similarity: {alt['similarity_score']:.2f}")
        else:
            print(f"  ⚠️ No similar posts found")
        
        print()
    
    print("=" * 50)
    print("BROKEN LINKS ANALYSIS COMPLETE")
    print("=" * 50)
    
    print("\nRecommendations:")
    print("1. Check if these URLs should exist and create the missing content")
    print("2. Update links in posts to point to correct URLs")
    print("3. Set up 301 redirects for commonly linked broken URLs")
    print("4. Run regular link checking to prevent future broken links")

if __name__ == "__main__":
    main()