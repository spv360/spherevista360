#!/usr/bin/env python3
"""
Test script for 404 error handling and fallback image URLs
"""

import sys
sys.path.append('./scripts')

from image_validator import ImageValidator
from wp_agent_bulk import validate_remote_image

def test_url_verification():
    """Test the URL verification functionality"""
    print("=== Testing URL Verification ===")
    
    validator = ImageValidator()
    
    # Test a working URL
    working_url = "https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80"
    is_ok, msg = validator.verify_image_url(working_url)
    print(f"Working URL: {is_ok} - {msg}")
    
    # Test a 404 URL
    broken_url = "https://images.unsplash.com/photo-nonexistent-12345.jpg"
    is_ok, msg = validator.verify_image_url(broken_url)
    print(f"404 URL: {is_ok} - {msg}")
    
    # Test fallback generation
    print("\n=== Testing Fallback URL Generation ===")
    fallback_urls = validator.get_multiple_fallback_urls("Finance", ["chart", "business"], count=2)
    for i, url in enumerate(fallback_urls):
        print(f"Fallback {i+1}: {url}")

def test_validate_remote_image():
    """Test the complete validate_remote_image with 404 handling"""
    print("\n=== Testing Complete Validation with 404 Handling ===")
    
    # Test with a broken URL that should trigger fallback
    broken_url = "https://images.unsplash.com/photo-broken-url-12345.jpg"
    metadata = {
        'category': 'Finance',
        'keywords': ['chart', 'business'],
        'title': 'Test Finance Article',
        'alt': 'Financial chart showing growth'
    }
    
    print(f"Testing broken URL: {broken_url}")
    is_valid, messages = validate_remote_image(broken_url, metadata)
    print(f"Result: {is_valid}")
    for msg in messages:
        print(f"  - {msg}")

if __name__ == "__main__":
    test_url_verification()
    test_validate_remote_image()
