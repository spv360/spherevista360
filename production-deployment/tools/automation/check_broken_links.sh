#!/bin/bash
# Broken Link Checker for SphereVista360
# Tests all article and page links from homepage

echo "🔗 Checking for Broken Links on SphereVista360"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Array of URLs to check (from homepage)
URLS=(
    "https://spherevista360.com/"
    "https://spherevista360.com/about-us/"
    "https://spherevista360.com/ai-in-investment-management-opportunities-and-challenges/"
    "https://spherevista360.com/ai-speech-and-safety-what-regulation-is-aiming-for-in-2025-2/"
    "https://spherevista360.com/archives/"
    "https://spherevista360.com/blog/"
    "https://spherevista360.com/celebrity-social-impact/"
    "https://spherevista360.com/contact/"
    "https://spherevista360.com/digital-identity-goes-global-cross-border-logins-payments/"
    "https://spherevista360.com/disclaimer/"
    "https://spherevista360.com/green-bonds-energy-transition-where-yields-make-sense/"
    "https://spherevista360.com/hollywood-blockbusters-2025/"
    "https://spherevista360.com/homepage/"
    "https://spherevista360.com/newsletter/"
    "https://spherevista360.com/open-source-ai-models-in-the-enterprise-build-buy-or-blend-2/"
    "https://spherevista360.com/ops-copilots-automating-unsexy-work-that-scales-businesses/"
    "https://spherevista360.com/privacy-policy/"
    "https://spherevista360.com/regulatory-technology-streamlining-compliance-in-finance/"
    "https://spherevista360.com/reshoring-20-supply-chains-really-changing-2025/"
    "https://spherevista360.com/sitemap/"
    "https://spherevista360.com/streaming-gets-personal-ai-recommenders-shape-you-watch/"
    "https://spherevista360.com/subscribe/"
    "https://spherevista360.com/terms-of-service/"
    "https://spherevista360.com/the-future-of-digital-banking-trends-to-watch-in-2025/"
)

total_urls=${#URLS[@]}
broken_count=0
working_count=0

echo -e "${BLUE}Testing $total_urls URLs...${NC}"
echo ""

for url in "${URLS[@]}"; do
    # Get HTTP status code
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    # Extract page name for display
    page_name=$(echo "$url" | sed 's|https://spherevista360.com/||' | sed 's|/$||')
    if [ -z "$page_name" ]; then
        page_name="homepage"
    fi

    case $status in
        200)
            echo -e "✅ ${GREEN}OK${NC} ($status) - $page_name"
            ((working_count++))
            ;;
        301|302)
            echo -e "↪️  ${YELLOW}REDIRECT${NC} ($status) - $page_name"
            ((working_count++))
            ;;
        404)
            echo -e "❌ ${RED}BROKEN${NC} ($status) - $page_name"
            ((broken_count++))
            ;;
        403)
            echo -e "🚫 ${YELLOW}FORBIDDEN${NC} ($status) - $page_name"
            ((working_count++))
            ;;
        500|502|503|504)
            echo -e "💥 ${RED}SERVER ERROR${NC} ($status) - $page_name"
            ((broken_count++))
            ;;
        *)
            echo -e "❓ ${YELLOW}UNKNOWN${NC} ($status) - $page_name"
            ;;
    esac
done

echo ""
echo "📊 Link Check Summary:"
echo "======================"
echo -e "Total URLs tested: $total_urls"
echo -e "${GREEN}Working links: $working_count${NC}"
echo -e "${RED}Broken/problematic links: $broken_count${NC}"

if [ $broken_count -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Excellent! No broken links found!${NC}"
    echo "Your site has perfect link integrity."
else
    echo ""
    echo -e "${RED}⚠️  $broken_count broken/problematic links found!${NC}"
    echo "These should be fixed for better SEO and user experience."
fi

echo ""
echo "💡 Recommendations:"
echo "- Run this check regularly to maintain link health"
echo "- Fix any 404 errors immediately"
echo "- Monitor for server errors (5xx status codes)"
echo "- Consider redirecting intentionally removed pages"

echo ""
echo "🔍 For AdSense: Perfect link health improves approval chances and user experience!"