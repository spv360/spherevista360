#!/usr/bin/env python3
"""
WordPress Post Analyzer and Targeted Cleanup
Identifies and cleans up posts published from week1_final content
"""

import os
import sys
import requests
import base64
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class WordPressPostAnalyzer:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', '').rstrip('/')
        self.wp_user = os.environ.get('WP_USER', '')
        self.wp_pass = os.environ.get('WP_APP_PASS', '')
        
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            raise ValueError("WordPress credentials not set")
        
        # Set up authentication
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        self.base_url = f"{self.wp_site}/wp-json/wp/v2"
        
        # Common week1_final content indicators
        self.week1_indicators = [
            'digital banking', 'fintech', 'future', 'revolution',
            'ai', 'artificial intelligence', 'cloud', 'technology',
            'politics', 'election', 'policy', 'government',
            'travel', 'visa', 'destination', 'tourism',
            'world', 'global', 'international', 'affairs'
        ]
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected as {user_data.get('name')} with roles: {user_data.get('roles')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_all_posts(self, limit: int = 100) -> List[Dict]:
        """Get all posts from WordPress"""
        all_posts = []
        page = 1
        per_page = 50
        
        while len(all_posts) < limit:
            try:
                response = requests.get(
                    f"{self.base_url}/posts",
                    headers=self.headers,
                    params={
                        'per_page': per_page, 
                        'page': page,
                        'status': 'publish,draft'
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    posts = response.json()
                    if not posts:  # No more posts
                        break
                    all_posts.extend(posts)
                    page += 1
                else:
                    print(f"❌ Failed to fetch posts page {page}: {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"❌ Error fetching posts: {e}")
                break
        
        return all_posts[:limit]
    
    def get_categories(self) -> Dict[int, str]:
        """Get all categories from WordPress"""
        try:
            response = requests.get(
                f"{self.base_url}/categories",
                headers=self.headers,
                params={'per_page': 100},
                timeout=30
            )
            
            if response.status_code == 200:
                categories = response.json()
                return {cat['id']: cat['name'] for cat in categories}
            else:
                print(f"❌ Failed to fetch categories: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error fetching categories: {e}")
            return {}
    
    def identify_week1_posts(self, posts: List[Dict]) -> Dict:
        """Identify posts that likely came from week1_final content"""
        categories = self.get_categories()
        
        # Get posts from last 24 hours (likely recent uploads)
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        
        recent_posts = []
        week1_categories = []
        likely_week1_posts = []
        
        for post in posts:
            try:
                # Parse publish date
                pub_date = datetime.fromisoformat(post['date'].replace('Z', '+00:00'))
                
                # Get post categories
                post_categories = []
                for cat_id in post.get('categories', []):
                    cat_name = categories.get(cat_id, f"Category {cat_id}")
                    post_categories.append(cat_name)
                
                post_info = {
                    'id': post['id'],
                    'title': post['title']['rendered'],
                    'status': post['status'],
                    'date': post['date'],
                    'pub_date': pub_date,
                    'categories': post_categories,
                    'link': post['link'],
                    'excerpt': post['excerpt']['rendered'][:200] if post.get('excerpt', {}).get('rendered') else '',
                    'is_recent': pub_date > yesterday
                }
                
                # Check if recent
                if pub_date > yesterday:
                    recent_posts.append(post_info)
                
                # Check if likely from week1_final based on content
                title_lower = post_info['title'].lower()
                excerpt_lower = post_info['excerpt'].lower()
                content_text = f"{title_lower} {excerpt_lower}"
                
                week1_score = 0
                matched_indicators = []
                
                for indicator in self.week1_indicators:
                    if indicator in content_text:
                        week1_score += 1
                        matched_indicators.append(indicator)
                
                # Check for week1_final typical categories
                week1_cats = ['Finance', 'Technology', 'Politics', 'Travel', 'World']
                for cat in post_categories:
                    if cat in week1_cats:
                        week1_score += 2
                        week1_categories.append(cat)
                
                if week1_score > 0:
                    post_info['week1_score'] = week1_score
                    post_info['matched_indicators'] = matched_indicators
                    likely_week1_posts.append(post_info)
                    
            except Exception as e:
                print(f"⚠️ Error processing post {post.get('id', 'unknown')}: {e}")
                continue
        
        return {
            'total_posts': len(posts),
            'recent_posts': recent_posts,
            'likely_week1_posts': sorted(likely_week1_posts, key=lambda x: x['week1_score'], reverse=True),
            'week1_categories': list(set(week1_categories))
        }
    
    def display_analysis(self, analysis: Dict):
        """Display detailed analysis of posts"""
        print(f"\n📊 WordPress Posts Analysis")
        print("=" * 30)
        print(f"📝 Total posts on site: {analysis['total_posts']}")
        print(f"🆕 Recent posts (last 24h): {len(analysis['recent_posts'])}")
        print(f"🎯 Likely week1_final posts: {len(analysis['likely_week1_posts'])}")
        
        if analysis['week1_categories']:
            print(f"📁 Week1 categories found: {', '.join(analysis['week1_categories'])}")
        
        # Show recent posts
        if analysis['recent_posts']:
            print(f"\n🆕 Recent Posts (Last 24 Hours):")
            print("-" * 35)
            for i, post in enumerate(analysis['recent_posts'], 1):
                status_icon = "🟢" if post['status'] == 'publish' else "📝"
                categories_str = ", ".join(post['categories']) if post['categories'] else "Uncategorized"
                pub_time = post['pub_date'].strftime('%H:%M')
                print(f"{i:2d}. {status_icon} {post['title']}")
                print(f"    📁 {categories_str} | ⏰ {pub_time}")
                print()
        
        # Show likely week1 posts
        if analysis['likely_week1_posts']:
            print(f"\n🎯 Likely Week1_Final Posts (by relevance):")
            print("-" * 45)
            for i, post in enumerate(analysis['likely_week1_posts'], 1):
                status_icon = "🟢" if post['status'] == 'publish' else "📝"
                categories_str = ", ".join(post['categories']) if post['categories'] else "Uncategorized"
                indicators = ", ".join(post['matched_indicators'][:3]) if post['matched_indicators'] else "N/A"
                print(f"{i:2d}. {status_icon} {post['title']} (Score: {post['week1_score']})")
                print(f"    📁 {categories_str}")
                print(f"    🎯 Indicators: {indicators}")
                print(f"    📅 {post['pub_date'].strftime('%Y-%m-%d %H:%M')}")
                print()
    
    def bulk_delete_posts(self, post_ids: List[int], description: str) -> int:
        """Delete multiple posts"""
        print(f"\n🗑️ Deleting {description}...")
        deleted_count = 0
        
        for post_id in post_ids:
            try:
                # Get post title first
                post_response = requests.get(
                    f"{self.base_url}/posts/{post_id}",
                    headers=self.headers,
                    timeout=30
                )
                
                if post_response.status_code == 200:
                    post_title = post_response.json()['title']['rendered']
                else:
                    post_title = f"Post {post_id}"
                
                # Delete the post
                delete_response = requests.delete(
                    f"{self.base_url}/posts/{post_id}",
                    headers=self.headers,
                    timeout=30
                )
                
                if delete_response.status_code == 200:
                    print(f"✅ Deleted: {post_title}")
                    deleted_count += 1
                else:
                    print(f"❌ Failed to delete: {post_title} (Status: {delete_response.status_code})")
                    
            except Exception as e:
                print(f"❌ Error deleting post {post_id}: {e}")
        
        return deleted_count
    
    def interactive_cleanup(self):
        """Interactive cleanup based on analysis"""
        print("🔍 WordPress Post Analyzer & Targeted Cleanup")
        print("=" * 45)
        print(f"🌐 Site: {self.wp_site}")
        print()
        
        # Test connection
        if not self.test_connection():
            return False
        
        print("📊 Analyzing all posts (this may take a moment)...")
        
        # Get all posts
        all_posts = self.get_all_posts(150)  # Get more posts for better analysis
        
        # Analyze posts
        analysis = self.identify_week1_posts(all_posts)
        self.display_analysis(analysis)
        
        if not analysis['likely_week1_posts'] and not analysis['recent_posts']:
            print("✅ No likely week1_final posts or recent posts found!")
            return True
        
        print("\n🛠️ Cleanup Options:")
        print("==================")
        print("1. 🗑️ Delete all recent posts (last 24h)")
        print("2. 🎯 Delete likely week1_final posts")
        print("3. 🔍 Select specific posts to delete")
        print("4. 📊 Show detailed post list only")
        print("5. ❌ Cancel cleanup")
        print()
        
        choice = input("Choose cleanup option (1-5): ").strip()
        
        if choice == "1":
            if analysis['recent_posts']:
                print(f"\n⚠️ This will delete ALL {len(analysis['recent_posts'])} recent posts!")
                confirm = input("Type 'DELETE RECENT' to confirm: ").strip()
                if confirm == 'DELETE RECENT':
                    post_ids = [post['id'] for post in analysis['recent_posts']]
                    deleted = self.bulk_delete_posts(post_ids, "recent posts")
                    print(f"\n✅ Deleted {deleted} recent posts")
                else:
                    print("❌ Cleanup cancelled")
            else:
                print("❌ No recent posts found")
        
        elif choice == "2":
            if analysis['likely_week1_posts']:
                print(f"\n⚠️ This will delete {len(analysis['likely_week1_posts'])} likely week1_final posts!")
                confirm = input("Type 'DELETE WEEK1' to confirm: ").strip()
                if confirm == 'DELETE WEEK1':
                    post_ids = [post['id'] for post in analysis['likely_week1_posts']]
                    deleted = self.bulk_delete_posts(post_ids, "likely week1_final posts")
                    print(f"\n✅ Deleted {deleted} week1_final posts")
                else:
                    print("❌ Cleanup cancelled")
            else:
                print("❌ No likely week1_final posts found")
        
        elif choice == "3":
            # Combine all posts for selection
            all_relevant_posts = analysis['recent_posts'] + [p for p in analysis['likely_week1_posts'] if p not in analysis['recent_posts']]
            
            if all_relevant_posts:
                print(f"\nSelect posts to delete (enter numbers, comma-separated):")
                for i, post in enumerate(all_relevant_posts, 1):
                    status_icon = "🟢" if post['status'] == 'publish' else "📝"
                    categories_str = ", ".join(post['categories']) if post['categories'] else "Uncategorized"
                    print(f"{i:2d}. {status_icon} {post['title']} ({categories_str})")
                
                selection = input("\nPost numbers to delete (e.g., 1,3,5): ").strip()
                if selection:
                    try:
                        indices = [int(x.strip()) - 1 for x in selection.split(',')]
                        post_ids = [all_relevant_posts[i]['id'] for i in indices if 0 <= i < len(all_relevant_posts)]
                        
                        if post_ids:
                            print(f"\nPosts to delete:")
                            for i in indices:
                                if 0 <= i < len(all_relevant_posts):
                                    print(f"   • {all_relevant_posts[i]['title']}")
                            
                            confirm = input(f"\n⚠️ Delete {len(post_ids)} selected posts? (type 'yes' to confirm): ").strip().lower()
                            if confirm == 'yes':
                                deleted = self.bulk_delete_posts(post_ids, "selected posts")
                                print(f"\n✅ Deleted {deleted} selected posts")
                            else:
                                print("❌ Cleanup cancelled")
                        else:
                            print("❌ No valid post numbers selected")
                            
                    except ValueError:
                        print("❌ Invalid selection format")
            else:
                print("❌ No relevant posts found for selection")
        
        elif choice == "4":
            print("\n✅ Analysis complete. No cleanup performed.")
            
        elif choice == "5":
            print("❌ Cleanup cancelled")
            
        else:
            print("❌ Invalid option")
        
        return True

def main():
    """Main execution function"""
    # Check environment variables
    required_vars = ['WP_SITE', 'WP_USER', 'WP_APP_PASS']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your_value'")
        return False
    
    try:
        analyzer = WordPressPostAnalyzer()
        return analyzer.interactive_cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()