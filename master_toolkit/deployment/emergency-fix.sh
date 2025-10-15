#!/bin/bash

# Emergency WordPress Theme Debug and Fix Script
# This script helps diagnose and fix critical errors after theme activation

echo "🚨 WordPress Critical Error Emergency Fix"
echo "========================================"

# Check if we can find WordPress error logs
echo "🔍 Step 1: Checking for WordPress error logs..."

# Common WordPress error log locations
ERROR_LOGS=(
    "/var/log/apache2/error.log"
    "/var/log/nginx/error.log" 
    "/var/www/html/wp-content/debug.log"
    "/home/*/public_html/wp-content/debug.log"
    "/var/www/*/wp-content/debug.log"
)

for log in "${ERROR_LOGS[@]}"; do
    if [ -f "$log" ]; then
        echo "📋 Found error log: $log"
        echo "🔍 Recent PHP errors:"
        tail -20 "$log" | grep -i "php\|fatal\|error" || echo "No recent PHP errors found"
        echo "---"
    fi
done

echo
echo "🔧 Step 2: Creating Emergency Functions.php Fix"

# Create a minimal, safe functions.php
cat > "/tmp/emergency_functions.php" << 'EOF'
<?php
/**
 * Emergency Functions.php - Minimal Safe Version
 * SphereVista360 Professional Theme
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Basic theme setup
function spherevista360_setup() {
    // Add theme support
    add_theme_support('post-thumbnails');
    add_theme_support('automatic-feed-links');
    add_theme_support('title-tag');
    add_theme_support('html5', array(
        'search-form',
        'comment-form', 
        'comment-list',
        'gallery',
        'caption'
    ));
    
    // Register navigation menus
    register_nav_menus(array(
        'primary' => __('Primary Navigation', 'spherevista360'),
        'footer'  => __('Footer Menu', 'spherevista360')
    ));
}
add_action('after_setup_theme', 'spherevista360_setup');

// Enqueue styles and scripts safely
function spherevista360_scripts() {
    // Enqueue main stylesheet
    wp_enqueue_style(
        'spherevista360-style',
        get_stylesheet_uri(),
        array(),
        '1.0.0'
    );
    
    // Enqueue main script (only if file exists)
    $script_path = get_template_directory() . '/script.js';
    if (file_exists($script_path)) {
        wp_enqueue_script(
            'spherevista360-script',
            get_template_directory_uri() . '/script.js',
            array(),
            '1.0.0',
            true
        );
    }
}
add_action('wp_enqueue_scripts', 'spherevista360_scripts');

// Register widget areas safely
function spherevista360_widgets_init() {
    register_sidebar(array(
        'name'          => __('Footer Widget Area 1', 'spherevista360'),
        'id'            => 'footer-1',
        'description'   => __('Add widgets here.', 'spherevista360'),
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    
    register_sidebar(array(
        'name'          => __('Footer Widget Area 2', 'spherevista360'),
        'id'            => 'footer-2', 
        'description'   => __('Add widgets here.', 'spherevista360'),
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
}
add_action('widgets_init', 'spherevista360_widgets_init');

// Simple breadcrumbs function
function spherevista360_breadcrumbs() {
    if (!is_home()) {
        echo '<nav class="breadcrumbs">';
        echo '<a href="' . home_url() . '">Home</a>';
        
        if (is_single()) {
            echo ' > ';
            the_category(' > ');
            echo ' > ';
            the_title();
        } elseif (is_page()) {
            echo ' > ';
            the_title();
        } elseif (is_category() || is_tag()) {
            echo ' > ';
            single_cat_title();
        }
        
        echo '</nav>';
    }
}

// Safe reading time function
function spherevista360_reading_time() {
    $content = get_post_field('post_content', get_the_ID());
    if ($content) {
        $word_count = str_word_count(strip_tags($content));
        $reading_time = ceil($word_count / 200);
        return max(1, $reading_time);
    }
    return 1;
}
EOF

echo "✅ Emergency functions.php created"
echo
echo "🔧 Step 3: Quick Fix Instructions"
echo
echo "IMMEDIATE ACTIONS TO TRY:"
echo
echo "1. 🔄 REVERT TO DEFAULT THEME (SAFEST):"
echo "   - Go to WordPress Admin > Appearance > Themes"  
echo "   - Activate Twenty Twenty-Three or any default theme"
echo "   - This will immediately fix the critical error"
echo
echo "2. 🛠️ FIX VIA FTP/cPanel (If you can't access admin):"
echo "   - Connect to your website via FTP or cPanel File Manager"
echo "   - Navigate to /wp-content/themes/"
echo "   - Rename 'spherevista-theme' to 'spherevista-theme-disabled'"
echo "   - WordPress will automatically revert to default theme"
echo
echo "3. 🔧 REPLACE FUNCTIONS.PHP (Advanced):"
echo "   - Use the emergency functions.php we created: /tmp/emergency_functions.php"
echo "   - Replace /wp-content/themes/spherevista-theme/functions.php with this file"
echo
echo "4. 🐛 ENABLE WORDPRESS DEBUG MODE:"
echo "   - Add these lines to wp-config.php:"
echo "     define('WP_DEBUG', true);"
echo "     define('WP_DEBUG_LOG', true);"
echo "     define('WP_DEBUG_DISPLAY', false);"
echo

echo "🚨 MOST LIKELY CAUSES:"
echo "   - PHP version compatibility issue"
echo "   - Missing WordPress functions"
echo "   - Syntax error in functions.php"
echo "   - Plugin conflict"
echo "   - Memory limit exceeded"
echo

echo "📞 EMERGENCY CONTACT STEPS:"
echo "   1. Try activating a different theme first (Twenty Twenty-Three)"
echo "   2. If that works, we can debug and fix our theme"
echo "   3. Check your hosting provider's error logs"
echo "   4. Contact your hosting support if needed"
echo

read -p "Would you like me to create a minimal, safe version of the theme? (y/n): " response

if [[ $response =~ ^[Yy]$ ]]; then
    echo
    echo "🔧 Creating minimal safe theme version..."
    
    # Create minimal theme structure
    SAFE_THEME_DIR="/tmp/spherevista-theme-safe"
    mkdir -p "$SAFE_THEME_DIR"
    
    # Copy the emergency functions.php
    cp "/tmp/emergency_functions.php" "$SAFE_THEME_DIR/functions.php"
    
    # Create minimal style.css
    cat > "$SAFE_THEME_DIR/style.css" << 'EOF'
/*
Theme Name: SphereVista360 Professional (Safe Mode)
Description: Emergency safe version of SphereVista360 Professional theme
Version: 1.0.0-safe
Author: SphereVista360 Team
*/

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background: #f9f9f9;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1, h2, h3 {
    color: #333;
}

.site-header {
    background: #667eea;
    color: white;
    padding: 20px;
    margin: -20px -20px 20px -20px;
}

.site-title {
    margin: 0;
    font-size: 2rem;
}

.main-navigation ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 20px;
}

.main-navigation a {
    color: white;
    text-decoration: none;
}

.entry-content {
    margin: 20px 0;
}

.site-footer {
    background: #333;
    color: white;
    padding: 20px;
    margin: 20px -20px -20px -20px;
    text-align: center;
}
EOF

    # Create minimal index.php
    cat > "$SAFE_THEME_DIR/index.php" << 'EOF'
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>

<div class="container">
    <header class="site-header">
        <h1 class="site-title">
            <a href="<?php echo home_url(); ?>" style="color: white; text-decoration: none;">
                <?php bloginfo('name'); ?>
            </a>
        </h1>
        <p><?php bloginfo('description'); ?></p>
        
        <nav class="main-navigation">
            <?php
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'fallback_cb' => false,
            ));
            ?>
        </nav>
    </header>

    <main class="site-main">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <article class="entry">
                    <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                    <div class="entry-content">
                        <?php the_excerpt(); ?>
                    </div>
                    <p><a href="<?php the_permalink(); ?>">Read More</a></p>
                </article>
            <?php endwhile; ?>
        <?php else : ?>
            <p>No content found.</p>
        <?php endif; ?>
    </main>

    <footer class="site-footer">
        <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.</p>
    </footer>
</div>

<?php wp_footer(); ?>
</body>
</html>
EOF

    # Package the safe theme
    cd "/tmp"
    zip -r "spherevista360-safe-theme.zip" "spherevista-theme-safe/"
    
    echo "✅ Safe theme created: /tmp/spherevista360-safe-theme.zip"
    echo "📦 You can upload this as a backup theme that should work"
fi

echo
echo "🚨 PRIORITY ACTION: Switch to a default theme immediately to restore your site!"