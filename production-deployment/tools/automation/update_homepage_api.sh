#!/bin/bash
# WordPress REST API Homepage Update Script
# Updates homepage content using the complete_homepage_fix.html content

# Configuration - Update these with your details
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="your_username"  # Your WordPress admin username
WP_APP_PASSWORD="your_app_password"  # Generate from WP Admin → Users → Your Profile → Application Passwords

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}WordPress Homepage Update via REST API${NC}"
echo "======================================"

# Check if content file exists
if [ ! -f "homepage_content.html" ]; then
    echo -e "${RED}❌ Error: homepage_content.html not found${NC}"
    echo "Run: grep -A 479 '<!-- wp:html -->' complete_homepage_fix.html | sed '1d' > homepage_content.html"
    exit 1
fi

# Read content and escape for JSON
CONTENT=$(cat homepage_content.html | jq -Rs .)

# Get homepage ID
echo -e "${YELLOW}Getting homepage ID...${NC}"
PAGE_RESPONSE=$(curl -s -X GET "${WP_SITE_URL}/wp-json/wp/v2/pages?slug=home&_fields=id" \
  -u "${WP_USERNAME}:${WP_APP_PASSWORD}")

PAGE_ID=$(echo $PAGE_RESPONSE | jq -r '.[0].id')

if [ "$PAGE_ID" = "null" ] || [ -z "$PAGE_ID" ]; then
    echo -e "${RED}❌ Error: Could not find homepage ID${NC}"
    echo "Response: $PAGE_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Homepage ID: $PAGE_ID${NC}"

# Prepare JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "content": $CONTENT,
  "status": "publish"
}
EOF
)

echo -e "${YELLOW}Updating homepage content...${NC}"

# Update homepage via REST API
UPDATE_RESPONSE=$(curl -s -X POST "${WP_SITE_URL}/wp-json/wp/v2/pages/${PAGE_ID}" \
  -u "${WP_USERNAME}:${WP_APP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Check response
if echo "$UPDATE_RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
    echo -e "${GREEN}✅ SUCCESS: Homepage updated successfully!${NC}"
    echo -e "${BLUE}View your updated homepage: ${WP_SITE_URL}${NC}"

    # Optional: Clear any caching
    echo -e "${YELLOW}Note: You may need to clear any caching plugins or CDN cache${NC}"
else
    echo -e "${RED}❌ ERROR: Failed to update homepage${NC}"
    echo "Response: $UPDATE_RESPONSE"
    exit 1
fi

echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Visit your homepage to verify the changes"
echo "2. Clear any caching (WP plugins, browser, CDN)"
echo "3. Test all links and functionality"
echo "4. Check mobile responsiveness"