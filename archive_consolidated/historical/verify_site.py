#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE SITE VERIFICATION TOOL
========================================
Verifies all optimizations and checks overall site health
"""

import requests
from requests.auth import HTTPBasicAuth
import getpass
from datetime import datetime
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print('='*50)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📊 {title}")
    print('-'*40)

def get_auth():
    """Get WordPress authentication"""
    print("🔐 AUTHENTICATION SETUP")
    print("="*30)
    username = input("Enter WordPress username: ")
    password = getpass.getpass("Enter application password: ")
    return HTTPBasicAuth(username, password)

def check_seo_compliance(content, title, url):
    """Check SEO compliance for a page"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Check for H2 headings
    h2_tags = soup.find_all('h2')
    h2_count = len(h2_tags)
    
    # Check for images
    img_tags = soup.find_all('img')
    img_count = len(img_tags)
    
    # Check title length
    title_length = len(title) if title else 0
    title_ok = title_length <= 60
    
    # Check for internal links
    links = soup.find_all('a', href=True)
    internal_links = [link for link in links if 'spherevista360.com' in link.get('href', '')]
    internal_link_count = len(internal_links)
    
    # Calculate SEO score
    score = 0
    max_score = 4
    
    if h2_count >= 2:
        score += 1
    if img_count >= 1:
        score += 1
    if title_ok:
        score += 1
    if internal_link_count >= 2:
        score += 1
    
    seo_score = (score / max_score) * 100
    
    return {
        'h2_count': h2_count,
        'img_count': img_count,
        'title_length': title_length,
        'title_ok': title_ok,
        'internal_links': internal_link_count,
        'seo_score': seo_score,
        'score_breakdown': f"{score}/{max_score}"
    }

def main():
    print_header("COMPREHENSIVE SITE VERIFICATION")
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get authentication
    auth = get_auth()
    base_url = "https://spherevista360.com/wp-json/wp/v2"
    
    print_section("1. CHECKING SEO OPTIMIZATION STATUS")
    
    try:
        # Get all posts
        posts_response = requests.get(f"{base_url}/posts?per_page=20", auth=auth)
        posts_response.raise_for_status()
        posts = posts_response.json()
        
        print(f"📄 Found {len(posts)} posts")
        
        entertainment_posts = []
        other_posts = []
        total_seo_score = 0
        post_count = 0
        
        for post in posts:
            # Get categories
            categories = []
            if post.get('categories'):
                for cat_id in post['categories']:
                    cat_response = requests.get(f"{base_url}/categories/{cat_id}", auth=auth)
                    if cat_response.status_code == 200:
                        cat_data = cat_response.json()
                        categories.append(cat_data['name'])
            
            # Get full content
            content_response = requests.get(f"https://spherevista360.com/?p={post['id']}")
            if content_response.status_code == 200:
                seo_data = check_seo_compliance(
                    content_response.text, 
                    post['title']['rendered'], 
                    post['link']
                )
                
                post_info = {
                    'title': post['title']['rendered'],
                    'categories': categories,
                    'seo_data': seo_data,
                    'url': post['link']
                }
                
                total_seo_score += seo_data['seo_score']
                post_count += 1
                
                if 'Entertainment' in categories:
                    entertainment_posts.append(post_info)
                else:
                    other_posts.append(post_info)
        
        # Display Entertainment posts
        print(f"\n🎭 ENTERTAINMENT CATEGORY POSTS ({len(entertainment_posts)}):")
        for i, post in enumerate(entertainment_posts, 1):
            seo = post['seo_data']
            print(f"   {i}. {post['title'][:50]}...")
            print(f"      📊 SEO Score: {seo['seo_score']:.1f}% ({seo['score_breakdown']})")
            print(f"      📝 H2 Headings: {seo['h2_count']}")
            print(f"      🖼️ Images: {seo['img_count']}")
            print(f"      📏 Title Length: {seo['title_length']}/60 {'✅' if seo['title_ok'] else '❌'}")
            print(f"      🔗 Internal Links: {seo['internal_links']}")
        
        # Display other posts sample
        print(f"\n📰 OTHER POSTS (showing first 3 of {len(other_posts)}):")
        for i, post in enumerate(other_posts[:3], 1):
            seo = post['seo_data']
            print(f"   {i}. {post['title'][:50]}...")
            print(f"      📊 SEO Score: {seo['seo_score']:.1f}% ({seo['score_breakdown']})")
        
        avg_seo_score = total_seo_score / post_count if post_count > 0 else 0
        print(f"\n📊 OVERALL SEO PERFORMANCE:")
        print(f"   📈 Average SEO Score: {avg_seo_score:.1f}%")
        print(f"   📄 Total Posts Analyzed: {post_count}")
        
    except Exception as e:
        print(f"❌ Error checking posts: {e}")
    
    print_section("2. CHECKING FOR DUPLICATE PAGES")
    
    try:
        # Get all pages
        pages_response = requests.get(f"{base_url}/pages?per_page=50", auth=auth)
        pages_response.raise_for_status()
        pages = pages_response.json()
        
        print(f"📄 Found {len(pages)} pages")
        
        # Check for duplicates by title similarity
        titles = {}
        duplicates = []
        
        for page in pages:
            title = page['title']['rendered']
            base_title = re.sub(r'\s*-\s*\d+\s*$', '', title)  # Remove -2, -3 suffixes
            
            if base_title in titles:
                duplicates.append({
                    'original': titles[base_title],
                    'duplicate': page
                })
            else:
                titles[base_title] = page
        
        if duplicates:
            print(f"🚨 Found {len(duplicates)} potential duplicate pairs:")
            for i, dup in enumerate(duplicates, 1):
                print(f"   {i}. Original: {dup['original']['title']['rendered']}")
                print(f"      Duplicate: {dup['duplicate']['title']['rendered']}")
        else:
            print("✅ No duplicate pages found!")
            
        # List all pages
        print(f"\n📋 ALL PAGES:")
        for i, page in enumerate(pages, 1):
            status = "✅ Published" if page['status'] == 'publish' else f"⚠️ {page['status']}"
            print(f"   {i}. {page['title']['rendered']} ({status})")
            
    except Exception as e:
        print(f"❌ Error checking pages: {e}")
    
    print_section("3. CHECKING SPECIFIC PAGE OPTIMIZATIONS")
    
    key_pages = ['newsletter', 'homepage']
    
    for page_slug in key_pages:
        try:
            # Get page by slug
            page_response = requests.get(f"{base_url}/pages?slug={page_slug}", auth=auth)
            page_response.raise_for_status()
            page_data = page_response.json()
            
            if page_data:
                page = page_data[0]
                print(f"\n📄 {page['title']['rendered'].upper()}:")
                
                # Get full page content
                content_response = requests.get(page['link'])
                if content_response.status_code == 200:
                    seo_data = check_seo_compliance(
                        content_response.text,
                        page['title']['rendered'],
                        page['link']
                    )
                    
                    print(f"   📊 SEO Score: {seo_data['seo_score']:.1f}%")
                    print(f"   📝 H2 Headings: {seo_data['h2_count']}")
                    print(f"   🖼️ Images: {seo_data['img_count']}")
                    print(f"   📏 Title: '{page['title']['rendered']}' ({seo_data['title_length']}/60)")
                    print(f"   🔗 Internal Links: {seo_data['internal_links']}")
                    print(f"   🌐 URL: {page['link']}")
                else:
                    print(f"   ❌ Could not access page content")
            else:
                print(f"❌ Page '{page_slug}' not found")
                
        except Exception as e:
            print(f"❌ Error checking {page_slug}: {e}")
    
    print_section("4. MENU VALIDATION")
    
    try:
        # Get menus
        menus_response = requests.get(f"{base_url}/menus", auth=auth)
        if menus_response.status_code == 200:
            menus = menus_response.json()
            
            # Find main menu
            main_menu = None
            for menu in menus:
                if 'main' in menu['name'].lower() or 'primary' in menu['name'].lower():
                    main_menu = menu
                    break
            
            if not main_menu and menus:
                main_menu = menus[0]  # Use first menu if no main menu found
            
            if main_menu:
                # Get menu items
                items_response = requests.get(f"{base_url}/menu-items?menus={main_menu['id']}", auth=auth)
                if items_response.status_code == 200:
                    items = items_response.json()
                    
                    print(f"🍔 Menu: {main_menu['name']} ({len(items)} items)")
                    
                    working_count = 0
                    total_count = len(items)
                    issues = []
                    
                    for item in items:
                        url = item.get('url', '')
                        title = item.get('title', 'Untitled')
                        
                        # Test URL accessibility
                        try:
                            if url:
                                response = requests.get(url, timeout=10)
                                if response.status_code == 200:
                                    status = "✅"
                                    working_count += 1
                                else:
                                    status = f"❌ {response.status_code}"
                                    issues.append(f"{title} → {url} (Status: {response.status_code})")
                            else:
                                status = "⚠️ No URL"
                                issues.append(f"{title} → No URL provided")
                        except Exception as e:
                            status = "❌ Error"
                            issues.append(f"{title} → {url} (Error: {str(e)[:30]}...)")
                        
                        print(f"   {status} {title}")
                        if url:
                            print(f"      → {url}")
                    
                    print(f"\n📊 Menu Status: {working_count}/{total_count} items working")
                    
                    if issues:
                        print(f"\n🚨 Issues Found:")
                        for issue in issues:
                            print(f"   ⚠️ {issue}")
                    else:
                        print("✅ All menu items working perfectly!")
                        
                else:
                    print("❌ Could not get menu items")
            else:
                print("❌ No main menu found")
        else:
            print("❌ Could not access menus API")
            
    except Exception as e:
        print(f"❌ Error checking menu: {e}")
    
    print_header("VERIFICATION COMPLETE")
    print("🎉 Site verification finished!")
    print("📋 Check the results above for any issues that need attention.")

if __name__ == "__main__":
    main()