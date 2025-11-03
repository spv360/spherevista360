#!/usr/bin/env python3
"""
Update Retirement Planner Page Script
Updates the retirement planner page (ID 3173) with the fixed version
"""

import json
import os

def update_retirement_planner():
    """Update the retirement planner page with fixed content"""

    print("🏖️ UPDATING RETIREMENT PLANNER PAGE...")
    print()

    # Check if the fixed file exists
    fixed_file = "retirement-planner-fixed.html"
    if not os.path.exists(fixed_file):
        print(f"❌ Error: {fixed_file} not found!")
        return False

    print(f"✅ Found fixed retirement planner file: {fixed_file}")
    print()

    # Read the fixed content
    try:
        with open(fixed_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {fixed_file}: {e}")
        return False

    print("📄 Content loaded successfully")
    print(f"   Size: {len(content)} characters")
    print()

    # Extract content between <body> tags (if present)
    import re
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if body_match:
        content = body_match.group(1).strip()
        print("✅ Extracted content between <body> tags")
    else:
        print("ℹ️  No <body> tags found, using full content")

    print()
    print("🔄 MANUAL UPDATE REQUIRED:")
    print("=" * 50)
    print("Since WordPress REST API requires authentication for updates,")
    print("you need to manually update the retirement planner page:")
    print()
    print("1. 🌐 Go to WordPress Admin:")
    print("   https://spherevista360.com/wp-admin/")
    print()
    print("2. 📄 Edit Page ID 3173:")
    print("   • Go to: Pages → All Pages")
    print("   • Find page ID 3173 (Retirement Planner and Estimator)")
    print("   • Click: Edit")
    print()
    print("3. 🔄 Switch to Code Editor:")
    print("   • Look for tabs: Visual | Code editor | Text")
    print("   • Click: Code editor (or HTML/Text tab)")
    print()
    print("4. 📝 Replace Content:")
    print("   • Select ALL existing content (Ctrl+A)")
    print("   • Delete everything")
    print("   • Paste the fixed content from below")
    print()
    print("5. 💾 Save Changes:")
    print("   • Click: Update button (top right)")
    print("   • Check: Preview the page to verify it works")
    print()
    print("=" * 50)
    print("📋 FIXED CONTENT TO PASTE:")
    print("=" * 50)

    # Show first 500 characters as preview
    preview = content[:500] + "..." if len(content) > 500 else content
    print(preview)

    print()
    print("=" * 50)
    print("📁 Full content saved to: retirement_planner_content.html")
    print("   (Copy from this file if needed)")
    print()

    # Save the content to a separate file for easy copying
    with open('retirement_planner_content.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ RETIREMENT PLANNER UPDATE PREPARED")
    print()
    print("🎯 EXPECTED RESULTS AFTER UPDATE:")
    print("• Aligned form labels with icons")
    print("• Horizontal button layout")
    print("• Interactive data displays")
    print("• Progress bars and charts")
    print("• No JavaScript console errors")
    print("• Mobile responsive design")

    return True

if __name__ == "__main__":
    update_retirement_planner()
