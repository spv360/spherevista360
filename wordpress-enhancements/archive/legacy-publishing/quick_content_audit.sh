#!/bin/bash

# WordPress Content Audit Quick Start
# Run this script to quickly audit your 26 pages for duplicates

echo "🔍 WordPress Content Audit - Quick Start"
echo "========================================"

# Check if in correct directory
if [ ! -d "wordpress-enhancements" ]; then
    echo "❌ Error: Please run from the spherevista360 project root directory"
    echo "   cd /home/kddevops/projects/spherevista360"
    exit 1
fi

# Check for required environment variables
if [ -z "$WP_SITE" ] || [ -z "$WP_USER" ] || [ -z "$WP_APP_PASS" ]; then
    echo "⚙️  Setting up WordPress credentials..."
    echo ""
    
    read -p "🌐 Enter your WordPress site URL (e.g., https://yoursite.com): " wp_site
    read -p "👤 Enter your WordPress admin username: " wp_user
    echo "🔑 Enter your WordPress application password:"
    echo "   (Go to Users > Profile > Application Passwords to create one)"
    read -s wp_pass
    
    export WP_SITE="$wp_site"
    export WP_USER="$wp_user"
    export WP_APP_PASS="$wp_pass"
    
    echo ""
    echo "✅ Credentials set for this session"
fi

echo ""
echo "🔍 Starting content audit..."
echo "   Site: $WP_SITE"
echo "   User: $WP_USER"
echo ""

# Run the content auditor
python wordpress-enhancements/scripts/content_auditor.py

# Check if audit completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "🎯 Audit Complete!"
    echo ""
    echo "📁 Generated Files:"
    echo "   📊 Audit Report: wordpress-enhancements/configs/content_audit_report.json"
    echo "   🗑️  Removal Script: wordpress-enhancements/scripts/remove_duplicate_content.py"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Review the audit report"
    echo "   2. If satisfied, run the removal script:"
    echo "      python wordpress-enhancements/scripts/remove_duplicate_content.py"
    echo ""
    echo "💡 Need help? Check: wordpress-enhancements/docs/CONTENT_CLEANUP_GUIDE.md"
else
    echo ""
    echo "❌ Audit failed. Please check:"
    echo "   • WordPress credentials are correct"
    echo "   • Site is accessible"
    echo "   • User has admin permissions"
    echo "   • WordPress REST API is enabled"
fi