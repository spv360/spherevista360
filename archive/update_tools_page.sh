#!/bin/bash

# Update existing Tools page to include SIP Calculator
# This script will modify the existing Tools page to add the SIP Calculator

set -e

echo "🔧 Updating existing Tools page to include SIP Calculator"
echo "======================================================"

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

# Update the existing Tools page
update_tools_page() {
    print_info "Updating existing Tools page (ID: 3072)..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    # New content that includes SIP Calculator and Compound Interest Calculator
    NEW_CONTENT='<!-- wp:heading {"level":1} -->
<h1>Financial Tools & Calculators</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Access our comprehensive suite of financial planning and analysis tools designed to help you make informed investment decisions.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Available Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li><strong><a href="/sip-calculator/">SIP Calculator</a></strong> – Calculate returns from Systematic Investment Plans in US stocks</li><li><strong><a href="/compound-interest-calculator/">Compound Interest Calculator</a></strong> – Calculate compound interest and investment growth over time</li><li><strong><a href="/loan-emi-calculator/">Loan EMI Calculator</a></strong> – Calculate loan payments, interest, and amortization schedules</li><li><strong><a href="/lump-sum-investment-calculator/">Lump Sum Investment Calculator</a></strong> – Calculate returns on one-time investments with compound interest</li><li><strong><a href="/us-tax-calculator-suite/">US Tax & Investment Calculator Suite</a></strong> – Comprehensive tax and investment calculation tools for federal, state, retirement, and lump sum investments</li><li><strong><a href="/retirement-planner-estimator/">Retirement Planner and Estimator</a></strong> – Plan your retirement with comprehensive savings projections and income estimates</li><li><strong><a href="/investment-calculator/">Investment Calculator</a></strong> – Project returns and analyze portfolio performance (Coming Soon)</li></ul>
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
<h3>🚀 Featured Tools</h3>
<!-- /wp:heading -->

<!-- wp:heading {"level":4} -->
<h4>SIP Calculator</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Our US Stock Market SIP Calculator helps you estimate returns from systematic monthly investments. Features include compound interest calculations, step-up investments, and export functionality.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","className":"is-style-fill"} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/sip-calculator/">Try SIP Calculator</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:heading {"level":4} -->
<h4>Lump Sum Investment Calculator</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Calculate the power of compound interest on a one-time investment. Perfect for understanding how lump sum investments grow over time with different compounding frequencies.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link" href="/lump-sum-investment-calculator/">Try Lump Sum Investment Calculator</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:heading {"level":4} -->
<h4>Retirement Planner and Estimator</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Comprehensive retirement planning tool that helps you estimate savings needed, project future income, and plan for long-term financial security with inflation-adjusted calculations.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link" href="/retirement-planner-estimator/">Try Retirement Planner</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'

    # Update the page
    JSON_PAYLOAD=$(cat << EOF
{
  "content": "$(echo "$NEW_CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')"
}
EOF
)

    RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages/3072" \
        -H "Content-Type: application/json" \
        -H "$AUTH_HEADER" \
        -d "$JSON_PAYLOAD")

    if echo "$RESPONSE" | grep -q '"id":3072'; then
        print_success "Tools page updated successfully!"
    else
        print_error "Failed to update Tools page"
        echo "Response: $RESPONSE"
        return 1
    fi
}

# Clean up duplicate pages
cleanup_duplicates() {
    print_info "Cleaning up duplicate pages..."

    AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

    # Delete the duplicate Tools page (ID: 3101)
    DELETE_RESPONSE=$(curl -s -X DELETE "$WP_SITE_URL/wp-json/wp/v2/pages/3101?force=true" \
        -H "$AUTH_HEADER")

    if echo "$DELETE_RESPONSE" | grep -q '"deleted":true'; then
        print_success "Duplicate Tools page deleted"
    else
        print_warning "Could not delete duplicate Tools page"
    fi

    # Update the placeholder page titles
    PLACEHOLDER_UPDATES=(
        "3103:Investment Calculator"
    )

    for UPDATE in "${PLACEHOLDER_UPDATES[@]}"; do
        IFS=':' read -r PAGE_ID TITLE <<< "$UPDATE"

        TITLE_JSON=$(cat << EOF
{
  "title": "$TITLE"
}
EOF
)

        curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID" \
            -H "Content-Type: application/json" \
            -H "$AUTH_HEADER" \
            -d "$TITLE_JSON" > /dev/null

        print_success "Updated page $PAGE_ID title to '$TITLE'"
    done
}

# Main execution
main() {
    echo ""
    get_credentials

    if update_tools_page; then
        cleanup_duplicates

        echo ""
        print_success "🎉 Tools page updated successfully!"
        echo ""
        echo "Changes made:"
        echo "✓ Updated existing Tools page (/tools/) to include SIP Calculator"
        echo "✓ Added SIP Calculator as the featured tool"
        echo "✓ Fixed placeholder page titles"
        echo "✓ Removed duplicate Tools page"
        echo ""
        echo "Visit: https://spherevista360.com/tools/"
        echo ""
        echo "The Tools page now shows:"
        echo "• SIP Calculator (featured)"
        echo "• Lump Sum Investment Calculator (featured)"
        echo "• Retirement Planner and Estimator (featured)"
    else
        print_error "Failed to update Tools page"
        exit 1
    fi
}

main