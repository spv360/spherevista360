#!/usr/bin/env python3
"""
Debug authentication issues.
"""

import sys
import requests
import base64

# Test direct authentication like the working tools
def test_direct_auth():
    """Test direct authentication method from working tools."""
    print("🔍 DEBUGGING AUTHENTICATION")
    print("=" * 40)
    
    username = "JK"
    password = "z7o6 eC4K pW6L dJTn Rh0K YdTm"
    
    # Test the exact method from working tools
    print("🧪 Testing direct method...")
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            "https://spherevista360.com/wp-json/wp/v2/users/me",
            headers=headers,
            timeout=30
        )
        
        print(f"Response code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ SUCCESS! User: {user_data.get('name')}")
            print(f"ID: {user_data.get('id')}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_direct_auth()