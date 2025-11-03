# US Stock Market SIP Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Systematic Investment Plan (SIP) Calculator optimized for US stock market investments. Calculate returns on regular monthly investments with advanced features like step-up contributions and inflation adjustment.

## � Quick Start

### Option 1: Web Interface (Recommended)
```bash
# Clone or download the calculator
cd us-stock-market-sip-calculator

# Run setup
./setup.sh

# Start the web server
python3 run_server.py
```
Then open http://localhost:8000 in your browser.

### Option 2: Command Line
```bash
# Basic calculation
python3 sip_calculator.py --monthly 500 --return-rate 10 --years 10

# With advanced options
python3 sip_calculator.py --monthly 500 --return-rate 10 --years 10 --step-up 5 --initial 5000 --export-json results.json
```

### Option 3: Standalone Executable
```bash
# Build standalone version
./build_standalone.sh

# Run the executable
cd dist
./sip-calculator --monthly 500 --return-rate 10 --years 10
```

## 📦 Installation

### Automatic Setup
```bash
git clone <repository-url>
cd us-stock-market-sip-calculator
./setup.sh
```

### Manual Setup
```bash
# Install Python dependencies (if any)
pip install -r requirements.txt

# Make scripts executable
chmod +x run_server.py setup.sh build_standalone.sh
```

### System Requirements
- **Python**: 3.6 or higher
- **Operating System**: Linux, macOS, Windows
- **Browser**: Any modern web browser (for web interface)

### Features

- **Basic SIP Calculation**: Monthly investment with expected annual returns
- **Advanced Options**:
  - Initial lump-sum investment
  - Annual step-up in monthly investments
  - Inflation adjustment
- **Detailed Breakdowns**: Year-by-year investment and return analysis
- **Export Options**: JSON and CSV export for further analysis
- **Web Interface**: User-friendly HTML interface for easy calculations

### Usage

#### Command Line (Python Script)

```bash
# Basic SIP calculation - $500/month at 10% annual return
python3 sip_calculator.py --monthly 500 --return-rate 10 --years 10

# Advanced calculation with step-up and initial investment
python3 sip_calculator.py --monthly 500 --return-rate 10 --years 10 --step-up 5 --initial 5000

# Conservative long-term investment
python3 sip_calculator.py --monthly 300 --return-rate 8 --years 30 --initial 10000

# Export results for analysis
python3 sip_calculator.py --monthly 500 --return-rate 10 --years 10 --export-json results.json --export-csv breakdown.csv
```

#### Parameters

- `--monthly, -m`: Monthly investment amount (required)
- `--return-rate, -r`: Expected annual return rate in percentage (required)
- `--years, -y`: Investment period in years (required)
- `--initial, -i`: Initial investment amount (default: 0)
- `--inflation`: Annual inflation rate in percentage (default: 0)
- `--step-up, -s`: Annual increase in monthly investment in percentage (default: 0)
- `--export-json`: Export results to JSON file
- `--export-csv`: Export breakdown to CSV file
- `--breakdown-type`: Type of breakdown for CSV export ('yearly' or 'monthly', default: yearly)

#### Web Interface

Open `sip_calculator.html` in your web browser for an interactive calculator with:
- Real-time calculations
- Visual result display
- Export functionality
- Advanced options toggle

### Example Output

```
============================================================
           SIP CALCULATOR RESULTS
============================================================

📊 INPUT PARAMETERS:
   Monthly Investment: $500
   Annual Return Rate: 10.0%
   Investment Period: 10 years

💰 SUMMARY:
   Total Invested: $60,000
   Final Portfolio Value: $98,744
   Total Returns: $38,744
   Total Return %: 64.6%
   Average Annual Return: 5.2%

============================================================
```

### US Market Context

The calculator is optimized for US stock market investments with:
- **Default return rate**: 10% (S&P 500 historical average)
- **Conservative estimates**: 8% for long-term planning
- **Growth scenarios**: 12% for diversified equity portfolios
- **Currency**: US Dollars ($)
- **Investment amounts**: Typical US investor ranges ($100-$2,000/month)

### Calculation Methodology

The calculator uses compound interest calculations with monthly compounding:

1. **Monthly Investment**: Added at the beginning of each month
2. **Monthly Returns**: Applied to the entire portfolio value
3. **Step-up**: Monthly investment increases annually by specified percentage
4. **Inflation**: Can be factored in for more realistic projections

### Formula

The future value of SIP is calculated using:

```
FV = P × [(1 + r)^n - 1] × (1 + r) / r
```

Where:
- FV = Future Value
- P = Monthly Investment
- r = Monthly return rate
- n = Number of months

## Contributing

To add new calculators:

1. Create a new Python script in the calculators directory
2. Add corresponding HTML interface if needed
3. Update this README with usage instructions
4. Test thoroughly with various input scenarios

## 📦 Distribution & Publishing

### Creating Standalone Executable
```bash
# Build for current platform
./build_standalone.sh

# The dist/ directory will contain:
# - sip-calculator (executable)
# - sip_calculator.html (web interface)
# - README.md and documentation
# - run_sip_calculator.sh/.bat (launchers)
```

### Web Deployment
The calculator can be deployed as a static website:
1. Upload `sip_calculator.html` to any web server
2. No server-side processing required
3. All calculations run client-side in JavaScript

### Python Package
For integration into other Python projects:
```python
from sip_calculator import SIPCalculator

calculator = SIPCalculator()
results = calculator.calculate_sip(
    monthly_investment=500,
    annual_return_rate=0.10,
    investment_period_years=10
)
calculator.print_summary()
```

## 🛠️ Development

### Project Structure
```
us-stock-market-sip-calculator/
├── sip_calculator.py          # Main Python calculator
├── sip_calculator.html        # Web interface
├── run_server.py             # Local web server
├── test_sip_calculator.py     # Test suite
├── setup.sh                   # Installation script
├── build_standalone.sh        # Build script
├── requirements.txt           # Python dependencies
├── package.json              # Package metadata
└── README.md                 # This file
```

### Running Tests
```bash
python3 test_sip_calculator.py
```

### Adding New Features
1. Update `sip_calculator.py` for core logic
2. Update `sip_calculator.html` for web interface
3. Add tests to `test_sip_calculator.py`
4. Update documentation in README.md

## 📊 Examples

### Basic Retirement Planning
```bash
# 30 years of $1000/month at 8% returns
python3 sip_calculator.py --monthly 1000 --return-rate 8 --years 30
```

### Aggressive Growth Portfolio
```bash
# 20 years of $500/month at 12% with 3% annual increase
python3 sip_calculator.py --monthly 500 --return-rate 12 --years 20 --step-up 3
```

### Conservative Long-term Investment
```bash
# 25 years of $300/month at 7% with $10K initial investment
python3 sip_calculator.py --monthly 300 --return-rate 7 --years 25 --initial 10000
```

## ⚖️ Disclaimer

This tool is provided as-is for educational and planning purposes. Past market performance does not guarantee future results. Always consult with qualified financial advisors before making investment decisions. The calculations are based on historical averages and should not be considered as financial advice.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.