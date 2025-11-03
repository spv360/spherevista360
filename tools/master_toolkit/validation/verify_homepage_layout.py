#!/usr/bin/env python3
"""
Verify homepage layout: sidebar position and carousel
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
HOME_PAGE_ID = 2412

def verify_homepage():
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{HOME_PAGE_ID}"
    response = requests.get(url, auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD))
    if response.status_code != 200:
        print(f"❌ Failed to fetch homepage: {response.status_code}")
        return
    content = response.json().get('content', {}).get('rendered', '')
    soup = BeautifulSoup(content, 'html.parser')
    # Check for sidebar and main content wrapper
    wrapper = soup.find(class_='home-content-wrapper')
    sidebar = soup.find(class_='sidebar-area')
    main = soup.find(class_='main-content-area')
    carousel = soup.find(string='[category_carousel]') or soup.find(class_='category-carousel-container')
    print("=== Homepage Layout Verification ===")
    print(f"home-content-wrapper found: {'✅' if wrapper else '❌'}")
    print(f"main-content-area found: {'✅' if main else '❌'}")
    print(f"sidebar-area found: {'✅' if sidebar else '❌'}")
    print(f"Carousel found: {'✅' if carousel else '❌'}")
    # Check sidebar position in grid (cannot fully verify visually, but can check order)
    if wrapper and sidebar and main:
        children = [c for c in wrapper.children if getattr(c, 'name', None)]
        sidebar_index = next((i for i, c in enumerate(children) if 'sidebar-area' in c.get('class', [])), -1)
        main_index = next((i for i, c in enumerate(children) if 'main-content-area' in c.get('class', [])), -1)
        print(f"main-content-area index: {main_index}")
        print(f"sidebar-area index: {sidebar_index}")
        if sidebar_index > main_index:
            print("✅ Sidebar appears after main content (should be right on desktop)")
        else:
            print("❌ Sidebar appears before main content (should be right on desktop)")
    print("=== End Verification ===")

if __name__ == "__main__":
    verify_homepage()
