#!/usr/bin/env python3
"""
Add Relevant Internal Links to Posts
Intelligently adds contextual internal links to posts that don't have any
"""

import requests
from bs4 import BeautifulSoup
import re

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

# Mapping of keywords to related post slugs for internal linking
LINK_MAPPING = {
    'ai': ['ai-investment-management', 'ai-politics-reshaping-democracy', 'ai-powered-investment-strategies'],
    'cloud': ['cloud-wars-2025', 'cloud-computing-ai-infrastructure', 'cloud-computing-evolution'],
    'cybersecurity': ['cybersecurity-age-ai-automation', 'data-privacy-future', 'digital-identity-global'],
    'finance': ['digital-banking-revolution', 'ai-investment-management', 'startup-funding-landscape'],
    'investment': ['ai-powered-investment-strategies', 'startup-funding-landscape', 'green-bonds-energy-transition'],
    'technology': ['tech-innovation-2025', 'generative-ai-tools', 'digital-banking-revolution'],
    'data': ['product-analytics-2025', 'data-privacy-future'],
    'digital': ['digital-banking-revolution', 'digital-nomad-visas', 'digital-identity-global'],
    'trade': ['us-india-trade-relations', 'supply-chain-reshoring'],
    'election': ['global-elections-2025', 'ai-politics-reshaping-democracy'],
}

def get_all_posts():
    """Get all posts with their content"""
    all_posts = []
    page = 1
    
    while True:
        response = requests.get(
            f'{WORDPRESS_URL}/wp-json/wp/v2/posts',
            params={'per_page': 100, 'page': page},
            auth=(USERNAME, PASSWORD)
        )
        
        if not response.ok or not response.json():
            break
        
        all_posts.extend(response.json())
        page += 1
    
    return all_posts

def get_posts_without_internal_links(posts):
    """Identify posts without internal links"""
    posts_without_links = []
    
    for post in posts:
        content = post['content']['rendered']
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for internal links
        internal_links = soup.find_all('a', href=re.compile(r'spherevista360\.com'))
        
        if len(internal_links) == 0:
            posts_without_links.append(post)
    
    return posts_without_links

def find_related_posts(post, all_posts):
    """Find related posts based on content keywords"""
    title = post['title']['rendered'].lower()
    content = BeautifulSoup(post['content']['rendered'], 'html.parser').get_text().lower()
    combined = title + " " + content
    
    related = []
    
    # Match keywords to find related posts
    for keyword, slugs in LINK_MAPPING.items():
        if keyword in combined:
            for slug in slugs:
                # Find the actual post
                for p in all_posts:
                    if p['slug'] == slug and p['id'] != post['id']:
                        related.append({
                            'id': p['id'],
                            'title': BeautifulSoup(p['title']['rendered'], 'html.parser').get_text(),
                            'slug': p['slug'],
                            'url': p['link']
                        })
                        break
    
    # Remove duplicates
    seen = set()
    unique_related = []
    for r in related:
        if r['slug'] not in seen:
            seen.add(r['slug'])
            unique_related.append(r)
    
    return unique_related[:3]  # Return top 3 related posts

def add_internal_links_to_post(post, related_posts):
    """Add internal links to post content"""
    if not related_posts:
        return None
    
    content = post['content']['rendered']
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the last paragraph
    paragraphs = soup.find_all('p')
    if not paragraphs:
        return None
    
    # Create "Related Reading" section
    related_section = soup.new_tag('div', **{'class': 'related-reading'})
    related_section['style'] = 'margin-top: 2rem; padding: 1.5rem; background: #f8f9fa; border-left: 4px solid #0073aa; border-radius: 4px;'
    
    heading = soup.new_tag('h3')
    heading['style'] = 'margin-top: 0; color: #0073aa; font-size: 1.2rem;'
    heading.string = '📚 Related Reading'
    related_section.append(heading)
    
    ul = soup.new_tag('ul')
    ul['style'] = 'margin: 1rem 0 0 0; padding-left: 1.5rem;'
    
    for related in related_posts:
        li = soup.new_tag('li')
        li['style'] = 'margin-bottom: 0.5rem;'
        
        link = soup.new_tag('a', href=related['url'])
        link['style'] = 'color: #0073aa; text-decoration: none; font-weight: 500;'
        link.string = related['title']
        
        li.append(link)
        ul.append(li)
    
    related_section.append(ul)
    
    # Add after the last paragraph
    paragraphs[-1].insert_after(related_section)
    
    return str(soup)

def update_post_content(post_id, new_content):
    """Update post with new content"""
    response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
        json={'content': new_content},
        auth=(USERNAME, PASSWORD)
    )
    
    return response.ok

def main():
    print("=" * 80)
    print("🔗 ADDING INTERNAL LINKS TO POSTS")
    print("=" * 80)
    print()
    
    # Get all posts
    print("📊 Fetching all posts...")
    all_posts = get_all_posts()
    print(f"   Found {len(all_posts)} total posts")
    print()
    
    # Find posts without internal links
    print("🔍 Identifying posts without internal links...")
    posts_without_links = get_posts_without_internal_links(all_posts)
    print(f"   Found {len(posts_without_links)} posts without internal links")
    print()
    
    if not posts_without_links:
        print("✅ All posts already have internal links!")
        return
    
    # Process each post
    print("=" * 80)
    print("📝 ADDING LINKS TO POSTS")
    print("=" * 80)
    print()
    
    updated_count = 0
    skipped_count = 0
    
    for idx, post in enumerate(posts_without_links[:10], 1):  # Process first 10
        post_id = post['id']
        title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text()
        
        print(f"[{idx}/10] 📝 {title[:60]}...")
        
        # Find related posts
        related_posts = find_related_posts(post, all_posts)
        
        if not related_posts:
            print(f"        ⚠️  No related posts found")
            skipped_count += 1
            print()
            continue
        
        print(f"        🔍 Found {len(related_posts)} related posts:")
        for rp in related_posts:
            print(f"           → {rp['title'][:50]}...")
        
        # Add internal links
        new_content = add_internal_links_to_post(post, related_posts)
        
        if not new_content:
            print(f"        ❌ Could not add links")
            skipped_count += 1
            print()
            continue
        
        # Update post
        success = update_post_content(post_id, new_content)
        
        if success:
            print(f"        ✅ Added {len(related_posts)} internal links")
            updated_count += 1
        else:
            print(f"        ❌ Failed to update post")
            skipped_count += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Posts updated: {updated_count}")
    print(f"⚠️  Posts skipped: {skipped_count}")
    print(f"📝 Total processed: {updated_count + skipped_count}")
    print()
    
    if updated_count > 0:
        print("✨ Internal links successfully added!")
        print()
        print("📈 BENEFITS:")
        print("   • Improved SEO (internal linking)")
        print("   • Better user engagement")
        print("   • Increased pageviews")
        print("   • Lower bounce rate")
        print()
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
