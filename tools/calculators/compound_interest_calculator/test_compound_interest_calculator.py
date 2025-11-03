#!/usr/bin/env python3
"""
Test suite for Compound Interest Calculator
"""

import unittest
import sys
import os
from datetime import datetime

# Add the calculator directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compound_interest_calculator import CompoundInterestCalculator


class TestCompoundInterestCalculator(unittest.TestCase):
    """Test cases for the Compound Interest Calculator"""

    def setUp(self):
        """Set up test fixtures"""
        self.calculator = CompoundInterestCalculator()

    def test_basic_compound_interest(self):
        """Test basic compound interest calculation without contributions"""
        results = self.calculator.calculate_compound_interest(
            principal=1000,
            annual_rate=0.05,  # 5%
            years=10,
            compounding_frequency=12
        )

        # Expected: $1000 * (1 + 0.05/12)^(10*12) ≈ $1628.89
        expected_future_value = 1000 * (1 + 0.05/12)**(10*12)
        self.assertAlmostEqual(results['future_value'], expected_future_value, places=2)
        self.assertEqual(results['total_contributions'], 1000)
        self.assertAlmostEqual(results['total_interest_earned'], expected_future_value - 1000, places=2)

    def test_with_monthly_contributions(self):
        """Test compound interest with regular monthly contributions"""
        results = self.calculator.calculate_compound_interest(
            principal=1000,
            annual_rate=0.07,  # 7%
            years=5,
            compounding_frequency=12,
            monthly_contribution=100
        )

        # Should have initial + contributions + interest
        expected_contributions = 1000 + (100 * 5 * 12)  # $7000
        self.assertEqual(results['total_contributions'], expected_contributions)
        self.assertGreater(results['future_value'], expected_contributions)
        self.assertGreater(results['total_interest_earned'], 0)

    def test_inflation_adjustment(self):
        """Test inflation-adjusted calculations"""
        results = self.calculator.calculate_compound_interest(
            principal=10000,
            annual_rate=0.08,  # 8%
            years=20,
            compounding_frequency=12,
            inflation_rate=0.03  # 3%
        )

        # Inflation-adjusted value should be less than nominal value
        self.assertLess(results['inflation_adjusted_value'], results['future_value'])
        self.assertGreater(results['inflation_rate'], 0)

    def test_effective_annual_rate(self):
        """Test effective annual rate calculation"""
        results = self.calculator.calculate_compound_interest(
            principal=1000,
            annual_rate=0.06,  # 6%
            years=1,
            compounding_frequency=12  # Monthly
        )

        # Effective annual rate should be slightly higher than nominal rate
        self.assertGreater(results['effective_annual_rate'], 0.06)
        # EAR = (1 + r/n)^(n) - 1 = (1 + 0.06/12)^12 - 1 ≈ 0.0618
        expected_ear = (1 + 0.06/12)**12 - 1
        self.assertAlmostEqual(results['effective_annual_rate'], expected_ear, places=4)

    def test_yearly_breakdown_generation(self):
        """Test that yearly breakdown is generated correctly"""
        results = self.calculator.calculate_compound_interest(
            principal=5000,
            annual_rate=0.04,  # 4%
            years=3,
            compounding_frequency=12,
            monthly_contribution=50
        )

        breakdown = results['yearly_breakdown']
        self.assertEqual(len(breakdown), 3)  # 3 years

        # Check first year
        year1 = breakdown[0]
        self.assertEqual(year1['year'], 1)
        self.assertEqual(year1['starting_balance'], 5000)
        self.assertEqual(year1['contributions'], 50 * 12)  # $600
        self.assertGreater(year1['interest_earned'], 0)
        self.assertEqual(year1['ending_balance'], year1['starting_balance'] + year1['contributions'] + year1['interest_earned'])

        # Check that balances carry forward
        year2 = breakdown[1]
        self.assertAlmostEqual(year2['starting_balance'], year1['ending_balance'], places=2)

    def test_invalid_inputs(self):
        """Test error handling for invalid inputs"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_compound_interest(-1000, 0.05, 10)

        with self.assertRaises(ValueError):
            self.calculator.calculate_compound_interest(1000, -0.05, 10)

        with self.assertRaises(ValueError):
            self.calculator.calculate_compound_interest(1000, 0.05, 0)

    def test_edge_cases(self):
        """Test edge cases"""
        # Zero interest rate
        results = self.calculator.calculate_compound_interest(1000, 0.0, 10)
        self.assertEqual(results['future_value'], 1000)
        self.assertEqual(results['total_interest_earned'], 0)

        # Single year
        results = self.calculator.calculate_compound_interest(1000, 0.05, 1)
        expected = 1000 * (1 + 0.05/12)**12
        self.assertAlmostEqual(results['future_value'], expected, places=2)

        # High compounding frequency
        results = self.calculator.calculate_compound_interest(1000, 0.05, 1, compounding_frequency=365)
        expected = 1000 * (1 + 0.05/365)**(365)
        self.assertAlmostEqual(results['future_value'], expected, places=2)

    def test_real_world_scenario(self):
        """Test a realistic investment scenario"""
        # $10,000 initial investment, 7% annual return, 30 years, $500 monthly
        results = self.calculator.calculate_compound_interest(
            principal=10000,
            annual_rate=0.07,
            years=30,
            compounding_frequency=12,
            monthly_contribution=500,
            inflation_rate=0.025  # 2.5% inflation
        )

        # Should have substantial growth
        self.assertGreater(results['future_value'], 100000)  # At least $100k
        self.assertGreaterEqual(results['total_contributions'], 10000 + 500*30*12)  # Initial + all contributions
        self.assertLess(results['inflation_adjusted_value'], results['future_value'])  # Inflation reduces real value

    def test_export_functionality(self):
        """Test that export methods don't raise errors"""
        results = self.calculator.calculate_compound_interest(1000, 0.05, 5)

        # These should not raise exceptions
        try:
            self.calculator.export_to_json("test_results.json", results)
            self.calculator.export_to_csv("test_breakdown.csv", results)
            # Clean up test files
            if os.path.exists("test_results.json"):
                os.remove("test_results.json")
            if os.path.exists("test_breakdown.csv"):
                os.remove("test_breakdown.csv")
        except Exception as e:
            self.fail(f"Export methods raised an exception: {e}")

    def test_print_summary_without_results(self):
        """Test print_summary with no results"""
        calculator = CompoundInterestCalculator()
        # Should not raise an exception
        calculator.print_summary()


def run_demo():
    """Run a demonstration of the calculator"""
    print("Compound Interest Calculator Demo")
    print("=" * 40)

    calculator = CompoundInterestCalculator()

    # Demo 1: Basic compound interest
    print("\n1. Basic Compound Interest:")
    print("   $10,000 at 6% for 10 years")
    results1 = calculator.calculate_compound_interest(10000, 0.06, 10)
    calculator.print_summary(results1)

    # Demo 2: With monthly contributions
    print("\n2. With Monthly Contributions:")
    print("   $5,000 initial + $200/month at 7% for 20 years")
    results2 = calculator.calculate_compound_interest(5000, 0.07, 20, monthly_contribution=200)
    calculator.print_summary(results2)

    # Demo 3: With inflation adjustment
    print("\n3. With Inflation Adjustment:")
    print("   $15,000 at 8% for 25 years, 3% inflation")
    results3 = calculator.calculate_compound_interest(15000, 0.08, 25, inflation_rate=0.03)
    calculator.print_summary(results3)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        run_demo()
    else:
        # Run unit tests
        unittest.main(verbosity=2)