#!/usr/bin/env python3
"""
Compound Interest Calculator
Calculate compound interest and investment growth over time.
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class CompoundInterestCalculator:
    """
    A comprehensive compound interest calculator for investment planning.
    """

    def __init__(self):
        self.results = {}

    def calculate_compound_interest(
        self,
        principal: float,
        annual_rate: float,
        years: int,
        compounding_frequency: int = 12,
        monthly_contribution: float = 0.0,
        inflation_rate: float = 0.0
    ) -> Dict:
        """
        Calculate compound interest with optional monthly contributions and inflation adjustment.

        Args:
            principal: Initial investment amount
            annual_rate: Annual interest rate (as decimal, e.g., 0.07 for 7%)
            years: Investment period in years
            compounding_frequency: How many times interest is compounded per year
            monthly_contribution: Additional monthly contribution
            inflation_rate: Annual inflation rate (as decimal)

        Returns:
            Dictionary containing calculation results
        """
        if principal < 0 or annual_rate < 0 or years <= 0:
            raise ValueError("Principal, rate, and years must be positive")

        # Calculate periodic rate
        periodic_rate = annual_rate / compounding_frequency

        # Total number of compounding periods
        total_periods = years * compounding_frequency

        # Calculate future value with compound interest
        future_value = principal * (1 + periodic_rate) ** total_periods

        # Add monthly contributions if any
        if monthly_contribution > 0:
            # Future value of annuity formula for regular contributions
            future_value += monthly_contribution * (
                ((1 + periodic_rate) ** total_periods - 1) / periodic_rate
            )

        # Calculate total contributions
        total_contributions = principal + (monthly_contribution * years * 12)

        # Calculate total interest earned
        total_interest = future_value - total_contributions

        # Adjust for inflation if specified
        if inflation_rate > 0:
            inflation_adjusted_value = future_value / ((1 + inflation_rate) ** years)
            real_return = inflation_adjusted_value - total_contributions
        else:
            inflation_adjusted_value = future_value
            real_return = total_interest

        # Calculate effective annual rate
        effective_annual_rate = (1 + periodic_rate) ** compounding_frequency - 1

        # Generate year-by-year breakdown
        yearly_breakdown = self._generate_yearly_breakdown(
            principal, annual_rate, years, compounding_frequency,
            monthly_contribution, inflation_rate
        )

        results = {
            "initial_investment": principal,
            "annual_interest_rate": annual_rate,
            "effective_annual_rate": effective_annual_rate,
            "investment_period_years": years,
            "compounding_frequency": compounding_frequency,
            "monthly_contribution": monthly_contribution,
            "total_contributions": total_contributions,
            "future_value": future_value,
            "total_interest_earned": total_interest,
            "inflation_rate": inflation_rate,
            "inflation_adjusted_value": inflation_adjusted_value,
            "real_return": real_return,
            "yearly_breakdown": yearly_breakdown,
            "calculation_date": datetime.now().isoformat()
        }

        self.results = results
        return results

    def _generate_yearly_breakdown(
        self,
        principal: float,
        annual_rate: float,
        years: int,
        compounding_frequency: int,
        monthly_contribution: float,
        inflation_rate: float
    ) -> List[Dict]:
        """
        Generate year-by-year breakdown of investment growth.
        """
        breakdown = []
        current_principal = principal
        periodic_rate = annual_rate / compounding_frequency
        periods_per_year = compounding_frequency

        for year in range(1, years + 1):
            year_start_value = current_principal

            # Add monthly contributions for the year
            yearly_contributions = monthly_contribution * 12
            current_principal += yearly_contributions

            # Apply compound interest for the year
            for _ in range(periods_per_year):
                current_principal *= (1 + periodic_rate)

            year_end_value = current_principal
            year_interest = year_end_value - year_start_value - yearly_contributions

            # Calculate inflation-adjusted values
            if inflation_rate > 0:
                inflation_factor = (1 + inflation_rate) ** year
                inflation_adjusted_value = year_end_value / inflation_factor
            else:
                inflation_adjusted_value = year_end_value

            breakdown.append({
                "year": year,
                "starting_balance": year_start_value,
                "contributions": yearly_contributions,
                "interest_earned": year_interest,
                "ending_balance": year_end_value,
                "inflation_adjusted_value": inflation_adjusted_value
            })

        return breakdown

    def print_summary(self, results: Optional[Dict] = None) -> None:
        """
        Print a formatted summary of the calculation results.
        """
        if results is None:
            results = self.results

        if not results:
            print("No calculation results available. Run calculate_compound_interest() first.")
            return

        print("\n" + "="*60)
        print("COMPOUND INTEREST CALCULATION SUMMARY")
        print("="*60)

        print(".2f")
        print(".1f")
        print(".1f")
        print(f"Compounding Frequency: {results['compounding_frequency']} times per year")
        if results['monthly_contribution'] > 0:
            print(".2f")
        print(f"Investment Period: {results['investment_period_years']} years")
        print()

        print("RESULTS:")
        print("-" * 40)
        print(".2f")
        print(".2f")
        print(".2f")
        print(".2f")

        if results['inflation_rate'] > 0:
            print(".2f")
            print(".2f")

        print()
        print("YEAR-BY-YEAR BREAKDOWN:")
        print("-" * 80)
        print("<4")
        print("-" * 80)

        for year_data in results['yearly_breakdown']:
            print("<4")

    def export_to_json(self, filename: str, results: Optional[Dict] = None) -> None:
        """
        Export calculation results to JSON file.
        """
        if results is None:
            results = self.results

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results exported to {filename}")

    def export_to_csv(self, filename: str, results: Optional[Dict] = None) -> None:
        """
        Export yearly breakdown to CSV file.
        """
        if results is None:
            results = self.results

        import csv

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Year', 'Starting Balance', 'Contributions', 'Interest Earned',
                           'Ending Balance', 'Inflation Adjusted Value'])

            for year_data in results['yearly_breakdown']:
                writer.writerow([
                    year_data['year'],
                    '.2f',
                    '.2f',
                    '.2f',
                    '.2f',
                    '.2f'
                ])

        print(f"Yearly breakdown exported to {filename}")


def main():
    """
    Command-line interface for the compound interest calculator.
    """
    parser = argparse.ArgumentParser(description="Compound Interest Calculator")
    parser.add_argument("principal", type=float, help="Initial investment amount")
    parser.add_argument("rate", type=float, help="Annual interest rate (as decimal, e.g., 0.07)")
    parser.add_argument("years", type=int, help="Investment period in years")
    parser.add_argument("--frequency", type=int, default=12,
                       help="Compounding frequency per year (default: 12)")
    parser.add_argument("--monthly", type=float, default=0.0,
                       help="Monthly contribution amount (default: 0)")
    parser.add_argument("--inflation", type=float, default=0.0,
                       help="Annual inflation rate (as decimal, default: 0)")
    parser.add_argument("--export-json", type=str,
                       help="Export results to JSON file")
    parser.add_argument("--export-csv", type=str,
                       help="Export yearly breakdown to CSV file")

    args = parser.parse_args()

    calculator = CompoundInterestCalculator()

    try:
        results = calculator.calculate_compound_interest(
            principal=args.principal,
            annual_rate=args.rate,
            years=args.years,
            compounding_frequency=args.frequency,
            monthly_contribution=args.monthly,
            inflation_rate=args.inflation
        )

        calculator.print_summary(results)

        if args.export_json:
            calculator.export_to_json(args.export_json, results)

        if args.export_csv:
            calculator.export_to_csv(args.export_csv, results)

    except ValueError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())