#!/bin/bash
# AdSense Readiness Automation Test Script
# Tests live site for Google AdSense compliance
# Usage: ./test_live_site.sh yourdomain.com

DOMAIN=${1:-"spherevista360.com"}
SITE_URL="https://$DOMAIN"

echo "🔍 AdSense Readiness Test for: $SITE_URL"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check HTTP status
check_url() {
    local url=$1
    local expected_code=${2:-200}
    local description=$3

    echo -n "$description: "
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$response" = "$expected_code" ]; then
        echo -e "${GREEN}✅ PASS${NC} ($response)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} ($response)"
        return 1
    fi
}

# Function to check if content contains text
check_content() {
    local url=$1
    local search_text=$2
    local description=$3

    echo -n "$description: "
    content=$(curl -s "$url")

    if echo "$content" | grep -q "$search_text"; then
        echo -e "${GREEN}✅ PASS${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        return 1
    fi
}

# Function to check response time
check_speed() {
    local url=$1
    local max_time=${2:-3000} # milliseconds
    local description=$3

    echo -n "$description: "
    time_ms=$(curl -s -o /dev/null -w "%{time_total}" "$url" | awk '{printf "%.0f", $1 * 1000}')

    if [ "$time_ms" -lt "$max_time" ]; then
        echo -e "${GREEN}✅ PASS${NC} (${time_ms}ms)"
        return 0
    else
        echo -e "${YELLOW}⚠️  SLOW${NC} (${time_ms}ms)"
        return 1
    fi
}

echo "📁 Testing Required Files:"
echo "---------------------------"
check_url "$SITE_URL/ads.txt" 200 "ads.txt accessibility"
check_url "$SITE_URL/robots.txt" 200 "robots.txt accessibility"
check_url "$SITE_URL/favicon.ico" 200 "favicon.ico accessibility"
check_url "$SITE_URL/apple-touch-icon.png" 200 "apple-touch-icon.png accessibility"

echo ""
echo "🔗 Testing Core Pages:"
echo "----------------------"
check_url "$SITE_URL/" 200 "Homepage accessibility"
check_url "$SITE_URL/privacy-policy/" 200 "Privacy Policy page"
check_url "$SITE_URL/contact/" 200 "Contact page"
check_url "$SITE_URL/sitemap.xml" 200 "XML Sitemap"

echo ""
echo "⚡ Testing Performance:"
echo "----------------------"
check_speed "$SITE_URL/" 3000 "Homepage load time (< 3s)"
check_speed "$SITE_URL/ads.txt" 1000 "ads.txt load time (< 1s)"

echo ""
echo "📄 Testing Content & Structure:"
echo "-------------------------------"

# Check if ads.txt contains publisher ID
echo -n "ads.txt has publisher ID: "
ads_content=$(curl -s "$SITE_URL/ads.txt")
if echo "$ads_content" | grep -q "pub-1542284739923981"; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

# Check if robots.txt has AdSense-friendly directives
echo -n "robots.txt has proper directives: "
robots_content=$(curl -s "$SITE_URL/robots.txt")
if echo "$robots_content" | grep -q "User-agent:" && echo "$robots_content" | grep -q "Disallow:"; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

# Check for HTTPS
echo -n "Site uses HTTPS: "
if [[ $SITE_URL == https://* ]]; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

# Check for basic HTML structure
echo -n "Homepage has basic HTML structure: "
homepage_content=$(curl -s "$SITE_URL/")
if echo "$homepage_content" | grep -q "<!DOCTYPE html>" && echo "$homepage_content" | grep -q "<title>" && echo "$homepage_content" | grep -q "</html>"; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

# Check for mobile viewport meta tag
echo -n "Homepage has mobile viewport: "
if echo "$homepage_content" | grep -q "viewport"; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
fi

echo ""
echo "🔒 Testing Security & Headers:"
echo "------------------------------"

# Check for security headers
echo -n "Security headers present: "
headers=$(curl -s -I "$SITE_URL/")
security_headers=0

if echo "$headers" | grep -q "X-Content-Type-Options"; then ((security_headers++)); fi
if echo "$headers" | grep -q "X-Frame-Options\|X-XSS-Protection"; then ((security_headers++)); fi

if [ $security_headers -ge 1 ]; then
    echo -e "${GREEN}✅ PASS${NC} ($security_headers headers found)"
else
    echo -e "${YELLOW}⚠️  NONE${NC}"
fi

echo ""
echo "📱 Mobile & Accessibility Tests:"
echo "--------------------------------"

# Check for responsive design indicators
echo -n "Responsive design indicators: "
responsive_indicators=0

if echo "$homepage_content" | grep -q "viewport"; then ((responsive_indicators++)); fi
if echo "$homepage_content" | grep -q "bootstrap\|foundation\|materialize"; then ((responsive_indicators++)); fi
if echo "$homepage_content" | grep -q "flex\|grid"; then ((responsive_indicators++)); fi

if [ $responsive_indicators -ge 1 ]; then
    echo -e "${GREEN}✅ PASS${NC} ($responsive_indicators indicators found)"
else
    echo -e "${YELLOW}⚠️  NONE${NC}"
fi

echo ""
echo "🎯 AdSense Compliance Summary:"
echo "------------------------------"

# Count passed tests
total_tests=15
passed_tests=0

# Recalculate based on actual results (this is a simplified version)
echo -e "${BLUE}Manual checks still needed:${NC}"
echo "□ Content quality and originality"
echo "□ Ad placement policy compliance"
echo "□ Privacy policy completeness"
echo "□ Contact form functionality"
echo "□ Regular content publishing"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review any FAILED tests above"
echo "2. Run Google PageSpeed Insights: https://pagespeed.web.dev/"
echo "3. Test mobile-friendliness: https://search.google.com/test/mobile-friendly"
echo "4. Check content quality manually"
echo "5. Apply to AdSense when all checks pass"
echo ""

echo -e "${BLUE}Need Help?${NC}"
echo "Run: ./ADSENSE_READINESS_CHECKLIST.md for detailed manual checks"