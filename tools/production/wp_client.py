#!/usr/bin/env python3
"""
WordPress API Client Module
==========================
Reusable WordPress REST API client with authentication and common operations.
"""

import requests
from requests.auth import HTTPBasicAuth
import getpass
from typing import Dict, List, Optional, Union
import json
from datetime import datetime


class WordPressClient:
    """WordPress REST API client with authentication and common operations."""
    
    def __init__(self, base_url: str = "https://spherevista360.com/wp-json/wp/v2"):
        """Initialize WordPress client.
        
        Args:
            base_url: Base URL for WordPress REST API
        """
        self.base_url = base_url.rstrip('/')
        self.auth = None
        self.session = requests.Session()
        
    def authenticate(self, username: str = None, password: str = None) -> bool:
        """Authenticate with WordPress using application password.
        
        Args:
            username: WordPress username (will prompt if not provided)
            password: Application password (will prompt if not provided)
            
        Returns:
            bool: True if authentication successful
        """
        if not username:
            username = input("Enter WordPress username: ")
        if not password:
            password = getpass.getpass("Enter application password: ")
            
        self.auth = HTTPBasicAuth(username, password)
        
        # Test authentication
        try:
            response = self.session.get(f"{self.base_url}/users/me", auth=self.auth)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Authenticated as: {user_data.get('name', username)}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_posts(self, **params) -> List[Dict]:
        """Get posts from WordPress.
        
        Args:
            **params: Additional query parameters (per_page, category, etc.)
            
        Returns:
            List of post dictionaries
        """
        default_params = {'per_page': 20}
        default_params.update(params)
        
        response = self.session.get(f"{self.base_url}/posts", 
                                  params=default_params, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_post(self, post_id: int) -> Dict:
        """Get a specific post by ID.
        
        Args:
            post_id: Post ID
            
        Returns:
            Post dictionary
        """
        response = self.session.get(f"{self.base_url}/posts/{post_id}", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def update_post(self, post_id: int, data: Dict) -> Dict:
        """Update a post.
        
        Args:
            post_id: Post ID
            data: Update data
            
        Returns:
            Updated post dictionary
        """
        response = self.session.post(f"{self.base_url}/posts/{post_id}", 
                                   json=data, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_pages(self, **params) -> List[Dict]:
        """Get pages from WordPress.
        
        Args:
            **params: Additional query parameters
            
        Returns:
            List of page dictionaries
        """
        default_params = {'per_page': 50}
        default_params.update(params)
        
        response = self.session.get(f"{self.base_url}/pages", 
                                  params=default_params, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_page(self, page_id: int) -> Dict:
        """Get a specific page by ID.
        
        Args:
            page_id: Page ID
            
        Returns:
            Page dictionary
        """
        response = self.session.get(f"{self.base_url}/pages/{page_id}", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def update_page(self, page_id: int, data: Dict) -> Dict:
        """Update a page.
        
        Args:
            page_id: Page ID
            data: Update data
            
        Returns:
            Updated page dictionary
        """
        response = self.session.post(f"{self.base_url}/pages/{page_id}", 
                                   json=data, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_categories(self) -> List[Dict]:
        """Get all categories.
        
        Returns:
            List of category dictionaries
        """
        response = self.session.get(f"{self.base_url}/categories", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_category(self, category_id: int) -> Dict:
        """Get a specific category by ID.
        
        Args:
            category_id: Category ID
            
        Returns:
            Category dictionary
        """
        response = self.session.get(f"{self.base_url}/categories/{category_id}", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def delete_page(self, page_id: int) -> bool:
        """Delete a page.
        
        Args:
            page_id: Page ID
            
        Returns:
            bool: True if successful
        """
        response = self.session.delete(f"{self.base_url}/pages/{page_id}", auth=self.auth)
        return response.status_code in [200, 204]
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post.
        
        Args:
            post_id: Post ID
            
        Returns:
            bool: True if successful
        """
        response = self.session.delete(f"{self.base_url}/posts/{post_id}", auth=self.auth)
        return response.status_code in [200, 204]
    
    def get_page_content(self, url: str) -> str:
        """Get full page content by URL.
        
        Args:
            url: Page URL
            
        Returns:
            Page HTML content
        """
        response = self.session.get(url)
        response.raise_for_status()
        return response.text
    
    def test_url(self, url: str) -> int:
        """Test if URL is accessible.
        
        Args:
            url: URL to test
            
        Returns:
            HTTP status code
        """
        try:
            response = self.session.head(url, timeout=10)
            return response.status_code
        except:
            return 0


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*50}")
    print(f"🔧 {title}")
    print('='*50)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n📊 {title}")
    print('-'*40)


def format_timestamp() -> str:
    """Get formatted timestamp."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')