#!/bin/bash

# Fixed SphereVista360 Professional Theme Packaging Script
# This creates a properly structured ZIP for WordPress

set -e

echo "🔧 Creating Fixed SphereVista360 Professional Theme Package..."

# Configuration
THEME_NAME="spherevista-theme"
THEME_DIR="/home/kddevops/projects/spherevista360/spherevista-theme"
TEMP_DIR="/tmp/spherevista-theme-fixed"
ZIP_NAME="spherevista360-professional-theme-fixed.zip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Clean and create temp directory
print_status "Preparing theme structure..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy theme files directly to temp directory (not in a subfolder)
print_status "Copying theme files with correct structure..."
cp "$THEME_DIR/"* "$TEMP_DIR/"

# Verify style.css has proper WordPress header
print_status "Verifying style.css header..."
if ! grep -q "Theme Name:" "$TEMP_DIR/style.css"; then
    print_error "Adding proper WordPress theme header to style.css"
    
    # Create proper WordPress theme header
    cat > "$TEMP_DIR/style_temp.css" << 'EOF'
/*
Theme Name: SphereVista360 Professional
Theme URI: https://spherevista360.com
Description: A modern, professional WordPress theme designed specifically for finance and technology content. Features responsive design, dark mode support, enhanced search functionality, and SEO optimization.
Author: SphereVista360 Team
Author URI: https://spherevista360.com
Version: 1.0.0
License: GPL v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: spherevista360
Tags: business, finance, technology, responsive, dark-mode, seo, professional
Requires at least: 5.0
Tested up to: 6.3
Requires PHP: 7.4
*/

EOF
    
    # Append the existing CSS content (skip existing header if present)
    if grep -q "Theme Name:" "$TEMP_DIR/style.css"; then
        # Remove existing header and append
        sed '/^\/\*/,/\*\//d' "$TEMP_DIR/style.css" >> "$TEMP_DIR/style_temp.css"
    else
        # Just append all content
        cat "$TEMP_DIR/style.css" >> "$TEMP_DIR/style_temp.css"
    fi
    
    mv "$TEMP_DIR/style_temp.css" "$TEMP_DIR/style.css"
fi

# Add screenshot.png (WordPress themes should have this)
print_status "Creating theme screenshot..."
cat > "$TEMP_DIR/screenshot.txt" << 'EOF'
# Theme Screenshot
# For a proper theme screenshot, create a 1200x900 PNG image showing your theme design
# Save it as screenshot.png in the theme root directory
EOF

# Create functions.php with proper WordPress theme headers if missing
print_status "Verifying functions.php..."
if ! grep -q "<?php" "$TEMP_DIR/functions.php"; then
    print_error "Adding PHP opening tag to functions.php"
    sed -i '1i<?php' "$TEMP_DIR/functions.php"
fi

# Verify all required theme files exist
print_status "Verifying theme files..."
required_files=("style.css" "index.php" "functions.php")
for file in "${required_files[@]}"; do
    if [ ! -f "$TEMP_DIR/$file" ]; then
        print_error "Required file missing: $file"
        exit 1
    fi
done

# Create the properly structured ZIP file
print_status "Creating WordPress-compatible ZIP package..."
cd "$TEMP_DIR"
zip -r "/home/kddevops/projects/spherevista360/$ZIP_NAME" . -x "*.DS_Store" "*/.*"

# Clean up temp directory
rm -rf "$TEMP_DIR"

print_success "=============================================="
print_success "Fixed theme package created successfully!"
print_success "=============================================="
echo
print_status "📦 Fixed package: $ZIP_NAME"
print_status "📁 Location: /home/kddevops/projects/spherevista360/$ZIP_NAME"
echo
print_status "✅ Package structure verified for WordPress compatibility"
print_status "✅ Theme files are now in ZIP root (not subfolder)"
print_status "✅ WordPress theme headers verified"
echo
print_status "Upload instructions:"
echo "  1. Use the NEW ZIP file: $ZIP_NAME"
echo "  2. Go to WordPress Admin > Appearance > Themes"
echo "  3. Click 'Add New' > 'Upload Theme'"
echo "  4. Select the fixed ZIP file"
echo "  5. Install and activate"
echo
print_success "This fixed package should install successfully! 🎉"

# Show the fixed ZIP contents
echo
print_status "Fixed package contents:"
unzip -l "/home/kddevops/projects/spherevista360/$ZIP_NAME"