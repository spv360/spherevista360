#!/usr/bin/env python3
"""
Quick Image URL Checker - Test specific image URLs from our fixed posts
"""

import requests
import re

# Check some of the URLs we fixed
test_urls = [
    "https://images.unsplash.com/photo-1518709268805-4e9042af2176?auto=format&fit=crop&w=1600&h=900&q=80",
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1600&h=900&q=80",
    "https://images.unsplash.com/photo-1561736778-92e52a7769ef?auto=format&fit=crop&w=1600&h=900&q=80",
]

print("Testing fixed image URLs:")
print("=" * 50)

for i, url in enumerate(test_urls, 1):
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        status = "✅ WORKING" if response.status_code == 200 else f"❌ ERROR {response.status_code}"
        print(f"{i}. {status} - {url}")
    except Exception as e:
        print(f"{i}. ❌ FAILED - {url} - {str(e)}")

print("\nTesting one of our recently published posts:")
print("=" * 50)

# Check post content directly
try:
    response = requests.get("https://spherevista360.com/wp-json/wp/v2/posts/1829")
    if response.status_code == 200:
        content = response.json().get('content', {}).get('rendered', '')
        
        # Find image URLs
        image_urls = re.findall(r'https://images\.unsplash\.com/[^"\s]*', content)
        print(f"Found {len(image_urls)} image URLs in post 1829:")
        
        for i, url in enumerate(image_urls[:3], 1):  # Check first 3
            try:
                img_response = requests.head(url, timeout=10, allow_redirects=True)
                status = "✅ WORKING" if img_response.status_code == 200 else f"❌ ERROR {img_response.status_code}"
                print(f"{i}. {status} - {url[:80]}...")
            except Exception as e:
                print(f"{i}. ❌ FAILED - {url[:80]}... - {str(e)}")
    else:
        print(f"Failed to fetch post: {response.status_code}")
except Exception as e:
    print(f"Error fetching post: {e}")