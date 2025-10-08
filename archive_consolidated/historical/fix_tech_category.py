#!/usr/bin/env python3
"""
WordPress Tech Category Cleanup Script
Fixes duplicate posts and removes old Tech category
"""

import requests
import json
import base64
from urllib.parse import urljoin

class WordPressCategoryFixer:
    def __init__(self):
        self.wp_url = "https://spherevista360.com"
        self.wp_user = "kadmin"
        self.wp_password = "YHH8 Kzeu 6f2x Zn1I LiX9 3eAP"
        
        # Create Basic Auth header
        credentials = f"{self.wp_user}:{self.wp_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
    
    def get_categories(self):
        """Get all categories"""
        response = requests.get(
            f"{self.wp_url}/wp-json/wp/v2/categories",
            headers=self.headers,
            params={'per_page': 100}
        )
        return response.json() if response.status_code == 200 else []
    
    def get_posts_by_category(self, category_id):
        """Get posts in a specific category"""
        response = requests.get(
            f"{self.wp_url}/wp-json/wp/v2/posts",
            headers=self.headers,
            params={'categories': category_id, 'per_page': 100}
        )
        return response.json() if response.status_code == 200 else []
    
    def delete_post(self, post_id):
        """Delete a post permanently"""
        response = requests.delete(
            f"{self.wp_url}/wp-json/wp/v2/posts/{post_id}",
            headers=self.headers,
            params={'force': True}
        )
        return response.status_code == 200
    
    def delete_category(self, category_id):
        """Delete a category"""
        response = requests.delete(
            f"{self.wp_url}/wp-json/wp/v2/categories/{category_id}",
            headers=self.headers,
            params={'force': True}
        )
        return response.status_code == 200
    
    def fix_tech_category_issue(self):
        """Main function to fix the Tech category duplication"""
        print("=== WordPress Tech Category Cleanup ===")
        
        # Get categories
        categories = self.get_categories()
        tech_cat = next((cat for cat in categories if cat['slug'] == 'tech'), None)
        technology_cat = next((cat for cat in categories if cat['slug'] == 'technology'), None)
        
        if not tech_cat:
            print("❌ Tech category not found")
            return
        
        if not technology_cat:
            print("❌ Technology category not found")
            return
        
        print(f"Found Tech category (ID: {tech_cat['id']}, Posts: {tech_cat['count']})")
        print(f"Found Technology category (ID: {technology_cat['id']}, Posts: {technology_cat['count']})")
        
        # Get posts in Tech category
        tech_posts = self.get_posts_by_category(tech_cat['id'])
        print(f"\n=== Posts in Tech Category ({len(tech_posts)} posts) ===")
        
        for post in tech_posts:
            print(f"- {post['title']['rendered']} (ID: {post['id']})")
        
        # Delete duplicate posts in Tech category
        print(f"\n=== Deleting {len(tech_posts)} duplicate posts ===")
        deleted_count = 0
        
        for post in tech_posts:
            print(f"Deleting: {post['title']['rendered']} (ID: {post['id']})")
            if self.delete_post(post['id']):
                print(f"✅ Successfully deleted post {post['id']}")
                deleted_count += 1
            else:
                print(f"❌ Failed to delete post {post['id']}")
        
        # Delete Tech category if it's now empty
        if deleted_count == len(tech_posts):
            print(f"\n=== Deleting empty Tech category ===")
            if self.delete_category(tech_cat['id']):
                print(f"✅ Successfully deleted Tech category (ID: {tech_cat['id']})")
            else:
                print(f"❌ Failed to delete Tech category")
        
        # Final verification
        print(f"\n=== Final Verification ===")
        final_categories = self.get_categories()
        
        tech_still_exists = any(cat['slug'] == 'tech' for cat in final_categories)
        technology_cat_final = next((cat for cat in final_categories if cat['slug'] == 'technology'), None)
        
        if not tech_still_exists:
            print("✅ Tech category successfully removed")
        else:
            print("❌ Tech category still exists")
        
        if technology_cat_final:
            print(f"✅ Technology category has {technology_cat_final['count']} posts")
        
        # Count total posts
        total_posts_response = requests.get(
            f"{self.wp_url}/wp-json/wp/v2/posts",
            headers=self.headers,
            params={'per_page': 1}
        )
        total_posts = total_posts_response.headers.get('X-WP-Total', 'Unknown')
        print(f"✅ Total posts on site: {total_posts}")

if __name__ == "__main__":
    fixer = WordPressCategoryFixer()
    fixer.fix_tech_category_issue()