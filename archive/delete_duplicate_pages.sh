#!/bin/bash
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
