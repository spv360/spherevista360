#!/bin/bash
# Interactive WordPress Homepage Update Script
# Securely prompts for credentials and updates homepage via REST API

# Configuration
WP_SITE_URL="https://spherevista360.com"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔐 WordPress Homepage Update via REST API${NC}"
echo "=========================================="
echo ""

# Check if content file exists
if [ ! -f "homepage_content.html" ]; then
    echo -e "${RED}❌ Error: homepage_content.html not found${NC}"
    echo "Run: grep -A 479 '<!-- wp:html -->' complete_homepage_fix.html | sed '1d' > homepage_content.html"
    exit 1
fi

echo -e "${YELLOW}Please provide your WordPress credentials:${NC}"
echo ""

# Securely prompt for username
read -p "WordPress Admin Username: " WP_USERNAME

# Securely prompt for application password (hidden input)
echo -n "WordPress Application Password: "
stty -echo
read WP_APP_PASSWORD
stty echo
echo ""  # New line after password input

echo ""
echo -e "${YELLOW}Authenticating and getting homepage ID...${NC}"

# Test authentication and get homepage ID
PAGE_RESPONSE=$(curl -s -X GET "${WP_SITE_URL}/wp-json/wp/v2/pages?slug=home&_fields=id" \
  -u "${WP_USERNAME}:${WP_APP_PASSWORD}")

# Check if authentication worked
if echo "$PAGE_RESPONSE" | grep -q "rest_forbidden\|rest_not_logged_in\|incorrect_password"; then
    echo -e "${RED}❌ Authentication failed!${NC}"
    echo "Please check your username and application password."
    exit 1
fi

PAGE_ID=$(echo $PAGE_RESPONSE | jq -r '.[0].id' 2>/dev/null)

if [ "$PAGE_ID" = "null" ] || [ -z "$PAGE_ID" ] || [ "$PAGE_ID" = "" ]; then
    echo -e "${RED}❌ Error: Could not find homepage ID${NC}"
    echo "Response: $PAGE_RESPONSE"
    echo ""
    echo "Possible issues:"
    echo "- Username may be incorrect"
    echo "- Application password may be expired"
    echo "- Homepage slug may not be 'home'"
    exit 1
fi

echo -e "${GREEN}✅ Authentication successful!${NC}"
echo -e "${GREEN}✅ Homepage ID: $PAGE_ID${NC}"
echo ""

# Read content and prepare for JSON
echo -e "${YELLOW}Preparing content for update...${NC}"
CONTENT=$(cat homepage_content.html | jq -Rs .)

# Prepare JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "content": $CONTENT,
  "status": "publish"
}
EOF
)

echo -e "${YELLOW}Updating homepage content...${NC}"
echo "This may take a few seconds..."

# Update homepage via REST API
UPDATE_RESPONSE=$(curl -s -X POST "${WP_SITE_URL}/wp-json/wp/v2/pages/${PAGE_ID}" \
  -u "${WP_USERNAME}:${WP_APP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Check response
if echo "$UPDATE_RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
    UPDATED_ID=$(echo $UPDATE_RESPONSE | jq -r '.id')
    UPDATED_SLUG=$(echo $UPDATE_RESPONSE | jq -r '.slug')

    echo ""
    echo -e "${GREEN}🎉 SUCCESS! Homepage updated successfully!${NC}"
    echo ""
    echo -e "${BLUE}📍 View your updated homepage:${NC}"
    echo -e "${BLUE}   https://spherevista360.com/${NC}"
    echo ""
    echo -e "${YELLOW}📋 What was updated:${NC}"
    echo "  ✅ Category carousel with animations"
    echo "  ✅ Professional header section"
    echo "  ✅ Latest posts grid layout"
    echo "  ✅ Interactive sidebar widgets"
    echo "  ✅ Bottom categories section"
    echo "  ✅ All responsive CSS styling"
    echo "  ✅ JavaScript functionality"
    echo ""

    # Optional: Clear any caching
    echo -e "${YELLOW}💡 Note: You may need to clear any caching plugins or CDN cache${NC}"
    echo ""

    echo -e "${BLUE}🔍 Next Steps:${NC}"
    echo "1. Visit your homepage to verify the changes"
    echo "2. Test the category carousel (should scroll automatically)"
    echo "3. Check mobile responsiveness"
    echo "4. Clear browser cache if content looks unchanged"
    echo "5. Test all links and functionality"

else
    echo ""
    echo -e "${RED}❌ ERROR: Failed to update homepage${NC}"
    echo "Response: $UPDATE_RESPONSE"
    echo ""
    echo "Possible solutions:"
    echo "1. Check if your application password is still valid"
    echo "2. Verify you have administrator privileges"
    echo "3. Try again in a few minutes"
    echo "4. Check WordPress error logs"
    exit 1
fi