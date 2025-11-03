#!/usr/bin/env python3
"""
Test script for SIP Calculator
Demonstrates various calculation scenarios
"""

from sip_calculator import SIPCalculator

def test_basic_sip():
    """Test basic SIP calculation."""
    print("🧪 Testing Basic SIP Calculation")
    print("=" * 40)

    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=500,  # $500/month (typical US investor)
        annual_return_rate=0.10,  # 10% (S&P 500 historical average)
        investment_period_years=10
    )

    calculator.print_summary()
    return results

def test_advanced_sip():
    """Test SIP with advanced options."""
    print("\n🧪 Testing Advanced SIP Calculation")
    print("=" * 40)

    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=500,
        annual_return_rate=0.10,
        investment_period_years=10,
        initial_investment=5000,  # $5,000 initial investment
        step_up_percentage=0.05  # 5% annual increase
    )

    calculator.print_summary()
    return results

def test_high_return_sip():
    """Test SIP with higher return expectations."""
    print("\n🧪 Testing High Return SIP Scenario")
    print("=" * 40)

    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=1000,  # $1,000/month
        annual_return_rate=0.12,  # 12% (growth stock average)
        investment_period_years=20,
        initial_investment=10000  # $10,000 initial investment
    )

    calculator.print_summary()
    return results

def test_export_functionality():
    """Test export functionality."""
    print("\n🧪 Testing Export Functionality")
    print("=" * 40)

    calculator = SIPCalculator()
    calculator.calculate_sip(
        monthly_investment=300,  # $300/month
        annual_return_rate=0.08,  # 8% (conservative estimate)
        investment_period_years=15
    )

    # Export to JSON
    calculator.export_to_json("test_sip_results.json")

    # Export yearly breakdown to CSV
    calculator.export_to_csv("test_yearly_breakdown.csv", "yearly")

    print("✅ Export tests completed")

def run_all_tests():
    """Run all test scenarios."""
    print("🚀 SIP Calculator Test Suite")
    print("=" * 50)

    # Run individual tests
    test_basic_sip()
    test_advanced_sip()
    test_high_return_sip()
    test_export_functionality()

    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    run_all_tests()