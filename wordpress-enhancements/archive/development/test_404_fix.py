#!/usr/bin/env python3
"""
Test the enhanced 404 handling
"""
import sys
sys.path.append('./scripts')

from wp_agent_bulk import validate_remote_image

def test_404_handling():
    """Test 404 handling with automatic fallback"""
    print("🧪 Testing 404 Error Handling with Fallback URLs")
    print("=" * 50)
    
    # Test with a broken URL that should trigger fallback
    broken_url = "https://images.unsplash.com/photo-1556741533-f6acd6477e9a?auto=format&fit=crop&w=800&h=500&q=80"
    
    metadata = {
        'category': 'Finance',
        'keywords': ['business', 'chart'],
        'title': 'Test Finance Article',
        'alt': 'Financial chart showing growth'
    }
    
    print(f"🔴 Testing broken URL: {broken_url}")
    print(f"📂 Category: {metadata['category']}")
    print(f"🔍 Keywords: {metadata['keywords']}")
    print()
    
    is_valid, messages = validate_remote_image(broken_url, metadata)
    
    print(f"📊 Validation Result: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    print("📝 Messages:")
    for msg in messages:
        print(f"  • {msg}")
    
    return is_valid

if __name__ == "__main__":
    test_404_handling()
