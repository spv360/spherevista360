"""
Authentication Module
====================
WordPress authentication management with support for various auth methods.
"""

import base64
import getpass
import requests
from typing import Optional, Tuple, Dict, Any
from requests.auth import HTTPBasicAuth

from .config import config


class WordPressAuth:
    """WordPress authentication manager."""
    
    def __init__(self):
        """Initialize authentication manager."""
        self.username = None
        self.password = None
        self.auth = None
        self.authenticated = False
        self._user_data = None
        self._last_error = None
    
    def authenticate_basic(self, username: str, password: str, base_url: str = None) -> bool:
        """
        Authenticate using basic auth (application password).
        This is the proven method that works with JK user.
        """
        try:
            # Create authentication
            self.auth = HTTPBasicAuth(username, password)
            
            # Test authentication - use provided base_url or default
            test_url = config.get_api_url('users/me')
            if base_url:
                # Override with specific base URL
                api_endpoint = config.get('api_endpoint', '/wp-json/wp/v2').strip('/')
                test_url = f"{base_url.rstrip('/')}/{api_endpoint}/users/me"
            
            # Test authentication
            headers = {
                'User-Agent': config.get('user_agent'),
                'Accept': 'application/json'
            }
            
            response = requests.get(
                test_url,
                auth=self.auth,
                headers=headers,
                timeout=config.get('timeout')
            )
            
            if response.status_code == 200:
                self._user_data = response.json()
                self.username = username
                self.password = password
                self.authenticated = True
                return True
            else:
                # Store error details for debugging
                self._last_error = {
                    'status_code': response.status_code,
                    'response_text': response.text[:500],  # Limit response text
                    'url': test_url
                }
                self._reset_auth()
                return False
                
        except Exception as e:
            self._last_error = {
                'exception': str(e),
                'exception_type': type(e).__name__
            }
            self._reset_auth()
            return False
    
    def authenticate_interactive(self) -> bool:
        """Interactive authentication prompting for credentials."""
        print("🔐 WordPress Authentication Required")
        print("-" * 40)
        
        username = input("Username: ")
        password = getpass.getpass("Application Password: ")
        
        if self.authenticate_basic(username, password):
            print(f"✅ Authenticated as: {self.get_user_name()}")
            return True
        else:
            print("❌ Authentication failed")
            return False
    
    def authenticate_from_args(self, username: str = None, password: str = None, base_url: str = None) -> bool:
        """Authenticate using provided credentials."""
        if not username or not password:
            return self.authenticate_interactive()
        
        return self.authenticate_basic(username, password, base_url)
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests."""
        if not self.authenticated:
            return {}
        
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'User-Agent': config.get('user_agent')
        }
    
    def get_auth_object(self) -> Optional[HTTPBasicAuth]:
        """Get requests auth object."""
        return self.auth if self.authenticated else None
    
    def get_user_data(self) -> Dict[str, Any]:
        """Get authenticated user data."""
        return self._user_data or {}
    
    def get_user_name(self) -> str:
        """Get authenticated user's display name."""
        return self._user_data.get('name', 'Unknown') if self._user_data else 'Not authenticated'
    
    def get_user_id(self) -> Optional[int]:
        """Get authenticated user's ID."""
        return self._user_data.get('id') if self._user_data else None
    
    def can_edit_posts(self) -> bool:
        """Check if user can edit posts."""
        if not self._user_data:
            return False
        capabilities = self._user_data.get('capabilities', {})
        return 'edit_posts' in capabilities
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        return self.authenticated
    
    def _reset_auth(self):
        """Reset authentication state."""
        self.username = None
        self.password = None
        self.auth = None
        self.authenticated = False
        self._user_data = None
    
    def get_last_error(self) -> Optional[Dict[str, Any]]:
        """Get details of the last authentication error."""
        return self._last_error


# Global authentication instance
auth = WordPressAuth()