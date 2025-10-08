#!/usr/bin/env python3
"""
Content Publisher
================
Modern WordPress content publishing tool using wp_tools framework.
Handles markdown files with front matter and automatic optimization.
"""

import os
import sys
import argparse
import yaml
import markdown
import re
from pathlib import Path

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))

from wp_client import WordPressClient, print_header, print_section
from seo_validator import SEOValidator
from image_validator import ImageValidator


class ContentPublisher:
    """WordPress content publisher with automatic optimization."""
    
    def __init__(self, wp_client):
        """Initialize publisher.
        
        Args:
            wp_client: WordPress client instance
        """
        self.wp_client = wp_client
        self.seo_validator = SEOValidator()
        self.image_validator = ImageValidator(wp_client)
        
        # Category mapping
        self.category_map = {
            'entertainment': 'Entertainment',
            'technology': 'Technology', 
            'finance': 'Finance',
            'travel': 'Travel',
            'world': 'World',
            'politics': 'Politics',
            'business': 'Business'
        }
    
    def publish_file(self, file_path, category=None, dry_run=False):
        """Publish a single markdown file.
        
        Args:
            file_path: Path to markdown file
            category: Category name (optional, can be auto-detected)
            dry_run: If True, don't actually publish
            
        Returns:
            Dict with publication results
        """
        try:
            # Read and parse file
            content_data = self._parse_markdown_file(file_path)
            
            # Auto-detect category if not provided
            if not category:
                category = self._detect_category(file_path)
            
            # Prepare WordPress post data
            post_data = self._prepare_post_data(content_data, category)
            
            if dry_run:
                print(f"📝 DRY RUN: Would publish '{post_data['title']}'")
                return {'success': True, 'dry_run': True, 'title': post_data['title']}
            
            # Check for existing post with same title
            existing = self._check_existing_post(post_data['title'])
            if existing:
                print(f"⚠️ Post with similar title already exists: {existing['title']['rendered']}")
                return {'success': False, 'error': 'duplicate_title', 'existing_id': existing['id']}
            
            # Publish post
            result = self.wp_client.session.post(
                f"{self.wp_client.base_url}/posts",
                json=post_data,
                auth=self.wp_client.auth
            )
            
            if result.status_code == 201:
                post = result.json()
                print(f"✅ Published: {post['title']['rendered']} (ID: {post['id']})")
                
                # Auto-optimize if needed
                if hasattr(self, 'auto_optimize') and self.auto_optimize:
                    self._optimize_post(post['id'])
                
                return {
                    'success': True,
                    'post_id': post['id'],
                    'title': post['title']['rendered'],
                    'url': post['link']
                }
            else:
                error_msg = f"HTTP {result.status_code}: {result.text}"
                print(f"❌ Failed to publish: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            print(f"❌ Error publishing {file_path}: {e}")
            return {'success': False, 'error': str(e)}
    
    def publish_directory(self, directory, category=None, dry_run=False):
        """Publish all markdown files in a directory.
        
        Args:
            directory: Directory path
            category: Category name (optional)
            dry_run: If True, don't actually publish
            
        Returns:
            List of publication results
        """
        results = []
        md_files = list(Path(directory).glob('*.md'))
        
        print(f"📁 Found {len(md_files)} markdown files in {directory}")
        
        for file_path in sorted(md_files):
            print(f"\n📄 Processing: {file_path.name}")
            result = self.publish_file(str(file_path), category, dry_run)
            result['file'] = str(file_path)
            results.append(result)
        
        return results
    
    def _parse_markdown_file(self, file_path):
        """Parse markdown file with YAML front matter."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    front_matter = yaml.safe_load(parts[1])
                    markdown_content = parts[2].strip()
                except yaml.YAMLError:
                    front_matter = {}
                    markdown_content = content
            else:
                front_matter = {}
                markdown_content = content
        else:
            front_matter = {}
            markdown_content = content
        
        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Extract title from front matter or first heading
        title = front_matter.get('title')
        if not title:
            title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # Use filename as fallback
                title = Path(file_path).stem.replace('-', ' ').title()
        
        return {
            'title': title,
            'content': html_content,
            'markdown': markdown_content,
            'front_matter': front_matter,
            'excerpt': front_matter.get('excerpt', ''),
            'tags': front_matter.get('tags', []),
            'seo_title': front_matter.get('seo_title', ''),
            'seo_description': front_matter.get('seo_description', '')
        }
    
    def _detect_category(self, file_path):
        """Auto-detect category from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            part_lower = part.lower()
            if part_lower in self.category_map:
                return self.category_map[part_lower]
        
        return 'Uncategorized'
    
    def _prepare_post_data(self, content_data, category):
        """Prepare WordPress post data."""
        # Get category ID
        category_id = self._get_category_id(category)
        
        post_data = {
            'title': content_data['title'],
            'content': content_data['content'],
            'status': 'publish',
            'categories': [category_id] if category_id else [],
            'tags': content_data['tags']
        }
        
        # Add excerpt if available
        if content_data['excerpt']:
            post_data['excerpt'] = content_data['excerpt']
        
        # Add SEO fields if available (for RankMath/Yoast)
        if content_data['seo_title']:
            post_data['meta'] = post_data.get('meta', {})
            post_data['meta']['_yoast_wpseo_title'] = content_data['seo_title']
        
        return post_data
    
    def _get_category_id(self, category_name):
        """Get or create category ID."""
        try:
            categories = self.wp_client.get_categories()
            
            # Find existing category
            for cat in categories:
                if cat['name'].lower() == category_name.lower():
                    return cat['id']
            
            # Create new category if not found
            new_cat_data = {
                'name': category_name,
                'slug': category_name.lower().replace(' ', '-')
            }
            
            response = self.wp_client.session.post(
                f"{self.wp_client.base_url}/categories",
                json=new_cat_data,
                auth=self.wp_client.auth
            )
            
            if response.status_code == 201:
                new_category = response.json()
                print(f"✅ Created new category: {category_name}")
                return new_category['id']
            
        except Exception as e:
            print(f"⚠️ Error handling category {category_name}: {e}")
        
        return None
    
    def _check_existing_post(self, title):
        """Check if a post with similar title already exists."""
        try:
            posts = self.wp_client.get_posts(per_page=100)
            
            clean_title = title.lower().strip()
            
            for post in posts:
                existing_title = post['title']['rendered'].lower().strip()
                if clean_title == existing_title:
                    return post
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error checking existing posts: {e}")
            return None
    
    def _optimize_post(self, post_id):
        """Auto-optimize post after publishing."""
        print(f"🔧 Auto-optimizing post {post_id}...")
        
        try:
            # Add images if missing
            from image_validator import fix_post_images
            fix_post_images(self.wp_client, post_id, add_images=True)
            print(f"   ✅ Images optimized")
        except Exception as e:
            print(f"   ⚠️ Image optimization failed: {e}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description='WordPress Content Publisher')
    parser.add_argument('path', help='File or directory to publish')
    parser.add_argument('--category', type=str, help='Category name')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be published without actually publishing')
    parser.add_argument('--auto-optimize', action='store_true', help='Auto-optimize posts after publishing')
    parser.add_argument('--username', type=str, help='WordPress username')
    parser.add_argument('--password', type=str, help='WordPress application password')
    
    args = parser.parse_args()
    
    print_header("CONTENT PUBLISHER")
    
    # Initialize WordPress client
    wp_client = WordPressClient()
    if not wp_client.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    # Initialize publisher
    publisher = ContentPublisher(wp_client)
    publisher.auto_optimize = args.auto_optimize
    
    # Publish content
    if os.path.isfile(args.path):
        # Single file
        print_section(f"PUBLISHING FILE: {args.path}")
        result = publisher.publish_file(args.path, args.category, args.dry_run)
        
        if result['success']:
            print("✅ Publication successful!")
        else:
            print(f"❌ Publication failed: {result.get('error', 'Unknown error')}")
            return 1
            
    elif os.path.isdir(args.path):
        # Directory
        print_section(f"PUBLISHING DIRECTORY: {args.path}")
        results = publisher.publish_directory(args.path, args.category, args.dry_run)
        
        # Summary
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        
        print(f"\n📊 PUBLICATION SUMMARY:")
        print(f"   ✅ Successful: {successful}/{total}")
        print(f"   ❌ Failed: {total - successful}/{total}")
        
        # Show failures
        failures = [r for r in results if not r['success']]
        if failures:
            print(f"\n🚨 FAILURES:")
            for failure in failures:
                print(f"   ❌ {Path(failure['file']).name}: {failure.get('error', 'Unknown error')}")
    
    else:
        print(f"❌ Path not found: {args.path}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())