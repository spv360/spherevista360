#!/bin/bash

# Clear WordPress cache by triggering admin actions
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"
WP_PASSWORD=""

echo "Clearing WordPress cache..."
read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
echo ""

AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

# Try to clear LiteSpeed cache via admin-ajax
echo "Attempting to clear LiteSpeed cache..."
curl -s -X POST "$WP_SITE_URL/wp-admin/admin-ajax.php" \
  -H "$AUTH_HEADER" \
  -d "action=litespeed_purge_all" > /dev/null

# Try to clear other common caches
echo "Attempting to clear other caches..."
curl -s -X POST "$WP_SITE_URL/wp-admin/admin-ajax.php" \
  -H "$AUTH_HEADER" \
  -d "action=wp_optimize_clear_cache" > /dev/null

# Force refresh the homepage
echo "Forcing homepage refresh..."
curl -s "$WP_SITE_URL/?nocache=1" > /dev/null

echo "Cache clearing attempts completed."
echo ""
echo "Manual steps if needed:"
echo "1. Login to WordPress admin: $WP_SITE_URL/wp-admin/"
echo "2. Go to LiteSpeed Cache → Toolbox → Purge All"
echo "3. Or go to WP-Optimize → Cache → Clear Cache"
echo "4. Visit homepage: $WP_SITE_URL/"
echo ""
echo "The CTA should now be visible at the top of the homepage!"