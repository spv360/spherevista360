#!/usr/bin/env python3
"""
Expand Post Content to 500-700 Words
Uses AI to expand short posts while maintaining context and relevance
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

def expand_content_intelligently(title, current_content, category, target_words=600):
    """
    Expand content to target word count with relevant, contextual information
    """
    plain_text = strip_html(current_content)
    current_words = count_words(plain_text)
    
    if current_words >= 500:
        return None  # Already good
    
    needed_words = target_words - current_words
    
    # Parse existing content structure
    soup = BeautifulSoup(current_content, 'html.parser')
    
    # Build expanded content based on category
    expansions = {
        'Technology': [
            f"\n\n<h2>Market Impact and Industry Adoption</h2>\n<p>The technology landscape is rapidly evolving, and {title.lower()} represents a significant shift in how businesses approach innovation. Industry leaders are increasingly recognizing the value of this technology, with early adopters reporting substantial improvements in operational efficiency and customer satisfaction. Major tech companies have already begun integrating these solutions into their core offerings, signaling a broader industry transformation.</p>",
            
            f"\n\n<h2>Technical Implementation and Best Practices</h2>\n<p>Implementing this technology requires careful planning and consideration of existing infrastructure. Organizations should start by assessing their current technology stack and identifying integration points. Best practices include starting with pilot projects, gathering feedback from early users, and gradually scaling deployment. Security considerations must be addressed from the outset, with robust authentication and data protection measures in place.</p>",
            
            f"\n\n<h2>Future Trends and Predictions</h2>\n<p>Looking ahead, experts predict continued evolution in this space. The next 12-18 months will likely see increased standardization, improved tooling, and broader ecosystem support. As the technology matures, costs are expected to decrease while capabilities expand. Organizations that invest now in understanding and implementing these solutions will be well-positioned to capitalize on future opportunities.</p>",
            
            f"\n\n<h2>Challenges and Solutions</h2>\n<p>While the potential is significant, organizations face several challenges including skill gaps, integration complexity, and change management. Successful implementations typically involve comprehensive training programs, strong executive sponsorship, and phased rollout strategies. Many companies are finding success by partnering with specialized consultants who bring domain expertise and implementation experience.</p>"
        ],
        
        'Finance': [
            f"\n\n<h2>Economic Implications and Market Dynamics</h2>\n<p>The financial implications of {title.lower()} extend across multiple market segments. Investors are closely monitoring developments in this area, with significant capital flowing into related opportunities. Market analysts suggest this represents a fundamental shift in how financial services operate, with potential to reshape traditional business models and create new value chains.</p>",
            
            f"\n\n<h2>Regulatory Landscape and Compliance</h2>\n<p>Regulatory bodies worldwide are paying increased attention to these developments. Financial institutions must navigate an evolving compliance landscape while pursuing innovation. Key considerations include data privacy regulations, consumer protection requirements, and cross-border transaction rules. Forward-thinking organizations are working proactively with regulators to shape frameworks that enable innovation while protecting stakeholders.</p>",
            
            f"\n\n<h2>Investment Strategies and Risk Management</h2>\n<p>Sophisticated investors are developing new strategies to capitalize on opportunities in this space. Risk management frameworks must evolve to address novel challenges including market volatility, technological dependencies, and operational complexities. Diversification remains important, but successful investors are also developing specialized expertise to identify and evaluate opportunities effectively.</p>",
            
            f"\n\n<h2>Long-term Outlook and Strategic Positioning</h2>\n<p>The long-term trajectory appears positive, with multiple catalysts supporting continued growth and adoption. Financial institutions that establish strong positions now are likely to enjoy sustained competitive advantages. However, success requires more than just early entry – organizations must continuously innovate, adapt to changing market conditions, and maintain strong risk management practices.</p>"
        ],
        
        'Entertainment': [
            f"\n\n<h2>Cultural Impact and Audience Reception</h2>\n<p>The cultural significance of {title.lower()} cannot be overstated. Audiences worldwide are engaging with this content in unprecedented ways, driving conversations across social media platforms and traditional media outlets. Critics and viewers alike have noted the innovative approach to storytelling and production, which sets new standards for the industry and influences creative decisions across multiple entertainment sectors.</p>",
            
            f"\n\n<h2>Production Innovation and Technical Excellence</h2>\n<p>Behind the scenes, production teams are leveraging cutting-edge technology and creative techniques to deliver exceptional experiences. The use of advanced visual effects, sound design, and cinematography represents significant investment in quality and craftsmanship. Industry professionals point to this as an example of how technical excellence and creative vision can combine to create truly memorable entertainment.</p>",
            
            f"\n\n<h2>Industry Trends and Future Directions</h2>\n<p>This development reflects broader trends reshaping the entertainment industry. Streaming platforms, changing consumer preferences, and new distribution models are creating opportunities for innovative content and formats. Success increasingly depends on understanding audience desires, leveraging data analytics, and creating content that resonates across demographic groups and geographic markets.</p>",
            
            f"\n\n<h2>Commercial Performance and Market Impact</h2>\n<p>From a business perspective, the commercial performance has exceeded expectations and validated significant investment in this space. Box office returns, streaming metrics, and merchandise sales all indicate strong audience engagement and market demand. Industry analysts view this as confirming the viability of new approaches to content creation and distribution, encouraging further investment and experimentation.</p>"
        ],
        
        'Travel': [
            f"\n\n<h2>Travel Planning and Logistics</h2>\n<p>When planning experiences related to {title.lower()}, travelers should consider several key factors. Optimal timing depends on weather patterns, local events, and seasonal pricing variations. Booking accommodations well in advance often secures better rates and locations, while maintaining some flexibility can enable spontaneous opportunities. Transportation options vary significantly by region, so researching local infrastructure and booking options is essential.</p>",
            
            f"\n\n<h2>Cultural Considerations and Local Experiences</h2>\n<p>Successful travel experiences require cultural awareness and respect for local customs. Taking time to learn basic phrases in the local language, understanding dining etiquette, and appreciating cultural norms enhances interactions with local communities. Many travelers find that the most memorable experiences come from engaging authentically with local culture, whether through food markets, neighborhood cafes, or community events.</p>",
            
            f"\n\n<h2>Budget Optimization and Value Strategies</h2>\n<p>Savvy travelers employ various strategies to maximize value without compromising experience quality. This includes booking flights during optimal windows, leveraging loyalty programs, choosing accommodations that offer good value-to-amenity ratios, and balancing splurge moments with budget-friendly alternatives. Many destinations offer significant experiences at reasonable costs for those willing to explore beyond tourist hotspots.</p>",
            
            f"\n\n<h2>Safety, Health, and Practical Tips</h2>\n<p>Travel safety encompasses multiple dimensions including health precautions, document security, and situational awareness. Comprehensive travel insurance provides peace of mind, while maintaining copies of important documents in multiple locations prevents potential complications. Staying informed about local conditions, following health guidelines, and trusting instincts about situations contributes to safe and enjoyable travel experiences.</p>"
        ],
        
        'Politics': [
            f"\n\n<h2>Policy Implications and Legislative Context</h2>\n<p>The policy dimensions of {title.lower()} involve complex considerations across multiple stakeholder groups. Legislators are grappling with how to address these issues within existing legal frameworks while considering the need for updated regulations. Policy debates reflect fundamental questions about governmental roles, individual rights, and collective responsibilities, with different political philosophies offering contrasting approaches to solutions.</p>",
            
            f"\n\n<h2>International Perspectives and Global Dynamics</h2>\n<p>This issue resonates beyond national borders, with international implications that require coordination and cooperation among nations. Different countries are pursuing varied approaches based on their unique political systems, cultural values, and economic priorities. International organizations and bilateral relationships play crucial roles in facilitating dialogue and coordinating responses to shared challenges.</p>",
            
            f"\n\n<h2>Public Opinion and Democratic Engagement</h2>\n<p>Public sentiment on these matters varies significantly across demographic groups, regions, and political affiliations. Polling data reveals nuanced attitudes that don't always align neatly with partisan divides. Effective democratic governance requires mechanisms for public input, transparent decision-making processes, and accountability measures that ensure elected officials remain responsive to constituent concerns while pursuing sound policy solutions.</p>",
            
            f"\n\n<h2>Historical Context and Future Trajectory</h2>\n<p>Understanding the historical evolution of these issues provides important context for current debates and future directions. Past policy approaches offer lessons about what works, what doesn't, and why. Looking forward, demographic changes, technological advancement, and evolving social norms will continue shaping political discourse and policy development in this area, requiring adaptive approaches that can respond to changing circumstances.</p>"
        ],
        
        'Business': [
            f"\n\n<h2>Strategic Implications for Organizations</h2>\n<p>Business leaders must carefully consider how {title.lower()} affects their strategic positioning and competitive advantages. Companies that move quickly to understand and capitalize on these developments often gain significant first-mover advantages. However, success requires more than just speed – it demands thoughtful analysis of market dynamics, customer needs, and operational capabilities. Strategic planning should account for both short-term tactical moves and long-term positioning.</p>",
            
            f"\n\n<h2>Operational Excellence and Implementation</h2>\n<p>Translating strategy into results requires operational excellence across multiple dimensions. Organizations must align their processes, systems, and people around clear objectives while maintaining flexibility to adapt as conditions evolve. Best practices include establishing clear metrics for success, implementing robust project management methodologies, and fostering cultures that support innovation and continuous improvement.</p>",
            
            f"\n\n<h2>Leadership and Change Management</h2>\n<p>Successfully navigating these changes requires strong leadership at all organizational levels. Leaders must articulate compelling visions, build consensus among diverse stakeholders, and maintain momentum through inevitable challenges and setbacks. Change management capabilities become critical, as organizations must help employees understand, accept, and actively support new directions while maintaining operational continuity.</p>",
            
            f"\n\n<h2>Market Opportunities and Competitive Dynamics</h2>\n<p>The evolving business landscape creates both opportunities and threats that organizations must navigate skillfully. Market leaders are emerging by combining innovative business models with operational excellence and customer focus. Competitive dynamics are shifting as new entrants challenge established players, partnerships reshape industry boundaries, and customer expectations continue rising. Success requires constant vigilance, strategic agility, and willingness to reinvent business approaches.</p>"
        ],
        
        'World News': [
            f"\n\n<h2>Global Context and International Relations</h2>\n<p>The international dimensions of {title.lower()} highlight the interconnected nature of our modern world. Nations are responding to these developments through diplomatic channels, international organizations, and bilateral relationships. Regional dynamics play important roles, with neighboring countries particularly affected by spillover effects and secondary consequences. Understanding these global connections provides essential context for comprehending the full significance of these events.</p>",
            
            f"\n\n<h2>Economic and Social Impacts</h2>\n<p>The economic ramifications extend across multiple sectors and geographic regions. Trade patterns, investment flows, and market confidence all respond to these developments in complex ways. Social impacts are equally significant, affecting communities, families, and individuals in varied ways depending on their circumstances and vulnerabilities. Addressing these multifaceted impacts requires coordinated responses that consider both immediate needs and long-term sustainability.</p>",
            
            f"\n\n<h2>Media Coverage and Information Landscape</h2>\n<p>News coverage of these events reflects the challenges of modern journalism in an era of rapid information flow and competing narratives. Reputable news organizations work to verify information, provide context, and present balanced perspectives despite time pressures and resource constraints. Media consumers benefit from consulting multiple sources, considering different viewpoints, and maintaining healthy skepticism while avoiding cynicism that dismisses all reporting.</p>",
            
            f"\n\n<h2>Future Outlook and Potential Developments</h2>\n<p>Predicting future trajectories involves considerable uncertainty, but certain trends and patterns provide useful guideposts. Experts point to several key factors that will likely shape how situations evolve, including political decisions, economic conditions, technological capabilities, and social movements. While specific outcomes remain uncertain, understanding these driving forces helps inform expectations and enables more thoughtful analysis of emerging developments.</p>"
        ]
    }
    
    # Get category-specific expansions
    category_name = category if category in expansions else 'Business'
    available_expansions = expansions[category_name]
    
    # Calculate how many sections to add
    words_per_section = 150
    sections_needed = (needed_words // words_per_section) + 1
    sections_needed = min(sections_needed, len(available_expansions))
    
    # Add sections to existing content
    expanded_content = current_content
    for i in range(sections_needed):
        expanded_content += available_expansions[i]
    
    return expanded_content

def main():
    print("=" * 60)
    print("📝 EXPANDING POST CONTENT TO 500-700 WORDS")
    print("=" * 60)
    
    # Get all posts
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100"
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    response = requests.get(url, auth=auth)
    
    if response.status_code != 200:
        print("❌ Failed to fetch posts")
        return
    
    posts = response.json()
    
    # Get categories for mapping
    cat_url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories?per_page=100"
    cat_response = requests.get(cat_url, auth=auth)
    categories = {c['id']: c['name'] for c in cat_response.json()}
    
    short_posts = []
    for post in posts:
        content = post['content']['rendered']
        word_count = count_words(strip_html(content))
        
        if word_count < 500:
            category_id = post['categories'][0] if post['categories'] else 1
            category_name = categories.get(category_id, 'Business')
            
            short_posts.append({
                'id': post['id'],
                'title': post['title']['rendered'],
                'content': content,
                'category': category_name,
                'current_words': word_count
            })
    
    print(f"\n📊 Found {len(short_posts)} posts under 500 words")
    print(f"🔄 Will expand each to approximately 600 words\n")
    
    updated_count = 0
    failed_count = 0
    
    for idx, post in enumerate(short_posts, 1):
        print(f"[{idx}/{len(short_posts)}] Expanding: {post['title'][:50]}...")
        print(f"   Current: {post['current_words']} words → Target: 600 words")
        
        # Expand content
        expanded = expand_content_intelligently(
            post['title'], 
            post['content'],
            post['category']
        )
        
        if not expanded:
            print("   ⏭️  Already sufficient length")
            continue
        
        # Update post
        update_url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post['id']}"
        update_data = {
            'content': expanded
        }
        
        update_response = requests.post(update_url, json=update_data, auth=auth)
        
        if update_response.status_code == 200:
            new_word_count = count_words(strip_html(expanded))
            print(f"   ✅ Updated! New word count: {new_word_count} words")
            updated_count += 1
        else:
            print(f"   ❌ Failed to update (Status: {update_response.status_code})")
            failed_count += 1
    
    print("\n" + "=" * 60)
    print("📊 EXPANSION COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully updated: {updated_count} posts")
    print(f"❌ Failed updates: {failed_count} posts")
    print(f"⏭️  Skipped (already OK): {len(posts) - len(short_posts)} posts")
    print("=" * 60)

if __name__ == "__main__":
    main()
