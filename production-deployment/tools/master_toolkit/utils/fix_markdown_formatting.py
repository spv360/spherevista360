#!/usr/bin/env python3
"""
Fix posts with markdown formatting stored as plain text
Convert markdown to proper HTML
"""

import os
import requests
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL', 'https://spherevista360.com')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def convert_markdown_to_html(content):
    """Convert markdown syntax to proper HTML"""
    if not content:
        return content
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all paragraphs
    for p in soup.find_all('p'):
        text = p.get_text()
        
        # Check if paragraph contains markdown headers
        if text.strip().startswith('###'):
            # H3
            new_tag = soup.new_tag('h3')
            new_tag.string = text.replace('###', '').strip()
            p.replace_with(new_tag)
        elif text.strip().startswith('##'):
            # H2
            new_tag = soup.new_tag('h2')
            new_tag.string = text.replace('##', '').strip()
            p.replace_with(new_tag)
        elif text.strip().startswith('#'):
            # H1
            new_tag = soup.new_tag('h1')
            new_tag.string = text.replace('#', '').strip()
            p.replace_with(new_tag)
        elif '**' in text:
            # Bold text
            # Replace **text** with <strong>text</strong>
            new_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', str(p))
            new_soup = BeautifulSoup(new_html, 'html.parser')
            p.replace_with(new_soup.p)
    
    return str(soup)

def fix_all_posts():
    """Fix all posts with markdown formatting"""
    print("=" * 80)
    print("🔧 FIXING MARKDOWN FORMATTING")
    print("=" * 80)
    print()
    
    # Get all posts
    page = 1
    all_posts = []
    
    while True:
        response = requests.get(
            f'{WORDPRESS_URL}/wp-json/wp/v2/posts',
            params={'per_page': 100, 'page': page},
            auth=(USERNAME, PASSWORD)
        )
        
        if not response.ok:
            break
        
        posts = response.json()
        if not posts:
            break
        
        all_posts.extend(posts)
        page += 1
    
    print(f"📊 Found {len(all_posts)} posts to check")
    print()
    
    fixed_count = 0
    skipped_count = 0
    
    for post in all_posts:
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        # Check if content has markdown syntax
        has_markdown = any([
            '<p>#' in content,
            '<p>##' in content,
            '<p>###' in content,
            '**' in content and '–' in content  # Bold with list items
        ])
        
        if not has_markdown:
            skipped_count += 1
            continue
        
        print(f"🔧 Fixing: {title[:60]}...")
        
        # Convert markdown to HTML
        fixed_content = convert_markdown_to_html(content)
        
        # Update the post
        update_data = {
            'content': fixed_content
        }
        
        response = requests.post(
            f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
            json=update_data,
            auth=(USERNAME, PASSWORD)
        )
        
        if response.ok:
            print(f"   ✅ Fixed markdown formatting")
            fixed_count += 1
        else:
            print(f"   ❌ Failed: {response.status_code}")
    
    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Posts fixed: {fixed_count}")
    print(f"⏭️  Posts skipped: {skipped_count}")
    print(f"📝 Total posts: {len(all_posts)}")
    print()

if __name__ == '__main__':
    fix_all_posts()
