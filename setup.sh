#!/bin/bash
# SphereVista360 Toolkit Setup
# Adds the bin/ directory to your PATH for easy access to convenience scripts

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN_DIR="$PROJECT_DIR/bin"

echo "🔧 SphereVista360 Toolkit Setup"
echo "================================"
echo ""
echo "This will add the toolkit bin/ directory to your PATH for easy access."
echo "Project directory: $PROJECT_DIR"
echo "Bin directory: $BIN_DIR"
echo ""

# Detect shell
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"fish"* ]]; then
    SHELL_RC="$HOME/.config/fish/config.fish"
    PATH_COMMAND="set -gx PATH $BIN_DIR \$PATH"
else
    SHELL_RC="$HOME/.bashrc"
fi

# Default PATH command for bash/zsh
if [[ -z "$PATH_COMMAND" ]]; then
    PATH_COMMAND="export PATH=\"$BIN_DIR:\$PATH\""
fi

echo "Detected shell: $SHELL"
echo "Shell config: $SHELL_RC"
echo ""

# Check if already in PATH
if echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "✅ Bin directory is already in your PATH!"
    echo ""
    echo "Available commands:"
    echo "  fix-links.sh         - Fix broken links in website content"
    echo "  comprehensive-fix.sh - Run comprehensive validation and fixing"
    echo ""
else
    echo "Would you like to add the bin/ directory to your PATH? (y/n)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "" >> "$SHELL_RC"
        echo "# SphereVista360 Toolkit" >> "$SHELL_RC"
        echo "$PATH_COMMAND" >> "$SHELL_RC"
        
        echo "✅ Added to $SHELL_RC"
        echo ""
        echo "Please run: source $SHELL_RC"
        echo "Or restart your terminal to use the commands globally."
        echo ""
        echo "Available commands after setup:"
        echo "  fix-links.sh         - Fix broken links in website content"
        echo "  comprehensive-fix.sh - Run comprehensive validation and fixing"
        echo ""
    else
        echo "Setup cancelled. You can run scripts directly:"
        echo "  $BIN_DIR/fix-links.sh"
        echo "  $BIN_DIR/comprehensive-fix.sh"
        echo ""
    fi
fi

echo "🎯 Manual Usage:"
echo "Without PATH setup, you can always run:"
echo "  ./bin/fix-links.sh"
echo "  ./bin/comprehensive-fix.sh"
echo ""
echo "Or add this project's bin/ to PATH manually:"
echo "  export PATH=\"$BIN_DIR:\$PATH\""