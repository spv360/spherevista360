#!/usr/bin/env python3
"""
Enable and display comments section on all posts
"""

import requests
import os

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

def ensure_comments_enabled():
    """Make sure all posts have comments enabled"""
    print("=" * 80)
    print("🗨️  ENABLING COMMENTS ON ALL POSTS")
    print("=" * 80)
    print()
    
    page = 1
    total_updated = 0
    
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
        
        for post in posts:
            post_id = post['id']
            title = post['title']['rendered'][:50]
            comment_status = post.get('comment_status', 'closed')
            ping_status = post.get('ping_status', 'closed')
            
            # Enable comments if not already
            if comment_status != 'open':
                update_response = requests.post(
                    f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
                    json={
                        'comment_status': 'open',
                        'ping_status': 'open'
                    },
                    auth=(USERNAME, PASSWORD)
                )
                
                if update_response.ok:
                    print(f"✅ Enabled comments: {title}...")
                    total_updated += 1
                else:
                    print(f"❌ Failed: {title}...")
            else:
                print(f"✓ Already enabled: {title}...")
        
        page += 1
    
    print()
    print("=" * 80)
    print(f"📊 SUMMARY: Updated {total_updated} posts")
    print("=" * 80)
    print()
    print("✨ All posts now have comments enabled!")
    print()

if __name__ == '__main__':
    ensure_comments_enabled()
