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
