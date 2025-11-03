#!/bin/bash
# Build standalone executable for Loan EMI Calculator
# Uses PyInstaller to create a single executable file

set -e  # Exit on any error

echo "🏗️  Building Loan EMI Calculator Standalone Executable"
echo "======================================================="

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Check if the main script exists
if [ ! -f "loan_emi_calculator.py" ]; then
    echo "❌ loan_emi_calculator.py not found in current directory"
    exit 1
fi

echo "🔨 Building executable..."

# Create the executable
pyinstaller --onefile \
            --name loan_emi_calculator \
            --add-data "loan_emi_calculator.html:." \
            loan_emi_calculator.py

echo "✅ Build complete!"

# Check if executable was created
if [ -f "dist/loan_emi_calculator" ]; then
    echo ""
    echo "📁 Executable created: dist/loan_emi_calculator"
    echo ""
    echo "To run the calculator:"
    echo "  ./dist/loan_emi_calculator"
    echo ""
    echo "To move to a convenient location:"
    echo "  sudo mv dist/loan_emi_calculator /usr/local/bin/"
    echo "  loan_emi_calculator  # Run from anywhere"
    echo ""

    # Show file size
    FILE_SIZE=$(du -h dist/loan_emi_calculator | cut -f1)
    echo "📊 Executable size: $FILE_SIZE"

else
    echo "❌ Build failed - executable not found"
    exit 1
fi

echo ""
echo "🧹 Cleaning up build files..."
rm -rf build/
echo "✅ Cleanup complete"

echo ""
echo "🎉 Standalone executable ready!"
echo "The executable includes both CLI and basic web server functionality."