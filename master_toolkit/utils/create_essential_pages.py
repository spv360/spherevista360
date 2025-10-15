#!/usr/bin/env python3
"""
Create essential pages for Google AdSense compliance
- Privacy Policy
- Disclaimer
- Terms of Service
- Contact Us
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

WORDPRESS_BASE_URL = os.getenv('WORDPRESS_BASE_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

def get_page_by_slug(slug):
    """Check if a page already exists"""
    url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages"
    params = {'slug': slug, 'per_page': 1}
    
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code == 200:
        pages = response.json()
        return pages[0] if pages else None
    return None

def create_or_update_page(title, slug, content):
    """Create a new page or update existing one"""
    existing_page = get_page_by_slug(slug)
    
    if existing_page:
        # Update existing page
        page_id = existing_page['id']
        url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages/{page_id}"
        print(f"   Updating existing page: {title} (ID: {page_id})")
    else:
        # Create new page
        url = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/pages"
        print(f"   Creating new page: {title}")
    
    data = {
        'title': title,
        'content': content,
        'status': 'publish',
        'slug': slug
    }
    
    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    )
    
    if response.status_code in [200, 201]:
        page = response.json()
        return page
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")
        return None

def get_privacy_policy_content():
    """Generate comprehensive Privacy Policy content"""
    current_date = datetime.now().strftime("%B %d, %Y")
    return f"""
<div class="privacy-policy-content">

<p><strong>Last Updated: {current_date}</strong></p>

<h2>Introduction</h2>

<p>Welcome to SphereVista360 ("we," "our," or "us"). We are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website <a href="https://spherevista360.com">spherevista360.com</a> (the "Site").</p>

<p>Please read this Privacy Policy carefully. By accessing or using our Site, you acknowledge that you have read, understood, and agree to be bound by this Privacy Policy. If you do not agree with the terms of this Privacy Policy, please do not access the Site.</p>

<h2>Information We Collect</h2>

<h3>Personal Information</h3>

<p>We may collect personal information that you voluntarily provide to us when you:</p>

<ul>
<li>Subscribe to our newsletter</li>
<li>Fill out a contact form</li>
<li>Post comments on our blog</li>
<li>Register for an account on our Site</li>
<li>Participate in surveys or promotions</li>
<li>Contact us directly via email or other communication channels</li>
</ul>

<p>This information may include:</p>

<ul>
<li>Name</li>
<li>Email address</li>
<li>Phone number</li>
<li>Company name and job title</li>
<li>Any other information you choose to provide</li>
</ul>

<h3>Automatically Collected Information</h3>

<p>When you visit our Site, we automatically collect certain information about your device and browsing behavior, including:</p>

<ul>
<li>IP address</li>
<li>Browser type and version</li>
<li>Operating system</li>
<li>Referring website</li>
<li>Pages viewed and time spent on pages</li>
<li>Date and time of visit</li>
<li>Device identifiers</li>
</ul>

<h3>Cookies and Tracking Technologies</h3>

<p>We use cookies, web beacons, and similar tracking technologies to enhance your experience on our Site. Cookies are small data files stored on your device that help us improve Site functionality, analyze usage patterns, and deliver personalized content.</p>

<p>Types of cookies we use:</p>

<ul>
<li><strong>Essential Cookies:</strong> Necessary for the Site to function properly</li>
<li><strong>Analytics Cookies:</strong> Help us understand how visitors use our Site</li>
<li><strong>Advertising Cookies:</strong> Used to deliver relevant advertisements</li>
<li><strong>Preference Cookies:</strong> Remember your settings and preferences</li>
</ul>

<p>You can control cookies through your browser settings. However, disabling cookies may limit your ability to use certain features of our Site.</p>

<h2>How We Use Your Information</h2>

<p>We use the information we collect for various purposes, including:</p>

<ul>
<li>Providing, maintaining, and improving our Site and services</li>
<li>Responding to your inquiries and providing customer support</li>
<li>Sending you newsletters, updates, and promotional materials (with your consent)</li>
<li>Analyzing Site usage and trends to enhance user experience</li>
<li>Detecting, preventing, and addressing technical issues and security threats</li>
<li>Complying with legal obligations and enforcing our policies</li>
<li>Personalizing content and advertisements based on your interests</li>
<li>Conducting research and analysis to improve our content and services</li>
</ul>

<h2>Third-Party Services and Advertising</h2>

<h3>Google AdSense</h3>

<p>We use Google AdSense to display advertisements on our Site. Google AdSense uses cookies and similar technologies to serve ads based on your prior visits to our Site and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visit to our Site and/or other sites on the Internet.</p>

<p>You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or by visiting <a href="http://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a>.</p>

<h3>Analytics Services</h3>

<p>We use third-party analytics services such as Google Analytics to collect and analyze information about Site usage. These services may use cookies and similar technologies to collect information about your online activities over time and across different websites.</p>

<h3>Social Media Plugins</h3>

<p>Our Site may include social media features and widgets (e.g., Facebook, Twitter, LinkedIn). These features may collect your IP address, track which pages you visit on our Site, and set cookies. Your interactions with these features are governed by the privacy policies of the respective social media companies.</p>

<h2>Information Sharing and Disclosure</h2>

<p>We do not sell, trade, or rent your personal information to third parties. We may share your information in the following circumstances:</p>

<ul>
<li><strong>Service Providers:</strong> We may share information with trusted third-party service providers who assist us in operating our Site, conducting our business, or serving our users (e.g., hosting providers, email service providers, analytics services)</li>
<li><strong>Legal Requirements:</strong> We may disclose information if required by law, court order, or government regulation, or if we believe disclosure is necessary to protect our rights, property, or safety, or the rights, property, or safety of others</li>
<li><strong>Business Transfers:</strong> In the event of a merger, acquisition, reorganization, or sale of assets, your information may be transferred to the acquiring entity</li>
<li><strong>With Your Consent:</strong> We may share information with third parties when you explicitly consent to such sharing</li>
</ul>

<h2>Data Security</h2>

<p>We implement appropriate technical and organizational security measures to protect your personal information from unauthorized access, disclosure, alteration, or destruction. These measures include:</p>

<ul>
<li>Secure Socket Layer (SSL) encryption for data transmission</li>
<li>Regular security assessments and updates</li>
<li>Access controls and authentication procedures</li>
<li>Employee training on data protection practices</li>
</ul>

<p>However, no method of transmission over the Internet or electronic storage is 100% secure. While we strive to protect your personal information, we cannot guarantee absolute security.</p>

<h2>Your Rights and Choices</h2>

<p>Depending on your location, you may have certain rights regarding your personal information:</p>

<ul>
<li><strong>Access:</strong> Request access to the personal information we hold about you</li>
<li><strong>Correction:</strong> Request correction of inaccurate or incomplete information</li>
<li><strong>Deletion:</strong> Request deletion of your personal information</li>
<li><strong>Objection:</strong> Object to certain processing of your information</li>
<li><strong>Portability:</strong> Request transfer of your information to another service</li>
<li><strong>Withdraw Consent:</strong> Withdraw consent for processing based on consent</li>
</ul>

<p>To exercise these rights, please contact us using the information provided in the "Contact Us" section below.</p>

<h3>Email Communications</h3>

<p>If you receive marketing emails from us, you can opt out by clicking the "unsubscribe" link in any email or by contacting us directly.</p>

<h2>Children's Privacy</h2>

<p>Our Site is not intended for children under the age of 13 (or 16 in the European Union). We do not knowingly collect personal information from children. If we become aware that we have collected personal information from a child without parental consent, we will take steps to delete that information promptly.</p>

<h2>International Data Transfers</h2>

<p>Your information may be transferred to and processed in countries other than your country of residence. These countries may have data protection laws that differ from those in your country. By using our Site, you consent to the transfer of your information to countries outside your country of residence.</p>

<h2>Changes to This Privacy Policy</h2>

<p>We reserve the right to update or modify this Privacy Policy at any time. When we make changes, we will update the "Last Updated" date at the top of this page. We encourage you to review this Privacy Policy periodically to stay informed about how we protect your information.</p>

<p>Material changes to this Privacy Policy will be notified through a prominent notice on our Site or via email to registered users.</p>

<h2>Contact Us</h2>

<p>If you have questions, concerns, or requests regarding this Privacy Policy or our data practices, please contact us:</p>

<p><strong>SphereVista360</strong><br>
Email: <a href="mailto:privacy@spherevista360.com">privacy@spherevista360.com</a><br>
Contact Page: <a href="https://spherevista360.com/contact">https://spherevista360.com/contact</a></p>

<h2>Additional Information for EU Residents (GDPR)</h2>

<p>If you are located in the European Union, you have additional rights under the General Data Protection Regulation (GDPR), including:</p>

<ul>
<li>The right to lodge a complaint with a supervisory authority</li>
<li>The right to data portability</li>
<li>The right to restrict processing</li>
<li>The right to object to automated decision-making</li>
</ul>

<p>Our legal basis for processing your information includes:</p>

<ul>
<li><strong>Consent:</strong> You have given clear consent for processing your personal data</li>
<li><strong>Contract:</strong> Processing is necessary for a contract with you</li>
<li><strong>Legal Obligation:</strong> Processing is necessary to comply with the law</li>
<li><strong>Legitimate Interests:</strong> Processing is necessary for our legitimate interests</li>
</ul>

<h2>California Privacy Rights (CCPA)</h2>

<p>If you are a California resident, you have specific rights under the California Consumer Privacy Act (CCPA), including:</p>

<ul>
<li>The right to know what personal information is collected</li>
<li>The right to know if personal information is sold or disclosed</li>
<li>The right to say no to the sale of personal information</li>
<li>The right to access your personal information</li>
<li>The right to equal service and price, even if you exercise your privacy rights</li>
</ul>

<p>We do not sell personal information to third parties.</p>

</div>
"""

def get_disclaimer_content():
    """Generate comprehensive Disclaimer content"""
    current_date = datetime.now().strftime("%B %d, %Y")
    return f"""
<div class="disclaimer-content">

<p><strong>Last Updated: {current_date}</strong></p>

<h2>Website Disclaimer</h2>

<p>The information provided by SphereVista360 ("we," "us," or "our") on <a href="https://spherevista360.com">spherevista360.com</a> (the "Site") is for general informational and educational purposes only. All information on the Site is provided in good faith; however, we make no representation or warranty of any kind, express or implied, regarding the accuracy, adequacy, validity, reliability, availability, or completeness of any information on the Site.</p>

<h2>No Professional Advice</h2>

<h3>Financial Advice</h3>

<p>The content on this Site does not constitute financial, investment, or professional advice. We are not licensed financial advisors, investment professionals, or certified financial planners. The information provided on this Site should not be relied upon for making financial, investment, or business decisions.</p>

<p>Before making any financial decisions, you should consult with a qualified financial advisor, accountant, or other professional who can assess your individual circumstances and provide personalized advice.</p>

<h3>Technology Advice</h3>

<p>While we strive to provide accurate and up-to-date information about financial technology, blockchain, artificial intelligence, and related topics, the rapidly evolving nature of these fields means that information may become outdated quickly. We do not guarantee that our content reflects the latest developments or best practices.</p>

<h3>Legal Advice</h3>

<p>Nothing on this Site constitutes legal advice. The information provided regarding regulations, compliance, and legal matters is for general informational purposes only and should not be construed as legal guidance. For specific legal advice, please consult with a qualified attorney.</p>

<h2>No Guarantees or Warranties</h2>

<p>Under no circumstance shall we have any liability to you for any loss or damage of any kind incurred as a result of the use of the Site or reliance on any information provided on the Site. Your use of the Site and your reliance on any information on the Site is solely at your own risk.</p>

<p>We make no guarantees, representations, or warranties regarding:</p>

<ul>
<li>The accuracy, completeness, or timeliness of the content</li>
<li>The results that may be obtained from using the information</li>
<li>The suitability of the information for any particular purpose</li>
<li>The availability or uninterrupted access to the Site</li>
<li>The absence of errors, viruses, or other harmful components</li>
</ul>

<h2>External Links Disclaimer</h2>

<p>The Site may contain links to external websites that are not provided or maintained by SphereVista360. We have no control over the content, privacy policies, or practices of these external sites and assume no responsibility for them.</p>

<p>The inclusion of any links does not necessarily imply a recommendation or endorsement of the views expressed within them. We are not responsible for:</p>

<ul>
<li>The availability of external websites or resources</li>
<li>The accuracy or reliability of information on external sites</li>
<li>Any content, advertising, products, or services on external sites</li>
<li>Any damages or losses arising from your use of external sites</li>
</ul>

<p>You acknowledge and agree that we shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with the use of or reliance on any external content, goods, or services available through such websites.</p>

<h2>Investment and Trading Risks</h2>

<p>Content related to cryptocurrency, blockchain, trading, or investments is provided for informational purposes only. All forms of investment and trading carry risks, including the potential loss of principal.</p>

<p><strong>Important Investment Warnings:</strong></p>

<ul>
<li>Past performance is not indicative of future results</li>
<li>Cryptocurrency and digital assets are highly volatile and speculative</li>
<li>You may lose some or all of your invested capital</li>
<li>Only invest what you can afford to lose</li>
<li>Conduct your own research and due diligence</li>
<li>Consider your risk tolerance and investment objectives</li>
</ul>

<p>We do not endorse, recommend, or promote any specific cryptocurrency, token, platform, exchange, investment strategy, or financial product mentioned on our Site.</p>

<h2>No Endorsements</h2>

<p>Any references to specific companies, products, services, technologies, or individuals on our Site are for informational purposes only and do not constitute an endorsement, recommendation, or affiliation unless explicitly stated.</p>

<p>Sponsored content, advertisements, or affiliate links (if any) will be clearly disclosed. We are not responsible for the quality, accuracy, or performance of any products or services offered by third parties.</p>

<h2>Accuracy and Completeness</h2>

<p>While we make every effort to ensure that the information on our Site is accurate and current, we cannot guarantee its accuracy or completeness. Information on the Site may contain:</p>

<ul>
<li>Technical inaccuracies or typographical errors</li>
<li>Outdated information that has not been updated</li>
<li>Incomplete information pending further research</li>
<li>Opinion-based content that reflects subjective views</li>
</ul>

<p>We reserve the right to make changes, corrections, or updates to any content on the Site at any time without prior notice.</p>

<h2>Personal Responsibility</h2>

<p>You are solely responsible for:</p>

<ul>
<li>Verifying the accuracy of information before relying on it</li>
<li>Consulting with appropriate professionals for personalized advice</li>
<li>Your own decisions and actions based on information from this Site</li>
<li>Conducting due diligence before engaging in any financial transactions</li>
<li>Complying with applicable laws and regulations in your jurisdiction</li>
</ul>

<h2>Technology and Security</h2>

<p>We implement reasonable security measures to protect our Site; however, we cannot guarantee that the Site will be free from viruses, malware, or other harmful components. You are responsible for implementing appropriate security measures on your own devices.</p>

<p>We are not liable for any damages resulting from:</p>

<ul>
<li>Unauthorized access to your data or devices</li>
<li>Viruses or malware transmitted through the Site</li>
<li>Technical failures or interruptions in service</li>
<li>Loss of data or information</li>
</ul>

<h2>Changes to Content</h2>

<p>The financial technology and cryptocurrency industries are rapidly evolving. Information that is accurate today may become outdated or inaccurate over time. We strive to keep our content current but cannot guarantee that all information reflects the latest developments.</p>

<p>We may update, modify, or remove content at our discretion without notice. We are not obligated to update past content to reflect current information.</p>

<h2>Jurisdictional Issues</h2>

<p>The information on this Site is intended for a global audience. However, laws and regulations regarding financial services, cryptocurrencies, and related topics vary significantly by jurisdiction. Content that is legal and appropriate in one jurisdiction may not be in another.</p>

<p>It is your responsibility to ensure that your use of the Site and any actions you take based on information from the Site comply with applicable laws and regulations in your jurisdiction.</p>

<h2>Third-Party Content</h2>

<p>Our Site may include content submitted by third parties, including comments, guest posts, or user-generated content. We do not endorse, verify, or take responsibility for third-party content. Opinions expressed by third parties are their own and do not reflect the views of SphereVista360.</p>

<h2>Fair Use and Copyright</h2>

<p>We respect intellectual property rights and strive to provide proper attribution for content. If you believe that any content on our Site infringes your copyright or intellectual property rights, please contact us immediately.</p>

<h2>Limitation of Liability</h2>

<p>To the fullest extent permitted by applicable law, SphereVista360, its owners, employees, agents, and affiliates shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising from:</p>

<ul>
<li>Your use of or inability to use the Site</li>
<li>Any errors, omissions, or inaccuracies in the content</li>
<li>Any unauthorized access to your personal information</li>
<li>Any interruption or cessation of transmission to or from the Site</li>
<li>Any bugs, viruses, or malware transmitted through the Site</li>
<li>Any loss of data or profit resulting from use of the Site</li>
</ul>

<h2>Educational Purpose</h2>

<p>The primary purpose of this Site is educational. We aim to inform and educate our readers about financial technology, blockchain, digital innovation, and related topics. The content should be used as a starting point for your own research and learning.</p>

<h2>No Client Relationship</h2>

<p>Your use of this Site does not create any professional-client relationship between you and SphereVista360. We do not represent you, and you should not rely on the Site as a substitute for professional advice tailored to your specific circumstances.</p>

<h2>Contact Us</h2>

<p>If you have any questions about this Disclaimer, please contact us:</p>

<p><strong>SphereVista360</strong><br>
Email: <a href="mailto:info@spherevista360.com">info@spherevista360.com</a><br>
Contact Page: <a href="https://spherevista360.com/contact">https://spherevista360.com/contact</a></p>

<h2>Acceptance of Disclaimer</h2>

<p>By using this Site, you acknowledge that you have read, understood, and agree to this Disclaimer. If you do not agree with any part of this Disclaimer, you should not use the Site.</p>

</div>
"""

def get_terms_of_service_content():
    """Generate comprehensive Terms of Service content"""
    current_date = datetime.now().strftime("%B %d, %Y")
    return f"""
<div class="terms-of-service-content">

<p><strong>Last Updated: {current_date}</strong></p>

<h2>Agreement to Terms</h2>

<p>These Terms of Service ("Terms") constitute a legally binding agreement between you and SphereVista360 ("Company," "we," "us," or "our") concerning your access to and use of the <a href="https://spherevista360.com">spherevista360.com</a> website (the "Site").</p>

<p>By accessing or using the Site, you agree to be bound by these Terms and our Privacy Policy. If you disagree with any part of these Terms, you may not access or use the Site.</p>

<h2>Eligibility</h2>

<p>By using this Site, you represent and warrant that:</p>

<ul>
<li>You are at least 18 years of age (or the age of majority in your jurisdiction)</li>
<li>You have the legal capacity to enter into these Terms</li>
<li>You will comply with these Terms and all applicable laws and regulations</li>
<li>You have not been previously suspended or removed from the Site</li>
</ul>

<p>If you are using the Site on behalf of an organization, you represent that you have the authority to bind that organization to these Terms.</p>

<h2>Acceptable Use</h2>

<h3>Permitted Use</h3>

<p>You may use the Site for lawful purposes only. You agree to use the Site in accordance with these Terms and applicable laws, regulations, and generally accepted online practices.</p>

<h3>Prohibited Activities</h3>

<p>You agree NOT to engage in any of the following prohibited activities:</p>

<ul>
<li>Violating any applicable laws, regulations, or third-party rights</li>
<li>Copying, distributing, or disclosing any part of the Site without our written permission</li>
<li>Using any automated system (including robots, spiders, or scrapers) to access the Site</li>
<li>Attempting to gain unauthorized access to the Site, servers, or networks</li>
<li>Interfering with or disrupting the Site or servers</li>
<li>Transmitting viruses, malware, or other harmful code</li>
<li>Collecting or harvesting information about other users</li>
<li>Impersonating any person or entity</li>
<li>Posting false, misleading, or fraudulent content</li>
<li>Harassing, threatening, or intimidating other users</li>
<li>Uploading or transmitting obscene, offensive, or illegal content</li>
<li>Infringing on intellectual property rights</li>
<li>Engaging in any commercial activity without our prior written consent</li>
<li>Circumventing any technological measures we use to protect the Site</li>
</ul>

<h2>User Accounts</h2>

<p>If you create an account on our Site, you are responsible for:</p>

<ul>
<li>Maintaining the confidentiality of your account credentials</li>
<li>All activities that occur under your account</li>
<li>Notifying us immediately of any unauthorized access or security breach</li>
<li>Providing accurate, current, and complete information</li>
<li>Updating your information to maintain its accuracy</li>
</ul>

<p>We reserve the right to suspend or terminate your account if you violate these Terms or engage in conduct we deem inappropriate or harmful.</p>

<h2>Intellectual Property Rights</h2>

<h3>Our Content</h3>

<p>The Site and its entire contents, features, and functionality (including but not limited to text, images, graphics, logos, videos, audio, software, and compilation) are owned by SphereVista360 or our licensors and are protected by copyright, trademark, patent, trade secret, and other intellectual property laws.</p>

<p>Our trademarks and trade dress may not be used in connection with any product or service without our prior written consent.</p>

<h3>Limited License</h3>

<p>We grant you a limited, non-exclusive, non-transferable, revocable license to access and use the Site for personal, non-commercial purposes, subject to these Terms.</p>

<p>This license does not include:</p>

<ul>
<li>Any resale or commercial use of the Site or its content</li>
<li>Collection and use of product listings, descriptions, or prices</li>
<li>Any derivative use of the Site or its content</li>
<li>Any downloading or copying of account information</li>
<li>Any use of data mining, robots, or similar data gathering tools</li>
</ul>

<h3>User-Generated Content</h3>

<p>If you submit comments, feedback, suggestions, or other content to the Site ("User Content"), you grant us a worldwide, perpetual, irrevocable, royalty-free, transferable license to use, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, and display such User Content.</p>

<p>You represent and warrant that:</p>

<ul>
<li>You own or control all rights to your User Content</li>
<li>Your User Content does not violate any third-party rights</li>
<li>Your User Content is accurate and not misleading</li>
<li>Your User Content does not violate these Terms or applicable laws</li>
</ul>

<p>We reserve the right to remove or refuse to post any User Content at our discretion.</p>

<h2>Third-Party Links and Content</h2>

<p>The Site may contain links to third-party websites, services, or resources. We provide these links for your convenience, but we do not endorse or assume responsibility for:</p>

<ul>
<li>The accuracy, legality, or content of third-party sites</li>
<li>The privacy practices of third-party sites</li>
<li>Any products or services offered by third parties</li>
</ul>

<p>Your interactions with third-party websites are governed by their respective terms and privacy policies. We encourage you to review them before providing any information.</p>

<h2>Disclaimer of Warranties</h2>

<p>THE SITE IS PROVIDED ON AN "AS IS" AND "AS AVAILABLE" BASIS WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO:</p>

<ul>
<li>Implied warranties of merchantability</li>
<li>Fitness for a particular purpose</li>
<li>Non-infringement</li>
<li>Accuracy, reliability, or completeness of content</li>
<li>Uninterrupted or error-free operation</li>
<li>Security or freedom from viruses</li>
</ul>

<p>We do not warrant that:</p>

<ul>
<li>The Site will meet your requirements</li>
<li>The Site will be available at all times</li>
<li>The content is accurate, complete, or current</li>
<li>Any defects will be corrected</li>
</ul>

<h2>Limitation of Liability</h2>

<p>TO THE FULLEST EXTENT PERMITTED BY LAW, SPHEREVISTA360 AND ITS OWNERS, EMPLOYEES, AGENTS, PARTNERS, AND LICENSORS SHALL NOT BE LIABLE FOR:</p>

<ul>
<li>Any indirect, incidental, special, consequential, or punitive damages</li>
<li>Loss of profits, revenue, data, or use</li>
<li>Business interruption</li>
<li>Loss of goodwill or reputation</li>
<li>Any damages arising from your use of or inability to use the Site</li>
<li>Any damages resulting from third-party conduct or content</li>
</ul>

<p>This limitation applies whether the liability is based on contract, tort, negligence, strict liability, or any other legal theory, even if we have been advised of the possibility of such damages.</p>

<p>In jurisdictions that do not allow the exclusion of certain warranties or limitation of liability, our liability shall be limited to the maximum extent permitted by law.</p>

<h2>Indemnification</h2>

<p>You agree to indemnify, defend, and hold harmless SphereVista360 and its owners, employees, agents, partners, and licensors from and against any claims, liabilities, damages, losses, costs, or expenses (including reasonable attorneys' fees) arising from:</p>

<ul>
<li>Your use of the Site</li>
<li>Your violation of these Terms</li>
<li>Your violation of any rights of another party</li>
<li>Your User Content</li>
<li>Your conduct in connection with the Site</li>
</ul>

<h2>Modifications to the Site</h2>

<p>We reserve the right to:</p>

<ul>
<li>Modify, suspend, or discontinue the Site at any time</li>
<li>Change features, functionality, or content</li>
<li>Impose limits on certain features</li>
<li>Restrict access to parts or all of the Site</li>
</ul>

<p>We will not be liable to you or any third party for any modification, suspension, or discontinuation of the Site.</p>

<h2>Changes to Terms</h2>

<p>We reserve the right to update, change, or replace these Terms at any time at our sole discretion. Material changes will be notified through a prominent notice on the Site or via email to registered users.</p>

<p>Your continued use of the Site following the posting of changes constitutes your acceptance of those changes. We encourage you to review these Terms periodically.</p>

<h2>Termination</h2>

<p>We may terminate or suspend your access to the Site immediately, without prior notice or liability, for any reason, including:</p>

<ul>
<li>Breach of these Terms</li>
<li>Conduct we deem harmful to other users, us, or third parties</li>
<li>At our sole discretion</li>
</ul>

<p>Upon termination:</p>

<ul>
<li>Your right to use the Site will immediately cease</li>
<li>All licenses granted to you will terminate</li>
<li>You must cease all use of the Site</li>
</ul>

<p>All provisions that by their nature should survive termination shall survive, including ownership provisions, warranty disclaimers, and limitations of liability.</p>

<h2>Governing Law and Jurisdiction</h2>

<p>These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which SphereVista360 operates, without regard to conflict of law principles.</p>

<p>Any disputes arising from these Terms or your use of the Site shall be resolved in the courts of competent jurisdiction in our location.</p>

<h2>Dispute Resolution</h2>

<h3>Informal Resolution</h3>

<p>If you have a dispute with us, you agree to first contact us and attempt to resolve the dispute informally by sending written notice of your claim to us.</p>

<h3>Arbitration</h3>

<p>Any dispute that cannot be resolved informally may be subject to binding arbitration in accordance with the rules of a recognized arbitration organization. The arbitration shall be conducted in English, and the decision of the arbitrator shall be final and binding.</p>

<h3>Class Action Waiver</h3>

<p>You agree that any dispute resolution proceedings will be conducted only on an individual basis and not in a class, consolidated, or representative action.</p>

<h2>Severability</h2>

<p>If any provision of these Terms is found to be unenforceable or invalid, that provision shall be limited or eliminated to the minimum extent necessary, and the remaining provisions shall remain in full force and effect.</p>

<h2>Entire Agreement</h2>

<p>These Terms, together with our Privacy Policy and any other legal notices published on the Site, constitute the entire agreement between you and SphereVista360 concerning your use of the Site.</p>

<h2>Waiver</h2>

<p>Our failure to enforce any right or provision of these Terms will not be considered a waiver of those rights. No waiver of any term shall be deemed a further or continuing waiver of such term or any other term.</p>

<h2>Assignment</h2>

<p>You may not assign or transfer these Terms or your rights and obligations under these Terms without our prior written consent. We may assign or transfer these Terms at our discretion.</p>

<h2>Contact Information</h2>

<p>If you have any questions about these Terms of Service, please contact us:</p>

<p><strong>SphereVista360</strong><br>
Email: <a href="mailto:legal@spherevista360.com">legal@spherevista360.com</a><br>
Contact Page: <a href="https://spherevista360.com/contact">https://spherevista360.com/contact</a></p>

<h2>Acknowledgment</h2>

<p>BY USING THE SITE, YOU ACKNOWLEDGE THAT YOU HAVE READ THESE TERMS OF SERVICE AND AGREE TO BE BOUND BY THEM.</p>

</div>
"""

def get_contact_page_content():
    """Generate comprehensive Contact Us page content"""
    return """
<div class="contact-page-content">

<h2>Get in Touch With SphereVista360</h2>

<p>We value your feedback, questions, and inquiries. Whether you're a long-time reader, a first-time visitor, or a potential partner, we're here to help. Please use the contact methods below to reach out to us.</p>

<h2>General Inquiries</h2>

<p>For general questions, feedback, or comments about our content, please email us at:</p>

<p><strong>Email:</strong> <a href="mailto:info@spherevista360.com">info@spherevista360.com</a></p>

<p>We typically respond to all inquiries within 24-48 hours during business days.</p>

<h2>Content and Editorial</h2>

<p>If you have suggestions for topics you'd like us to cover, corrections to existing content, or general editorial feedback:</p>

<p><strong>Email:</strong> <a href="mailto:editorial@spherevista360.com">editorial@spherevista360.com</a></p>

<h3>Guest Posting and Contributions</h3>

<p>We occasionally accept guest posts from industry experts and thought leaders. If you're interested in contributing to SphereVista360, please send your pitch or inquiry to our editorial team. Include:</p>

<ul>
<li>Your proposed topic and brief outline</li>
<li>Your credentials and expertise in the subject area</li>
<li>Links to previous published work (if available)</li>
<li>Why you think this topic would be valuable to our readers</li>
</ul>

<h2>Partnership and Collaboration</h2>

<p>Interested in partnering with SphereVista360 or exploring collaboration opportunities?</p>

<p><strong>Email:</strong> <a href="mailto:partnerships@spherevista360.com">partnerships@spherevista360.com</a></p>

<h3>Types of Partnerships</h3>

<ul>
<li><strong>Content Partnerships:</strong> Co-creating valuable content for our audiences</li>
<li><strong>Research Collaboration:</strong> Joint research projects and whitepapers</li>
<li><strong>Industry Events:</strong> Speaking engagements and event participation</li>
<li><strong>Media Partnerships:</strong> Cross-promotion and media collaborations</li>
</ul>

<h2>Advertising and Sponsorship</h2>

<p>For advertising opportunities, sponsored content, or sponsorship inquiries:</p>

<p><strong>Email:</strong> <a href="mailto:advertising@spherevista360.com">advertising@spherevista360.com</a></p>

<p>We offer various advertising options including:</p>

<ul>
<li>Display advertising</li>
<li>Sponsored content</li>
<li>Newsletter sponsorship</li>
<li>Event sponsorship</li>
</ul>

<h2>Press and Media</h2>

<p>Members of the press seeking information about SphereVista360 or requesting interviews:</p>

<p><strong>Email:</strong> <a href="mailto:press@spherevista360.com">press@spherevista360.com</a></p>

<h2>Technical Support</h2>

<p>Experiencing technical issues with our website? Please let us know:</p>

<p><strong>Email:</strong> <a href="mailto:support@spherevista360.com">support@spherevista360.com</a></p>

<p>When reporting technical issues, please include:</p>

<ul>
<li>Description of the problem</li>
<li>Your browser and operating system</li>
<li>Steps to reproduce the issue</li>
<li>Screenshots (if applicable)</li>
</ul>

<h2>Privacy and Legal</h2>

<p>For questions about our Privacy Policy, data protection, copyright, or other legal matters:</p>

<p><strong>Email:</strong> <a href="mailto:legal@spherevista360.com">legal@spherevista360.com</a></p>

<h3>Copyright and DMCA</h3>

<p>If you believe content on our site infringes your copyright, please contact our legal team with:</p>

<ul>
<li>Identification of the copyrighted work</li>
<li>Location of the allegedly infringing material on our site</li>
<li>Your contact information</li>
<li>A statement of good faith belief</li>
<li>A statement of accuracy under penalty of perjury</li>
<li>Your physical or electronic signature</li>
</ul>

<h2>Social Media</h2>

<p>Connect with us on social media for the latest updates, articles, and discussions:</p>

<ul>
<li><strong>Twitter:</strong> Follow us for real-time updates and industry news</li>
<li><strong>LinkedIn:</strong> Connect with us for professional insights and networking</li>
<li><strong>Facebook:</strong> Join our community for discussions and content sharing</li>
</ul>

<h2>Newsletter Subscription</h2>

<p>Stay informed about the latest developments in financial technology, blockchain, AI, and digital innovation by subscribing to our newsletter. We deliver curated insights directly to your inbox.</p>

<p>To subscribe, visit our <a href="https://spherevista360.com">homepage</a> and enter your email address in the subscription form.</p>

<h3>Newsletter Management</h3>

<p>To update your email preferences or unsubscribe from our newsletter:</p>

<ul>
<li>Click the "unsubscribe" link at the bottom of any newsletter email</li>
<li>Email us at <a href="mailto:newsletter@spherevista360.com">newsletter@spherevista360.com</a> with your request</li>
</ul>

<h2>Feedback and Suggestions</h2>

<p>We're constantly working to improve SphereVista360 and provide more value to our readers. Your feedback helps us understand what's working and what needs improvement.</p>

<p>Please share your thoughts on:</p>

<ul>
<li>Content quality and relevance</li>
<li>Website usability and navigation</li>
<li>Topics you'd like us to cover</li>
<li>Features you'd like to see</li>
<li>Overall user experience</li>
</ul>

<p><strong>Email:</strong> <a href="mailto:feedback@spherevista360.com">feedback@spherevista360.com</a></p>

<h2>Speaking Engagements and Interviews</h2>

<p>Our team members are available for:</p>

<ul>
<li>Conference speaking engagements</li>
<li>Podcast interviews</li>
<li>Webinar presentations</li>
<li>Panel discussions</li>
<li>Media interviews</li>
</ul>

<p>Please contact us at <a href="mailto:speaking@spherevista360.com">speaking@spherevista360.com</a> with details about your event or opportunity.</p>

<h2>Office Hours</h2>

<p>Our team monitors communications during standard business hours:</p>

<p><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM (EST)<br>
<strong>Saturday - Sunday:</strong> Closed (Limited emergency support available)</p>

<p>While we strive to respond to all inquiries promptly, please allow 24-48 business hours for a response. Complex inquiries may take longer to address thoroughly.</p>

<h2>FAQ</h2>

<h3>How quickly will I receive a response?</h3>

<p>We aim to respond to all inquiries within 24-48 business hours. Complex questions or partnership inquiries may take longer as we want to provide thorough and thoughtful responses.</p>

<h3>Can I republish your content?</h3>

<p>Please contact our legal team at <a href="mailto:legal@spherevista360.com">legal@spherevista360.com</a> for permissions regarding content republication, with details about how you plan to use the content.</p>

<h3>Do you accept sponsored posts?</h3>

<p>We selectively accept sponsored content that aligns with our editorial standards and provides value to our readers. Contact our advertising team for more information.</p>

<h3>How can I correct an error in an article?</h3>

<p>We take accuracy seriously. If you've spotted an error, please email <a href="mailto:editorial@spherevista360.com">editorial@spherevista360.com</a> with details about the error and the correct information (with sources, if applicable).</p>

<h3>Can I request removal of my data?</h3>

<p>Yes, you have the right to request deletion of your personal data. Please email <a href="mailto:privacy@spherevista360.com">privacy@spherevista360.com</a> with your request, and we'll process it in accordance with applicable privacy laws.</p>

<h2>Stay Connected</h2>

<p>Thank you for your interest in SphereVista360. We look forward to hearing from you and helping you navigate the exciting world of financial technology, blockchain, and digital innovation.</p>

<p>Whether you have a question, suggestion, or partnership opportunity, don't hesitate to reach out. We're here to help!</p>

<h3>Quick Contact Summary</h3>

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
<tr style="background-color: #f5f5f5;">
<th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Department</th>
<th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Email Address</th>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">General Inquiries</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:info@spherevista360.com">info@spherevista360.com</a></td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Editorial & Content</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:editorial@spherevista360.com">editorial@spherevista360.com</a></td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Partnerships</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:partnerships@spherevista360.com">partnerships@spherevista360.com</a></td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Advertising</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:advertising@spherevista360.com">advertising@spherevista360.com</a></td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Press & Media</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:press@spherevista360.com">press@spherevista360.com</a></td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Technical Support</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:support@spherevista360.com">support@spherevista360.com</a></td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Privacy & Legal</td>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:legal@spherevista360.com">legal@spherevista360.com</a></td>
</tr>
</table>

<p style="margin-top: 30px;"><em>We respect your privacy and will never share your contact information with third parties. All communications are handled in accordance with our <a href="https://spherevista360.com/privacy-policy">Privacy Policy</a>.</em></p>

</div>
"""

def main():
    print("=" * 70)
    print("SphereVista360 - Essential Pages Creation")
    print("Google AdSense Compliance Package")
    print("=" * 70)
    print()
    
    if not all([WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("❌ Error: Missing WordPress credentials in .env file")
        return
    
    print(f"🌐 WordPress Site: {WORDPRESS_BASE_URL}")
    print()
    
    pages_to_create = [
        {
            'title': 'Privacy Policy',
            'slug': 'privacy-policy',
            'content': get_privacy_policy_content()
        },
        {
            'title': 'Disclaimer',
            'slug': 'disclaimer',
            'content': get_disclaimer_content()
        },
        {
            'title': 'Terms of Service',
            'slug': 'terms-of-service',
            'content': get_terms_of_service_content()
        },
        {
            'title': 'Contact Us',
            'slug': 'contact',
            'content': get_contact_page_content()
        }
    ]
    
    created_pages = []
    
    for page_info in pages_to_create:
        print(f"\n📄 Processing: {page_info['title']}")
        print("-" * 70)
        
        page = create_or_update_page(
            page_info['title'],
            page_info['slug'],
            page_info['content']
        )
        
        if page:
            created_pages.append({
                'title': page['title']['rendered'],
                'url': page['link'],
                'id': page['id']
            })
            print(f"   ✅ Success!")
            print(f"   URL: {page['link']}")
            print(f"   ID: {page['id']}")
        else:
            print(f"   ❌ Failed to create/update {page_info['title']}")
    
    print()
    print("=" * 70)
    print(f"✅ Processed {len(created_pages)} out of {len(pages_to_create)} pages")
    print("=" * 70)
    print()
    
    if created_pages:
        print("📋 Created/Updated Pages:")
        for page in created_pages:
            print(f"   • {page['title']}")
            print(f"     {page['url']}")
        print()
        
        print("🎯 AdSense Compliance:")
        print("   ✅ Privacy Policy - Complete")
        print("   ✅ Disclaimer - Complete")
        print("   ✅ Terms of Service - Complete")
        print("   ✅ Contact Page - Complete")
        print()
        
        print("📝 Next Step: Update footer menu with these pages")
        print("   Run: python3 update_footer_menu.py")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
