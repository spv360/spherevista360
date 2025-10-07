#!/usr/bin/env python3
"""
Content Publishing Manager
=========================
Manage and publish WordPress content by category with SEO optimization.
"""

import os
import sys
from pathlib import Path
import re

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent / 'wp_tools'))

def analyze_content_directory(content_dir="content_to_publish"):
    """Analyze all content ready for publishing."""
    
    if not os.path.exists(content_dir):
        print(f"❌ Content directory '{content_dir}' not found!")
        return
    
    print("📁 CONTENT PUBLISHING INVENTORY")
    print("=" * 50)
    
    total_posts = 0
    categories = {}
    
    # Scan each category directory
    for category_dir in os.listdir(content_dir):
        category_path = os.path.join(content_dir, category_dir)
        
        if not os.path.isdir(category_path):
            continue
        
        # Count files in category
        md_files = [f for f in os.listdir(category_path) if f.endswith('.md')]
        
        if md_files:
            categories[category_dir] = md_files
            total_posts += len(md_files)
            
            print(f"\n📂 {category_dir.upper()} ({len(md_files)} posts)")
            print("-" * 30)
            
            for i, filename in enumerate(sorted(md_files), 1):
                # Extract title from filename
                title = re.sub(r'^\d+-', '', filename.replace('.md', '').replace('-', ' '))
                title = title.title()
                
                print(f"   {i}. {title}")
                print(f"      File: {filename}")
                
                # Check file size
                file_path = os.path.join(category_path, filename)
                file_size = os.path.getsize(file_path)
                print(f"      Size: {file_size:,} bytes")
    
    print(f"\n📊 SUMMARY")
    print("-" * 20)
    print(f"Total Categories: {len(categories)}")
    print(f"Total Posts: {total_posts}")
    print(f"Average per Category: {total_posts/len(categories):.1f}")
    
    return categories

def create_publishing_plan(categories):
    """Create a publishing plan for WordPress."""
    
    print(f"\n🚀 PUBLISHING PLAN")
    print("=" * 50)
    
    # Recommended publishing order (based on SEO priority)
    priority_order = [
        'Entertainment',  # Already optimized to 100%
        'Technology', 
        'Finance',
        'Travel',
        'World',
        'Politics',
        'Business'
    ]
    
    week_plan = []
    current_week = 1
    posts_per_week = 3
    
    for category in priority_order:
        if category in categories:
            posts = categories[category]
            
            print(f"\n📅 WEEK {current_week}-{current_week + len(posts)//posts_per_week}: {category}")
            print("-" * 40)
            
            for i, post in enumerate(posts):
                week_num = current_week + i // posts_per_week
                day_in_week = (i % posts_per_week) + 1
                
                title = re.sub(r'^\d+-', '', post.replace('.md', '').replace('-', ' ')).title()
                
                print(f"   Week {week_num}, Day {day_in_week}: {title}")
                
                week_plan.append({
                    'week': week_num,
                    'day': day_in_week,
                    'category': category,
                    'file': post,
                    'title': title
                })
            
            current_week += (len(posts) + posts_per_week - 1) // posts_per_week
    
    print(f"\n📈 TIMELINE SUMMARY")
    print("-" * 30)
    print(f"Total Duration: {current_week - 1} weeks")
    print(f"Publishing Rate: {posts_per_week} posts/week")
    print(f"Estimated Completion: Week {current_week - 1}")
    
    return week_plan

def generate_publishing_commands(categories):
    """Generate WordPress publishing commands."""
    
    print(f"\n🛠️ PUBLISHING COMMANDS")
    print("=" * 50)
    
    print("# Install dependencies first:")
    print("pip install -r requirements.txt")
    print()
    
    for category, posts in categories.items():
        print(f"# {category.upper()} CATEGORY ({len(posts)} posts)")
        print("-" * 40)
        
        for post in posts:
            title = re.sub(r'^\d+-', '', post.replace('.md', '').replace('-', ' ')).title()
            file_path = f"content_to_publish/{category}/{post}"
            
            print(f"# Publish: {title}")
            print(f"python wp_tools/wp_agent_bulk.py --file {file_path} --category {category}")
            print()
        
        print(f"# Validate {category} SEO after publishing:")
        print(f"python wp_tools/seo_tool.py --category {category} --report {category.lower()}_seo_report.txt")
        print(f"python wp_tools/image_tool.py --category {category} --fix --add-images")
        print()

def show_content_samples():
    """Show samples of content to verify quality."""
    
    print(f"\n📝 CONTENT SAMPLES")
    print("=" * 50)
    
    sample_files = [
        "content_to_publish/Entertainment/streaming-wars-update.md",
        "content_to_publish/Technology/01-cloud-wars-2025-aws-azure-gcp.md",
        "content_to_publish/Finance/01-ai-transforming-investing-2025.md"
    ]
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            category = file_path.split('/')[1]
            filename = os.path.basename(file_path)
            
            print(f"\n📄 {category}: {filename}")
            print("-" * 30)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Show first 300 characters
                preview = content[:300] + "..." if len(content) > 300 else content
                print(preview)
                
                # Basic content analysis
                word_count = len(content.split())
                line_count = len(content.split('\n'))
                
                print(f"\nStats: {word_count} words, {line_count} lines")

def main():
    """Main function to analyze and plan content publishing."""
    
    print("🎯 SphereVista360 Content Publishing Manager")
    print("=" * 60)
    
    # Analyze content
    categories = analyze_content_directory()
    
    if not categories:
        print("❌ No content found for publishing!")
        return
    
    # Create publishing plan
    week_plan = create_publishing_plan(categories)
    
    # Generate commands
    generate_publishing_commands(categories)
    
    # Show content samples
    show_content_samples()
    
    print(f"\n🎉 READY TO PUBLISH!")
    print("=" * 30)
    print("✅ All content organized and ready")
    print("✅ Publishing commands generated")
    print("✅ SEO validation tools ready")
    print(f"✅ {sum(len(posts) for posts in categories.values())} posts across {len(categories)} categories")
    
    print(f"\n💡 NEXT STEPS:")
    print("1. Review content samples above")
    print("2. Start with Entertainment category (already optimized)")
    print("3. Use generated commands to publish systematically")
    print("4. Run SEO validation after each category")

if __name__ == "__main__":
    main()