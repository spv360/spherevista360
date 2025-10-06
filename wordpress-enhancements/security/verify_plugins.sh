#!/bin/bash
# WordPress Plugin Verification Script
# Checks if essential plugins are installed and active

echo "🔍 WordPress Plugin Verification for SphereVista360"
echo "================================================="

# Check if we can access WordPress directory
if [ ! -f "wp-config.php" ]; then
    echo "❌ WordPress installation not found in current directory"
    echo "📍 Please run this script from your WordPress root directory"
    exit 1
fi

echo "✅ WordPress installation found"
echo ""

# List of essential plugins to check
declare -a plugins=(
    "wordfence/wordfence.php"
    "updraftplus/updraftplus.php"
    "wordpress-seo/wp-seo.php"
    "wp-smushit/wp-smush.php"
    "contact-form-7/wp-contact-form-7.php"
    "google-analytics-for-wordpress/googleanalytics.php"
)

declare -a plugin_names=(
    "Wordfence Security"
    "UpdraftPlus"
    "Yoast SEO"
    "Smush"
    "Contact Form 7"
    "MonsterInsights"
)

echo "🔌 Checking essential plugins:"
echo "-----------------------------"

for i in "${!plugins[@]}"; do
    plugin_path="wp-content/plugins/${plugins[$i]}"
    plugin_name="${plugin_names[$i]}"
    
    if [ -f "$plugin_path" ]; then
        echo "  ✅ $plugin_name - Installed"
    else
        echo "  ❌ $plugin_name - Not found"
    fi
done

echo ""
echo "📋 Next Steps:"
echo "1. Install any missing plugins via WordPress Admin"
echo "2. Activate all installed plugins"
echo "3. Configure each plugin according to setup guide"
echo "4. Run security scan with Wordfence"
echo "5. Create backup with UpdraftPlus"

echo ""
echo "🌐 WordPress Admin: https://spherevista360.com/wp-admin/"
echo "📖 Setup Guide: See manual installation guide"
