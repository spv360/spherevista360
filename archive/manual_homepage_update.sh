#!/bin/bash

# Manually update homepage with Compound Interest Calculator button
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"
PAGE_ID=2412

echo "Manually updating homepage with Compound Interest Calculator"
read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
echo ""

AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

# Create the complete updated homepage content
NEW_CONTENT='<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"24px","bottom":"24px"}},"color":{"background":"#f4f8ff"}},"className":"homepage-tools-cta"} -->
<div class="wp-block-group alignfull homepage-tools-cta" style="background:#f4f8ff;padding-top:24px;padding-bottom:24px"><div class="wp-block-group__inner-container"><!-- wp:heading {"textAlign":"center","level":3} -->
<h3 class="wp-block-heading has-text-align-center">Explore our free financial tools</h3>
<!-- /wp:heading --><!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","className":"is-style-fill"} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/tools/">All Tools</a></div>
<!-- /wp:button --><!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link" href="/sip-calculator/">SIP Calculator</a></div>
<!-- /wp:button --><!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link" href="/compound-interest-calculator/">Compound Interest</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div></div>
<!-- /wp:group -->

<!-- wp:paragraph -->
<p>Welcome to SphereVista360 – Your comprehensive source for financial insights, market analysis, and investment guidance. We provide expert analysis on global markets, economic trends, and investment strategies to help you make informed financial decisions.</p>
<!-- /wp:paragraph -->

<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"40px","bottom":"40px"}},"color":{"background":"#f8f9fa"}},"className":"finance-spotlight"} -->
<div class="wp-block-group alignfull finance-spotlight" style="background:#f8f9fa;padding-top:40px;padding-bottom:40px"><div class="wp-block-group__inner-container"><!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="wp-block-heading has-text-align-center">📈 Market Intelligence & Investment Insights</h2>
<!-- /wp:heading --><!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Stay informed with our comprehensive market analysis and investment guidance</p>
<!-- /wp:paragraph --></div></div>
<!-- /wp:group -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {"width":"33.33%"} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:heading {"level":3} -->
<h3>💰 Investment Strategies</h3>
<!-- /wp:heading --><!-- wp:list -->
<ul><li><strong>Portfolio Diversification</strong> – Build resilient investment portfolios</li><li><strong>Risk Management</strong> – Protect your investments from market volatility</li><li><strong>Asset Allocation</strong> – Optimize your investment mix</li><li><strong>Tax-Efficient Investing</strong> – Maximize returns through smart tax planning</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column --><!-- wp:column {"width":"33.33%"} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:heading {"level":3} -->
<h3>📊 Economic Analysis</h3>
<!-- /wp:heading --><!-- wp:list -->
<ul><li><strong>GDP Trends</strong> – Global economic growth indicators</li><li><strong>Inflation Monitoring</strong> – Impact on purchasing power and investments</li><li><strong>Interest Rate Analysis</strong> – Federal Reserve policy implications</li><li><strong>Currency Markets</strong> – Forex trends and international trade</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column --><!-- wp:column {"width":"33.33%"} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:heading {"level":3} -->
<h3>🏦 Banking & Finance</h3>
<!-- /wp:heading --><!-- wp:list -->
<ul><li><strong>Digital Banking</strong> – Fintech innovations and mobile banking</li><li><strong>Cryptocurrency</strong> – Blockchain and digital asset strategies</li><li><strong>Fintech Startups</strong> – Emerging financial technology companies</li><li><strong>Regulatory Updates</strong> – Compliance and regulatory changes</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="wp-block-heading has-text-align-center">🎯 Featured Financial Topics</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Stock Market Analysis</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>In-depth analysis of equity markets, sector performance, and investment opportunities in stocks and ETFs.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Bond Markets & Fixed Income</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Understanding bond yields, credit ratings, and fixed income investment strategies for portfolio stability.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Real Estate Investment</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Commercial and residential real estate trends, REITs, and property investment strategies.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Alternative Investments</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Hedge funds, private equity, commodities, and other alternative investment vehicles.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"30px","bottom":"30px"}},"color":{"background":"#e8f4fd"}},"className":"market-tools"} -->
<div class="wp-block-group alignfull market-tools" style="background:#e8f4fd;padding-top:30px;padding-bottom:30px"><div class="wp-block-group__inner-container"><!-- wp:heading {"textAlign":"center","level":3} -->
<h3 class="wp-block-heading has-text-align-center">🛠️ Free Financial Tools</h3>
<!-- /wp:heading --><!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Access our suite of free calculators and tools to make informed financial decisions</p>
<!-- /wp:paragraph --><!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"vivid-cyan-blue","textColor":"white","className":"is-style-fill"} -->
<div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-white-color has-vivid-cyan-blue-background-color has-text-color has-background" href="/tools/">Explore All Tools</a></div>
<!-- /wp:button --><!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link" href="/sip-calculator/">SIP Calculator</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div></div>
<!-- /wp:group -->

<!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="wp-block-heading has-text-align-center">Why Choose SphereVista360?</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Expert Analysis</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Professional financial analysis and market insights from experienced analysts.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Comprehensive Coverage</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Complete coverage of global markets, economic trends, and investment opportunities.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Free Tools</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Access powerful financial calculators and analysis tools at no cost.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":4} -->
<h4>Educational Resources</h4>
<!-- /wp:heading --><!-- wp:paragraph -->
<p>Learn about investing, markets, and financial planning with our educational content.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {"textAlign":"center","level":2} -->
<h2 class="wp-block-heading has-text-align-center">Join Our Community</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Stay updated with the latest financial news, market analysis, and investment insights. Subscribe to our newsletter and follow us on social media.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="/newsletter/">Subscribe to Newsletter</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'

# Escape for JSON
ESCAPED_CONTENT=$(echo "$NEW_CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')

JSON_PAYLOAD="{\"content\": \"$ESCAPED_CONTENT\"}"

echo "Updating homepage with new CTA section..."
RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages/$PAGE_ID" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d "$JSON_PAYLOAD")

if echo "$RESPONSE" | grep -q '"id":'; then
  echo "✅ Homepage updated successfully with Compound Interest Calculator!"
  echo ""
  echo "🔄 Clear cache to see changes:"
  echo "WordPress Admin → LiteSpeed Cache → Toolbox → Purge All"
  echo "Visit: https://spherevista360.com/"
else
  echo "❌ Update failed. Response: $RESPONSE"
  exit 1
fi