#!/bin/bash

# WordPress Duplicate Files Cleanup Script
# Moves old/duplicate files to backup folder
# Keeps only the latest, most functional versions

echo "═══════════════════════════════════════════════════════════════════════════"
echo "  🧹 WORDPRESS CALCULATOR FILES CLEANUP"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Create backup directory with timestamp
BACKUP_DIR="backup_old_versions_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Creating backup directory: $BACKUP_DIR"
echo ""

# Function to move file to backup
move_to_backup() {
    local file="$1"
    local reason="$2"
    
    if [ -f "$file" ]; then
        # Create subdirectory structure in backup
        local dir=$(dirname "$file")
        mkdir -p "$BACKUP_DIR/$dir"
        
        echo "  📦 Moving: $file"
        echo "     Reason: $reason"
        mv "$file" "$BACKUP_DIR/$file"
        echo "     ✅ Backed up to: $BACKUP_DIR/$file"
        echo ""
    fi
}

echo "🗑️  REMOVING DUPLICATE FILES..."
echo "─────────────────────────────────────────────────────────────────────────"
echo ""

# Root level duplicates
echo "1️⃣  Root Level Duplicates:"
move_to_backup "clean_calculator.html" "Old version - superseded by tools/calculators versions"
move_to_backup "improved_calculator.html" "Development version - superseded by final versions"
move_to_backup "sip_calculator_wordpress_page.html" "Old version - superseded by sip_calculator_new.html"

# Superseded versions in tools
echo ""
echo "2️⃣  Superseded Calculator Versions:"
move_to_backup "tools/calculators/sip_calculator.html" "Old version - superseded by sip_calculator_new.html"
move_to_backup "tools/calculators/us_tax_calculator/tax-withholding.html" "Old version - superseded by tax-withholding-new.html"
move_to_backup "tools/calculators/us_tax_calculator/retirement-planner-estimator.html" "Old version with broken layouts - superseded by retirement-planner-fixed.html"

# Upload package duplicates
echo ""
echo "3️⃣  Upload Package Duplicates:"
move_to_backup "upload_package/loan_emi_calculator.html" "Backup copy - superseded by tools/calculators/loan_emi_calculator/"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "  📊 CLEANUP SUMMARY"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Count files in backup
backup_count=$(find "$BACKUP_DIR" -type f -name "*.html" 2>/dev/null | wc -l)
echo "✅ Files moved to backup: $backup_count"
echo "📁 Backup location: $BACKUP_DIR"
echo ""

# List remaining calculator files
echo "📋 REMAINING CALCULATOR FILES (ORGANIZED):"
echo "─────────────────────────────────────────────────────────────────────────"
echo ""

echo "🎯 US Tax Calculator Suite:"
ls -lh tools/calculators/us_tax_calculator/*.html 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'

echo ""
echo "💰 Investment Calculators:"
[ -f "tools/calculators/sip_calculator_new.html" ] && ls -lh tools/calculators/sip_calculator_new.html | awk '{print "  " $9 " (" $5 ")"}'
[ -f "tools/calculators/compound_interest_calculator/compound_interest_calculator.html" ] && ls -lh tools/calculators/compound_interest_calculator/compound_interest_calculator.html | awk '{print "  " $9 " (" $5 ")"}'

echo ""
echo "🏠 Loan Calculators:"
[ -f "tools/calculators/loan_emi_calculator/loan_emi_calculator.html" ] && ls -lh tools/calculators/loan_emi_calculator/loan_emi_calculator.html | awk '{print "  " $9 " (" $5 ")"}'

echo ""
echo "🏖️  Retirement Planner:"
[ -f "retirement-planner-fixed.html" ] && ls -lh retirement-planner-fixed.html | awk '{print "  " $9 " (" $5 ")"}'

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "  ✅ CLEANUP COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "Next Steps:"
echo "  1. Review backed up files in: $BACKUP_DIR"
echo "  2. Clean up duplicate WordPress pages manually via admin panel"
echo "  3. Deploy updated calculators using deployment scripts"
echo "  4. Clear WordPress cache after deployment"
echo ""
echo "📖 See WORDPRESS_CLEANUP_PLAN.md for detailed instructions"
echo ""

# Create archive of backup
echo "📦 Creating backup archive..."
tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR" 2>/dev/null && echo "✅ Archive created: ${BACKUP_DIR}.tar.gz"
echo ""

# Create cleanup report
cat > "${BACKUP_DIR}/CLEANUP_REPORT.txt" << EOF
WordPress Calculator Cleanup Report
Generated: $(date)

Files Moved to Backup:
=====================

Root Level Duplicates:
- clean_calculator.html (Old version)
- improved_calculator.html (Development version)
- sip_calculator_wordpress_page.html (Old version)

Superseded Versions:
- tools/calculators/sip_calculator.html (Old version)
- tools/calculators/us_tax_calculator/tax-withholding.html (Old version)
- tools/calculators/us_tax_calculator/retirement-planner-estimator.html (Broken version)

Upload Package:
- upload_package/loan_emi_calculator.html (Backup copy)

Total Files Backed Up: $backup_count

Files Kept in Production:
=========================

US Tax Calculator Suite (8 files):
- federal-income-tax.html
- state-income-tax.html
- capital-gains-tax.html
- self-employment-tax.html
- retirement-tax.html
- tax-withholding-new.html
- lump-sum-investment.html
- index.html

Investment Calculators (2 files):
- sip_calculator_new.html
- compound_interest_calculator.html

Loan Calculator (1 file):
- loan_emi_calculator.html

Retirement Planner (1 file):
- retirement-planner-fixed.html

Total Production Files: 12

Backup Location: $BACKUP_DIR
Backup Archive: ${BACKUP_DIR}.tar.gz

Next Steps:
===========
1. Verify remaining files work correctly
2. Clean up WordPress admin pages (see WORDPRESS_CLEANUP_PLAN.md)
3. Deploy updated calculators
4. Test all functionality
5. Clear caches

EOF

echo "📄 Cleanup report saved: ${BACKUP_DIR}/CLEANUP_REPORT.txt"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
