#!/usr/bin/env python3
"""
Complete SEO Fix - Meta Descriptions and Remaining Titles
Fix meta descriptions and any remaining title issues
"""

import requests
import json
import getpass
from bs4 import BeautifulSoup

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Fix for Post 1835 title (the one still exceeding 60 chars)
TITLE_FIX_1835 = 'Supply Chain Reshoring: How 2025 Changes Everything'

# Optimized meta descriptions (under 155 characters)
META_DESCRIPTIONS = {
    1827: 'AI agents help retail investors with position limits, order confirmation, and weekly portfolio reviews for better investment outcomes.',
    1828: 'Green bonds in energy transition offer varying yields. Look beyond labels to frameworks, capex plans, and third-party assurance.',
    1829: 'Open-source AI models reduce vendor risk and lower costs. The trade-off: owning updates, evaluations, and safety tuning processes.',
    1830: 'AI inference is shifting. Lightweight models run locally for speed and privacy while heavier tasks remain in the cloud infrastructure.',
    1831: 'Modern product analytics connects events to experiments and roadmaps. Track fewer, better metrics and design for action over dashboards.',
    1832: 'Studios use AI to accelerate VFX steps. Artists focus on look development and storytelling while tools handle masks and automated fills.',
    1833: 'AI recommenders become context-aware and multi-objective. Cold starts shrink with graph signals while mood mixes keep sessions active.',
    1834: 'Cross-border digital identity simplifies with passkeys reducing phishing and verified credentials speeding remote onboarding processes.',
    1835: 'Companies build regional supply chain hubs with dual sources for critical inputs. Software replaces spreadsheets for better visibility.',
    1836: 'AI trip planning sequences cities, optimizes budgets, and avoids crowds. Export to maps while keeping room for spontaneous discoveries.',
    1837: 'AI speech regulation converges on model transparency, media provenance, and accountability. Obligations scale with potential risk levels.',
    1838: 'Operations copilots speed business closings, vendor checks, and onboarding by turning manual checklists into automated workflows.'
}

def authenticate():
    """Get WordPress credentials"""
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    return username, app_password

def update_post_title(post_id, new_title, auth):
    """Update post title via REST API"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'title': new_title}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, auth=auth, headers=headers)
    return response.status_code == 200, response

def update_post_excerpt(post_id, excerpt, auth):
    """Update post excerpt (which often becomes meta description)"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'excerpt': excerpt}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, auth=auth, headers=headers)
    return response.status_code == 200, response

def main():
    """Fix all remaining SEO issues"""
    print("Complete SEO Fix - Meta Descriptions and Titles")
    print("=" * 60)
    
    # Get authentication
    auth = authenticate()
    
    print("\nPLANNED FIXES:")
    print("-" * 30)
    
    print("1. TITLE FIX:")
    print(f"   Post 1835: {TITLE_FIX_1835} ({len(TITLE_FIX_1835)} chars)")
    
    print("\n2. META DESCRIPTION FIXES:")
    for post_id, desc in META_DESCRIPTIONS.items():
        print(f"   Post {post_id}: {desc[:50]}... ({len(desc)} chars)")
    
    proceed = input(f"\nProceed with title and meta description fixes? (y/N): ").lower().strip()
    if proceed != 'y':
        print("Aborted.")
        return
    
    print("\nApplying fixes...")
    print("=" * 40)
    
    successful_updates = 0
    total_updates = 0
    
    # Fix Post 1835 title
    print(f"\nFixing Post 1835 title...")
    total_updates += 1
    success, response = update_post_title(1835, TITLE_FIX_1835, auth)
    if success:
        print(f"  ✅ Title updated: {TITLE_FIX_1835}")
        successful_updates += 1
    else:
        print(f"  ❌ Title update failed: {response.text[:100]}")
    
    # Fix meta descriptions (using excerpt field)
    print(f"\nFixing meta descriptions...")
    for post_id, description in META_DESCRIPTIONS.items():
        print(f"\nPost {post_id}:")
        print(f"  New excerpt: {description}")
        
        total_updates += 1
        success, response = update_post_excerpt(post_id, description, auth)
        if success:
            print(f"  ✅ Meta description updated")
            successful_updates += 1
        else:
            print(f"  ❌ Meta description update failed: {response.text[:100]}")
    
    # Summary
    print(f"\n" + "=" * 60)
    print("SEO FIX SUMMARY")
    print("=" * 60)
    print(f"Total updates attempted: {total_updates}")
    print(f"Successful updates: {successful_updates}")
    print(f"Failed updates: {total_updates - successful_updates}")
    
    if successful_updates == total_updates:
        print("\n🎉 All SEO issues fixed!")
        print("✅ Post 1835 title optimized")
        print("✅ All meta descriptions optimized")
        print("\nThis should resolve the 'Search engine title exceeds 60 characters' warnings.")
    elif successful_updates > 0:
        print(f"\n⚠️ Partial success: {successful_updates}/{total_updates} updates completed")
    else:
        print(f"\n❌ All updates failed. Please check manually.")
    
    print(f"\nNext steps:")
    print("1. Clear any SEO plugin caches")
    print("2. Check your SEO plugin for remaining warnings")
    print("3. Run site audit to verify improvements")

if __name__ == "__main__":
    main()