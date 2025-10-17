#!/bin/bash

# SphereVista360 Professional Theme Deployment Script
# This script installs and activates the professional theme

set -e  # Exit on any error

echo "🚀 Starting SphereVista360 Professional Theme Deployment..."

# Configuration
THEME_NAME="spherevista-theme"
THEME_DIR="/home/kddevops/projects/spherevista360/spherevista-theme"
WP_THEMES_DIR="/var/www/html/wp-content/themes"
WP_CLI_PATH="/usr/local/bin/wp"
SITE_URL="http://localhost"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if running as appropriate user
check_permissions() {
    print_status "Checking permissions..."
    
    if [ ! -w "$WP_THEMES_DIR" ]; then
        print_error "No write permission to WordPress themes directory: $WP_THEMES_DIR"
        print_status "You may need to run with sudo or change ownership"
        exit 1
    fi
    
    print_success "Permissions check passed"
}

# Backup existing theme if it exists
backup_existing_theme() {
    print_status "Checking for existing theme..."
    
    if [ -d "$WP_THEMES_DIR/$THEME_NAME" ]; then
        BACKUP_NAME="${THEME_NAME}_backup_$(date +%Y%m%d_%H%M%S)"
        print_warning "Existing theme found. Creating backup: $BACKUP_NAME"
        
        mv "$WP_THEMES_DIR/$THEME_NAME" "$WP_THEMES_DIR/$BACKUP_NAME"
        print_success "Backup created successfully"
    else
        print_status "No existing theme found"
    fi
}

# Copy theme files
install_theme_files() {
    print_status "Installing theme files..."
    
    # Create theme directory
    mkdir -p "$WP_THEMES_DIR/$THEME_NAME"
    
    # Copy all theme files
    cp -r "$THEME_DIR/"* "$WP_THEMES_DIR/$THEME_NAME/"
    
    # Set appropriate permissions
    find "$WP_THEMES_DIR/$THEME_NAME" -type f -exec chmod 644 {} \;
    find "$WP_THEMES_DIR/$THEME_NAME" -type d -exec chmod 755 {} \;
    
    print_success "Theme files installed successfully"
}

# Create theme screenshot if it doesn't exist
create_theme_screenshot() {
    print_status "Checking for theme screenshot..."
    
    if [ ! -f "$WP_THEMES_DIR/$THEME_NAME/screenshot.png" ]; then
        print_status "Creating theme screenshot..."
        
        # Create a simple theme screenshot using ImageMagick (if available)
        if command -v convert &> /dev/null; then
            convert -size 1200x900 gradient:blue-purple \
                    -pointsize 72 -fill white -gravity center \
                    -annotate +0+0 "SphereVista360\nProfessional Theme" \
                    "$WP_THEMES_DIR/$THEME_NAME/screenshot.png"
            print_success "Theme screenshot created"
        else
            print_warning "ImageMagick not found. Skipping screenshot creation."
        fi
    else
        print_status "Theme screenshot already exists"
    fi
}

# Verify WordPress installation
verify_wordpress() {
    print_status "Verifying WordPress installation..."
    
    if [ ! -f "/var/www/html/wp-config.php" ]; then
        print_error "WordPress installation not found at /var/www/html/"
        print_status "Please ensure WordPress is properly installed"
        exit 1
    fi
    
    print_success "WordPress installation verified"
}

# Activate theme using WP-CLI
activate_theme() {
    print_status "Activating theme..."
    
    if command -v wp &> /dev/null; then
        cd /var/www/html
        
        # Check if WP-CLI can connect to the site
        if wp core is-installed --allow-root 2>/dev/null; then
            # Activate the theme
            wp theme activate $THEME_NAME --allow-root
            print_success "Theme activated successfully using WP-CLI"
            
            # Set up theme options
            setup_theme_options
        else
            print_warning "WP-CLI cannot connect to WordPress. Theme files installed but not activated."
            print_status "Please activate the theme manually from WordPress admin dashboard."
        fi
    else
        print_warning "WP-CLI not found. Theme files installed but not activated."
        print_status "Please activate the theme manually from WordPress admin dashboard."
    fi
}

# Setup theme options and customizations
setup_theme_options() {
    print_status "Setting up theme options..."
    
    cd /var/www/html
    
    # Enable theme support features
    wp option update show_on_front page --allow-root 2>/dev/null || true
    
    # Create default menus
    wp menu create "Primary Navigation" --allow-root 2>/dev/null || true
    wp menu create "Footer Menu" --allow-root 2>/dev/null || true
    
    # Set menu locations
    MENU_ID=$(wp menu list --fields=term_id --format=csv --allow-root 2>/dev/null | tail -n 1)
    if [ ! -z "$MENU_ID" ]; then
        wp menu location assign $MENU_ID primary --allow-root 2>/dev/null || true
    fi
    
    print_success "Theme options configured"
}

# Optimize theme assets
optimize_assets() {
    print_status "Optimizing theme assets..."
    
    THEME_PATH="$WP_THEMES_DIR/$THEME_NAME"
    
    # Minify CSS if tools are available
    if command -v cssmin &> /dev/null; then
        cssmin "$THEME_PATH/style.css" > "$THEME_PATH/style.min.css"
        print_success "CSS minified"
    fi
    
    # Minify JavaScript if tools are available
    if command -v uglifyjs &> /dev/null; then
        uglifyjs "$THEME_PATH/script.js" -o "$THEME_PATH/script.min.js"
        print_success "JavaScript minified"
    fi
    
    print_status "Asset optimization completed"
}

# Generate theme documentation
generate_documentation() {
    print_status "Generating theme documentation..."
    
    cat > "$WP_THEMES_DIR/$THEME_NAME/README.md" << 'EOF'
# SphereVista360 Professional Theme

A modern, responsive WordPress theme designed for professional finance and technology content.

## Features

- ✨ Modern gradient design with professional aesthetics
- 📱 Fully responsive layout for all devices
- 🎨 Dark mode support with automatic switching
- ⚡ Performance optimized with lazy loading
- 🔍 Enhanced search functionality
- 📊 SEO optimized structure
- 🎯 Focus on readability and user experience
- 🔒 Security best practices implemented

## Theme Structure

```
spherevista-theme/
├── style.css           # Main stylesheet
├── script.js          # Main JavaScript file
├── functions.php      # Theme functions
├── index.php          # Main template
├── header.php         # Header template
├── footer.php         # Footer template
├── page.php           # Page template
├── single.php         # Single post template
├── archive.php        # Archive template
├── search.php         # Search results template
├── 404.php            # 404 error page
└── README.md          # This file
```

## Customization

The theme supports WordPress Customizer for easy customization:
- Colors and branding
- Typography settings
- Layout options
- Social media links

## Requirements

- WordPress 5.0+
- PHP 7.4+
- Modern web browser with CSS Grid support

## Installation

This theme has been automatically installed and configured.

## Support

For support and customization requests, contact the development team.

## Changelog

### Version 1.0.0
- Initial release
- Modern professional design
- Full responsive layout
- Dark mode support
- Performance optimizations
EOF

    print_success "Documentation generated"
}

# Main deployment function
main() {
    echo
    print_status "SphereVista360 Professional Theme Deployment"
    print_status "=============================================="
    echo
    
    # Pre-deployment checks
    verify_wordpress
    check_permissions
    
    # Theme installation
    backup_existing_theme
    install_theme_files
    create_theme_screenshot
    
    # Theme activation and setup
    activate_theme
    optimize_assets
    generate_documentation
    
    echo
    print_success "=============================================="
    print_success "Theme deployment completed successfully!"
    print_success "=============================================="
    echo
    
    print_status "Next steps:"
    echo "  1. Visit your WordPress admin dashboard"
    echo "  2. Go to Appearance > Themes to verify activation"
    echo "  3. Customize the theme under Appearance > Customize"
    echo "  4. Set up your menus under Appearance > Menus"
    echo "  5. Configure widgets under Appearance > Widgets"
    echo
    
    if [ ! -z "$SITE_URL" ]; then
        print_status "Your site: $SITE_URL"
        print_status "Admin: $SITE_URL/wp-admin"
    fi
    
    echo
    print_success "Enjoy your new professional theme! 🎉"
}

# Run deployment
main "$@"