#!/usr/bin/env python3
"""
Loan EMI Calculator
Calculate Equated Monthly Installment for loans with detailed amortization schedule.
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import math


class LoanEMICalculator:
    """
    A comprehensive loan EMI calculator with amortization schedule.
    """

    def __init__(self):
        self.results = {}

    def calculate_emi(
        self,
        principal: float,
        annual_rate: float,
        tenure_years: int,
        tenure_months: int = 0
    ) -> Dict:
        """
        Calculate EMI for a loan.

        Args:
            principal: Loan amount
            annual_rate: Annual interest rate (as decimal, e.g., 0.12 for 12%)
            tenure_years: Loan tenure in years
            tenure_months: Additional months for tenure

        Returns:
            Dictionary containing EMI calculation results
        """
        if principal <= 0 or annual_rate <= 0 or tenure_years < 0 or tenure_months < 0 or (tenure_years <= 0 and tenure_months <= 0):
            raise ValueError("Invalid loan parameters")

        # Convert to months
        total_months = (tenure_years * 12) + tenure_months

        # Monthly interest rate
        monthly_rate = annual_rate / 12

        # EMI calculation formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
        emi = principal * monthly_rate * math.pow(1 + monthly_rate, total_months) / (
            math.pow(1 + monthly_rate, total_months) - 1
        )

        # Total amount payable
        total_amount = emi * total_months

        # Total interest payable
        total_interest = total_amount - principal

        # Generate amortization schedule
        amortization_schedule = self._generate_amortization_schedule(
            principal, monthly_rate, total_months, emi
        )

        results = {
            "loan_amount": principal,
            "annual_rate": annual_rate,
            "tenure_years": tenure_years,
            "tenure_months": tenure_months,
            "total_months": total_months,
            "monthly_emi": emi,
            "total_amount": total_amount,
            "total_interest": total_interest,
            "interest_percentage": (total_interest / principal) * 100,
            "amortization_schedule": amortization_schedule,
            "calculation_date": datetime.now().isoformat()
        }

        self.results = results
        return results

    def _generate_amortization_schedule(
        self,
        principal: float,
        monthly_rate: float,
        total_months: int,
        emi: float
    ) -> List[Dict]:
        """
        Generate month-by-month amortization schedule.
        """
        schedule = []
        remaining_balance = principal

        for month in range(1, total_months + 1):
            # Interest for this month
            monthly_interest = remaining_balance * monthly_rate

            # Principal payment for this month
            principal_payment = emi - monthly_interest

            # Remaining balance after this payment
            remaining_balance = remaining_balance - principal_payment

            # Ensure remaining balance doesn't go negative due to rounding
            if remaining_balance < 0:
                remaining_balance = 0
                principal_payment = principal_payment + remaining_balance

            schedule.append({
                "month": month,
                "emi": emi,
                "interest_payment": monthly_interest,
                "principal_payment": principal_payment,
                "remaining_balance": max(0, remaining_balance)  # Ensure non-negative
            })

        return schedule

    def calculate_loan_eligibility(
        self,
        monthly_income: float,
        existing_obligations: float = 0,
        max_emi_percentage: float = 0.50
    ) -> Dict:
        """
        Calculate maximum loan amount based on income and existing obligations.

        Args:
            monthly_income: Monthly income
            existing_obligations: Existing monthly obligations (EMIs, etc.)
            max_emi_percentage: Maximum percentage of income that can go to EMI

        Returns:
            Dictionary with loan eligibility details
        """
        max_emi = monthly_income * max_emi_percentage
        available_emi = max_emi - existing_obligations

        # For different interest rates and tenures
        scenarios = []
        rates = [0.08, 0.10, 0.12, 0.14]  # 8%, 10%, 12%, 14%
        tenures = [5, 10, 15, 20]  # years

        for rate in rates:
            for tenure in tenures:
                try:
                    # Calculate maximum loan amount for this EMI
                    monthly_rate = rate / 12
                    total_months = tenure * 12

                    if available_emi > 0:
                        # Reverse EMI formula to find principal
                        principal = available_emi * (math.pow(1 + monthly_rate, total_months) - 1) / (
                            monthly_rate * math.pow(1 + monthly_rate, total_months)
                        )
                    else:
                        principal = 0

                    scenarios.append({
                        "rate": rate,
                        "tenure": tenure,
                        "max_loan": principal,
                        "monthly_emi": available_emi
                    })
                except:
                    continue

        return {
            "monthly_income": monthly_income,
            "existing_obligations": existing_obligations,
            "max_emi_percentage": max_emi_percentage,
            "max_monthly_emi": max_emi,
            "available_emi": max(0, available_emi),
            "scenarios": scenarios
        }

    def print_summary(self, results: Optional[Dict] = None) -> None:
        """
        Print a formatted summary of the EMI calculation results.
        """
        if results is None:
            results = self.results

        if not results:
            print("No calculation results available. Run calculate_emi() first.")
            return

        print("\n" + "="*60)
        print("LOAN EMI CALCULATION SUMMARY")
        print("="*60)

        print(".2f")
        print(".1f")
        print(f"Loan Tenure: {results['tenure_years']} years {results['tenure_months']} months")
        print(f"Total Months: {results['total_months']}")
        print()

        print("PAYMENT DETAILS:")
        print("-" * 40)
        print(".2f")
        print(".2f")
        print(".2f")
        print(".1f")

        print()
        print("ADDITIONAL INFORMATION:")
        print("-" * 40)
        print(".2f")
        print(".2f")

    def export_to_json(self, results: Dict, filename: Optional[str] = None) -> None:
        """
        Export calculation results to JSON file.
        """
        if filename is None:
            filename = f"loan_emi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results exported to {filename}")

    def export_amortization_csv(self, results: Dict, filename: Optional[str] = None) -> None:
        """
        Export amortization schedule to CSV file.
        """
        if filename is None:
            filename = f"loan_amortization_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        import csv

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Month', 'EMI', 'Interest Payment', 'Principal Payment', 'Remaining Balance'])

            for payment in results['amortization_schedule']:
                writer.writerow([
                    payment['month'],
                    '.2f',
                    '.2f',
                    '.2f',
                    '.2f'
                ])

        print(f"Amortization schedule exported to {filename}")


def main():
    """
    Command-line interface for the loan EMI calculator.
    """
    parser = argparse.ArgumentParser(description="Loan EMI Calculator")
    parser.add_argument("principal", type=float, help="Loan amount")
    parser.add_argument("rate", type=float, help="Annual interest rate (as decimal, e.g., 0.12)")
    parser.add_argument("years", type=int, help="Loan tenure in years")
    parser.add_argument("--months", type=int, default=0, help="Additional months for tenure")
    parser.add_argument("--export-json", type=str, help="Export results to JSON file")
    parser.add_argument("--export-csv", type=str, help="Export amortization schedule to CSV file")

    args = parser.parse_args()

    calculator = LoanEMICalculator()

    try:
        results = calculator.calculate_emi(
            principal=args.principal,
            annual_rate=args.rate,
            tenure_years=args.years,
            tenure_months=args.months
        )

        calculator.print_summary(results)

        if args.export_json:
            calculator.export_to_json(args.export_json, results)

        if args.export_csv:
            calculator.export_amortization_csv(args.export_csv, results)

    except ValueError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())