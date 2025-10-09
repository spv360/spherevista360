#!/usr/bin/env python3
"""
Direct Fix for Post 1833 Broken Links
Target the specific broken links in post 1833
"""

import requests
import base64

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"
WP_USERNAME = "admin"
WP_PASSWORD = "DTYzFB6dZS9sHNY7QM73w&@F"

def fix_post_1833():
    """Fix the broken links specifically in post 1833"""
    post_id = 1833
    
    print("🔧 FIXING POST 1833 BROKEN LINKS")
    print("=" * 50)
    
    # Get current content
    response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
    if response.status_code != 200:
        print("❌ Failed to fetch post")
        return False
    
    post = response.json()
    current_content = post['content']['rendered']
    
    print(f"📝 Post: {post['title']['rendered']}")
    print(f"Current content length: {len(current_content)} characters")
    
    # Make replacements
    updated_content = current_content
    
    # Replace first broken link
    old_link_1 = 'https://spherevista360.com/product-analytics-2025/'
    new_link_1 = 'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/'
    
    # Replace second broken link  
    old_link_2 = 'https://spherevista360.com/on-device-vs-cloud-ai-2025/'
    new_link_2 = 'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/'
    
    if old_link_1 in updated_content:
        updated_content = updated_content.replace(old_link_1, new_link_1)
        print(f"✅ Replaced: {old_link_1}")
        print(f"   With: {new_link_1}")
    
    if old_link_2 in updated_content:
        updated_content = updated_content.replace(old_link_2, new_link_2)
        print(f"✅ Replaced: {old_link_2}")
        print(f"   With: {new_link_2}")
    
    if updated_content == current_content:
        print("⚠️ No changes needed - links may already be fixed")
        return True
    
    # Try multiple authentication methods
    auth_methods = [
        ('Basic Auth', (WP_USERNAME, WP_PASSWORD)),
        ('App Password', requests.auth.HTTPBasicAuth(WP_USERNAME, WP_PASSWORD))
    ]
    
    headers = {'Content-Type': 'application/json'}
    
    for auth_name, auth in auth_methods:
        print(f"\\nTrying {auth_name}...")
        
        try:
            # Try different data structures
            data_variants = [
                {'content': updated_content},
                {'content': {'raw': updated_content}},
                {'content': {'rendered': updated_content}}
            ]
            
            for i, data in enumerate(data_variants):
                try:
                    response = requests.post(
                        f"{WP_BASE_URL}/posts/{post_id}",
                        json=data,
                        auth=auth,
                        headers=headers,
                        timeout=20
                    )
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ SUCCESS with {auth_name} (variant {i+1})!")
                        return True
                    else:
                        print(f"   Variant {i+1}: {response.status_code} - {response.text[:100]}")
                        
                except Exception as e:
                    print(f"   Variant {i+1} error: {e}")
                    
        except Exception as e:
            print(f"   {auth_name} failed: {e}")
    
    # If all API methods fail, let's try a direct curl approach
    print("\\n🔄 Trying direct curl method...")
    
    import subprocess
    import json
    
    try:
        # Prepare the data
        curl_data = json.dumps({'content': updated_content})
        
        # Use curl directly
        curl_command = [
            'curl', '-X', 'POST',
            f'{WP_BASE_URL}/posts/{post_id}',
            '-H', 'Content-Type: application/json',
            '-u', f'{WP_USERNAME}:{WP_PASSWORD}',
            '-d', curl_data
        ]
        
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                response_data = json.loads(result.stdout)
                if 'id' in response_data:
                    print("✅ SUCCESS with direct curl method!")
                    return True
                else:
                    print(f"❌ Curl failed: {result.stdout[:200]}")
            except:
                print(f"❌ Curl response parsing failed: {result.stdout[:200]}")
        else:
            print(f"❌ Curl command failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Curl method error: {e}")
    
    print("\\n❌ All update methods failed")
    return False

def verify_fix():
    """Verify the fix worked"""
    print("\\n🔍 VERIFYING FIX...")
    
    response = requests.get(f"{WP_BASE_URL}/posts/1833")
    if response.status_code == 200:
        post = response.json()
        content = post['content']['rendered']
        
        broken_links = [
            'https://spherevista360.com/product-analytics-2025/',
            'https://spherevista360.com/on-device-vs-cloud-ai-2025/'
        ]
        
        correct_links = [
            'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/',
            'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/'
        ]
        
        still_broken = 0
        fixed_count = 0
        
        for broken_link in broken_links:
            if broken_link in content:
                still_broken += 1
                print(f"❌ Still contains: {broken_link}")
            else:
                print(f"✅ No longer contains: {broken_link}")
        
        for correct_link in correct_links:
            if correct_link in content:
                fixed_count += 1
                print(f"✅ Now contains: {correct_link}")
        
        if still_broken == 0 and fixed_count == 2:
            print("\\n🎉 SUCCESS! All broken links fixed!")
        else:
            print(f"\\n⚠️ Still {still_broken} broken links, {fixed_count} correct links")
    else:
        print("❌ Failed to verify")

if __name__ == "__main__":
    success = fix_post_1833()
    verify_fix()
    
    if not success:
        print("\\n📋 MANUAL FIX NEEDED:")
        print("Go to: https://spherevista360.com/wp-admin/post.php?post=1833&action=edit")
        print("Replace the broken links in the 'Related reading' section")