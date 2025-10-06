#!/usr/bin/env python3
"""
Quick Website Improvement Implementation Script
Creates essential pages and content for spherevista360.com
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.append('./scripts')

from wp_agent_bulk import post_json, upload_media_return_url
from datetime import datetime

def create_about_page():
    """Create an About page for the website"""
    about_content = """
<h2>Welcome to SphereVista360</h2>

<p>SphereVista360 is your comprehensive source for insightful analysis and perspectives on the world's most pressing topics. We provide 360-degree coverage of finance, technology, politics, travel, and global affairs.</p>

<h3>Our Mission</h3>
<p>To deliver timely, accurate, and actionable insights that help our readers navigate an increasingly complex world. Whether you're tracking market trends, understanding political developments, or exploring new technologies, SphereVista360 provides the perspective you need.</p>

<h3>What We Cover</h3>
<ul>
    <li><strong>Finance:</strong> Market analysis, investment trends, and economic insights</li>
    <li><strong>Technology:</strong> AI developments, cybersecurity, and digital transformation</li>
    <li><strong>Politics:</strong> Global elections, policy analysis, and governance trends</li>
    <li><strong>Travel:</strong> Destination guides, visa information, and travel trends</li>
    <li><strong>World Affairs:</strong> International relations and global developments</li>
</ul>

<h3>Stay Connected</h3>
<p>Join our community of informed readers who rely on SphereVista360 for their daily dose of global insights. Subscribe to our newsletter and follow us on social media for the latest updates.</p>

<p><em>Exploring the world from every angle - that's the SphereVista360 difference.</em></p>
"""
    
    about_page = {
        'title': 'About SphereVista360',
        'content': about_content,
        'status': 'publish',
        'type': 'page',
        'slug': 'about'
    }
    
    return about_page

def create_contact_page():
    """Create a Contact page for the website"""
    contact_content = """
<h2>Get in Touch</h2>

<p>We'd love to hear from you! Whether you have questions, feedback, or story suggestions, the SphereVista360 team is here to connect.</p>

<h3>Contact Information</h3>
<ul>
    <li><strong>Email:</strong> contact@spherevista360.com</li>
    <li><strong>General Inquiries:</strong> info@spherevista360.com</li>
    <li><strong>Editorial:</strong> editorial@spherevista360.com</li>
</ul>

<h3>Editorial Guidelines</h3>
<p>Interested in contributing to SphereVista360? We welcome guest contributions that align with our mission of providing insightful, well-researched content. Please include:</p>
<ul>
    <li>A brief article pitch (2-3 sentences)</li>
    <li>Your background and expertise in the topic</li>
    <li>Links to previous work (if available)</li>
</ul>

<h3>Business Inquiries</h3>
<p>For partnership opportunities, advertising, or business development, please reach out to our business development team.</p>

<h3>Social Media</h3>
<p>Follow us for real-time updates and engage with our community:</p>
<ul>
    <li>Twitter: @SphereVista360</li>
    <li>LinkedIn: SphereVista360</li>
    <li>Facebook: SphereVista360</li>
</ul>

<p><strong>Response Time:</strong> We typically respond to inquiries within 24-48 hours during business days.</p>
"""
    
    contact_page = {
        'title': 'Contact Us',
        'content': contact_content,
        'status': 'publish',
        'type': 'page',
        'slug': 'contact'
    }
    
    return contact_page

def create_privacy_policy():
    """Create a Privacy Policy page"""
    privacy_content = """
<h2>Privacy Policy</h2>
<p><em>Last updated: October 5, 2025</em></p>

<h3>Information We Collect</h3>
<p>SphereVista360 collects information to provide better services to our users. We collect information in the following ways:</p>
<ul>
    <li><strong>Information you give us:</strong> When you subscribe to our newsletter or contact us</li>
    <li><strong>Information we get from your use of our services:</strong> Analytics data to improve user experience</li>
</ul>

<h3>How We Use Information</h3>
<p>We use the information we collect to:</p>
<ul>
    <li>Provide and improve our content and services</li>
    <li>Send you newsletters and updates (if subscribed)</li>
    <li>Analyze website traffic and user behavior</li>
    <li>Respond to your inquiries and requests</li>
</ul>

<h3>Information Sharing</h3>
<p>We do not sell, trade, or rent your personal information to third parties. We may share aggregated, non-personally identifiable information for analytics purposes.</p>

<h3>Cookies</h3>
<p>We use cookies to enhance your browsing experience and analyze website traffic. You can choose to disable cookies through your browser settings.</p>

<h3>Contact Us</h3>
<p>If you have any questions about this Privacy Policy, please contact us at privacy@spherevista360.com</p>
"""
    
    privacy_page = {
        'title': 'Privacy Policy',
        'content': privacy_content,
        'status': 'publish',
        'type': 'page',
        'slug': 'privacy-policy'
    }
    
    return privacy_page

def publish_essential_pages():
    """Publish all essential pages to WordPress"""
    pages = [
        create_about_page(),
        create_contact_page(),
        create_privacy_policy()
    ]
    
    results = []
    
    for page in pages:
        try:
            print(f"📄 Creating page: {page['title']}")
            response = post_json(f"{os.environ.get('WP_SITE')}/wp-json/wp/v2/pages", page)
            
            if response and 'id' in response:
                print(f"✅ Successfully created: {page['title']} (ID: {response['id']})")
                results.append({
                    'title': page['title'],
                    'status': 'success',
                    'url': response.get('link', ''),
                    'id': response['id']
                })
            else:
                print(f"❌ Failed to create: {page['title']}")
                results.append({
                    'title': page['title'],
                    'status': 'failed',
                    'error': str(response)
                })
                
        except Exception as e:
            print(f"❌ Error creating {page['title']}: {str(e)}")
            results.append({
                'title': page['title'],
                'status': 'error',
                'error': str(e)
            })
    
    return results

if __name__ == "__main__":
    print("🚀 SphereVista360 Website Improvement Script")
    print("=" * 50)
    
    # Check if WordPress credentials are set
    if not all([os.environ.get('WP_SITE'), os.environ.get('WP_USER'), os.environ.get('WP_APP_PASS')]):
        print("❌ WordPress credentials not set. Please run:")
        print('export WP_SITE="https://spherevista360.com"')
        print('export WP_USER="your_username"')
        print('export WP_APP_PASS="your_app_password"')
        sys.exit(1)
    
    print(f"🌐 Target site: {os.environ.get('WP_SITE')}")
    print("📋 Creating essential pages...")
    print()
    
    results = publish_essential_pages()
    
    print("\n📊 Summary:")
    print("-" * 30)
    for result in results:
        status_emoji = "✅" if result['status'] == 'success' else "❌"
        print(f"{status_emoji} {result['title']}: {result['status']}")
        if result['status'] == 'success' and 'url' in result:
            print(f"   🔗 {result['url']}")
    
    print(f"\n🎉 Process completed! Check your website to see the new pages.")