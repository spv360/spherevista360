# Loan EMI Calculator

A comprehensive Python-based loan calculator that helps users calculate Equated Monthly Installments (EMI), generate amortization schedules, and assess loan eligibility based on income.

## Features

### 🧮 EMI Calculation
- Calculate monthly EMI using standard financial formulas
- Support for different loan amounts, interest rates, and tenures
- Handles both years and months for flexible tenure input

### 📊 Amortization Schedule
- Generate detailed month-by-month repayment breakdown
- Shows interest payment, principal payment, and remaining balance
- Export functionality for CSV and JSON formats

### 💰 Loan Eligibility Assessment
- Calculate maximum loan amount based on monthly income
- Account for existing financial obligations
- Multiple scenarios with different interest rates and tenures

### 📈 Export Options
- Export EMI results to JSON format
- Export amortization schedule to CSV format
- Ready for integration with other financial tools

## Installation

### Option 1: Direct Python Usage
```bash
# Clone or download the calculator
cd /path/to/loan_emi_calculator

# Run the calculator
python loan_emi_calculator.py
```

### Option 2: Web Interface
```bash
# Start the local web server
python run_server.py

# Open browser to http://localhost:8000
```

### Option 3: Standalone Executable
```bash
# Build standalone executable
./build_standalone.sh

# Run the executable
./dist/loan_emi_calculator
```

## Usage

### Python API

```python
from loan_emi_calculator import LoanEMICalculator

calculator = LoanEMICalculator()

# Calculate EMI
results = calculator.calculate_emi(
    loan_amount=100000,    # $100,000 loan
    interest_rate=0.12,    # 12% annual interest
    tenure_years=5,        # 5 years
    tenure_months=0        # 0 additional months
)

print(f"Monthly EMI: ${results['monthly_emi']:.2f}")
print(f"Total Amount: ${results['total_amount']:.2f}")
print(f"Total Interest: ${results['total_interest']:.2f}")

# Check loan eligibility
eligibility = calculator.calculate_loan_eligibility(
    monthly_income=5000,      # $5,000 monthly income
    existing_obligations=500, # $500 existing EMIs
    max_emi_percentage=0.5    # 50% of income for EMI
)

print(f"Maximum Monthly EMI: ${eligibility['max_monthly_emi']:.2f}")
print(f"Available EMI: ${eligibility['available_emi']:.2f}")
```

### Command Line Interface

```bash
# Calculate EMI
python loan_emi_calculator.py --loan-amount 100000 --interest-rate 12 --tenure-years 5

# Check eligibility
python loan_emi_calculator.py --monthly-income 5000 --existing-obligations 500 --max-emi-percentage 50
```

### Web Interface

1. Start the web server:
   ```bash
   python run_server.py
   ```

2. Open your browser to `http://localhost:8000`

3. Use the interactive calculator with:
   - EMI Calculator tab for loan calculations
   - Loan Eligibility tab for affordability assessment

## Examples

### Example 1: Home Loan Calculation
```python
# $300,000 home loan at 8.5% for 20 years
results = calculator.calculate_emi(300000, 0.085, 20, 0)
# Monthly EMI: ~$2,484
```

### Example 2: Car Loan Calculation
```python
# $25,000 car loan at 9.5% for 5 years
results = calculator.calculate_emi(25000, 0.095, 5, 0)
# Monthly EMI: ~$532
```

### Example 3: Loan Eligibility Check
```python
# Income: $6,000/month, Obligations: $300, Max EMI: 40%
eligibility = calculator.calculate_loan_eligibility(6000, 300, 0.4)
# Available EMI: $2,100
# Can afford loans up to various amounts based on rates/tenures
```

## Mathematical Formulas

### EMI Calculation
```
EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)

Where:
- P = Principal loan amount
- r = Monthly interest rate (annual rate / 12)
- n = Total number of months
```

### Monthly Interest Rate
```
r = Annual Interest Rate / 12
```

### Total Amount Payable
```
Total Amount = EMI × n
```

### Total Interest
```
Total Interest = Total Amount - Principal
```

## File Structure

```
loan_emi_calculator/
├── loan_emi_calculator.py      # Main calculator class
├── loan_emi_calculator.html    # Web interface
├── test_loan_emi_calculator.py # Comprehensive test suite
├── run_server.py             # Web server script
├── setup.sh                   # Installation script
├── build_standalone.sh        # Standalone build script
└── README.md                  # This documentation
```

## Testing

Run the comprehensive test suite:

```bash
python test_loan_emi_calculator.py
```

Tests cover:
- EMI calculations with various scenarios
- Amortization schedule generation
- Loan eligibility assessment
- Export functionality
- Edge cases and error handling
- Real-world loan scenarios

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This tool is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the calculator.

## Disclaimer

This calculator provides estimates based on standard financial formulas. Actual loan terms may vary based on lender policies, credit score, and other factors. Always consult with financial professionals for important financial decisions.