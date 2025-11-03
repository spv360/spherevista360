#!/bin/bash

# Force homepage cache refresh and verify content
WP_SITE_URL="https://spherevista360.com"
PAGE_ID=1686

echo "=== FORCE HOMEPAGE CACHE REFRESH ==="
echo ""

echo "1. Checking WordPress API content..."
API_CONTENT=$(curl -s "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID?_fields=content" | jq -r '.content.rendered')

if echo "$API_CONTENT" | grep -q "homepage-tools-cta"; then
    echo "✅ CTA section found in WordPress database"
else
    echo "❌ CTA section NOT found in WordPress database"
fi

if echo "$API_CONTENT" | grep -q "Market Intelligence"; then
    echo "✅ Finance content found in WordPress database"
else
    echo "❌ Finance content NOT found in WordPress database"
fi

echo ""
echo "2. Checking live homepage..."
LIVE_CONTENT=$(curl -s "$WP_SITE_URL/")

if echo "$LIVE_CONTENT" | grep -q "homepage-tools-cta"; then
    echo "✅ CTA visible on live site"
else
    echo "❌ CTA NOT visible on live site (cached)"
fi

if echo "$LIVE_CONTENT" | grep -q "Market Intelligence"; then
    echo "✅ Finance content visible on live site"
else
    echo "❌ Finance content NOT visible on live site (cached)"
fi

echo ""
echo "3. SIP Calculator Status:"
SIP_STATUS=$(curl -s -I "$WP_SITE_URL/sip-calculator/" | head -1)
if echo "$SIP_STATUS" | grep -q "200"; then
    echo "✅ SIP Calculator accessible at: $WP_SITE_URL/sip-calculator/"
else
    echo "❌ SIP Calculator not accessible"
fi

TOOLS_STATUS=$(curl -s -I "$WP_SITE_URL/tools/" | head -1)
if echo "$TOOLS_STATUS" | grep -q "200"; then
    echo "✅ Tools page accessible at: $WP_SITE_URL/tools/"
else
    echo "❌ Tools page not accessible"
fi

echo ""
echo "=== MANUAL CACHE CLEARING REQUIRED ==="
echo "Since automated cache clearing failed, please manually clear cache:"
echo ""
echo "1. Login to WordPress Admin: https://spherevista360.com/wp-admin/"
echo "2. Go to LiteSpeed Cache → Toolbox → Purge All"
echo "3. Alternative: WP-Optimize → Cache → Clear Cache"
echo "4. Visit homepage: https://spherevista360.com/"
echo ""
echo "After clearing cache, you should see:"
echo "- Tools CTA buttons at the top"
echo "- Finance-focused content sections"
echo "- No carousel/category cards"