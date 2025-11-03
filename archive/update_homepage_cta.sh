#!/bin/bash

# Update homepage (ID 1686) to add direct Tools / SIP Calculator CTA
set -e

WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"
WP_PASSWORD=""
PAGE_ID=1686

echo "Updating homepage (ID: $PAGE_ID) to add Tools CTA"
read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
echo ""

AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

# CTA HTML to prepend to the homepage
CTA_HTML='<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"24px","bottom":"24px"}},"color":{"background":"#f4f8ff"}},"className":"homepage-tools-cta"} -->
<div class="wp-block-group alignfull homepage-tools-cta" style="background:#f4f8ff;padding-top:24px;padding-bottom:24px"><div class="wp-block-group__inner-container"><!-- wp:columns -->
<div class="wp-block-columns"><div class="wp-block-column" style="flex-basis:66.66%"><!-- wp:heading {"level":3} -->
<h3>Explore our free financial tools</h3>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Quickly access our calculators and planning tools to estimate investments, loans, and retirement needs.</p>
<!-- /wp:paragraph --></div><div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","className":"is-style-fill"} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/tools/">Open Tools Hub</a></div>
<!-- /wp:button --><!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link" href="/sip-calculator/">Try SIP Calculator</a></div>
<!-- /wp:button --></div></div></div><!-- /wp:columns --></div></div>
<!-- /wp:group -->'

# Retrieve existing content
EXISTING_CONTENT_RAW=$(curl -s -H "$AUTH_HEADER" "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID?_fields=content")
EXISTING_CONTENT=$(echo "$EXISTING_CONTENT_RAW" | jq -r '.content.rendered')

# Prepend CTA to the existing content
UPDATED_CONTENT="$CTA_HTML\n$EXISTING_CONTENT"

# Escape quotes and newlines for JSON payload
ESCAPED_CONTENT=$(echo "$UPDATED_CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')
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
  echo "Homepage updated successfully."
else
  echo "Failed to update homepage. Response: $RESPONSE"
  exit 1
fi
