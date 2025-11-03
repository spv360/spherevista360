#!/usr/bin/env python3
"""
Check current homepage content
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WordPress credentials from .env
WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# Page ID
HOME_PAGE_ID = 2412

def check_homepage():
    """Check the current homepage content"""
    
    # WordPress API endpoint
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{HOME_PAGE_ID}"
    
    # Make the API request
    print("Fetching current homepage content...")
    response = requests.get(
        url,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        result = response.json()
        content = result.get('content', {}).get('rendered', '')
        
        print("✅ Current Homepage Content:")
        print("=" * 80)
        print(content)
        print("=" * 80)
        print(f"\nContent length: {len(content)} characters")
        
        # Check for key elements
        has_carousel = '[category_carousel]' in content
        has_latest_posts = '[latest_posts' in content
        has_trending = '[trending_topics' in content
        
        print("\nKey Elements Check:")
        print(f"  [category_carousel]: {'✅ Present' if has_carousel else '❌ Missing'}")
        print(f"  [latest_posts]: {'✅ Present' if has_latest_posts else '❌ Missing'}")
        print(f"  [trending_topics]: {'✅ Present' if has_trending else '❌ Missing'}")
        
        return content
    else:
        print(f"❌ Failed to fetch homepage!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

if __name__ == "__main__":
    check_homepage()
