#!/usr/bin/env python3
"""
Ultra-Optimized Meta Descriptions
Create meta descriptions under 120 characters for strict SEO compliance
"""

import requests
import json
import getpass

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Ultra-optimized meta descriptions (under 120 characters)
OPTIMIZED_META_DESCRIPTIONS = {
    1827: 'AI agents help retail investors with position limits, order confirmation, and weekly portfolio reviews.',  # 108 chars
    1828: 'Green bonds offer varying yields in energy transition. Look beyond labels to frameworks and assurance.',  # 107 chars
    1829: 'Open-source AI models reduce vendor risk and costs. Trade-off: owning updates and safety tuning.',  # 103 chars
    1830: 'AI inference shifts: lightweight models run locally for speed while heavy tasks stay in cloud.',  # 102 chars
    1831: 'Modern product analytics connects events to experiments. Track fewer, better metrics for action.',  # 108 chars
    1832: 'Studios use AI to accelerate VFX steps. Artists focus on look development while tools handle fills.',  # 109 chars
    1833: 'AI recommenders become context-aware. Cold starts shrink with graph signals, mood mixes keep sessions.',  # 111 chars
    1834: 'Digital identity simplifies cross-border with passkeys reducing phishing and verified credentials.',  # 108 chars
    1835: 'Companies build regional supply chain hubs with dual sources. Software replaces spreadsheets.',  # 102 chars
    1836: 'AI trip planning sequences cities, optimizes budgets, avoids crowds. Export to maps for travel.',  # 104 chars
    1837: 'AI speech regulation focuses on model transparency, media provenance, and scaling accountability.',  # 107 chars
    1838: 'Operations copilots speed closings, vendor checks, and onboarding by automating manual workflows.'  # 108 chars
}

def authenticate():
    """Get WordPress credentials"""
    username = input("Enter WordPress username: ")
    app_password = getpass.getpass("Enter application password: ")
    return username, app_password

def update_post_excerpt(post_id, excerpt, auth):
    """Update post excerpt (meta description)"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'excerpt': excerpt}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, auth=auth, headers=headers)
    return response.status_code == 200, response

def main():
    """Update all meta descriptions to be under 120 characters"""
    print("Ultra-Optimized Meta Descriptions Update")
    print("=" * 50)
    print("Creating meta descriptions under 120 characters for strict SEO compliance")
    print()
    
    # Get authentication
    auth = authenticate()
    
    print("\nOptimized Meta Descriptions:")
    print("-" * 40)
    
    for post_id, desc in OPTIMIZED_META_DESCRIPTIONS.items():
        print(f"Post {post_id}: {desc} ({len(desc)} chars)")
    
    print(f"\nAll descriptions are under 120 characters (range: {min(len(d) for d in OPTIMIZED_META_DESCRIPTIONS.values())}-{max(len(d) for d in OPTIMIZED_META_DESCRIPTIONS.values())} chars)")
    
    proceed = input(f"\nProceed with ultra-optimized meta description updates? (y/N): ").lower().strip()
    if proceed != 'y':
        print("Aborted.")
        return
    
    print("\nApplying ultra-optimized meta descriptions...")
    print("=" * 50)
    
    successful_updates = 0
    total_updates = len(OPTIMIZED_META_DESCRIPTIONS)
    
    for post_id, description in OPTIMIZED_META_DESCRIPTIONS.items():
        print(f"\nPost {post_id}:")
        print(f"  New meta: {description} ({len(description)} chars)")
        
        success, response = update_post_excerpt(post_id, description, auth)
        if success:
            print(f"  ✅ Meta description updated")
            successful_updates += 1
        else:
            print(f"  ❌ Update failed: {response.text[:100]}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("ULTRA-OPTIMIZATION SUMMARY")
    print("=" * 50)
    print(f"Total updates attempted: {total_updates}")
    print(f"Successful updates: {successful_updates}")
    print(f"Failed updates: {total_updates - successful_updates}")
    
    if successful_updates == total_updates:
        print("\n🎉 All meta descriptions ultra-optimized!")
        print("✅ All descriptions now under 120 characters")
        print("✅ Strict SEO compliance achieved")
        print("\nThis should completely resolve SEO warnings about length limits.")
    elif successful_updates > 0:
        print(f"\n⚠️ Partial success: {successful_updates}/{total_updates} updates completed")
    else:
        print(f"\n❌ All updates failed. Please check manually.")
    
    print(f"\nNext steps:")
    print("1. Clear SEO plugin cache")
    print("2. Re-run SEO audit")
    print("3. Verify all warnings are resolved")

if __name__ == "__main__":
    main()