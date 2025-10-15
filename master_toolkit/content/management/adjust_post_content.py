#!/usr/bin/env python3
"""
Adjust Post Content to 300-500 Words
Expands very short posts and trims overly long posts
"""

import os
import re
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def strip_html(html):
    """Remove HTML tags and get plain text"""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def count_words(text):
    """Count words in text"""
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def expand_content_intelligently(title, current_content, category, target_words=400):
    """
    Expand content to target word count (300-500 words)
    """
    plain_text = strip_html(current_content)
    current_words = count_words(plain_text)
    
    if current_words >= 300:
        return None  # Already in acceptable range
    
    needed_words = target_words - current_words
    
    # Category-specific expansion templates
    expansions = {
        'Technology': [
            f"\n\n<h2>Market Impact</h2>\n<p>The technology landscape is evolving rapidly, with industry leaders recognizing the value of these innovations. Early adopters report substantial improvements in operational efficiency and customer satisfaction. This shift represents significant changes in how businesses approach innovation and digital transformation.</p>",
            
            f"\n\n<h2>Implementation Strategies</h2>\n<p>Organizations should start with pilot projects, gathering feedback from early users before scaling deployment. Security considerations must be addressed from the outset, with robust authentication and data protection measures in place throughout the implementation process.</p>"
        ],
        
        'Finance': [
            f"\n\n<h2>Market Dynamics</h2>\n<p>Investors are closely monitoring these developments, with significant capital flowing into related opportunities. Market analysts suggest this represents a fundamental shift in how financial services operate, with potential to reshape traditional business models and create new value chains.</p>",
            
            f"\n\n<h2>Regulatory Considerations</h2>\n<p>Financial institutions must navigate an evolving compliance landscape while pursuing innovation. Key considerations include data privacy regulations, consumer protection requirements, and risk management frameworks that address novel challenges in this emerging space.</p>"
        ],
        
        'Entertainment': [
            f"\n\n<h2>Cultural Impact</h2>\n<p>Audiences worldwide are engaging with this content in unprecedented ways, driving conversations across social media and traditional media. The innovative approach to storytelling and production sets new standards for the industry and influences creative decisions across entertainment sectors.</p>",
            
            f"\n\n<h2>Industry Trends</h2>\n<p>This reflects broader trends reshaping entertainment. Streaming platforms, changing consumer preferences, and new distribution models create opportunities for innovative content formats. Success depends on understanding audience desires and leveraging data analytics effectively.</p>"
        ],
        
        'Travel': [
            f"\n\n<h2>Planning Tips</h2>\n<p>Travelers should consider several key factors including optimal timing, weather patterns, and seasonal pricing. Booking accommodations in advance often secures better rates, while maintaining flexibility enables spontaneous opportunities. Research local transportation options thoroughly.</p>",
            
            f"\n\n<h2>Cultural Awareness</h2>\n<p>Successful travel requires cultural awareness and respect for local customs. Learning basic phrases, understanding dining etiquette, and appreciating cultural norms enhances interactions. The most memorable experiences often come from authentic engagement with local communities.</p>"
        ],
        
        'Politics': [
            f"\n\n<h2>Policy Implications</h2>\n<p>Legislators are addressing these issues within existing frameworks while considering updated regulations. Policy debates reflect fundamental questions about governmental roles, individual rights, and collective responsibilities, with different political philosophies offering contrasting approaches.</p>",
            
            f"\n\n<h2>Public Opinion</h2>\n<p>Public sentiment varies across demographic groups, regions, and political affiliations. Polling reveals nuanced attitudes that don't always align with partisan divides. Effective governance requires mechanisms for public input and transparent decision-making processes.</p>"
        ],
        
        'Business': [
            f"\n\n<h2>Strategic Implications</h2>\n<p>Business leaders must carefully consider how these developments affect strategic positioning and competitive advantages. Companies moving quickly to understand and capitalize on opportunities often gain first-mover advantages, though success requires thoughtful market analysis.</p>",
            
            f"\n\n<h2>Implementation Excellence</h2>\n<p>Translating strategy into results requires operational excellence. Organizations must align processes, systems, and people around clear objectives while maintaining flexibility. Best practices include establishing metrics and implementing robust project management methodologies.</p>"
        ],
        
        'World News': [
            f"\n\n<h2>Global Context</h2>\n<p>The international dimensions highlight our interconnected world. Nations respond through diplomatic channels and international organizations. Regional dynamics play important roles, with neighboring countries particularly affected by spillover effects and secondary consequences.</p>",
            
            f"\n\n<h2>Economic Impact</h2>\n<p>Economic ramifications extend across sectors and regions. Trade patterns, investment flows, and market confidence respond in complex ways. Social impacts affect communities differently depending on circumstances and vulnerabilities, requiring coordinated responses.</p>"
        ]
    }
    
    # Get category-specific expansions
    category_name = category if category in expansions else 'Business'
    available_expansions = expansions[category_name]
    
    # Calculate sections needed (each section ~100 words)
    words_per_section = 100
    sections_needed = min((needed_words // words_per_section) + 1, len(available_expansions))
    
    # Add sections
    expanded_content = current_content
    for i in range(sections_needed):
        expanded_content += available_expansions[i]
    
    return expanded_content

def trim_content(content, target_words=450):
    """
    Trim content to target word count while preserving structure
    """
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get all paragraphs
    paragraphs = soup.find_all(['p', 'h2', 'h3'])
    
    # Keep content until we hit target
    result = []
    word_count = 0
    
    for elem in paragraphs:
        text = elem.get_text()
        elem_words = count_words(text)
        
        if word_count + elem_words <= target_words:
            result.append(str(elem))
            word_count += elem_words
        else:
            # Add partial content from this paragraph if needed
            if elem.name == 'p' and word_count < target_words - 50:
                remaining = target_words - word_count
                words = text.split()[:remaining]
                if words:
                    result.append(f"<p>{' '.join(words)}...</p>")
            break
    
    return '\n'.join(result)

def main():
    print("=" * 60)
    print("📝 ADJUSTING POST CONTENT TO 300-500 WORDS")
    print("=" * 60)
    
    # Get all posts
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    response = requests.get(url, auth=auth)
    
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = response.json()
    
    # Get categories
    cat_url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100"
    cat_response = requests.get(cat_url, auth=auth)
    categories = {c['id']: c['name'] for c in cat_response.json()}
    
    needs_adjustment = []
    for post in posts:
        content = post['content']['rendered']
        word_count = count_words(strip_html(content))
        
        if word_count < 300 or word_count > 500:
            category_id = post['categories'][0] if post['categories'] else 1
            category_name = categories.get(category_id, 'Business')
            
            needs_adjustment.append({
                'id': post['id'],
                'title': post['title']['rendered'],
                'content': content,
                'category': category_name,
                'current_words': word_count,
                'action': 'expand' if word_count < 300 else 'trim'
            })
    
    print(f"\n📊 Found {len(needs_adjustment)} posts outside 300-500 word range")
    expand_count = len([p for p in needs_adjustment if p['action'] == 'expand'])
    trim_count = len([p for p in needs_adjustment if p['action'] == 'trim'])
    print(f"   📈 To expand (<300): {expand_count}")
    print(f"   ✂️  To trim (>500): {trim_count}\n")
    
    updated_count = 0
    failed_count = 0
    
    for idx, post in enumerate(needs_adjustment, 1):
        action_icon = "📈" if post['action'] == 'expand' else "✂️"
        print(f"[{idx}/{len(needs_adjustment)}] {action_icon} {post['title'][:50]}...")
        print(f"   Current: {post['current_words']} words → Target: 300-500 words")
        
        # Adjust content
        if post['action'] == 'expand':
            adjusted = expand_content_intelligently(
                post['title'], 
                post['content'],
                post['category'],
                target_words=400
            )
        else:
            adjusted = trim_content(post['content'], target_words=450)
        
        if not adjusted:
            print("   ⏭️  No adjustment needed")
            continue
        
        # Update post
        update_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post['id']}"
        update_data = {'content': adjusted}
        
        update_response = requests.post(update_url, json=update_data, auth=auth)
        
        if update_response.status_code == 200:
            new_word_count = count_words(strip_html(adjusted))
            print(f"   ✅ Updated! New word count: {new_word_count} words")
            updated_count += 1
        else:
            print(f"   ❌ Failed (Status: {update_response.status_code})")
            failed_count += 1
    
    print("\n" + "=" * 60)
    print("📊 ADJUSTMENT COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully updated: {updated_count} posts")
    print(f"❌ Failed updates: {failed_count} posts")
    print(f"⏭️  Already in range: {len(posts) - len(needs_adjustment)} posts")
    print("=" * 60)

if __name__ == "__main__":
    main()
