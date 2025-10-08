#!/usr/bin/env python3

import os
import requests
import base64
from typing import List

SITE = os.getenv("WP_SITE", "https://spherevista360.com")
USER = os.getenv("WP_USER", "EDITOR_USERNAME")
APP_PASS = os.getenv("WP_APP_PASS", "APPLICATION PASSWORD WITH SPACES")
API = f"{SITE.rstrip('/')}/wp-json/wp/v2"

def auth_header():
    token = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

def get_readme_posts() -> List[dict]:
    """Find all posts that appear to be READMEs"""
    headers = auth_header()
    readme_posts = []
    
    # Search through all posts (handle pagination)
    page = 1
    while True:
        response = requests.get(
            f"{API}/posts",
            headers=headers,
            params={
                "per_page": 100,
                "page": page,
                "search": "README",  # Search for posts containing README
                "status": "publish,draft"  # Include both published and draft posts
            }
        )
        
        if response.status_code == 400:  # No more pages
            break
            
        posts = response.json()
        if not posts:
            break
            
        # Filter posts that look like READMEs
        for post in posts:
            title = post["title"]["rendered"].lower()
            if "readme" in title or post["slug"].lower().startswith("readme"):
                readme_posts.append({
                    "id": post["id"],
                    "title": post["title"]["rendered"],
                    "status": post["status"],
                    "link": post["link"]
                })
        
        page += 1
    
    return readme_posts

def delete_post(post_id: int, force: bool = True) -> bool:
    """Delete a post by ID. Use force=True to skip trash and delete permanently."""
    try:
        response = requests.delete(
            f"{API}/posts/{post_id}",
            headers=auth_header(),
            params={"force": force}
        )
        return response.status_code in (200, 201, 204)
    except Exception as e:
        print(f"Error deleting post {post_id}: {e}")
        return False

def main():
    # Test connection
    try:
        name = requests.get(f"{SITE}/wp-json/").json().get("name")
        me = requests.get(f"{API}/users/me", headers=auth_header()).json()
        print(f"✅ Connected to {name} as {me.get('name')} (roles: {me.get('roles')})")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Find README posts
    print("\nSearching for README posts...")
    readme_posts = get_readme_posts()
    
    if not readme_posts:
        print("No README posts found!")
        return
    
    # Show found posts
    print(f"\nFound {len(readme_posts)} README posts:")
    for i, post in enumerate(readme_posts, 1):
        print(f"{i}. [{post['status'].upper()}] {post['title']}")
        print(f"   URL: {post['link']}")
    
    # Confirm deletion
    response = input("\nDo you want to delete these posts? [y/N]: ").lower()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Delete posts
    print("\nDeleting posts...")
    for post in readme_posts:
        success = delete_post(post["id"])
        status = "✅" if success else "❌"
        print(f"{status} Deleted: {post['title']}")

if __name__ == "__main__":
    main()