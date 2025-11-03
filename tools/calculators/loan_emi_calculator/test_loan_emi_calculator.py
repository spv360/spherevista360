#!/usr/bin/env python3
"""
Test suite for Loan EMI Calculator
Tests EMI calculations, amortization schedules, and loan eligibility features.
"""

import unittest
import json
import csv
import tempfile
import os
from loan_emi_calculator import LoanEMICalculator


class TestLoanEMICalculator(unittest.TestCase):
    """Test cases for LoanEMICalculator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.calculator = LoanEMICalculator()

    def test_calculate_emi_basic(self):
        """Test basic EMI calculation"""
        # Test case: $100,000 loan at 12% for 5 years
        results = self.calculator.calculate_emi(100000, 0.12, 5, 0)

        # Expected monthly EMI (approximately)
        expected_emi = 2224.44  # Corrected expected value based on standard EMI formula
        self.assertAlmostEqual(results['monthly_emi'], expected_emi, places=2)

        # Total amount should be EMI * number of months
        expected_total = expected_emi * 60
        self.assertAlmostEqual(results['total_amount'], expected_total, places=0)  # Allow for rounding differences

        # Total interest should be total amount - principal
        expected_interest = expected_total - 100000
        self.assertAlmostEqual(results['total_interest'], expected_interest, places=0)  # Allow for rounding differences

    def test_calculate_emi_with_months(self):
        """Test EMI calculation with additional months"""
        # Test case: $50,000 loan at 10% for 3 years and 6 months
        results = self.calculator.calculate_emi(50000, 0.10, 3, 6)

        # Should have 42 months total
        self.assertEqual(results['total_months'], 42)

        # EMI should be reasonable
        self.assertGreater(results['monthly_emi'], 0)
        self.assertLess(results['monthly_emi'], 2000)

    def test_amortization_schedule(self):
        """Test amortization schedule generation"""
        results = self.calculator.calculate_emi(100000, 0.12, 1, 0)  # 1 year for easier testing

        schedule = results['amortization_schedule']
        self.assertEqual(len(schedule), 12)  # 12 months

        # First payment
        first_payment = schedule[0]
        self.assertEqual(first_payment['month'], 1)
        self.assertAlmostEqual(first_payment['emi'], results['monthly_emi'], places=2)

        # Interest payment should be principal * monthly_rate
        monthly_rate = 0.12 / 12
        expected_interest = 100000 * monthly_rate
        self.assertAlmostEqual(first_payment['interest_payment'], expected_interest, places=2)

        # Principal payment should be EMI - interest
        expected_principal = first_payment['emi'] - first_payment['interest_payment']
        self.assertAlmostEqual(first_payment['principal_payment'], expected_principal, places=2)

        # Last payment should have zero balance
        last_payment = schedule[-1]
        self.assertAlmostEqual(last_payment['remaining_balance'], 0, places=2)

    def test_loan_eligibility_calculation(self):
        """Test loan eligibility calculation"""
        # Test case: $5000 monthly income, $500 existing obligations, 50% max EMI
        results = self.calculator.calculate_loan_eligibility(5000, 500, 0.5)

        # Max EMI should be 50% of income
        expected_max_emi = 5000 * 0.5
        self.assertEqual(results['max_monthly_emi'], expected_max_emi)

        # Available EMI should be max EMI - existing obligations
        expected_available = expected_max_emi - 500
        self.assertEqual(results['available_emi'], expected_available)

        # Should have scenarios
        self.assertIn('scenarios', results)
        self.assertGreater(len(results['scenarios']), 0)

    def test_loan_eligibility_scenarios(self):
        """Test loan eligibility scenarios generation"""
        results = self.calculator.calculate_loan_eligibility(6000, 300, 0.4)

        scenarios = results['scenarios']

        # Should have scenarios for different rates and tenures
        self.assertGreater(len(scenarios), 0)

        # Each scenario should have required fields
        for scenario in scenarios:
            self.assertIn('rate', scenario)
            self.assertIn('tenure', scenario)
            self.assertIn('max_loan', scenario)
            self.assertIn('monthly_emi', scenario)

            # Values should be reasonable
            self.assertGreater(scenario['rate'], 0)
            self.assertLess(scenario['rate'], 1)  # Should be decimal
            self.assertGreater(scenario['tenure'], 0)
            self.assertGreaterEqual(scenario['max_loan'], 0)

    def test_print_summary(self):
        """Test summary printing (capture output)"""
        results = self.calculator.calculate_emi(75000, 0.11, 4, 0)

        # This should not raise an exception
        try:
            self.calculator.print_summary(results)
        except Exception as e:
            self.fail(f"print_summary raised an exception: {e}")

    def test_export_to_json(self):
        """Test JSON export functionality"""
        results = self.calculator.calculate_emi(80000, 0.09, 6, 0)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            self.calculator.export_to_json(results, temp_file)

            # Verify file was created and contains valid JSON
            self.assertTrue(os.path.exists(temp_file))

            with open(temp_file, 'r') as f:
                data = json.load(f)

            # Verify structure
            self.assertIn('loan_amount', data)
            self.assertIn('monthly_emi', data)
            self.assertIn('amortization_schedule', data)
            self.assertEqual(data['loan_amount'], 80000)

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_export_amortization_csv(self):
        """Test CSV export functionality"""
        results = self.calculator.calculate_emi(60000, 0.13, 3, 0)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name

        try:
            self.calculator.export_amortization_csv(results, temp_file)

            # Verify file was created
            self.assertTrue(os.path.exists(temp_file))

            # Verify CSV content
            with open(temp_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # Should have header + 36 data rows (3 years)
            self.assertEqual(len(rows), 37)  # Header + 36 months

            # Check header
            self.assertEqual(rows[0], ['Month', 'EMI', 'Interest Payment', 'Principal Payment', 'Remaining Balance'])

            # Check first data row
            first_row = rows[1]
            self.assertEqual(int(first_row[0]), 1)  # Month 1

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""

        # Very small loan
        results = self.calculator.calculate_emi(1000, 0.05, 1, 0)
        self.assertGreater(results['monthly_emi'], 0)

        # High interest rate
        results = self.calculator.calculate_emi(50000, 0.25, 2, 0)
        self.assertGreater(results['monthly_emi'], 0)

        # Long tenure
        results = self.calculator.calculate_emi(200000, 0.08, 25, 0)
        self.assertEqual(results['total_months'], 300)  # 25 years

        # Zero existing obligations for eligibility
        results = self.calculator.calculate_loan_eligibility(4000, 0, 0.6)
        self.assertEqual(results['available_emi'], 4000 * 0.6)

    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""

        # Negative loan amount should raise ValueError
        with self.assertRaises(ValueError):
            self.calculator.calculate_emi(-10000, 0.12, 5, 0)

        # Zero interest rate should raise ValueError
        with self.assertRaises(ValueError):
            self.calculator.calculate_emi(100000, 0, 5, 0)

        # Negative tenure should raise ValueError
        with self.assertRaises(ValueError):
            self.calculator.calculate_emi(100000, 0.12, -1, 0)

        # Invalid months (negative) should raise ValueError
        with self.assertRaises(ValueError):
            self.calculator.calculate_emi(100000, 0.12, 5, -2)

    def test_real_world_scenarios(self):
        """Test with real-world loan scenarios"""

        # Home loan scenario
        home_loan = self.calculator.calculate_emi(300000, 0.085, 20, 0)
        self.assertGreater(home_loan['monthly_emi'], 2000)
        self.assertLess(home_loan['monthly_emi'], 3000)

        # Car loan scenario
        car_loan = self.calculator.calculate_emi(25000, 0.095, 5, 0)
        self.assertGreater(car_loan['monthly_emi'], 500)
        self.assertLess(car_loan['monthly_emi'], 600)

        # Personal loan scenario
        personal_loan = self.calculator.calculate_emi(15000, 0.15, 3, 0)
        self.assertGreater(personal_loan['monthly_emi'], 500)
        self.assertLess(personal_loan['monthly_emi'], 700)


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoanEMICalculator)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")

    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")