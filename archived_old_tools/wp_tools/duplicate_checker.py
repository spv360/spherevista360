#!/usr/bin/env python3
"""
Duplicate Post/Page Checker
==========================
Modern tool to detect duplicate posts and pages in WordPress using wp_tools framework.
"""

import sys
import argparse
from pathlib import Path
import re
from difflib import SequenceMatcher

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent / 'wp_tools'))

from wp_client import WordPressClient, print_header, print_section

class DuplicateChecker:
    """Check for duplicate posts and pages in WordPress."""
    
    def __init__(self, wp_client):
        """Initialize duplicate checker.
        
        Args:
            wp_client: WordPress client instance
        """
        self.wp_client = wp_client
    
    def check_duplicate_posts(self):
        """Check for duplicate posts."""
        print_section("CHECKING DUPLICATE POSTS")
        
        try:
            posts = self.wp_client.get_posts(per_page=100)
            print(f"📄 Found {len(posts)} posts to analyze")
            
            duplicates = self._find_content_duplicates(posts, 'post')
            self._report_duplicates(duplicates, 'Posts')
            
            return duplicates
            
        except Exception as e:
            print(f"❌ Error checking posts: {e}")
            return []
    
    def check_duplicate_pages(self):
        """Check for duplicate pages."""
        print_section("CHECKING DUPLICATE PAGES")
        
        try:
            pages = self.wp_client.get_pages(per_page=100)
            print(f"📄 Found {len(pages)} pages to analyze")
            
            duplicates = self._find_content_duplicates(pages, 'page')
            self._report_duplicates(duplicates, 'Pages')
            
            return duplicates
            
        except Exception as e:
            print(f"❌ Error checking pages: {e}")
            return []
    
    def _find_content_duplicates(self, items, item_type):
        """Find duplicates in a list of posts or pages."""
        duplicates = []
        
        # Group by similar titles
        title_groups = {}
        for item in items:
            title = item['title']['rendered']
            clean_title = self._clean_title(title)
            
            # Look for existing similar titles
            found_group = False
            for existing_title in title_groups:
                if self._titles_similar(clean_title, existing_title):
                    title_groups[existing_title].append(item)
                    found_group = True
                    break
            
            if not found_group:
                title_groups[clean_title] = [item]
        
        # Find groups with multiple items
        for title, group_items in title_groups.items():
            if len(group_items) > 1:
                # Check if they're actually duplicates
                duplicate_group = self._analyze_duplicate_group(group_items, item_type)
                if duplicate_group:
                    duplicates.append(duplicate_group)
        
        # Also check for exact URL duplicates
        url_duplicates = self._find_url_duplicates(items, item_type)
        duplicates.extend(url_duplicates)
        
        return duplicates
    
    def _clean_title(self, title):
        """Clean title for comparison."""
        # Remove HTML entities
        title = re.sub(r'&[^;]+;', '', title)
        # Remove numbers, dashes, and common suffixes
        title = re.sub(r'\s*-\s*\d+\s*$', '', title)
        title = re.sub(r'\s*\(\d+\)\s*$', '', title)
        # Convert to lowercase and remove extra spaces
        return ' '.join(title.lower().split())
    
    def _titles_similar(self, title1, title2, threshold=0.8):
        """Check if two titles are similar."""
        return SequenceMatcher(None, title1, title2).ratio() > threshold
    
    def _analyze_duplicate_group(self, items, item_type):
        """Analyze a group of potentially duplicate items."""
        if len(items) < 2:
            return None
        
        # Sort by date (oldest first)
        items.sort(key=lambda x: x['date'])
        
        duplicate_info = {
            'type': item_type,
            'original': items[0],  # Assume oldest is original
            'duplicates': items[1:],
            'similarity_scores': [],
            'recommended_action': 'review'
        }
        
        # Calculate similarity scores
        original_title = self._clean_title(items[0]['title']['rendered'])
        for dup_item in items[1:]:
            dup_title = self._clean_title(dup_item['title']['rendered'])
            similarity = SequenceMatcher(None, original_title, dup_title).ratio()
            duplicate_info['similarity_scores'].append(similarity)
        
        # Determine recommended action
        avg_similarity = sum(duplicate_info['similarity_scores']) / len(duplicate_info['similarity_scores'])
        if avg_similarity > 0.95:
            duplicate_info['recommended_action'] = 'delete_duplicates'
        elif avg_similarity > 0.8:
            duplicate_info['recommended_action'] = 'merge_content'
        
        return duplicate_info
    
    def _find_url_duplicates(self, items, item_type):
        """Find items with duplicate URLs/slugs."""
        url_groups = {}
        duplicates = []
        
        for item in items:
            slug = item['slug']
            if slug in url_groups:
                url_groups[slug].append(item)
            else:
                url_groups[slug] = [item]
        
        for slug, group_items in url_groups.items():
            if len(group_items) > 1:
                # Sort by date (oldest first)
                group_items.sort(key=lambda x: x['date'])
                
                duplicates.append({
                    'type': f'{item_type}_url_duplicate',
                    'slug': slug,
                    'original': group_items[0],
                    'duplicates': group_items[1:],
                    'recommended_action': 'delete_duplicates'
                })
        
        return duplicates
    
    def _report_duplicates(self, duplicates, content_type):
        """Report found duplicates."""
        if not duplicates:
            print(f"✅ No duplicate {content_type.lower()} found!")
            return
        
        print(f"🚨 Found {len(duplicates)} duplicate groups in {content_type.lower()}")
        
        for i, dup_group in enumerate(duplicates, 1):
            print(f"\n📋 Duplicate Group {i}:")
            print(f"   Type: {dup_group['type']}")
            
            # Original item
            original = dup_group['original']
            print(f"   🟢 Original: {original['title']['rendered']}")
            print(f"      ID: {original['id']}, Date: {original['date'][:10]}")
            print(f"      URL: {original['link']}")
            
            # Duplicate items
            duplicates_list = dup_group['duplicates']
            for j, dup_item in enumerate(duplicates_list):
                similarity = ""
                if 'similarity_scores' in dup_group and j < len(dup_group['similarity_scores']):
                    similarity = f" (Similarity: {dup_group['similarity_scores'][j]:.1%})"
                
                print(f"   🔴 Duplicate: {dup_item['title']['rendered']}{similarity}")
                print(f"      ID: {dup_item['id']}, Date: {dup_item['date'][:10]}")
                print(f"      URL: {dup_item['link']}")
            
            # Recommendation
            action = dup_group['recommended_action']
            if action == 'delete_duplicates':
                print(f"   💡 Recommendation: ❌ Delete duplicates (high similarity)")
            elif action == 'merge_content':
                print(f"   💡 Recommendation: 🔄 Review and merge content")
            else:
                print(f"   💡 Recommendation: 👀 Manual review needed")
    
    def generate_cleanup_commands(self, duplicates):
        """Generate cleanup commands for duplicates."""
        if not duplicates:
            return
        
        print_section("CLEANUP COMMANDS")
        
        print("# Commands to clean up duplicates:")
        print("# Review each command before running!")
        print()
        
        for i, dup_group in enumerate(duplicates, 1):
            print(f"# Duplicate Group {i}: {dup_group['original']['title']['rendered']}")
            
            if dup_group['recommended_action'] == 'delete_duplicates':
                for dup_item in dup_group['duplicates']:
                    item_type = 'post' if dup_group['type'] == 'post' else 'page'
                    print(f"# Delete duplicate: {dup_item['title']['rendered']}")
                    print(f"# python wp_tools/wp_client.py --delete-{item_type} {dup_item['id']}")
            
            print()


def main():
    """Main function for duplicate checking."""
    parser = argparse.ArgumentParser(description='WordPress Duplicate Content Checker')
    parser.add_argument('--posts', action='store_true', help='Check duplicate posts')
    parser.add_argument('--pages', action='store_true', help='Check duplicate pages')
    parser.add_argument('--all', action='store_true', help='Check both posts and pages')
    parser.add_argument('--cleanup-commands', action='store_true', help='Generate cleanup commands')
    parser.add_argument('--username', type=str, help='WordPress username')
    parser.add_argument('--password', type=str, help='WordPress application password')
    
    args = parser.parse_args()
    
    if not any([args.posts, args.pages, args.all]):
        args.all = True  # Default to checking everything
    
    print_header("DUPLICATE CONTENT CHECKER")
    
    # Initialize WordPress client
    wp_client = WordPressClient()
    if not wp_client.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    checker = DuplicateChecker(wp_client)
    all_duplicates = []
    
    # Check posts
    if args.posts or args.all:
        post_duplicates = checker.check_duplicate_posts()
        all_duplicates.extend(post_duplicates)
    
    # Check pages
    if args.pages or args.all:
        page_duplicates = checker.check_duplicate_pages()
        all_duplicates.extend(page_duplicates)
    
    # Generate cleanup commands if requested
    if args.cleanup_commands and all_duplicates:
        checker.generate_cleanup_commands(all_duplicates)
    
    # Summary
    print_section("SUMMARY")
    total_groups = len(all_duplicates)
    total_duplicates = sum(len(group['duplicates']) for group in all_duplicates)
    
    print(f"📊 Total duplicate groups found: {total_groups}")
    print(f"📊 Total duplicate items: {total_duplicates}")
    
    if total_groups > 0:
        print(f"\n💡 Next steps:")
        print(f"   1. Review each duplicate group carefully")
        print(f"   2. Use --cleanup-commands to generate deletion commands")
        print(f"   3. Always backup before deleting content")
    else:
        print("✅ No duplicates found - your content is clean!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())