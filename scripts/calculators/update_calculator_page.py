#!/usr/bin/env python3
import requests
import json
import getpass

# WordPress site details
WP_SITE_URL = "https://spherevista360.com"
WP_USERNAME = "jk"  # Default username

# Page ID for the EMI Calculator page
PAGE_ID = 3115

def update_page_content():
    """Update the EMI Calculator page with new content"""

    # Get password securely
    wp_password = getpass.getpass("WordPress application password: ").strip()

    if not wp_password:
        print("❌ Password is required")
        return False

    # Read the clean calculator HTML
    try:
        with open('/home/kddevops/projects/spherevista360/clean_calculator.html', 'r', encoding='utf-8') as f:
            calculator_html = f.read()
    except FileNotFoundError:
        print("Error: clean_calculator.html file not found")
        return False

    # Create new page content with proper wrapper
    new_content = f'''
<div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
<div style="text-align: center; margin-bottom: 30px;">
<h1>🏠 Loan EMI Calculator</h1>
<p style="font-size: 18px; color: #666;">Calculate your Equated Monthly Installment and loan repayment schedule</p>
</div>
<div id="loan-emi-calculator-container">
{calculator_html}
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

    # API endpoint
    api_url = f"{WP_SITE_URL}/wp-json/wp/v2/pages/{PAGE_ID}"

    try:
        print("🔄 Updating EMI Calculator page...")
        response = requests.post(api_url,
                                json={'content': new_content},
                                auth=(WP_USERNAME, wp_password),
                                headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print("✅ Page updated successfully!")
            print("🌐 Test the calculator at: https://spherevista360.com/loan-emi-calculator/")
            return True
        else:
            print(f"❌ Failed to update page. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error updating page: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting EMI Calculator page update...")
    success = update_page_content()
    if success:
        print("🎉 EMI Calculator page has been updated with the new professional design!")
    else:
        print("❌ Failed to update the page. Please check your credentials and try again.")