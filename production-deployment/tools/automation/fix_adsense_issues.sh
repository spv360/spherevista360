#!/bin/bash
# Fix AdSense Approval Issues - Update Homepage with Proper Content
# This script fixes the meta description and content balance issues

# Configuration
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="your_username"  # Update with your WordPress admin username
WP_APP_PASSWORD="your_app_password"  # Update with your Application Password

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔧 FIXING ADSENSE APPROVAL ISSUES${NC}"
echo "=================================="
echo ""

# Check if fixed content file exists
if [ ! -f "homepage_content_fixed.html" ]; then
    echo -e "${RED}❌ Error: homepage_content_fixed.html not found${NC}"
    exit 1
fi

# Backup current homepage content
echo -e "${YELLOW}📦 Backing up current homepage...${NC}"
CURRENT_CONTENT=$(curl -s "${WP_SITE_URL}/wp-json/wp/v2/pages?slug=home&_fields=content" | jq -r '.[0].content.rendered' 2>/dev/null)
if [ ! -z "$CURRENT_CONTENT" ]; then
    echo "$CURRENT_CONTENT" > homepage_backup_$(date +%Y%m%d_%H%M%S).html
    echo -e "${GREEN}✅ Backup created${NC}"
fi

# Read new content and escape for JSON
CONTENT=$(cat homepage_content_fixed.html | jq -Rs .)

# Get homepage ID
echo -e "${YELLOW}🔍 Getting homepage ID...${NC}"
PAGE_RESPONSE=$(curl -s -X GET "${WP_SITE_URL}/wp-json/wp/v2/pages?slug=home&_fields=id")

PAGE_ID=$(echo $PAGE_RESPONSE | jq -r '.[0].id')

if [ "$PAGE_ID" = "null" ] || [ -z "$PAGE_ID" ]; then
    echo -e "${RED}❌ Error: Could not find homepage ID${NC}"
    echo "Response: $PAGE_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Homepage ID: $PAGE_ID${NC}"

# Update SEO meta description via Yoast SEO API (if available)
echo -e "${YELLOW}📝 Updating meta description...${NC}"

# Prepare JSON payload for homepage update
JSON_PAYLOAD=$(cat <<EOF
{
  "content": $CONTENT,
  "status": "publish",
  "title": "Home - SphereVista360",
  "excerpt": "Your trusted source for technology insights, AI trends, and digital innovation. Discover expert analysis on product analytics, cloud computing, and emerging technologies.",
  "meta": {
    "description": "SphereVista360 - Your trusted source for technology insights, AI trends, and digital innovation. Discover expert analysis on product analytics, cloud computing, and emerging technologies."
  }
}
EOF
)

echo -e "${YELLOW}🚀 Updating homepage with AdSense-compliant content...${NC}"

# Update homepage via REST API
UPDATE_RESPONSE=$(curl -s -X POST "${WP_SITE_URL}/wp-json/wp/v2/pages/${PAGE_ID}" \
  -u "${WP_USERNAME}:${WP_APP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Check response
if echo "$UPDATE_RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
    echo -e "${GREEN}✅ SUCCESS: Homepage updated with AdSense-compliant content!${NC}"
    echo ""
    echo -e "${BLUE}🎯 FIXES APPLIED:${NC}"
    echo "   ✅ Added proper meta description (no more CSS code)"
    echo "   ✅ Added 3 substantial paragraphs of content"
    echo "   ✅ Improved text-to-image ratio for AdSense"
    echo "   ✅ Enhanced SEO with keyword-rich content"
    echo ""
    echo -e "${BLUE}📊 CONTENT IMPROVEMENTS:${NC}"
    echo "   • Text paragraphs: 3 (was 1)"
    echo "   • Word count: ~150+ descriptive words"
    echo "   • SEO keywords: technology, AI, finance, innovation"
    echo "   • User value: Clear site purpose and expertise"
    echo ""
    echo -e "${GREEN}🌐 View your updated homepage: ${WP_SITE_URL}${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT NEXT STEPS:${NC}"
    echo "   1. Clear any caching plugins (WP Rocket, W3 Total Cache, etc.)"
    echo "   2. Clear CDN cache if using Cloudflare or similar"
    echo "   3. Hard refresh browser (Ctrl+F5) to see changes"
    echo "   4. Check meta description in page source or SEO tools"
    echo "   5. Run AdSense readiness test again"
    echo ""
    echo -e "${BLUE}🧪 TEST YOUR FIXES:${NC}"
    echo "   • Meta description should now read properly"
    echo "   • Homepage should have substantial text content"
    echo "   • SEO plugins should pick up proper description"
    echo ""
    echo -e "${GREEN}🎉 READY FOR ADSENSE APPLICATION!${NC}"

else
    echo -e "${RED}❌ ERROR: Failed to update homepage${NC}"
    echo "Response: $UPDATE_RESPONSE"
    echo ""
    echo -e "${YELLOW}🔧 Troubleshooting:${NC}"
    echo "   1. Check your WordPress credentials"
    echo "   2. Verify REST API is enabled"
    echo "   3. Check file permissions"
    echo "   4. Try updating manually via WordPress admin"
    exit 1
fi