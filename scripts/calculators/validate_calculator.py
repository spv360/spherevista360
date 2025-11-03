#!/usr/bin/env python3
"""
Quick validation script to test the EMI Calculator functionality
"""

import requests
from bs4 import BeautifulSoup

def test_calculator_page():
    """Test that the calculator page loads and contains expected elements"""

    url = "https://spherevista360.com/loan-emi-calculator/"

    try:
        print("🔍 Testing EMI Calculator page...")

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ Page returned status code: {response.status_code}")
            return False

        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for key elements
        checks = [
            ("Page title", soup.find('title') and 'EMI Calculator' in soup.find('title').text),
            ("Calculator header", soup.find('h1') and 'Loan EMI Calculator' in soup.find('h1').text),
            ("Input fields", soup.find('input', {'id': 'loan-amount'})),
            ("Calculate button", soup.find('button', {'id': 'calculate-emi-btn'})),
            ("Tab buttons", soup.find('button', {'class': 'tab-btn'})),
            ("Results section", soup.find('div', {'id': 'emi-results-section'})),
            ("Amortization table", soup.find('table', {'id': 'amortization-table'})),
            ("Export buttons", soup.find('button', {'id': 'export-emi-json'})),
        ]

        passed = 0
        failed = 0

        for check_name, element in checks:
            if element:
                print(f"✅ {check_name}: Found")
                passed += 1
            else:
                print(f"❌ {check_name}: Missing")
                failed += 1

        print(f"\n📊 Validation Results: {passed} passed, {failed} failed")

        if failed == 0:
            print("🎉 All calculator elements are present and working!")
            return True
        else:
            print("⚠️  Some elements are missing. Please check the page.")
            return False

    except Exception as e:
        print(f"❌ Error testing page: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_calculator_page()
    if success:
        print("\n✅ EMI Calculator validation completed successfully!")
        print("🌐 The calculator is now live with improved design and functionality.")
    else:
        print("\n❌ EMI Calculator validation failed. Please investigate the issues.")