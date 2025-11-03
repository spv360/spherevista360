#!/bin/bash

# WordPress API Tools Setup Script
# Automatically creates Tools pages and navigation using WordPress REST API

set -e

echo "🔧 Setting up Tools Navigation via WordPress API"
echo "==============================================="

# Configuration - Update these with your actual WordPress details
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"  # Your WordPress admin username
WP_PASSWORD=""    # Will be prompted securely

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

# Get WordPress password securely
get_credentials() {
    if [ -z "$WP_PASSWORD" ]; then
        read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
        echo ""
    fi
}

# Get WordPress API authentication token
get_api_token() {
    print_info "Authenticating with WordPress..."

    # Get JWT token or use basic auth
    TOKEN_RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/jwt-auth/v1/token" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$WP_USERNAME\",\"password\":\"$WP_PASSWORD\"}")

    JWT_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)

    if [ -z "$JWT_TOKEN" ]; then
        print_warning "JWT authentication failed, trying basic auth..."
        # Fall back to basic auth
        AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"
        USE_BASIC_AUTH=true
    else
        AUTH_HEADER="Authorization: Bearer $JWT_TOKEN"
        USE_BASIC_AUTH=false
        print_success "JWT authentication successful"
    fi
}

# Test API connection
test_api_connection() {
    print_info "Testing WordPress API connection..."

    if [ "$USE_BASIC_AUTH" = true ]; then
        RESPONSE=$(curl -s -H "$AUTH_HEADER" "$WP_SITE_URL/wp-json/wp/v2/users/me")
    else
        RESPONSE=$(curl -s -H "$AUTH_HEADER" "$WP_SITE_URL/wp-json/wp/v2/users/me")
    fi

    if echo "$RESPONSE" | grep -q '"id":'; then
        print_success "API connection successful"
    else
        print_error "API connection failed"
        echo "Response: $RESPONSE"
        exit 1
    fi
}

# Create Tools parent page
create_tools_page() {
    print_info "Creating Tools parent page..."

    TOOLS_CONTENT=$(cat << 'EOF'
<!-- wp:heading {"level":3} -->
<h3>Financial Tools & Calculators</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Explore our collection of free financial tools designed to help you make informed investment decisions and plan for your financial future.</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {"width":"50%"} -->
<div class="wp-block-column" style="flex-basis:50%"><!-- wp:heading {"level":4} -->
<h4>📈 Investment Calculators</h4>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li><strong><a href="/sip-calculator/">SIP Calculator</a></strong> - Calculate returns from Systematic Investment Plans in US stocks</li><li><strong><a href="/investment-calculator/">Investment Calculator</a></strong> - Basic investment return calculator (Coming Soon)</li><li><strong><a href="/retirement-calculator/">Retirement Calculator</a></strong> - Plan your retirement savings (Coming Soon)</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column {"width":"50%"} -->
<div class="wp-block-column" style="flex-basis:50%"><!-- wp:heading {"level":4} -->
<h4>💰 Financial Planning</h4>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li><strong><a href="/loan-calculator/">Loan Calculator</a></strong> - Calculate loan payments and interest (Coming Soon)</li><li><strong><a href="/tax-calculator/">Tax Calculator</a></strong> - Estimate your tax liability (Coming Soon)</li><li><strong><a href="/budget-planner/">Budget Planner</a></strong> - Create and manage your budget (Coming Soon)</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":4} -->
<h4>🚀 Featured Tool: SIP Calculator</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Our flagship US Stock Market SIP Calculator helps you estimate returns from systematic monthly investments. Features include:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>✅ Accurate compound interest calculations</li><li>✅ Advanced options (step-up investments, initial lump sum)</li><li>✅ Export results for further analysis</li><li>✅ Mobile-friendly responsive design</li><li>✅ Free to use with no registration required</li></ul>
<!-- /wp:list -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","className":"is-style-fill"} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/sip-calculator/">Try SIP Calculator Now</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->
EOF
)

    TOOLS_DATA=$(cat << EOF
{
    "title": "Tools",
    "content": "$TOOLS_CONTENT",
    "status": "publish",
    "type": "page",
    "slug": "tools"
}
EOF
)

    if [ "$USE_BASIC_AUTH" = true ]; then
        RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
            -H "Content-Type: application/json" \
            -H "$AUTH_HEADER" \
            -d "$TOOLS_DATA")
    else
        RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
            -H "Content-Type: application/json" \
            -H "$AUTH_HEADER" \
            -d "$TOOLS_DATA")
    fi

    TOOLS_PAGE_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 | tr -d ',')

    if [ -n "$TOOLS_PAGE_ID" ] && [ "$TOOLS_PAGE_ID" != "null" ]; then
        print_success "Tools page created (ID: $TOOLS_PAGE_ID)"
        echo "$TOOLS_PAGE_ID" > .tools_page_id
    else
        print_error "Failed to create Tools page"
        echo "Response: $RESPONSE"
        exit 1
    fi
}

# Create SIP Calculator page
create_sip_calculator_page() {
    print_info "Creating SIP Calculator page..."

    SIP_CONTENT='<!-- wp:paragraph -->
<p>Welcome to our US Stock Market SIP Calculator. Use this free tool to estimate returns from systematic monthly investments in stocks.</p>
<!-- /wp:paragraph -->

<!-- wp:shortcode -->
[sip_calculator]
<!-- /wp:shortcode -->

<!-- wp:paragraph -->
<p><em>Disclaimer: This calculator provides estimates based on historical market performance and should not be considered as financial advice. Past performance does not guarantee future results.</em></p>
<!-- /wp:paragraph -->'

    SIP_DATA=$(cat << EOF
{
    "title": "SIP Calculator",
    "content": "$SIP_CONTENT",
    "status": "publish",
    "type": "page",
    "slug": "sip-calculator"
}
EOF
)

    if [ "$USE_BASIC_AUTH" = true ]; then
        RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
            -H "Content-Type: application/json" \
            -H "$AUTH_HEADER" \
            -d "$SIP_DATA")
    else
        RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
            -H "Content-Type: application/json" \
            -H "$AUTH_HEADER" \
            -d "$SIP_DATA")
    fi

    SIP_PAGE_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 | tr -d ',')

    if [ -n "$SIP_PAGE_ID" ] && [ "$SIP_PAGE_ID" != "null" ]; then
        print_success "SIP Calculator page created (ID: $SIP_PAGE_ID)"
        echo "$SIP_PAGE_ID" > .sip_page_id
    else
        print_error "Failed to create SIP Calculator page"
        echo "Response: $RESPONSE"
        exit 1
    fi
}

# Create placeholder pages for other tools
create_placeholder_tools() {
    print_info "Creating placeholder pages for other tools..."

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

    # Loan Calculator
    LOAN_CONTENT='<!-- wp:heading -->
<h2>Loan Calculator</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Calculate loan payments, interest rates, and amortization schedules with our Loan Calculator.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Coming Soon!</strong> Features will include EMI calculations, prepayment options, and comparison tools.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="/tools/">← Back to Tools</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'

    # Create pages array
    declare -a PAGES=(
        "investment-calculator:$INVEST_CONTENT:Investment Calculator"
        "retirement-calculator:$RETIRE_CONTENT:Retirement Calculator"
        "loan-calculator:$LOAN_CONTENT:Loan Calculator"
    )

    for PAGE_DATA in "${PAGES[@]}"; do
        IFS=':' read -r SLUG CONTENT TITLE <<< "$PAGE_DATA"

        PAGE_JSON=$(cat << EOF
{
    "title": "$TITLE",
    "content": "$CONTENT",
    "status": "publish",
    "type": "page",
    "slug": "$SLUG"
}
EOF
)

        if [ "$USE_BASIC_AUTH" = true ]; then
            RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
                -H "Content-Type: application/json" \
                -H "$AUTH_HEADER" \
                -d "$PAGE_JSON")
        else
            RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
                -H "Content-Type: application/json" \
                -H "$AUTH_HEADER" \
                -d "$PAGE_JSON")
        fi

        PAGE_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 | tr -d ',')

        if [ -n "$PAGE_ID" ] && [ "$PAGE_ID" != "null" ]; then
            print_success "$TITLE page created (ID: $PAGE_ID)"
        else
            print_warning "Failed to create $TITLE page"
        fi
    done
}

# Update navigation menu
update_navigation_menu() {
    print_info "Updating navigation menu..."

    # Get menu ID (assuming primary menu)
    if [ "$USE_BASIC_AUTH" = true ]; then
        MENU_RESPONSE=$(curl -s "$WP_SITE_URL/wp-json/wp/v2/menus" \
            -H "$AUTH_HEADER")
    else
        MENU_RESPONSE=$(curl -s "$WP_SITE_URL/wp-json/wp/v2/menus" \
            -H "$AUTH_HEADER")
    fi

    # Try to find primary menu
    MENU_ID=$(echo "$MENU_RESPONSE" | grep -o '"id":[0-9]*,"name":"[^"]*Primary[^"]*"' | head -1 | cut -d':' -f2 | cut -d',' -f1)
    if [ -z "$MENU_ID" ]; then
        MENU_ID=$(echo "$MENU_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2 | tr -d ',')
    fi

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
            # Add Tools as top-level menu item
            MENU_ITEM_DATA=$(cat << EOF
{
    "title": "Tools",
    "url": "/tools/",
    "menu_order": 10,
    "status": "publish",
    "type": "post_type",
    "object": "page",
    "object_id": $TOOLS_ID,
    "menu_id": $MENU_ID
}
EOF
)

            if [ "$USE_BASIC_AUTH" = true ]; then
                curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/menu-items" \
                    -H "Content-Type: application/json" \
                    -H "$AUTH_HEADER" \
                    -d "$MENU_ITEM_DATA" > /dev/null
            else
                curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/menu-items" \
                    -H "Content-Type: application/json" \
                    -H "$AUTH_HEADER" \
                    -d "$MENU_ITEM_DATA" > /dev/null
            fi

            print_success "Added Tools to navigation menu"
        fi

        if [ -n "$SIP_ID" ] && [ -n "$TOOLS_ID" ]; then
            # Add SIP Calculator as submenu item
            SUBMENU_ITEM_DATA=$(cat << EOF
{
    "title": "SIP Calculator",
    "url": "/sip-calculator/",
    "menu_order": 1,
    "status": "publish",
    "type": "post_type",
    "object": "page",
    "object_id": $SIP_ID,
    "menu_id": $MENU_ID,
    "parent": $TOOLS_ID
}
EOF
)

            if [ "$USE_BASIC_AUTH" = true ]; then
                curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/menu-items" \
                    -H "Content-Type: application/json" \
                    -H "$AUTH_HEADER" \
                    -d "$SUBMENU_ITEM_DATA" > /dev/null
            else
                curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/menu-items" \
                    -H "Content-Type: application/json" \
                    -H "$AUTH_HEADER" \
                    -d "$SUBMENU_ITEM_DATA" > /dev/null
            fi

            print_success "Added SIP Calculator as submenu item"
        fi
    else
        print_warning "Could not find menu to update. You may need to add menu items manually."
    fi
}

# Clean up temporary files
cleanup() {
    rm -f .tools_page_id .sip_page_id
}

# Main execution
main() {
    echo ""
    get_credentials
    get_api_token
    test_api_connection
    create_tools_page
    create_sip_calculator_page
    create_placeholder_tools
    update_navigation_menu
    cleanup

    echo ""
    print_success "🎉 Tools setup completed via WordPress API!"
    echo ""
    echo "What was created:"
    echo "✓ Tools parent page (/tools/)"
    echo "✓ SIP Calculator page (/sip-calculator/)"
    echo "✓ Placeholder pages for future tools"
    echo "✓ Navigation menu updated with Tools → SIP Calculator structure"
    echo ""
    echo "Next steps:"
    echo "1. Visit your site and check the Tools menu"
    echo "2. Test the SIP Calculator functionality"
    echo "3. Customize the placeholder pages as you add more tools"
    echo ""
    echo "Navigation structure:"
    echo "Tools"
    echo "  └─ SIP Calculator"
    echo "  └─ Investment Calculator (Coming Soon)"
    echo "  └─ Retirement Calculator (Coming Soon)"
    echo "  └─ Loan Calculator (Coming Soon)"
}

# Run main function
main