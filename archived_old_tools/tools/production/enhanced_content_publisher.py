#!/usr/bin/env python3
"""
Enhanced Content Publisher
==========================
Production-ready content publishing system with templates and automation.
"""

import os
import sys
import yaml
import markdown
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import re
from datetime import datetime
from slugify import slugify

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))
from enhanced_wp_client import WordPressClient, print_header, print_section


class ContentPublisher:
    """Enhanced content publishing system."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize publisher."""
        self.wp = wp_client or WordPressClient()
        self.image_templates = {
            'technology': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'entertainment': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'finance': 'https://images.unsplash.com/photo-1559589688-f26e20a6c987?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'business': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'travel': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'politics': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'world': 'https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'default': 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80'
        }
        
    def parse_markdown_file(self, file_path: str) -> Dict:
        """Parse markdown file with front matter."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1]) or {}
                    markdown_content = parts[2].strip()
                else:
                    front_matter = {}
                    markdown_content = content
            else:
                front_matter = {}
                markdown_content = content
            
            # Extract title from markdown if not in front matter
            if not front_matter.get('title'):
                title_match = re.match(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
                if title_match:
                    front_matter['title'] = title_match.group(1).strip()
                    # Remove the title from content to avoid duplication
                    markdown_content = re.sub(r'^#\s+.+\n?', '', markdown_content, count=1)
            
            # Convert markdown to HTML
            html_content = markdown.markdown(markdown_content)
            
            return {
                'title': front_matter.get('title', 'Untitled'),
                'content': html_content,
                'category': front_matter.get('category'),
                'tags': front_matter.get('tags', []),
                'status': front_matter.get('status', 'publish'),
                'featured_image': front_matter.get('featured_image'),
                'excerpt': front_matter.get('excerpt'),
                'meta': front_matter
            }
            
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return {}
    
    def add_featured_image(self, content: str, category: str, title: str) -> str:
        """Add featured image to content."""
        # Get appropriate image URL
        image_url = self.image_templates.get(category.lower(), self.image_templates['default'])
        
        # Create alt text from title
        alt_text = title.replace('&#8217;', "'").replace('&amp;', '&')
        
        # Create image HTML
        image_html = f'''<p><img alt="{alt_text}" decoding="async" src="{image_url}" style="width: 100%; height: auto; max-width: 1600px; border-radius: 8px; margin: 20px 0;" title="{alt_text}"/></p>'''
        
        return image_html + '\n\n' + content
    
    def add_internal_links(self, content: str, category: str) -> str:
        """Add strategic internal links to content."""
        # Get available posts for linking
        posts = self.wp.get_posts(per_page=50)
        
        # Create a mapping of keywords to posts
        link_map = {}
        for post in posts:
            title = post.get('title', {}).get('rendered', '').lower()
            slug = post.get('slug', '')
            url = f"https://spherevista360.com/{slug}/"
            
            # Map keywords to URLs
            if 'ai' in title or 'artificial intelligence' in title:
                link_map['AI technology'] = url
                link_map['artificial intelligence'] = url
            if 'cloud' in title:
                link_map['cloud technology'] = url
                link_map['cloud platforms'] = url
            if 'streaming' in title:
                link_map['streaming platforms'] = url
                link_map['entertainment industry'] = url
            if 'global' in title:
                link_map['global market'] = url
                link_map['global trends'] = url
        
        # Add links strategically
        for keyword, url in link_map.items():
            if keyword.lower() in content.lower() and url not in content:
                # Replace first occurrence
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                if pattern.search(content):
                    content = pattern.sub(f'<a href="{url}">{keyword}</a>', content, count=1)
                    break  # Add only one link per post to avoid over-optimization
        
        return content
    
    def publish_file(self, file_path: str, category: str = None, dry_run: bool = False) -> Dict:
        """Publish a single markdown file."""
        parsed = self.parse_markdown_file(file_path)
        if not parsed:
            return {'success': False, 'error': 'Failed to parse file'}
        
        title = parsed['title']
        content = parsed['content']
        post_category = category or parsed.get('category') or 'Uncategorized'
        
        # Check for existing post with similar title
        existing_posts = self.wp.get_posts(per_page=50)
        for post in existing_posts:
            existing_title = post.get('title', {}).get('rendered', '')
            if self._similarity_score(title, existing_title) > 0.8:
                return {
                    'success': False, 
                    'error': f'duplicate_title - Similar post exists: {existing_title}'
                }
        
        if dry_run:
            return {
                'success': True,
                'action': 'dry_run',
                'title': title,
                'category': post_category,
                'content_length': len(content)
            }
        
        # Enhance content
        content = self.add_featured_image(content, post_category, title)
        content = self.add_internal_links(content, post_category)
        
        # Publish to WordPress
        result = self.wp.create_post(
            title=title,
            content=content,
            categories=[post_category],
            tags=parsed.get('tags', []),
            status=parsed.get('status', 'publish')
        )
        
        if result and result.get('id'):
            return {
                'success': True,
                'id': result['id'],
                'title': title,
                'url': result.get('link', '')
            }
        else:
            return {'success': False, 'error': 'WordPress API error'}
    
    def publish_directory(self, directory: str, category: str = None, dry_run: bool = False) -> Dict:
        """Publish all markdown files in a directory."""
        directory_path = Path(directory)
        if not directory_path.exists():
            return {'success': False, 'error': f'Directory not found: {directory}'}
        
        md_files = list(directory_path.glob('*.md'))
        if not md_files:
            return {'success': False, 'error': 'No markdown files found'}
        
        results = {'successful': [], 'failed': []}
        
        print_section(f"PUBLISHING DIRECTORY: {directory}")
        print(f"📁 Found {len(md_files)} markdown files")
        
        for file_path in md_files:
            print(f"\n📄 Processing: {file_path.name}")
            
            result = self.publish_file(str(file_path), category, dry_run)
            
            if result['success']:
                results['successful'].append(result)
                if dry_run:
                    print(f"📝 DRY RUN: Would publish '{result['title']}'")
                else:
                    print(f"✅ Published: {result['title']} (ID: {result['id']})")
            else:
                results['failed'].append({'file': file_path.name, 'error': result['error']})
                print(f"❌ Failed: {result['error']}")
        
        return results
    
    def _similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings."""
        # Simple similarity based on common words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Enhanced Content Publisher')
    parser.add_argument('path', help='Path to markdown file or directory')
    parser.add_argument('--category', help='Target category for posts')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')
    parser.add_argument('--username', help='WordPress username')
    parser.add_argument('--password', help='WordPress application password')
    
    args = parser.parse_args()
    
    print_header("ENHANCED CONTENT PUBLISHER")
    
    # Initialize WordPress client
    wp = WordPressClient()
    if not wp.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    # Initialize publisher
    publisher = ContentPublisher(wp)
    
    # Determine if path is file or directory
    path = Path(args.path)
    
    if path.is_file():
        result = publisher.publish_file(str(path), args.category, args.dry_run)
        if result['success']:
            print("✅ File processed successfully")
        else:
            print(f"❌ Failed: {result['error']}")
    elif path.is_dir():
        results = publisher.publish_directory(str(path), args.category, args.dry_run)
        
        print_section("PUBLICATION SUMMARY")
        successful = len(results['successful'])
        failed = len(results['failed'])
        total = successful + failed
        
        print(f"   ✅ Successful: {successful}/{total}")
        print(f"   ❌ Failed: {failed}/{total}")
        
        if results['failed']:
            print(f"\n🚨 FAILURES:")
            for failure in results['failed']:
                print(f"   ❌ {failure['file']}: {failure['error']}")
    else:
        print(f"❌ Path not found: {args.path}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())