#!/usr/bin/env python3
"""
US Tax Calculator Suite Deployment Script
Creates WordPress pages for the US Tax Calculator Suite using WordPress REST API
"""

import os
import json
import requests
import base64
import getpass
from pathlib import Path

class WordPressDeployer:
    def __init__(self, site_url, username, password):
        self.site_url = site_url.rstrip('/')
        self.username = username
        self.password = password
        self.auth_header = self._get_auth_header()
        self.session = requests.Session()
        self.session.headers.update({'Authorization': self.auth_header})

    def _get_auth_header(self):
        """Get authentication header for WordPress API"""
        # Try JWT first
        jwt_url = f"{self.site_url}/wp-json/jwt-auth/v1/token"
        jwt_data = {
            "username": self.username,
            "password": self.password
        }

        try:
            response = requests.post(jwt_url, json=jwt_data, timeout=10)
            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    return f"Bearer {token}"
        except:
            pass

        # Fall back to basic auth
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return f"Basic {credentials}"

    def test_connection(self):
        """Test WordPress API connection"""
        url = f"{self.site_url}/wp-json/wp/v2/users/me"
        response = self.session.get(url)

        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Connected to WordPress as: {user_data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ API connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    def create_page(self, title, content, slug, status="publish"):
        """Create a WordPress page"""
        url = f"{self.site_url}/wp-json/wp/v2/pages"

        page_data = {
            "title": title,
            "content": content,
            "slug": slug,
            "status": status,
            "type": "page"
        }

        response = self.session.post(url, json=page_data)

        if response.status_code in [200, 201]:
            page_data = response.json()
            page_id = page_data.get('id')
            print(f"✅ Created page: {title} (ID: {page_id})")
            return page_id
        else:
            print(f"❌ Failed to create page: {title}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    def read_html_file(self, file_path):
        """Read and clean HTML file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the main HTML body content, avoiding body tags inside JavaScript
            lines = content.split('\n')
            body_start = -1
            body_end = -1
            in_script = False

            for i, line in enumerate(lines):
                # Track if we're inside a script tag
                if '<script' in line:
                    in_script = True
                if '</script>' in line:
                    in_script = False

                # Only look for body tags when not inside script
                if not in_script:
                    if '<body' in line or ('<body>' in line and body_start == -1):
                        if body_start == -1:
                            body_start = i
                    if '</body>' in line:
                        body_end = i

            if body_start != -1 and body_end != -1:
                # Extract content between body tags
                body_content = '\n'.join(lines[body_start+1:body_end])
                return body_content.strip()
            else:
                # If no body tags found, return the whole content but remove html structure
                return content.replace('<!DOCTYPE html>', '').replace('<html', '').replace('</html>', '').strip()

        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None

def main():
    print("🚀 US Tax Calculator Suite Deployment")
    print("=" * 50)

    # Configuration
    SITE_URL = "https://spherevista360.com"
    USERNAME = "JK"  # WordPress admin username

    # Get password securely
    PASSWORD = getpass.getpass("Enter WordPress password: ")

    # Initialize deployer
    deployer = WordPressDeployer(SITE_URL, USERNAME, PASSWORD)

    # Test connection
    if not deployer.test_connection():
        print("❌ Cannot proceed without API access")
        return

    # Calculator configurations
    calculators = [
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/index.html",
            "title": "US Tax & Investment Calculator Suite",
            "slug": "us-tax-calculator-suite",
            "description": "Complete suite of US tax and investment calculators for individuals and businesses"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/federal-income-tax.html",
            "title": "Federal Income Tax Calculator",
            "slug": "federal-income-tax-calculator",
            "description": "Calculate your federal income tax liability with accurate brackets and deductions"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/state-income-tax.html",
            "title": "State Income Tax Calculator",
            "slug": "state-income-tax-calculator",
            "description": "Calculate state income tax for all 50 states with current rates and rules"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/capital-gains-tax.html",
            "title": "Capital Gains Tax Calculator",
            "slug": "capital-gains-tax-calculator",
            "description": "Calculate capital gains tax on investments with short-term and long-term rates"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/self-employment-tax.html",
            "title": "Self Employment Tax Calculator",
            "slug": "self-employment-tax-calculator",
            "description": "Calculate self-employment tax for freelancers and business owners"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/retirement-tax.html",
            "title": "Retirement Tax Calculator",
            "slug": "retirement-tax-calculator",
            "description": "Calculate taxes on retirement income including 401(k), IRA, and Social Security"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/tax-withholding.html",
            "title": "Tax Withholding Calculator",
            "slug": "tax-withholding-calculator",
            "description": "Optimize your W-4 form and calculate proper tax withholding amounts"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/lump-sum-investment.html",
            "title": "Lump Sum Investment Calculator",
            "slug": "lump-sum-investment-calculator",
            "description": "Calculate returns on a one-time investment with compound interest over time"
        },
        {
            "file": "/home/kddevops/projects/spherevista360/tools/calculators/us_tax_calculator/retirement-planner-estimator.html",
            "title": "Retirement Planner and Estimator",
            "slug": "retirement-planner-estimator",
            "description": "Plan your retirement with comprehensive savings projections and income estimates"
        }
    ]

    created_pages = []

    for calc in calculators:
        print(f"\n📄 Processing: {calc['title']}")

        # Read HTML content
        html_content = deployer.read_html_file(calc['file'])
        if not html_content:
            continue

        # Wrap content for WordPress
        wordpress_content = f"""
<!-- wp:paragraph -->
<p><strong>{calc['description']}</strong></p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{html_content}
<!-- /wp:html -->

<!-- wp:paragraph -->
<p><em>Disclaimer: This calculator provides estimates based on current tax laws and rates. Tax laws can change, and this tool should not be considered as professional tax advice. Please consult with a qualified tax professional for your specific situation.</em></p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="/us-tax-calculator-suite/">← Back to Tax Calculator Suite</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->
"""

        # Create the page
        page_id = deployer.create_page(calc['title'], wordpress_content, calc['slug'])
        if page_id:
            created_pages.append({
                "title": calc['title'],
                "slug": calc['slug'],
                "id": page_id
            })

    # Summary
    print(f"\n🎉 Deployment completed!")
    print(f"Created {len(created_pages)} pages:")
    for page in created_pages:
        print(f"  ✅ {page['title']} → {SITE_URL}/{page['slug']}/")

    print("\n📋 Next steps:")
    print("1. Visit your site and test each calculator")
    print("2. Check that CSS and JavaScript are loading properly")
    print("3. Update navigation menus if needed")
    print("4. Clear any caching plugins")
    print("\n🔗 Direct links:")
    for page in created_pages:
        print(f"   {page['title']}: {SITE_URL}/{page['slug']}/")

if __name__ == "__main__":
    main()