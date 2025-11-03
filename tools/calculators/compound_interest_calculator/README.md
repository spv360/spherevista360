# Compound Interest Calculator

A comprehensive compound interest calculator for investment planning and financial analysis.

## Features

- **Accurate Calculations**: Uses standard compound interest formulas with support for different compounding frequencies
- **Regular Contributions**: Factor in monthly investments to see how consistent saving accelerates growth
- **Inflation Adjustment**: Account for inflation to understand your real purchasing power
- **Year-by-Year Breakdown**: Detailed annual view of your investment growth and contributions
- **Export Options**: Export results to JSON or CSV for further analysis
- **Web Interface**: Beautiful, responsive web interface for easy use

## Usage

### Python Script

```bash
# Basic calculation
python compound_interest_calculator.py 10000 0.07 10

# With monthly contributions
python compound_interest_calculator.py 5000 0.08 20 --monthly 200

# With inflation adjustment
python compound_interest_calculator.py 10000 0.06 30 --inflation 0.03

# Export results
python compound_interest_calculator.py 10000 0.07 10 --export-json results.json --export-csv breakdown.csv
```

### Web Interface

Open `compound_interest_calculator.html` in your web browser for an interactive calculator.

### Python Library

```python
from compound_interest_calculator import CompoundInterestCalculator

calculator = CompoundInterestCalculator()
results = calculator.calculate_compound_interest(
    principal=10000,
    annual_rate=0.07,  # 7%
    years=20,
    compounding_frequency=12,  # Monthly
    monthly_contribution=100,
    inflation_rate=0.025  # 2.5%
)

calculator.print_summary(results)
```

## Parameters

- `principal`: Initial investment amount (required)
- `annual_rate`: Annual interest rate as decimal (e.g., 0.07 for 7%) (required)
- `years`: Investment period in years (required)
- `compounding_frequency`: How many times interest is compounded per year (default: 12)
- `monthly_contribution`: Additional monthly contribution (default: 0)
- `inflation_rate`: Annual inflation rate as decimal (default: 0)

## Examples

### Example 1: Retirement Planning
```python
# $10,000 initial investment, 7% annual return, 30 years, $300 monthly contributions
results = calculator.calculate_compound_interest(10000, 0.07, 30, monthly_contribution=300)
# Result: ~$500,000+ future value
```

### Example 2: College Savings
```python
# $5,000 initial, 6% return, 18 years, $150 monthly, 2.5% inflation
results = calculator.calculate_compound_interest(5000, 0.06, 18, monthly_contribution=150, inflation_rate=0.025)
```

### Example 3: Investment Comparison
```python
# Compare different scenarios
scenarios = [
    (10000, 0.05, 20, 0),      # 5% no contributions
    (10000, 0.05, 20, 100),    # 5% with $100/month
    (10000, 0.07, 20, 100),    # 7% with $100/month
]

for principal, rate, years, monthly in scenarios:
    results = calculator.calculate_compound_interest(principal, rate, years, monthly_contribution=monthly)
    print(f"Rate: {rate*100}%, Monthly: ${monthly}")
    print(f"Future Value: ${results['future_value']:,.2f}")
```

## Testing

Run the test suite:

```bash
python test_compound_interest_calculator.py
```

Run a demonstration:

```bash
python test_compound_interest_calculator.py demo
```

## Files

- `compound_interest_calculator.py`: Main calculator class and command-line interface
- `compound_interest_calculator.html`: Web interface
- `test_compound_interest_calculator.py`: Comprehensive test suite
- `README.md`: This documentation

## Dependencies

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This tool is provided as-is for educational and personal use.