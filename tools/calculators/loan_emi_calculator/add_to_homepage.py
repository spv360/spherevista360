#!/usr/bin/env python3
"""
Add Loan EMI Calculator button to homepage CTA section
"""

import sys
import os

# Add the project root to Python path to import master_toolkit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info
import re


def add_loan_emi_to_homepage():
    """Add Loan EMI Calculator button to homepage"""

    # Initialize WordPress client
    wp = WordPressClient()

    # Get the homepage
    try:
        # Try to get the front page
        homepage_pages = wp.get_pages(slug='home')
        if not homepage_pages:
            # Try 'front-page' or just get the first page
            all_pages = wp.get_pages(per_page=1)
            homepage = all_pages[0] if all_pages else None
        else:
            homepage = homepage_pages[0]

        if not homepage:
            print_error("❌ Homepage not found")
            return False
    except Exception as e:
        print_error(f"❌ Failed to get homepage: {e}")
        return False

    content = homepage['content']['rendered']

    # Check if Loan EMI Calculator button already exists
    if 'loan-emi-calculator' in content.lower():
        print("✅ Loan EMI Calculator button already exists on homepage")
        return True

    # Look for the calculator buttons section
    # This assumes there's a section with calculator buttons
    button_pattern = r'<a[^>]*href="[^"]*calculator[^"]*"[^>]*>.*?</a>'
    buttons_match = re.findall(button_pattern, content, re.IGNORECASE | re.DOTALL)

    if not buttons_match:
        print("⚠️  No calculator buttons found on homepage - adding to end of content")
        # Add at the end of content
        loan_emi_button = '''
<div style="text-align: center; margin: 20px 0;">
    <a href="/loan-emi-calculator/" class="calculator-button" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        🏠 Loan EMI Calculator
    </a>
</div>
'''
        new_content = content + loan_emi_button
    else:
        # Insert after the last calculator button
        last_button_end = content.rfind('</a>', content.find(buttons_match[-1]))
        if last_button_end != -1:
            before = content[:last_button_end + 4]  # +4 for </a>
            after = content[last_button_end + 4:]

            loan_emi_button = '''
    <a href="/loan-emi-calculator/" class="calculator-button" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        🏠 Loan EMI Calculator
    </a>'''

            new_content = before + loan_emi_button + after
        else:
            # Fallback: add at end
            loan_emi_button = '''
<div style="text-align: center; margin: 20px 0;">
    <a href="/loan-emi-calculator/" class="calculator-button" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        🏠 Loan EMI Calculator
    </a>
</div>
'''
            new_content = content + loan_emi_button

    # Update the homepage
    try:
        update_data = {
            'content': new_content
        }

        updated_page = wp.update_post(homepage['id'], update_data)

        if updated_page:
            print_success("✅ Added Loan EMI Calculator button to homepage")
            return True
        else:
            print_error("❌ Failed to update homepage")
            return False
    except Exception as e:
        print_error(f"❌ Failed to update homepage: {e}")
        return False


def main():
    """Main function"""
    print("🏠 Adding Loan EMI Calculator to Homepage")
    print("=" * 45)

    try:
        if add_loan_emi_to_homepage():
            print("\n✅ Homepage updated successfully!")
            print("📱 Loan EMI Calculator button added to homepage CTA section")
            return 0
        else:
            print("\n❌ Failed to update homepage")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    # The script uses the existing WordPressClient authentication
    # Make sure you're authenticated with the WordPress site
    sys.exit(main())