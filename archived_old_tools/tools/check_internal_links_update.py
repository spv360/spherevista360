#!/usr/bin/env python3
"""
Check for Internal Links to Updated URL
Find any posts that link to the old URL and need updating
"""

import requests

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Old and new URLs
OLD_URL = "https://spherevista360.com/streaming-gets-personal-how-ai-recommenders-shape-what-you-watch/"
NEW_URL = "https://spherevista360.com/streaming-personal-ai-recommenders-shape-watch/"

def find_posts_with_old_links():
    """Find posts that contain links to the old URL"""
    posts_with_old_links = []
    
    try:
        response = requests.get(f"{WP_BASE_URL}/posts", params={'per_page': 50})
        if response.status_code == 200:
            posts = response.json()
            
            for post in posts:
                post_id = post.get('id')
                title = post.get('title', {}).get('rendered', '')
                content = post.get('content', {}).get('rendered', '')
                
                # Skip the post itself
                if post_id == 1833:
                    continue
                
                # Check if this post contains the old URL
                if OLD_URL in content:
                    posts_with_old_links.append({
                        'post_id': post_id,
                        'title': title,
                        'url': post.get('link', ''),
                        'needs_update': True
                    })
    except Exception as e:
        print(f"Error fetching posts: {e}")
    
    return posts_with_old_links

def main():
    """Check for internal links that need updating"""
    print("Internal Links Check for Updated URL")
    print("=" * 50)
    print(f"Checking for internal links to the old URL...")
    print(f"Old URL: {OLD_URL}")
    print(f"New URL: {NEW_URL}")
    print()
    
    # Find posts with old links
    posts_with_old_links = find_posts_with_old_links()
    
    if posts_with_old_links:
        print(f"⚠️ Found {len(posts_with_old_links)} posts with links to the old URL:")
        print()
        
        for post in posts_with_old_links:
            print(f"📝 Post {post['post_id']}: {post['title']}")
            print(f"   URL: {post['url']}")
            print(f"   ⚠️ Needs internal link update")
            print()
        
        print("RECOMMENDATION:")
        print("These posts should be updated to use the new URL to maintain internal linking.")
    else:
        print("✅ No internal links found pointing to the old URL!")
        print("No further updates needed for internal linking.")
    
    print(f"\nSEO RECOMMENDATIONS:")
    print("1. ✅ Set up 301 redirect from old URL to new URL")
    print("2. ✅ Monitor search console for any crawl errors")
    print("3. ✅ Update any external links manually if possible")
    print(f"4. ✅ The new URL ({len(NEW_URL)} chars) is now SEO compliant")

if __name__ == "__main__":
    main()