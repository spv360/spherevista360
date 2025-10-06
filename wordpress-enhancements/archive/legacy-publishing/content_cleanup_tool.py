#!/usr/bin/env python3
"""
WordPress Content Cleanup Tool
Helps clean up unwanted posts that were published accidentally
"""

import os
import sys
import requests
import base64
import json
from datetime import datetime
from typing import Dict, List, Optional

class WordPressContentCleanup:
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
    
    def get_all_posts(self, limit: int = 50) -> List[Dict]:
        """Get recent posts from WordPress"""
        try:
            response = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={'per_page': limit, 'status': 'publish,draft'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to fetch posts: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching posts: {e}")
            return []
    
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
    
    def analyze_recent_posts(self) -> Dict:
        """Analyze recent posts to identify cleanup candidates"""
        print("🔍 Analyzing recent WordPress posts...")
        
        posts = self.get_all_posts(100)  # Get more posts to analyze
        categories = self.get_categories()
        
        if not posts:
            print("❌ No posts found or unable to fetch")
            return {}
        
        print(f"📊 Found {len(posts)} posts")
        
        # Group posts by category and analyze publishing patterns
        today = datetime.now().date()
        recent_posts = []
        category_counts = {}
        
        for post in posts:
            # Parse publish date
            pub_date = datetime.fromisoformat(post['date'].replace('Z', '+00:00')).date()
            
            # Focus on posts from today (likely from your recent publishing)
            if pub_date == today:
                post_categories = []
                for cat_id in post.get('categories', []):
                    cat_name = categories.get(cat_id, f"Category {cat_id}")
                    post_categories.append(cat_name)
                
                post_info = {
                    'id': post['id'],
                    'title': post['title']['rendered'],
                    'status': post['status'],
                    'date': post['date'],
                    'categories': post_categories,
                    'link': post['link']
                }
                
                recent_posts.append(post_info)
                
                # Count by category
                for cat in post_categories:
                    category_counts[cat] = category_counts.get(cat, 0) + 1
        
        return {
            'recent_posts': recent_posts,
            'category_counts': category_counts,
            'total_recent': len(recent_posts)
        }
    
    def display_cleanup_options(self, analysis: Dict):
        """Display cleanup options based on analysis"""
        recent_posts = analysis['recent_posts']
        category_counts = analysis['category_counts']
        
        if not recent_posts:
            print("✅ No recent posts found from today. Nothing to clean up!")
            return
        
        print(f"\n📋 Recent Posts Analysis (Today: {datetime.now().date()})")
        print("=" * 50)
        print(f"📝 Total recent posts: {analysis['total_recent']}")
        print(f"\n📁 Posts by Category:")
        for category, count in sorted(category_counts.items()):
            print(f"   • {category}: {count} posts")
        
        print(f"\n📄 Recent Posts Details:")
        print("-" * 30)
        for i, post in enumerate(recent_posts, 1):
            status_icon = "🟢" if post['status'] == 'publish' else "📝"
            categories_str = ", ".join(post['categories']) if post['categories'] else "Uncategorized"
            print(f"{i:2d}. {status_icon} {post['title']}")
            print(f"    Categories: {categories_str}")
            print(f"    Status: {post['status']}")
            print(f"    Link: {post['link']}")
            print()
    
    def delete_posts_by_category(self, category_name: str) -> int:
        """Delete all posts from a specific category"""
        print(f"🗑️ Deleting posts from '{category_name}' category...")
        
        # Get all categories
        categories = self.get_categories()
        category_id = None
        
        for cat_id, cat_name in categories.items():
            if cat_name.lower() == category_name.lower():
                category_id = cat_id
                break
        
        if not category_id:
            print(f"❌ Category '{category_name}' not found")
            return 0
        
        # Get posts from this category
        try:
            response = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={'categories': category_id, 'per_page': 100},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch posts from category: {response.status_code}")
                return 0
            
            posts = response.json()
            deleted_count = 0
            
            for post in posts:
                # Move to trash (safer than permanent deletion)
                delete_response = requests.delete(
                    f"{self.base_url}/posts/{post['id']}",
                    headers=self.headers,
                    timeout=30
                )
                
                if delete_response.status_code == 200:
                    print(f"✅ Deleted: {post['title']['rendered']}")
                    deleted_count += 1
                else:
                    print(f"❌ Failed to delete: {post['title']['rendered']} (Status: {delete_response.status_code})")
            
            return deleted_count
            
        except Exception as e:
            print(f"❌ Error deleting posts: {e}")
            return 0
    
    def delete_posts_by_ids(self, post_ids: List[int]) -> int:
        """Delete specific posts by their IDs"""
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
        """Interactive cleanup process"""
        print("🧹 WordPress Content Cleanup Tool")
        print("=" * 35)
        print(f"🌐 Site: {self.wp_site}")
        print()
        
        # Test connection
        if not self.test_connection():
            return False
        
        # Analyze recent posts
        analysis = self.analyze_recent_posts()
        self.display_cleanup_options(analysis)
        
        if analysis['total_recent'] == 0:
            return True
        
        print("\n🛠️ Cleanup Options:")
        print("==================")
        print("1. 🗑️ Delete posts from specific category")
        print("2. 🎯 Delete specific posts by selection")
        print("3. 📊 Show detailed post analysis only")
        print("4. ❌ Cancel (no cleanup)")
        print()
        
        choice = input("Choose cleanup option (1-4): ").strip()
        
        if choice == "1":
            print(f"\nAvailable categories:")
            for category in sorted(analysis['category_counts'].keys()):
                count = analysis['category_counts'][category]
                print(f"   • {category} ({count} posts)")
            
            category = input("\nEnter category name to delete: ").strip()
            if category:
                confirm = input(f"⚠️ Delete ALL posts from '{category}' category? (type 'yes' to confirm): ").strip().lower()
                if confirm == 'yes':
                    deleted = self.delete_posts_by_category(category)
                    print(f"\n✅ Cleanup complete: {deleted} posts deleted from '{category}' category")
                else:
                    print("❌ Cleanup cancelled")
            
        elif choice == "2":
            print(f"\nSelect posts to delete (enter post numbers, comma-separated):")
            recent_posts = analysis['recent_posts']
            
            selection = input("Post numbers to delete (e.g., 1,3,5): ").strip()
            if selection:
                try:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    post_ids = [recent_posts[i]['id'] for i in indices if 0 <= i < len(recent_posts)]
                    
                    if post_ids:
                        print(f"\nPosts to delete:")
                        for i in indices:
                            if 0 <= i < len(recent_posts):
                                print(f"   • {recent_posts[i]['title']}")
                        
                        confirm = input(f"\n⚠️ Delete {len(post_ids)} selected posts? (type 'yes' to confirm): ").strip().lower()
                        if confirm == 'yes':
                            deleted = self.delete_posts_by_ids(post_ids)
                            print(f"\n✅ Cleanup complete: {deleted} posts deleted")
                        else:
                            print("❌ Cleanup cancelled")
                    else:
                        print("❌ No valid post numbers selected")
                        
                except ValueError:
                    print("❌ Invalid selection format")
            
        elif choice == "3":
            print("\n✅ Analysis complete. No cleanup performed.")
            
        elif choice == "4":
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
        print("\n💡 Set these first, then run the cleanup tool again")
        return False
    
    try:
        cleanup_tool = WordPressContentCleanup()
        return cleanup_tool.interactive_cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()