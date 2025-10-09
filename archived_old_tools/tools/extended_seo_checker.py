#!/usr/bin/env python3
"""
Extended SEO Title Checker
Check ALL posts on the site for SEO title length issues
"""

import requests
import json

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def get_all_posts(per_page=20, max_pages=10):
    """Get all posts from WordPress"""
    all_posts = []
    page = 1
    
    while page <= max_pages:
        url = f"{WP_BASE_URL}/posts"
        params = {
            'per_page': per_page,
            'page': page,
            'status': 'publish'
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                posts = response.json()
                if not posts:  # No more posts
                    break
                all_posts.extend(posts)
                print(f"Fetched page {page}: {len(posts)} posts")
                page += 1
            else:
                print(f"Error fetching page {page}: {response.status_code}")
                break
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    return all_posts

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
    """Main function to check ALL posts for SEO title lengths"""
    print("Extended SEO Title Length Checker")
    print("=" * 60)
    print("Scanning ALL published posts for title length issues...")
    print()
    
    # Get all posts
    print("Fetching all posts...")
    all_posts = get_all_posts(per_page=50, max_pages=20)  # Up to 1000 posts
    
    print(f"\nFound {len(all_posts)} total published posts")
    print("Analyzing titles...")
    print()
    
    issues_found = []
    total_checked = 0
    
    for post in all_posts:
        post_id = post.get('id')
        title = post.get('title', {}).get('rendered', '')
        date = post.get('date', '')[:10]  # Get just the date part
        
        if not title:
            continue
        
        total_checked += 1
        title_length, exceeds_limit = check_title_length(title)
        
        if exceeds_limit:
            suggested = suggest_shortened_title(title)
            issues_found.append({
                'post_id': post_id,
                'title': title,
                'length': title_length,
                'suggested_title': suggested,
                'url': post.get('link', ''),
                'date': date
            })
            
            print(f"❌ Post {post_id} ({date}): {title}")
            print(f"   Length: {title_length} characters")
            print(f"   Suggested: {suggested} ({len(suggested)} chars)")
            print()
        else:
            # Only show recent ones that are OK to verify our fixes worked
            if post_id >= 1820:  # Recent posts
                print(f"✅ Post {post_id} ({date}): {title[:50]}... ({title_length} chars)")
    
    # Summary
    print("=" * 60)
    print("COMPREHENSIVE SEO TITLE ANALYSIS")
    print("=" * 60)
    
    if issues_found:
        print(f"🚨 Found {len(issues_found)} posts with title length issues:")
        print()
        
        # Sort by post ID (newest first)
        issues_found.sort(key=lambda x: x['post_id'], reverse=True)
        
        print("POSTS REQUIRING TITLE OPTIMIZATION:")
        print("-" * 40)
        
        for issue in issues_found:
            post_id = issue['post_id']
            title = issue['title']
            length = issue['length']
            suggested = issue['suggested_title']
            date = issue['date']
            
            print(f"📝 Post {post_id} ({date}):")
            print(f"   Current: {title} ({length} chars)")
            print(f"   Suggested: {suggested} ({len(suggested)} chars)")
            print(f"   URL: {issue['url']}")
            print()
        
        # Create update script data
        update_data = {}
        for issue in issues_found:
            update_data[issue['post_id']] = issue['suggested_title']
        
        print("TITLE_FIXES = {")
        for post_id, new_title in update_data.items():
            print(f"    {post_id}: '{new_title}',")
        print("}")
        
    else:
        print("🎉 No posts found with title length issues!")
        print("All titles comply with the 60-character SEO limit.")
    
    print(f"\n📊 STATISTICS:")
    print(f"Total posts analyzed: {total_checked}")
    print(f"Posts with title issues: {len(issues_found)}")
    print(f"Compliance rate: {((total_checked - len(issues_found)) / total_checked * 100):.1f}%")

if __name__ == "__main__":
    main()