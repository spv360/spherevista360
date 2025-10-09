"""
Content Publisher
================
WordPress content publishing with markdown support and optimization.
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    from slugify import slugify
except ImportError:
    def slugify(text):
        """Simple slugify fallback."""
        import re
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'\s+', '-', text)
        return text.strip('-')

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_header, print_section, print_success, print_error, safe_get


class ContentPublisher:
    """Content publishing system with markdown support."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize publisher."""
        self.wp = wp_client or WordPressClient()
        
        # Default image templates by category
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
    
    def parse_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """Parse markdown file with YAML front matter."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            front_matter = {}
            markdown_content = content
            
            # Check for YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        front_matter = yaml.safe_load(parts[1]) or {}
                        markdown_content = parts[2].strip()
                    except yaml.YAMLError:
                        print_error(f"Invalid YAML front matter in {file_path}")
            
            # Convert markdown to HTML
            if HAS_MARKDOWN:
                html_content = markdown.markdown(
                    markdown_content,
                    extensions=['extra', 'codehilite', 'toc']
                )
            else:
                # Simple markdown conversion fallback
                html_content = self._simple_markdown_to_html(markdown_content)
            
            return {
                'front_matter': front_matter,
                'raw_content': markdown_content,
                'html_content': html_content,
                'file_path': file_path
            }
            
        except Exception as e:
            raise ValueError(f"Error parsing {file_path}: {e}")
    
    def prepare_post_data(self, parsed_content: Dict[str, Any], 
                         category: str = None, status: str = 'publish') -> Dict[str, Any]:
        """Prepare post data for WordPress."""
        front_matter = parsed_content['front_matter']
        
        # Extract title
        title = front_matter.get('title')
        if not title:
            # Try to extract from first heading in content
            content = parsed_content['raw_content']
            heading_match = re.search(r'^#+\s*(.+)', content, re.MULTILINE)
            title = heading_match.group(1).strip() if heading_match else "Untitled Post"
        
        # Generate slug
        slug = front_matter.get('slug', slugify(title))
        
        # Determine category
        if not category:
            category = front_matter.get('category', 'technology')
        
        # Prepare post data
        post_data = {
            'title': title,
            'content': parsed_content['html_content'],
            'status': front_matter.get('status', status),
            'slug': slug,
            'excerpt': front_matter.get('excerpt', ''),
            'meta': {
                'category': category,
                'featured_image': self._get_featured_image(category, front_matter),
                'seo_title': self._optimize_seo_title(title),
                'meta_description': self._generate_meta_description(parsed_content['html_content'])
            }
        }
        
        # Add categories if specified
        if category:
            post_data['categories'] = [category]
        
        # Add tags
        tags = front_matter.get('tags', [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]
        if tags:
            post_data['tags'] = tags
        
        return post_data
    
    def publish_from_file(self, file_path: str, category: str = None, 
                         status: str = 'publish', dry_run: bool = False) -> Dict[str, Any]:
        """Publish content from markdown file."""
        print_header(f"Publishing: {os.path.basename(file_path)}")
        
        try:
            # Parse file
            parsed_content = self.parse_markdown_file(file_path)
            print_success("File parsed successfully")
            
            # Prepare post data
            post_data = self.prepare_post_data(parsed_content, category, status)
            print_success(f"Post prepared: {post_data['title']}")
            
            if dry_run:
                print_section("DRY RUN - Post Data")
                print(f"Title: {post_data['title']}")
                print(f"Category: {post_data.get('categories', ['None'])[0] if post_data.get('categories') else 'None'}")
                print(f"Status: {post_data['status']}")
                print(f"Content length: {len(post_data['content'])} characters")
                return {
                    'success': True,
                    'dry_run': True,
                    'post_data': post_data
                }
            
            # Publish to WordPress
            result = self.wp.create_post(
                title=post_data['title'],
                content=post_data['content'],
                status=post_data['status'],
                categories=post_data.get('categories', [])
            )
            
            print_success(f"Post published successfully! ID: {result.get('id')}")
            
            return {
                'success': True,
                'post_id': result.get('id'),
                'post_url': result.get('link'),
                'post_data': post_data
            }
            
        except Exception as e:
            print_error(f"Failed to publish: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def publish_from_directory(self, directory: str, category: str = None,
                              status: str = 'publish', dry_run: bool = False) -> Dict[str, Any]:
        """Publish all markdown files from directory."""
        print_header(f"Batch Publishing: {directory}")
        
        directory_path = Path(directory)
        if not directory_path.exists():
            raise ValueError(f"Directory not found: {directory}")
        
        markdown_files = list(directory_path.glob("*.md"))
        if not markdown_files:
            print_error("No markdown files found")
            return {'success': False, 'error': 'No markdown files found'}
        
        results = {
            'total_files': len(markdown_files),
            'published': 0,
            'failed': 0,
            'results': []
        }
        
        for file_path in markdown_files:
            print_section(f"Processing {file_path.name}")
            
            try:
                result = self.publish_from_file(str(file_path), category, status, dry_run)
                
                if result['success']:
                    results['published'] += 1
                else:
                    results['failed'] += 1
                
                results['results'].append({
                    'file': file_path.name,
                    'result': result
                })
                
            except Exception as e:
                print_error(f"Error processing {file_path.name}: {e}")
                results['failed'] += 1
                results['results'].append({
                    'file': file_path.name,
                    'result': {'success': False, 'error': str(e)}
                })
        
        # Summary
        print_header("Batch Publishing Summary")
        print(f"Total files: {results['total_files']}")
        print(f"Published: {results['published']}")
        print(f"Failed: {results['failed']}")
        
        return results
    
    def update_post_from_file(self, post_id: int, file_path: str) -> Dict[str, Any]:
        """Update existing post from markdown file."""
        try:
            parsed_content = self.parse_markdown_file(file_path)
            post_data = self.prepare_post_data(parsed_content)
            
            update_data = {
                'title': post_data['title'],
                'content': post_data['content']
            }
            
            result = self.wp.update_post(post_id, update_data)
            print_success(f"Post {post_id} updated successfully")
            
            return {'success': True, 'post_id': post_id}
            
        except Exception as e:
            print_error(f"Failed to update post {post_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_featured_image(self, category: str, front_matter: Dict) -> str:
        """Get featured image URL."""
        # Check front matter first
        if 'featured_image' in front_matter:
            return front_matter['featured_image']
        
        # Use category template
        return self.image_templates.get(category.lower(), self.image_templates['default'])
    
    def _optimize_seo_title(self, title: str) -> str:
        """Optimize title for SEO (max 60 characters)."""
        if len(title) <= 60:
            return title
        
        # Truncate at word boundary
        truncated = title[:57].rsplit(' ', 1)[0]
        return truncated + "..."
    
    def _generate_meta_description(self, html_content: str) -> str:
        """Generate meta description from content."""
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        # Truncate to 155 characters at word boundary
        if len(text) <= 155:
            return text
        
        truncated = text[:152].rsplit(' ', 1)[0]
        return truncated + "..."
    
    def _simple_markdown_to_html(self, markdown_text: str) -> str:
        """Simple markdown to HTML conversion fallback."""
        html = markdown_text
        
        # Headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Paragraphs (simple approach)
        paragraphs = html.split('\n\n')
        html = ''.join(f'<p>{p.strip()}</p>\n' for p in paragraphs if p.strip())
        
        return html