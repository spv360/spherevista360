#!/bin/bash

# Create Compound Interest Calculator page in WordPress
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="JK"

echo "Creating Compound Interest Calculator page"
read -s -p "Enter WordPress password for user '$WP_USERNAME': " WP_PASSWORD
echo ""

AUTH_HEADER="Authorization: Basic $(echo -n "$WP_USERNAME:$WP_PASSWORD" | base64)"

# HTML content for the compound interest calculator page
PAGE_CONTENT='<!-- wp:html -->
<div class="compound-interest-calculator-container" style="max-width: 1200px; margin: 0 auto; padding: 20px; font-family: '\''Segoe UI'\'', Tahoma, Geneva, Verdana, sans-serif;">
    <div class="calculator-header" style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2c3e50; margin-bottom: 10px; font-size: 2.5em;">📈 Compound Interest Calculator</h1>
        <p style="color: #7f8c8d; font-size: 1.1em; margin-bottom: 20px;">
            Calculate the power of compound interest and plan your investment growth
        </p>
        <div class="calculator-badges" style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 20px;">
            <span style="background: #3498db; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em;">Free Tool</span>
            <span style="background: #27ae60; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em;">No Registration</span>
            <span style="background: #e74c3c; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em;">Instant Results</span>
        </div>
    </div>

    <div class="calculator-inputs" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px;">
        <div class="input-group" style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">💰 Initial Investment</h3>
            <input type="number" id="principal" class="input-field" placeholder="Enter initial amount" min="0" step="100" style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; margin-bottom: 10px; transition: border-color 0.3s;">
            <small style="color: #7f8c8d;">Your starting investment amount</small>
        </div>

        <div class="input-group" style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">📊 Annual Interest Rate</h3>
            <input type="number" id="rate" class="input-field" placeholder="7.0" min="0" max="50" step="0.1" style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; margin-bottom: 10px; transition: border-color 0.3s;">
            <small style="color: #7f8c8d;">Expected annual return (e.g., 7% = 7.0)</small>
        </div>

        <div class="input-group" style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">⏰ Investment Period</h3>
            <input type="number" id="years" class="input-field" placeholder="10" min="1" max="50" style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; margin-bottom: 10px; transition: border-color 0.3s;">
            <small style="color: #7f8c8d;">Number of years to invest</small>
        </div>

        <div class="input-group" style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🔄 Compounding Frequency</h3>
            <select id="frequency" class="input-field" style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; margin-bottom: 10px; transition: border-color 0.3s;">
                <option value="1">Annually</option>
                <option value="2">Semi-annually</option>
                <option value="4">Quarterly</option>
                <option value="12" selected>Monthly</option>
                <option value="365">Daily</option>
            </select>
            <small style="color: #7f8c8d;">How often interest is compounded</small>
        </div>

        <div class="input-group" style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">💵 Monthly Contribution</h3>
            <input type="number" id="monthly" class="input-field" placeholder="0" min="0" step="10" style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; margin-bottom: 10px; transition: border-color 0.3s;">
            <small style="color: #7f8c8d;">Additional monthly investment (optional)</small>
        </div>

        <div class="input-group" style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">📉 Inflation Rate</h3>
            <input type="number" id="inflation" class="input-field" placeholder="3.0" min="0" max="20" step="0.1" style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; margin-bottom: 10px; transition: border-color 0.3s;">
            <small style="color: #7f8c8d;">Annual inflation rate (optional)</small>
        </div>
    </div>

    <div id="error-message" class="error-message" style="background: #e74c3c; color: white; padding: 15px; border-radius: 8px; margin: 20px 0; display: none;"></div>

    <button id="calculate-btn" class="calculate-btn" style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); color: white; border: none; padding: 15px 30px; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; width: 100%; margin: 20px 0;">Calculate Compound Interest</button>

    <div id="results-section" class="results-section" style="background: #f8f9fa; border-radius: 10px; padding: 25px; margin-top: 30px; display: none;">
        <div class="results-header" style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #2c3e50; margin-bottom: 10px;">Investment Results</h2>
            <p>Your compound interest calculation summary</p>
        </div>

        <div class="results-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div class="result-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div class="result-label" style="color: #7f8c8d; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Future Value</div>
                <div id="future-value" class="result-value" style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">$0.00</div>
            </div>

            <div class="result-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div class="result-label" style="color: #7f8c8d; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Total Contributions</div>
                <div id="total-contributions" class="result-value" style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">$0.00</div>
            </div>

            <div class="result-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div class="result-label" style="color: #7f8c8d; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Total Interest Earned</div>
                <div id="total-interest" class="result-value" style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">$0.00</div>
            </div>

            <div class="result-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div class="result-label" style="color: #7f8c8d; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Effective Annual Rate</div>
                <div id="effective-rate" class="result-value" style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">0.00%</div>
            </div>
        </div>

        <div id="inflation-results" style="display: none;">
            <div class="results-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
                <div class="result-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                    <div class="result-label" style="color: #7f8c8d; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Inflation-Adjusted Value</div>
                    <div id="inflation-adjusted" class="result-value" style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">$0.00</div>
                </div>

                <div class="result-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                    <div class="result-label" style="color: #7f8c8d; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Real Return</div>
                    <div id="real-return" class="result-value" style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">$0.00</div>
                </div>
            </div>
        </div>

        <div class="yearly-breakdown" style="margin-top: 30px;">
            <div class="breakdown-header" style="text-align: center; margin-bottom: 20px;">
                <h3 style="color: #2c3e50;">Year-by-Year Growth Breakdown</h3>
                <p>Detailed view of your investment growth over time</p>
            </div>

            <div class="table-container" style="overflow-x: auto;">
                <table id="breakdown-table" class="breakdown-table" style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <thead>
                        <tr>
                            <th style="padding: 12px; background: #2c3e50; color: white; font-weight: 600; text-align: center;">Year</th>
                            <th style="padding: 12px; background: #2c3e50; color: white; font-weight: 600; text-align: center;">Starting Balance</th>
                            <th style="padding: 12px; background: #2c3e50; color: white; font-weight: 600; text-align: center;">Contributions</th>
                            <th style="padding: 12px; background: #2c3e50; color: white; font-weight: 600; text-align: center;">Interest Earned</th>
                            <th style="padding: 12px; background: #2c3e50; color: white; font-weight: 600; text-align: center;">Ending Balance</th>
                            <th style="padding: 12px; background: #2c3e50; color: white; font-weight: 600; text-align: center;">Inflation Adjusted</th>
                        </tr>
                    </thead>
                    <tbody id="breakdown-body">
                    </tbody>
                </table>
            </div>
        </div>

        <div class="export-buttons" style="text-align: center; margin-top: 20px;">
            <button id="export-json" class="export-btn" style="background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 0 5px; font-size: 14px;">Export JSON</button>
            <button id="export-csv" class="export-btn" style="background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 0 5px; font-size: 14px;">Export CSV</button>
        </div>
    </div>

    <div class="info-section" style="background: white; border-radius: 10px; padding: 25px; margin-top: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">About This Calculator</h3>
        <p style="color: #555; line-height: 1.6; margin-bottom: 15px;">
            This compound interest calculator helps you understand the power of compounding and plan your investment growth. It includes options for regular contributions and inflation adjustment to provide realistic projections.
        </p>
        <div class="features" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;">
            <div class="feature" style="padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
                <h4 style="margin: 0 0 8px 0; color: #2c3e50;">📊 Accurate Calculations</h4>
                <p style="margin: 0; color: #7f8c8d; font-size: 0.9em;">Uses standard compound interest formulas with support for different compounding frequencies</p>
            </div>

            <div class="feature" style="padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
                <h4 style="margin: 0 0 8px 0; color: #2c3e50;">💰 Regular Contributions</h4>
                <p style="margin: 0; color: #7f8c8d; font-size: 0.9em;">Factor in monthly investments to see how consistent saving accelerates growth</p>
            </div>

            <div class="feature" style="padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
                <h4 style="margin: 0 0 8px 0; color: #2c3e50;">📉 Inflation Adjustment</h4>
                <p style="margin: 0; color: #7f8c8d; font-size: 0.9em;">Account for inflation to understand your real purchasing power</p>
            </div>

            <div class="feature" style="padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
                <h4 style="margin: 0 0 8px 0; color: #2c3e50;">📈 Year-by-Year Breakdown</h4>
                <p style="margin: 0; color: #7f8c8d; font-size: 0.9em;">Detailed annual view of your investment growth and contributions</p>
            </div>
        </div>
    </div>
</div>

<script>
class CompoundInterestCalculator {
    constructor() {
        this.results = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const calculateBtn = document.getElementById('\''calculate-btn'\'');
        const exportJsonBtn = document.getElementById('\''export-json'\'');
        const exportCsvBtn = document.getElementById('\''export-csv'\'');

        calculateBtn.addEventListener('\''click'\'', () => this.calculate());
        exportJsonBtn.addEventListener('\''click'\'', () => this.exportJSON());
        exportCsvBtn.addEventListener('\''click'\'', () => this.exportCSV());
    }

    calculate() {
        const principal = parseFloat(document.getElementById('\''principal'\'').value);
        const rate = parseFloat(document.getElementById('\''rate'\'').value) / 100;
        const years = parseInt(document.getElementById('\''years'\'').value);
        const frequency = parseInt(document.getElementById('\''frequency'\'').value);
        const monthly = parseFloat(document.getElementById('\''monthly'\'').value) || 0;
        const inflation = parseFloat(document.getElementById('\''inflation'\'').value) || 0;

        // Validation
        if (!principal || principal < 0) {
            this.showError('\''Please enter a valid initial investment amount'\'');
            return;
        }

        if (!rate || rate < 0 || rate > 0.5) {
            this.showError('\''Please enter a valid interest rate between 0% and 50%'\'');
            return;
        }

        if (!years || years < 1 || years > 50) {
            this.showError('\''Please enter investment period between 1 and 50 years'\'');
            return;
        }

        this.hideError();
        this.results = this.calculateCompoundInterest(principal, rate, years, frequency, monthly, inflation / 100);
        this.displayResults();
    }

    calculateCompoundInterest(principal, annualRate, years, compoundingFreq, monthlyContribution, inflationRate) {
        const periodicRate = annualRate / compoundingFreq;
        const totalPeriods = years * compoundingFreq;

        // Calculate future value of principal
        let futureValue = principal * Math.pow(1 + periodicRate, totalPeriods);

        // Add future value of regular contributions
        if (monthlyContribution > 0) {
            const monthlyRate = annualRate / 12;
            const totalMonths = years * 12;
            futureValue += monthlyContribution * (Math.pow(1 + monthlyRate, totalMonths) - 1) / monthlyRate;
        }

        const totalContributions = principal + (monthlyContribution * years * 12);
        const totalInterest = futureValue - totalContributions;
        const effectiveAnnualRate = Math.pow(1 + periodicRate, compoundingFreq) - 1;

        // Inflation adjustment
        let inflationAdjustedValue = futureValue;
        let realReturn = totalInterest;

        if (inflationRate > 0) {
            inflationAdjustedValue = futureValue / Math.pow(1 + inflationRate, years);
            realReturn = inflationAdjustedValue - totalContributions;
        }

        // Generate yearly breakdown
        const yearlyBreakdown = this.generateYearlyBreakdown(
            principal, annualRate, years, compoundingFreq, monthlyContribution, inflationRate
        );

        return {
            principal,
            annualRate,
            effectiveAnnualRate,
            years,
            compoundingFreq,
            monthlyContribution,
            totalContributions,
            futureValue,
            totalInterest,
            inflationRate,
            inflationAdjustedValue,
            realReturn,
            yearlyBreakdown
        };
    }

    generateYearlyBreakdown(principal, annualRate, years, compoundingFreq, monthlyContribution, inflationRate) {
        const breakdown = [];
        let currentPrincipal = principal;
        const periodicRate = annualRate / compoundingFreq;
        const periodsPerYear = compoundingFreq;

        for (let year = 1; year <= years; year++) {
            const yearStartValue = currentPrincipal;

            // Add yearly contributions
            const yearlyContributions = monthlyContribution * 12;
            currentPrincipal += yearlyContributions;

            // Apply compound interest for the year
            for (let i = 0; i < periodsPerYear; i++) {
                currentPrincipal *= (1 + periodicRate);
            }

            const yearEndValue = currentPrincipal;
            const yearInterest = yearEndValue - yearStartValue - yearlyContributions;

            // Inflation adjustment
            let inflationAdjustedValue = yearEndValue;
            if (inflationRate > 0) {
                const inflationFactor = Math.pow(1 + inflationRate, year);
                inflationAdjustedValue = yearEndValue / inflationFactor;
            }

            breakdown.push({
                year,
                startingBalance: yearStartValue,
                contributions: yearlyContributions,
                interestEarned: yearInterest,
                endingBalance: yearEndValue,
                inflationAdjustedValue
            });
        }

        return breakdown;
    }

    displayResults() {
        const results = this.results;
        const resultsSection = document.getElementById('\''results-section'\'');

        // Main results
        document.getElementById('\''future-value'\'').textContent = this.formatCurrency(results.futureValue);
        document.getElementById('\''total-contributions'\'').textContent = this.formatCurrency(results.totalContributions);
        document.getElementById('\''total-interest'\'').textContent = this.formatCurrency(results.totalInterest);
        document.getElementById('\''effective-rate'\'').textContent = (results.effectiveAnnualRate * 100).toFixed(2) + '\''%'\'';

        // Inflation results
        if (results.inflationRate > 0) {
            document.getElementById('\''inflation-results'\'').style.display = '\''block'\'';
            document.getElementById('\''inflation-adjusted'\'').textContent = this.formatCurrency(results.inflationAdjustedValue);
            document.getElementById('\''real-return'\'').textContent = this.formatCurrency(results.realReturn);
        } else {
            document.getElementById('\''inflation-results'\'').style.display = '\''none'\'';
        }

        // Yearly breakdown table
        this.displayYearlyBreakdown();

        resultsSection.style.display = '\''block'\'';
        resultsSection.scrollIntoView({ behavior: '\''smooth'\'' });
    }

    displayYearlyBreakdown() {
        const tbody = document.getElementById('\''breakdown-body'\'');
        tbody.innerHTML = '\'''\'';

        this.results.yearlyBreakdown.forEach(year => {
            const row = document.createElement('\''tr'\'');
            row.innerHTML = `
                <td>${year.year}</td>
                <td>${this.formatCurrency(year.startingBalance)}</td>
                <td>${this.formatCurrency(year.contributions)}</td>
                <td>${this.formatCurrency(year.interestEarned)}</td>
                <td>${this.formatCurrency(year.endingBalance)}</td>
                <td>${this.formatCurrency(year.inflationAdjustedValue)}</td>
            `;
            tbody.appendChild(row);
        });
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('\''en-US'\'', {
            style: '\''currency'\'',
            currency: '\''USD'\'',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    showError(message) {
        const errorDiv = document.getElementById('\''error-message'\'');
        errorDiv.textContent = message;
        errorDiv.style.display = '\''block'\'';
    }

    hideError() {
        document.getElementById('\''error-message'\'').style.display = '\''none'\'';
    }

    exportJSON() {
        if (!this.results) return;

        const dataStr = JSON.stringify(this.results, null, 2);
        const dataBlob = new Blob([dataStr], { type: '\''application/json'\'' });
        this.downloadBlob(dataBlob, '\''compound_interest_results.json'\'');
    }

    exportCSV() {
        if (!this.results) return;

        let csv = '\''Year,Starting Balance,Contributions,Interest Earned,Ending Balance,Inflation Adjusted Value\n'\'';

        this.results.yearlyBreakdown.forEach(year => {
            csv += `${year.year},${year.startingBalance},${year.contributions},${year.interestEarned},${year.endingBalance},${year.inflationAdjustedValue}\n`;
        });

        const dataBlob = new Blob([csv], { type: '\''text/csv'\'' });
        this.downloadBlob(dataBlob, '\''compound_interest_breakdown.csv'\'');
    }

    downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('\''a'\'');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Initialize calculator when page loads
document.addEventListener('\''DOMContentLoaded'\'', () => {
    new CompoundInterestCalculator();
});
</script>
<!-- /wp:html -->'

# Create the page
JSON_PAYLOAD=$(cat << EOF
{
  "title": "Compound Interest Calculator",
  "content": "$(echo "$PAGE_CONTENT" | sed 's/"/\\"/g' | sed 's/$/\\n/g' | tr -d '\n')",
  "status": "publish",
  "slug": "compound-interest-calculator"
}
EOF
)

RESPONSE=$(curl -s -X POST "$WP_SITE_URL/wp-json/wp/v2/pages" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d "$JSON_PAYLOAD")

if echo "$RESPONSE" | grep -q '"id":'; then
  echo "✅ Compound Interest Calculator page created successfully!"
  echo "Page URL: https://spherevista360.com/compound-interest-calculator/"
else
  echo "❌ Failed to create Compound Interest Calculator page. Response: $RESPONSE"
  exit 1
fi