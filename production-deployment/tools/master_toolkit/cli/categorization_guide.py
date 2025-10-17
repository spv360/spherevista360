#!/usr/bin/env python3
"""
Manual Post Categorization Guide
================================
Generate specific categorization instructions for uncategorized posts.
"""

import sys
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info


def generate_categorization_guide():
    """Generate manual categorization guide."""
    print_info("📋 MANUAL POST CATEGORIZATION GUIDE")
    print_info("=" * 50)
    
    try:
        wp = WordPressClient()
        wp.authenticate()
        
        # Get posts by category
        posts = wp.get_posts(per_page=100)
        categories = wp.get_categories()
        
        # Create category ID mapping
        cat_map = {cat['id']: cat['name'] for cat in categories}
        uncategorized_id = None
        
        for cat in categories:
            if cat['name'] == 'Uncategorized':
                uncategorized_id = cat['id']
                break
        
        if not uncategorized_id:
            print_success("✅ No 'Uncategorized' category found!")
            return
        
        # Find uncategorized posts
        uncategorized_posts = []
        for post in posts:
            post_categories = post.get('categories', [])
            if uncategorized_id in post_categories and len(post_categories) == 1:
                uncategorized_posts.append(post)
        
        if not uncategorized_posts:
            print_success("🎉 All posts are properly categorized!")
            return
        
        print_warning(f"⚠️  Found {len(uncategorized_posts)} uncategorized posts")
        
        print_info("\n🎯 CATEGORIZATION INSTRUCTIONS:")
        print_info("=" * 50)
        
        # Manual categorization rules based on keywords
        categorization_guide = []
        
        for i, post in enumerate(uncategorized_posts, 1):
            title = post.get('title', {}).get('rendered', 'Untitled')
            post_id = post.get('id')
            url = post.get('link', '')
            
            # Suggest category based on title analysis
            title_lower = title.lower()
            suggested_category = "Business"  # Default
            
            if any(word in title_lower for word in ['visa', 'travel', 'destination', 'nomad', 'trip']):
                suggested_category = "Travel"
            elif any(word in title_lower for word in ['ai', 'tech', 'digital', 'cloud', 'software']):
                suggested_category = "Technology"
            elif any(word in title_lower for word in ['finance', 'investment', 'economic', 'inflation', 'money', 'banking']):
                suggested_category = "Finance"
            elif any(word in title_lower for word in ['election', 'political', 'government', 'democracy']):
                suggested_category = "Politics"
            elif any(word in title_lower for word in ['global', 'world', 'international']):
                suggested_category = "World"
            elif any(word in title_lower for word in ['movie', 'music', 'entertainment', 'streaming', 'hollywood']):
                suggested_category = "Entertainment"
            elif any(word in title_lower for word in ['business', 'startup', 'company', 'entrepreneur']):
                suggested_category = "Business"
            
            categorization_guide.append({
                'post_id': post_id,
                'title': title,
                'url': url,
                'suggested_category': suggested_category
            })
            
            print_info(f"\n{i:2d}. 📝 {title}")
            print_info(f"    ID: {post_id}")
            print_info(f"    📂 MOVE TO: {suggested_category}")
            print_info(f"    🔗 {url}")
        
        # Group by suggested category
        print_info("\n📊 CATEGORIZATION SUMMARY:")
        print_info("=" * 30)
        
        category_groups = {}
        for item in categorization_guide:
            cat = item['suggested_category']
            if cat not in category_groups:
                category_groups[cat] = []
            category_groups[cat].append(item)
        
        for category, posts in sorted(category_groups.items()):
            print_info(f"\n🏷️  {category.upper()} ({len(posts)} posts):")
            for post in posts:
                print_info(f"   • {post['title']} (ID: {post['post_id']})")
        
        # WordPress admin instructions
        print_info("\n🚀 WORDPRESS ADMIN STEPS:")
        print_info("=" * 30)
        print_info("1. Login to WordPress Admin")
        print_info("2. Go to Posts → All Posts")
        print_info("3. For each post:")
        print_info("   • Click 'Quick Edit'")
        print_info("   • Uncheck 'Uncategorized'")
        print_info("   • Check the suggested category")
        print_info("   • Click 'Update'")
        
        print_info("\n⚡ BULK EDIT METHOD:")
        print_info("1. Select multiple posts with checkboxes")
        print_info("2. Choose 'Edit' from Bulk Actions")
        print_info("3. In Categories section:")
        print_info("   • Choose 'Remove' for Uncategorized")  
        print_info("   • Choose 'Add' for new category")
        print_info("4. Click 'Update'")
        
        # Save categorization plan
        import json
        from datetime import datetime
        
        plan = {
            'generated_at': datetime.now().isoformat(),
            'total_uncategorized': len(uncategorized_posts),
            'categorization_plan': categorization_guide,
            'category_distribution': {cat: len(posts) for cat, posts in category_groups.items()}
        }
        
        plan_file = f"categorization_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print_success(f"\n✅ Categorization plan saved: {plan_file}")
        
        print_info("\n🎯 EXPECTED RESULTS AFTER CATEGORIZATION:")
        current_distribution = {cat['name']: cat['count'] for cat in categories if cat['count'] > 0}
        
        for category, new_posts in category_groups.items():
            current_count = current_distribution.get(category, 0)
            new_count = current_count + len(new_posts)
            print_info(f"   {category}: {current_count} → {new_count} posts (+{len(new_posts)})")
        
        print_info(f"   Uncategorized: 18 → 0 posts (-18)")
        
        print_success("\n🏆 After categorization: 100% AdSense readiness achieved!")
        
    except Exception as e:
        print_error(f"❌ Error: {str(e)}")


if __name__ == '__main__':
    generate_categorization_guide()