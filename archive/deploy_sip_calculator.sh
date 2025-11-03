#!/bin/bash

# SIP Calculator Deployment Script for SphereVista360
# This script deploys the SIP calculator to the WordPress site

set -e  # Exit on any error

echo "🚀 Deploying SIP Calculator to SphereVista360"
echo "=============================================="

# Configuration
WP_SITE_URL="https://spherevista360.com"
WP_ADMIN_USER=""  # Will be prompted
WP_ADMIN_PASS=""  # Will be prompted
PLUGIN_NAME="sip-calculator"
PLUGIN_FILE="sip-calculator.php"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."

    if [ ! -f "$PLUGIN_FILE" ]; then
        print_error "Plugin file $PLUGIN_FILE not found!"
        exit 1
    fi

    print_success "All required files found"
}

# Get WordPress credentials
get_credentials() {
    print_status "WordPress Admin Credentials Required"

    if [ -z "$WP_ADMIN_USER" ]; then
        read -p "Enter WordPress admin username: " WP_ADMIN_USER
    fi

    if [ -z "$WP_ADMIN_PASS" ]; then
        read -s -p "Enter WordPress admin password: " WP_ADMIN_PASS
        echo ""
    fi
}

# Test WordPress connection
test_connection() {
    print_status "Testing WordPress connection..."

    # Try to access wp-admin
    if curl -s -o /dev/null -w "%{http_code}" "$WP_SITE_URL/wp-admin/" | grep -q "200\|301\|302"; then
        print_success "WordPress site is accessible"
    else
        print_error "Cannot access WordPress site at $WP_SITE_URL"
        exit 1
    fi
}

# Create plugin directory structure
create_plugin_structure() {
    print_status "Creating plugin directory structure..."

    PLUGIN_DIR="sip-calculator-plugin"
    mkdir -p "$PLUGIN_DIR"

    # Copy main plugin file
    cp "$PLUGIN_FILE" "$PLUGIN_DIR/"

    # Create CSS file
    cat > "$PLUGIN_DIR/sip-calculator.css" << 'EOF'
/* SIP Calculator Styles */
.sip-calculator-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.sip-header {
    text-align: center;
    margin-bottom: 30px;
}

.sip-header h1 {
    color: #2c3e50;
    margin-bottom: 10px;
    font-size: 2.5em;
}

.sip-badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

.sip-badges span {
    background: #3498db;
    color: white;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 0.9em;
}

.sip-calculator-wrapper {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.sip-form-section {
    background: white;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 25px;
    border-left: 5px solid #3498db;
}

.sip-form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
}

.sip-input-group {
    display: flex;
    align-items: center;
}

.sip-input-group input {
    flex: 1;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 8px 0 0 8px;
    font-size: 16px;
    border-right: none;
}

.sip-unit {
    padding: 12px 15px;
    background: #ecf0f1;
    border: 2px solid #ddd;
    border-left: none;
    border-radius: 0 8px 8px 0;
    color: #7f8c8d;
    font-weight: 600;
}

.sip-advanced-options {
    margin-top: 15px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.sip-actions {
    text-align: center;
    margin: 30px 0;
}

.sip-actions button {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    margin: 5px;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
}

.sip-results {
    background: #f8f9fa;
    padding: 25px;
    border-radius: 10px;
    border-left: 5px solid #27ae60;
}

.sip-result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
}

.sip-result-item {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.sip-result-label {
    font-size: 14px;
    color: #7f8c8d;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.sip-result-value {
    font-size: 24px;
    font-weight: bold;
    color: #27ae60;
}

.sip-yearly-breakdown {
    background: #34495e;
    color: white;
    padding: 20px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    white-space: pre-line;
    overflow-x: auto;
}

.sip-info-section {
    margin-top: 30px;
    background: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.sip-features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-top: 20px;
}

.sip-feature {
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}

.sip-disclaimer {
    margin-top: 20px;
    padding: 15px;
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
}

@media (max-width: 768px) {
    .sip-calculator-container {
        padding: 10px;
    }

    .sip-header h1 {
        font-size: 2em;
    }

    .sip-form-grid {
        grid-template-columns: 1fr;
    }

    .sip-result-grid {
        grid-template-columns: 1fr;
    }

    .sip-features {
        grid-template-columns: 1fr;
    }
}
EOF

    # Create JS file
    cat > "$PLUGIN_DIR/sip-calculator.js" << 'EOF'
jQuery(document).ready(function($) {
    let currentResults = null;

    // Make functions global for onclick handlers
    window.toggleAdvanced = function() {
        const advanced = document.getElementById('sip-advanced-options');
        advanced.style.display = advanced.style.display === 'none' ? 'block' : 'none';
    };

    window.calculateSIP = function() {
        // Get input values
        const monthlyInvestment = parseFloat(document.getElementById('sip-monthly-investment').value) || 0;
        const returnRate = parseFloat(document.getElementById('sip-return-rate').value) / 100 || 0;
        const investmentPeriod = parseInt(document.getElementById('sip-investment-period').value) || 0;
        const initialInvestment = parseFloat(document.getElementById('sip-initial-investment').value) || 0;
        const stepUp = parseFloat(document.getElementById('sip-step-up').value) / 100 || 0;

        if (monthlyInvestment <= 0 || returnRate < 0 || investmentPeriod <= 0) {
            alert('Please enter valid values for monthly investment, return rate, and investment period.');
            return;
        }

        // Calculate SIP returns
        let totalInvested = initialInvestment;
        let currentValue = initialInvestment;
        let currentMonthlyInvestment = monthlyInvestment;
        const yearlyBreakdown = [];

        for (let year = 1; year <= investmentPeriod; year++) {
            const yearlyStartValue = currentValue;
            let yearlyInvested = 0;

            for (let month = 1; month <= 12; month++) {
                currentValue += currentMonthlyInvestment;
                totalInvested += currentMonthlyInvestment;
                yearlyInvested += currentMonthlyInvestment;

                // Apply monthly returns
                currentValue *= (1 + returnRate / 12);
            }

            const yearlyReturn = currentValue - yearlyStartValue - yearlyInvested;
            const yearlyReturnPct = yearlyStartValue > 0 ? (yearlyReturn / yearlyStartValue) * 100 : 0;

            yearlyBreakdown.push({
                year,
                investment: yearlyInvested,
                cumulativeInvestment: totalInvested,
                portfolioValue: currentValue,
                yearlyReturn,
                yearlyReturnPct
            });

            // Apply step-up for next year
            currentMonthlyInvestment *= (1 + stepUp);
        }

        const totalReturns = currentValue - totalInvested;
        const totalReturnPct = totalInvested > 0 ? (totalReturns / totalInvested) * 100 : 0;

        // Store results
        currentResults = {
            inputs: { monthlyInvestment, returnRate: returnRate * 100, investmentPeriod, initialInvestment, stepUp: stepUp * 100 },
            summary: { totalInvested, currentValue, totalReturns, totalReturnPct },
            yearlyBreakdown
        };

        // Display results
        displayResults(currentResults);
    };

    function displayResults(results) {
        document.getElementById('sip-results').style.display = 'block';

        // Update summary values
        document.getElementById('sip-total-invested').textContent = formatCurrency(results.summary.totalInvested);
        document.getElementById('sip-final-value').textContent = formatCurrency(results.summary.currentValue);
        document.getElementById('sip-total-returns').textContent = formatCurrency(results.summary.totalReturns);
        document.getElementById('sip-return-percentage').textContent = formatPercentage(results.summary.totalReturnPct);

        // Update yearly breakdown
        let breakdownText = 'Year  Investment  Cumulative  Portfolio  Yearly Return  Return %\n';
        breakdownText += '----  ----------  ----------  ---------  -------------  --------\n';

        results.yearlyBreakdown.forEach(row => {
            breakdownText += `${row.year.toString().padStart(4)}  ${formatCurrency(row.investment).padStart(10)}  ${formatCurrency(row.cumulativeInvestment).padStart(10)}  ${formatCurrency(row.portfolioValue).padStart(9)}  ${formatCurrency(row.yearlyReturn).padStart(13)}  ${formatPercentage(row.yearlyReturnPct).padStart(8)}\n`;
        });

        document.getElementById('sip-yearly-breakdown').textContent = breakdownText;

        // Scroll to results
        document.getElementById('sip-results').scrollIntoView({ behavior: 'smooth' });
    }

    window.exportResults = function() {
        if (!currentResults) {
            alert('Please calculate results first.');
            return;
        }

        const dataStr = JSON.stringify(currentResults, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `sip-calculation-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    };

    window.resetForm = function() {
        document.getElementById('sip-monthly-investment').value = '500';
        document.getElementById('sip-return-rate').value = '10';
        document.getElementById('sip-investment-period').value = '10';
        document.getElementById('sip-initial-investment').value = '0';
        document.getElementById('sip-step-up').value = '0';
        document.getElementById('sip-results').style.display = 'none';
        currentResults = null;
    };

    // Helper functions
    function formatCurrency(amount) {
        return '$' + Math.round(amount).toLocaleString('en-US');
    }

    function formatPercentage(value) {
        return value.toFixed(1) + '%';
    }

    // Initialize with default calculation
    calculateSIP();
});
EOF

    # Create README for the plugin
    cat > "$PLUGIN_DIR/README.md" << 'EOF'
# SIP Calculator WordPress Plugin

A professional US Stock Market SIP (Systematic Investment Plan) calculator plugin for WordPress.

## Features

- 📊 Accurate compound interest calculations with monthly compounding
- 🚀 Advanced options: step-up investments, initial lump sum
- 💾 Export results as JSON for further analysis
- 📱 Responsive design that works on all devices
- 🎨 Beautiful, modern UI with gradient backgrounds
- ⚡ Fast, client-side calculations (no server load)

## Installation

1. Upload the `sip-calculator` folder to your `/wp-content/plugins/` directory
2. Activate the plugin through the WordPress admin dashboard
3. Use the shortcode `[sip_calculator]` on any page or post

## Shortcode Parameters

```
[sip_calculator monthly_investment="500" return_rate="10" investment_period="10" initial_investment="0" step_up="0"]
```

## Usage

Simply add the shortcode to any WordPress page or post:

```
[sip_calculator]
```

## Disclaimer

This calculator provides estimates based on historical market performance and should not be considered as financial advice. Past performance does not guarantee future results. Always consult with qualified financial advisors before making investment decisions.

## License

GPL v2 or later
EOF

    print_success "Plugin structure created in $PLUGIN_DIR/"
}

# Create ZIP file for upload
create_zip() {
    print_status "Creating plugin ZIP file..."

    if command -v zip &> /dev/null; then
        zip -r "sip-calculator.zip" "sip-calculator-plugin/"
        print_success "Plugin ZIP created: sip-calculator.zip"
    else
        print_warning "zip command not found. Please manually create ZIP from sip-calculator-plugin/ folder"
    fi
}

# Create deployment instructions
create_instructions() {
    print_status "Creating deployment instructions..."

    cat > "SIP_CALCULATOR_DEPLOYMENT_INSTRUCTIONS.md" << EOF
# SIP Calculator Deployment Instructions

## Method 1: WordPress Admin Upload (Recommended)

1. **Login to WordPress Admin**
   - Go to $WP_SITE_URL/wp-admin/
   - Login with your admin credentials

2. **Upload Plugin**
   - Navigate to Plugins → Add New
   - Click "Upload Plugin"
   - Choose the \`sip-calculator.zip\` file
   - Click "Install Now"
   - Activate the plugin

3. **Add Calculator to Page**
   - Create a new page or edit existing page
   - Add the shortcode: \`[sip_calculator]\`
   - Publish the page

## Method 2: Manual FTP Upload

1. **Upload Files**
   - Upload the \`sip-calculator-plugin\` folder to \`/wp-content/plugins/\`
   - Rename folder to \`sip-calculator\`

2. **Activate Plugin**
   - Login to WordPress admin
   - Go to Plugins
   - Activate "SIP Calculator"

3. **Add to Page**
   - Use shortcode \`[sip_calculator]\` in any page/post

## Method 3: Direct HTML Embed

If you prefer not to use a plugin, you can embed the calculator directly:

1. Copy the content from \`sip_calculator_wordpress_page.html\`
2. Create a new WordPress page
3. Switch to "HTML" editor mode
4. Paste the content
5. Publish the page

## Testing

After deployment:

1. Visit the page with the calculator
2. Test with default values (should show ~\$103K final value for \$500/month at 10% for 10 years)
3. Test export functionality
4. Test advanced options

## Customization

You can customize the calculator by modifying the shortcode parameters:

\`\`\`
[sip_calculator monthly_investment="1000" return_rate="12" investment_period="20"]
\`\`\`

## Troubleshooting

- **Calculator not loading**: Check if plugin is activated
- **Styles not working**: Clear browser cache and WordPress cache
- **Shortcode not working**: Make sure you're using the correct shortcode format

## Support

For issues or questions, check the plugin's README.md file or contact the developer.
EOF

    print_success "Deployment instructions created: SIP_CALCULATOR_DEPLOYMENT_INSTRUCTIONS.md"
}

# Main deployment function
main() {
    echo ""
    print_status "Starting SIP Calculator deployment process..."

    check_files
    get_credentials
    test_connection
    create_plugin_structure
    create_zip
    create_instructions

    echo ""
    print_success "🎉 Deployment package ready!"
    echo ""
    echo "Next steps:"
    echo "1. Upload sip-calculator.zip to WordPress via Plugins → Add New → Upload Plugin"
    echo "2. Activate the plugin"
    echo "3. Create a new page with shortcode: [sip_calculator]"
    echo "4. Test the calculator functionality"
    echo ""
    echo "See SIP_CALCULATOR_DEPLOYMENT_INSTRUCTIONS.md for detailed instructions"
}

# Run main function
main
EOF