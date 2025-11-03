#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════════════"
echo "  📊 CALCULATOR & TOOL FILES ANALYSIS"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

echo "🔍 Searching for all calculator HTML files..."
echo ""

# Find all calculator-related HTML files
echo "1️⃣  US TAX CALCULATORS:"
echo "─────────────────────────────────────────────────────────────────────────"
find tools/calculators/us_tax_calculator -name "*.html" 2>/dev/null | while read file; do
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    modified=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t"%Y-%m-%d" "$file" 2>/dev/null)
    echo "  📄 $(basename "$file")"
    echo "     Path: $file"
    echo "     Size: $size bytes"
    echo "     Modified: $modified"
    echo ""
done

echo ""
echo "2️⃣  INVESTMENT CALCULATORS:"
echo "─────────────────────────────────────────────────────────────────────────"
find tools/calculators -name "*sip*.html" -o -name "*compound*.html" -o -name "*investment*.html" -o -name "*lump*.html" 2>/dev/null | while read file; do
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    modified=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t"%Y-%m-%d" "$file" 2>/dev/null)
    echo "  📄 $(basename "$file")"
    echo "     Path: $file"
    echo "     Size: $size bytes"
    echo "     Modified: $modified"
    echo ""
done

echo ""
echo "3️⃣  LOAN CALCULATORS:"
echo "─────────────────────────────────────────────────────────────────────────"
find . -name "*loan*.html" -o -name "*emi*.html" 2>/dev/null | while read file; do
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    modified=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t"%Y-%m-%d" "$file" 2>/dev/null)
    echo "  📄 $(basename "$file")"
    echo "     Path: $file"
    echo "     Size: $size bytes"
    echo "     Modified: $modified"
    echo ""
done

echo ""
echo "4️⃣  RETIREMENT PLANNERS:"
echo "─────────────────────────────────────────────────────────────────────────"
find . -name "*retirement*.html" 2>/dev/null | while read file; do
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    modified=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t"%Y-%m-%d" "$file" 2>/dev/null)
    echo "  📄 $(basename "$file")"
    echo "     Path: $file"
    echo "     Size: $size bytes"
    echo "     Modified: $modified"
    echo ""
done

echo ""
echo "5️⃣  ROOT LEVEL CALCULATORS (Potential Duplicates):"
echo "─────────────────────────────────────────────────────────────────────────"
find . -maxdepth 1 -name "*calculator*.html" 2>/dev/null | while read file; do
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    modified=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t"%Y-%m-%d" "$file" 2>/dev/null)
    echo "  📄 $(basename "$file")"
    echo "     Path: $file"
    echo "     Size: $size bytes"
    echo "     Modified: $modified"
    echo ""
done

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "  📈 SUMMARY"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

us_tax_count=$(find tools/calculators/us_tax_calculator -name "*.html" 2>/dev/null | wc -l)
investment_count=$(find tools/calculators -name "*sip*.html" -o -name "*compound*.html" 2>/dev/null | wc -l)
loan_count=$(find . -name "*loan*.html" -o -name "*emi*.html" 2>/dev/null | wc -l)
retirement_count=$(find . -name "*retirement*.html" 2>/dev/null | wc -l)
root_calc_count=$(find . -maxdepth 1 -name "*calculator*.html" 2>/dev/null | wc -l)

echo "US Tax Calculators: $us_tax_count"
echo "Investment Calculators: $investment_count"
echo "Loan Calculators: $loan_count"
echo "Retirement Planners: $retirement_count"
echo "Root Level Calculators: $root_calc_count"
echo ""

