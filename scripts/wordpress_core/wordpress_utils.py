#!/usr/bin/env python3
"""
WordPress Utilities Module
Reusable functions for WordPress REST API interactions
"""
import requests
import base64
from typing import Optional, Dict, List

# WordPress Configuration
WP_URL = "https://spherevista360.com"
WP_USER = "JK"
WP_APP_PASSWORD = "R8sj tOZG 8ORr ntSZ XlPt qTE9"


class WordPressAPI:
    """WordPress REST API wrapper for common operations"""
    
    def __init__(self, url: str = WP_URL, username: str = WP_USER, password: str = WP_APP_PASSWORD):
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        self._headers = self._create_headers()
    
    def _create_headers(self) -> Dict[str, str]:
        """Create authorization headers"""
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }
    
    def get_page(self, page_id: int) -> Optional[Dict]:
        """Get a page by ID"""
        response = requests.get(
            f"{self.url}/wp-json/wp/v2/pages/{page_id}",
            headers=self._headers
        )
        return response.json() if response.status_code == 200 else None
    
    def search_pages(self, search_term: str, per_page: int = 20) -> List[Dict]:
        """Search for pages by term"""
        response = requests.get(
            f"{self.url}/wp-json/wp/v2/pages",
            headers=self._headers,
            params={"search": search_term, "per_page": per_page}
        )
        return response.json() if response.status_code == 200 else []
    
    def find_page_by_slug(self, slug: str) -> Optional[Dict]:
        """Find page by slug"""
        pages = self.search_pages(slug)
        for page in pages:
            if page['slug'] == slug:
                return page
        return None
    
    def update_page(self, page_id: int, content: str, title: Optional[str] = None) -> bool:
        """Update page content and optionally title"""
        update_data = {"content": content, "status": "publish"}
        if title:
            update_data["title"] = title
        
        response = requests.post(
            f"{self.url}/wp-json/wp/v2/pages/{page_id}",
            headers=self._headers,
            json=update_data
        )
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Error updating page: {response.status_code}")
            print(response.text)
            return False
    
    def create_page(self, title: str, content: str, slug: Optional[str] = None) -> Optional[int]:
        """Create a new page"""
        page_data = {
            "title": title,
            "content": content,
            "status": "publish"
        }
        if slug:
            page_data["slug"] = slug
        
        response = requests.post(
            f"{self.url}/wp-json/wp/v2/pages",
            headers=self._headers,
            json=page_data
        )
        
        if response.status_code == 201:
            return response.json()['id']
        else:
            print(f"❌ Error creating page: {response.status_code}")
            print(response.text)
            return None
    
    def delete_page(self, page_id: int, force: bool = False) -> bool:
        """Delete a page (move to trash or permanently delete)"""
        params = {"force": "true"} if force else {}
        response = requests.delete(
            f"{self.url}/wp-json/wp/v2/pages/{page_id}",
            headers=self._headers,
            params=params
        )
        return response.status_code in [200, 204]
    
    def list_pages(self, per_page: int = 100, page: int = 1) -> List[Dict]:
        """List all pages"""
        response = requests.get(
            f"{self.url}/wp-json/wp/v2/pages",
            headers=self._headers,
            params={"per_page": per_page, "page": page}
        )
        return response.json() if response.status_code == 200 else []


def read_content_file(filepath: str) -> str:
    """Read HTML content from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        return ""
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return ""


def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")


def print_info(message: str):
    """Print info message"""
    print(f"ℹ️  {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"⚠️  {message}")


if __name__ == "__main__":
    # Test the module
    print("🔧 WordPress Utilities Module")
    print("=" * 50)
    
    api = WordPressAPI()
    print_info("Testing WordPress API connection...")
    
    pages = api.list_pages(per_page=5)
    if pages:
        print_success(f"Connected! Found {len(pages)} pages")
        for page in pages:
            print(f"  - {page['title']['rendered']} (ID: {page['id']})")
    else:
        print_error("Failed to connect or no pages found")
