#!/usr/bin/env python3
"""
SIP Calculator Demo
Showcases the US Stock Market SIP Calculator capabilities
"""

from sip_calculator import SIPCalculator
import time

def demo_basic_calculation():
    """Demo basic SIP calculation"""
    print("📊 BASIC SIP CALCULATION DEMO")
    print("=" * 40)

    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=500,
        annual_return_rate=0.10,
        investment_period_years=10
    )

    calculator.print_summary()
    time.sleep(1)

def demo_advanced_calculation():
    """Demo advanced SIP with step-up and initial investment"""
    print("\n🚀 ADVANCED SIP CALCULATION DEMO")
    print("=" * 40)

    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=500,
        annual_return_rate=0.10,
        investment_period_years=10,
        initial_investment=5000,
        step_up_percentage=0.05  # 5% annual increase
    )

    calculator.print_summary()
    time.sleep(1)

def demo_long_term_investment():
    """Demo long-term retirement planning"""
    print("\n🏖️  LONG-TERM RETIREMENT PLANNING DEMO")
    print("=" * 40)

    calculator = SIPCalculator()
    results = calculator.calculate_sip(
        monthly_investment=1000,
        annual_return_rate=0.08,  # Conservative 8%
        investment_period_years=30
    )

    calculator.print_summary()
    time.sleep(1)

def demo_export_features():
    """Demo export functionality"""
    print("\n💾 EXPORT FEATURES DEMO")
    print("=" * 40)

    calculator = SIPCalculator()
    calculator.calculate_sip(
        monthly_investment=750,
        annual_return_rate=0.11,
        investment_period_years=15,
        initial_investment=10000
    )

    # Export to JSON
    calculator.export_to_json("demo_results.json")

    # Export yearly breakdown to CSV
    calculator.export_to_csv("demo_yearly_breakdown.csv")

    print("✅ Demo files exported:")
    print("   - demo_results.json")
    print("   - demo_yearly_breakdown.csv")

def interactive_demo():
    """Interactive demo with user input"""
    print("\n🎮 INTERACTIVE DEMO")
    print("=" * 40)

    try:
        print("Let's calculate your SIP returns!")
        monthly = float(input("Monthly investment amount ($): ") or "500")
        rate = float(input("Expected annual return rate (%): ") or "10")
        years = int(input("Investment period (years): ") or "10")
        initial = float(input("Initial investment ($): ") or "0")

        calculator = SIPCalculator()
        results = calculator.calculate_sip(
            monthly_investment=monthly,
            annual_return_rate=rate/100,
            investment_period_years=years,
            initial_investment=initial
        )

        calculator.print_summary()

        if input("Export results? (y/n): ").lower().startswith('y'):
            calculator.export_to_json("my_sip_results.json")
            print("✅ Results exported to my_sip_results.json")

    except ValueError:
        print("❌ Invalid input. Using default values...")
        demo_basic_calculation()

def main():
    """Run all demos"""
    print("🎯 US STOCK MARKET SIP CALCULATOR DEMO")
    print("=" * 50)
    print("This demo showcases various SIP calculation scenarios")
    print("Perfect for retirement planning and investment analysis")
    print("=" * 50)

    # Run demos
    demo_basic_calculation()
    demo_advanced_calculation()
    demo_long_term_investment()
    demo_export_features()

    # Interactive demo
    if input("\nTry interactive mode? (y/n): ").lower().startswith('y'):
        interactive_demo()

    print("\n🎉 Demo Complete!")
    print("=" * 50)
    print("💡 Tips:")
    print("   • Start small and increase gradually")
    print("   • Consider dollar-cost averaging benefits")
    print("   • Historical S&P 500 returns average ~10% annually")
    print("   • Always consult financial advisors for personal advice")
    print("=" * 50)

if __name__ == "__main__":
    main()