#!/usr/bin/env python3
"""
Generate complete WordPress configuration commands
Creates executable scripts for WP-CLI, SSH, or cPanel Terminal
"""

import os
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')

def generate_wpcli_script():
    """Generate WP-CLI commands script"""
    
    script = f'''#!/bin/bash
# WordPress Configuration Script
# Run this via SSH, cPanel Terminal, or WordPress CLI

echo "=========================================="
echo "🔧 WordPress Auto-Configuration"
echo "=========================================="
echo "Site: {WORDPRESS_URL}"
echo ""

# Navigate to WordPress root (adjust path if needed)
# cd /path/to/wordpress or cd public_html

# 1. Set static homepage
echo "🏠 Setting homepage..."
wp option update show_on_front 'page' --allow-root 2>/dev/null || wp option update show_on_front 'page'
wp option update page_on_front 2157 --allow-root 2>/dev/null || wp option update page_on_front 2157
wp option update page_for_posts 2168 --allow-root 2>/dev/null || wp option update page_for_posts 2168
echo "✅ Homepage configured!"

# 2. Update site title
echo ""
echo "📝 Updating site title..."
wp option update blogname "SphereVista360" --allow-root 2>/dev/null || wp option update blogname "SphereVista360"
wp option update blogdescription "Your 360° View on Global Insights - Finance, Technology & Innovation" --allow-root 2>/dev/null || wp option update blogdescription "Your 360° View on Global Insights - Finance, Technology & Innovation"
echo "✅ Site title updated!"

# 3. Set permalinks
echo ""
echo "🔗 Setting permalinks..."
wp rewrite structure '/%postname%/' --allow-root 2>/dev/null || wp rewrite structure '/%postname%/'
wp rewrite flush --allow-root 2>/dev/null || wp rewrite flush
echo "✅ Permalinks configured!"

# 4. Create and configure menu
echo ""
echo "🧭 Configuring menu..."

# Create menu if it doesn't exist
MENU_ID=$(wp menu list --format=ids --name="Main Navigation" --allow-root 2>/dev/null | head -n1)
if [ -z "$MENU_ID" ]; then
    MENU_ID=$(wp menu create "Main Navigation" --porcelain --allow-root 2>/dev/null || wp menu create "Main Navigation" --porcelain)
    echo "   Created menu ID: $MENU_ID"
else
    echo "   Using menu ID: $MENU_ID"
fi

# Add pages to menu
wp menu item add-post $MENU_ID 2157 --title="Home" --allow-root 2>/dev/null || wp menu item add-post $MENU_ID 2157 --title="Home"
wp menu item add-post $MENU_ID 2159 --title="About" --allow-root 2>/dev/null || wp menu item add-post $MENU_ID 2159 --title="About"
wp menu item add-post $MENU_ID 2161 --title="Services" --allow-root 2>/dev/null || wp menu item add-post $MENU_ID 2161 --title="Services"
wp menu item add-post $MENU_ID 2163 --title="Contact" --allow-root 2>/dev/null || wp menu item add-post $MENU_ID 2163 --title="Contact"

# Assign to primary location
wp menu location assign $MENU_ID primary --allow-root 2>/dev/null || wp menu location assign $MENU_ID primary
echo "✅ Menu configured!"

echo ""
echo "=========================================="
echo "✅ Configuration Complete!"
echo "=========================================="
echo ""
echo "🌐 Visit: {WORDPRESS_URL}"
echo ""
'''
    
    return script

def generate_sql_script():
    """Generate SQL commands"""
    
    sql = f'''-- WordPress Configuration SQL
-- Run these queries in phpMyAdmin or MySQL

-- Update site options
UPDATE wp_options SET option_value = 'page' WHERE option_name = 'show_on_front';
UPDATE wp_options SET option_value = '2157' WHERE option_name = 'page_on_front';
UPDATE wp_options SET option_value = '2168' WHERE option_name = 'page_for_posts';
UPDATE wp_options SET option_value = 'SphereVista360' WHERE option_name = 'blogname';
UPDATE wp_options SET option_value = 'Your 360° View on Global Insights - Finance, Technology & Innovation' WHERE option_name = 'blogdescription';
UPDATE wp_options SET option_value = '/%postname%/' WHERE option_name = 'permalink_structure';

-- Note: After running these queries, you still need to configure the menu in WordPress admin
'''
    
    return sql

def generate_php_script():
    """Generate PHP script that can be uploaded and executed"""
    
    php = f'''<?php
/**
 * WordPress Configuration Script
 * Upload this file to your WordPress root and visit it in browser
 * URL: {WORDPRESS_URL}/configure-site.php
 * Then DELETE this file after running!
 */

// Load WordPress
require_once('wp-load.php');

// Check if user is logged in as admin
if (!current_user_can('manage_options')) {{
    die('ERROR: You must be logged in as administrator to run this script.');
}}

echo '<html><head><title>WordPress Configuration</title></head><body>';
echo '<h1>WordPress Configuration</h1>';
echo '<hr>';

// 1. Set static homepage
echo '<h2>1. Setting Homepage...</h2>';
update_option('show_on_front', 'page');
update_option('page_on_front', 2157);  // Homepage
update_option('page_for_posts', 2168); // Blog
echo '<p style="color:green;">✅ Homepage configured!</p>';

// 2. Update site title
echo '<h2>2. Updating Site Title...</h2>';
update_option('blogname', 'SphereVista360');
update_option('blogdescription', 'Your 360° View on Global Insights - Finance, Technology & Innovation');
echo '<p style="color:green;">✅ Site title updated!</p>';

// 3. Set permalinks
echo '<h2>3. Setting Permalinks...</h2>';
update_option('permalink_structure', '/%postname%/');
flush_rewrite_rules();
echo '<p style="color:green;">✅ Permalinks configured!</p>';

// 4. Create menu
echo '<h2>4. Creating Navigation Menu...</h2>';

$menu_name = 'Main Navigation';
$menu_exists = wp_get_nav_menu_object($menu_name);

if (!$menu_exists) {{
    $menu_id = wp_create_nav_menu($menu_name);
    echo '<p>Created menu: ' . $menu_name . ' (ID: ' . $menu_id . ')</p>';
    
    // Add menu items
    $pages = array(
        2157 => 'Home',
        2159 => 'About',
        2161 => 'Services',
        2163 => 'Contact'
    );
    
    $position = 1;
    foreach ($pages as $page_id => $title) {{
        wp_update_nav_menu_item($menu_id, 0, array(
            'menu-item-title' => $title,
            'menu-item-object-id' => $page_id,
            'menu-item-object' => 'page',
            'menu-item-type' => 'post_type',
            'menu-item-status' => 'publish',
            'menu-item-position' => $position++
        ));
        echo '<p>Added: ' . $title . '</p>';
    }}
    
    // Assign to primary location
    $locations = get_theme_mod('nav_menu_locations');
    $locations['primary'] = $menu_id;
    set_theme_mod('nav_menu_locations', $locations);
    
    echo '<p style="color:green;">✅ Menu configured and assigned to Primary location!</p>';
}} else {{
    echo '<p style="color:orange;">Menu already exists!</p>';
}}

echo '<hr>';
echo '<h2 style="color:green;">✅ Configuration Complete!</h2>';
echo '<p><strong>Important:</strong> DELETE this file now for security!</p>';
echo '<p><a href="{WORDPRESS_URL}" target="_blank">Visit Your Site →</a></p>';
echo '<p><a href="{WORDPRESS_URL}/wp-admin/" target="_blank">WordPress Admin →</a></p>';
echo '</body></html>';
?>'''
    
    return php

def main():
    """Generate all configuration scripts"""
    
    print("=" * 60)
    print("📝 WordPress Configuration Script Generator")
    print("=" * 60)
    print(f"Site: {WORDPRESS_URL}")
    print("=" * 60)
    
    # Save WP-CLI script
    wpcli_script = generate_wpcli_script()
    with open('wordpress-config.sh', 'w') as f:
        f.write(wpcli_script)
    print("\n✅ Created: wordpress-config.sh")
    print("   Run via: SSH or cPanel Terminal")
    print("   Command: bash wordpress-config.sh")
    
    # Save SQL script
    sql_script = generate_sql_script()
    with open('wordpress-config.sql', 'w') as f:
        f.write(sql_script)
    print("\n✅ Created: wordpress-config.sql")
    print("   Run via: phpMyAdmin or MySQL client")
    
    # Save PHP script
    php_script = generate_php_script()
    with open('configure-site.php', 'w') as f:
        f.write(php_script)
    print("\n✅ Created: configure-site.php")
    print(f"   Upload to: WordPress root directory")
    print(f"   Visit: {WORDPRESS_URL}/configure-site.php")
    print("   ⚠️  DELETE after running!")
    
    print("\n" + "=" * 60)
    print("🎯 EASIEST METHOD - PHP Script:")
    print("=" * 60)
    print(f"\n1. Upload 'configure-site.php' to your WordPress root")
    print(f"2. Login to WordPress admin")
    print(f"3. Visit: {WORDPRESS_URL}/configure-site.php")
    print(f"4. Script will auto-configure everything")
    print(f"5. DELETE the file after running")
    
    print("\n" + "=" * 60)
    print("🔧 ALTERNATIVE - WP-CLI:")
    print("=" * 60)
    print(f"\n1. SSH or cPanel Terminal access")
    print(f"2. Upload wordpress-config.sh")
    print(f"3. Run: bash wordpress-config.sh")
    
    print("\n" + "=" * 60)
    print("💾 ALTERNATIVE - SQL:")
    print("=" * 60)
    print(f"\n1. Open phpMyAdmin")
    print(f"2. Select your WordPress database")
    print(f"3. Copy contents of wordpress-config.sql")
    print(f"4. Run in SQL tab")
    print(f"5. Then configure menu in WordPress admin")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
