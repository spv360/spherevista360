#!/bin/bash

# SIP Calculator WordPress Setup Script
# This script helps configure the SIP calculator and tools navigation

set -e

echo "🔧 Setting up SIP Calculator and Tools Navigation"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if plugin is active
check_plugin_status() {
    print_info "Checking SIP Calculator plugin status..."

    # This would need to be run on the WordPress server
    echo "Please verify the plugin is activated in WordPress admin:"
    echo "1. Go to Plugins → Installed Plugins"
    echo "2. Confirm 'SIP Calculator' is Active"
    echo ""
}

# Create setup instructions
create_setup_instructions() {
    print_info "Creating WordPress setup instructions..."

    cat > "WORDPRESS_TOOLS_SETUP.md" << 'EOF'
# WordPress Tools Setup Guide

## Step 1: Create SIP Calculator Page

1. **Login to WordPress Admin**
   - Go to your WordPress dashboard

2. **Create New Page**
   - Pages → Add New
   - Title: "SIP Calculator"
   - Permalink: `/sip-calculator/` (WordPress will auto-generate this)

3. **Add Calculator Content**
   - Switch to "Code Editor" (or use shortcode block)
   - Add this shortcode: `[sip_calculator]`
   - Optional: Add introductory text above the shortcode

4. **Publish Page**
   - Click "Publish"

## Step 2: Create Tools Page

1. **Create New Page**
   - Pages → Add New
   - Title: "Tools"
   - Permalink: `/tools/`

2. **Add Tools Content**
   - Copy the content from `tools_page_content.html`
   - Switch to "Code Editor" and paste the content
   - Or use the visual editor and recreate the layout

3. **Publish Page**
   - Click "Publish"

## Step 3: Add to Navigation Menu

1. **Go to Menus**
   - Appearance → Menus

2. **Add Pages to Menu**
   - Check "Tools" page
   - Check "SIP Calculator" page
   - Click "Add to Menu"

3. **Organize Menu Structure**
   - Drag "Tools" to be a top-level menu item
   - Drag "SIP Calculator" under "Tools" (make it a submenu item)
   - Or keep both as top-level items

4. **Save Menu**
   - Click "Save Menu"

## Step 4: Test Navigation

1. **Visit Your Site**
   - Go to your homepage
   - Check that "Tools" appears in navigation
   - Click "Tools" → should show tools listing page
   - Click "SIP Calculator" → should show the calculator

## Step 5: SEO Optimization (Optional)

1. **Add Meta Descriptions**
   - Install Yoast SEO or similar plugin
   - Add compelling meta descriptions for both pages

2. **Internal Linking**
   - Link to tools from your homepage or blog posts
   - Add "Try our SIP Calculator" links in relevant content

## Troubleshooting

### Calculator Not Showing
- Verify plugin is activated
- Check shortcode syntax: `[sip_calculator]`
- Clear WordPress cache if using caching plugin

### Menu Not Appearing
- Check theme supports menus
- Verify menu is assigned to correct location
- Clear browser cache

### Pages Not Found (404)
- Go to Settings → Permalinks
- Click "Save Changes" to refresh permalinks

## Customization Options

### Shortcode Parameters
```
[sip_calculator monthly_investment="500" return_rate="10" investment_period="10"]
```

### Custom CSS
Add to Appearance → Customize → Additional CSS:
```css
/* Custom styling for tools pages */
.tools-page-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
}
```

## Next Steps

1. **Add More Tools**: Expand your tools section with additional calculators
2. **Track Usage**: Use Google Analytics to monitor tool engagement
3. **User Feedback**: Add feedback forms to improve tools
4. **Mobile Optimization**: Ensure all tools work perfectly on mobile devices

## Support

If you encounter issues:
1. Check this guide first
2. Verify plugin compatibility with your WordPress version
3. Test with default WordPress theme (Twenty Twenty-One)
4. Contact plugin developer if issues persist
EOF

    print_success "Setup instructions created: WORDPRESS_TOOLS_SETUP.md"
}

# Create menu configuration script
create_menu_script() {
    print_info "Creating menu configuration script..."

    cat > "configure_tools_menu.php" << 'EOF'
<?php
/**
 * WordPress Tools Menu Configuration Script
 * Run this in your theme's functions.php or as a standalone script
 */

// Add Tools menu item programmatically
function add_tools_menu_item() {
    // Only run this once
    if (get_option('tools_menu_configured')) {
        return;
    }

    // Get primary menu
    $menu_name = 'primary'; // Change this to match your menu location
    $menu = wp_get_nav_menu_object($menu_name);

    if (!$menu) {
        // Try to get the first available menu
        $menus = wp_get_nav_menus();
        if (!empty($menus)) {
            $menu = $menus[0];
        }
    }

    if ($menu) {
        // Check if Tools page exists
        $tools_page = get_page_by_title('Tools');
        if (!$tools_page) {
            // Create Tools page
            $tools_content = '<!-- Content from tools_page_content.html -->';
            $tools_page_id = wp_insert_post(array(
                'post_title' => 'Tools',
                'post_content' => $tools_content,
                'post_status' => 'publish',
                'post_type' => 'page',
            ));
        } else {
            $tools_page_id = $tools_page->ID;
        }

        // Check if SIP Calculator page exists
        $sip_page = get_page_by_title('SIP Calculator');
        if (!$sip_page) {
            // Create SIP Calculator page
            $sip_page_id = wp_insert_post(array(
                'post_title' => 'SIP Calculator',
                'post_content' => '[sip_calculator]',
                'post_status' => 'publish',
                'post_type' => 'page',
            ));
        } else {
            $sip_page_id = $sip_page->ID;
        }

        // Add items to menu
        wp_update_nav_menu_item($menu->term_id, 0, array(
            'menu-item-title' => 'Tools',
            'menu-item-url' => get_permalink($tools_page_id),
            'menu-item-status' => 'publish',
            'menu-item-type' => 'post_type',
            'menu-item-object' => 'page',
            'menu-item-object-id' => $tools_page_id,
        ));

        wp_update_nav_menu_item($menu->term_id, 0, array(
            'menu-item-title' => 'SIP Calculator',
            'menu-item-url' => get_permalink($sip_page_id),
            'menu-item-status' => 'publish',
            'menu-item-type' => 'post_type',
            'menu-item-object' => 'page',
            'menu-item-object-id' => $sip_page_id,
            'menu-item-parent-id' => $tools_page_id, // Make it a submenu
        ));

        // Mark as configured
        update_option('tools_menu_configured', true);

        echo "Tools menu configured successfully!";
    } else {
        echo "Could not find a menu to update. Please create a menu first.";
    }
}

// Uncomment the line below to run the configuration
// add_tools_menu_config();

// Alternative: Add this to your theme's functions.php
/*
add_action('init', 'add_tools_menu_item');
*/
?>
EOF

    print_success "Menu configuration script created: configure_tools_menu.php"
}

# Create quick setup script
create_quick_setup() {
    print_info "Creating quick setup script..."

    cat > "quick_tools_setup.php" << 'EOF'
<?php
/**
 * Quick Tools Setup Script
 * Upload this to your WordPress root and run it once, then delete it
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    die('Direct access not allowed');
}

require_once('wp-load.php');

// Check if user is admin
if (!current_user_can('administrator')) {
    die('Admin access required');
}

echo "<h1>SIP Calculator Tools Setup</h1>";

// Create Tools page
$tools_content = file_get_contents('tools_page_content.html');
if ($tools_content === false) {
    $tools_content = '<!-- Add tools content here -->';
}

$tools_page = array(
    'post_title' => 'Tools',
    'post_content' => $tools_content,
    'post_status' => 'publish',
    'post_type' => 'page',
);

$tools_page_id = wp_insert_post($tools_page);

if ($tools_page_id) {
    echo "<p>✓ Tools page created (ID: $tools_page_id)</p>";
} else {
    echo "<p>✗ Failed to create Tools page</p>";
}

// Create SIP Calculator page
$sip_page = array(
    'post_title' => 'SIP Calculator',
    'post_content' => '[sip_calculator]',
    'post_status' => 'publish',
    'post_type' => 'page',
);

$sip_page_id = wp_insert_post($sip_page);

if ($sip_page_id) {
    echo "<p>✓ SIP Calculator page created (ID: $sip_page_id)</p>";
} else {
    echo "<p>✗ Failed to create SIP Calculator page</p>";
}

// Update menu
if ($tools_page_id && $sip_page_id) {
    $menu_name = 'primary';
    $menu = wp_get_nav_menu_object($menu_name);

    if (!$menu) {
        $menus = wp_get_nav_menus();
        if (!empty($menus)) {
            $menu = $menus[0];
        }
    }

    if ($menu) {
        wp_update_nav_menu_item($menu->term_id, 0, array(
            'menu-item-title' => 'Tools',
            'menu-item-url' => get_permalink($tools_page_id),
            'menu-item-status' => 'publish',
            'menu-item-type' => 'post_type',
            'menu-item-object' => 'page',
            'menu-item-object-id' => $tools_page_id,
        ));

        wp_update_nav_menu_item($menu->term_id, 0, array(
            'menu-item-title' => 'SIP Calculator',
            'menu-item-url' => get_permalink($sip_page_id),
            'menu-item-status' => 'publish',
            'menu-item-type' => 'post_type',
            'menu-item-object' => 'page',
            'menu-item-object-id' => $sip_page_id,
        ));

        echo "<p>✓ Menu items added</p>";
    } else {
        echo "<p>⚠ Could not update menu automatically</p>";
    }
}

echo "<h2>Setup Complete!</h2>";
echo "<p><strong>Next steps:</strong></p>";
echo "<ul>";
echo "<li>Check your site's navigation menu</li>";
echo "<li>Visit the Tools page: <a href='" . get_permalink($tools_page_id) . "' target='_blank'>View Tools</a></li>";
echo "<li>Visit the SIP Calculator: <a href='" . get_permalink($sip_page_id) . "' target='_blank'>View Calculator</a></li>";
echo "<li>Delete this file for security</li>";
echo "</ul>";
?>
EOF

    print_success "Quick setup script created: quick_tools_setup.php"
}

# Main function
main() {
    echo ""
    check_plugin_status
    create_setup_instructions
    create_menu_script
    create_quick_setup

    echo ""
    print_success "🎉 Tools setup files created!"
    echo ""
    echo "Next steps:"
    echo "1. Follow WORDPRESS_TOOLS_SETUP.md for manual setup"
    echo "2. Or upload quick_tools_setup.php to WordPress root and run it"
    echo "3. Test navigation and calculator functionality"
    echo ""
    echo "Files created:"
    echo "- WORDPRESS_TOOLS_SETUP.md (detailed instructions)"
    echo "- configure_tools_menu.php (menu configuration)"
    echo "- quick_tools_setup.php (automated setup)"
    echo "- tools_page_content.html (page content)"
}

main
EOF