#!/usr/bin/env python3
"""
Test Technical Validation
=========================
Quick test of the new technical validation capabilities.
"""

import sys
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent.parent))

from master_toolkit.validation.technical import TechnicalValidator
from master_toolkit.utils import print_header, print_success, print_error


def test_technical_validation():
    """Test the technical validation functionality."""
    print_header("🔧 Testing Technical Validation")
    
    try:
        validator = TechnicalValidator()
        
        # Test robots.txt validation
        print("\n🤖 Testing robots.txt validation...")
        robots_result = validator.validate_robots_txt()
        
        if robots_result.get('success', True):
            print_success("Robots.txt validation completed!")
            print(f"   Status: {robots_result.get('status', 'unknown')}")
            print(f"   Score: {robots_result.get('score', 0)}/100")
            if robots_result.get('message'):
                print(f"   Message: {robots_result.get('message')}")
        else:
            print_error(f"Robots.txt validation failed: {robots_result.get('error', 'Unknown error')}")
        
        # Test sitemap validation for a specific post (post ID 20)
        print("\n🗺️  Testing sitemap validation for post 20...")
        sitemap_result = validator.validate_sitemap_inclusion(20)
        
        if sitemap_result.get('success', True):
            print_success("Sitemap validation completed!")
            print(f"   Status: {sitemap_result.get('status', 'unknown')}")
            print(f"   Score: {sitemap_result.get('score', 0)}/100")
            if sitemap_result.get('message'):
                print(f"   Message: {sitemap_result.get('message')}")
        else:
            print_error(f"Sitemap validation failed: {sitemap_result.get('error', 'Unknown error')}")
        
        print_success("\n✅ Technical validation test completed!")
        
    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_technical_validation()