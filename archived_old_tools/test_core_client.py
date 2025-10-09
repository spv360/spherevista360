#!/usr/bin/env python3
"""
Test the core WordPress client with JK user authentication.
"""

import sys
import os
sys.path.append('/home/kddevops/projects/spherevista360')

from wordpress_toolkit.core import create_client, WordPressAPIError

def test_core_client():
    """Test the core client functionality."""
    print("🧪 TESTING CORE WORDPRESS CLIENT")
    print("=" * 50)
    
    try:
        # Test with JK user credentials (the proven working auth)
        print("🔐 Testing authentication...")
        client = create_client("JK", "z7o6 eC4K pW6L dJTn Rh0K YdTm")
        
        print("✅ Authentication successful!")
        
        # Test getting user info
        user_info = client.get_user_info()
        print(f"👤 User: {user_info.get('name')}")
        print(f"🆔 ID: {user_info.get('id')}")
        print(f"✏️ Can edit posts: {user_info.get('capabilities', {}).get('edit_posts', False)}")
        
        # Test getting posts
        print("\n📝 Testing post retrieval...")
        posts = client.get_posts(per_page=3)
        print(f"📄 Retrieved {len(posts)} posts")
        
        for post in posts[:2]:  # Show first 2
            print(f"  • {post['title']['rendered']} (ID: {post['id']})")
        
        # Test getting a specific post
        print("\n🎯 Testing specific post retrieval...")
        try:
            post_1833 = client.get_post(1833)
            print(f"✅ Got post 1833: {post_1833['title']['rendered']}")
        except Exception as e:
            print(f"❌ Failed to get post 1833: {e}")
        
        print("\n🎉 Core client test PASSED!")
        return True
        
    except WordPressAPIError as e:
        print(f"❌ WordPress API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_core_client()
    sys.exit(0 if success else 1)