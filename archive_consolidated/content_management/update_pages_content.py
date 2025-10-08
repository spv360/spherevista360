#!/usr/bin/env python3
"""
Update Newsletter and Homepage content via WordPress API
"""

import requests
import json
from datetime import datetime
import base64

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def update_newsletter_page():
    print("📧 UPDATING NEWSLETTER PAGE")
    print("=" * 40)
    
    # Newsletter content
    content = """<h2>Stay Updated with SphereVista360 Newsletter</h2>
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
<li>In-depth market reports and expert forecasts</li>
<li>Exclusive interviews with industry leaders</li>
<li>Investment tips and financial planning advice</li>
<li>Technology trend analysis and predictions</li>
<li>Global news impact assessments</li>
</ul>

<h2>Subscribe Today</h2>
<p>Join our community of informed readers and never miss important updates. Our newsletter is delivered every Tuesday and Friday, ensuring you stay ahead of the curve in today's fast-paced world.</p>

<p><strong>Free subscription</strong> - No spam, easy unsubscribe, your privacy protected.</p>

<h2>What Our Subscribers Say</h2>
<p>Recent newsletter highlights have covered AI impact on global markets, cryptocurrency regulations, geopolitical events affecting international trade, and emerging technology trends shaping the future.</p>

<p>Sign up now and join thousands of readers who trust SphereVista360 for accurate, timely, and insightful analysis.</p>"""

    # Try to update both newsletter pages (just in case both exist)
    newsletter_pages = [1658, 1680]  # Original and potentially remaining duplicate
    
    for page_id in newsletter_pages:
        print(f"\n📄 Updating Newsletter page ID: {page_id}")
        
        # Data to update
        update_data = {
            "title": "Newsletter - Stay Updated with SphereVista360 Insights",
            "content": content,
            "excerpt": "Subscribe to SphereVista360 newsletter for weekly insights on finance, technology, politics, and global affairs. Join thousands of informed readers today.",
            "status": "publish"
        }
        
        try:
            # Try to update page
            response = requests.post(f"{WP_API_BASE}/pages/{page_id}", json=update_data)
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Successfully updated Newsletter page {page_id}")
                result = response.json()
                print(f"   📝 Title: {result.get('title', {}).get('rendered', 'Unknown')}")
                print(f"   🔗 URL: {result.get('link', 'Unknown')}")
            elif response.status_code == 401:
                print(f"   🔐 Authentication required for page {page_id}")
                print(f"   📋 Manual update needed")
            elif response.status_code == 404:
                print(f"   ❌ Page {page_id} not found (may have been deleted)")
            else:
                print(f"   ❌ Update failed for page {page_id}: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error updating page {page_id}: {e}")

def update_homepage():
    print("\n🏠 UPDATING HOMEPAGE")
    print("=" * 30)
    
    # Homepage content
    content = """<h2>Welcome to SphereVista360 - Your Global Perspective Hub</h2>
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
<p>Connect with thousands of readers who rely on SphereVista360 for informed decision-making. <a href="/newsletter/">Subscribe to our newsletter</a>, follow our social media channels, and become part of our growing community of informed global citizens.</p>

<p>Whether you're an investor, technology enthusiast, political observer, or simply curious about global affairs, SphereVista360 provides the insights you need to understand our complex world.</p>"""

    homepage_id = 1686
    print(f"📄 Updating Homepage page ID: {homepage_id}")
    
    # Data to update
    update_data = {
        "title": "SphereVista360 - Global Perspectives on Finance, Technology, Politics & More",
        "content": content,
        "excerpt": "SphereVista360 provides expert analysis and insights on finance, technology, politics, and global affairs. Stay informed with our comprehensive coverage.",
        "status": "publish"
    }
    
    try:
        # Try to update page
        response = requests.post(f"{WP_API_BASE}/pages/{homepage_id}", json=update_data)
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Successfully updated Homepage")
            result = response.json()
            print(f"   📝 Title: {result.get('title', {}).get('rendered', 'Unknown')}")
            print(f"   🔗 URL: {result.get('link', 'Unknown')}")
        elif response.status_code == 401:
            print(f"   🔐 Authentication required")
            print(f"   📋 Manual update needed")
        else:
            print(f"   ❌ Update failed: {response.status_code}")
            
    except Exception as e:
        print(f"   💥 Error updating homepage: {e}")

def verify_pages():
    print("\n🔍 VERIFYING UPDATED PAGES")
    print("=" * 40)
    
    # Check pages
    pages_to_check = [
        {"id": 1658, "name": "Newsletter (original)"},
        {"id": 1680, "name": "Newsletter-2"},
        {"id": 1686, "name": "Homepage"}
    ]
    
    for page in pages_to_check:
        print(f"\n📄 Checking {page['name']} (ID: {page['id']})")
        
        try:
            response = requests.get(f"{WP_API_BASE}/pages/{page['id']}")
            if response.status_code == 200:
                result = response.json()
                title = result.get('title', {}).get('rendered', 'No Title')
                content_length = len(result.get('content', {}).get('rendered', ''))
                
                print(f"   ✅ Page exists")
                print(f"   📝 Title: {title}")
                print(f"   📊 Content length: {content_length} characters")
                print(f"   🔗 URL: {result.get('link', 'Unknown')}")
                print(f"   📅 Last modified: {result.get('modified', 'Unknown')}")
            elif response.status_code == 404:
                print(f"   ❌ Page not found (may have been deleted)")
            else:
                print(f"   ❌ Error checking page: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")

def generate_seo_instructions():
    print("\n📈 SEO OPTIMIZATION INSTRUCTIONS")
    print("=" * 45)
    
    print("🎯 IF API UPDATE FAILED, MANUAL STEPS:")
    print("\n📧 NEWSLETTER PAGE:")
    print("   1. Go to WordPress Admin → Pages")
    print("   2. Edit Newsletter page")
    print("   3. Title: 'Newsletter - Stay Updated with SphereVista360 Insights'")
    print("   4. Meta Description: 'Subscribe to SphereVista360 newsletter for expert insights on finance, technology, politics, and global affairs. Free weekly updates delivered to your inbox.'")
    print("   5. Focus Keyword: 'newsletter'")
    
    print("\n🏠 HOMEPAGE:")
    print("   1. Go to WordPress Admin → Pages")
    print("   2. Edit Homepage page")
    print("   3. Title: 'SphereVista360 - Global Perspectives on Finance, Technology, Politics & More'")
    print("   4. Meta Description: 'SphereVista360 offers expert analysis on finance, technology, politics, and global affairs. Get comprehensive insights and stay informed with our professional coverage.'")
    print("   5. Focus Keyword: 'global perspectives'")
    
    print("\n🔧 SEO PLUGIN SETUP:")
    print("   1. Install Yoast SEO or Rank Math")
    print("   2. Set focus keywords as specified above")
    print("   3. Ensure meta descriptions are under 160 characters")
    print("   4. Add internal links between pages")
    print("   5. Check page loading speed")

def main():
    print("🚀 WORDPRESS CONTENT UPDATE AUTOMATION")
    print("=" * 50)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ Duplicate pages already deleted")
    print()
    
    # Try to update via API
    update_newsletter_page()
    update_homepage()
    
    # Verify updates
    verify_pages()
    
    # Provide manual instructions
    generate_seo_instructions()
    
    print("\n" + "=" * 50)
    print("🎉 UPDATE PROCESS COMPLETE")
    print("=" * 50)
    print("✅ Attempted automatic updates via WordPress API")
    print("📋 Manual instructions provided if API updates failed")
    print("🔍 Page verification completed")
    print("📈 SEO optimization guidance included")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Check if pages updated successfully")
    print("2. If not, follow manual instructions above")
    print("3. Install SEO plugin for better optimization")
    print("4. Test pages load correctly on frontend")

if __name__ == "__main__":
    main()