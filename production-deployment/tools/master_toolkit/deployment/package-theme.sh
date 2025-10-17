#!/bin/bash

# SphereVista360 Professional Theme Packaging Script
# This script packages the theme for manual upload to WordPress

set -e

echo "📦 Packaging SphereVista360 Professional Theme..."

# Configuration
THEME_NAME="spherevista-theme"
THEME_DIR="/home/kddevops/projects/spherevista360/spherevista-theme"
PACKAGE_DIR="/home/kddevops/projects/spherevista360/theme-package"
ZIP_NAME="spherevista360-professional-theme.zip"

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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create package directory
print_status "Creating package directory..."
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR/$THEME_NAME"

# Copy theme files
print_status "Copying theme files..."
cp -r "$THEME_DIR/"* "$PACKAGE_DIR/$THEME_NAME/"

# Create theme info file
print_status "Creating theme information file..."
cat > "$PACKAGE_DIR/INSTALLATION_INSTRUCTIONS.md" << 'EOF'
# SphereVista360 Professional Theme - Installation Instructions

## Quick Installation Guide

### Method 1: WordPress Admin Upload (Recommended)

1. **Login to WordPress Admin**:
   - Go to your WordPress admin dashboard
   - Navigate to `Appearance > Themes`

2. **Upload Theme**:
   - Click "Add New" button
   - Click "Upload Theme" button
   - Choose the `spherevista360-professional-theme.zip` file
   - Click "Install Now"

3. **Activate Theme**:
   - After installation, click "Activate"
   - Your theme is now live!

### Method 2: FTP/cPanel Upload

1. **Extract the ZIP file** to get the `spherevista-theme` folder

2. **Upload via FTP/cPanel**:
   - Connect to your website via FTP or cPanel File Manager
   - Navigate to `/wp-content/themes/`
   - Upload the entire `spherevista-theme` folder

3. **Activate via WordPress Admin**:
   - Go to `Appearance > Themes`
   - Find "SphereVista360 Professional"
   - Click "Activate"

## Required Setup After Installation

### 1. Set Up Menus
- Go to `Appearance > Menus`
- Create a new menu called "Primary Navigation"
- Add your pages/links to the menu
- Assign it to the "Primary" location

### 2. Configure Widgets
- Go to `Appearance > Widgets`
- Add widgets to the footer areas:
  - Footer Widget Area 1: About/Contact info
  - Footer Widget Area 2: Recent posts or categories
  - Footer Widget Area 3: Social media or newsletter signup

### 3. Customize Theme
- Go to `Appearance > Customize`
- Set your site logo and colors
- Configure homepage settings
- Set up social media links

### 4. Recommended Plugins
- **Yoast SEO**: For enhanced SEO features
- **Contact Form 7**: For contact forms
- **WP Super Cache**: For performance optimization

## Theme Features

✅ **Professional Design**: Modern gradient design perfect for finance/tech content
✅ **Fully Responsive**: Works perfectly on all devices
✅ **Dark Mode**: Automatic dark/light mode switching
✅ **SEO Optimized**: Built-in SEO best practices
✅ **Fast Loading**: Optimized for speed and performance
✅ **Enhanced Search**: Advanced search functionality
✅ **Social Sharing**: Built-in social media sharing

## Support

For any issues or customization needs, refer to the README.md file included in the theme package.

---
**SphereVista360 Professional Theme v1.0.0**
EOF

# Create README for the package
print_status "Creating package README..."
cat > "$PACKAGE_DIR/README.md" << 'EOF'
# SphereVista360 Professional WordPress Theme Package

This package contains a complete, professional WordPress theme designed specifically for SphereVista360.

## What's Included

- ✅ Complete WordPress theme files
- ✅ Professional styling and responsive design
- ✅ Dark mode support
- ✅ Enhanced functionality and SEO optimization
- ✅ Installation instructions
- ✅ Documentation

## Quick Start

1. Upload `spherevista360-professional-theme.zip` to WordPress
2. Activate the theme
3. Follow the setup instructions in `INSTALLATION_INSTRUCTIONS.md`

## Theme Features

- Modern professional design with gradient styling
- Fully responsive layout for all devices
- Dark mode toggle functionality
- Enhanced search with filters
- SEO optimized structure
- Social sharing buttons
- Reading time calculation
- Related posts suggestions
- Professional 404 error page
- Advanced navigation and breadcrumbs

## Files Structure

```
spherevista-theme/
├── style.css          # Main stylesheet
├── script.js          # JavaScript functionality
├── functions.php      # WordPress theme functions
├── index.php          # Homepage template
├── header.php         # Header template
├── footer.php         # Footer template
├── page.php           # Page template
├── single.php         # Blog post template
├── archive.php        # Archive template
├── search.php         # Search template
├── 404.php            # 404 error page
└── README.md          # Theme documentation
```

For detailed installation and customization instructions, see `INSTALLATION_INSTRUCTIONS.md`.
EOF

# Add version info to style.css if not present
print_status "Updating theme version info..."
if ! grep -q "Version:" "$PACKAGE_DIR/$THEME_NAME/style.css"; then
    # Add version header to style.css
    sed -i '1i/*\nTheme Name: SphereVista360 Professional\nDescription: A modern, professional WordPress theme for finance and technology content\nVersion: 1.0.0\nAuthor: SphereVista360 Development Team\nLicense: GPL v2 or later\n*/' "$PACKAGE_DIR/$THEME_NAME/style.css"
fi

# Create the ZIP package
print_status "Creating ZIP package..."
cd "$PACKAGE_DIR"
zip -r "$ZIP_NAME" . -x "*.DS_Store" "*/.*"

# Move ZIP to main directory
mv "$ZIP_NAME" "/home/kddevops/projects/spherevista360/"

# Set proper permissions
chmod 644 "/home/kddevops/projects/spherevista360/$ZIP_NAME"

print_success "=============================================="
print_success "Theme packaging completed successfully!"
print_success "=============================================="
echo
print_status "📦 Package created: $ZIP_NAME"
print_status "📁 Location: /home/kddevops/projects/spherevista360/$ZIP_NAME"
echo
print_status "Next steps:"
echo "  1. Download the ZIP file: $ZIP_NAME"
echo "  2. Login to your WordPress admin dashboard"
echo "  3. Go to Appearance > Themes > Add New"
echo "  4. Click 'Upload Theme' and select the ZIP file"
echo "  5. Install and activate the theme"
echo "  6. Follow the setup instructions included in the package"
echo
print_success "Your professional theme is ready for deployment! 🎉"

# Show package contents
echo
print_status "Package contents:"
ls -la "/home/kddevops/projects/spherevista360/$ZIP_NAME"
unzip -l "/home/kddevops/projects/spherevista360/$ZIP_NAME" | head -20
echo
print_warning "Installation instructions and documentation are included in the package."