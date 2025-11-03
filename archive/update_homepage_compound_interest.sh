#!/bin/bash

# Update homepage to add Compound Interest Calculator button
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"
PAGE_ID=2412

echo "Adding Compound Interest Calculator to homepage CTA"
read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
echo ""

AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

# Get current content
echo "Fetching current homepage content..."
CURRENT_CONTENT=$(curl -s -H "$AUTH_HEADER" "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID?_fields=content" | jq -r '.content.rendered')

if [ -z "$CURRENT_CONTENT" ]; then
    echo "❌ Failed to fetch homepage content"
    exit 1
fi

echo "Updating CTA section..."

# Replace the buttons section to add Compound Interest Calculator
OLD_BUTTONS='<div class="wp-block-buttons is-content-justification-center is-layout-flex wp-container-core-buttons-is-layout-16018d1d wp-block-buttons-is-layout-flex">
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/tools/">All Tools</a></div>
<div class="wp-block-button is-style-outline is-style-outline--1"><a class="wp-block-button__link" href="/sip-calculator/">SIP Calculator</a></div>
</div>'

NEW_BUTTONS='<div class="wp-block-buttons is-content-justification-center is-layout-flex wp-container-core-buttons-is-layout-16018d1d wp-block-buttons-is-layout-flex">
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/tools/">All Tools</a></div>
<div class="wp-block-button is-style-outline is-style-outline--1"><a class="wp-block-button__link" href="/sip-calculator/">SIP Calculator</a></div>
<div class="wp-block-button is-style-outline is-style-outline--2"><a class="wp-block-button__link" href="/compound-interest-calculator/">Compound Interest</a></div>
</div>'

# Replace the buttons
NEW_CONTENT="${CURRENT_CONTENT/$OLD_BUTTONS/$NEW_BUTTONS}"

# If replacement didn't work, try a different approach
if [ "$NEW_CONTENT" = "$CURRENT_CONTENT" ]; then
    echo "Direct replacement failed, trying alternative approach..."
    # Try to replace just the SIP Calculator button line
    NEW_CONTENT=$(echo "$CURRENT_CONTENT" | sed 's|href="/sip-calculator/">SIP Calculator</a></div>|href="/sip-calculator/">SIP Calculator</a></div>\
<div class="wp-block-button is-style-outline is-style-outline--2"><a class="wp-block-button__link" href="/compound-interest-calculator/">Compound Interest</a></div>|g')
fi

# Escape for JSON
ESCAPED_CONTENT=$(echo "$NEW_CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')

JSON_PAYLOAD="{\"content\": \"$ESCAPED_CONTENT\"}"

echo "Updating homepage..."
RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d "$JSON_PAYLOAD")

if echo "$RESPONSE" | grep -q '"id":'; then
  echo "✅ Homepage updated successfully!"
  echo ""
  echo "🔄 Clear cache to see changes:"
  echo "WordPress Admin → LiteSpeed Cache → Toolbox → Purge All"
else
  echo "❌ Update failed. Response: $RESPONSE"
  exit 1
fi