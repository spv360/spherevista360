#!/usr/bin/env python3
"""
Enhanced WordPress Client
=========================
Production-ready WordPress REST API client with comprehensive functionality.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import getpass


class WordPressClient:
    """Enhanced WordPress REST API client for content management."""
    
    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        """Initialize WordPress client with optional credentials."""
        self.base_url = base_url or "https://spherevista360.com"
        self.username = username
        self.password = password
        self.auth = None
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'WordPress-Tools/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def authenticate(self, username: str = None, password: str = None) -> bool:
        """Authenticate with WordPress using application password."""
        try:
            if not username:
                username = self.username or input("Enter WordPress username: ")
            if not password:
                password = self.password or getpass.getpass("Enter application password: ")
            
            self.auth = HTTPBasicAuth(username, password)
            self.session.auth = self.auth
            
            # Test authentication
            response = self.session.get(f"{self.base_url}/wp-json/wp/v2/users/me")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Authenticated as: {user_data.get('name', 'Unknown')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_posts(self, per_page: int = 10, page: int = 1, category: str = None, 
                  status: str = 'publish', **kwargs) -> List[Dict]:
        """Get posts with optional filtering."""
        params = {
            'per_page': min(per_page, 100),  # WordPress API limit
            'page': page,
            'status': status,
            **kwargs
        }
        
        if category:
            # Get category ID
            categories = self.get_categories()
            cat_id = None
            for cat in categories:
                if cat.get('name', '').lower() == category.lower():
                    cat_id = cat.get('id')
                    break
            if cat_id:
                params['categories'] = cat_id
        
        response = self.session.get(f"{self.base_url}/wp-json/wp/v2/posts", params=params)
        return response.json() if response.status_code == 200 else []
    
    def get_post(self, post_id: int) -> Dict:
        """Get a single post by ID."""
        response = self.session.get(f"{self.base_url}/wp-json/wp/v2/posts/{post_id}")
        return response.json() if response.status_code == 200 else {}
    
    def create_post(self, title: str, content: str, status: str = 'publish', 
                   categories: List[str] = None, tags: List[str] = None, **kwargs) -> Dict:
        """Create a new post."""
        data = {
            'title': title,
            'content': content,
            'status': status,
            **kwargs
        }
        
        if categories:
            data['categories'] = self._get_category_ids(categories)
        if tags:
            data['tags'] = self._get_tag_ids(tags)
        
        response = self.session.post(f"{self.base_url}/wp-json/wp/v2/posts", json=data)
        return response.json() if response.status_code == 201 else {}
    
    def update_post(self, post_id: int, data: Dict) -> bool:
        """Update an existing post."""
        response = self.session.post(f"{self.base_url}/wp-json/wp/v2/posts/{post_id}", json=data)
        return response.status_code == 200
    
    def delete_post(self, post_id: int, force: bool = False) -> bool:
        """Delete a post."""
        params = {'force': force} if force else {}
        response = self.session.delete(f"{self.base_url}/wp-json/wp/v2/posts/{post_id}", params=params)
        return response.status_code in [200, 410]
    
    def get_categories(self) -> List[Dict]:
        """Get all categories."""
        response = self.session.get(f"{self.base_url}/wp-json/wp/v2/categories", 
                                  params={'per_page': 100})
        return response.json() if response.status_code == 200 else []
    
    def get_pages(self, per_page: int = 10) -> List[Dict]:
        """Get pages."""
        response = self.session.get(f"{self.base_url}/wp-json/wp/v2/pages", 
                                  params={'per_page': per_page})
        return response.json() if response.status_code == 200 else []
    
    def _get_category_ids(self, category_names: List[str]) -> List[int]:
        """Convert category names to IDs."""
        categories = self.get_categories()
        category_map = {cat.get('name', '').lower(): cat.get('id') for cat in categories}
        return [category_map.get(name.lower()) for name in category_names if category_map.get(name.lower())]
    
    def _get_tag_ids(self, tag_names: List[str]) -> List[int]:
        """Convert tag names to IDs (simplified)."""
        # This would need implementation for tag creation/retrieval
        return []
    
    def test_connection(self) -> bool:
        """Test WordPress site connectivity."""
        try:
            response = self.session.get(f"{self.base_url}/wp-json/wp/v2/")
            return response.status_code == 200
        except:
            return False


# Utility functions
def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"🔧 {title}")
    print("=" * 50)


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n📊 {title}")
    print("-" * 40)


def format_percentage(value: float) -> str:
    """Format percentage with color coding."""
    if value >= 90:
        return f"🟢 {value:.1f}%"
    elif value >= 70:
        return f"🟡 {value:.1f}%"
    else:
        return f"🔴 {value:.1f}%"


if __name__ == "__main__":
    # Test the client
    wp = WordPressClient()
    if wp.authenticate():
        print("✅ WordPress client working!")
        posts = wp.get_posts(per_page=3)
        print(f"📄 Found {len(posts)} recent posts")
    else:
        print("❌ Authentication failed")