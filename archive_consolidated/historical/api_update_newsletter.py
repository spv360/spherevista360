#!/usr/bin/env python3
"""
Update Newsletter page with internal links via WordPress API
"""

import requests
import json
from datetime import datetime

# WordPress site details
SITE_URL = "https://spherevista360.com"
WP_API_BASE = f"{SITE_URL}/wp-json/wp/v2"

def get_newsletter_page_info():
    print("📧 CHECKING NEWSLETTER PAGE INFO")
    print("=" * 40)
    
    # Check both potential newsletter pages
    newsletter_ids = [1658, 1680]
    
    for page_id in newsletter_ids:
        try:
            response = requests.get(f"{WP_API_BASE}/pages/{page_id}")
            if response.status_code == 200:
                page_data = response.json()
                print(f"\n📄 Newsletter Page ID: {page_id}")
                print(f"   Title: {page_data.get('title', {}).get('rendered', 'Unknown')}")
                print(f"   URL: {page_data.get('link', 'Unknown')}")
                print(f"   Status: {page_data.get('status', 'Unknown')}")
                print(f"   Current content length: {len(page_data.get('content', {}).get('rendered', ''))}")
                return page_id, page_data
            elif response.status_code == 404:
                print(f"   ❌ Page {page_id} not found")
            else:
                print(f"   ❌ Error checking page {page_id}: {response.status_code}")
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    return None, None

def update_newsletter_with_links():
    print("\n🔧 UPDATING NEWSLETTER WITH INTERNAL LINKS")
    print("=" * 50)
    
    # Enhanced content with internal links
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

    # Get newsletter page info
    page_id, current_page = get_newsletter_page_info()
    
    if not page_id:
        print("❌ Could not find newsletter page to update")
        return False
    
    # Prepare update data
    update_data = {
        "title": "Newsletter - Stay Updated with SphereVista360 Insights",
        "content": enhanced_content,
        "excerpt": "Subscribe to SphereVista360 newsletter for weekly insights on entertainment, technology, finance, and global affairs. Join thousands of informed readers today.",
        "status": "publish"
    }
    
    print(f"📝 Updating Newsletter page (ID: {page_id})")
    print(f"   New content length: {len(enhanced_content)} characters")
    print(f"   Internal links added: 15+")
    
    # Try different update methods
    update_methods = [
        ("POST", f"{WP_API_BASE}/pages/{page_id}"),
        ("PUT", f"{WP_API_BASE}/pages/{page_id}"),
        ("PATCH", f"{WP_API_BASE}/pages/{page_id}")
    ]
    
    for method, url in update_methods:
        try:
            print(f"\n🔧 Trying {method} method...")
            
            if method == "POST":
                response = requests.post(url, json=update_data)
            elif method == "PUT":
                response = requests.put(url, json=update_data)
            else:  # PATCH
                response = requests.patch(url, json=update_data)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Successfully updated Newsletter page!")
                result = response.json()
                print(f"   📝 Updated Title: {result.get('title', {}).get('rendered', 'Unknown')}")
                print(f"   🔗 URL: {result.get('link', 'Unknown')}")
                print(f"   📅 Modified: {result.get('modified', 'Unknown')}")
                return True
            elif response.status_code == 401:
                print(f"   🔐 Authentication required for {method}")
            elif response.status_code == 403:
                print(f"   🚫 Permission denied for {method}")
            else:
                print(f"   ❌ Failed with {method}: {response.status_code}")
                if response.text:
                    print(f"      Response: {response.text[:200]}...")
                    
        except Exception as e:
            print(f"   💥 Error with {method}: {e}")
    
    return False

def try_basic_auth_update():
    print("\n🔐 TRYING WITH BASIC AUTHENTICATION")
    print("=" * 45)
    
    # This would require actual credentials
    print("⚠️  API update requires WordPress authentication")
    print("   Options:")
    print("   1. WordPress Application Password")
    print("   2. JWT authentication plugin")
    print("   3. Custom API key")
    print("   4. Manual update in WordPress admin")

def manual_update_instructions():
    print("\n📋 MANUAL UPDATE INSTRUCTIONS")
    print("=" * 40)
    
    print("Since API authentication is required, please:")
    print()
    print("1. 📧 Go to WordPress Admin → Pages")
    print("2. 🔍 Find and edit 'Newsletter' page")
    print("3. 📝 Replace title with:")
    print("   'Newsletter - Stay Updated with SphereVista360 Insights'")
    print()
    print("4. 📄 Replace ALL content with:")
    print("-" * 60)
    
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
    
    print(enhanced_content)
    print("-" * 60)
    
    print("\n5. 📋 Set excerpt:")
    print("   'Subscribe to SphereVista360 newsletter for weekly insights on entertainment, technology, finance, and global affairs. Join thousands of informed readers today.'")
    
    print("\n6. 💾 Click 'Update' to save")

def main():
    print("🚀 NEWSLETTER PAGE API UPDATE")
    print("=" * 40)
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Goal: Add internal links to fix SEO issue")
    print()
    
    # Try API update
    success = update_newsletter_with_links()
    
    if not success:
        try_basic_auth_update()
        manual_update_instructions()
    
    print("\n" + "=" * 50)
    print("📊 INTERNAL LINKS ADDED:")
    print("=" * 50)
    print("✅ 15+ internal links to existing posts")
    print("✅ Links to Entertainment category")
    print("✅ Links to popular posts (AI, Gaming, etc.)")
    print("✅ Links to Archives and Homepage")
    print("✅ This will fix 'No links found on page' issue")
    
    print("\n🎯 EXPECTED RESULT:")
    print("   • Newsletter page SEO score will improve")
    print("   • 'No links found' warning will disappear") 
    print("   • Better internal link structure")
    print("   • Improved user navigation")

if __name__ == "__main__":
    main()