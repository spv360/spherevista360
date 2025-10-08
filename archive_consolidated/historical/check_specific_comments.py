#!/usr/bin/env python3
"""
Check specific comment details and try different API endpoints
"""

import requests
import json
from datetime import datetime

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def check_comments_detailed():
    print("🔍 DETAILED COMMENT INVESTIGATION")
    print("=" * 50)
    
    # Try different comment endpoints
    endpoints = [
        "/comments",
        "/comments?status=approve",
        "/comments?status=approved", 
        "/comments?status=hold",
        "/comments?status=pending",
        "/comments?per_page=100",
        "/comments?context=view",
        "/comments?context=edit",
        "/comments?_fields=id,status,content,post,author_name,date"
    ]
    
    for endpoint in endpoints:
        print(f"\n🌐 Testing: {WP_API_BASE}{endpoint}")
        try:
            response = requests.get(f"{WP_API_BASE}{endpoint}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   📊 Found: {len(data)} comments")
                
                if data:
                    for comment in data[:3]:  # Show first 3
                        print(f"   💬 Comment ID: {comment.get('id')}")
                        print(f"      Status: {comment.get('status')}")
                        print(f"      Post: {comment.get('post')}")
                        print(f"      Author: {comment.get('author_name', 'Unknown')}")
                        print(f"      Content: {comment.get('content', {}).get('rendered', 'No content')[:100]}...")
                        print()
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")

def check_comment_moderation():
    print("\n🛡️ COMMENT MODERATION CHECK")
    print("=" * 40)
    
    # Check WordPress settings
    settings_url = f"{WP_API_BASE}/settings"
    try:
        response = requests.get(settings_url)
        if response.status_code == 200:
            settings = response.json()
            
            # Look for comment-related settings
            comment_settings = {
                'default_comment_status': settings.get('default_comment_status'),
                'comment_registration': settings.get('comment_registration'),
                'close_comments_for_old_posts': settings.get('close_comments_for_old_posts'),
                'close_comments_days_old': settings.get('close_comments_days_old'),
                'thread_comments': settings.get('thread_comments'),
                'thread_comments_depth': settings.get('thread_comments_depth'),
                'page_comments': settings.get('page_comments'),
                'comments_per_page': settings.get('comments_per_page'),
                'default_comments_page': settings.get('default_comments_page'),
                'comment_order': settings.get('comment_order'),
                'comments_notify': settings.get('comments_notify'),
                'moderation_notify': settings.get('moderation_notify'),
                'comment_moderation': settings.get('comment_moderation'),
                'comment_previously_approved': settings.get('comment_previously_approved')
            }
            
            print("📋 WordPress Comment Settings:")
            for key, value in comment_settings.items():
                if value is not None:
                    print(f"   {key}: {value}")
        else:
            print(f"❌ Could not retrieve settings: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Error checking settings: {e}")

def test_specific_post_comments():
    print("\n📝 CHECKING SPECIFIC POST COMMENTS")
    print("=" * 45)
    
    # Test a few specific posts
    post_ids = [1695, 1694, 1693, 1691, 1689]  # From our earlier check
    
    for post_id in post_ids:
        print(f"\n📋 Post ID: {post_id}")
        
        # Get post details
        try:
            post_response = requests.get(f"{WP_API_BASE}/posts/{post_id}")
            if post_response.status_code == 200:
                post_data = post_response.json()
                print(f"   Title: {post_data.get('title', {}).get('rendered', 'Unknown')}")
                print(f"   Comment Status: {post_data.get('comment_status')}")
                print(f"   URL: {post_data.get('link')}")
                
                # Try to get comments for this specific post
                comments_response = requests.get(f"{WP_API_BASE}/comments?post={post_id}")
                if comments_response.status_code == 200:
                    comments = comments_response.json()
                    print(f"   💬 Comments found: {len(comments)}")
                    
                    for comment in comments:
                        print(f"      - ID: {comment.get('id')}, Status: {comment.get('status')}")
                        print(f"        Author: {comment.get('author_name')}")
                        print(f"        Content: {comment.get('content', {}).get('rendered', '')[:50]}...")
                else:
                    print(f"   ❌ Comments API error: {comments_response.status_code}")
            else:
                print(f"   ❌ Post API error: {post_response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")

def main():
    print("🔧 WORDPRESS COMMENT DEEP DIVE")
    print("=" * 50)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    check_comments_detailed()
    check_comment_moderation()
    test_specific_post_comments()
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("1. If no comments found via API but you see them in admin:")
    print("   - Comments might be in database but not accessible via REST API")
    print("   - Theme might be using custom comment queries")
    print("   - Comment permissions/authentication issues")
    print()
    print("2. Check WordPress Admin → Comments:")
    print("   - Note the exact post ID where approved comment exists")
    print("   - Check the comment content and author")
    print("   - Try editing the comment to 'update' it")
    print()
    print("3. Theme Investigation:")
    print("   - Comments form shows = theme supports comments")
    print("   - Missing comments = theme not displaying existing comments")
    print("   - Check theme's comments.php or single.php files")

if __name__ == "__main__":
    main()