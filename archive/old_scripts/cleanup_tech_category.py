#!/usr/bin/env python3
"""
WordPress Category Cleanup Script
Uses the same authentication as the bulk publisher
"""

import os
import requests
import base64
import json

# Use the same credentials as the bulk publisher
SITE = os.getenv("WP_SITE", "https://spherevista360.com")
USER = os.getenv("WP_USER", "JK")
APP_PASS = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
API = f"{SITE.rstrip('/')}/wp-json/wp/v2"

def auth_header():
    token = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

def get_categories():
    """Get all categories"""
    response = requests.get(f"{API}/categories", headers=auth_header(), params={'per_page': 100})
    return response.json() if response.status_code == 200 else []

def get_posts_by_category(category_id):
    """Get posts in a specific category"""
    response = requests.get(f"{API}/posts", headers=auth_header(), params={'categories': category_id, 'per_page': 100})
    return response.json() if response.status_code == 200 else []

def delete_post(post_id):
    """Delete a post permanently"""
    response = requests.delete(f"{API}/posts/{post_id}", headers=auth_header(), params={'force': True})
    return response.status_code == 200

def delete_category(category_id):
    """Delete a category"""
    response = requests.delete(f"{API}/categories/{category_id}", headers=auth_header(), params={'force': True})
    return response.status_code == 200

def main():
    print("=== WordPress Tech Category Cleanup ===")
    print("Using bulk publisher authentication method")
    
    # Get categories
    categories = get_categories()
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
    tech_posts = get_posts_by_category(tech_cat['id'])
    print(f"\n=== Posts in Tech Category ({len(tech_posts)} posts) ===")
    
    for post in tech_posts:
        print(f"- {post['title']['rendered']} (ID: {post['id']})")
    
    # Delete duplicate posts in Tech category
    print(f"\n=== Deleting {len(tech_posts)} duplicate posts ===")
    deleted_count = 0
    
    for post in tech_posts:
        print(f"Deleting: {post['title']['rendered']} (ID: {post['id']})")
        if delete_post(post['id']):
            print(f"✅ Successfully deleted post {post['id']}")
            deleted_count += 1
        else:
            print(f"❌ Failed to delete post {post['id']}")
    
    # Delete Tech category if it's now empty
    if deleted_count == len(tech_posts):
        print(f"\n=== Deleting empty Tech category ===")
        if delete_category(tech_cat['id']):
            print(f"✅ Successfully deleted Tech category (ID: {tech_cat['id']})")
        else:
            print(f"❌ Failed to delete Tech category")
    
    # Final verification
    print(f"\n=== Final Verification ===")
    final_categories = get_categories()
    
    tech_still_exists = any(cat['slug'] == 'tech' for cat in final_categories)
    technology_cat_final = next((cat for cat in final_categories if cat['slug'] == 'technology'), None)
    
    if not tech_still_exists:
        print("✅ Tech category successfully removed")
    else:
        print("❌ Tech category still exists")
    
    if technology_cat_final:
        print(f"✅ Technology category has {technology_cat_final['count']} posts")
    
    # Count total posts
    total_posts_response = requests.get(f"{API}/posts", headers=auth_header(), params={'per_page': 1})
    total_posts = total_posts_response.headers.get('X-WP-Total', 'Unknown')
    print(f"✅ Total posts on site: {total_posts}")

if __name__ == "__main__":
    main()