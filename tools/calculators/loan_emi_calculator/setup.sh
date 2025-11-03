#!/bin/bash
# Setup script for Loan EMI Calculator
# This script sets up the calculator for use on Linux/macOS systems

set -e  # Exit on any error

echo "🏠 Loan EMI Calculator Setup"
echo "================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3.6 or higher from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.6"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x run_server.py
chmod +x build_standalone.sh
echo "✅ Scripts are now executable"

# Create virtual environment (optional)
read -p "🤔 Create a virtual environment? (recommended) [Y/n]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv

    echo "🔄 Activating virtual environment..."
    source venv/bin/activate

    echo "📚 No additional packages needed (uses only standard library)"
    echo "✅ Virtual environment ready"
    echo ""
    echo "To activate the virtual environment in future sessions:"
    echo "  source venv/bin/activate"
    echo ""
fi

# Run tests to verify everything works
echo "🧪 Running tests to verify installation..."
if python3 test_loan_emi_calculator.py > /dev/null 2>&1; then
    echo "✅ All tests passed!"
else
    echo "⚠️  Some tests failed, but basic functionality should still work"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Usage options:"
echo "1. Run calculator directly:"
echo "   python3 loan_emi_calculator.py"
echo ""
echo "2. Start web interface:"
echo "   python3 run_server.py"
echo "   Then open http://localhost:8000 in your browser"
echo ""
echo "3. Build standalone executable:"
echo "   ./build_standalone.sh"
echo ""
echo "4. Run tests:"
echo "   python3 test_loan_emi_calculator.py"
echo ""
echo "📖 See README.md for detailed usage instructions"