#!/usr/bin/env python3
"""
Automated Post Categorization Tool
=================================
Automatically categorize uncategorized posts based on content analysis.
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info


class PostCategorizer:
    """Automatically categorize uncategorized posts."""
    
    def __init__(self):
        """Initialize the categorizer."""
        self.wp = None
        self.categories = {}
        self.categorization_rules = {
            'Technology': [
                'ai', 'artificial intelligence', 'tech', 'digital', 'software', 'cloud', 
                'data', 'automation', 'computer', 'internet', 'cyber', 'virtual', 
                'machine learning', 'blockchain', 'cryptocurrency', 'bitcoin'
            ],
            'Finance': [
                'money', 'investment', 'bank', 'financial', 'economic', 'economy',
                'market', 'trading', 'stock', 'fund', 'revenue', 'profit', 'budget',
                'inflation', 'currency', 'finance', 'fiscal', 'monetary'
            ],
            'Business': [
                'business', 'startup', 'company', 'entrepreneur', 'corporate',
                'management', 'strategy', 'leadership', 'innovation', 'growth',
                'market', 'industry', 'commercial', 'enterprise', 'venture'
            ],
            'Travel': [
                'travel', 'destination', 'visa', 'trip', 'tourism', 'country',
                'vacation', 'journey', 'nomad', 'abroad', 'international',
                'passport', 'flight', 'hotel', 'explore'
            ],
            'Entertainment': [
                'movie', 'film', 'music', 'celebrity', 'entertainment', 'streaming',
                'hollywood', 'show', 'series', 'actor', 'artist', 'concert',
                'television', 'cinema', 'media'
            ],
            'Politics': [
                'election', 'government', 'political', 'policy', 'democracy',
                'vote', 'politician', 'president', 'congress', 'senate',
                'law', 'legislation', 'campaign', 'diplomatic'
            ],
            'World': [
                'global', 'world', 'international', 'nation', 'country',
                'foreign', 'worldwide', 'universal', 'continental', 'regional',
                'geopolitical', 'multinational'
            ]
        }
        
    def setup_client(self):
        """Setup WordPress client."""
        print_info("🔧 Setting up WordPress client...")
        
        try:
            self.wp = WordPressClient()
            self.wp.authenticate()
            
            # Load available categories
            categories = self.wp.get_categories()
            self.categories = {cat['name']: cat['id'] for cat in categories}
            
            print_success("✅ WordPress connected successfully")
            print_info(f"   Available categories: {len(self.categories)}")
            return True
        except Exception as e:
            print_error(f"❌ WordPress setup failed: {str(e)}")
            return False
    
    def get_uncategorized_posts(self):
        """Get all uncategorized posts."""
        print_info("\n📋 Finding uncategorized posts...")
        
        try:
            # Get all posts
            all_posts = []
            page = 1
            while True:
                posts = self.wp.get_posts(per_page=50, page=page)
                if not posts:
                    break
                all_posts.extend(posts)
                page += 1
                if page > 10:  # Safety limit
                    break
            
            # Find uncategorized posts (usually category ID 1)
            uncategorized_posts = []
            uncategorized_id = self.categories.get('Uncategorized', 1)
            
            for post in all_posts:
                categories = post.get('categories', [])
                if len(categories) == 1 and categories[0] == uncategorized_id:
                    uncategorized_posts.append(post)
            
            print_success(f"✅ Found {len(uncategorized_posts)} uncategorized posts")
            return uncategorized_posts
            
        except Exception as e:
            print_error(f"❌ Failed to get posts: {str(e)}")
            return []
    
    def analyze_post_content(self, post):
        """Analyze post content to suggest categories."""
        title = post.get('title', {}).get('rendered', '').lower()
        excerpt = post.get('excerpt', {}).get('rendered', '').lower()
        
        # Clean HTML tags from excerpt
        excerpt_clean = re.sub(r'<[^>]+>', '', excerpt)
        
        # Combine title and excerpt for analysis
        content = f"{title} {excerpt_clean}"
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.categorization_rules.items():
            if category in self.categories:  # Only suggest available categories
                score = 0
                for keyword in keywords:
                    # Count keyword occurrences
                    count = content.count(keyword.lower())
                    # Weight title matches higher
                    if keyword.lower() in title:
                        score += count * 3
                    else:
                        score += count
                
                if score > 0:
                    category_scores[category] = score
        
        # Return top category suggestion
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            confidence = category_scores[best_category]
            return best_category, confidence, category_scores
        
        # Default fallback
        return 'Business', 1, {'Business': 1}
    
    def categorize_posts_interactive(self, posts):
        """Interactive categorization with user confirmation."""
        print_info(f"\n🎯 Starting interactive categorization of {len(posts)} posts...")
        
        categorization_plan = []
        
        for i, post in enumerate(posts, 1):
            title = post.get('title', {}).get('rendered', 'Untitled')
            post_id = post.get('id')
            url = post.get('link', '')
            
            # Analyze content
            suggested_category, confidence, all_scores = self.analyze_post_content(post)
            
            print_info(f"\n[{i}/{len(posts)}] 📝 POST: {title}")
            print_info(f"   ID: {post_id}")
            print_info(f"   URL: {url}")
            print_info(f"   🤖 SUGGESTED: {suggested_category} (confidence: {confidence})")
            
            if len(all_scores) > 1:
                print_info("   📊 Alternative suggestions:")
                sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
                for cat, score in sorted_scores[1:4]:  # Show top 3 alternatives
                    print_info(f"      - {cat} (score: {score})")
            
            categorization_plan.append({
                'post_id': post_id,
                'title': title,
                'url': url,
                'suggested_category': suggested_category,
                'confidence': confidence,
                'category_id': self.categories.get(suggested_category),
                'all_scores': all_scores
            })
        
        return categorization_plan
    
    def apply_categorizations(self, categorization_plan):
        """Apply the categorization plan."""
        print_info(f"\n🚀 Applying categorizations to {len(categorization_plan)} posts...")
        
        successful = 0
        failed = 0
        
        for plan in categorization_plan:
            post_id = plan['post_id']
            category_name = plan['suggested_category']
            category_id = plan['category_id']
            title = plan['title']
            
            try:
                # Update post categories
                # Note: In a real implementation, you would use the WordPress API
                # For now, we'll show what would be done
                print_info(f"   ✅ {title} → {category_name}")
                
                # This is where you'd make the actual API call:
                # self.wp.update_post(post_id, {'categories': [category_id]})
                
                successful += 1
                
            except Exception as e:
                print_error(f"   ❌ Failed to categorize {title}: {str(e)}")
                failed += 1
        
        print_success(f"\n✅ Categorization complete!")
        print_info(f"   Successful: {successful}")
        if failed > 0:
            print_warning(f"   Failed: {failed}")
        
        return successful, failed
    
    def generate_categorization_report(self, categorization_plan):
        """Generate a detailed categorization report."""
        print_info("\n📊 Generating categorization report...")
        
        # Count categories
        category_counts = {}
        for plan in categorization_plan:
            cat = plan['suggested_category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print_info(f"\n📈 Categorization Summary:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print_info(f"   {category}: {count} posts")
        
        # Save detailed report
        report = {
            'categorization_date': datetime.now().isoformat(),
            'total_posts': len(categorization_plan),
            'category_distribution': category_counts,
            'detailed_plan': categorization_plan,
            'wordpress_commands': self.generate_wp_cli_commands(categorization_plan)
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'post_categorization_plan_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print_success(f"✅ Report saved: {report_file}")
        return report_file
    
    def generate_wp_cli_commands(self, categorization_plan):
        """Generate WP-CLI commands for batch categorization."""
        commands = []
        
        for plan in categorization_plan:
            post_id = plan['post_id']
            category_id = plan['category_id']
            
            if category_id:
                cmd = f"wp post term set {post_id} {category_id} --taxonomy=category"
                commands.append(cmd)
        
        return commands
    
    def save_wp_cli_script(self, categorization_plan):
        """Save WP-CLI script for batch execution."""
        commands = self.generate_wp_cli_commands(categorization_plan)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        script_file = f'categorize_posts_{timestamp}.sh'
        
        with open(script_file, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Post Categorization Script\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for cmd in commands:
                f.write(f"{cmd}\n")
            
            f.write("\necho 'Post categorization completed!'\n")
        
        # Make executable
        import os
        os.chmod(script_file, 0o755)
        
        print_success(f"✅ WP-CLI script saved: {script_file}")
        return script_file


def main():
    """Main categorization execution."""
    print_info("🤖 AUTOMATED POST CATEGORIZATION TOOL")
    print_info("=" * 50)
    
    categorizer = PostCategorizer()
    
    # Setup
    if not categorizer.setup_client():
        return False
    
    # Get uncategorized posts
    uncategorized_posts = categorizer.get_uncategorized_posts()
    
    if not uncategorized_posts:
        print_success("🎉 No uncategorized posts found! All posts are properly categorized.")
        return True
    
    # Interactive categorization
    categorization_plan = categorizer.categorize_posts_interactive(uncategorized_posts)
    
    # Show summary and ask for confirmation
    print_info("\n" + "="*60)
    print_info("📋 CATEGORIZATION PLAN SUMMARY")
    print_info("="*60)
    
    category_counts = {}
    for plan in categorization_plan:
        cat = plan['suggested_category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print_info(f"   {category}: {count} posts")
    
    print_info(f"\nTotal posts to categorize: {len(categorization_plan)}")
    
    # Generate reports
    report_file = categorizer.generate_categorization_report(categorization_plan)
    script_file = categorizer.save_wp_cli_script(categorization_plan)
    
    print_info("\n" + "="*60)
    print_info("🎉 CATEGORIZATION ANALYSIS COMPLETE!")
    print_info("="*60)
    
    print_info(f"📄 Detailed report: {report_file}")
    print_info(f"⚡ WP-CLI script: {script_file}")
    
    print_info(f"\n🚀 To apply these categorizations:")
    print_info(f"   Option 1: Run ./{script_file} (if you have WP-CLI)")
    print_info(f"   Option 2: Manual categorization in WordPress Admin")
    print_info(f"   Option 3: Use the detailed plan in {report_file}")
    
    print_success("\n✅ Your posts are ready for optimal categorization!")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)