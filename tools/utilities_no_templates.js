/**
 * SPHEREVISTA360 FINANCIAL TOOLS UTILITIES
 * A comprehensive JavaScript utility library for financial calculators
 */

class SphereVistaTools {
    constructor() {
        this.animations = new AnimationManager();
        this.validation = new ValidationManager();
        this.export = new ExportManager();
        this.charts = new ChartManager();
        this.ui = new UIManager();
        this.storage = new StorageManager();
    }
}

/**
 * ANIMATION MANAGER
 * Handles smooth animations and transitions
 */
class AnimationManager {
    constructor() {
        this.observers = new Map();
    }

    // Smooth scroll to element
    scrollTo(element, offset = 0) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }

    // Animate number counting
    animateNumber(element, start, end, duration = 1000, formatter = null) {
        const startTime = performance.now();
        const difference = end - start;

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = start + (difference * easeOutQuart);

            element.textContent = formatter ? formatter(current) : Math.round(current);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    // Fade in element
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';

        const start = performance.now();

        const fade = (timestamp) => {
            const elapsed = timestamp - start;
            const progress = elapsed / duration;

            element.style.opacity = Math.min(progress, 1);

            if (progress < 1) {
                requestAnimationFrame(fade);
            }
        };

        requestAnimationFrame(fade);
    }

    // Slide in element from bottom
    slideInUp(element, duration = 400) {
        element.style.transform = 'translateY(30px)';
        element.style.opacity = '0';
        element.style.display = 'block';

        const start = performance.now();

        const slide = (timestamp) => {
            const elapsed = timestamp - start;
            const progress = elapsed / duration;
            const easeOut = 1 - Math.pow(1 - progress, 3);

            element.style.transform = "translateY(" + (30 * (1 - easeOut)) + "px)";
            element.style.opacity = Math.min(easeOut, 1);

            if (progress < 1) {
                requestAnimationFrame(slide);
            }
        };

        requestAnimationFrame(slide);
    }

    // Add loading state to button
    setLoading(button, loading = true) {
        if (loading) {
            button.disabled = true;
            button.innerHTML = '<span class="loading-spinner"></span> Calculating...';
            button.classList.add('btn-loading');
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || 'Calculate';
            button.classList.remove('btn-loading');
        }
    }
}

/**
 * VALIDATION MANAGER
 * Handles input validation and error display
 */
class ValidationManager {
    constructor() {
        this.rules = {
            required: (value) => value !== '' && value !== null && value !== undefined,
            number: (value) => !isNaN(value) && !isNaN(parseFloat(value)),
            positive: (value) => parseFloat(value) > 0,
            integer: (value) => Number.isInteger(parseFloat(value)),
            range: (value, min, max) => parseFloat(value) >= min && parseFloat(value) <= max,
            email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
        };
    }

    // Validate single field
    validateField(field, rules) {
        const value = field.value.trim();
        const errors = [];

        for (const rule of rules) {
            const [ruleName, ...params] = rule.split(':');
            const validator = this.rules[ruleName];

            if (!validator) continue;

            const isValid = validator(value, ...params);
            if (!isValid) {
                errors.push(this.getErrorMessage(ruleName, params, field));
            }
        }

        this.showFieldErrors(field, errors);
        return errors.length === 0;
    }

    // Validate entire form
    validateForm(form, rules) {
        let isValid = true;
        const errors = {};

        for (const [fieldName, fieldRules] of Object.entries(rules)) {
            const field = form.querySelector(`[name="${fieldName}"]`) || form.querySelector(`#${fieldName}`);
            if (!field) continue;

            const fieldValid = this.validateField(field, fieldRules);
            if (!fieldValid) {
                isValid = false;
                errors[fieldName] = true;
            }
        }

        return { isValid, errors };
    }

    // Show field errors
    showFieldErrors(field, errors) {
        // Remove existing error messages
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        // Update field styling
        field.classList.toggle('error', errors.length > 0);

        if (errors.length > 0) {
            // Add error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.textContent = errors[0];
            field.parentNode.appendChild(errorDiv);
        }
    }

    // Get error message for rule
    getErrorMessage(ruleName, params, field) {
        const messages = {
            required: this.getFieldLabel(field) + " is required",
            number: this.getFieldLabel(field) + " must be a valid number",
            positive: this.getFieldLabel(field) + " must be greater than 0",
            integer: `${this.getFieldLabel(field)} must be a whole number`,
            range: `${this.getFieldLabel(field)} must be between ${params[0]} and ${params[1]}`,
            email: 'Please enter a valid email address'
        };

        return messages[ruleName] || 'Invalid value';
    }

    // Get field label
    getFieldLabel(field) {
        const label = field.parentNode.querySelector('label');
        return label ? label.textContent.replace('*', '').trim() : 'This field';
    }

    // Clear all errors
    clearErrors(form) {
        const errorElements = form.querySelectorAll('.field-error');
        errorElements.forEach(el => el.remove());

        const errorFields = form.querySelectorAll('.error');
        errorFields.forEach(field => field.classList.remove('error'));
    }
}

/**
 * EXPORT MANAGER
 * Handles data export functionality
 */
class ExportManager {
    constructor() {
        this.formats = {
            json: this.exportJSON.bind(this),
            csv: this.exportCSV.bind(this),
            pdf: this.exportPDF.bind(this)
        };
    }

    // Export data in specified format
    export(data, format = 'json', filename = 'data') {
        const exporter = this.formats[format];
        if (!exporter) {
            throw new Error(`Unsupported export format: ${format}`);
        }

        return exporter(data, filename);
    }

    // Export as JSON
    exportJSON(data, filename) {
        const jsonString = JSON.stringify(data, null, 2);
        this.downloadFile(jsonString, `${filename}.json`, 'application/json');
    }

    // Export as CSV
    exportCSV(data, filename) {
        if (!Array.isArray(data)) {
            data = [data];
        }

        if (data.length === 0) return;

        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => {
                const value = row[header];
                // Escape commas and quotes in CSV
                if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                    return `"${value.replace(/"/g, '""')}"`;
                }
                return value;
            }).join(','))
        ].join('\n');

        this.downloadFile(csvContent, `${filename}.csv`, 'text/csv');
    }

    // Export as PDF (placeholder - would need pdf.js or similar)
    exportPDF(data, filename) {
        console.warn('PDF export not implemented. Consider using a library like jsPDF.');
        // Implementation would go here
    }

    // Download file helper
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(url);
    }

    // Share data (if Web Share API is available)
    async share(data, title = 'Financial Calculator Results') {
        if (!navigator.share) {
            console.warn('Web Share API not supported');
            return false;
        }

        try {
            const jsonData = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonData], { type: 'application/json' });
            const file = new File([blob], 'calculator-results.json', { type: 'application/json' });

            await navigator.share({
                title,
                files: [file]
            });

            return true;
        } catch (error) {
            console.error('Error sharing:', error);
            return false;
        }
    }
}

/**
 * CHART MANAGER
 * Handles chart creation and management
 */
class ChartManager {
    constructor() {
        this.charts = new Map();
        this.colors = {
            primary: '#2563eb',
            secondary: '#64748b',
            success: '#059669',
            warning: '#d97706',
            danger: '#dc2626',
            info: '#0891b2'
        };
    }

    // Create line chart
    createLineChart(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time Period'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        };

        const chartOptions = { ...defaultOptions, ...options };

        // This would use Chart.js in a real implementation
        console.log('Chart creation would happen here with Chart.js', { canvasId, data, chartOptions });

        // Placeholder for chart creation
        this.charts.set(canvasId, { type: 'line', data, options: chartOptions });

        return {
            update: (newData) => this.updateChart(canvasId, newData),
            destroy: () => this.destroyChart(canvasId)
        };
    }

    // Create bar chart
    createBarChart(canvasId, data, options = {}) {
        // Similar to line chart but for bar charts
        console.log('Bar chart creation would happen here', { canvasId, data, options });
        this.charts.set(canvasId, { type: 'bar', data, options });
    }

    // Update existing chart
    updateChart(canvasId, newData) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.data = newData;
            console.log('Chart updated:', canvasId, newData);
        }
    }

    // Destroy chart
    destroyChart(canvasId) {
        this.charts.delete(canvasId);
        console.log('Chart destroyed:', canvasId);
    }

    // Create placeholder chart visualization
    createPlaceholderChart(containerId, title = 'Chart Visualization') {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="chart-placeholder">
                <div class="icon">📊</div>
                <h4>${title}</h4>
                <p>Interactive chart visualization would appear here.<br>
                <small>Requires Chart.js library for full functionality</small></p>
            </div>
        `;
    }
}

/**
 * UI MANAGER
 * Handles UI interactions and state management
 */
class UIManager {
    constructor() {
        this.tabs = new Map();
        this.modals = new Map();
        this.tooltips = new Map();
        this.init();
    }

    init() {
        this.initTabs();
        this.initTooltips();
        this.initModals();
    }

    // Initialize tab functionality
    initTabs() {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const tabId = btn.dataset.tab;
                this.showTab(tabId);
            });
        });
    }

    // Show specific tab
    showTab(tabId) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Remove active class from all buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected tab
        const tabContent = document.getElementById(tabId);
        const tabButton = document.querySelector(`[data-tab="${tabId}"]`);

        if (tabContent) {
            tabContent.classList.add('active');
        }

        if (tabButton) {
            tabButton.classList.add('active');
        }
    }

    // Initialize tooltips
    initTooltips() {
        // Tooltips are handled via CSS hover states
        // This could be enhanced with JavaScript for better control
    }

    // Initialize modals
    initModals() {
        // Modal functionality can be added here
    }

    // Show alert/notification
    showAlert(message, type = 'info', duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <span class="alert-icon">
                ${this.getAlertIcon(type)}
            </span>
            <span>${message}</span>
        `;

        // Insert at top of container
        const container = document.querySelector('.tool-content') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                alertDiv.remove();
            }, duration);
        }

        return alertDiv;
    }

    // Get alert icon based on type
    getAlertIcon(type) {
        const icons = {
            error: '❌',
            success: '✅',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    // Show loading overlay
    showLoading(message = 'Calculating...') {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            ">
                <div style="
                    background: white;
                    padding: 2rem;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                ">
                    <div class="loading-spinner" style="
                        width: 40px;
                        height: 40px;
                        border: 4px solid #f3f3f3;
                        border-top: 4px solid #2563eb;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin: 0 auto 1rem;
                    "></div>
                    <p style="margin: 0; color: #374151; font-weight: 500;">${message}</p>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);
        return overlay;
    }

    // Hide loading overlay
    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

/**
 * STORAGE MANAGER
 * Handles local storage for user preferences and data
 */
class StorageManager {
    constructor() {
        this.prefix = 'spherevista_';
    }

    // Set item in localStorage
    set(key, value) {
        try {
            const serializedValue = JSON.stringify(value);
            localStorage.setItem(this.prefix + key, serializedValue);
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    }

    // Get item from localStorage
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(this.prefix + key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Storage error:', error);
            return defaultValue;
        }
    }

    // Remove item from localStorage
    remove(key) {
        try {
            localStorage.removeItem(this.prefix + key);
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    }

    // Clear all SphereVista data
    clear() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(this.prefix)) {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    }

    // Save calculator state
    saveCalculatorState(calculatorId, state) {
        return this.set(`calc_${calculatorId}_state`, {
            data: state,
            timestamp: new Date().toISOString()
        });
    }

    // Load calculator state
    loadCalculatorState(calculatorId) {
        const state = this.get(`calc_${calculatorId}_state`);
        return state ? state.data : null;
    }
}

/**
 * NUMBER FORMATTER
 * Utility for formatting numbers and currencies
 */
class NumberFormatter {
    static formatCurrency(amount, currency = 'USD', locale = 'en-US') {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    static formatNumber(number, decimals = 2, locale = 'en-US') {
        return new Intl.NumberFormat(locale, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(number);
    }

    static formatPercent(value, decimals = 2) {
        return `${(value * 100).toFixed(decimals)}%`;
    }

    static compactNumber(number) {
        return new Intl.NumberFormat('en-US', {
            notation: 'compact',
            compactDisplay: 'short'
        }).format(number);
    }
}

/**
 * DATE UTILITIES
 * Helper functions for date operations
 */
class DateUtils {
    static formatDate(date, format = 'short') {
        const options = {
            short: { year: 'numeric', month: 'short', day: 'numeric' },
            long: { year: 'numeric', month: 'long', day: 'numeric' },
            full: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
        };

        return new Intl.DateTimeFormat('en-US', options[format]).format(date);
    }

    static addYears(date, years) {
        const result = new Date(date);
        result.setFullYear(result.getFullYear() + years);
        return result;
    }

    static addMonths(date, months) {
        const result = new Date(date);
        result.setMonth(result.getMonth() + months);
        return result;
    }

    static getYearDiff(startDate, endDate) {
        return endDate.getFullYear() - startDate.getFullYear();
    }
}

// Global instance
const sphereVistaTools = new SphereVistaTools();

// Export for use in other scripts
window.SphereVistaTools = SphereVistaTools;
window.NumberFormatter = NumberFormatter;
window.DateUtils = DateUtils;