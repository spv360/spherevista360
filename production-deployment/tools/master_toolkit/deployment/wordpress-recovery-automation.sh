#!/bin/bash

# WordPress Theme Debugging and Recovery Automation Script
# This script creates tools and instructions for WordPress admin recovery

echo "🔧 WordPress Theme Recovery Automation Guide"
echo "============================================="

# Create a debug information gathering script
cat > "/tmp/wordpress_debug_info.php" << 'EOF'
<?php
/**
 * WordPress Debug Information Gatherer
 * Save this as debug-info.php and upload to your WordPress root directory
 * Then visit: yoursite.com/debug-info.php
 */

// Security check - only run if logged in as admin or add a secret key
session_start();
$secret_key = "debug2025"; // Change this to something secure

if (!isset($_GET['key']) || $_GET['key'] !== $secret_key) {
    die('Access denied. Add ?key=' . $secret_key . ' to the URL');
}

echo "<h1>WordPress Debug Information</h1>";
echo "<style>body{font-family:Arial;padding:20px;} .info{background:#f0f0f0;padding:15px;margin:10px 0;border-radius:5px;} .error{color:red;} .success{color:green;}</style>";

// PHP Information
echo "<div class='info'>";
echo "<h2>PHP Information</h2>";
echo "PHP Version: " . phpversion() . "<br>";
echo "Memory Limit: " . ini_get('memory_limit') . "<br>";
echo "Max Execution Time: " . ini_get('max_execution_time') . " seconds<br>";
echo "Upload Max Filesize: " . ini_get('upload_max_filesize') . "<br>";
echo "Post Max Size: " . ini_get('post_max_size') . "<br>";
echo "</div>";

// WordPress Information
if (file_exists('wp-config.php')) {
    echo "<div class='info success'>";
    echo "<h2>WordPress Status</h2>";
    echo "✅ wp-config.php found<br>";
    
    // Include WordPress
    define('WP_USE_THEMES', false);
    require_once('wp-blog-header.php');
    
    echo "WordPress Version: " . get_bloginfo('version') . "<br>";
    echo "Site URL: " . home_url() . "<br>";
    echo "Admin URL: " . admin_url() . "<br>";
    echo "Current Theme: " . wp_get_theme()->get('Name') . "<br>";
    echo "Theme Version: " . wp_get_theme()->get('Version') . "<br>";
    echo "</div>";
    
    // Active Plugins
    echo "<div class='info'>";
    echo "<h2>Active Plugins</h2>";
    $active_plugins = get_option('active_plugins');
    if ($active_plugins) {
        foreach ($active_plugins as $plugin) {
            echo "• " . $plugin . "<br>";
        }
    } else {
        echo "No active plugins";
    }
    echo "</div>";
    
    // Theme Information
    echo "<div class='info'>";
    echo "<h2>Current Theme Details</h2>";
    $theme = wp_get_theme();
    echo "Name: " . $theme->get('Name') . "<br>";
    echo "Version: " . $theme->get('Version') . "<br>";
    echo "Author: " . $theme->get('Author') . "<br>";
    echo "Template: " . $theme->get('Template') . "<br>";
    echo "Stylesheet: " . $theme->get('Stylesheet') . "<br>";
    echo "Theme Root: " . $theme->get_theme_root() . "<br>";
    echo "</div>";
    
    // Recent Errors
    echo "<div class='info'>";
    echo "<h2>Error Log Check</h2>";
    $error_log_paths = [
        WP_CONTENT_DIR . '/debug.log',
        ABSPATH . 'wp-content/debug.log',
        ini_get('error_log')
    ];
    
    foreach ($error_log_paths as $log_path) {
        if ($log_path && file_exists($log_path)) {
            echo "<strong>Found error log:</strong> $log_path<br>";
            $recent_errors = shell_exec("tail -10 '$log_path' 2>/dev/null");
            if ($recent_errors) {
                echo "<pre style='background:#ffe6e6;padding:10px;overflow:auto;max-height:200px;'>$recent_errors</pre>";
            }
            break;
        }
    }
    echo "</div>";
    
} else {
    echo "<div class='info error'>";
    echo "<h2>❌ WordPress Not Found</h2>";
    echo "wp-config.php not found in current directory";
    echo "</div>";
}

// File Permissions Check
echo "<div class='info'>";
echo "<h2>File Permissions</h2>";
$check_paths = ['wp-content', 'wp-content/themes', 'wp-content/plugins', 'wp-content/uploads'];
foreach ($check_paths as $path) {
    if (file_exists($path)) {
        $perms = substr(sprintf('%o', fileperms($path)), -4);
        echo "$path: $perms<br>";
    }
}
echo "</div>";

echo "<div class='info'>";
echo "<h2>Quick Actions</h2>";
echo "<p><strong>To fix critical errors:</strong></p>";
echo "<ul>";
echo "<li>Switch to default theme: Go to Appearance > Themes > Activate Twenty Twenty-Three</li>";
echo "<li>Enable debug mode: Add WP_DEBUG=true to wp-config.php</li>";
echo "<li>Deactivate all plugins temporarily</li>";
echo "<li>Check file permissions (themes folder should be 755)</li>";
echo "</ul>";
echo "</div>";
?>
EOF

echo "✅ Debug script created: /tmp/wordpress_debug_info.php"

# Create step-by-step recovery instructions
cat > "/tmp/recovery_steps.md" << 'EOF'
# WordPress Theme Critical Error - Step-by-Step Recovery

## IMMEDIATE STEPS (Do in WordPress Admin)

### Step 1: Switch to Safe Theme (URGENT)
1. **Login to WordPress Admin**: yoursite.com/wp-admin
2. **Go to**: Appearance > Themes
3. **Click "Activate"** on any default theme:
   - Twenty Twenty-Four (recommended)
   - Twenty Twenty-Three
   - Twenty Twenty-Two
4. **Verify**: Your site should work immediately

### Step 2: Enable Debug Mode
1. **Access your site files** (FTP/cPanel)
2. **Edit wp-config.php**
3. **Add these lines** before "/* That's all, stop editing! */"
   ```php
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   define('WP_DEBUG_DISPLAY', false);
   define('WP_MEMORY_LIMIT', '256M');
   ```
4. **Save the file**

### Step 3: Upload Debug Script
1. **Upload** `/tmp/wordpress_debug_info.php` to your WordPress root directory
2. **Visit**: yoursite.com/debug-info.php?key=debug2025
3. **Review** the debug information to identify issues

### Step 4: Test Safe Theme Version
1. **Upload** the safe theme: `spherevista360-safe-theme.zip`
2. **Activate it** in WordPress admin
3. **Test** if this basic version works

## DEBUGGING SPECIFIC ISSUES

### If PHP Version Issues:
- Check if your hosting uses PHP 7.4+ 
- Ask hosting to upgrade to PHP 8.0+ if needed

### If Memory Issues:
- Increase memory limit in wp-config.php:
  `ini_set('memory_limit', '512M');`

### If Plugin Conflicts:
1. **Deactivate all plugins** temporarily
2. **Test the theme** again
3. **Reactivate plugins** one by one to find conflicts

### If File Permission Issues:
- Set themes folder to 755: `chmod 755 wp-content/themes`
- Set theme files to 644: `chmod 644 wp-content/themes/spherevista-theme/*`

## RECOVERY TIMELINE

✅ **Immediate (5 minutes)**: Switch to default theme
✅ **Quick (15 minutes)**: Enable debug mode and gather info  
✅ **Short term (30 minutes)**: Test safe theme version
✅ **Long term (1 hour)**: Debug and fix full theme

## NEXT STEPS AFTER RECOVERY

1. **Site Working?** ✅ Proceed to theme customization
2. **Still Issues?** 🔧 Check debug logs and system requirements
3. **Need Help?** 📞 Contact hosting support with debug information

Remember: Your site's functionality is priority #1. We can always fix the theme later!
EOF

echo "✅ Recovery guide created: /tmp/recovery_steps.md"

# Create a WordPress admin automation guide
cat > "/tmp/wordpress_admin_guide.txt" << 'EOF'
WORDPRESS ADMIN QUICK ACTIONS GUIDE
===================================

🚨 IMMEDIATE FIX (Do this first):
1. Login: yoursite.com/wp-admin
2. Go to: Appearance > Themes  
3. Click: "Activate" on Twenty Twenty-Three or Twenty Twenty-Four
4. Result: Site should work immediately

🔧 ENABLE DEBUGGING:
1. Edit wp-config.php (via FTP/cPanel)
2. Add before "/* That's all, stop editing! */":

define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);  
define('WP_DEBUG_DISPLAY', false);
define('WP_MEMORY_LIMIT', '256M');

🔍 GATHER DEBUG INFO:
1. Upload debug-info.php to site root
2. Visit: yoursite.com/debug-info.php?key=debug2025
3. Review PHP version, memory, errors

📦 TEST SAFE THEME:
1. Upload: spherevista360-safe-theme.zip
2. Activate in WordPress admin
3. Test basic functionality

🎯 COMMON SOLUTIONS:
- PHP Version: Upgrade to PHP 8.0+
- Memory: Increase to 256M or 512M  
- Plugins: Deactivate all temporarily
- Permissions: Set themes folder to 755

AVAILABLE THEME FILES:
✅ spherevista360-safe-theme.zip (Use this first)
🔧 spherevista360-professional-theme-fixed.zip (Full theme)
📦 spherevista360-professional-theme.zip (Original)
EOF

echo "✅ WordPress admin guide created: /tmp/wordpress_admin_guide.txt"

echo
echo "📋 RECOVERY PACKAGE READY!"
echo "=========================="
echo
echo "📁 Files created for you:"
echo "   • /tmp/wordpress_debug_info.php - Upload this to your site"
echo "   • /tmp/recovery_steps.md - Detailed recovery instructions" 
echo "   • /tmp/wordpress_admin_guide.txt - Quick action guide"
echo
echo "🎯 YOUR IMMEDIATE ACTION PLAN:"
echo "   1. Go to WordPress Admin > Appearance > Themes"
echo "   2. Activate 'Twenty Twenty-Three' or any default theme"
echo "   3. Verify your site works"
echo "   4. Then we can debug and fix the professional theme"
echo
echo "📞 After your site is working, let me know and we'll:"
echo "   • Enable debug mode"
echo "   • Test the safe theme version"  
echo "   • Fix any issues with the full theme"
echo "   • Get your professional design working perfectly"
echo

# Copy files to downloads for easy access
cp /tmp/wordpress_debug_info.php ~/downloads/
cp /tmp/recovery_steps.md ~/downloads/
cp /tmp/wordpress_admin_guide.txt ~/downloads/

echo "✅ All files also copied to ~/downloads/ for easy access"
echo
echo "🚀 Ready to recover your site! Start with switching themes in WordPress admin."