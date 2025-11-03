#!/usr/bin/env python3
"""
Identify Priority Posts for Content Expansion
Analyzes posts and recommends which ones to expand first for AdSense approval
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'wordpress_core'))

from wordpress_utils import WordPressAPI, print_success, print_error, print_info, print_warning
import re
from datetime import datetime
import json

class PostAnalyzer:
    def __init__(self):
        self.wp = WordPressAPI()
    
    def analyze_all_posts(self):
        """Analyze all posts and categorize by priority"""
        print_info("Fetching all posts...")
        
        posts = self.wp.list_posts(per_page=100)
        if not posts:
            print_error("No posts found")
            return None
        
        analysis = {
            'critical': [],  # < 500 words
            'high': [],      # 500-799 words
            'medium': [],    # 800-999 words
            'low': []        # 1000+ words (already good)
        }
        
        print_info(f"Analyzing {len(posts)} posts...\n")
        
        for post in posts:
            if post['status'] != 'publish':
                continue
            
            content = re.sub(r'<[^>]+>', ' ', post['content']['rendered'])
            word_count = len(content.split())
            
            post_info = {
                'id': post['id'],
                'title': post['title']['rendered'],
                'words': word_count,
                'url': post['link'],
                'date': post['date']
            }
            
            if word_count < 500:
                analysis['critical'].append(post_info)
            elif word_count < 800:
                analysis['high'].append(post_info)
            elif word_count < 1000:
                analysis['medium'].append(post_info)
            else:
                analysis['low'].append(post_info)
        
        return analysis
    
    def print_analysis(self, analysis):
        """Print formatted analysis report"""
        print("\n" + "="*80)
        print("📊 CONTENT EXPANSION PRIORITY ANALYSIS")
        print("="*80)
        
        # Critical Priority
        print(f"\n🚨 CRITICAL PRIORITY (<500 words): {len(analysis['critical'])} posts")
        print("-"*80)
        if analysis['critical']:
            print("These MUST be expanded to 1500+ words for AdSense approval:\n")
            for i, post in enumerate(analysis['critical'][:10], 1):
                print(f"{i:2d}. [{post['id']:4d}] {post['title'][:50]:50s} - {post['words']:4d} words")
                print(f"     Need: +{1500-post['words']:4d} words | {post['url']}")
        
        # High Priority
        print(f"\n⚠️  HIGH PRIORITY (500-799 words): {len(analysis['high'])} posts")
        print("-"*80)
        if analysis['high']:
            print("These should be expanded to 1500+ words:\n")
            for i, post in enumerate(analysis['high'][:10], 1):
                print(f"{i:2d}. [{post['id']:4d}] {post['title'][:50]:50s} - {post['words']:4d} words")
                print(f"     Need: +{1500-post['words']:4d} words")
        
        # Medium Priority
        print(f"\n⚡ MEDIUM PRIORITY (800-999 words): {len(analysis['medium'])} posts")
        print("-"*80)
        if analysis['medium']:
            print("Close to target - expand to 1500+ words:\n")
            for i, post in enumerate(analysis['medium'][:10], 1):
                print(f"{i:2d}. [{post['id']:4d}] {post['title'][:50]:50s} - {post['words']:4d} words")
                print(f"     Need: +{1500-post['words']:4d} words")
        
        # Already Good
        print(f"\n✅ ALREADY GOOD (1000+ words): {len(analysis['low'])} posts")
        print("-"*80)
        if analysis['low']:
            print("These meet minimum standards (but could still be improved to 1500+):\n")
            for i, post in enumerate(analysis['low'][:5], 1):
                print(f"{i:2d}. [{post['id']:4d}] {post['title'][:50]:50s} - {post['words']:4d} words")
        
        # Summary
        total = len(analysis['critical']) + len(analysis['high']) + len(analysis['medium']) + len(analysis['low'])
        needs_work = len(analysis['critical']) + len(analysis['high']) + len(analysis['medium'])
        
        print("\n" + "="*80)
        print("📈 SUMMARY")
        print("="*80)
        print(f"Total Posts: {total}")
        print(f"Need Expansion (< 1000 words): {needs_work} ({needs_work/total*100:.1f}%)")
        print(f"Meet Minimum (1000+ words): {len(analysis['low'])} ({len(analysis['low'])/total*100:.1f}%)")
        print(f"\nTarget for AdSense: Expand {needs_work} posts to 1500+ words")
        print(f"Estimated work: {needs_work * 2} hours (assuming 2 hours per post)")
        print("="*80 + "\n")
    
    def generate_expansion_commands(self, analysis, top_n=30):
        """Generate ready-to-use expansion commands"""
        print("\n" + "="*80)
        print("🛠️  READY-TO-USE EXPANSION COMMANDS")
        print("="*80)
        
        # Combine critical and high priority
        priority_posts = analysis['critical'] + analysis['high']
        priority_posts = sorted(priority_posts, key=lambda x: x['words'])[:top_n]
        
        if not priority_posts:
            print("No posts need expansion!")
            return
        
        # Generate individual commands
        print(f"\n1️⃣  Expand Individual Posts (Top {min(5, len(priority_posts))}):")
        print("-"*80)
        for i, post in enumerate(priority_posts[:5], 1):
            cmd = f"python3 scripts/content_enhancement/content_expander.py --post-id {post['id']}"
            print(f"\n# {i}. {post['title'][:60]}")
            print(f"# Current: {post['words']} words → Target: 1500+ words")
            print(cmd)
        
        # Generate bulk command
        post_ids = [str(post['id']) for post in priority_posts[:30]]
        print(f"\n\n2️⃣  Bulk Expand Top {len(post_ids)} Posts:")
        print("-"*80)
        print("\n# This will expand all priority posts in one command")
        print("# WARNING: This may take 10-30 minutes")
        print(f"\npython3 scripts/content_enhancement/content_expander.py --post-ids {','.join(post_ids)}")
        
        # Generate phased approach
        print(f"\n\n3️⃣  Phased Approach (Recommended):")
        print("-"*80)
        
        phases = [
            ("Week 1: Critical Posts", priority_posts[:10]),
            ("Week 2: High Priority", priority_posts[10:20]),
            ("Week 3: Remaining Priority", priority_posts[20:30])
        ]
        
        for phase_name, posts in phases:
            if not posts:
                continue
            phase_ids = ','.join([str(p['id']) for p in posts])
            print(f"\n# {phase_name} ({len(posts)} posts)")
            print(f"python3 scripts/content_enhancement/content_expander.py --post-ids {phase_ids}")
        
        print("\n" + "="*80 + "\n")
    
    def save_report(self, analysis, filename='content_expansion_report.json'):
        """Save analysis report to JSON file"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'critical': len(analysis['critical']),
                'high': len(analysis['high']),
                'medium': len(analysis['medium']),
                'already_good': len(analysis['low']),
                'total': sum(len(v) for v in analysis.values())
            },
            'posts': analysis
        }
        
        filepath = os.path.join(os.path.dirname(__file__), '..', '..', filename)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print_success(f"Report saved to: {filepath}")
        return filepath

def main():
    analyzer = PostAnalyzer()
    
    print_info("Starting content analysis for AdSense readiness...\n")
    
    # Analyze all posts
    analysis = analyzer.analyze_all_posts()
    
    if not analysis:
        return
    
    # Print formatted analysis
    analyzer.print_analysis(analysis)
    
    # Generate expansion commands
    analyzer.generate_expansion_commands(analysis)
    
    # Save report
    analyzer.save_report(analysis)
    
    print_info("\n💡 Next Steps:")
    print_info("1. Start with critical priority posts (<500 words)")
    print_info("2. Use the bulk expand command above to process multiple posts")
    print_info("3. Review expanded content and customize as needed")
    print_info("4. Aim for 1500-2000+ words per post for AdSense approval\n")

if __name__ == "__main__":
    main()
