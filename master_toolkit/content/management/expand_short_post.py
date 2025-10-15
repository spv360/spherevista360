#!/usr/bin/env python3
"""
Expand Short Post: Cloud Computing AI Infrastructure Focus
Add concluding content to reach 300+ words
"""

import requests
from bs4 import BeautifulSoup

WORDPRESS_URL = 'https://spherevista360.com'
USERNAME = 'JK'
PASSWORD = 'R8sj tOZG 8ORr ntSZ XlPt qTE9'

def expand_short_post():
    """Expand the Cloud Computing post to meet word count"""
    print("=" * 80)
    print("📝 EXPANDING SHORT POST")
    print("=" * 80)
    print()
    
    # Find the specific post by ID (slug was incorrect: visa-free-destinations-2025)
    post_id = 1952
    response = requests.get(
        f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
        auth=(USERNAME, PASSWORD)
    )
    
    if not response.ok:
        print("❌ Post not found")
        return
    
    post = response.json()
    title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text()
    content = post['content']['rendered']
    
    print(f"📝 Post: {title}")
    print()
    
    # Count current words
    soup = BeautifulSoup(content, 'html.parser')
    current_text = soup.get_text()
    current_word_count = len(current_text.split())
    
    print(f"📊 Current word count: {current_word_count}")
    print()
    
    if current_word_count >= 300:
        print(f"✅ Post already has {current_word_count} words (target: 300+)")
        return
    
    # Add concluding paragraph before the related reading section
    additional_content = """
<h3>Looking Ahead: The Future of Cloud-Based AI</h3>

<p>As we move forward into 2025 and beyond, the convergence of cloud computing and artificial intelligence will continue to reshape how businesses operate and innovate. Organizations that strategically invest in cloud-based AI infrastructure today are positioning themselves at the forefront of tomorrow's digital economy. The key to success lies in choosing the right cloud platform, implementing robust data governance, and maintaining a forward-thinking approach to AI adoption. Whether you're a startup or an enterprise, the cloud-AI ecosystem offers unprecedented opportunities for growth, innovation, and competitive advantage.</p>
"""
    
    # Find where to insert (before related reading section if it exists, otherwise at the end)
    related_div = soup.find('div', class_='related-reading')
    
    if related_div:
        # Insert before related reading
        new_content_soup = BeautifulSoup(additional_content, 'html.parser')
        related_div.insert_before(new_content_soup)
    else:
        # Append at the end
        soup.append(BeautifulSoup(additional_content, 'html.parser'))
    
    new_content = str(soup)
    
    # Count new words
    new_soup = BeautifulSoup(new_content, 'html.parser')
    new_text = new_soup.get_text()
    new_word_count = len(new_text.split())
    
    print(f"📈 Adding content...")
    print(f"   New word count: {new_word_count}")
    print(f"   Added: {new_word_count - current_word_count} words")
    print()
    
    # Update the post
    update_response = requests.post(
        f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}',
        json={'content': new_content},
        auth=(USERNAME, PASSWORD)
    )
    
    if update_response.ok:
        print("✅ Post successfully expanded!")
        print()
        print(f"   Before: {current_word_count} words")
        print(f"   After: {new_word_count} words")
        print(f"   Status: {'✅ Above 300 words!' if new_word_count >= 300 else '⚠️ Still below 300'}")
        print()
    else:
        print(f"❌ Failed to update post: {update_response.status_code}")
        print()
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    expand_short_post()
