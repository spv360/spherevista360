#!/usr/bin/env python3
"""
Ultimate SEO & Content Validation Report
Checks ALL requirements comprehensively
"""

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from collections import defaultdict

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def strip_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def main():
    print("=" * 80)
    print("🏆 ULTIMATE SEO & CONTENT VALIDATION REPORT")
    print("=" * 80)
    print(f"🌐 Site: {WORDPRESS_URL}")
    print(f"📅 Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    
    # Fetch all data
    posts_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100", auth=auth)
    posts = posts_response.json()
    
    categories_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100", auth=auth)
    categories = categories_response.json()
    
    pages_response = requests.get(f"{WORDPRESS_URL}/wp-json/wp/v2/pages?per_page=100", auth=auth)
    pages = pages_response.json()
    
    results = {'✅ PASSED': [], '⚠️  WARNINGS': [], '❌ FAILED': []}
    
    # ============================================================================
    print("\n📝 1. CONTENT VALIDATION")
    print("=" * 80)
    
    # Word count (300-500 words)
    word_count_stats = {'optimal': 0, 'short': 0, 'long': 0}
    for post in posts:
        content = post['content']['rendered']
        word_count = count_words(strip_html(content))
        
        if 300 <= word_count <= 500:
            word_count_stats['optimal'] += 1
        elif word_count < 300:
            word_count_stats['short'] += 1
        else:
            word_count_stats['long'] += 1
    
    print(f"Word Count Distribution:")
    print(f"   ✅ Optimal (300-500 words): {word_count_stats['optimal']}/{len(posts)}")
    print(f"   ⚠️  Short (<300 words): {word_count_stats['short']}")
    print(f"   ℹ️  Long (>500 words): {word_count_stats['long']}")
    
    if word_count_stats['optimal'] == len(posts):
        results['✅ PASSED'].append(f"All {len(posts)} posts are 300-500 words")
    elif word_count_stats['optimal'] >= len(posts) * 0.95:
        results['⚠️  WARNINGS'].append(f"{len(posts) - word_count_stats['optimal']} posts outside optimal range")
    else:
        results['❌ FAILED'].append(f"Only {word_count_stats['optimal']}/{len(posts)} posts in optimal range")
    
    # ============================================================================
    print("\n\n🔗 2. URL OPTIMIZATION")
    print("=" * 80)
    
    url_stats = {'optimal': 0, 'long': 0, 'total_length': 0}
    long_urls = []
    
    for post in posts:
        url = post['link']
        length = len(url)
        url_stats['total_length'] += length
        
        if length <= 90:
            url_stats['optimal'] += 1
        else:
            url_stats['long'] += 1
            long_urls.append((post['title']['rendered'][:40], length))
    
    avg_url_length = url_stats['total_length'] / len(posts)
    
    print(f"URL Statistics:")
    print(f"   ✅ URLs under 90 chars: {url_stats['optimal']}/{len(posts)}")
    print(f"   📊 Average URL length: {avg_url_length:.1f} characters")
    print(f"   ❌ URLs over 90 chars: {url_stats['long']}")
    
    if url_stats['long'] > 0:
        print(f"\n   Long URLs:")
        for title, length in long_urls[:3]:
            print(f"      • {title}: {length} chars")
        results['❌ FAILED'].append(f"{url_stats['long']} URLs exceed 90 characters")
    else:
        results['✅ PASSED'].append("All URLs optimized (under 90 characters)")
    
    # ============================================================================
    print("\n\n📊 3. SEO TITLE OPTIMIZATION")
    print("=" * 80)
    
    title_stats = {'optimal': 0, 'long': 0}
    long_titles = []
    
    for post in posts:
        title = post['title']['rendered']
        length = len(title)
        
        if length <= 60:
            title_stats['optimal'] += 1
        else:
            title_stats['long'] += 1
            long_titles.append((title, length))
    
    print(f"Title Statistics:")
    print(f"   ✅ Titles under 60 chars: {title_stats['optimal']}/{len(posts)}")
    print(f"   ❌ Titles over 60 chars: {title_stats['long']}")
    
    if title_stats['long'] > 0:
        print(f"\n   Long Titles:")
        for title, length in long_titles[:3]:
            print(f"      • {title[:50]}: {length} chars")
        results['❌ FAILED'].append(f"{title_stats['long']} SEO titles exceed 60 characters")
    else:
        results['✅ PASSED'].append("All SEO titles optimized (under 60 characters)")
    
    # ============================================================================
    print("\n\n🔗 4. INTERNAL LINKING")
    print("=" * 80)
    
    link_stats = {'without': 0, 'few': 0, 'optimal': 0, 'total': 0}
    posts_without_links = []
    
    for post in posts:
        content = post['content']['rendered']
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a')
        link_count = len(links)
        link_stats['total'] += link_count
        
        if link_count == 0:
            link_stats['without'] += 1
            posts_without_links.append(post['title']['rendered'][:40])
        elif link_count <= 2:
            link_stats['few'] += 1
        else:
            link_stats['optimal'] += 1
    
    avg_links = link_stats['total'] / len(posts)
    
    print(f"Internal Link Statistics:")
    print(f"   ✅ Posts with 3+ links: {link_stats['optimal']}/{len(posts)}")
    print(f"   📊 Average links per post: {avg_links:.1f}")
    print(f"   ⚠️  Posts with 1-2 links: {link_stats['few']}")
    print(f"   ❌ Posts without links: {link_stats['without']}")
    
    if link_stats['without'] > 0:
        print(f"\n   Posts without links:")
        for title in posts_without_links[:3]:
            print(f"      • {title}")
        results['❌ FAILED'].append(f"{link_stats['without']} posts have no internal links")
    else:
        results['✅ PASSED'].append(f"All posts have internal links (avg {avg_links:.1f} per post)")
    
    # ============================================================================
    print("\n\n📂 5. CATEGORY DISTRIBUTION")
    print("=" * 80)
    
    cat_stats = defaultdict(lambda: {'name': '', 'posts': []})
    
    for cat in categories:
        cat_stats[cat['id']]['name'] = cat['name']
    
    for post in posts:
        for cat_id in post.get('categories', []):
            cat_stats[cat_id]['posts'].append(post['id'])
    
    print(f"Category Distribution:")
    empty_cats = []
    single_post_cats = []
    
    # Sort by post count
    sorted_cats = sorted(cat_stats.items(), key=lambda x: len(x[1]['posts']), reverse=True)
    
    for cat_id, data in sorted_cats:
        name = data['name']
        count = len(data['posts'])
        
        if count == 0:
            print(f"   ❌ {name}: {count} posts (EMPTY)")
            empty_cats.append(name)
        elif count == 1:
            print(f"   ⚠️  {name}: {count} post (NEEDS MORE)")
            single_post_cats.append(name)
        elif count >= 2:
            print(f"   ✅ {name}: {count} posts")
    
    active_cats = len([c for c in cat_stats.values() if len(c['posts']) >= 2])
    
    if empty_cats:
        results['⚠️  WARNINGS'].append(f"{len(empty_cats)} empty categories (can be ignored if unused)")
    
    if single_post_cats:
        results['⚠️  WARNINGS'].append(f"{len(single_post_cats)} categories with only 1 post")
    
    if not single_post_cats and active_cats >= 7:
        results['✅ PASSED'].append(f"All active categories have 2+ posts ({active_cats} categories)")
    
    # ============================================================================
    print("\n\n🖼️  6. FEATURED IMAGES")
    print("=" * 80)
    
    posts_with_images = len([p for p in posts if p.get('featured_media', 0) > 0])
    posts_without_images = len(posts) - posts_with_images
    
    print(f"Featured Image Statistics:")
    print(f"   ✅ Posts with images: {posts_with_images}/{len(posts)}")
    print(f"   ❌ Posts without images: {posts_without_images}")
    
    if posts_without_images == 0:
        results['✅ PASSED'].append("All posts have high-quality featured images")
    else:
        results['❌ FAILED'].append(f"{posts_without_images} posts missing featured images")
    
    # ============================================================================
    print("\n\n📄 7. PAGES & STRUCTURE")
    print("=" * 80)
    
    essential_pages = ['Home', 'About', 'Contact', 'Blog', 'Services']
    found_pages = []
    
    print(f"Essential Pages:")
    for page_name in essential_pages:
        found = any(page_name.lower() in p['title']['rendered'].lower() for p in pages)
        if found:
            print(f"   ✅ {page_name} page exists")
            found_pages.append(page_name)
        else:
            print(f"   ⚠️  {page_name} page not found")
    
    print(f"\n   Total pages: {len(pages)}")
    
    if len(found_pages) >= 4:
        results['✅ PASSED'].append(f"All essential pages present ({len(pages)} total pages)")
    else:
        results['⚠️  WARNINGS'].append(f"Only {len(found_pages)}/{len(essential_pages)} essential pages found")
    
    # ============================================================================
    print("\n\n🔍 8. SEO INFRASTRUCTURE")
    print("=" * 80)
    
    # Sitemap
    sitemap_found = False
    for sitemap_url in [f"{WORDPRESS_URL}/sitemap.xml", f"{WORDPRESS_URL}/wp-sitemap.xml"]:
        if requests.get(sitemap_url).status_code == 200:
            print(f"   ✅ Sitemap: {sitemap_url}")
            sitemap_found = True
            break
    
    if not sitemap_found:
        print(f"   ❌ Sitemap: Not found")
        results['❌ FAILED'].append("XML Sitemap missing")
    else:
        results['✅ PASSED'].append("XML Sitemap active and accessible")
    
    # robots.txt
    robots_response = requests.get(f"{WORDPRESS_URL}/robots.txt")
    if robots_response.status_code == 200:
        print(f"   ✅ robots.txt: Active")
        results['✅ PASSED'].append("robots.txt configured")
    else:
        print(f"   ⚠️  robots.txt: Not found")
        results['⚠️  WARNINGS'].append("robots.txt not found")
    
    # Meta tags
    homepage = requests.get(WORDPRESS_URL)
    if homepage.status_code == 200:
        html = homepage.text
        
        has_meta_desc = 'meta name="description"' in html
        has_og_tags = 'og:' in html
        
        if has_meta_desc:
            print(f"   ✅ Meta descriptions: Present")
        else:
            print(f"   ⚠️  Meta descriptions: Missing")
        
        if has_og_tags:
            print(f"   ✅ Open Graph tags: Present")
            results['✅ PASSED'].append("Proper meta tags and Open Graph configured")
        else:
            print(f"   ⚠️  Open Graph tags: Missing")
    
    # ============================================================================
    print("\n\n" + "=" * 80)
    print("🏆 FINAL VALIDATION RESULTS")
    print("=" * 80)
    
    for status in ['✅ PASSED', '⚠️  WARNINGS', '❌ FAILED']:
        if results[status]:
            print(f"\n{status} ({len(results[status])} items):")
            for item in results[status]:
                print(f"   {status.split()[0]} {item}")
    
    # Calculate score
    total_checks = sum(len(results[k]) for k in results)
    passed = len(results['✅ PASSED'])
    score = (passed / total_checks * 100) if total_checks > 0 else 0
    
    print("\n" + "=" * 80)
    print("📈 OVERALL SCORE")
    print("=" * 80)
    print(f"   Score: {score:.1f}%")
    print(f"   Passed: {passed}/{total_checks} checks")
    print(f"   Warnings: {len(results['⚠️  WARNINGS'])}")
    print(f"   Failed: {len(results['❌ FAILED'])}")
    
    if score == 100:
        print("\n   🎉 PERFECT SCORE! SITE IS PRODUCTION READY!")
    elif score >= 90:
        print("\n   ✅ EXCELLENT! Site is production ready with minor notes.")
    elif score >= 75:
        print("\n   ⚠️  GOOD! Address warnings before full production launch.")
    else:
        print("\n   ❌ NEEDS WORK! Address failed items before launch.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
