#!/usr/bin/env python3
"""
Post Categorization Tool
========================
Help categorize uncategorized posts for better AdSense performance.
"""

import sys
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def suggest_post_categories():
    """Suggest categories for uncategorized posts."""
    print_info("📂 POST CATEGORIZATION HELPER")
    print_info("=" * 40)
    
    try:
        wp = WordPressClient()
        wp.authenticate()
        
        # Get uncategorized posts
        posts = wp.get_posts(per_page=100)
        uncategorized_posts = []
        
        for post in posts:
            categories = post.get('categories', [])
            # Check if post only has 'Uncategorized' category (usually ID 1)
            if len(categories) == 1 and categories[0] == 1:
                uncategorized_posts.append(post)
        
        if not uncategorized_posts:
            print_success("✅ No uncategorized posts found!")
            return
        
        print_info(f"📊 Found {len(uncategorized_posts)} uncategorized posts:")
        print_info("\n📋 CATEGORIZATION SUGGESTIONS:")
        
        # Get available categories for suggestions
        categories = wp.get_categories()
        active_categories = {cat['name']: cat['id'] for cat in categories if cat.get('count', 0) > 0}
        
        for i, post in enumerate(uncategorized_posts[:10], 1):  # Show first 10
            title = post.get('title', {}).get('rendered', 'Untitled')
            content = post.get('excerpt', {}).get('rendered', '')
            
            # Suggest category based on title keywords
            suggested_category = suggest_category_from_title(title, active_categories.keys())
            
            print_info(f"\n{i}. POST: {title}")
            print_info(f"   ID: {post.get('id')}")
            print_info(f"   URL: {post.get('link')}")
            print_info(f"   SUGGESTED CATEGORY: {suggested_category}")
            
        print_info(f"\n🎯 MANUAL CATEGORIZATION STEPS:")
        print_info("   1. Go to Posts > All Posts in WordPress Admin")
        print_info("   2. Use Quick Edit to assign categories")
        print_info("   3. Or edit each post individually")
        
        print_info(f"\n📈 AVAILABLE CATEGORIES:")
        for cat_name in sorted(active_categories.keys()):
            print_info(f"   - {cat_name}")
        
        print_success("\n✅ Proper categorization will boost your AdSense performance!")
        
    except Exception as e:
        print_error(f"❌ Error: {str(e)}")


def suggest_category_from_title(title, available_categories):
    """Suggest category based on post title."""
    title_lower = title.lower()
    
    # Category keyword mapping
    category_keywords = {
        'Technology': ['ai', 'tech', 'digital', 'software', 'computer', 'internet', 'cloud', 'data'],
        'Finance': ['money', 'investment', 'bank', 'finance', 'economic', 'market', 'trading', 'crypto'],
        'Business': ['business', 'startup', 'company', 'entrepreneur', 'corporate', 'management'],
        'Travel': ['travel', 'destination', 'visa', 'trip', 'tourism', 'country', 'vacation'],
        'Entertainment': ['movie', 'music', 'celebrity', 'entertainment', 'streaming', 'hollywood'],
        'Politics': ['election', 'government', 'political', 'policy', 'democracy', 'vote'],
        'World': ['global', 'world', 'international', 'nation', 'country']
    }
    
    # Find best match
    for category, keywords in category_keywords.items():
        if category in available_categories:
            for keyword in keywords:
                if keyword in title_lower:
                    return category
    
    # Default suggestions based on common patterns
    if any(word in title_lower for word in ['how', 'guide', 'tips']):
        return 'Business'  # How-to content often fits business
    elif any(word in title_lower for word in ['2025', '2024', 'future', 'trend']):
        return 'Technology'  # Future-focused content
    
    return 'Business'  # Safe default for general content


if __name__ == '__main__':
    suggest_post_categories()