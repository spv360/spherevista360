#!/usr/bin/env python3
"""
URL Slug Optimizer
Optimize long URLs that exceed SEO recommendations
"""

import requests
import json
import getpass
import re

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def authenticate():
    """Get WordPress credentials"""
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    return username, app_password

def analyze_url_length(post_id):
    """Analyze URL length for a specific post"""
    try:
        response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
        if response.status_code == 200:
            data = response.json()
            title = data['title']['rendered']
            url = data['link']
            slug = data['slug']
            
            return {
                'post_id': post_id,
                'title': title,
                'url': url,
                'slug': slug,
                'url_length': len(url),
                'slug_length': len(slug),
                'exceeds_limit': len(url) > 90
            }
    except Exception as e:
        return {'error': f'Error fetching post {post_id}: {e}'}
    
    return None

def suggest_optimized_slug(title, current_slug):
    """Suggest an optimized slug for better SEO"""
    # Base domain length
    base_url = "https://spherevista360.com/"
    base_length = len(base_url)
    
    # Target: keep total URL under 85 characters (5 char buffer)
    target_slug_length = 85 - base_length
    
    # If current slug is already good, return it
    if len(current_slug) <= target_slug_length:
        return current_slug
    
    # Create optimized suggestions
    suggestions = []
    
    # Method 1: Remove common words and keep key terms
    words = current_slug.split('-')
    
    # Words to prioritize (keep these)
    priority_words = ['ai', 'streaming', 'recommenders', 'experience', 'personal', 'shape']
    
    # Words to remove if needed
    stop_words = ['how', 'what', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'gets', 'your', 'you']
    
    # Build optimized slug
    essential_words = []
    optional_words = []
    
    for word in words:
        if word.lower() in priority_words:
            essential_words.append(word)
        elif word.lower() not in stop_words:
            optional_words.append(word)
    
    # Start with essential words
    optimized_slug = '-'.join(essential_words)
    
    # Add optional words if space allows
    for word in optional_words:
        test_slug = optimized_slug + '-' + word if optimized_slug else word
        if len(test_slug) <= target_slug_length:
            optimized_slug = test_slug
        else:
            break
    
    suggestions.append({
        'slug': optimized_slug,
        'length': len(optimized_slug),
        'total_url_length': base_length + len(optimized_slug),
        'method': 'Remove stop words, keep key terms'
    })
    
    # Method 2: Shorten based on title keywords
    title_words = re.findall(r'\b\w+\b', title.lower())
    key_title_words = [w for w in title_words if w not in stop_words and len(w) > 2][:5]
    
    title_based_slug = '-'.join(key_title_words[:4])  # Limit to 4 key words
    suggestions.append({
        'slug': title_based_slug,
        'length': len(title_based_slug),
        'total_url_length': base_length + len(title_based_slug),
        'method': 'Based on title keywords'
    })
    
    # Method 3: Ultra-short version
    ultra_short = 'ai-streaming-recommenders'
    suggestions.append({
        'slug': ultra_short,
        'length': len(ultra_short),
        'total_url_length': base_length + len(ultra_short),
        'method': 'Ultra-short core terms'
    })
    
    # Return the best suggestion (shortest that makes sense)
    valid_suggestions = [s for s in suggestions if s['total_url_length'] <= 85]
    
    if valid_suggestions:
        return valid_suggestions[0]['slug']
    else:
        return suggestions[-1]['slug']  # Return ultra-short as fallback

def update_post_slug(post_id, new_slug, auth):
    """Update post slug via WordPress API"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'slug': new_slug}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, auth=auth, headers=headers)
    
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.text

def main():
    """Optimize URL slugs that exceed SEO recommendations"""
    print("URL Slug Optimizer")
    print("=" * 40)
    print("Optimizing URLs that exceed 90 characters...")
    print()
    
    # Check post 1833 specifically
    post_id = 1833
    
    print(f"Analyzing Post {post_id}...")
    analysis = analyze_url_length(post_id)
    
    if not analysis or 'error' in analysis:
        print(f"❌ Could not analyze post {post_id}")
        return
    
    print(f"Current URL: {analysis['url']}")
    print(f"Current Length: {analysis['url_length']} characters")
    print(f"Current Slug: {analysis['slug']}")
    print(f"Status: {'❌ EXCEEDS 90 CHARS' if analysis['exceeds_limit'] else '✅ OK'}")
    print()
    
    if not analysis['exceeds_limit']:
        print("✅ URL length is already optimal!")
        return
    
    # Suggest optimized slug
    optimized_slug = suggest_optimized_slug(analysis['title'], analysis['slug'])
    base_url = "https://spherevista360.com/"
    new_url = base_url + optimized_slug + "/"
    new_length = len(new_url)
    
    print("OPTIMIZATION SUGGESTION:")
    print("-" * 25)
    print(f"Current: {analysis['url']} ({analysis['url_length']} chars)")
    print(f"Optimized: {new_url} ({new_length} chars)")
    print(f"Savings: {analysis['url_length'] - new_length} characters")
    print()
    
    if new_length <= 90:
        print("✅ Optimized URL meets SEO recommendations!")
    else:
        print("⚠️ Optimized URL still exceeds 90 chars, but is improved")
    
    # Confirm with user
    proceed = input(f"\nUpdate post {post_id} slug to '{optimized_slug}'? (y/N): ").lower().strip()
    if proceed != 'y':
        print("Update cancelled.")
        return
    
    # Get authentication and update
    auth = authenticate()
    
    print(f"\nUpdating post {post_id} slug...")
    success, result = update_post_slug(post_id, optimized_slug, auth)
    
    if success:
        print("✅ Successfully updated post slug!")
        print(f"New URL: {result.get('link', 'Unknown')}")
        print()
        print("⚠️ IMPORTANT NOTE:")
        print("The old URL will return 404 until you set up a 301 redirect.")
        print("Consider adding this redirect in WordPress admin:")
        print(f"  {analysis['slug']} → {optimized_slug}")
    else:
        print(f"❌ Failed to update slug: {result}")

if __name__ == "__main__":
    main()