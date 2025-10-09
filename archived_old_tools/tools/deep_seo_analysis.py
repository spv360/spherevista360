#!/usr/bin/env python3
"""
Deep SEO Title Analysis
Check post titles, meta titles, and SEO plugin data for length issues
"""

import requests
import json
from bs4 import BeautifulSoup

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def get_post_seo_data(post_id):
    """Get comprehensive SEO data for a post"""
    # Get WordPress REST API data
    try:
        api_response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
        if api_response.status_code == 200:
            api_data = api_response.json()
        else:
            api_data = None
    except:
        api_data = None
    
    # Get actual page content to check meta tags
    page_content = None
    page_url = None
    if api_data:
        page_url = api_data.get('link', '')
        try:
            page_response = requests.get(page_url)
            if page_response.status_code == 200:
                page_content = page_response.text
        except:
            page_content = None
    
    return api_data, page_content, page_url

def analyze_page_seo_titles(html_content):
    """Extract all title-related meta tags from page HTML"""
    if not html_content:
        return {}
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    title_data = {}
    
    # Page title
    title_tag = soup.find('title')
    if title_tag:
        title_data['page_title'] = title_tag.get_text().strip()
        title_data['page_title_length'] = len(title_data['page_title'])
    
    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        title_data['meta_description'] = meta_desc.get('content', '').strip()
        title_data['meta_description_length'] = len(title_data['meta_description'])
    
    # Open Graph title
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        title_data['og_title'] = og_title.get('content', '').strip()
        title_data['og_title_length'] = len(title_data['og_title'])
    
    # Twitter title
    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if twitter_title:
        title_data['twitter_title'] = twitter_title.get('content', '').strip()
        title_data['twitter_title_length'] = len(title_data['twitter_title'])
    
    # Yoast SEO specific meta tags
    yoast_title = soup.find('meta', attrs={'name': 'title'})
    if yoast_title:
        title_data['yoast_title'] = yoast_title.get('content', '').strip()
        title_data['yoast_title_length'] = len(title_data['yoast_title'])
    
    # RankMath SEO specific
    rankmath_title = soup.find('meta', attrs={'name': 'robots'})
    # Look for any other SEO plugin specific meta tags
    
    return title_data

def main():
    """Check recent posts for all types of SEO title issues"""
    print("Deep SEO Title Analysis")
    print("=" * 50)
    print("Checking all title fields for SEO compliance...")
    print()
    
    # Recent posts that we know about
    recent_posts = [1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838]
    
    issues_found = []
    
    for post_id in recent_posts:
        print(f"Analyzing Post {post_id}...")
        
        # Get all SEO data
        api_data, page_content, page_url = get_post_seo_data(post_id)
        
        if not api_data:
            print(f"  ❌ Could not fetch API data for post {post_id}")
            continue
        
        # WordPress post title
        wp_title = api_data.get('title', {}).get('rendered', '')
        wp_title_length = len(wp_title)
        
        print(f"  WordPress Title: {wp_title} ({wp_title_length} chars)")
        
        # Analyze page HTML for meta titles
        if page_content:
            seo_data = analyze_page_seo_titles(page_content)
            
            # Check all title fields
            for field_name, field_value in seo_data.items():
                if field_name.endswith('_length'):
                    continue
                    
                field_length = seo_data.get(f"{field_name}_length", 0)
                if field_length > 60:
                    print(f"  ❌ {field_name}: {field_value} ({field_length} chars) - EXCEEDS LIMIT")
                    issues_found.append({
                        'post_id': post_id,
                        'field': field_name,
                        'value': field_value,
                        'length': field_length,
                        'url': page_url
                    })
                else:
                    print(f"  ✅ {field_name}: {field_value[:50]}... ({field_length} chars)")
        else:
            print(f"  ⚠️ Could not fetch page content for analysis")
        
        print()
    
    # Summary
    print("=" * 50)
    print("DEEP SEO ANALYSIS SUMMARY")
    print("=" * 50)
    
    if issues_found:
        print(f"🚨 Found {len(issues_found)} SEO title issues:")
        print()
        
        for issue in issues_found:
            print(f"Post {issue['post_id']} - {issue['field']}:")
            print(f"  Current: {issue['value']} ({issue['length']} chars)")
            print(f"  URL: {issue['url']}")
            print()
        
        print("These issues might be causing the SEO warnings you're seeing.")
        print("They could be from:")
        print("- SEO plugin meta titles")
        print("- Open Graph titles")
        print("- Twitter card titles")
        print("- Page title tags")
        
    else:
        print("✅ No SEO title issues found in any field!")
        print()
        print("If you're still seeing SEO warnings, they might be from:")
        print("1. Cached data in your SEO plugin")
        print("2. Different posts not in our recent batch")
        print("3. Plugin-specific optimization suggestions")
        print("4. Meta descriptions (not titles)")
    
    print(f"\nTotal posts analyzed: {len(recent_posts)}")
    print(f"Posts with title field issues: {len(set(issue['post_id'] for issue in issues_found))}")

if __name__ == "__main__":
    main()