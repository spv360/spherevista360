#!/bin/bash

# WordPress Authentication Quick Fix
# Helps resolve 401 authentication errors

echo "🔧 WordPress Authentication Quick Fix"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -d "wordpress-enhancements" ]; then
    echo "❌ Error: Please run from the spherevista360 project root"
    exit 1
fi

# Run authentication diagnosis
echo "🩺 Running authentication diagnosis..."
python wordpress-enhancements/scripts/wp_auth_tester.py

# Check if diagnosis passed
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Authentication is working! You can now:"
    echo "   1. Re-run the content audit:"
    echo "      ./wordpress-enhancements/scripts/quick_content_audit.sh"
    echo ""
    echo "   2. Or run the removal script directly:"
    echo "      python wordpress-enhancements/scripts/remove_duplicate_content.py"
else
    echo ""
    echo "🔧 Need to fix authentication first. Common solutions:"
    echo ""
    echo "1. CREATE APPLICATION PASSWORD:"
    echo "   • Login to WordPress admin"
    echo "   • Go to Users > Your Profile"
    echo "   • Scroll to 'Application Passwords'"
    echo "   • Create new password named 'Content Audit'"
    echo "   • Copy the generated password"
    echo ""
    echo "2. SET ENVIRONMENT VARIABLES:"
    echo "   export WP_SITE='https://your-site.com'"
    echo "   export WP_USER='your_wordpress_username'"
    echo "   export WP_APP_PASS='xxxx xxxx xxxx xxxx'"
    echo ""
    echo "3. VERIFY CREDENTIALS:"
    echo "   • Use WordPress USERNAME (not email)"
    echo "   • Use APPLICATION password (not login password)"
    echo "   • Include https:// in site URL"
    echo "   • Remove trailing slash from URL"
    echo ""
    echo "4. TEST MANUALLY:"
    read -p "Enter your WordPress site URL: " wp_site
    read -p "Enter your WordPress username: " wp_user
    echo "Test command:"
    echo "curl -u '$wp_user:YOUR_APP_PASSWORD' '$wp_site/wp-json/wp/v2/users/me'"
    echo ""
    echo "💡 Run this script again after fixing credentials"
fi