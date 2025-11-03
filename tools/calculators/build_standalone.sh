#!/bin/bash
# Build Standalone SIP Calculator Executable
# Creates a distributable executable using PyInstaller

set -e

echo "🔨 Building Standalone SIP Calculator"
echo "====================================="

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Create spec file for PyInstaller
cat > sip_calculator.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sip_calculator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sip_calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOF

echo "🏗️  Building executable..."
pyinstaller --onefile --name sip-calculator sip_calculator.py

echo "📁 Creating distribution package..."
mkdir -p dist

# Copy additional files
cp sip_calculator.html dist/
cp README.md dist/
cp requirements.txt dist/

# Create a simple launcher script
cat > dist/run_sip_calculator.sh << 'EOF'
#!/bin/bash
# SIP Calculator Launcher

if [ -f "./sip_calculator.html" ]; then
    echo "🌐 Opening web interface..."
    if command -v xdg-open &> /dev/null; then
        xdg-open sip_calculator.html
    elif command -v open &> /dev/null; then
        open sip_calculator.html
    else
        echo "📋 Please open sip_calculator.html in your web browser"
    fi
else
    echo "❌ Web interface not found. Running command-line version..."
    ./sip-calculator --help
fi
EOF

chmod +x dist/run_sip_calculator.sh

# Create a Windows batch file launcher
cat > dist/run_sip_calculator.bat << 'EOF'
@echo off
REM SIP Calculator Launcher for Windows

if exist "sip_calculator.html" (
    echo Opening web interface...
    start sip_calculator.html
) else (
    echo Web interface not found. Running command-line version...
    sip-calculator.exe --help
)
pause
EOF

echo "📦 Creating archive..."
cd dist
if command -v tar &> /dev/null; then
    tar -czf ../sip_calculator_standalone.tar.gz *
    echo "✅ Created: sip_calculator_standalone.tar.gz"
fi

if command -v zip &> /dev/null; then
    zip -r ../sip_calculator_standalone.zip * 2>/dev/null || true
    echo "✅ Created: sip_calculator_standalone.zip"
fi

cd ..

echo ""
echo "🎉 Build Complete!"
echo "=================="
echo ""
echo "📁 Distribution files created in: dist/"
echo "📦 Archives created:"
echo "   - sip_calculator_standalone.tar.gz"
echo "   - sip_calculator_standalone.zip (if zip available)"
echo ""
echo "🚀 To run:"
echo "   cd dist"
echo "   ./sip-calculator --help"
echo "   # or open sip_calculator.html in browser"