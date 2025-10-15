#!/bin/bash
# WordPress Configuration Script
# Run this via SSH, cPanel Terminal, or WordPress CLI

echo "=========================================="
echo "🔧 WordPress Auto-Configuration"
echo "=========================================="
echo "Site: https://spherevista360.com"
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
echo "🌐 Visit: https://spherevista360.com"
echo ""
