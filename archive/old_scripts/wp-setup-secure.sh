#!/bin/bash
# Secure WordPress setup script - No hardcoded credentials

echo "🔐 WordPress Setup - Secure Credential Input"
echo "============================================"

# Check if environment variables are already set
if [ -n "$WP_SITE" ] && [ -n "$WP_USER" ] && [ -n "$WP_APP_PASS" ]; then
    echo "✅ WordPress credentials loaded from environment"
    echo "🌐 Site: $WP_SITE"
    echo "👤 User: $WP_USER"
    echo "🔑 Password: [HIDDEN]"
else
    # Interactive credential input
    echo "Please provide WordPress credentials:"
    
    # Get site URL
    read -p "WordPress Site URL [https://spherevista360.com]: " wp_site
    export WP_SITE=${wp_site:-https://spherevista360.com}
    
    # Get username
    read -p "WordPress Username: " WP_USER
    export WP_USER
    
    # Get password (hidden input)
    echo -n "WordPress App Password: "
    read -s WP_APP_PASS
    export WP_APP_PASS
    echo
    
    echo ""
    echo "✅ Credentials configured"
fi

# Verify all required variables are set
if [ -z "$WP_SITE" ] || [ -z "$WP_USER" ] || [ -z "$WP_APP_PASS" ]; then
    echo "❌ Error: Missing required credentials"
    exit 1
fi

# Run the WordPress agent
echo "🚀 Starting WordPress operations..."
python wp_agent_bulk.py "${1:-/absolute/path/to/posts_to_upload}"
