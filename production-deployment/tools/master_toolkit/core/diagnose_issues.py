#!/usr/bin/env python3
"""
Diagnose Specific Issues on Problem Posts
"""

import requests
from bs4 import BeautifulSoup

def diagnose_post(url):
    """Detailed diagnosis of post issues"""
    print(f"\n{'='*80}")
    print(f"🔍 DIAGNOSING: {url}")
    print(f"{'='*80}\n")
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check 1: Featured Image
        print("1️⃣  FEATURED IMAGE CHECK")
        print("-" * 80)
        featured = soup.find('img', class_=lambda x: x and 'wp-post-image' in x)
        if featured:
            print(f"✅ Found: {featured.get('src', 'N/A')[:70]}")
            print(f"   Width attr: {featured.get('width', 'not set')}")
            print(f"   Height attr: {featured.get('height', 'not set')}")
            
            parent = featured.parent
            print(f"   Parent element: <{parent.name}> class='{parent.get('class', [])}'")
            
            # Check for inline styles
            if featured.get('style'):
                print(f"   ⚠️  Inline style: {featured.get('style')}")
            if parent.get('style'):
                print(f"   ⚠️  Parent style: {parent.get('style')}")
        else:
            print("❌ Featured image not found")
        
        # Check 2: Content Structure
        print(f"\n2️⃣  CONTENT STRUCTURE CHECK")
        print("-" * 80)
        entry_content = soup.find('div', class_='entry-content')
        if entry_content:
            # Count elements
            paragraphs = entry_content.find_all('p')
            headings = entry_content.find_all(['h1', 'h2', 'h3', 'h4'])
            lists = entry_content.find_all(['ul', 'ol'])
            links = entry_content.find_all('a')
            images = entry_content.find_all('img')
            
            print(f"✅ Entry content found")
            print(f"   Paragraphs: {len(paragraphs)}")
            print(f"   Headings: {len(headings)}")
            print(f"   Lists: {len(lists)}")
            print(f"   Links: {len(links)}")
            print(f"   Images: {len(images)}")
            
            # Check first paragraph
            if paragraphs:
                first_p = paragraphs[0]
                text = first_p.get_text()[:100]
                print(f"\n   First paragraph preview:")
                print(f"   '{text}...'")
                
                # Check for broken content
                if '<br' in str(first_p) and 'br />' in str(first_p):
                    print(f"   ⚠️  Contains manual line breaks")
                
                if first_p.get('style'):
                    print(f"   ⚠️  Has inline style: {first_p.get('style')}")
        else:
            print("❌ Entry content not found")
        
        # Check 3: CSS Applied
        print(f"\n3️⃣  CSS CHECK")
        print("-" * 80)
        
        # Look for custom CSS
        style_tags = soup.find_all('style')
        custom_css_found = False
        
        for style in style_tags:
            if style.string:
                if 'max-width: 100%' in style.string and '!important' in style.string:
                    custom_css_found = True
                    print(f"✅ Custom CSS detected in <style> tag")
                    break
        
        if not custom_css_found:
            # Check for inline styles that might interfere
            elements_with_styles = soup.find_all(style=True)
            print(f"⚠️  Custom fix CSS not detected")
            print(f"   Found {len(elements_with_styles)} elements with inline styles")
        
        # Check 4: Theme Detection
        print(f"\n4️⃣  THEME DETECTION")
        print("-" * 80)
        
        theme_links = soup.find_all('link', rel='stylesheet')
        for link in theme_links:
            href = link.get('href', '')
            if 'themes/' in href:
                theme_name = href.split('themes/')[-1].split('/')[0]
                print(f"✅ Theme detected: {theme_name}")
                break
        
        # Check 5: Specific Issues
        print(f"\n5️⃣  SPECIFIC ISSUE CHECK")
        print("-" * 80)
        
        # Check for overflow issues
        article = soup.find('article')
        if article and article.get('style'):
            if 'overflow' in article.get('style', ''):
                print(f"⚠️  Article has overflow style: {article.get('style')}")
        
        # Check for position absolute (causes overlapping)
        absolute_elements = soup.find_all(style=lambda x: x and 'position: absolute' in x)
        if absolute_elements:
            print(f"⚠️  Found {len(absolute_elements)} absolutely positioned elements")
            for elem in absolute_elements[:3]:
                print(f"      <{elem.name}> class='{elem.get('class', [])}' style='{elem.get('style')[:50]}...'")
        
        # Check for negative margins
        negative_margin_elements = soup.find_all(style=lambda x: x and 'margin: -' in x)
        if negative_margin_elements:
            print(f"⚠️  Found {len(negative_margin_elements)} elements with negative margins")
        
        print(f"\n{'='*80}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print("=" * 80)
    print("🔧 DETAILED POST DIAGNOSIS")
    print("=" * 80)
    print("\nAnalyzing specific issues you mentioned:")
    print("  • Post contents showing without formatting")
    print("  • Some content broken")
    print("  • Images overlapping")
    print("  • Featured images showing only half")
    print("")
    
    # Test the problem post
    diagnose_post("https://spherevista360.com/green-bonds-energy-transition-where-yields-make-sense/")
    
    # Test homepage
    diagnose_post("https://spherevista360.com/")
    
    print("\n" + "=" * 80)
    print("📋 RECOMMENDATIONS BASED ON DIAGNOSIS")
    print("=" * 80)
    print("""
Based on the diagnostic results above:

1. If featured images show "half":
   → Remove any max-height or height constraints
   → Use the improved-fix.css (simpler version)

2. If content formatting is broken:
   → Remove the aggressive CSS rules
   → Use only essential fixes

3. If still overlapping:
   → Check for theme-specific CSS conflicts
   → May need to adjust theme files directly

NEXT STEP: Use improved-fix.css instead of critical-fix.css
File: /home/kddevops/downloads/improved-fix.css

This version:
✅ Preserves all formatting
✅ Fixes overlapping issues
✅ No aggressive !important rules
✅ Works with theme CSS
    """)
    print("=" * 80)

if __name__ == "__main__":
    main()
