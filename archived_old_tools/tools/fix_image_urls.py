#!/usr/bin/env python3
"""
Fix Broken Image URLs
Replaces broken Unsplash URLs with working contextual alternatives
"""

import sys
import os
from pathlib import Path

# Add tools to path
sys.path.append(str(Path(__file__).parent / 'production'))
from enhanced_wp_client import WordPressClient

# URL mappings for broken to working images (with HTML encoding)
URL_FIXES = {
    # Finance context (HTML encoded)
    "https://images.unsplash.com/photo-1559589688-f26e20a6c987?ixlib=rb-4.0.3&amp;auto=format&amp;fit=crop&amp;w=1600&amp;h=900&amp;q=80": 
    "https://images.unsplash.com/photo-1559126961-cc431cc43e55?auto=format&amp;fit=crop&amp;w=800&amp;h=500&amp;q=80",
    
    # Technology context (HTML encoded)
    "https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&amp;auto=format&amp;fit=crop&amp;w=1600&amp;h=900&amp;q=80":
    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&amp;fit=crop&amp;w=800&amp;h=500&amp;q=80",
    
    # Entertainment context (HTML encoded)
    "https://images.unsplash.com/photo-1489599904335-1f69ba4d43da?ixlib=rb-4.0.3&amp;auto=format&amp;fit=crop&amp;w=1600&amp;h=900&amp;q=80":
    "https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?auto=format&amp;fit=crop&amp;w=800&amp;h=500&amp;q=80",
    
    # Also handle non-encoded versions
    "https://images.unsplash.com/photo-1559589688-f26e20a6c987?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80": 
    "https://images.unsplash.com/photo-1559126961-cc431cc43e55?auto=format&fit=crop&w=800&h=500&q=80",
    
    "https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80":
    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=800&h=500&q=80",
    
    "https://images.unsplash.com/photo-1489599904335-1f69ba4d43da?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80":
    "https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?auto=format&fit=crop&w=800&h=500&q=80"
}

def fix_broken_images():
    """Fix broken image URLs in WordPress posts"""
    client = WordPressClient()
    
    # Posts that need fixing based on our validation
    posts_to_fix = [1827, 1828, 1829, 1830, 1831, 1832, 1833]
    
    print("🔧 FIXING BROKEN IMAGE URLS")
    print("=" * 50)
    
    fixed_count = 0
    
    for post_id in posts_to_fix:
        try:
            # Get post content
            post = client.get_post(post_id)
            if not post:
                print(f"❌ Could not retrieve post {post_id}")
                continue
                
            # Check both rendered and raw content
            original_content = post['content']['rendered']
            print(f"🔍 Checking post {post_id}: {post['title']['rendered'][:50]}...")
            
            # Debug: check if any broken URLs are present
            broken_found = []
            for broken_url in URL_FIXES.keys():
                if broken_url in original_content:
                    broken_found.append(broken_url)
            
            if broken_found:
                print(f"   📍 Found {len(broken_found)} broken URLs")
                updated_content = original_content
                
                # Replace broken URLs
                for broken_url, working_url in URL_FIXES.items():
                    if broken_url in updated_content:
                        updated_content = updated_content.replace(broken_url, working_url)
                        print(f"   ✅ Replaced: {broken_url[:60]}...")
                        fixed_count += 1
                
                # Update post if content changed
                if updated_content != original_content:
                    update_data = {
                        'content': updated_content
                    }
                    
                    if client.update_post(post_id, update_data):
                        print(f"   ✅ Post {post_id} updated successfully")
                    else:
                        print(f"   ❌ Failed to update post {post_id}")
                else:
                    print(f"   ⚠️ No changes made to post {post_id}")
            else:
                print(f"   ℹ️ No broken URLs found in post {post_id}")
            
        except Exception as e:
            print(f"❌ Error processing post {post_id}: {e}")
    
    print(f"\n📊 SUMMARY: Fixed {fixed_count} broken image URLs")
    return fixed_count

if __name__ == "__main__":
    fix_broken_images()