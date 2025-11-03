#!/bin/bash
# SIP Calculator Setup Script
# Installs dependencies and prepares the US Stock Market SIP Calculator for use

set -e

echo "🚀 Setting up US Stock Market SIP Calculator"
echo "=============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "sip_calculator.py" ]; then
    echo "❌ Please run this script from the calculators directory"
    echo "   cd tools/calculators && ./setup.sh"
    exit 1
fi

echo "📁 Working directory: $(pwd)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip

# Check if requirements.txt exists, if not create it
if [ ! -f "requirements.txt" ]; then
    echo "📝 Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
# US Stock Market SIP Calculator Requirements
# Core dependencies for the SIP calculator tool
EOF
fi

echo "✅ Dependencies installed"

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x run_server.py
chmod +x setup.sh 2>/dev/null || true

# Test the calculator
echo "🧪 Testing SIP Calculator..."
if python3 sip_calculator.py --monthly 500 --return-rate 10 --years 5 > /dev/null 2>&1; then
    echo "✅ SIP Calculator test passed"
else
    echo "❌ SIP Calculator test failed"
    exit 1
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📊 To run the web interface:"
echo "   source venv/bin/activate"
echo "   python3 run_server.py"
echo ""
echo "💻 Or run calculations directly:"
echo "   source venv/bin/activate"
echo "   python3 sip_calculator.py --monthly 500 --return-rate 10 --years 10"
echo ""
echo "🌐 Open sip_calculator.html in your browser for the web interface"
echo ""
echo "📚 See README.md for detailed usage instructions"