#!/usr/bin/env python3
"""
Advanced WordPress Title Updater
Try multiple authentication approaches and API methods
"""

import requests
import json
import getpass
import base64

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

# Optimized titles
TITLE_FIXES = {
    1828: 'Green Bonds in Energy Transition: Where Yields Make Sense',
    1829: 'Enterprise AI Models: Build, Buy, or Blend Strategy?',
    1833: 'How AI Recommenders Shape Your Streaming Experience',
    1834: 'Global Digital Identity: Cross-Border Logins & Payments',
    1837: 'AI Speech Safety: What 2025 Regulation Will Target',
    1838: 'Ops Copilots: Automating Work That Scales Businesses'
}

def get_auth_methods():
    """Get multiple authentication options"""
    print("WordPress Authentication Options:")
    print("1. Application Password (recommended)")
    print("2. Basic Auth with regular password")
    print("3. JWT Token (if available)")
    
    choice = input("Choose authentication method (1-3): ").strip()
    username = input("Enter WordPress username: ")
    
    if choice == "1" or choice == "":
        app_password = getpass.getpass("Enter application password: ")
        return ("app_password", username, app_password)
    elif choice == "2":
        password = getpass.getpass("Enter WordPress password: ")
        return ("basic", username, password)
    elif choice == "3":
        token = getpass.getpass("Enter JWT token: ")
        return ("jwt", username, token)
    else:
        print("Invalid choice, using application password")
        app_password = getpass.getpass("Enter application password: ")
        return ("app_password", username, app_password)

def create_auth_header(auth_type, username, credential):
    """Create appropriate authentication header"""
    if auth_type == "app_password":
        return ("basic", (username, credential))
    elif auth_type == "basic":
        return ("basic", (username, credential))
    elif auth_type == "jwt":
        return ("bearer", credential)
    return None

def test_auth(auth_type, username, credential):
    """Test authentication by fetching user info"""
    print(f"\nTesting authentication...")
    
    if auth_type in ["app_password", "basic"]:
        auth = (username, credential)
        headers = {'Content-Type': 'application/json'}
        
        # Test with a simple user request
        response = requests.get(f"{WP_BASE_URL}/users/me", auth=auth, headers=headers)
        
    elif auth_type == "jwt":
        headers = {
            'Authorization': f'Bearer {credential}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{WP_BASE_URL}/users/me", headers=headers)
        auth = None
    
    print(f"Auth test response: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Authentication successful! User: {user_data.get('name', 'Unknown')}")
        return True, (auth if auth_type in ["app_password", "basic"] else None), headers
    else:
        print(f"❌ Authentication failed: {response.text}")
        return False, None, None

def check_post_permissions(post_id, auth, headers):
    """Check if we can edit a specific post"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    # First, try to get the post
    if auth:
        response = requests.get(url, auth=auth, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return False, f"Cannot fetch post: {response.status_code}"
    
    post_data = response.json()
    
    # Check if we can edit by looking at capabilities or trying a minimal update
    print(f"Post author: {post_data.get('author', 'Unknown')}")
    print(f"Post status: {post_data.get('status', 'Unknown')}")
    
    return True, "Can fetch post"

def update_post_title_method1(post_id, new_title, auth, headers):
    """Method 1: Standard REST API POST"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'title': new_title}
    
    if auth:
        response = requests.post(url, json=data, auth=auth, headers=headers)
    else:
        response = requests.post(url, json=data, headers=headers)
    
    return response

def update_post_title_method2(post_id, new_title, auth, headers):
    """Method 2: PUT request"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'title': new_title}
    
    if auth:
        response = requests.put(url, json=data, auth=auth, headers=headers)
    else:
        response = requests.put(url, json=data, headers=headers)
    
    return response

def update_post_title_method3(post_id, new_title, auth, headers):
    """Method 3: PATCH request"""
    url = f"{WP_BASE_URL}/posts/{post_id}"
    
    data = {'title': new_title}
    
    if auth:
        response = requests.patch(url, json=data, auth=auth, headers=headers)
    else:
        response = requests.patch(url, json=data, headers=headers)
    
    return response

def try_all_update_methods(post_id, new_title, auth, headers):
    """Try all available update methods"""
    methods = [
        ("POST", update_post_title_method1),
        ("PUT", update_post_title_method2),
        ("PATCH", update_post_title_method3)
    ]
    
    for method_name, method_func in methods:
        print(f"    Trying {method_name} method...")
        try:
            response = method_func(post_id, new_title, auth, headers)
            print(f"    {method_name} response: {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✅ {method_name} method succeeded!")
                return True, response
            else:
                print(f"    ❌ {method_name} failed: {response.text[:200]}")
        except Exception as e:
            print(f"    ❌ {method_name} error: {e}")
    
    return False, None

def main():
    """Main function"""
    print("Advanced WordPress Title Updater")
    print("=" * 50)
    
    # Get authentication
    auth_type, username, credential = get_auth_methods()
    
    # Test authentication
    auth_success, auth, headers = test_auth(auth_type, username, credential)
    
    if not auth_success:
        print("❌ Authentication failed. Cannot proceed.")
        return
    
    # Show what we plan to update
    print(f"\nPlanned updates:")
    for post_id, new_title in TITLE_FIXES.items():
        print(f"  Post {post_id}: {new_title}")
    
    proceed = input(f"\nProceed with {len(TITLE_FIXES)} updates? (y/N): ").lower().strip()
    if proceed != 'y':
        print("Aborted.")
        return
    
    print("\nStarting updates...")
    print("=" * 30)
    
    successful_updates = 0
    
    for post_id, new_title in TITLE_FIXES.items():
        print(f"\nUpdating Post {post_id}...")
        print(f"New title: {new_title}")
        
        # Check permissions first
        can_edit, perm_msg = check_post_permissions(post_id, auth, headers)
        print(f"  Permission check: {perm_msg}")
        
        if not can_edit:
            print(f"  ❌ Cannot access post {post_id}")
            continue
        
        # Try all update methods
        success, response = try_all_update_methods(post_id, new_title, auth, headers)
        
        if success:
            print(f"  ✅ Successfully updated post {post_id}")
            successful_updates += 1
        else:
            print(f"  ❌ All update methods failed for post {post_id}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("UPDATE SUMMARY")
    print(f"Total posts: {len(TITLE_FIXES)}")
    print(f"Successful: {successful_updates}")
    print(f"Failed: {len(TITLE_FIXES) - successful_updates}")
    
    if successful_updates == len(TITLE_FIXES):
        print("\n🎉 All titles successfully updated!")
    elif successful_updates > 0:
        print(f"\n⚠️ Partial success: {successful_updates}/{len(TITLE_FIXES)} updated")
    else:
        print(f"\n❌ No updates succeeded. Manual update required.")

if __name__ == "__main__":
    main()