// Minimal utilities for retirement calculator
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

class AnimationManager {
    scrollTo(element, offset = 0) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;
        window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
        });
    }
    
    animateNumber(element, start, end, duration = 1000, formatter = null) {
        const startTime = performance.now();
        const difference = end - start;
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = start + (difference * easeOutQuart);
            element.textContent = formatter ? formatter(current) : Math.round(current);
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    }
}

class ValidationManager {
    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        
        if (field.hasAttribute("required") && !value) {
            return "This field is required";
        }
        
        if (type === "number") {
            const numValue = parseFloat(value);
            if (isNaN(numValue)) {
                return "Please enter a valid number";
            }
            if (field.hasAttribute("min") && numValue < parseFloat(field.getAttribute("min"))) {
                return "Value must be at least " + field.getAttribute("min");
            }
        }
        
        return null;
    }
}

class ExportManager {
    exportToCSV(data, filename) {
        let csv = "";
        if (data.length > 0) {
            csv += Object.keys(data[0]).join(",") + "\n";
            data.forEach(row => {
                csv += Object.values(row).join(",") + "\n";
            });
        }
        this.downloadFile(csv, filename + ".csv", "text/csv");
    }
    
    exportToPDF(content, filename) {
        // Simple PDF export using browser print
        const printWindow = window.open("", "_blank");
        printWindow.document.write(content);
        printWindow.document.close();
        printWindow.print();
    }
    
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

class ChartManager {
    createPlaceholderChart(containerId, title) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = "<div style=\"padding: 20px; text-align: center; border: 1px dashed #ccc; color: #666;\">Chart: " + title + "</div>";
        }
    }
    
    clearCharts() {
        // Clear any chart containers
    }
}

class UIManager {
    showAlert(message, type = "info") {
        alert(message);
    }
}

class StorageManager {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.warn("Storage not available");
        }
    }
    
    get(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            return null;
        }
    }
}

// Number formatting utility
class NumberFormatter {
    static formatCurrency(num) {
        return "$" + num.toLocaleString("en-US", { maximumFractionDigits: 0 });
    }
}
