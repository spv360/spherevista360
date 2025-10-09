#!/usr/bin/env python3
"""
SEO Title Optimizer
Fix posts with titles exceeding 60 characters for better SEO
"""

import requests
import json
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Optimized titles that maintain meaning while staying under 60 chars
TITLE_FIXES = {
    1828: {
        'current': 'Green Bonds and the Energy Transition: Where Yields Make Sense',
        'optimized': 'Green Bonds in Energy Transition: Where Yields Make Sense',
        'length': 54
    },
    1829: {
        'current': 'Open-Source AI Models in the Enterprise: Build, Buy, or Blend?',
        'optimized': 'Enterprise AI Models: Build, Buy, or Blend Strategy?',
        'length': 51
    },
    1833: {
        'current': 'Streaming Gets Personal: How AI Recommenders Shape What You Watch',
        'optimized': 'How AI Recommenders Shape Your Streaming Experience',
        'length': 49
    },
    1834: {
        'current': 'Digital Identity Goes Global: Cross-Border Logins and Payments',
        'optimized': 'Global Digital Identity: Cross-Border Logins & Payments',
        'length': 55
    },
    1837: {
        'current': 'AI, Speech, and Safety: What Regulation Is Aiming for in 2025',
        'optimized': 'AI Speech Safety: What 2025 Regulation Will Target',
        'length': 49
    },
    1838: {
        'current': 'Ops Copilots: Automating the Unsexy Work That Scales Businesses',
        'optimized': 'Ops Copilots: Automating Work That Scales Businesses',
        'length': 51
    }
}

def authenticate():
    """Get WordPress credentials"""
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    return username, app_password

def update_post_title(post_id, new_title, auth):
    """Update post title in WordPress"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {
        'title': new_title
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=data, auth=auth, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print(f"Error updating post {post_id}: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Main function to fix SEO title lengths"""
    print("SEO Title Optimizer")
    print("=" * 50)
    print("Fixing posts with titles exceeding 60 characters...")
    print()
    
    # Show what we're going to fix
    print("PLANNED FIXES:")
    print("-" * 30)
    for post_id, fix in TITLE_FIXES.items():
        print(f"Post {post_id}:")
        print(f"  Current: {fix['current']} ({len(fix['current'])} chars)")
        print(f"  New: {fix['optimized']} ({fix['length']} chars)")
        print(f"  Savings: {len(fix['current']) - fix['length']} characters")
        print()
    
    # Confirm with user
    proceed = input("Proceed with title updates? (y/N): ").lower().strip()
    if proceed != 'y':
        print("Aborted.")
        return
    
    # Get authentication
    auth = authenticate()
    
    # Apply fixes
    print("\nApplying fixes...")
    print("=" * 30)
    
    successful_updates = 0
    
    for post_id, fix in TITLE_FIXES.items():
        print(f"Updating post {post_id}...")
        
        if update_post_title(post_id, fix['optimized'], auth):
            print(f"  ✅ Successfully updated to: {fix['optimized']}")
            successful_updates += 1
        else:
            print(f"  ❌ Failed to update post {post_id}")
        print()
    
    # Summary
    print("=" * 50)
    print("UPDATE SUMMARY")
    print("=" * 50)
    print(f"Posts processed: {len(TITLE_FIXES)}")
    print(f"Successful updates: {successful_updates}")
    print(f"Failed updates: {len(TITLE_FIXES) - successful_updates}")
    
    if successful_updates == len(TITLE_FIXES):
        print("\n🎉 All SEO titles successfully optimized!")
        print("All titles now comply with the 60-character SEO limit.")
    else:
        print(f"\n⚠️ {len(TITLE_FIXES) - successful_updates} updates failed. Please check manually.")

if __name__ == "__main__":
    main()