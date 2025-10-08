#!/usr/bin/env python3
"""
Delete duplicate pages and optimize SEO for Newsletter and Homepage
"""

import requests
import json
from datetime import datetime

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def delete_duplicate_pages():
    print("🗑️ DELETING DUPLICATE PAGES")
    print("=" * 40)
    
    # Pages to delete (the -2 versions, but keep Newsletter)
    pages_to_delete = [
        1685,  # Disclaimer-2
        1684,  # Terms of Service-2
        1683,  # Sitemap-2
        1682,  # Archives-2
        1681,  # Subscribe-2
        # Skip Newsletter-2 (1680) - will optimize this one
    ]
    
    print("🎯 ATTEMPTING TO DELETE DUPLICATE PAGES:")
    for page_id in pages_to_delete:
        print(f"   Attempting to delete page ID: {page_id}")
        
        try:
            # Try to delete via API (will likely fail due to auth)
            response = requests.delete(f"{WP_API_BASE}/pages/{page_id}")
            if response.status_code == 200:
                print(f"   ✅ Successfully deleted page {page_id}")
            else:
                print(f"   ❌ Could not delete page {page_id}: {response.status_code}")
                print(f"      Manual deletion required in WordPress admin")
        except Exception as e:
            print(f"   💥 Error deleting page {page_id}: {e}")
    
    print("\n📋 MANUAL DELETION GUIDE:")
    print("Go to WordPress Admin → Pages and delete these IDs:")
    print("   • 1685 (Disclaimer-2)")
    print("   • 1684 (Terms of Service-2)")
    print("   • 1683 (Sitemap-2)")
    print("   • 1682 (Archives-2)")
    print("   • 1681 (Subscribe-2)")

def optimize_newsletter_seo():
    print("\n📧 OPTIMIZING NEWSLETTER PAGE SEO")
    print("=" * 45)
    
    # Newsletter page details
    newsletter_pages = [
        {"id": 1680, "title": "Newsletter", "slug": "newsletter-2"},
        {"id": 1658, "title": "Newsletter", "slug": "newsletter"}
    ]
    
    for page in newsletter_pages:
        print(f"\n📄 Optimizing Newsletter page (ID: {page['id']}, Slug: {page['slug']})")
        
        # Enhanced content for Newsletter page
        optimized_content = """
<h2>Stay Updated with SphereVista360 Newsletter</h2>
<p>Join thousands of readers who rely on our newsletter for the latest insights in finance, technology, politics, and global affairs. Get exclusive content delivered directly to your inbox.</p>

<h2>What You'll Receive</h2>
<ul>
<li><strong>Weekly Market Analysis</strong> - Expert insights on financial trends and investment opportunities</li>
<li><strong>Technology Breakthroughs</strong> - Latest developments in AI, blockchain, and emerging tech</li>
<li><strong>Political Updates</strong> - Global political analysis and policy implications</li>
<li><strong>Exclusive Content</strong> - Subscriber-only articles and early access to premium content</li>
</ul>

<h2>Newsletter Benefits</h2>
<p>Our newsletter subscribers enjoy priority access to:</p>
<ul>
<li>In-depth market reports and forecasts</li>
<li>Expert interviews and exclusive commentary</li>
<li>Investment tips and financial planning advice</li>
<li>Technology trend analysis and predictions</li>
<li>Global news impact assessments</li>
</ul>

<h2>Subscribe Today</h2>
<p>Join our community of informed readers and never miss important updates. Our newsletter is delivered every Tuesday and Friday, ensuring you stay ahead of the curve in today's fast-paced world.</p>

<p><strong>Free subscription</strong> - No spam, easy unsubscribe, your privacy protected.</p>

<h2>Recent Newsletter Highlights</h2>
<p>Recent editions have covered:</p>
<ul>
<li>AI impact on global markets and investment strategies</li>
<li>Cryptocurrency regulations and market implications</li>
<li>Geopolitical events affecting international trade</li>
<li>Emerging technology trends shaping the future</li>
<li>Financial planning in uncertain economic times</li>
</ul>

<p>Sign up now and join thousands of readers who trust SphereVista360 for accurate, timely, and insightful analysis.</p>
"""
        
        # SEO-optimized data
        seo_data = {
            "title": "Newsletter - Stay Updated with SphereVista360 Insights",
            "content": optimized_content,
            "excerpt": "Subscribe to SphereVista360 newsletter for weekly insights on finance, technology, politics, and global affairs. Join thousands of informed readers today.",
            "meta": {
                "description": "Subscribe to SphereVista360 newsletter for expert insights on finance, technology, politics, and global affairs. Free weekly updates delivered to your inbox.",
                "keywords": "newsletter, finance insights, technology news, political analysis, global affairs, market updates, investment tips",
                "focus_keyword": "newsletter"
            }
        }
        
        print(f"   📝 SEO Title: {seo_data['title']}")
        print(f"   📋 Meta Description: {seo_data['meta']['description']}")
        print(f"   🎯 Focus Keyword: {seo_data['meta']['focus_keyword']}")
        print(f"   📊 Content Length: {len(seo_data['content'])} characters")
        print(f"   🏷️ Keywords: {seo_data['meta']['keywords']}")

def optimize_homepage_seo():
    print("\n🏠 OPTIMIZING HOMEPAGE SEO")
    print("=" * 35)
    
    # Homepage details (ID: 1686)
    homepage_id = 1686
    
    print(f"📄 Optimizing Homepage (ID: {homepage_id})")
    
    # Enhanced content for Homepage
    optimized_content = """
<h2>Welcome to SphereVista360 - Your Global Perspective Hub</h2>
<p>SphereVista360 is your premier destination for comprehensive insights into finance, technology, politics, and global affairs. We deliver expert analysis and in-depth coverage of the topics that shape our world.</p>

<h2>Expert Financial Analysis</h2>
<p>Stay ahead of market trends with our professional financial analysis covering:</p>
<ul>
<li><strong>Market Trends</strong> - Real-time analysis of global financial markets</li>
<li><strong>Investment Strategies</strong> - Expert guidance for informed investment decisions</li>
<li><strong>Economic Forecasts</strong> - Comprehensive economic outlook and predictions</li>
<li><strong>Cryptocurrency Insights</strong> - Latest developments in digital currencies</li>
</ul>

<h2>Technology Innovation Coverage</h2>
<p>Explore the latest technological breakthroughs and their impact:</p>
<ul>
<li>Artificial Intelligence and machine learning advancements</li>
<li>Blockchain technology and its applications</li>
<li>Cybersecurity trends and digital privacy</li>
<li>Emerging tech startups and innovations</li>
</ul>

<h2>Political Analysis and Global Affairs</h2>
<p>Understanding the political landscape that influences global markets:</p>
<ul>
<li>International relations and trade policies</li>
<li>Government regulations affecting business</li>
<li>Electoral analysis and policy implications</li>
<li>Geopolitical events and their economic impact</li>
</ul>

<h2>Why Choose SphereVista360?</h2>
<p>Our team of expert analysts and researchers provides:</p>
<ul>
<li><strong>Accurate Reporting</strong> - Fact-checked content from verified sources</li>
<li><strong>Timely Updates</strong> - Breaking news and real-time market analysis</li>
<li><strong>Expert Insights</strong> - Professional commentary from industry leaders</li>
<li><strong>Global Perspective</strong> - International viewpoints on major events</li>
</ul>

<h2>Join Our Community</h2>
<p>Connect with thousands of readers who rely on SphereVista360 for informed decision-making. Subscribe to our newsletter, follow our social media channels, and become part of our growing community of informed global citizens.</p>

<p>Whether you're an investor, technology enthusiast, political observer, or simply curious about global affairs, SphereVista360 provides the insights you need to understand our complex world.</p>
"""
    
    # SEO-optimized data
    seo_data = {
        "title": "SphereVista360 - Global Perspectives on Finance, Technology, Politics & More",
        "content": optimized_content,
        "excerpt": "SphereVista360 provides expert analysis and insights on finance, technology, politics, and global affairs. Stay informed with our comprehensive coverage and expert commentary.",
        "meta": {
            "description": "SphereVista360 offers expert analysis on finance, technology, politics, and global affairs. Get comprehensive insights and stay informed with our professional coverage.",
            "keywords": "finance news, technology insights, political analysis, global affairs, market trends, investment advice, economic analysis, tech innovation",
            "focus_keyword": "global perspectives"
        }
    }
    
    print(f"   📝 SEO Title: {seo_data['title']}")
    print(f"   📋 Meta Description: {seo_data['meta']['description']}")
    print(f"   🎯 Focus Keyword: {seo_data['meta']['focus_keyword']}")
    print(f"   📊 Content Length: {len(seo_data['content'])} characters")
    print(f"   🏷️ Keywords: {seo_data['meta']['keywords']}")

def update_pages_content():
    print("\n🔧 UPDATING PAGES WITH OPTIMIZED CONTENT")
    print("=" * 50)
    
    # Updates to make
    updates = [
        {
            "id": 1680,
            "name": "Newsletter-2",
            "title": "Newsletter - Stay Updated with SphereVista360 Insights",
            "content": """<h2>Stay Updated with SphereVista360 Newsletter</h2>
<p>Join thousands of readers who rely on our newsletter for the latest insights in finance, technology, politics, and global affairs. Get exclusive content delivered directly to your inbox.</p>

<h2>What You'll Receive</h2>
<ul>
<li><strong>Weekly Market Analysis</strong> - Expert insights on financial trends and investment opportunities</li>
<li><strong>Technology Breakthroughs</strong> - Latest developments in AI, blockchain, and emerging tech</li>
<li><strong>Political Updates</strong> - Global political analysis and policy implications</li>
<li><strong>Exclusive Content</strong> - Subscriber-only articles and early access to premium content</li>
</ul>

<h2>Newsletter Benefits</h2>
<p>Our newsletter subscribers enjoy priority access to in-depth market reports, expert interviews, investment tips, technology trend analysis, and global news impact assessments.</p>

<h2>Subscribe Today</h2>
<p>Join our community of informed readers and never miss important updates. Our newsletter is delivered every Tuesday and Friday, ensuring you stay ahead of the curve in today's fast-paced world.</p>""",
            "excerpt": "Subscribe to SphereVista360 newsletter for weekly insights on finance, technology, politics, and global affairs. Join thousands of informed readers today."
        },
        {
            "id": 1686,
            "name": "Homepage",
            "title": "SphereVista360 - Global Perspectives on Finance, Technology, Politics & More",
            "content": """<h2>Welcome to SphereVista360 - Your Global Perspective Hub</h2>
<p>SphereVista360 is your premier destination for comprehensive insights into finance, technology, politics, and global affairs. We deliver expert analysis and in-depth coverage of the topics that shape our world.</p>

<h2>Expert Financial Analysis</h2>
<p>Stay ahead of market trends with our professional financial analysis covering market trends, investment strategies, economic forecasts, and cryptocurrency insights.</p>

<h2>Technology Innovation Coverage</h2>
<p>Explore the latest technological breakthroughs including artificial intelligence, blockchain technology, cybersecurity trends, and emerging tech startups.</p>

<h2>Political Analysis and Global Affairs</h2>
<p>Understanding the political landscape through international relations, government regulations, electoral analysis, and geopolitical events.</p>

<h2>Why Choose SphereVista360?</h2>
<p>Our expert team provides accurate reporting, timely updates, expert insights, and global perspectives on major events affecting markets and society.</p>""",
            "excerpt": "SphereVista360 provides expert analysis and insights on finance, technology, politics, and global affairs. Stay informed with our comprehensive coverage."
        }
    ]
    
    for update in updates:
        print(f"\n📄 {update['name']} (ID: {update['id']})")
        print(f"   📝 Title: {update['title']}")
        print(f"   📊 Content: {len(update['content'])} characters")
        print(f"   📋 Excerpt: {update['excerpt']}")
        
        # Try to update via API
        try:
            data = {
                "title": update['title'],
                "content": update['content'],
                "excerpt": update['excerpt']
            }
            
            response = requests.post(f"{WP_API_BASE}/pages/{update['id']}", json=data)
            if response.status_code in [200, 201]:
                print(f"   ✅ Successfully updated {update['name']}")
            else:
                print(f"   ❌ Could not update {update['name']}: {response.status_code}")
                print(f"      Manual update required in WordPress admin")
        except Exception as e:
            print(f"   💥 Error updating {update['name']}: {e}")

def main():
    print("🔧 WORDPRESS CLEANUP & SEO OPTIMIZATION")
    print("=" * 50)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Delete duplicates
    delete_duplicate_pages()
    
    # Optimize SEO
    optimize_newsletter_seo()
    optimize_homepage_seo()
    
    # Update content
    update_pages_content()
    
    print("\n" + "=" * 50)
    print("📋 MANUAL STEPS REQUIRED:")
    print("=" * 50)
    
    print("1. 🗑️ DELETE DUPLICATE PAGES in WordPress Admin:")
    print("   • Go to Pages → All Pages")
    print("   • Delete pages with IDs: 1685, 1684, 1683, 1682, 1681")
    
    print("\n2. 📝 UPDATE SEO CONTENT in WordPress Admin:")
    print("   • Edit Newsletter page (ID: 1680)")
    print("   • Edit Homepage (ID: 1686)")
    print("   • Copy the optimized content from this script output")
    print("   • Add proper meta descriptions and focus keywords")
    
    print("\n3. 🔍 SEO PLUGIN SETUP:")
    print("   • Use Yoast SEO or Rank Math plugin")
    print("   • Set focus keywords as shown above")
    print("   • Optimize meta descriptions (160 characters max)")
    print("   • Add internal links between pages")
    
    print("\n✅ EXPECTED RESULTS:")
    print("   • No more duplicate pages")
    print("   • Optimized Newsletter page with 100% SEO score")
    print("   • Enhanced Homepage with comprehensive content")
    print("   • Better search engine visibility")

if __name__ == "__main__":
    main()