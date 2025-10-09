#!/usr/bin/env python3
"""
Final Validation Report
Check all recently published posts for image and link quality
"""

import requests
import re
import html

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def test_url(url, timeout=10):
    """Test if a URL is working"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def get_post_content(post_id):
    """Get post content from WordPress"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def validate_post_images(post_id):
    """Validate all images in a post"""
    post_data = get_post_content(post_id)
    if not post_data:
        return {"error": "Could not fetch post"}
    
    content = post_data.get('content', {}).get('rendered', '')
    content = html.unescape(content)
    
    # Find all image URLs
    image_urls = re.findall(r'https://images\.unsplash\.com/[^"\s]*', content)
    
    working_images = 0
    broken_images = 0
    
    for url in image_urls:
        if test_url(url):
            working_images += 1
        else:
            broken_images += 1
    
    return {
        "total_images": len(image_urls),
        "working_images": working_images,
        "broken_images": broken_images,
        "success_rate": (working_images / len(image_urls) * 100) if image_urls else 100
    }

def main():
    """Main validation function"""
    print("Final Validation Report")
    print("=" * 50)
    
    # Post IDs to validate
    post_ids = [1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838]
    
    total_images = 0
    total_working = 0
    total_broken = 0
    
    for post_id in post_ids:
        print(f"\nPost {post_id}:")
        
        result = validate_post_images(post_id)
        
        if "error" in result:
            print(f"  ❌ {result['error']}")
            continue
        
        total_images += result['total_images']
        total_working += result['working_images']
        total_broken += result['broken_images']
        
        status = "✅" if result['success_rate'] == 100 else "⚠️"
        print(f"  {status} Images: {result['working_images']}/{result['total_images']} working ({result['success_rate']:.1f}%)")
    
    print("\n" + "=" * 50)
    print("OVERALL SUMMARY:")
    print(f"Total images: {total_images}")
    print(f"Working images: {total_working}")
    print(f"Broken images: {total_broken}")
    
    if total_images > 0:
        overall_success = (total_working / total_images * 100)
        print(f"Overall success rate: {overall_success:.1f}%")
        
        if overall_success == 100:
            print("🎉 ALL IMAGES ARE WORKING!")
        elif overall_success >= 90:
            print("✅ Excellent image quality!")
        elif overall_success >= 80:
            print("⚠️ Good image quality, some issues remain")
        else:
            print("❌ Poor image quality, needs attention")
    else:
        print("No images found to validate")

if __name__ == "__main__":
    main()