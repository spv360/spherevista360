#!/usr/bin/env python3
"""
Script to embed the Loan EMI Calculator directly into the WordPress page
This replaces the iframe approach with direct HTML embedding
"""

import requests
import json
import re
import getpass

def main():
    # WordPress API details
    wp_site = 'https://spherevista360.com'
    wp_user = input("WordPress username: ").strip() or 'jk'

    # Get password securely
    wp_password = getpass.getpass("WordPress application password: ").strip()

    if not wp_password:
        print("❌ Password is required")
        return

    print("📖 Reading calculator HTML content...")

    # Get the calculator HTML content
    try:
        with open('upload_package/loan_emi_calculator.html', 'r') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ Calculator HTML file not found. Please run this script from the project root.")
        return

    # Extract the body content
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    if not body_match:
        print("❌ Could not extract body content from HTML")
        return

    calculator_body = body_match.group(1)
    print(f"✅ Extracted calculator content ({len(calculator_body)} characters)")

    # Create new page content
    new_content = f'''
<div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
<div style="text-align: center; margin-bottom: 30px;">
<h1>🏠 Loan EMI Calculator</h1>
<p style="font-size: 18px; color: #666;">Calculate your Equated Monthly Installment and loan repayment schedule</p>
</div>
<div id="loan-emi-calculator-container">
{calculator_body}
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
'''

    print("🔄 Updating WordPress page...")

    # Update the WordPress page
    url = f'{wp_site}/wp-json/wp/v2/pages/3115'
    auth = (wp_user, wp_password)

    try:
        response = requests.post(url,
                                json={'content': new_content},
                                auth=auth,
                                headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print("✅ Successfully updated WordPress page with embedded calculator!")
            print("🌐 Test the calculator at: https://spherevista360.com/loan-emi-calculator/")
        else:
            print(f"❌ Failed to update page: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error updating page: {e}")

if __name__ == "__main__":
    main()