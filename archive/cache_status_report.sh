#!/bin/bash

echo "=== HOMEPAGE CACHE STATUS REPORT ==="
echo ""

WP_SITE_URL="https://spherevista360.com"
PAGE_ID=1686

echo "🔍 CHECKING WORDPRESS DATABASE CONTENT:"
API_CONTENT=$(curl -s "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID?_fields=content" | jq -r '.content.rendered')

if echo "$API_CONTENT" | grep -q "homepage-tools-cta"; then
    echo "✅ Tools CTA section: FOUND in database"
else
    echo "❌ Tools CTA section: NOT FOUND in database"
fi

if echo "$API_CONTENT" | grep -q "Market Intelligence"; then
    echo "✅ Finance content: FOUND in database"
else
    echo "❌ Finance content: NOT FOUND in database"
fi

if echo "$API_CONTENT" | grep -q "category-carousel"; then
    echo "❌ Old carousel: STILL PRESENT in database"
else
    echo "✅ Old carousel: REMOVED from database"
fi

echo ""
echo "🌐 CHECKING LIVE HOMEPAGE:"
LIVE_CONTENT=$(curl -s "$WP_SITE_URL/")

if echo "$LIVE_CONTENT" | grep -q "homepage-tools-cta"; then
    echo "✅ Tools CTA: VISIBLE on live site"
else
    echo "❌ Tools CTA: NOT VISIBLE (cached)"
fi

if echo "$LIVE_CONTENT" | grep -q "Market Intelligence"; then
    echo "✅ Finance content: VISIBLE on live site"
else
    echo "❌ Finance content: NOT VISIBLE (cached)"
fi

if echo "$LIVE_CONTENT" | grep -q "category-carousel"; then
    echo "❌ Old carousel: STILL VISIBLE on live site"
else
    echo "✅ Old carousel: REMOVED from live site"
fi

echo ""
echo "📊 SUMMARY:"
if echo "$API_CONTENT" | grep -q "homepage-tools-cta" && echo "$LIVE_CONTENT" | grep -q "category-carousel"; then
    echo "❌ CACHE ISSUE: Content updated in database but live site shows old cached version"
    echo ""
    echo "🔧 SOLUTION: Manual cache clearing required"
    echo ""
    echo "1. Login to WordPress Admin: https://spherevista360.com/wp-admin/"
    echo "2. Go to LiteSpeed Cache → Toolbox → Purge All"
    echo "3. Or WP-Optimize → Cache → Clear Cache"
    echo "4. Visit homepage to verify changes"
else
    echo "✅ Everything looks good!"
fi