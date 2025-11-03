#!/usr/bin/env python3
"""
WordPress API - Move Duplicate Pages to Trash
Automatically moves identified duplicate pages to trash using WordPress REST API
"""

import requests
import json
import getpass
from requests.auth import HTTPBasicAuth

def load_pages_to_delete():
    """Load the list of pages to delete"""
    try:
        with open('pages_to_delete.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading pages_to_delete.json: {e}")
        return []

def move_page_to_trash(page_id, auth, base_url="https://spherevista360.com"):
    """Move a single page to trash using WordPress REST API"""

    # Use DELETE method to move to trash (not POST with status)
    url = f"{base_url}/wp-json/wp/v2/pages/{page_id}"

    try:
        # DELETE request moves the page to trash
        response = requests.delete(url, auth=auth)

        if response.status_code == 200:
            page_data = response.json()
            title = page_data.get('title', {}).get('rendered', 'Unknown')
            print(f"✅ Moved to trash: ID {page_id} - {title}")
            return True
        else:
            print(f"❌ Failed to trash page {page_id}: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ Error trashing page {page_id}: {e}")
        return False

def main():
    print("🗑️ WORDPRESS API - MOVE DUPLICATE PAGES TO TRASH")
    print("=" * 60)
    print()

    # Load pages to delete
    pages_to_delete = load_pages_to_delete()
    if not pages_to_delete:
        print("❌ No pages to delete found!")
        return

    print(f"📄 Found {len(pages_to_delete)} pages to move to trash")
    print()

    # Get WordPress credentials
    username = input("WordPress Username: ").strip()
    if not username:
        username = "Sphere Vista"  # Default based on previous context

    password = getpass.getpass("WordPress Password: ")

    if not password:
        print("❌ Password is required!")
        return

    # Setup authentication
    auth = HTTPBasicAuth(username, password)

    print()
    print("🔄 Starting trash operation...")
    print("Note: This moves pages to trash (not permanent deletion)")
    print("You can restore them from WordPress Admin → Pages → Trash if needed")
    print()

    # Confirm before proceeding
    confirm = input(f"Move {len(pages_to_delete)} pages to trash? (yes/no): ").lower().strip()
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return

    print()

    # Process each page
    success_count = 0
    fail_count = 0

    for page in pages_to_delete:
        page_id = page.get('id')
        if move_page_to_trash(page_id, auth):
            success_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 60)
    print("📊 TRASH OPERATION COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully trashed: {success_count} pages")
    print(f"❌ Failed to trash: {fail_count} pages")
    print()

    if success_count > 0:
        print("🔄 NEXT STEPS:")
        print("1. Go to WordPress Admin → Pages → Trash")
        print("2. Verify the pages are there (can be restored if needed)")
        print("3. Run: python3 update_retirement_planner.py")
        print("4. Clear WordPress cache")
        print()

        print("🎯 REMAINING CLEANUP:")
        print(f"• {len(pages_to_delete) - success_count} duplicate pages still need manual deletion")
        print("• Update retirement planner page (ID 3173)")
        print("• Test all remaining calculator pages")

    if fail_count > 0:
        print("⚠️  SOME PAGES FAILED TO TRASH:")
        print("You may need to delete them manually in WordPress Admin")
        print("Check your authentication and try again, or delete manually")

if __name__ == "__main__":
    main()