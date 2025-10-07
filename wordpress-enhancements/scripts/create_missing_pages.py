#!/usr/bin/env python3
"""
Create Missing WordPress Pages
Helps create essential pages that may be referenced but don't exist
"""

import os
import sys
import requests
import base64
import json
from typing import Dict, List

class PageCreator:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', '').rstrip('/')
        self.wp_user = os.environ.get('WP_USER', '')
        self.wp_pass = os.environ.get('WP_APP_PASS', '')
        
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            raise ValueError("WordPress credentials not set")
        
        # Set up authentication
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        self.base_url = f"{self.wp_site}/wp-json/wp/v2"
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected as {user_data.get('name')} with roles: {user_data.get('roles')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def check_page_exists(self, slug: str) -> bool:
        """Check if a page with given slug exists"""
        try:
            response = requests.get(
                f"{self.base_url}/pages",
                headers=self.headers,
                params={'slug': slug},
                timeout=10
            )
            
            if response.status_code == 200:
                pages = response.json()
                return len(pages) > 0
            return False
        except Exception as e:
            print(f"❌ Error checking page existence: {e}")
            return False
    
    def create_page(self, title: str, content: str, slug: str = None) -> Dict:
        """Create a new WordPress page"""
        if not slug:
            slug = title.lower().replace(' ', '-').replace('&', 'and')
        
        page_data = {
            'title': title,
            'content': content,
            'slug': slug,
            'status': 'publish',
            'type': 'page'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json=page_data,
                timeout=30
            )
            
            if response.status_code == 201:
                page = response.json()
                print(f"✅ Created page: {title}")
                print(f"   🔗 URL: {page.get('link')}")
                return page
            else:
                print(f"❌ Failed to create page: {title} (Status: {response.status_code})")
                return {}
                
        except Exception as e:
            print(f"❌ Error creating page: {e}")
            return {}
    
    def get_essential_pages(self) -> List[Dict]:
        """Get list of essential pages that might be missing"""
        return [
            {
                'title': 'Newsletter',
                'slug': 'newsletter',
                'content': '''
                <h2>Stay Updated with SphereVista360 Newsletter</h2>
                
                <p>Get the latest insights on finance, technology, politics, travel, and global affairs delivered directly to your inbox.</p>
                
                <h3>What You'll Get:</h3>
                <ul>
                    <li>Weekly roundup of our best articles</li>
                    <li>Exclusive analysis and insights</li>
                    <li>Early access to new content</li>
                    <li>Special reports on trending topics</li>
                </ul>
                
                <h3>Subscribe Today</h3>
                <p>Join thousands of informed readers who rely on SphereVista360 for their daily dose of global insights.</p>
                
                <p><em>We respect your privacy and will never share your email address.</em></p>
                
                <h3>Recent Newsletter Issues</h3>
                <p>Browse our recent newsletter archives to see what you've been missing:</p>
                <ul>
                    <li>Weekly Insights - Finance & Tech Trends</li>
                    <li>Global Affairs Update - Political Analysis</li>
                    <li>Travel & World News Digest</li>
                </ul>
                '''
            },
            {
                'title': 'Subscribe',
                'slug': 'subscribe',
                'content': '''
                <h2>Subscribe to SphereVista360</h2>
                
                <p>Never miss an update from SphereVista360. Choose how you'd like to stay connected:</p>
                
                <h3>Email Newsletter</h3>
                <p>Get our weekly digest with the best articles and exclusive insights.</p>
                
                <h3>RSS Feed</h3>
                <p>Subscribe to our RSS feed for instant updates: <a href="/feed">RSS Feed</a></p>
                
                <h3>Social Media</h3>
                <p>Follow us on social media for real-time updates and discussions:</p>
                <ul>
                    <li>Twitter: @SphereVista360</li>
                    <li>LinkedIn: SphereVista360</li>
                    <li>Facebook: SphereVista360</li>
                </ul>
                
                <h3>Categories</h3>
                <p>Subscribe to specific categories that interest you most:</p>
                <ul>
                    <li><a href="/category/finance/">Finance</a> - Market analysis and investment insights</li>
                    <li><a href="/category/tech/">Technology</a> - AI, cybersecurity, and digital transformation</li>
                    <li><a href="/category/politics/">Politics</a> - Global elections and policy analysis</li>
                    <li><a href="/category/travel/">Travel</a> - Destination guides and travel trends</li>
                    <li><a href="/category/world/">World</a> - International affairs and global events</li>
                </ul>
                '''
            },
            {
                'title': 'Archives',
                'slug': 'archives',
                'content': '''
                <h2>SphereVista360 Content Archives</h2>
                
                <p>Browse our comprehensive archive of articles covering finance, technology, politics, travel, and world affairs.</p>
                
                <h3>Browse by Category</h3>
                <ul>
                    <li><a href="/category/finance/">Finance</a> - Market analysis, investment trends, and economic insights</li>
                    <li><a href="/category/tech/">Technology</a> - AI developments, cybersecurity, and digital transformation</li>
                    <li><a href="/category/politics/">Politics</a> - Global elections, policy analysis, and governance trends</li>
                    <li><a href="/category/travel/">Travel</a> - Destination guides, visa information, and travel insights</li>
                    <li><a href="/category/world/">World</a> - International relations and global developments</li>
                </ul>
                
                <h3>Browse by Date</h3>
                <p>View articles by publication date:</p>
                <ul>
                    <li><a href="/?year=2025&month=10">October 2025</a></li>
                    <li><a href="/?year=2025&month=09">September 2025</a></li>
                    <li><a href="/?year=2025&month=08">August 2025</a></li>
                </ul>
                
                <h3>Popular Articles</h3>
                <p>Check out our most popular content across all categories.</p>
                
                <h3>Search</h3>
                <p>Use the search function above to find specific topics or articles.</p>
                '''
            },
            {
                'title': 'Sitemap',
                'slug': 'sitemap',
                'content': '''
                <h2>SphereVista360 Sitemap</h2>
                
                <p>Navigate our complete site structure and find the content you're looking for.</p>
                
                <h3>Main Pages</h3>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about/">About SphereVista360</a></li>
                    <li><a href="/contact/">Contact Us</a></li>
                    <li><a href="/newsletter/">Newsletter</a></li>
                    <li><a href="/subscribe/">Subscribe</a></li>
                    <li><a href="/archives/">Archives</a></li>
                </ul>
                
                <h3>Content Categories</h3>
                <ul>
                    <li><a href="/category/finance/">Finance</a></li>
                    <li><a href="/category/tech/">Technology</a></li>
                    <li><a href="/category/politics/">Politics</a></li>
                    <li><a href="/category/travel/">Travel</a></li>
                    <li><a href="/category/world/">World</a></li>
                </ul>
                
                <h3>Legal & Policy</h3>
                <ul>
                    <li><a href="/privacy-policy/">Privacy Policy</a></li>
                    <li><a href="/terms-of-service/">Terms of Service</a></li>
                    <li><a href="/disclaimer/">Disclaimer</a></li>
                </ul>
                
                <h3>Technical</h3>
                <ul>
                    <li><a href="/feed/">RSS Feed</a></li>
                    <li><a href="/sitemap.xml">XML Sitemap</a></li>
                </ul>
                '''
            },
            {
                'title': 'Terms of Service',
                'slug': 'terms-of-service',
                'content': '''
                <h2>Terms of Service</h2>
                <p><em>Last updated: October 6, 2025</em></p>
                
                <h3>1. Acceptance of Terms</h3>
                <p>By accessing and using SphereVista360.com, you accept and agree to be bound by the terms and provision of this agreement.</p>
                
                <h3>2. Use License</h3>
                <p>Permission is granted to temporarily download one copy of the materials on SphereVista360 for personal, non-commercial transitory viewing only.</p>
                
                <h3>3. Disclaimer</h3>
                <p>The materials on SphereVista360 are provided on an 'as is' basis. SphereVista360 makes no warranties, expressed or implied.</p>
                
                <h3>4. Limitations</h3>
                <p>In no event shall SphereVista360 or its suppliers be liable for any damages arising out of the use or inability to use the materials on SphereVista360.</p>
                
                <h3>5. Content Guidelines</h3>
                <p>Users may not post content that is offensive, illegal, or violates intellectual property rights.</p>
                
                <h3>6. Revisions</h3>
                <p>SphereVista360 may revise these terms of service at any time without notice.</p>
                
                <h3>Contact</h3>
                <p>If you have any questions about these Terms of Service, please contact us at legal@spherevista360.com</p>
                '''
            },
            {
                'title': 'Disclaimer',
                'slug': 'disclaimer',
                'content': '''
                <h2>Disclaimer</h2>
                <p><em>Last updated: October 6, 2025</em></p>
                
                <h3>Information Accuracy</h3>
                <p>The information contained in SphereVista360 is for general information purposes only. While we endeavor to keep the information up to date and correct, we make no representations or warranties of any kind about the completeness, accuracy, reliability, suitability or availability of the information, products, services, or related graphics contained on the website.</p>
                
                <h3>Financial Information</h3>
                <p>Content related to finance, investments, and markets is for informational purposes only and should not be considered as financial advice. Always consult with qualified financial professionals before making investment decisions.</p>
                
                <h3>Political Content</h3>
                <p>Political analysis and commentary represent the views of the authors and do not necessarily reflect the official position of SphereVista360.</p>
                
                <h3>Travel Information</h3>
                <p>Travel information, visa requirements, and destination details may change frequently. Always verify current information with official sources before traveling.</p>
                
                <h3>External Links</h3>
                <p>Our website may contain links to external sites. We have no control over and assume no responsibility for the content, privacy policies, or practices of any third-party sites.</p>
                
                <h3>Limitation of Liability</h3>
                <p>In no event will SphereVista360 be liable for any loss or damage arising from the use of information on this website.</p>
                '''
            }
        ]
    
    def create_missing_pages(self):
        """Create all missing essential pages"""
        print("📄 Creating Missing WordPress Pages")
        print("=" * 35)
        print(f"🌐 Site: {self.wp_site}")
        print()
        
        # Test connection
        if not self.test_connection():
            return False
        
        essential_pages = self.get_essential_pages()
        created_count = 0
        skipped_count = 0
        
        print(f"📋 Checking {len(essential_pages)} essential pages...")
        print()
        
        for page_info in essential_pages:
            title = page_info['title']
            slug = page_info['slug']
            
            print(f"🔍 Checking: {title} ({slug})")
            
            if self.check_page_exists(slug):
                print(f"  ⏭️ Already exists, skipping")
                skipped_count += 1
            else:
                print(f"  ➕ Creating new page...")
                result = self.create_page(
                    title=title,
                    content=page_info['content'],
                    slug=slug
                )
                if result:
                    created_count += 1
                else:
                    print(f"  ❌ Failed to create")
            
            print()
        
        print(f"📊 Summary:")
        print(f"  ✅ Created: {created_count} pages")
        print(f"  ⏭️ Skipped (existing): {skipped_count} pages")
        print(f"  📄 Total checked: {len(essential_pages)} pages")
        
        if created_count > 0:
            print(f"\n🎉 Successfully created {created_count} missing pages!")
            print("🔗 Visit your WordPress admin to review and customize the new pages.")
        
        return True

def main():
    """Main execution function"""
    # Check environment variables
    required_vars = ['WP_SITE', 'WP_USER', 'WP_APP_PASS']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your_value'")
        return False
    
    try:
        creator = PageCreator()
        return creator.create_missing_pages()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()