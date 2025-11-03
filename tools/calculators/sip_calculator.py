#!/usr/bin/env python3
"""
SIP (Systematic Investment Plan) Calculator
==========================================

A comprehensive tool to calculate returns on regular monthly investments.
Supports various investment scenarios and provides detailed breakdowns.
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse

class SIPCalculator:
    """SIP Calculator for systematic investment planning."""

    def __init__(self):
        """Initialize the SIP calculator."""
        self.results = {}

    def calculate_sip(self,
                     monthly_investment: float,
                     annual_return_rate: float,
                     investment_period_years: int,
                     initial_investment: float = 0.0,
                     inflation_rate: float = 0.0,
                     step_up_percentage: float = 0.0) -> Dict:
        """
        Calculate SIP returns with comprehensive breakdown.

        Args:
            monthly_investment: Monthly investment amount
            annual_return_rate: Expected annual return rate (as decimal, e.g., 0.12 for 12%)
            investment_period_years: Total investment period in years
            initial_investment: One-time initial investment amount
            inflation_rate: Annual inflation rate for step-up calculations
            step_up_percentage: Annual increase in monthly investment

        Returns:
            Dictionary containing calculation results
        """

        # Convert annual rates to monthly
        monthly_return_rate = annual_return_rate / 12
        monthly_inflation_rate = inflation_rate / 12

        # Initialize variables
        total_invested = initial_investment
        current_value = initial_investment
        monthly_breakdown = []
        yearly_breakdown = []

        current_monthly_investment = monthly_investment

        # Calculate month by month
        for year in range(investment_period_years):
            yearly_invested = 0
            yearly_start_value = current_value

            for month in range(12):
                # Apply monthly investment
                current_value += current_monthly_investment
                total_invested += current_monthly_investment
                yearly_invested += current_monthly_investment

                # Apply monthly returns
                current_value *= (1 + monthly_return_rate)

                monthly_breakdown.append({
                    'year': year + 1,
                    'month': month + 1,
                    'investment': current_monthly_investment,
                    'total_invested': total_invested,
                    'portfolio_value': current_value
                })

            # Calculate yearly statistics
            yearly_return = current_value - yearly_start_value - yearly_invested
            yearly_return_percentage = (yearly_return / yearly_start_value) * 100 if yearly_start_value > 0 else 0

            yearly_breakdown.append({
                'year': year + 1,
                'yearly_investment': yearly_invested,
                'cumulative_investment': total_invested,
                'portfolio_value': current_value,
                'yearly_return': yearly_return,
                'yearly_return_percentage': yearly_return_percentage
            })

            # Apply step-up for next year
            if step_up_percentage > 0:
                current_monthly_investment *= (1 + step_up_percentage)

        # Calculate final statistics
        total_returns = current_value - total_invested
        total_return_percentage = (total_returns / total_invested) * 100 if total_invested > 0 else 0
        average_annual_return = ((current_value / total_invested) ** (1 / investment_period_years) - 1) * 100

        results = {
            'input_parameters': {
                'monthly_investment': monthly_investment,
                'annual_return_rate': annual_return_rate * 100,
                'investment_period_years': investment_period_years,
                'initial_investment': initial_investment,
                'inflation_rate': inflation_rate * 100,
                'step_up_percentage': step_up_percentage * 100
            },
            'summary': {
                'total_invested': round(total_invested, 2),
                'final_portfolio_value': round(current_value, 2),
                'total_returns': round(total_returns, 2),
                'total_return_percentage': round(total_return_percentage, 2),
                'average_annual_return': round(average_annual_return, 2),
                'monthly_investment_final': round(current_monthly_investment, 2)
            },
            'yearly_breakdown': yearly_breakdown,
            'monthly_breakdown': monthly_breakdown,
            'calculated_at': datetime.now().isoformat()
        }

        self.results = results
        return results

    def export_to_json(self, filename: str) -> None:
        """Export results to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"Results exported to {filename}")

    def export_to_csv(self, filename: str, breakdown_type: str = 'yearly') -> None:
        """Export breakdown to CSV file."""
        if breakdown_type not in ['yearly', 'monthly']:
            raise ValueError("breakdown_type must be 'yearly' or 'monthly'")

        breakdown = self.results.get(f'{breakdown_type}_breakdown', [])

        if not breakdown:
            print("No breakdown data available")
            return

        with open(filename, 'w', newline='') as f:
            if breakdown:
                writer = csv.DictWriter(f, fieldnames=breakdown[0].keys())
                writer.writeheader()
                writer.writerows(breakdown)

        print(f"{breakdown_type.capitalize()} breakdown exported to {filename}")

    def print_summary(self) -> None:
        """Print a formatted summary of the calculations."""
        if not self.results:
            print("No calculation results available. Run calculate_sip() first.")
            return

        params = self.results['input_parameters']
        summary = self.results['summary']

        print("\n" + "="*60)
        print("           SIP CALCULATOR RESULTS")
        print("="*60)

        print("\n📊 INPUT PARAMETERS:")
        print(f"   Monthly Investment: ${params['monthly_investment']:,.0f}")
        print(f"   Annual Return Rate: {params['annual_return_rate']:.1f}%")
        print(f"   Investment Period: {params['investment_period_years']} years")
        if params['initial_investment'] > 0:
            print(f"   Initial Investment: ${params['initial_investment']:,.0f}")
        if params['step_up_percentage'] > 0:
            print(f"   Annual Step-up: {params['step_up_percentage']:.1f}%")

        print("\n💰 SUMMARY:")
        print(f"   Total Invested: ${summary['total_invested']:,.0f}")
        print(f"   Final Portfolio Value: ${summary['final_portfolio_value']:,.0f}")
        print(f"   Total Returns: ${summary['total_returns']:,.0f}")
        print(f"   Total Return %: {summary['total_return_percentage']:.1f}%")
        print(f"   Average Annual Return: {summary['average_annual_return']:.1f}%")

        if params['step_up_percentage'] > 0:
            print(f"   Final Monthly Investment: ${summary['monthly_investment_final']:.0f}")

        print("\n" + "="*60)

    def print_yearly_breakdown(self) -> None:
        """Print yearly breakdown of investments and returns."""
        if not self.results or 'yearly_breakdown' not in self.results:
            print("No yearly breakdown available. Run calculate_sip() first.")
            return

        print("\n" + "="*80)
        print("                        YEARLY BREAKDOWN")
        print("="*80)
        print("Year  Investment  Cumulative  Portfolio  Yearly Return  Return %")
        print("-"*80)

        for year_data in self.results['yearly_breakdown']:
            print(f"{year_data['year']:4d}  ${year_data['yearly_investment']:10,.0f}  ${year_data['cumulative_investment']:10,.0f}  ${year_data['portfolio_value']:9,.0f}  ${year_data['yearly_return']:13,.0f}  {year_data['yearly_return_percentage']:7.1f}%")

        print("="*80)

def main():
    """Command line interface for SIP calculator."""
    parser = argparse.ArgumentParser(description='SIP Calculator - Calculate Systematic Investment Plan returns')
    parser.add_argument('--monthly', '-m', type=float, required=True, help='Monthly investment amount')
    parser.add_argument('--return-rate', '-r', type=float, required=True, help='Annual return rate (percentage)')
    parser.add_argument('--years', '-y', type=int, required=True, help='Investment period in years')
    parser.add_argument('--initial', '-i', type=float, default=0, help='Initial investment amount')
    parser.add_argument('--inflation', type=float, default=0, help='Annual inflation rate for step-up (percentage)')
    parser.add_argument('--step-up', '-s', type=float, default=0, help='Annual increase in monthly investment (percentage)')
    parser.add_argument('--export-json', type=str, help='Export results to JSON file')
    parser.add_argument('--export-csv', type=str, help='Export breakdown to CSV file')
    parser.add_argument('--breakdown-type', choices=['yearly', 'monthly'], default='yearly', help='Type of breakdown for CSV export')

    args = parser.parse_args()

    # Convert percentages to decimals
    return_rate = args.return_rate / 100
    inflation_rate = args.inflation / 100 if args.inflation else 0
    step_up = args.step_up / 100 if args.step_up else 0

    # Calculate
    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=args.monthly,
        annual_return_rate=return_rate,
        investment_period_years=args.years,
        initial_investment=args.initial,
        inflation_rate=inflation_rate,
        step_up_percentage=step_up
    )

    # Display results
    calculator.print_summary()

    # Export if requested
    if args.export_json:
        calculator.export_to_json(args.export_json)

    if args.export_csv:
        calculator.export_to_csv(args.export_csv, args.breakdown_type)

if __name__ == "__main__":
    main()