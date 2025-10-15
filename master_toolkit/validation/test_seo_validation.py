#!/usr/bin/env python3
"""
Test Enhanced SEO Validation
============================
Quick test of the enhanced SEO validation capabilities.
"""

import sys
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent.parent))

from master_toolkit.validation.seo import SEOValidator
from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_header, print_success, print_error


def test_seo_validation():
    """Test the enhanced SEO validation functionality."""
    print_header("🔍 Testing Enhanced SEO Validation")
    
    try:
        # Test with authenticated client
        wp_client = WordPressClient()
        validator = SEOValidator(wp_client)
        
        # Test structured data validation for a specific post
        print("\n📋 Testing structured data validation for post 20...")
        structured_result = validator.validate_structured_data(20)
        
        if structured_result.get('success', True):
            print_success("Structured data validation completed!")
            print(f"   Status: {structured_result.get('status', 'unknown')}")
            print(f"   Score: {structured_result.get('score', 0)}/100")
            if structured_result.get('message'):
                print(f"   Message: {structured_result.get('message')}")
            
            # Show detailed results
            structured_data = structured_result.get('structured_data', {})
            print(f"   JSON-LD found: {structured_data.get('json_ld_found', False)}")
            print(f"   Article schema valid: {structured_data.get('article_schema_valid', False)}")
            
        else:
            print_error(f"Structured data validation failed: {structured_result.get('error', 'Unknown error')}")
        
        # Test canonical tag validation
        print("\n🔗 Testing canonical tag validation for post 20...")
        canonical_result = validator.validate_canonical_tags(20)
        
        if canonical_result.get('success', True):
            print_success("Canonical tag validation completed!")
            print(f"   Status: {canonical_result.get('status', 'unknown')}")
            print(f"   Score: {canonical_result.get('score', 0)}/100")
            if canonical_result.get('message'):
                print(f"   Message: {canonical_result.get('message')}")
            
            # Show detailed results
            canonical_data = canonical_result.get('canonical', {})
            print(f"   Canonical tag found: {canonical_data.get('canonical_found', False)}")
            print(f"   URL matches post: {canonical_data.get('url_matches_post', False)}")
            
        else:
            print_error(f"Canonical tag validation failed: {canonical_result.get('error', 'Unknown error')}")
        
        print_success("\n✅ Enhanced SEO validation test completed!")
        
    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_seo_validation()