#!/bin/bash

# WordPress API Tools Setup Script - Simplified Version
# Automatically creates Tools pages and navigation using WordPress REST API

set -e

echo "🔧 Setting up Tools Navigation via WordPress API (Simplified)"
echo "==========================================================="

# Configuration
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"
WP_PASSWORD=""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get WordPress password
get_credentials() {
    if [ -z "$WP_PASSWORD" ]; then
        read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
        echo ""
    fi
}

# Test API connection with basic auth
test_api_connection() {
    print_info "Testing WordPress API connection..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    RESPONSE=$(curl -s -H "$AUTH_HEADER" "$WP_SITE_URL/wp-json/wp/v2/users/me")

    if echo "$RESPONSE" | grep -q '"id":'; then
        print_success "API connection successful"
    else
        print_error "API connection failed"
        echo "Response: $RESPONSE"
        exit 1
    fi
}

# Create Tools page
create_tools_page() {
    print_info "Creating Tools page..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    # Simple HTML content
    CONTENT='<!-- wp:heading {"level":3} -->
<h3>Financial Tools & Calculators</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Explore our collection of free financial tools designed to help you make informed investment decisions and plan for your financial future.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4>🚀 Featured Tool: SIP Calculator</h4>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li><strong><a href="/sip-calculator/">SIP Calculator</a></strong> - Calculate returns from Systematic Investment Plans in US stocks</li><li><strong><a href="/investment-calculator/">Investment Calculator</a></strong> - Basic investment return calculator (Coming Soon)</li><li><strong><a href="/retirement-calculator/">Retirement Calculator</a></strong> - Plan your retirement savings (Coming Soon)</li><li><strong><a href="/loan-calculator/">Loan Calculator</a></strong> - Calculate loan payments and interest (Coming Soon)</li></ul>
<!-- /wp:list -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","className":"is-style-fill"} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/sip-calculator/">Try SIP Calculator Now</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'

    # Create JSON payload
    JSON_PAYLOAD=$(cat << EOF
{
  "title": "Tools",
  "content": "$(echo "$CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')",
  "status": "publish",
  "type": "page",
  "slug": "tools"
}
EOF
)

    RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
        -H "Content-Type: application/json" \
        -H "$AUTH_HEADER" \
        -d "$JSON_PAYLOAD")

    TOOLS_PAGE_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 | tr -d ',')

    if [ -n "$TOOLS_PAGE_ID" ] && [ "$TOOLS_PAGE_ID" != "null" ]; then
        print_success "Tools page created (ID: $TOOLS_PAGE_ID)"
        echo "$TOOLS_PAGE_ID" > .tools_page_id
    else
        print_error "Failed to create Tools page"
        echo "Response: $RESPONSE"
        return 1
    fi
}

# Create SIP Calculator page
create_sip_calculator_page() {
    print_info "Creating SIP Calculator page..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    CONTENT='<!-- wp:paragraph -->
<p>Welcome to our US Stock Market SIP Calculator. Use this free tool to estimate returns from systematic monthly investments in stocks.</p>
<!-- /wp:paragraph -->

<!-- wp:shortcode -->
[sip_calculator]
<!-- /wp:shortcode -->

<!-- wp:paragraph -->
<p><em>Disclaimer: This calculator provides estimates based on historical market performance and should not be considered as financial advice. Past performance does not guarantee future results.</em></p>
<!-- /wp:paragraph -->'

    JSON_PAYLOAD=$(cat << EOF
{
  "title": "SIP Calculator",
  "content": "$(echo "$CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')",
  "status": "publish",
  "type": "page",
  "slug": "sip-calculator"
}
EOF
)

    RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
        -H "Content-Type: application/json" \
        -H "$AUTH_HEADER" \
        -d "$JSON_PAYLOAD")

    SIP_PAGE_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 | tr -d ',')

    if [ -n "$SIP_PAGE_ID" ] && [ "$SIP_PAGE_ID" != "null" ]; then
        print_success "SIP Calculator page created (ID: $SIP_PAGE_ID)"
        echo "$SIP_PAGE_ID" > .sip_page_id
    else
        print_error "Failed to create SIP Calculator page"
        echo "Response: $RESPONSE"
        return 1
    fi
}

# Create placeholder tools pages
create_placeholder_pages() {
    print_info "Creating placeholder tools pages..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    # Investment Calculator
    INVEST_CONTENT='<!-- wp:heading -->
<h2>Investment Calculator</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Our Investment Calculator is coming soon! This tool will help you calculate returns on lump-sum investments with different compounding frequencies.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="/tools/">← Back to Tools</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'

    # Retirement Calculator
    RETIRE_CONTENT='<!-- wp:heading -->
<h2>Retirement Calculator</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Plan your retirement with our comprehensive Retirement Calculator. Estimate how much you need to save for a comfortable retirement.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Coming Soon!</strong> This advanced calculator will include inflation adjustments, life expectancy factors, and retirement income projections.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="/tools/">← Back to Tools</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'

    # Create pages
    declare -a PAGES=(
        "investment-calculator:$INVEST_CONTENT:Investment Calculator"
        "retirement-calculator:$RETIRE_CONTENT:Retirement Calculator"
    )

    for PAGE_DATA in "${PAGES[@]}"; do
        IFS=':' read -r SLUG CONTENT TITLE <<< "$PAGE_DATA"

        JSON_PAYLOAD=$(cat << EOF
{
  "title": "$TITLE",
  "content": "$(echo "$CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')",
  "status": "publish",
  "type": "page",
  "slug": "$SLUG"
}
EOF
)

        RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
            -H "Content-Type: application/json" \
            -H "$AUTH_HEADER" \
            -d "$JSON_PAYLOAD")

        PAGE_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 | tr -d ',')

        if [ -n "$PAGE_ID" ] && [ "$PAGE_ID" != "null" ]; then
            print_success "$TITLE page created (ID: $PAGE_ID)"
        else
            print_warning "Failed to create $TITLE page"
        fi
    done
}

# Update navigation menu
update_menu() {
    print_info "Updating navigation menu..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    # Get menus
    MENU_RESPONSE=$(curl -s "$WP_SITE_URL/wp-json/wp/v2/menus" \
        -H "$AUTH_HEADER")

    # Try to find primary menu
    MENU_ID=$(echo "$MENU_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2 | tr -d ',')

    if [ -n "$MENU_ID" ] && [ "$MENU_ID" != "null" ]; then
        print_info "Found menu ID: $MENU_ID"

        # Read page IDs
        if [ -f .tools_page_id ]; then
            TOOLS_ID=$(cat .tools_page_id)
        fi
        if [ -f .sip_page_id ]; then
            SIP_ID=$(cat .sip_page_id)
        fi

        if [ -n "$TOOLS_ID" ]; then
            # Add Tools menu item
            MENU_DATA=$(cat << EOF
{
  "title": "Tools",
  "url": "/tools/",
  "status": "publish",
  "type": "post_type",
  "object": "page",
  "object_id": $TOOLS_ID,
  "menu_id": $MENU_ID
}
EOF
)

            curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/menu-items" \
                -H "Content-Type: application/json" \
                -H "$AUTH_HEADER" \
                -d "$MENU_DATA" > /dev/null

            print_success "Added Tools to navigation menu"
        fi

        if [ -n "$SIP_ID" ] && [ -n "$TOOLS_ID" ]; then
            # Add SIP Calculator submenu
            SUBMENU_DATA=$(cat << EOF
{
  "title": "SIP Calculator",
  "url": "/sip-calculator/",
  "status": "publish",
  "type": "post_type",
  "object": "page",
  "object_id": $SIP_ID,
  "menu_id": $MENU_ID,
  "parent": $TOOLS_ID
}
EOF
)

            curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/menu-items" \
                -H "Content-Type: application/json" \
                -H "$AUTH_HEADER" \
                -d "$SUBMENU_DATA" > /dev/null

            print_success "Added SIP Calculator as submenu"
        fi
    else
        print_warning "Could not find menu to update automatically"
        print_info "You can manually add the pages to your menu:"
        echo "  - Go to Appearance → Menus"
        echo "  - Add 'Tools' and 'SIP Calculator' pages"
        echo "  - Set Tools as parent menu item"
    fi
}

# Clean up
cleanup() {
    rm -f .tools_page_id .sip_page_id
}

# Main execution
main() {
    echo ""
    get_credentials
    test_api_connection

    if create_tools_page && create_sip_calculator_page; then
        create_placeholder_pages
        update_menu
        cleanup

        echo ""
        print_success "🎉 Tools setup completed successfully!"
        echo ""
        echo "Created pages:"
        echo "✓ /tools/ - Tools overview page"
        echo "✓ /sip-calculator/ - SIP Calculator with working plugin"
        echo "✓ /investment-calculator/ - Coming soon page"
        echo "✓ /retirement-calculator/ - Coming soon page"
        echo ""
        echo "Navigation structure:"
        echo "Tools"
        echo "  └─ SIP Calculator"
        echo ""
        echo "Next steps:"
        echo "1. Visit your site and check the Tools menu"
        echo "2. Test the SIP Calculator functionality"
        echo "3. Update placeholder pages as you add more tools"
    else
        print_error "Failed to create required pages. Please check your WordPress setup."
        cleanup
        exit 1
    fi
}

main