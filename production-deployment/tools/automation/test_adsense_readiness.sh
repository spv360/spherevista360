#!/bin/bash
# AdSense Readiness Quick Test Script
# Run this to check basic technical requirements

echo "🔍 Google AdSense Readiness Quick Test"
echo "======================================"
echo ""

# Check if required files exist
echo "📁 Checking required files:"
echo -n "ads.txt: "
if [ -f "ads.txt" ]; then
    echo "✅ Found"
else
    echo "❌ Missing"
fi

echo -n "robots.txt: "
if [ -f "robots.txt" ]; then
    echo "✅ Found"
else
    echo "❌ Missing"
fi

echo -n ".htaccess: "
if [ -f ".htaccess" ]; then
    echo "✅ Found"
else
    echo "❌ Missing"
fi

echo ""
echo "🌐 Online Tests to Run:"
echo "1. Google PageSpeed Insights: https://pagespeed.web.dev/"
echo "2. Google Mobile-Friendly Test: https://search.google.com/test/mobile-friendly"
echo "3. Google Rich Results Test: https://search.google.com/test/rich-results"
echo "4. W3C HTML Validator: https://validator.w3.org/"
echo ""

echo "📊 Content Quality Checklist:"
echo "□ Minimum 3-5 pages of quality content"
echo "□ Original, valuable content (not copied)"
echo "□ Clear navigation and site structure"
echo "□ Privacy Policy page exists"
echo "□ Contact page with working form"
echo "□ About page explaining site purpose"
echo ""

echo "⚡ Performance Checklist:"
echo "□ Site loads in under 3 seconds"
echo "□ Mobile-responsive design"
echo "□ HTTPS enabled"
echo "□ No broken links"
echo "□ Proper title tags and meta descriptions"
echo ""

echo "🚀 Next Steps:"
echo "1. Upload all files to Hostinger"
echo "2. Run online tests above"
echo "3. Check content quality manually"
echo "4. Apply to AdSense when ready"
echo ""

echo "📞 Need Help?"
echo "Check ADSENSE_READINESS_CHECKLIST.md for detailed guide"