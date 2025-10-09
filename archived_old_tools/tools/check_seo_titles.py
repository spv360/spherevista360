#!/usr/bin/env python3
"""
SEO Title Length Checker
Check all recent posts for SEO title length issues (should be ≤60 characters)
"""

import requests
import json

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def get_post_data(post_id):
    """Get post data from WordPress"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching post {post_id}: {response.status_code}")
        return None

def check_title_length(title):
    """Check if title exceeds SEO recommendations"""
    return len(title), len(title) > 60

def suggest_shortened_title(title, max_length=60):
    """Suggest a shortened version of the title"""
    if len(title) <= max_length:
        return title
    
    # Try to shorten while keeping meaning
    words = title.split()
    shortened = ""
    
    for word in words:
        if len(shortened + " " + word) <= max_length:
            if shortened:
                shortened += " " + word
            else:
                shortened = word
        else:
            break
    
    # If we couldn't fit any meaningful content, truncate
    if not shortened:
        shortened = title[:max_length-3] + "..."
    
    return shortened

def main():
    """Main function to check SEO title lengths"""
    print("SEO Title Length Checker")
    print("=" * 50)
    print("Checking posts for titles exceeding 60 characters...")
    print()
    
    # Post IDs to check (recent publications)
    post_ids = [1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838]
    
    issues_found = []
    
    for post_id in post_ids:
        post_data = get_post_data(post_id)
        if not post_data:
            continue
        
        title = post_data.get('title', {}).get('rendered', '')
        if not title:
            continue
        
        title_length, exceeds_limit = check_title_length(title)
        
        print(f"Post {post_id}: {title}")
        print(f"  Length: {title_length} characters", end="")
        
        if exceeds_limit:
            print(" ❌ EXCEEDS 60 CHAR LIMIT")
            suggested = suggest_shortened_title(title)
            print(f"  Suggested: {suggested} ({len(suggested)} chars)")
            issues_found.append({
                'post_id': post_id,
                'original_title': title,
                'length': title_length,
                'suggested_title': suggested,
                'url': post_data.get('link', '')
            })
        else:
            print(" ✅ OK")
        
        print()
    
    # Summary
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if issues_found:
        print(f"Found {len(issues_found)} posts with title length issues:")
        print()
        
        for issue in issues_found:
            print(f"🔧 Post {issue['post_id']}: {issue['original_title'][:50]}...")
            print(f"   Current: {issue['length']} chars")
            print(f"   Suggested: {issue['suggested_title']}")
            print(f"   URL: {issue['url']}")
            print()
        
        print("Recommendation: Update these titles to improve SEO performance.")
    else:
        print("✅ All posts have appropriate title lengths!")
    
    print(f"\nTotal posts checked: {len(post_ids)}")
    print(f"Posts with issues: {len(issues_found)}")

if __name__ == "__main__":
    main()