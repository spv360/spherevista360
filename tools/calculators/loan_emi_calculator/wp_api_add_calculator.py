#!/usr/bin/env python3
"""
Add Loan EMI Calculator to WordPress site
Creates the calculator page and updates the tools listing
"""

import sys
import os

# Add the project root to Python path to import master_toolkit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def create_loan_emi_calculator_page():
    """Create the Loan EMI Calculator page"""

    # Initialize WordPress client
    wp = WordPressClient()

    # Check if page already exists
    try:
        existing_pages = wp.get_pages(slug='loan-emi-calculator')
        if existing_pages:
            print_info(f"Page 'loan-emi-calculator' already exists (ID: {existing_pages[0]['id']})")
            return existing_pages[0]
    except Exception as e:
        print_error(f"Failed to check existing pages: {e}")
        return None

    # Create the page content
    content = """
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

<script>
// Add any additional JavaScript if needed
console.log('Loan EMI Calculator page loaded');
</script>
"""

    try:
        page = wp.create_post(
            title="Loan EMI Calculator",
            content=content,
            status="publish",
            post_type="page",
            slug="loan-emi-calculator"
        )

        if page:
            print_success(f"✅ Created Loan EMI Calculator page: {page['link']}")
            return page
        else:
            print_error("❌ Failed to create page")
            return None
    except Exception as e:
        print_error(f"❌ Failed to create page: {e}")
        return None


def update_tools_page():
    """Update the tools page to include Loan EMI Calculator"""

    # You'll need to set these credentials
    WP_SITE_URL = "https://spherevista360.com"
    WP_USERNAME = "wp_api_user"  # Replace with actual username
    WP_PASSWORD = "your_password_here"  # Replace with actual password

    wp = WordPressAPI(WP_SITE_URL, WP_USERNAME, WP_PASSWORD)

    # Get the tools page
def update_tools_page():
    """Update the tools page to include Loan EMI Calculator"""

    # Initialize WordPress client
    wp = WordPressClient()

    # Get the tools page
    try:
        tools_pages = wp.get_pages(slug='tools')
        if not tools_pages:
            print_error("❌ Tools page not found")
            return False

        tools_page = tools_pages[0]
    except Exception as e:
        print_error(f"❌ Failed to get tools page: {e}")
        return False

    # Check if Loan EMI Calculator is already listed
    content = tools_page['content']['rendered']
    if 'loan-emi-calculator' in content.lower():
        print_info("✅ Loan EMI Calculator already listed in tools page")
        return True

    # Add Loan EMI Calculator to the tools list
    loan_emi_tool_html = """
    <div class="tool-card">
        <div class="tool-icon">🏠</div>
        <h3>Loan EMI Calculator</h3>
        <p>Calculate loan EMIs, view amortization schedules, and check loan eligibility based on your income.</p>
        <a href="/loan-emi-calculator/" class="tool-link">Use Calculator</a>
    </div>
    """

    # Find where to insert the new tool (before the closing div or after existing tools)
    if '<div class="tool-card">' in content:
        # Insert before the last tool card or at the end
        insert_position = content.rfind('<div class="tool-card">')
        if insert_position != -1:
            before = content[:insert_position]
            after = content[insert_position:]
            new_content = before + loan_emi_tool_html + after
        else:
            new_content = content + loan_emi_tool_html
    else:
        new_content = content + loan_emi_tool_html

    # Update the page
    try:
        update_data = {
            'content': new_content
        }

        updated_page = wp.update_post(tools_page['id'], update_data)

        if updated_page:
            print_success("✅ Updated tools page with Loan EMI Calculator")
            return True
        else:
            print_error("❌ Failed to update tools page")
            return False
    except Exception as e:
        print_error(f"❌ Failed to update tools page: {e}")
        return False


def main():
    """Main function"""
    print("🏠 Adding Loan EMI Calculator to WordPress")
    print("=" * 50)

    try:
        # Create the calculator page
        page = create_loan_emi_calculator_page()
        if not page:
            print("❌ Failed to create calculator page")
            return 1

        # Update the tools page
        if not update_tools_page():
            print("⚠️  Calculator page created but failed to update tools listing")

        print("\n✅ Loan EMI Calculator setup complete!")
        print(f"📱 Calculator URL: {page['link']}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    # The script uses the existing WordPressClient authentication
    # Make sure you're authenticated with the WordPress site
    sys.exit(main())