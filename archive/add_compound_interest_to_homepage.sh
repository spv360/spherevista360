#!/bin/bash

# Add Compound Interest Calculator to homepage CTA section
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"
PAGE_ID=2412  # Homepage ID

echo "Adding Compound Interest Calculator to homepage CTA section"
read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
echo ""

AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

# Get current content
CURRENT_CONTENT=$(curl -s -H "$AUTH_HEADER" "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID?_fields=content" | jq -r '.content.rendered')

# Replace the CTA section to include Compound Interest Calculator
UPDATED_CTA='<div class="wp-block-group alignfull homepage-tools-cta" style="background:#f4f8ff;padding-top:24px;padding-bottom:24px"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow">
<h3 class="wp-block-heading has-text-align-center">Explore our free financial tools</h3>

<div class="wp-block-buttons is-content-justification-center is-layout-flex wp-container-core-buttons-is-layout-16018d1d wp-block-buttons-is-layout-flex">
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/tools/">All Tools</a></div>
<div class="wp-block-button is-style-outline is-style-outline--1"><a class="wp-block-button__link" href="/sip-calculator/">SIP Calculator</a></div>
<div class="wp-block-button is-style-outline is-style-outline--2"><a class="wp-block-button__link" href="/compound-interest-calculator/">Compound Interest</a></div>
</div>
</div></div>'

# Replace the CTA section in the content
NEW_CONTENT=$(echo "$CURRENT_CONTENT" | sed "s|<div class=\"wp-block-group alignfull homepage-tools-cta\" style=\"background:#f4f8ff;padding-top:24px;padding-bottom:24px\"><div class=\"wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow\">.*</div></div></div>|$UPDATED_CTA|")

# Escape for JSON
ESCAPED_CONTENT=$(echo "$NEW_CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')

JSON_PAYLOAD=$(cat << EOF
{
  "content": "$ESCAPED_CONTENT"
}
EOF
)

RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d "$JSON_PAYLOAD")

if echo "$RESPONSE" | grep -q '"id":'; then
  echo "✅ Homepage updated with Compound Interest Calculator CTA!"
  echo ""
  echo "🔄 Now clear cache to see the changes:"
  echo "1. WordPress Admin → LiteSpeed Cache → Toolbox → Purge All"
  echo "2. Visit https://spherevista360.com/ to see the new button"
else
  echo "❌ Failed to update homepage. Response: $RESPONSE"
  exit 1
fi