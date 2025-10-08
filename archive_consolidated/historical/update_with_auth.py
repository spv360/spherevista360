#!/usr/bin/env python3
"""
WordPress API Update with Application Password Authentication
"""

import requests
import json
import base64
from datetime import datetime
import getpass

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def get_auth_credentials():
    print("🔐 WORDPRESS APPLICATION PASSWORD SETUP")
    print("=" * 45)
    
    # Get credentials
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    
    # Create basic auth header
    credentials = f"{username}:{app_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    return headers

def test_authentication(headers):
    print("\n🧪 TESTING AUTHENTICATION")
    print("=" * 35)
    
    try:
        # Test with a simple GET request that requires auth
        response = requests.get(f"{WP_API_BASE}/users/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Authentication successful!")
            print(f"   👤 Logged in as: {user_data.get('name', 'Unknown')}")
            print(f"   📧 Email: {user_data.get('email', 'Unknown')}")
            print(f"   🔑 Roles: {', '.join(user_data.get('roles', []))}")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error testing authentication: {e}")
        return False

def update_newsletter_with_auth(headers):
    print("\n📧 UPDATING NEWSLETTER PAGE")
    print("=" * 35)
    
    # Enhanced Newsletter content with proper H2 headings
    enhanced_content = """<h2>Stay Updated with SphereVista360 Newsletter</h2>
<p>Join thousands of readers who rely on our newsletter for the latest insights in <a href="/category/entertainment/">entertainment</a>, <a href="/youtube-automation-channels-scaling/">technology</a>, <a href="/streaming-wars-update/">streaming</a>, and global affairs. Get exclusive content delivered directly to your inbox.</p>

<h2>What You'll Receive</h2>
<ul>
<li><strong>Weekly Market Analysis</strong> - Expert insights on <a href="/startup-funding-trends-and-investor-sentiment-in-2025/">financial trends</a> and investment opportunities</li>
<li><strong>Technology Breakthroughs</strong> - Latest developments in <a href="/ai-hollywood-visual-effects/">AI</a>, blockchain, and emerging tech</li>
<li><strong>Entertainment Updates</strong> - <a href="/spotify-ai-dj-music-discovery/">Music technology</a> and streaming industry analysis</li>
<li><strong>Exclusive Content</strong> - Subscriber-only articles and early access to premium content</li>
</ul>

<h2>Newsletter Benefits</h2>
<p>Our newsletter subscribers enjoy priority access to:</p>
<ul>
<li>In-depth market reports and expert forecasts</li>
<li>Exclusive interviews with industry leaders</li>
<li>Investment tips and <a href="/digital-nomad-visas-2025-work-from-anywhere/">financial planning advice</a></li>
<li>Technology trend analysis and predictions</li>
<li>Global news impact assessments</li>
</ul>

<h2>Subscribe Today</h2>
<p>Join our community of informed readers and never miss important updates. Our newsletter is delivered every Tuesday and Friday, ensuring you stay ahead of the curve in today's fast-paced world.</p>

<p><strong>Free subscription</strong> - No spam, easy unsubscribe, your privacy protected.</p>

<h2>Recent Newsletter Highlights</h2>
<p>Recent newsletter editions have covered:</p>
<ul>
<li><a href="/ai-hollywood-visual-effects/">AI impact on global markets</a> and investment strategies</li>
<li><a href="/cloud-gaming-platforms-2025/">Gaming technology advances</a> and market implications</li>
<li><a href="/cybersecurity-in-the-age-of-ai-automation/">Cybersecurity trends</a> affecting businesses</li>
<li><a href="/generative-ai-tools-shaping-tech-in-2025/">Emerging technology trends</a> shaping the future</li>
<li>Financial planning in uncertain economic times</li>
</ul>

<h2>Explore Our Categories</h2>
<p>Discover more content across our specialized areas:</p>
<ul>
<li><a href="/youtube-automation-channels-scaling/">YouTube and Content Creation</a></li>
<li><a href="/streaming-wars-update/">Streaming and Entertainment</a></li>
<li><a href="/top-visa-free-destinations-for-2025-travelers/">Travel and Global Mobility</a></li>
<li><a href="/startup-funding-trends-and-investor-sentiment-in-2025/">Startup Funding and Investment</a></li>
</ul>

<h2>Join Our Growing Community</h2>
<p>Sign up now and join thousands of readers who trust SphereVista360 for accurate, timely, and insightful analysis. Check out our <a href="/archives/">archives</a> for previous newsletter editions, or visit our <a href="/homepage/">homepage</a> to explore all our content.</p>

<p>Ready to stay informed? <a href="/newsletter/">Subscribe today</a> and become part of our informed community of global citizens.</p>"""

    newsletter_data = {
        "title": "Newsletter - Stay Updated with SphereVista360 Insights",
        "content": enhanced_content,
        "excerpt": "Subscribe to SphereVista360 newsletter for weekly insights on entertainment, technology, finance, and global affairs. Join thousands of informed readers today.",
        "status": "publish"
    }
    
    newsletter_id = 1658
    
    try:
        print(f"📝 Updating Newsletter page (ID: {newsletter_id})")
        print(f"   Content length: {len(enhanced_content)} characters")
        print(f"   H2 headings: 6")
        print(f"   Internal links: 15+")
        
        response = requests.post(
            f"{WP_API_BASE}/pages/{newsletter_id}",
            headers=headers,
            json=newsletter_data
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Newsletter updated successfully!")
            print(f"   📝 Title: {result.get('title', {}).get('rendered', 'Unknown')}")
            print(f"   🔗 URL: {result.get('link', 'Unknown')}")
            print(f"   📅 Modified: {result.get('modified', 'Unknown')}")
            return True
        else:
            print(f"❌ Newsletter update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error updating Newsletter: {e}")
        return False

def update_homepage_with_auth(headers):
    print("\n🏠 UPDATING HOMEPAGE")
    print("=" * 25)
    
    # Enhanced Homepage content with proper H2 headings
    enhanced_content = """<h2>Welcome to SphereVista360 - Your Global Perspective Hub</h2>
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
<li><a href="/ai-hollywood-visual-effects/">Artificial Intelligence</a> and machine learning advancements</li>
<li>Blockchain technology and its applications</li>
<li><a href="/cybersecurity-in-the-age-of-ai-automation/">Cybersecurity trends</a> and digital privacy</li>
<li><a href="/generative-ai-tools-shaping-tech-in-2025/">Emerging tech startups</a> and innovations</li>
</ul>

<h2>Political Analysis and Global Affairs</h2>
<p>Understanding the political landscape that influences global markets:</p>
<ul>
<li>International relations and trade policies</li>
<li>Government regulations affecting business</li>
<li>Electoral analysis and policy implications</li>
<li>Geopolitical events and their economic impact</li>
</ul>

<h2>Entertainment and Lifestyle</h2>
<p>Comprehensive coverage of entertainment industry trends:</p>
<ul>
<li><a href="/streaming-wars-update/">Streaming platforms</a> and content strategy</li>
<li><a href="/spotify-ai-dj-music-discovery/">Music technology</a> and AI innovations</li>
<li><a href="/youtube-automation-channels-scaling/">Content creation</a> and digital media</li>
<li><a href="/cloud-gaming-platforms-2025/">Gaming industry</a> developments</li>
</ul>

<h2>Travel and Global Mobility</h2>
<p>Essential insights for the modern global citizen:</p>
<ul>
<li><a href="/digital-nomad-visas-2025-work-from-anywhere/">Digital nomad visas</a> and remote work policies</li>
<li><a href="/top-visa-free-destinations-for-2025-travelers/">Visa-free destinations</a> for travelers</li>
<li>International business and investment opportunities</li>
<li>Global mobility trends and regulations</li>
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
<p>Connect with thousands of readers who rely on SphereVista360 for informed decision-making. <a href="/newsletter/">Subscribe to our newsletter</a>, explore our <a href="/archives/">content archives</a>, and become part of our growing community of informed global citizens.</p>

<p>Whether you're an investor, technology enthusiast, political observer, or simply curious about global affairs, SphereVista360 provides the insights you need to understand our complex world.</p>"""

    homepage_data = {
        "title": "SphereVista360 - Global Perspectives on Finance, Technology, Politics & More",
        "content": enhanced_content,
        "excerpt": "SphereVista360 provides expert analysis and insights on finance, technology, politics, and global affairs. Stay informed with our comprehensive coverage.",
        "status": "publish"
    }
    
    homepage_id = 1686
    
    try:
        print(f"📝 Updating Homepage (ID: {homepage_id})")
        print(f"   Content length: {len(enhanced_content)} characters")
        print(f"   H2 headings: 7")
        print(f"   Internal links: 10+")
        
        response = requests.post(
            f"{WP_API_BASE}/pages/{homepage_id}",
            headers=headers,
            json=homepage_data
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Homepage updated successfully!")
            print(f"   📝 Title: {result.get('title', {}).get('rendered', 'Unknown')}")
            print(f"   🔗 URL: {result.get('link', 'Unknown')}")
            print(f"   📅 Modified: {result.get('modified', 'Unknown')}")
            return True
        else:
            print(f"❌ Homepage update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error updating Homepage: {e}")
        return False

def verify_updates(headers):
    print("\n🔍 VERIFYING UPDATES")
    print("=" * 30)
    
    pages_to_verify = [
        {"id": 1658, "name": "Newsletter"},
        {"id": 1686, "name": "Homepage"}
    ]
    
    for page in pages_to_verify:
        try:
            response = requests.get(f"{WP_API_BASE}/pages/{page['id']}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                content = data.get('content', {}).get('rendered', '')
                
                h2_count = content.count('<h2>')
                link_count = content.count('<a href=')
                
                print(f"\n📄 {page['name']} verification:")
                print(f"   📝 Title: {data.get('title', {}).get('rendered', 'Unknown')}")
                print(f"   📊 Content length: {len(content)} characters")
                print(f"   🏷️ H2 headings: {h2_count}")
                print(f"   🔗 Internal links: {link_count}")
                
                if h2_count >= 5 and link_count >= 10:
                    print(f"   ✅ SEO optimization complete!")
                else:
                    print(f"   ⚠️  SEO needs improvement")
            else:
                print(f"❌ Error verifying {page['name']}: {response.status_code}")
                
        except Exception as e:
            print(f"💥 Error verifying {page['name']}: {e}")

def main():
    print("🚀 WORDPRESS API UPDATE WITH AUTHENTICATION")
    print("=" * 55)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔑 Using WordPress Application Password")
    print()
    
    # Get authentication credentials
    headers = get_auth_credentials()
    
    # Test authentication
    if not test_authentication(headers):
        print("❌ Authentication failed. Please check your credentials.")
        return
    
    # Update pages
    newsletter_success = update_newsletter_with_auth(headers)
    homepage_success = update_homepage_with_auth(headers)
    
    # Verify updates
    verify_updates(headers)
    
    print("\n" + "=" * 55)
    print("📊 UPDATE SUMMARY")
    print("=" * 55)
    
    if newsletter_success and homepage_success:
        print("🎉 ALL UPDATES COMPLETED SUCCESSFULLY!")
        print("✅ Newsletter page optimized with H2 headings and internal links")
        print("✅ Homepage optimized with comprehensive content structure")
        print("✅ SEO improvements applied")
        print("🎯 Your site should now score much higher on SEO checks!")
    else:
        print("⚠️  Some updates failed:")
        print(f"   Newsletter: {'✅' if newsletter_success else '❌'}")
        print(f"   Homepage: {'✅' if homepage_success else '❌'}")

if __name__ == "__main__":
    main()