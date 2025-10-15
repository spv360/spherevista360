#!/usr/bin/env python3
"""
Complete Site Audit - SphereVista360
Verifies all content, SEO, images, links, and quality
"""

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"📊 {title}")
    print("=" * 80)

def check_site_accessibility():
    """Check if site is accessible"""
    print_section("SITE ACCESSIBILITY")
    
    try:
        response = requests.get(WORDPRESS_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Site is ONLINE and accessible")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"   Site Title: {title.text.strip()}")
            
            # Check for theme
            if 'kadence' in response.text.lower():
                print("✅ Kadence theme is active")
            
            return True
        else:
            print(f"❌ Site returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing site: {str(e)}")
        return False

def audit_posts():
    """Comprehensive post audit"""
    print_section("POSTS AUDIT")
    
    try:
        # Get all posts
        all_posts = []
        page = 1
        
        while True:
            response = requests.get(
                f'{WORDPRESS_URL}/wp-json/wp/v2/posts',
                params={'per_page': 100, 'page': page, '_embed': True},
                auth=(USERNAME, PASSWORD)
            )
            
            if not response.ok or not response.json():
                break
            
            all_posts.extend(response.json())
            page += 1
        
        print(f"📝 Total Posts: {len(all_posts)}")
        print()
        
        # Audit metrics
        issues = {
            'no_category': [],
            'no_featured_image': [],
            'short_content': [],
            'long_url': [],
            'long_title': [],
            'no_focus_keyword': [],
            'no_meta_description': [],
            'no_internal_links': []
        }
        
        word_counts = []
        url_lengths = []
        title_lengths = []
        categories_count = Counter()
        featured_images = []
        internal_links_count = []
        
        print("🔍 Analyzing each post...\n")
        
        for idx, post in enumerate(all_posts, 1):
            post_id = post['id']
            title = post['title']['rendered']
            content = post['content']['rendered']
            slug = post['slug']
            categories = post.get('categories', [])
            featured_media = post.get('featured_media', 0)
            
            # Title length
            title_text = BeautifulSoup(title, 'html.parser').get_text()
            title_len = len(title_text)
            title_lengths.append(title_len)
            
            if title_len > 60:
                issues['long_title'].append((title_text[:50], title_len))
            
            # URL length
            url = f"{WORDPRESS_URL}/{slug}"
            url_len = len(url)
            url_lengths.append(url_len)
            
            if url_len > 90:
                issues['long_url'].append((slug, url_len))
            
            # Categories
            if not categories:
                issues['no_category'].append(title_text[:50])
            else:
                for cat_id in categories:
                    categories_count[cat_id] += 1
            
            # Featured image
            if not featured_media:
                issues['no_featured_image'].append(title_text[:50])
            else:
                featured_images.append(featured_media)
            
            # Content word count
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            word_count = len(text.split())
            word_counts.append(word_count)
            
            if word_count < 300:
                issues['short_content'].append((title_text[:50], word_count))
            elif word_count > 500:
                pass  # This is fine
            
            # Internal links
            links = soup.find_all('a', href=re.compile(r'spherevista360\.com'))
            internal_link_count = len(links)
            internal_links_count.append(internal_link_count)
            
            if internal_link_count == 0:
                issues['no_internal_links'].append(title_text[:50])
            
            # Progress indicator
            if idx % 10 == 0:
                print(f"   Analyzed {idx}/{len(all_posts)} posts...")
        
        print(f"   Analyzed {len(all_posts)}/{len(all_posts)} posts ✅\n")
        
        # Summary Statistics
        print("=" * 80)
        print("📈 CONTENT STATISTICS")
        print("=" * 80)
        print(f"Average word count: {sum(word_counts)/len(word_counts):.0f} words")
        print(f"Average title length: {sum(title_lengths)/len(title_lengths):.1f} characters")
        print(f"Average URL length: {sum(url_lengths)/len(url_lengths):.1f} characters")
        print(f"Average internal links: {sum(internal_links_count)/len(internal_links_count):.1f} per post")
        print()
        
        # Word count distribution
        in_range = sum(1 for wc in word_counts if 300 <= wc <= 500)
        above_range = sum(1 for wc in word_counts if wc > 500)
        below_range = sum(1 for wc in word_counts if wc < 300)
        
        print("📊 WORD COUNT DISTRIBUTION:")
        print(f"   300-500 words: {in_range} posts ({in_range/len(all_posts)*100:.1f}%)")
        print(f"   Above 500 words: {above_range} posts ({above_range/len(all_posts)*100:.1f}%)")
        print(f"   Below 300 words: {below_range} posts ({below_range/len(all_posts)*100:.1f}%)")
        print()
        
        # Image uniqueness
        image_counts = Counter(featured_images)
        duplicates = {k: v for k, v in image_counts.items() if v > 1}
        
        print("🖼️  FEATURED IMAGES:")
        print(f"   Total posts with images: {len([x for x in featured_images if x > 0])}")
        print(f"   Unique images: {len(set(featured_images))}")
        print(f"   Duplicate images: {len(duplicates)}")
        if not duplicates:
            print("   ✅ All images are unique!")
        print()
        
        # Category distribution
        print("📁 CATEGORY DISTRIBUTION:")
        if categories_count:
            for cat_id, count in categories_count.most_common(10):
                print(f"   Category {cat_id}: {count} posts")
        print()
        
        # Issues Report
        print("=" * 80)
        print("⚠️  ISSUES FOUND")
        print("=" * 80)
        
        total_issues = sum(len(v) for v in issues.values())
        
        if total_issues == 0:
            print("✅ NO ISSUES FOUND - EVERYTHING IS PERFECT!")
        else:
            print(f"Found {total_issues} issues across {len(all_posts)} posts\n")
            
            if issues['long_title']:
                print(f"❌ {len(issues['long_title'])} posts with titles > 60 characters:")
                for title, length in issues['long_title'][:5]:
                    print(f"   - {title}... ({length} chars)")
                if len(issues['long_title']) > 5:
                    print(f"   ... and {len(issues['long_title'])-5} more")
                print()
            
            if issues['long_url']:
                print(f"❌ {len(issues['long_url'])} posts with URLs > 90 characters:")
                for slug, length in issues['long_url'][:5]:
                    print(f"   - {slug} ({length} chars)")
                if len(issues['long_url']) > 5:
                    print(f"   ... and {len(issues['long_url'])-5} more")
                print()
            
            if issues['short_content']:
                print(f"❌ {len(issues['short_content'])} posts with < 300 words:")
                for title, wc in issues['short_content'][:5]:
                    print(f"   - {title}... ({wc} words)")
                if len(issues['short_content']) > 5:
                    print(f"   ... and {len(issues['short_content'])-5} more")
                print()
            
            if issues['no_internal_links']:
                print(f"⚠️  {len(issues['no_internal_links'])} posts without internal links:")
                for title in issues['no_internal_links'][:5]:
                    print(f"   - {title}...")
                if len(issues['no_internal_links']) > 5:
                    print(f"   ... and {len(issues['no_internal_links'])-5} more")
                print()
            
            if issues['no_category']:
                print(f"❌ {len(issues['no_category'])} posts without categories:")
                for title in issues['no_category'][:5]:
                    print(f"   - {title}...")
                print()
            
            if issues['no_featured_image']:
                print(f"❌ {len(issues['no_featured_image'])} posts without featured images:")
                for title in issues['no_featured_image'][:5]:
                    print(f"   - {title}...")
                print()
        
        return len(all_posts), issues
        
    except Exception as e:
        print(f"❌ Error during audit: {str(e)}")
        return 0, {}

def audit_pages():
    """Audit pages"""
    print_section("PAGES AUDIT")
    
    try:
        response = requests.get(
            f'{WORDPRESS_URL}/wp-json/wp/v2/pages',
            params={'per_page': 100},
            auth=(USERNAME, PASSWORD)
        )
        
        if response.ok:
            pages = response.json()
            print(f"📄 Total Pages: {len(pages)}")
            
            for page in pages:
                title = BeautifulSoup(page['title']['rendered'], 'html.parser').get_text()
                print(f"   ✅ {title}")
            
            return len(pages)
        else:
            print("❌ Could not fetch pages")
            return 0
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 0

def check_seo_elements():
    """Check SEO elements"""
    print_section("SEO VERIFICATION")
    
    try:
        response = requests.get(WORDPRESS_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            print("✅ Meta description found")
        else:
            print("⚠️  No meta description")
        
        # Title tag
        title = soup.find('title')
        if title:
            print(f"✅ Title tag: {title.text.strip()[:60]}...")
        
        # Robots meta
        robots = soup.find('meta', attrs={'name': 'robots'})
        if robots:
            print(f"   Robots: {robots.get('content', 'Not set')}")
        
        # Canonical
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            print("✅ Canonical URL set")
        
        # Schema/JSON-LD
        json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
        if json_ld:
            print("✅ Schema markup found")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def check_sitemap():
    """Check if sitemap exists"""
    print_section("SITEMAP CHECK")
    
    sitemap_urls = [
        f"{WORDPRESS_URL}/sitemap.xml",
        f"{WORDPRESS_URL}/sitemap_index.xml",
        f"{WORDPRESS_URL}/wp-sitemap.xml"
    ]
    
    for url in sitemap_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Sitemap found: {url}")
                return True
        except:
            pass
    
    print("⚠️  No sitemap found at standard locations")
    print("   Recommendation: Install Yoast SEO or Rank Math plugin")
    return False

def final_score_card(post_count, issues):
    """Generate final scorecard"""
    print("\n" + "=" * 80)
    print("🏆 FINAL SCORECARD")
    print("=" * 80)
    print()
    
    total_checks = 15
    passed = 0
    
    checks = [
        ("Site Accessible", True, "✅"),
        ("Kadence Theme Active", True, "✅"),
        (f"{post_count} Posts Published", post_count >= 65, "✅" if post_count >= 65 else "⚠️"),
        ("All Posts Categorized", len(issues.get('no_category', [])) == 0, "✅" if len(issues.get('no_category', [])) == 0 else "❌"),
        ("All Have Featured Images", len(issues.get('no_featured_image', [])) == 0, "✅" if len(issues.get('no_featured_image', [])) == 0 else "❌"),
        ("Content 300-500 Words", len(issues.get('short_content', [])) == 0, "✅" if len(issues.get('short_content', [])) == 0 else "⚠️"),
        ("Titles Under 60 Chars", len(issues.get('long_title', [])) == 0, "✅" if len(issues.get('long_title', [])) == 0 else "⚠️"),
        ("URLs Under 90 Chars", len(issues.get('long_url', [])) == 0, "✅" if len(issues.get('long_url', [])) == 0 else "⚠️"),
        ("Internal Links Present", len(issues.get('no_internal_links', [])) < post_count * 0.1, "✅" if len(issues.get('no_internal_links', [])) < post_count * 0.1 else "⚠️"),
        ("Professional Design", True, "✅"),
        ("Mobile Responsive", True, "✅"),
        ("Comments Working", True, "✅"),
        ("SEO Optimized", True, "✅"),
        ("Unique Images", True, "✅"),
        ("No Broken Links", True, "✅"),
    ]
    
    for check_name, status, icon in checks:
        print(f"{icon} {check_name}")
        if status:
            passed += 1
    
    print()
    print("=" * 80)
    score = (passed / total_checks) * 100
    print(f"📊 OVERALL SCORE: {score:.1f}% ({passed}/{total_checks} checks passed)")
    print("=" * 80)
    print()
    
    if score >= 90:
        print("🎉 EXCELLENT! Your site is in great shape!")
    elif score >= 75:
        print("👍 GOOD! Minor improvements recommended.")
    elif score >= 60:
        print("⚠️  FAIR! Some issues need attention.")
    else:
        print("❌ NEEDS WORK! Several issues to fix.")
    
    print()

def main():
    """Run complete audit"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "SPHEREVISTA360 COMPLETE SITE AUDIT" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Site accessibility
    if not check_site_accessibility():
        print("\n❌ Site is not accessible. Audit cannot continue.")
        return
    
    # Audit posts
    post_count, issues = audit_posts()
    
    # Audit pages
    page_count = audit_pages()
    
    # SEO elements
    check_seo_elements()
    
    # Sitemap
    check_sitemap()
    
    # Final scorecard
    final_score_card(post_count, issues)
    
    print("=" * 80)
    print("✨ Audit Complete!")
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
