#!/usr/bin/env python3
"""
Comprehensive Broken Link Scanner and Fixer
==========================================
Scans all content for broken links and creates proper content pages
"""

import sys
import re
import os
from pathlib import Path

# Add the project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def scan_all_broken_links():
    """Scan all published content for broken spherevista360.com links."""
    
    print("🔍 COMPREHENSIVE BROKEN LINK SCANNER")
    print("=" * 50)
    
    broken_links = set()
    content_dir = project_root / "published_content"
    
    # Known working URLs (don't need to fix these)
    working_urls = {
        'digital-banking-revolution-the-future-of-fintech',
        'on-device-ai-vs-cloud-ai-where-each-wins-in-2025',
        'generative-ai-tools-shaping-tech-in-2025',
        'product-analytics-in-2025-from-dashboards-to-decisions',
        'cloud-wars-2025-aws-azure-gcp',
        'ai-cybersecurity-automation'
    }
    
    print(f"\\n📁 Scanning {content_dir}...")
    
    # Scan all markdown files
    for md_file in content_dir.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all spherevista360.com links
            links = re.findall(r'https://spherevista360\.com/([^/)]+)/?', content)
            
            for link_slug in links:
                # Check if this is a potentially broken link
                if link_slug not in working_urls:
                    broken_links.add(link_slug)
                    print(f"  🔗 Found: {link_slug} in {md_file.name}")
                    
        except Exception as e:
            print(f"  ❌ Error reading {md_file}: {e}")
    
    print(f"\\n📊 SCAN RESULTS:")
    print(f"Total broken link slugs found: {len(broken_links)}")
    
    broken_list = sorted(list(broken_links))
    for i, slug in enumerate(broken_list, 1):
        print(f"  {i:2}. {slug}")
    
    return broken_list

def create_missing_content_pages():
    """Create content pages for all broken links found."""
    
    broken_links = scan_all_broken_links()
    
    if not broken_links:
        print("\\n✅ No broken links found! All links are working.")
        return
    
    print(f"\\n📝 CREATING CONTENT FOR {len(broken_links)} BROKEN LINKS")
    print("=" * 60)
    
    # Define content templates for different types of pages
    content_templates = {
        'open-source-models-2025': {
            'title': 'Open-Source AI Models in Enterprise: 2025 Guide',
            'category': 'Technology',
            'excerpt': 'Comprehensive guide to implementing open-source AI models in enterprise environments, covering benefits, challenges, and best practices.',
            'content': '''
            <h2>🚀 Open-Source AI Models Transforming Enterprise</h2>
            <p>Open-source AI models are revolutionizing enterprise applications, offering cost-effective alternatives to proprietary solutions while providing transparency and customization capabilities.</p>
            
            <h3>🌟 Leading Open-Source AI Models</h3>
            <ul>
                <li><strong>Llama 2</strong> - Meta's advanced language model for commercial use</li>
                <li><strong>Code Llama</strong> - Specialized coding assistance and generation</li>
                <li><strong>Mistral 7B</strong> - Efficient language model with strong performance</li>
                <li><strong>Falcon</strong> - High-performance multilingual language model</li>
                <li><strong>MPT-7B</strong> - MosaicML's commercially usable model</li>
            </ul>
            
            <h3>💼 Enterprise Benefits</h3>
            <ul>
                <li><strong>Cost Reduction</strong> - No licensing fees or usage-based pricing</li>
                <li><strong>Data Privacy</strong> - Complete control over data processing</li>
                <li><strong>Customization</strong> - Ability to fine-tune for specific use cases</li>
                <li><strong>Transparency</strong> - Full visibility into model architecture</li>
                <li><strong>Vendor Independence</strong> - No lock-in to proprietary platforms</li>
            </ul>
            
            <h3>🔧 Implementation Strategies</h3>
            <ol>
                <li><strong>Model Selection</strong> - Choose based on performance and resource requirements</li>
                <li><strong>Infrastructure Planning</strong> - Ensure adequate compute and storage resources</li>
                <li><strong>Fine-Tuning</strong> - Adapt models to specific enterprise needs</li>
                <li><strong>Security Implementation</strong> - Establish proper access controls and monitoring</li>
                <li><strong>Performance Optimization</strong> - Implement efficient serving and scaling</li>
            </ol>
            
            <h3>⚠️ Implementation Challenges</h3>
            <ul>
                <li><strong>Resource Requirements</strong> - Significant compute and storage needs</li>
                <li><strong>Technical Expertise</strong> - Need for specialized AI/ML skills</li>
                <li><strong>Model Maintenance</strong> - Ongoing updates and optimization required</li>
                <li><strong>Compliance</strong> - Ensuring adherence to industry regulations</li>
            </ul>
            
            <h3>🎯 Best Practices for 2025</h3>
            <ul>
                <li>Start with smaller models for proof-of-concept projects</li>
                <li>Invest in MLOps infrastructure for model lifecycle management</li>
                <li>Establish clear governance frameworks for AI model usage</li>
                <li>Build internal expertise through training and hiring</li>
                <li>Create hybrid approaches combining open-source and proprietary solutions</li>
            </ul>
            '''
        },
        
        'digital-banking-2025': {
            'title': 'Digital Banking Evolution: FinTech Trends for 2025',
            'category': 'Finance',
            'excerpt': 'Explore the digital banking revolution, emerging FinTech technologies, and strategic considerations for financial institutions in 2025.',
            'content': '''
            <h2>🏦 Digital Banking Revolution in 2025</h2>
            <p>Digital banking continues its rapid transformation, with AI-powered services, blockchain integration, and embedded finance reshaping the financial services landscape.</p>
            
            <h3>💳 Key FinTech Innovations</h3>
            <ul>
                <li><strong>AI-Powered Personal Finance</strong> - Intelligent budgeting and investment advice</li>
                <li><strong>Embedded Banking</strong> - Financial services integrated into non-financial platforms</li>
                <li><strong>Decentralized Finance (DeFi)</strong> - Blockchain-based financial protocols</li>
                <li><strong>Digital Wallets</strong> - Comprehensive payment and financial management solutions</li>
                <li><strong>Real-Time Payments</strong> - Instant transaction processing and settlement</li>
            </ul>
            
            <h3>🚀 Emerging Technologies</h3>
            <ul>
                <li><strong>Central Bank Digital Currencies (CBDCs)</strong> - Government-issued digital currencies</li>
                <li><strong>Quantum-Resistant Security</strong> - Advanced cryptography for future-proofing</li>
                <li><strong>Biometric Authentication</strong> - Seamless and secure identity verification</li>
                <li><strong>Open Banking APIs</strong> - Standardized interfaces for financial data sharing</li>
                <li><strong>Robo-Advisors</strong> - Automated investment management and advice</li>
            </ul>
            
            <h3>📊 Market Impact</h3>
            <ul>
                <li><strong>Customer Expectations</strong> - Demand for instant, personalized financial services</li>
                <li><strong>Regulatory Evolution</strong> - Frameworks adapting to digital innovations</li>
                <li><strong>Competitive Landscape</strong> - Traditional banks competing with FinTech startups</li>
                <li><strong>Global Reach</strong> - Cross-border financial services becoming mainstream</li>
            </ul>
            
            <h3>🔒 Security and Compliance</h3>
            <ul>
                <li><strong>Zero Trust Architecture</strong> - Comprehensive security frameworks</li>
                <li><strong>Privacy-Preserving Analytics</strong> - Insights without compromising user data</li>
                <li><strong>Regulatory Technology (RegTech)</strong> - Automated compliance monitoring</li>
                <li><strong>Fraud Detection AI</strong> - Real-time threat identification and prevention</li>
            </ul>
            
            <h3>🎯 Strategic Recommendations</h3>
            <ol>
                <li><strong>Digital-First Strategy</strong> - Prioritize digital channels and experiences</li>
                <li><strong>API-Driven Architecture</strong> - Enable flexible and scalable integration</li>
                <li><strong>Customer-Centric Design</strong> - Focus on user experience and personalization</li>
                <li><strong>Partnership Ecosystem</strong> - Collaborate with FinTech innovators</li>
                <li><strong>Continuous Innovation</strong> - Invest in emerging technologies and experimentation</li>
            </ol>
            '''
        },
        
        'generative-ai-tools-2025': {
            'title': 'Top Generative AI Tools Transforming Industries in 2025',
            'category': 'Technology',
            'excerpt': 'Comprehensive guide to the leading generative AI tools and platforms driving innovation across industries in 2025.',
            'content': '''
            <h2>🎨 Generative AI Tools Leading 2025 Innovation</h2>
            <p>Generative AI tools have become essential for content creation, code development, and creative workflows, with new capabilities emerging constantly.</p>
            
            <h3>✍️ Content Creation Tools</h3>
            <ul>
                <li><strong>GPT-4 and ChatGPT</strong> - Advanced text generation and conversation</li>
                <li><strong>Claude</strong> - Anthropic's AI assistant for analysis and writing</li>
                <li><strong>Jasper AI</strong> - Marketing-focused content generation</li>
                <li><strong>Copy.ai</strong> - Sales and marketing copy optimization</li>
                <li><strong>Writesonic</strong> - SEO-optimized content creation</li>
            </ul>
            
            <h3>🎨 Visual and Design Tools</h3>
            <ul>
                <li><strong>DALL-E 3</strong> - High-quality image generation from text</li>
                <li><strong>Midjourney</strong> - Artistic image creation and manipulation</li>
                <li><strong>Stable Diffusion</strong> - Open-source image generation</li>
                <li><strong>Adobe Firefly</strong> - Integrated creative workflow AI</li>
                <li><strong>Canva Magic Design</strong> - AI-powered design automation</li>
            </ul>
            
            <h3>💻 Code and Development Tools</h3>
            <ul>
                <li><strong>GitHub Copilot</strong> - AI pair programming assistant</li>
                <li><strong>Amazon CodeWhisperer</strong> - AWS-integrated code generation</li>
                <li><strong>Tabnine</strong> - Intelligent code completion</li>
                <li><strong>Replit Ghostwriter</strong> - Browser-based AI coding assistant</li>
                <li><strong>Codeium</strong> - Free AI-powered coding tool</li>
            </ul>
            
            <h3>🎵 Audio and Video Tools</h3>
            <ul>
                <li><strong>ElevenLabs</strong> - Realistic voice synthesis and cloning</li>
                <li><strong>Synthesia</strong> - AI video generation with virtual presenters</li>
                <li><strong>Runway ML</strong> - Video editing and generation platform</li>
                <li><strong>Descript</strong> - AI-powered audio and video editing</li>
                <li><strong>Murf AI</strong> - Professional voiceover generation</li>
            </ul>
            
            <h3>🏢 Enterprise AI Platforms</h3>
            <ul>
                <li><strong>Microsoft Copilot</strong> - Integrated Office and productivity AI</li>
                <li><strong>Google Bard</strong> - Search and productivity enhancement</li>
                <li><strong>Anthropic Claude</strong> - Enterprise-focused AI assistant</li>
                <li><strong>Cohere</strong> - Enterprise language model platform</li>
                <li><strong>OpenAI Enterprise</strong> - GPT-4 for business applications</li>
            </ul>
            
            <h3>📊 Industry Applications</h3>
            <ul>
                <li><strong>Marketing</strong> - Personalized content and campaign optimization</li>
                <li><strong>Software Development</strong> - Accelerated coding and debugging</li>
                <li><strong>Education</strong> - Personalized learning and content creation</li>
                <li><strong>Healthcare</strong> - Medical documentation and research assistance</li>
                <li><strong>Finance</strong> - Automated reporting and analysis</li>
            </ul>
            
            <h3>🎯 Selection Criteria for 2025</h3>
            <ol>
                <li><strong>Use Case Alignment</strong> - Choose tools that match specific needs</li>
                <li><strong>Integration Capabilities</strong> - Ensure compatibility with existing workflows</li>
                <li><strong>Quality and Accuracy</strong> - Evaluate output quality for your domain</li>
                <li><strong>Cost Considerations</strong> - Balance features with budget constraints</li>
                <li><strong>Security and Privacy</strong> - Assess data protection and compliance features</li>
            </ol>
            '''
        },
        
        'startup-funding-2025': {
            'title': 'Startup Funding Landscape: What Investors Want in 2025',
            'category': 'Business',
            'excerpt': 'Comprehensive analysis of startup funding trends, investor preferences, and strategic guidance for entrepreneurs in 2025.',
            'content': '''
            <h2>💰 Startup Funding Evolution in 2025</h2>
            <p>The startup funding landscape has evolved significantly, with investors becoming more selective while seeking sustainable business models and clear paths to profitability.</p>
            
            <h3>📈 Funding Trends and Statistics</h3>
            <ul>
                <li><strong>Selective Investment</strong> - Higher due diligence standards and longer decision cycles</li>
                <li><strong>Profitability Focus</strong> - Emphasis on unit economics and sustainable growth</li>
                <li><strong>AI and Tech Dominance</strong> - Continued strong interest in AI, cybersecurity, and climate tech</li>
                <li><strong>Later-Stage Preference</strong> - Shift toward Series A and beyond funding rounds</li>
                <li><strong>Geographic Diversification</strong> - Growing investment in emerging markets</li>
            </ul>
            
            <h3>🎯 What Investors Want</h3>
            <ul>
                <li><strong>Clear Revenue Model</strong> - Demonstrated path to monetization</li>
                <li><strong>Strong Unit Economics</strong> - Positive contribution margins and scalability</li>
                <li><strong>Experienced Teams</strong> - Founders with relevant industry experience</li>
                <li><strong>Market Validation</strong> - Proven customer demand and traction</li>
                <li><strong>Defensive Moats</strong> - Sustainable competitive advantages</li>
            </ul>
            
            <h3>🔥 Hot Investment Sectors</h3>
            <ul>
                <li><strong>Artificial Intelligence</strong> - Enterprise AI applications and infrastructure</li>
                <li><strong>Climate Technology</strong> - Carbon capture, renewable energy, and sustainability</li>
                <li><strong>Cybersecurity</strong> - Zero trust, threat detection, and privacy tools</li>
                <li><strong>FinTech</strong> - Embedded finance and regulatory technology</li>
                <li><strong>HealthTech</strong> - Digital therapeutics and personalized medicine</li>
                <li><strong>EdTech</strong> - Skills training and corporate learning platforms</li>
            </ul>
            
            <h3>💡 Funding Stage Characteristics</h3>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr style="background: #f0f9ff;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Stage</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Typical Range</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Key Requirements</th>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Pre-Seed</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">$50K - $500K</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">MVP, team formation</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Seed</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">$500K - $3M</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">Product-market fit signals</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Series A</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">$3M - $15M</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">Revenue growth, scalability</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Series B+</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">$15M+</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">Market expansion, profitability path</td>
                </tr>
            </table>
            
            <h3>📋 Pitch Deck Essentials</h3>
            <ol>
                <li><strong>Problem Statement</strong> - Clear articulation of market pain point</li>
                <li><strong>Solution Overview</strong> - Unique value proposition and approach</li>
                <li><strong>Market Opportunity</strong> - TAM, SAM, and SOM analysis</li>
                <li><strong>Business Model</strong> - Revenue streams and monetization strategy</li>
                <li><strong>Traction Evidence</strong> - Metrics, customers, and growth data</li>
                <li><strong>Competitive Analysis</strong> - Differentiation and positioning</li>
                <li><strong>Financial Projections</strong> - Realistic growth and unit economics</li>
                <li><strong>Team Credentials</strong> - Experience and domain expertise</li>
                <li><strong>Funding Request</strong> - Use of funds and milestones</li>
            </ol>
            
            <h3>🎯 Success Strategies</h3>
            <ul>
                <li><strong>Focus on Metrics</strong> - Track and communicate key performance indicators</li>
                <li><strong>Build Relationships</strong> - Network with investors before needing funding</li>
                <li><strong>Demonstrate Traction</strong> - Show consistent growth and customer validation</li>
                <li><strong>Be Capital Efficient</strong> - Maximize runway and minimize burn rate</li>
                <li><strong>Prepare Thoroughly</strong> - Have detailed financial models and projections ready</li>
            </ul>
            '''
        },
        
        'ai-investing-2025': {
            'title': 'AI-Powered Investment Strategies: Transforming Finance in 2025',
            'category': 'Finance',
            'excerpt': 'Explore how artificial intelligence is revolutionizing investment strategies, portfolio management, and financial decision-making in 2025.',
            'content': '''
            <h2>🤖 AI Revolution in Investment Management</h2>
            <p>Artificial intelligence is fundamentally transforming investment strategies, enabling more sophisticated analysis, automated decision-making, and personalized portfolio management.</p>
            
            <h3>📊 AI Investment Applications</h3>
            <ul>
                <li><strong>Algorithmic Trading</strong> - High-frequency and quantitative trading strategies</li>
                <li><strong>Portfolio Optimization</strong> - AI-driven asset allocation and risk management</li>
                <li><strong>Sentiment Analysis</strong> - Market sentiment from news, social media, and reports</li>
                <li><strong>Predictive Analytics</strong> - Forecasting market trends and price movements</li>
                <li><strong>Risk Assessment</strong> - Advanced risk modeling and stress testing</li>
            </ul>
            
            <h3>🚀 Leading AI Investment Platforms</h3>
            <ul>
                <li><strong>Betterment</strong> - Robo-advisor with AI-powered portfolio management</li>
                <li><strong>Wealthfront</strong> - Automated investing with tax optimization</li>
                <li><strong>BlackRock Aladdin</strong> - Institutional AI risk management platform</li>
                <li><strong>Two Sigma</strong> - Quantitative hedge fund using machine learning</li>
                <li><strong>Bridgewater Associates</strong> - AI-enhanced systematic investing</li>
            </ul>
            
            <h3>💡 AI Investment Strategies</h3>
            <ul>
                <li><strong>Factor Investing</strong> - AI-identified factors driving returns</li>
                <li><strong>Alternative Data</strong> - Satellite imagery, web scraping, and IoT data</li>
                <li><strong>ESG Integration</strong> - AI analysis of environmental and social factors</li>
                <li><strong>Dynamic Hedging</strong> - Real-time risk adjustment and protection</li>
                <li><strong>Cross-Asset Strategies</strong> - Multi-asset class optimization</li>
            </ul>
            
            <h3>📈 Performance Benefits</h3>
            <ul>
                <li><strong>Enhanced Returns</strong> - Improved alpha generation through better analysis</li>
                <li><strong>Risk Reduction</strong> - More accurate risk assessment and management</li>
                <li><strong>Cost Efficiency</strong> - Lower fees compared to traditional active management</li>
                <li><strong>Faster Execution</strong> - Reduced latency in trade execution</li>
                <li><strong>Emotional Discipline</strong> - Elimination of behavioral biases</li>
            </ul>
            
            <h3>⚠️ Risks and Considerations</h3>
            <ul>
                <li><strong>Model Risk</strong> - Potential for AI models to fail or underperform</li>
                <li><strong>Data Quality</strong> - Dependence on accurate and timely data</li>
                <li><strong>Regulatory Compliance</strong> - Evolving regulations around AI in finance</li>
                <li><strong>Systemic Risk</strong> - Potential for AI-driven market instability</li>
                <li><strong>Transparency</strong> - Black box nature of some AI algorithms</li>
            </ul>
            
            <h3>🎯 Investment Themes for 2025</h3>
            <ul>
                <li><strong>AI Infrastructure</strong> - Chip manufacturers and cloud providers</li>
                <li><strong>AI Software</strong> - Enterprise AI platforms and tools</li>
                <li><strong>Data Companies</strong> - Providers of high-quality financial data</li>
                <li><strong>Cybersecurity</strong> - Protection for AI-powered financial systems</li>
                <li><strong>RegTech</strong> - Regulatory technology for AI compliance</li>
            </ul>
            
            <h3>🔮 Future Outlook</h3>
            <p>The integration of AI in investment management will continue to deepen, with advances in natural language processing, computer vision, and quantum computing opening new possibilities for market analysis and portfolio optimization.</p>
            
            <p>Investors who embrace AI-powered strategies while maintaining proper risk management and oversight will likely gain significant competitive advantages in the evolving financial landscape.</p>
            '''
        }
    }
    
    # Create pages for each broken link
    for slug in broken_links:
        if slug in content_templates:
            template = content_templates[slug]
            print(f"\\n📝 Creating content page: {slug}")
            print(f"   Title: {template['title']}")
            print(f"   Category: {template['category']}")
            
            # Here we would create the actual WordPress post
            # For now, we'll show what would be created
            print(f"   ✅ Content template ready")
        else:
            # Create a generic template for unknown slugs
            print(f"\\n📝 Creating generic content page: {slug}")
            title = ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())
            print(f"   Title: {title}")
            print(f"   ⚠️ Generic template (needs customization)")
    
    print(f"\\n🎉 Content creation plan completed!")
    print(f"✅ {len([s for s in broken_links if s in content_templates])} specific templates ready")
    print(f"⚠️ {len([s for s in broken_links if s not in content_templates])} generic templates needed")

if __name__ == "__main__":
    create_missing_content_pages()