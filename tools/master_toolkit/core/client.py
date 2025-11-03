"""
WordPress API Client
===================
Unified WordPress REST API client with comprehensive functionality.
"""

import requests
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin

from .config import config
from .auth import auth


class WordPressAPIError(Exception):
    """Custom exception for WordPress API errors."""
    pass


class WordPressClient:
    """
    Comprehensive WordPress REST API client.
    Combines the best features from existing tools with proven authentication.
    """
    
    def __init__(self, username: str = None, password: str = None):
        """Initialize WordPress client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.get('user_agent'),
            'Accept': 'application/json'
        })
        
        # Authenticate if credentials provided
        if username and password:
            self.authenticate(username, password)
    
    def authenticate(self, username: str = None, password: str = None) -> bool:
        """Authenticate with WordPress."""
        if auth.authenticate_from_args(username, password):
            # Update session with auth
            self.session.auth = auth.get_auth_object()
            self.session.headers.update(auth.get_auth_headers())
            return True
        return False
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Dict = None, params: Dict = None, 
                     context: str = None) -> requests.Response:
        """Make authenticated API request with error handling."""
        if not auth.is_authenticated():
            raise WordPressAPIError("Not authenticated. Call authenticate() first.")
        
        url = config.get_api_url(endpoint)
        
        # Add context parameter if specified
        if context and not params:
            params = {}
        if context:
            params['context'] = context
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=config.get('timeout')
            )
            return response
            
        except requests.RequestException as e:
            raise WordPressAPIError(f"Request failed: {e}")
    
    def test_connection(self) -> bool:
        """Test WordPress site connectivity."""
        try:
            response = requests.get(
                config.get_api_url(),
                timeout=config.get('timeout')
            )
            return response.status_code == 200
        except:
            return False
    
    def get_posts(self, per_page: int = 10, page: int = 1, 
                  status: str = 'publish', category: str = None,
                  context: str = None, **kwargs) -> List[Dict]:
        """Get posts with optional filtering."""
        params = {
            'per_page': min(per_page, config.get('per_page_limit')),
            'page': page,
            'status': status,
            **kwargs
        }
        
        if category:
            cat_id = self._get_category_id(category)
            if cat_id:
                params['categories'] = cat_id
        
        response = self._make_request('GET', 'posts', params=params, context=context)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise WordPressAPIError(f"Failed to get posts: {response.status_code}")
    
    def get_post(self, post_id: int, context: str = None) -> Dict:
        """Get a single post by ID."""
        response = self._make_request('GET', f'posts/{post_id}', context=context)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise WordPressAPIError(f"Failed to get post {post_id}: {response.status_code}")
    
    def update_post(self, post_id: int, data: Dict, force_update: bool = False) -> Dict:
        """
        Update an existing post.
        Uses the proven update method from successful tools.
        """
        # Try edit context first (proven to work)
        try:
            current_post = self.get_post(post_id, context='edit')
        except:
            current_post = self.get_post(post_id)
        
        # Prepare update data
        update_data = {}
        if 'content' in data:
            update_data['content'] = data['content']
        if 'title' in data:
            update_data['title'] = data['title']
        if 'status' in data:
            update_data['status'] = data['status']
        if 'categories' in data:
            update_data['categories'] = data['categories']
        
        response = self._make_request('POST', f'posts/{post_id}', data=update_data)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_text = response.text
            raise WordPressAPIError(f"Failed to update post {post_id}: {response.status_code} - {error_text}")
    
    def create_post(self, title: str, content: str, status: str = None,
                   categories: List[str] = None, **kwargs) -> Dict:
        """Create a new post."""
        data = {
            'title': title,
            'content': content,
            'status': status or config.get('default_status'),
            **kwargs
        }
        
        if categories:
            data['categories'] = self._get_category_ids(categories)
        
        response = self._make_request('POST', 'posts', data=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise WordPressAPIError(f"Failed to create post: {response.status_code}")
    
    def get_categories(self) -> List[Dict]:
        """Get all categories."""
        response = self._make_request('GET', 'categories', 
                                    params={'per_page': config.get('per_page_limit')})
        
        if response.status_code == 200:
            return response.json()
        else:
            raise WordPressAPIError(f"Failed to get categories: {response.status_code}")
    
    def get_pages(self, per_page: int = 10, **kwargs) -> List[Dict]:
        """Get pages."""
        params = {
            'per_page': min(per_page, config.get('per_page_limit')),
            **kwargs
        }
        
        response = self._make_request('GET', 'pages', params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise WordPressAPIError(f"Failed to get pages: {response.status_code}")
    
    def _get_category_id(self, category_name: str) -> Optional[int]:
        """Get category ID by name."""
        categories = self.get_categories()
        for cat in categories:
            if cat.get('name', '').lower() == category_name.lower():
                return cat.get('id')
        return None
    
    def _get_category_ids(self, category_names: List[str]) -> List[int]:
        """Convert category names to IDs."""
        categories = self.get_categories()
        category_map = {cat.get('name', '').lower(): cat.get('id') for cat in categories}
        return [category_map.get(name.lower()) for name in category_names 
                if category_map.get(name.lower())]
    
    def get_user_info(self) -> Dict:
        """Get current user information."""
        return auth.get_user_data()


# Convenience function for quick client creation
def create_client(username: str = None, password: str = None) -> WordPressClient:
    """Create and authenticate a WordPress client."""
    client = WordPressClient()
    if username and password:
        if not client.authenticate(username, password):
            raise WordPressAPIError("Authentication failed")
    return client