#!/usr/bin/env python3
"""
WordPress Pages Duplicate Analysis Script
Analyzes WordPress pages via REST API to identify duplicates for cleanup
"""

import json
import re
from collections import defaultdict
from datetime import datetime

def load_pages_data():
    """Load pages data from JSON file"""
    try:
        with open('wordpress_pages_raw.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading pages data: {e}")
        return []

def normalize_title(title):
    """Normalize page titles for grouping"""
    if isinstance(title, dict) and 'rendered' in title:
        title = title['rendered']

    # Remove HTML entities and extra spaces
    title = re.sub(r'&#\d+;', '', title)
    title = re.sub(r'&[a-zA-Z]+;', '', title)
    title = title.strip().lower()

    # Remove common suffixes that indicate duplicates
    title = re.sub(r'\s*-\s*\d+$', '', title)  # Remove -2, -3, etc.
    title = re.sub(r'\s*\(\d+\)$', '', title)  # Remove (2), (3), etc.
    title = re.sub(r'\s+copy\s*\d*$', '', title)  # Remove copy, copy2, etc.

    return title.strip()

def group_duplicates(pages):
    """Group pages by normalized title to find duplicates"""
    groups = defaultdict(list)

    for page in pages:
        title = page.get('title', {})
        if isinstance(title, dict):
            title = title.get('rendered', '')

        normalized = normalize_title(title)
        groups[normalized].append(page)

    return groups

def identify_pages_to_keep(group):
    """For a group of duplicate pages, identify which one(s) to keep"""
    if len(group) <= 1:
        return group  # No duplicates

    # First priority: Clean slug (no numbers at end)
    clean_slug_pages = []
    numbered_slug_pages = []

    for page in group:
        slug = page.get('slug', '')
        # Check if slug ends with numbers (like -2, -3, etc.)
        if re.search(r'-\d+$', slug):
            numbered_slug_pages.append(page)
        else:
            clean_slug_pages.append(page)

    # If we have clean slug pages, keep the newest among them
    if clean_slug_pages:
        return [max(clean_slug_pages, key=lambda x: x.get('modified', ''))]

    # If no clean slugs, keep the newest numbered one
    return [max(group, key=lambda x: x.get('modified', ''))]

def analyze_duplicates():
    """Main analysis function"""
    pages = load_pages_data()
    if not pages:
        print("No pages data found!")
        return

    print(f"📊 Total pages found: {len(pages)}")
    print()

    # Group by normalized title
    groups = group_duplicates(pages)

    # Filter to only calculator-related pages
    calculator_keywords = [
        'calculator', 'tax', 'investment', 'retirement', 'sip', 'emi', 'loan',
        'federal', 'state', 'capital gains', 'withholding', 'self-employment'
    ]

    calculator_groups = {}
    for title, group in groups.items():
        if any(keyword in title for keyword in calculator_keywords) and len(group) > 1:
            calculator_groups[title] = group

    print(f"🔍 Calculator pages with duplicates: {len(calculator_groups)}")
    print()

    # Analyze each duplicate group
    pages_to_delete = []
    pages_to_keep = []

    for title, group in calculator_groups.items():
        print(f"📄 {title.upper()} ({len(group)} pages):")

        # Identify pages to keep and delete FIRST
        to_keep = identify_pages_to_keep(group)
        to_delete = [p for p in group if p not in to_keep]

        # Display results
        all_pages = to_keep + to_delete
        for page in all_pages:
            page_id = page.get('id')
            slug = page.get('slug', '')
            modified = page.get('modified', '')[:19]  # Truncate timestamp
            status = "✅ KEEP" if page in to_keep else "🗑️  DELETE"

            print(f"  {status} ID {page_id}: {slug} (modified: {modified})")

        print()

        # Accumulate results
        pages_to_keep.extend(to_keep)
        pages_to_delete.extend(to_delete)

    print("=" * 60)
    print("📋 SUMMARY:")
    print(f"• Total calculator pages: {sum(len(g) for g in calculator_groups.values())}")
    print(f"• Pages to keep: {len(pages_to_keep)}")
    print(f"• Pages to delete: {len(pages_to_delete)}")
    print()

    # Save results to files
    with open('pages_to_keep.json', 'w') as f:
        json.dump(pages_to_keep, f, indent=2)

    with open('pages_to_delete.json', 'w') as f:
        json.dump(pages_to_delete, f, indent=2)

    # Create deletion script
    create_deletion_script(pages_to_delete)

    print("📁 Files created:")
    print("• pages_to_keep.json - Pages to preserve")
    print("• pages_to_delete.json - Pages to remove")
    print("• delete_duplicate_pages.sh - Automated deletion script")

def create_deletion_script(pages_to_delete):
    """Create a bash script to delete duplicate pages via API"""
    script_content = """#!/bin/bash
# WordPress Duplicate Pages Deletion Script
# This script deletes duplicate calculator pages identified by the analysis

echo "🗑️  DELETING DUPLICATE WORDPRESS PAGES..."
echo "This will move pages to trash (not permanently delete)"
echo ""

# Check if we have pages to delete
if [ ! -f "pages_to_delete.json" ]; then
    echo "❌ Error: pages_to_delete.json not found!"
    exit 1
fi

# Note: WordPress REST API requires authentication for DELETE operations
# This script shows the pages that should be deleted
# You'll need to delete them manually via WordPress admin or use proper authentication

echo "📄 PAGES TO DELETE (move to trash in WordPress admin):"
echo ""

# Parse JSON and show pages to delete
python3 -c "
import json
with open('pages_to_delete.json', 'r') as f:
    pages = json.load(f)

for page in pages:
    page_id = page.get('id')
    title = page.get('title', {}).get('rendered', 'Unknown')
    slug = page.get('slug', '')
    print(f'• ID {page_id}: {title} (slug: {slug})')
"

echo ""
echo "🔄 NEXT STEPS:"
echo "1. Go to WordPress Admin → Pages → All Pages"
echo "2. Search for each page ID above"
echo "3. Click 'Trash' for each duplicate page"
echo "4. After trashing, run: python3 update_retirement_planner.py"
echo ""

echo "⚠️  IMPORTANT: Pages go to trash first, not permanently deleted"
echo "You can restore them from trash if needed"
"""

    with open('delete_duplicate_pages.sh', 'w') as f:
        f.write(script_content)

    # Make executable
    import os
    os.chmod('delete_duplicate_pages.sh', 0o755)

if __name__ == "__main__":
    analyze_duplicates()