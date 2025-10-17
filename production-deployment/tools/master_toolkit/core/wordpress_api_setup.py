#!/usr/bin/env python3
"""
WordPress Content Creator via REST API - Improved Version
Handles WordPress authentication and creates all content automatically
"""

import requests
import json
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

class WordPressAPI:
    def __init__(self):
        self.base_url = os.getenv('WORDPRESS_BASE_URL', '').rstrip('/')
        self.username = os.getenv('WORDPRESS_USERNAME', '')
        self.password = os.getenv('WORDPRESS_PASSWORD', '')
        
        if not all([self.base_url, self.username, self.password]):
            raise ValueError("Missing WordPress credentials. Please check .env file.")
        
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        
        # Use HTTPBasicAuth for better authentication
        self.auth = HTTPBasicAuth(self.username, self.password)
        
        print(f"🔧 WordPress API Content Creator")
        print(f"📍 Site: {self.base_url}")
        print(f"👤 User: {self.username}")
        print("=" * 60)

    def test_connection(self):
        """Test WordPress API connection"""
        print("\n🔍 Testing WordPress connection...")
        
        try:
            # Try to get current user info
            response = requests.get(
                f"{self.api_url}/users/me",
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected successfully!")
                print(f"   User: {user_data.get('name', 'Unknown')}")
                print(f"   Role: {', '.join(user_data.get('roles', []))}")
                return True
            elif response.status_code == 401:
                print(f"❌ Authentication failed (401)")
                print(f"   Please check your username and password")
                print(f"   Tip: Use an Application Password for better security")
                return False
            else:
                print(f"❌ Connection failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Connection timeout. Please check your site URL.")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection error. Please check your site URL and internet connection.")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False

    def create_page(self, title, content, slug=None):
        """Create a WordPress page"""
        page_data = {
            'title': title,
            'content': content,
            'status': 'publish',
            'type': 'page'
        }
        
        if slug:
            page_data['slug'] = slug
            
        try:
            response = requests.post(
                f"{self.api_url}/pages",
                auth=self.auth,
                json=page_data,
                timeout=30
            )
            
            if response.status_code == 201:
                page = response.json()
                print(f"   ✅ Created: {title} (ID: {page['id']})")
                return page
            else:
                print(f"   ❌ Failed: {title} - HTTP {response.status_code}")
                if response.status_code == 401:
                    print("      Authentication error - check credentials")
                return None
                
        except Exception as e:
            print(f"   ❌ Error creating '{title}': {str(e)}")
            return None

    def create_post(self, title, content, excerpt=None):
        """Create a WordPress blog post"""
        post_data = {
            'title': title,
            'content': content,
            'status': 'publish',
            'type': 'post'
        }
        
        if excerpt:
            post_data['excerpt'] = excerpt
            
        try:
            response = requests.post(
                f"{self.api_url}/posts",
                auth=self.auth,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post = response.json()
                print(f"   ✅ Created: {title} (ID: {post['id']})")
                return post
            else:
                print(f"   ❌ Failed: {title} - HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error creating '{title}': {str(e)}")
            return None

    def create_all_content(self):
        """Create all pages and posts"""
        
        # Test connection first
        if not self.test_connection():
            print("\n❌ Cannot proceed without valid connection")
            print("\n💡 Troubleshooting Tips:")
            print("   1. Create an Application Password in WordPress:")
            print("      Go to Users > Profile > Application Passwords")
            print("   2. Update your .env file with the new password")
            print("   3. Make sure your WordPress site allows REST API access")
            return False
        
        print("\n📝 Creating Pages...")
        print("-" * 60)
        
        # Homepage
        homepage_content = """
        <h1>Welcome to SphereVista360</h1>
        <p class="lead">Your Gateway to Financial Innovation</p>
        
        <p>At SphereVista360, we provide cutting-edge insights into the intersection of finance and technology. Our expert analysis helps businesses navigate the rapidly evolving financial landscape.</p>
        
        <div class="features">
            <h3>🔹 Financial Technology Insights</h3>
            <p>Stay ahead with the latest FinTech trends and innovations.</p>
            
            <h3>🔹 Investment Strategy Analysis</h3>
            <p>Data-driven insights for informed investment decisions.</p>
            
            <h3>🔹 Digital Transformation Guidance</h3>
            <p>Navigate the digital revolution in financial services.</p>
            
            <h3>🔹 Market Intelligence Reports</h3>
            <p>Comprehensive analysis of market trends and opportunities.</p>
        </div>
        
        <p><strong>Explore our latest articles and discover how technology is reshaping the future of finance.</strong></p>
        """
        
        homepage = self.create_page("Homepage", homepage_content, "home")
        
        # About Page
        about_content = """
        <h2>About SphereVista360</h2>
        
        <p><strong>SphereVista360 is a leading source of financial technology insights and analysis.</strong> Our team of experts combines deep industry knowledge with cutting-edge technology understanding to deliver actionable intelligence.</p>
        
        <h3>Our Mission</h3>
        <p>To empower businesses and individuals with the knowledge they need to thrive in the digital financial ecosystem.</p>
        
        <h3>Our Expertise</h3>
        <ul>
            <li><strong>Financial Technology (FinTech)</strong> - Emerging payment solutions and digital banking</li>
            <li><strong>Investment Management</strong> - Portfolio optimization and risk assessment</li>
            <li><strong>Regulatory Technology</strong> - Compliance automation and reporting</li>
            <li><strong>Blockchain</strong> - Distributed ledger technology and digital assets</li>
            <li><strong>AI in Finance</strong> - Machine learning applications and predictive analytics</li>
        </ul>
        """
        
        self.create_page("About", about_content, "about")
        
        # Services Page
        services_content = """
        <h2>Our Services</h2>
        
        <p>SphereVista360 offers comprehensive financial technology consulting and analysis services:</p>
        
        <h3>✅ Market Research & Analysis</h3>
        <p>In-depth research on emerging financial technologies and market trends.</p>
        
        <h3>✅ Technology Strategy Consulting</h3>
        <p>Strategic guidance for financial institutions adopting new technologies.</p>
        
        <h3>✅ Investment Intelligence</h3>
        <p>Data-driven insights for informed investment decisions.</p>
        
        <h3>✅ Regulatory Compliance</h3>
        <p>Navigate complex regulatory requirements in the digital age.</p>
        """
        
        self.create_page("Services", services_content, "services")
        
        # Contact Page
        contact_content = """
        <h2>Contact SphereVista360</h2>
        
        <p>We'd love to hear from you. Contact us for inquiries about our services, partnership opportunities, or media requests.</p>
        
        <p>📧 Email: contact@spherevista360.com<br>
        🌐 Website: www.spherevista360.com<br>
        💼 Business: business@spherevista360.com</p>
        
        <h3>Business Hours</h3>
        <p>Monday - Friday: 9:00 AM - 6:00 PM<br>
        Saturday: 10:00 AM - 2:00 PM<br>
        Sunday: Closed</p>
        """
        
        self.create_page("Contact", contact_content, "contact")
        
        print("\n📰 Creating Blog Posts...")
        print("-" * 60)
        
        # Blog Post 1
        self.create_post(
            "The Future of Digital Banking: Trends to Watch in 2025",
            """<p>The financial services industry is experiencing unprecedented transformation as digital technologies reshape traditional banking models.</p>
            
            <h3>Key Trends Shaping Digital Banking</h3>
            <p><strong>1. Artificial Intelligence</strong> - AI-powered fraud detection and personalized customer experiences.</p>
            <p><strong>2. Open Banking</strong> - API ecosystems enabling seamless integration of services.</p>
            <p><strong>3. Blockchain</strong> - Streamlining cross-border payments and improving transparency.</p>
            <p><strong>4. Cybersecurity</strong> - Zero-trust architectures and biometric authentication.</p>""",
            "Explore the latest innovations reshaping the banking industry."
        )
        
        # Blog Post 2
        self.create_post(
            "AI in Investment Management: Opportunities and Challenges",
            """<p>Artificial Intelligence is revolutionizing investment management with unprecedented capabilities in portfolio optimization and risk assessment.</p>
            
            <h3>AI Applications</h3>
            <p><strong>Automated Portfolio Management</strong> - Robo-advisors creating and managing investment portfolios.</p>
            <p><strong>Predictive Analytics</strong> - Machine learning models analyzing market data and trends.</p>
            <p><strong>Risk Management</strong> - Real-time portfolio risk assessment.</p>""",
            "How AI is transforming investment strategies and portfolio management."
        )
        
        # Blog Post 3
        self.create_post(
            "Regulatory Technology: Streamlining Compliance in Finance",
            """<p>RegTech is transforming compliance from a cost center into a competitive advantage.</p>
            
            <h3>RegTech Solutions</h3>
            <p><strong>Automated Monitoring</strong> - AI-powered continuous compliance monitoring.</p>
            <p><strong>Regulatory Reporting</strong> - Automated report generation in required formats.</p>
            <p><strong>Risk Management</strong> - Advanced analytics for identifying and managing risks.</p>""",
            "How RegTech solutions help financial institutions navigate regulatory landscapes."
        )
        
        print("\n" + "=" * 60)
        print("🎉 Content Creation Complete!")
        print("=" * 60)
        
        if homepage:
            print(f"\n📋 Next Steps:")
            print(f"   1. Set static homepage: Settings > Reading")
            print(f"      Homepage ID: {homepage['id']}")
            print(f"   2. Create menu: Appearance > Menus")
            print(f"   3. Upload logo: Appearance > Customize")
            print(f"   4. Visit your site to see the new content!")
            print(f"\n🌐 Your site: {self.base_url}")
        
        return True

def main():
    """Main execution"""
    try:
        api = WordPressAPI()
        api.create_all_content()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Please ensure your .env file has:")
        print("   WORDPRESS_BASE_URL=https://yoursite.com")
        print("   WORDPRESS_USERNAME=your_username")
        print("   WORDPRESS_PASSWORD=your_password")
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()