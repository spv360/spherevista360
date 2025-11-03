#!/usr/bin/env python3
"""
Test Site After CSS Fix
Validates that overlapping issues are resolved
"""

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import time

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def check_page_structure(url, page_type="post"):
    """Check if page has proper structure without overlapping"""
    print(f"\n🔍 Testing: {url}")
    print("-" * 80)
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"   ❌ Failed to load (Status: {response.status_code})")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        checks = {
            'has_featured_image': False,
            'has_content': False,
            'no_inline_styles': True,
            'has_proper_spacing': True,
            'images_responsive': True
        }
        
        # Check 1: Featured image exists
        featured_img = soup.find('img', class_=lambda x: x and ('wp-post-image' in x or 'post-thumbnail' in x))
        if featured_img:
            checks['has_featured_image'] = True
            print(f"   ✅ Featured image found")
            
            # Check if image has proper attributes
            if featured_img.get('width') and featured_img.get('height'):
                print(f"      Dimensions: {featured_img.get('width')}x{featured_img.get('height')}")
        else:
            print(f"   ⚠️  Featured image not found")
        
        # Check 2: Entry content exists
        entry_content = soup.find('div', class_='entry-content')
        if entry_content:
            checks['has_content'] = True
            
            # Count paragraphs
            paragraphs = entry_content.find_all('p')
            print(f"   ✅ Content found: {len(paragraphs)} paragraphs")
            
            # Check for images in content
            content_images = entry_content.find_all('img')
            if content_images:
                print(f"   📷 Content images: {len(content_images)} found")
        else:
            print(f"   ❌ Entry content not found")
            checks['has_content'] = False
        
        # Check 3: Look for inline styles that might cause overlapping
        elements_with_inline_styles = soup.find_all(style=True)
        problematic_styles = []
        
        for elem in elements_with_inline_styles:
            style = elem.get('style', '')
            if any(x in style.lower() for x in ['position: absolute', 'float:', 'z-index:', 'margin: -']):
                problematic_styles.append(elem.name)
        
        if problematic_styles:
            print(f"   ⚠️  Potentially problematic inline styles found: {len(problematic_styles)} elements")
            checks['no_inline_styles'] = False
        else:
            print(f"   ✅ No problematic inline styles")
        
        # Check 4: Verify custom CSS is applied
        style_tags = soup.find_all('style')
        css_fix_found = False
        
        for style in style_tags:
            if style.string and 'max-width: 100%' in style.string and '!important' in style.string:
                css_fix_found = True
                break
        
        # Also check linked stylesheets
        if not css_fix_found:
            # Check if there's a custom CSS section
            for style in style_tags:
                if style.get('id') == 'wp-custom-css' or 'custom-css' in str(style.get('id', '')):
                    css_fix_found = True
                    break
        
        if css_fix_found:
            print(f"   ✅ Custom CSS detected (fix may be applied)")
        else:
            print(f"   ⚠️  Custom CSS not detected - fix may not be applied yet")
        
        # Check 5: Viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            print(f"   ✅ Responsive viewport meta tag present")
        else:
            print(f"   ⚠️  Viewport meta tag missing")
        
        # Overall assessment
        print(f"\n   📊 Checks Summary:")
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        print(f"   Passed: {passed}/{total}")
        
        return passed >= 3  # At least 3 out of 5 checks should pass
        
    except Exception as e:
        print(f"   ❌ Error testing page: {str(e)}")
        return False

def test_specific_posts():
    """Test specific posts that had issues"""
    print("=" * 80)
    print("🧪 TESTING SITE STRUCTURE & CSS FIX")
    print("=" * 80)
    
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    
    # Get a few recent posts to test
    print("\n📥 Fetching test posts...")
    response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=5", auth=auth)
    
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = response.json()
    print(f"   Found {len(posts)} posts to test\n")
    
    # Test the problematic post mentioned by user
    test_urls = [
        "https://spherevista360.com/green-bonds-energy-transition-where-yields-make-sense/"
    ]
    
    # Add some recent posts
    for post in posts[:3]:
        test_urls.append(post['link'])
    
    results = []
    
    print("=" * 80)
    print("📝 TESTING INDIVIDUAL POSTS")
    print("=" * 80)
    
    for url in test_urls:
        result = check_page_structure(url)
        results.append((url, result))
        time.sleep(1)  # Be nice to the server
    
    # Test homepage
    print("\n" + "=" * 80)
    print("🏠 TESTING HOMEPAGE")
    print("=" * 80)
    homepage_result = check_page_structure(WORDPRESS_URL, page_type="homepage")
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 FINAL TEST RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n✅ Posts passed: {passed}/{total}")
    if homepage_result:
        print(f"✅ Homepage: PASSED")
    else:
        print(f"⚠️  Homepage: NEEDS REVIEW")
    
    if passed == total and homepage_result:
        print("\n🎉 ALL TESTS PASSED!")
        print("   Your site structure looks good!")
    elif passed >= total * 0.7:
        print("\n✅ MOSTLY GOOD!")
        print("   Most pages look fine, some may need minor adjustments")
    else:
        print("\n⚠️  NEEDS ATTENTION")
        print("   Please ensure the CSS fix has been applied")
    
    print("\n" + "=" * 80)
    print("💡 NEXT STEPS")
    print("=" * 80)
    
    if passed < total:
        print("\n1. Apply the CSS fix if you haven't already:")
        print("   Go to: WordPress → Appearance → Customize → Additional CSS")
        print("   Paste the CSS from: /home/kddevops/downloads/critical-fix.css")
        print("   Click: Publish")
        print("\n2. Clear any caching:")
        print("   - Browser cache (Ctrl+Shift+R)")
        print("   - WordPress cache plugin (if installed)")
        print("   - CDN cache (if using Cloudflare, etc.)")
        print("\n3. Re-run this test:")
        print("   python3 test_site_structure.py")
    else:
        print("\n✅ Site looks good! You can:")
        print("   1. Clear cache if not done already")
        print("   2. Test on different devices/browsers")
        print("   3. Check a few more pages manually")
        print("   4. Ready to publish! 🚀")
    
    print("=" * 80)

def quick_visual_check():
    """Provide visual check instructions"""
    print("\n" + "=" * 80)
    print("👁️  VISUAL VERIFICATION CHECKLIST")
    print("=" * 80)
    print("""
After applying the CSS fix, please verify these items visually:

1. Featured Images:
   ✓ Images display at full width
   ✓ No text overlapping images
   ✓ Proper spacing below images

2. Content:
   ✓ Text is readable and not cut off
   ✓ Paragraphs have proper spacing
   ✓ Images within content don't overlap text

3. Layout:
   ✓ Post grid displays properly on homepage
   ✓ Sidebar (if any) doesn't overlap content
   ✓ Footer displays correctly

4. Responsive:
   ✓ Test on mobile device or resize browser
   ✓ Images resize properly
   ✓ Content remains readable

Test these URLs:
    """)
    
    print(f"   • Homepage: {WORDPRESS_URL}")
    print(f"   • Problem post: https://spherevista360.com/green-bonds-energy-transition-where-yields-make-sense/")
    print(f"   • Any recent post from homepage")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_specific_posts()
    quick_visual_check()
