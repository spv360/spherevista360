#!/usr/bin/env python3
"""
WordPress Theme Auto-Setup via REST API
Automatically configures the SphereVista360 theme with content, menus, and settings
"""

import requests
import json
import base64
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WordPressThemeSetup:
    def __init__(self):
        self.base_url = os.getenv('WORDPRESS_BASE_URL', '')
        self.username = os.getenv('WORDPRESS_USERNAME', '')
        self.password = os.getenv('WORDPRESS_PASSWORD', '')
        
        if not all([self.base_url, self.username, self.password]):
            print("❌ Missing WordPress credentials in .env file")
            print("Please set: WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD")
            return
            
        # Create authentication header
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode('utf-8')
        self.headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json'
        }
        
        self.api_url = f"{self.base_url.rstrip('/')}/wp-json/wp/v2"
        
        print(f"🔧 WordPress Theme Setup Tool")
        print(f"📍 Site: {self.base_url}")
        print(f"👤 User: {self.username}")
        print("=" * 50)

    def test_connection(self):
        """Test WordPress API connection"""
        try:
            response = requests.get(f"{self.api_url}/users/me", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected successfully as: {user_data.get('name', 'Unknown')}")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
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
            response = requests.post(f"{self.api_url}/pages", 
                                   headers=self.headers, 
                                   json=page_data)
            
            if response.status_code == 201:
                page = response.json()
                print(f"✅ Created page: {title} (ID: {page['id']})")
                return page
            else:
                print(f"❌ Failed to create page '{title}': {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error creating page '{title}': {str(e)}")
            return None

    def create_post(self, title, content, excerpt=None, featured_image=None):
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
            response = requests.post(f"{self.api_url}/posts", 
                                   headers=self.headers, 
                                   json=post_data)
            
            if response.status_code == 201:
                post = response.json()
                print(f"✅ Created post: {title} (ID: {post['id']})")
                return post
            else:
                print(f"❌ Failed to create post '{title}': {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error creating post '{title}': {str(e)}")
            return None

    def setup_homepage_content(self):
        """Create homepage and essential pages"""
        print("\n📝 Creating Essential Pages...")
        
        # Homepage
        homepage_content = """
        <div class="hero-section">
            <h1>Welcome to SphereVista360</h1>
            <p class="hero-subtitle">Your Gateway to Financial Innovation</p>
            
            <div class="hero-description">
                <p>At SphereVista360, we provide cutting-edge insights into the intersection of finance and technology. Our expert analysis helps businesses navigate the rapidly evolving financial landscape.</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <h3>🔹 Financial Technology Insights</h3>
                    <p>Stay ahead with the latest FinTech trends and innovations.</p>
                </div>
                
                <div class="feature-card">
                    <h3>🔹 Investment Strategy Analysis</h3>
                    <p>Data-driven insights for informed investment decisions.</p>
                </div>
                
                <div class="feature-card">
                    <h3>🔹 Digital Transformation Guidance</h3>
                    <p>Navigate the digital revolution in financial services.</p>
                </div>
                
                <div class="feature-card">
                    <h3>🔹 Market Intelligence Reports</h3>
                    <p>Comprehensive analysis of market trends and opportunities.</p>
                </div>
            </div>
            
            <div class="cta-section">
                <p><strong>Explore our latest articles and discover how technology is reshaping the future of finance.</strong></p>
                <a href="/blog" class="cta-button">Read Our Latest Insights</a>
            </div>
        </div>
        """
        
        homepage = self.create_page("Homepage", homepage_content, "homepage")
        
        # About Page
        about_content = """
        <h2>About SphereVista360</h2>
        
        <p><strong>SphereVista360 is a leading source of financial technology insights and analysis.</strong> Our team of experts combines deep industry knowledge with cutting-edge technology understanding to deliver actionable intelligence.</p>
        
        <h3>Our Mission</h3>
        <p>To empower businesses and individuals with the knowledge they need to thrive in the digital financial ecosystem.</p>
        
        <h3>Our Expertise</h3>
        <ul>
            <li><strong>Financial Technology (FinTech)</strong> - Emerging payment solutions, digital banking, and financial apps</li>
            <li><strong>Digital Banking Solutions</strong> - Cloud infrastructure, API integration, and customer experience</li>
            <li><strong>Investment Management</strong> - Portfolio optimization, risk assessment, and automated trading</li>
            <li><strong>Regulatory Technology (RegTech)</strong> - Compliance automation and regulatory reporting</li>
            <li><strong>Blockchain and Cryptocurrency</strong> - Distributed ledger technology and digital assets</li>
            <li><strong>AI in Finance</strong> - Machine learning applications and predictive analytics</li>
        </ul>
        
        <h3>Why Choose SphereVista360?</h3>
        <p>Our unique perspective comes from years of experience in both traditional finance and cutting-edge technology. We translate complex concepts into actionable strategies that drive real business results.</p>
        """
        
        self.create_page("About", about_content, "about")
        
        # Services Page
        services_content = """
        <h2>Our Services</h2>
        
        <p>SphereVista360 offers comprehensive financial technology consulting and analysis services:</p>
        
        <div class="services-grid">
            <div class="service-item">
                <h3>✅ Market Research & Analysis</h3>
                <p>In-depth research on emerging financial technologies and market trends. We provide detailed reports on market opportunities, competitive landscapes, and growth projections.</p>
            </div>
            
            <div class="service-item">
                <h3>✅ Technology Strategy Consulting</h3>
                <p>Strategic guidance for financial institutions adopting new technologies. From digital transformation roadmaps to technology vendor selection.</p>
            </div>
            
            <div class="service-item">
                <h3>✅ Investment Intelligence</h3>
                <p>Data-driven insights for informed investment decisions. Market analysis, risk assessment, and portfolio optimization strategies.</p>
            </div>
            
            <div class="service-item">
                <h3>✅ Regulatory Compliance</h3>
                <p>Navigate complex regulatory requirements in the digital age. Compliance strategy, regulatory technology solutions, and risk management.</p>
            </div>
        </div>
        
        <div class="contact-cta">
            <h3>Ready to Get Started?</h3>
            <p>Contact us to learn how we can help your organization succeed in the digital financial landscape.</p>
            <a href="/contact" class="cta-button">Get In Touch</a>
        </div>
        """
        
        self.create_page("Services", services_content, "services")
        
        # Contact Page
        contact_content = """
        <h2>Contact SphereVista360</h2>
        
        <p><strong>We'd love to hear from you.</strong> Contact us for inquiries about our services, partnership opportunities, or media requests.</p>
        
        <div class="contact-info">
            <div class="contact-method">
                <h3>📧 Email</h3>
                <p>contact@spherevista360.com</p>
            </div>
            
            <div class="contact-method">
                <h3>🌐 Website</h3>
                <p>www.spherevista360.com</p>
            </div>
            
            <div class="contact-method">
                <h3>💼 Business Inquiries</h3>
                <p>business@spherevista360.com</p>
            </div>
            
            <div class="contact-method">
                <h3>📰 Media Requests</h3>
                <p>media@spherevista360.com</p>
            </div>
        </div>
        
        <div class="business-hours">
            <h3>Business Hours</h3>
            <ul>
                <li><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM</li>
                <li><strong>Saturday:</strong> 10:00 AM - 2:00 PM</li>
                <li><strong>Sunday:</strong> Closed</li>
            </ul>
        </div>
        
        <div class="contact-form-note">
            <p><em>For immediate assistance, please use the contact form below or send us an email. We typically respond within 24 hours during business days.</em></p>
        </div>
        """
        
        self.create_page("Contact", contact_content, "contact")
        
        return homepage

    def setup_blog_content(self):
        """Create sample blog posts"""
        print("\n📰 Creating Sample Blog Posts...")
        
        # Blog Post 1
        post1_content = """
        <p>The financial services industry is experiencing unprecedented transformation as digital technologies reshape traditional banking models. From mobile-first banking to AI-powered financial advisory services, the landscape is evolving rapidly.</p>
        
        <h3>Key Trends Shaping Digital Banking in 2025</h3>
        
        <h4>1. Artificial Intelligence and Machine Learning</h4>
        <p>Banks are leveraging AI for fraud detection, risk assessment, and personalized customer experiences. Machine learning algorithms analyze spending patterns to provide tailored financial advice and detect suspicious activities in real-time.</p>
        
        <h4>2. Open Banking and API Ecosystems</h4>
        <p>Open banking initiatives are creating new opportunities for collaboration between traditional banks and fintech companies. APIs enable seamless integration of third-party services, enhancing customer choice and innovation.</p>
        
        <h4>3. Blockchain and Digital Currencies</h4>
        <p>Central Bank Digital Currencies (CBDCs) are gaining momentum globally, while blockchain technology promises to streamline cross-border payments and improve transaction transparency.</p>
        
        <h4>4. Enhanced Cybersecurity Measures</h4>
        <p>As digital banking grows, so does the importance of robust cybersecurity. Banks are implementing zero-trust architectures and biometric authentication to protect customer data.</p>
        
        <h3>What This Means for Businesses</h3>
        <p>Organizations must adapt to these changes by investing in digital infrastructure, partnering with fintech companies, and prioritizing customer experience in their digital transformation strategies.</p>
        
        <p><strong>The future of banking is digital, and those who embrace these trends will be best positioned to thrive in the evolving financial landscape.</strong></p>
        """
        
        self.create_post(
            "The Future of Digital Banking: Trends to Watch in 2025",
            post1_content,
            "Explore the latest innovations reshaping the banking industry, from AI-powered customer service to blockchain-based transactions."
        )
        
        # Blog Post 2
        post2_content = """
        <p>Artificial Intelligence is revolutionizing investment management, offering unprecedented capabilities in portfolio optimization, risk assessment, and market analysis. However, with these opportunities come new challenges that investors and fund managers must navigate carefully.</p>
        
        <h3>AI Applications in Investment Management</h3>
        
        <h4>Automated Portfolio Management</h4>
        <p>Robo-advisors use sophisticated algorithms to create and manage investment portfolios based on individual risk tolerance, financial goals, and market conditions. These systems can rebalance portfolios automatically and provide 24/7 monitoring.</p>
        
        <h4>Predictive Analytics</h4>
        <p>Machine learning models analyze vast amounts of market data, news sentiment, and economic indicators to predict market movements and identify investment opportunities that human analysts might miss.</p>
        
        <h4>Risk Management</h4>
        <p>AI systems can assess portfolio risk in real-time, considering factors such as market volatility, correlation between assets, and macroeconomic conditions to optimize risk-adjusted returns.</p>
        
        <h3>Opportunities for Investors</h3>
        <ul>
            <li><strong>Lower Costs:</strong> Automated processes reduce management fees and operational expenses</li>
            <li><strong>Improved Performance:</strong> Data-driven decisions can lead to better investment outcomes</li>
            <li><strong>Accessibility:</strong> Sophisticated investment strategies become available to retail investors</li>
            <li><strong>Personalization:</strong> AI can tailor investment strategies to individual preferences and circumstances</li>
        </ul>
        
        <h3>Challenges to Consider</h3>
        <ul>
            <li><strong>Black Box Problem:</strong> Complex AI models can be difficult to interpret and explain</li>
            <li><strong>Market Volatility:</strong> AI systems may amplify market movements during periods of high volatility</li>
            <li><strong>Regulatory Compliance:</strong> Ensuring AI-driven decisions meet regulatory requirements</li>
            <li><strong>Data Quality:</strong> AI models are only as good as the data they're trained on</li>
        </ul>
        
        <h3>Best Practices for AI Implementation</h3>
        <p>Successful integration of AI in investment management requires careful consideration of model transparency, regulatory compliance, and human oversight. Organizations should focus on gradual implementation, thorough testing, and maintaining human expertise alongside AI capabilities.</p>
        """
        
        self.create_post(
            "AI in Investment Management: Opportunities and Challenges",
            post2_content,
            "How artificial intelligence is transforming investment strategies and what it means for portfolio management in the digital age."
        )
        
        # Blog Post 3
        post3_content = """
        <p>Regulatory Technology (RegTech) is emerging as a critical solution for financial institutions struggling to keep pace with ever-evolving regulatory requirements. By leveraging advanced technologies, RegTech solutions are transforming compliance from a cost center into a competitive advantage.</p>
        
        <h3>The Regulatory Challenge</h3>
        <p>Financial institutions face an increasingly complex regulatory environment with requirements spanning multiple jurisdictions, frequent policy changes, and severe penalties for non-compliance. Traditional compliance methods are often manual, expensive, and prone to errors.</p>
        
        <h3>How RegTech Addresses These Challenges</h3>
        
        <h4>Automated Compliance Monitoring</h4>
        <p>RegTech solutions use AI and machine learning to continuously monitor transactions, communications, and market activities for regulatory violations. This real-time monitoring significantly reduces the risk of compliance breaches.</p>
        
        <h4>Regulatory Reporting Automation</h4>
        <p>Automated systems can generate regulatory reports in the required formats, ensuring accuracy and timeliness while reducing manual effort. This includes everything from suspicious activity reports to capital adequacy calculations.</p>
        
        <h4>Risk Assessment and Management</h4>
        <p>Advanced analytics help institutions identify, assess, and manage various types of risk, including credit risk, operational risk, and market risk, in compliance with regulatory frameworks.</p>
        
        <h3>Key Benefits of RegTech Implementation</h3>
        <ul>
            <li><strong>Cost Reduction:</strong> Automated processes significantly reduce compliance costs</li>
            <li><strong>Improved Accuracy:</strong> Reduced human error in regulatory reporting and monitoring</li>
            <li><strong>Real-time Monitoring:</strong> Immediate detection of potential compliance issues</li>
            <li><strong>Scalability:</strong> Systems that can adapt to new regulations and growing business volumes</li>
            <li><strong>Enhanced Transparency:</strong> Better audit trails and reporting capabilities</li>
        </ul>
        
        <h3>Implementation Strategies</h3>
        <p>Successful RegTech implementation requires a clear understanding of regulatory requirements, careful vendor selection, and strong change management processes. Organizations should start with pilot programs, focus on high-impact use cases, and ensure adequate staff training.</p>
        
        <h3>The Future of RegTech</h3>
        <p>As regulatory complexity continues to increase, RegTech solutions will become even more sophisticated, incorporating technologies like natural language processing for regulatory interpretation and blockchain for immutable audit trails.</p>
        
        <p><strong>Organizations that embrace RegTech today will be better positioned to navigate the regulatory landscape of tomorrow while maintaining competitive advantages through operational efficiency.</strong></p>
        """
        
        self.create_post(
            "Regulatory Technology: Streamlining Compliance in Finance",
            post3_content,
            "Discover how RegTech solutions are helping financial institutions navigate complex regulatory landscapes more efficiently and cost-effectively."
        )

    def setup_reading_settings(self, homepage_id):
        """Configure WordPress reading settings"""
        print(f"\n⚙️ Configuring Reading Settings...")
        
        # Note: WordPress REST API doesn't directly support changing reading settings
        # This would need to be done via WordPress admin or a custom endpoint
        print("📝 Manual step required: Set homepage in Settings > Reading")
        print(f"   Use page ID: {homepage_id} as static homepage")

    def create_primary_menu(self):
        """Create and configure primary navigation menu"""
        print("\n📋 Setting up Primary Menu...")
        
        # Note: Menu creation via REST API requires custom endpoints or plugins
        # For now, we'll provide instructions for manual setup
        print("📝 Manual step required: Create menu in Appearance > Menus")
        print("   Menu name: 'Primary Navigation'")
        print("   Add pages: Home, About, Services, Blog, Contact")
        print("   Assign to: 'Primary' location")

    def run_full_setup(self):
        """Run the complete theme setup process"""
        print("🚀 Starting Complete Theme Setup...\n")
        
        # Test connection first
        if not self.test_connection():
            return False
        
        # Create pages and get homepage ID
        homepage = self.setup_homepage_content()
        
        # Create blog posts
        self.setup_blog_content()
        
        # Additional setup steps (require manual intervention)
        if homepage:
            self.setup_reading_settings(homepage['id'])
        
        self.create_primary_menu()
        
        print("\n🎉 Theme Setup Complete!")
        print("=" * 50)
        print("✅ Pages created: Homepage, About, Services, Contact")
        print("✅ Blog posts created: 3 sample articles")
        print("📝 Manual steps remaining:")
        print("   1. Set static homepage in Settings > Reading")
        print("   2. Create primary menu in Appearance > Menus")
        print("   3. Upload logo in Appearance > Customize")
        print("   4. Test all functionality")
        
        return True

def main():
    """Main function"""
    setup = WordPressThemeSetup()
    
    if hasattr(setup, 'base_url') and setup.base_url:
        setup.run_full_setup()
    else:
        print("Please configure your WordPress credentials in .env file")

if __name__ == "__main__":
    main()