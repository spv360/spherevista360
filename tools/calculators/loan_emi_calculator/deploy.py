#!/usr/bin/env python3
"""
Simple deployment script for Loan EMI Calculator
Run this script with your WordPress credentials to deploy the calculator.
"""

import requests
import json
import getpass
import sys


def deploy_loan_emi_calculator():
    """Deploy the Loan EMI Calculator to WordPress"""

    print("🏠 Loan EMI Calculator Deployment")
    print("=" * 40)

    # Get credentials
    username = input("WordPress username: ").strip()
    password = getpass.getpass("WordPress application password: ").strip()

    if not username or not password:
        print("❌ Username and password are required")
        return False

    site_url = "https://spherevista360.com"
    api_url = f"{site_url}/wp-json/wp/v2"

    # Create session with authentication
    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({
        'User-Agent': 'Loan-EMI-Calculator-Deploy/1.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

    print("🔐 Authenticating...")

    # Test authentication
    try:
        response = session.get(f"{api_url}/users/me")
        if response.status_code != 200:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.text)
            return False
        print("✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

    # Step 1: Create the calculator page
    print("\n📄 Creating calculator page...")

    page_content = """
<div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>🏠 Loan EMI Calculator</h1>
        <p style="font-size: 18px; color: #666;">Calculate your Equated Monthly Installment and loan repayment schedule</p>
    </div>

    <div id="loan-emi-calculator-container">
        <iframe src="/tools/calculators/loan_emi_calculator/loan_emi_calculator.html"
                width="100%"
                height="800"
                frameborder="0"
                style="border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        </iframe>
    </div>

    <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
        <h3>About This Calculator</h3>
        <p>This comprehensive loan EMI calculator helps you:</p>
        <ul>
            <li>Calculate exact monthly EMI payments</li>
            <li>View detailed amortization schedule</li>
            <li>Understand interest vs principal breakdown</li>
            <li>Assess loan affordability based on income</li>
            <li>Export results for record keeping</li>
        </ul>
    </div>
</div>
"""

    page_data = {
        'title': 'Loan EMI Calculator',
        'content': page_content,
        'slug': 'loan-emi-calculator',
        'status': 'publish',
        'type': 'page'
    }

    try:
        response = session.post(f"{api_url}/pages", json=page_data)
        if response.status_code == 201:
            page = response.json()
            print(f"✅ Calculator page created: {page['link']}")
            page_id = page['id']
        elif response.status_code == 400 and 'slug' in response.text:
            # Page might already exist, try to find it
            print("⚠️  Page might already exist, checking...")
            response = session.get(f"{api_url}/pages", params={'slug': 'loan-emi-calculator'})
            if response.status_code == 200:
                pages = response.json()
                if pages:
                    page = pages[0]
                    print(f"✅ Calculator page already exists: {page['link']}")
                    page_id = page['id']
                else:
                    print("❌ Could not find existing page")
                    return False
            else:
                print(f"❌ Failed to check existing pages: {response.status_code}")
                return False
        else:
            print(f"❌ Failed to create page: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error creating page: {e}")
        return False

    # Step 2: Update the tools page
    print("\n🔧 Updating tools page...")

    try:
        # Get the tools page
        response = session.get(f"{api_url}/pages", params={'slug': 'tools'})
        if response.status_code != 200:
            print(f"❌ Failed to get tools page: {response.status_code}")
            return False

        pages = response.json()
        if not pages:
            print("❌ Tools page not found")
            return False

        tools_page = pages[0]
        content = tools_page['content']['rendered']

        # Check if already listed
        if 'loan-emi-calculator' in content.lower():
            print("✅ Loan EMI Calculator already listed in tools page")
        else:
            # Add the calculator to tools
            loan_emi_tool = """
    <div class="tool-card">
        <div class="tool-icon">🏠</div>
        <h3>Loan EMI Calculator</h3>
        <p>Calculate loan EMIs, view amortization schedules, and check loan eligibility based on your income.</p>
        <a href="/loan-emi-calculator/" class="tool-link">Use Calculator</a>
    </div>
"""

            # Insert before the last tool card
            insert_pos = content.rfind('<div class="tool-card">')
            if insert_pos != -1:
                before = content[:insert_pos]
                after = content[insert_pos:]
                new_content = before + loan_emi_tool + after
            else:
                new_content = content + loan_emi_tool

            # Update the page
            update_data = {'content': new_content}
            response = session.post(f"{api_url}/pages/{tools_page['id']}", json=update_data)
            if response.status_code == 200:
                print("✅ Tools page updated with Loan EMI Calculator")
            else:
                print(f"⚠️  Failed to update tools page: {response.status_code}")
                print("Calculator page created but not added to tools listing")

    except Exception as e:
        print(f"⚠️  Error updating tools page: {e}")
        print("Calculator page created but tools page not updated")

    # Step 3: Add to homepage (optional)
    print("\n🏠 Adding to homepage...")

    try:
        # Get homepage
        response = session.get(f"{api_url}/pages", params={'slug': 'home'})
        if response.status_code != 200:
            # Try to get the first page
            response = session.get(f"{api_url}/pages", params={'per_page': 1})

        if response.status_code == 200:
            pages = response.json()
            if pages:
                homepage = pages[0]
                content = homepage['content']['rendered']

                if 'loan-emi-calculator' in content.lower():
                    print("✅ Loan EMI Calculator button already on homepage")
                else:
                    # Add button to homepage
                    loan_emi_button = '''
<div style="text-align: center; margin: 20px 0;">
    <a href="/loan-emi-calculator/" class="calculator-button" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        🏠 Loan EMI Calculator
    </a>
</div>
'''
                    new_content = content + loan_emi_button

                    update_data = {'content': new_content}
                    response = session.post(f"{api_url}/pages/{homepage['id']}", json=update_data)
                    if response.status_code == 200:
                        print("✅ Homepage updated with Loan EMI Calculator button")
                    else:
                        print(f"⚠️  Failed to update homepage: {response.status_code}")
            else:
                print("⚠️  Homepage not found")
        else:
            print("⚠️  Could not access homepage")

    except Exception as e:
        print(f"⚠️  Error updating homepage: {e}")

    print("\n🎉 Deployment completed!")
    print(f"📱 Calculator URL: https://spherevista360.com/loan-emi-calculator/")
    print("📁 Files are accessible at: https://spherevista360.com/tools/calculators/loan_emi_calculator/")

    return True


if __name__ == "__main__":
    try:
        success = deploy_loan_emi_calculator()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Deployment cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)