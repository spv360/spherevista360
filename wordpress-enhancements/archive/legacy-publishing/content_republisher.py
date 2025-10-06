#!/usr/bin/env python3
"""
SphereVista360 Content Republisher
Republishes week1_final content to WordPress after cleanup
Includes enhanced SEO, categorization, and content optimization
"""

import os
import sys
import requests
import base64
import json
import re
import yaml
import markdown
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from slugify import slugify

class SphereVistaContentPublisher:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', '').rstrip('/')
        self.wp_user = os.environ.get('WP_USER', '')
        self.wp_pass = os.environ.get('WP_APP_PASS', '')
        
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            raise ValueError("WordPress credentials not set")
        
        # Set up authentication
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        self.base_url = f"{self.wp_site}/wp-json/wp/v2"
        
        # Enhanced category mapping for week1_final content
        self.category_mapping = {
            'Finance': {
                'wp_category': 'Finance',
                'description': 'Financial insights, investment strategies, and market analysis',
                'keywords': ['finance', 'investment', 'market', 'banking', 'fintech', 'economy'],
                'image_fallback': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1600&h=900'
            },
            'Technology': {
                'wp_category': 'Technology', 
                'description': 'Technology trends, AI developments, and digital transformation',
                'keywords': ['technology', 'AI', 'digital', 'innovation', 'software', 'tech'],
                'image_fallback': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=1600&h=900'
            },
            'Politics': {
                'wp_category': 'Politics',
                'description': 'Political analysis, policy insights, and governance',
                'keywords': ['politics', 'policy', 'government', 'election', 'governance'],
                'image_fallback': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1600&h=900'
            },
            'Travel': {
                'wp_category': 'Travel',
                'description': 'Travel guides, destination insights, and visa information',
                'keywords': ['travel', 'destination', 'visa', 'tourism', 'journey'],
                'image_fallback': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1600&h=900'
            },
            'World': {
                'wp_category': 'World',
                'description': 'Global affairs, international relations, and world events',
                'keywords': ['world', 'global', 'international', 'affairs', 'news'],
                'image_fallback': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600&h=900'
            },
            'Business': {
                'wp_category': 'Business',
                'description': 'Business insights, entrepreneurship, and industry trends',
                'keywords': ['business', 'entrepreneur', 'startup', 'industry', 'corporate'],
                'image_fallback': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1600&h=900'
            }
        }
        
        # Publication schedule for optimal SEO
        self.publication_schedule = {
            'Finance': 0,     # Publish immediately (priority content)
            'Technology': 1,  # 1 day delay
            'Politics': 2,    # 2 day delay  
            'Business': 3,    # 3 day delay
            'Travel': 4,      # 4 day delay
            'World': 5        # 5 day delay
        }
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected as {user_data.get('name')} with roles: {user_data.get('roles')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def ensure_category(self, category_name: str, description: str = '') -> int:
        """Ensure category exists, create if not"""
        try:
            # Check if category exists
            response = requests.get(
                f"{self.base_url}/categories",
                headers=self.headers,
                params={'search': category_name, 'per_page': 100}
            )
            
            if response.status_code == 200:
                categories = response.json()
                for cat in categories:
                    if cat['name'].lower() == category_name.lower():
                        print(f"✅ Category exists: {category_name} (ID: {cat['id']})")
                        return cat['id']
            
            # Create new category
            payload = {
                'name': category_name,
                'description': description
            }
            
            response = requests.post(
                f"{self.base_url}/categories",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                cat_data = response.json()
                print(f"✅ Created category: {category_name} (ID: {cat_data['id']})")
                return cat_data['id']
            else:
                print(f"❌ Failed to create category {category_name}: {response.status_code}")
                return 1  # Default to Uncategorized
                
        except Exception as e:
            print(f"❌ Category error: {e}")
            return 1
    
    def parse_markdown_file(self, file_path: Path) -> Tuple[Dict, str]:
        """Parse markdown file with YAML front matter"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1]) or {}
                    markdown_content = parts[2].strip()
                    return front_matter, markdown_content
            
            # No front matter, return empty dict and full content
            return {}, content
            
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return {}, ""
    
    def enhance_content_seo(self, content: str, category: str, title: str) -> str:
        """Enhance content with SEO-friendly elements"""
        # Convert markdown to HTML
        html_content = markdown.markdown(
            content, 
            extensions=['extra', 'codehilite', 'toc']
        )
        
        # Add category-specific enhancements
        category_info = self.category_mapping.get(category, {})
        keywords = category_info.get('keywords', [])
        
        # Add internal linking opportunities
        internal_links = self.generate_internal_links(html_content, category)
        if internal_links:
            html_content += f"\n\n<h3>Related Articles</h3>\n{internal_links}"
        
        # Add structured data hints
        html_content = self.add_structured_data(html_content, category, title)
        
        return html_content
    
    def generate_internal_links(self, content: str, category: str) -> str:
        """Generate internal links for SEO"""
        # This is a simplified version - in practice, you'd query existing posts
        related_links = {
            'Finance': [
                '🔗 [Digital Banking Trends](https://spherevista360.com/digital-banking-trends/)',
                '🔗 [Investment Strategies 2025](https://spherevista360.com/investment-strategies-2025/)',
                '🔗 [FinTech Revolution](https://spherevista360.com/fintech-revolution/)'
            ],
            'Technology': [
                '🔗 [AI in Business](https://spherevista360.com/ai-business/)',
                '🔗 [Cloud Computing Guide](https://spherevista360.com/cloud-computing/)',
                '🔗 [Tech Startup Trends](https://spherevista360.com/tech-startups/)'
            ],
            'Politics': [
                '🔗 [Election Analysis](https://spherevista360.com/election-analysis/)',
                '🔗 [Policy Updates](https://spherevista360.com/policy-updates/)',
                '🔗 [Government Technology](https://spherevista360.com/gov-tech/)'
            ]
        }
        
        links = related_links.get(category, [])
        if links:
            return '<ul>' + ''.join(f'<li>{link}</li>' for link in links[:3]) + '</ul>'
        return ''
    
    def add_structured_data(self, content: str, category: str, title: str) -> str:
        """Add structured data hints for better SEO"""
        # Add article schema hints
        schema_hints = f"""
<!-- Article Schema Hints -->
<meta itemscope itemtype="http://schema.org/Article">
<meta itemprop="headline" content="{title}">
<meta itemprop="articleSection" content="{category}">
<meta itemprop="datePublished" content="{datetime.now().isoformat()}">
"""
        return content + schema_hints
    
    def optimize_image_url(self, image_url: str, category: str) -> str:
        """Optimize image URL with fallbacks"""
        if not image_url or not image_url.startswith('http'):
            # Use category fallback image
            return self.category_mapping.get(category, {}).get('image_fallback', 
                'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1600&h=900'
            )
        
        # Optimize Unsplash URLs for better performance
        if 'unsplash.com' in image_url:
            # Ensure proper sizing parameters
            if '?' in image_url:
                image_url += '&auto=format&fit=crop&w=1600&h=900&q=80'
            else:
                image_url += '?auto=format&fit=crop&w=1600&h=900&q=80'
        
        return image_url
    
    def create_wordpress_post(self, title: str, content: str, category_id: int, 
                            front_matter: Dict, publish: bool = False) -> Optional[Dict]:
        """Create WordPress post with enhanced SEO"""
        
        # Generate SEO-optimized slug
        slug = front_matter.get('slug') or slugify(title)[:50]
        
        # Create excerpt
        excerpt = front_matter.get('excerpt', '')
        if not excerpt:
            # Generate excerpt from content
            clean_content = re.sub(r'<[^>]+>', '', content)
            excerpt = ' '.join(clean_content.split()[:25]) + '...'
        
        # Prepare post data
        post_data = {
            'title': title,
            'content': content,
            'excerpt': excerpt,
            'slug': slug,
            'status': 'publish' if publish else 'draft',
            'categories': [category_id],
            'meta': {}
        }
        
        # Add tags if available
        if front_matter.get('tags'):
            # In a real implementation, you'd ensure tags exist first
            post_data['tags'] = front_matter['tags']
        
        # Add SEO meta fields
        if front_matter.get('seo_title'):
            post_data['meta']['_yoast_wpseo_title'] = front_matter['seo_title']
        
        if front_matter.get('seo_description'):
            post_data['meta']['_yoast_wpseo_metadesc'] = front_matter['seo_description']
        
        # Add featured image
        if front_matter.get('image'):
            post_data['meta']['_thumbnail_url'] = front_matter['image']
        
        try:
            response = requests.post(
                f"{self.base_url}/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post = response.json()
                print(f"✅ Created post: {title}")
                print(f"   📝 Status: {post['status']}")
                print(f"   🔗 Edit: {self.wp_site}/wp-admin/post.php?post={post['id']}&action=edit")
                print(f"   👁️  View: {post.get('link', 'N/A')}")
                return post
            else:
                print(f"❌ Failed to create post '{title}': {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating post '{title}': {e}")
            return None
    
    def scan_week1_content(self, base_path: str = './spherevista360_week1_final') -> Dict[str, List[Path]]:
        """Scan week1_final directory for content files"""
        content_map = {}
        base_dir = Path(base_path)
        
        if not base_dir.exists():
            print(f"❌ Week1 content directory not found: {base_path}")
            print("💡 Please specify the correct path to spherevista360_week1_final/")
            return {}
        
        # Scan for markdown files in each category folder
        for category_dir in base_dir.iterdir():
            if category_dir.is_dir() and category_dir.name in self.category_mapping:
                md_files = list(category_dir.glob('*.md'))
                if md_files:
                    content_map[category_dir.name] = md_files
                    print(f"📁 Found {len(md_files)} files in {category_dir.name}/")
        
        return content_map
    
    def republish_content(self, content_path: str = './spherevista360_week1_final', 
                         publish: bool = False, specific_category: str = None):
        """Republish week1_final content to WordPress"""
        
        print("🚀 SphereVista360 Content Republisher")
        print("=" * 40)
        print(f"📁 Source: {content_path}")
        print(f"🌐 Target: {self.wp_site}")
        print(f"📝 Mode: {'PUBLISH' if publish else 'DRAFT'}")
        print()
        
        # Test connection
        if not self.test_connection():
            return False
        
        # Scan for content
        content_map = self.scan_week1_content(content_path)
        if not content_map:
            return False
        
        # Filter by specific category if requested
        if specific_category:
            if specific_category in content_map:
                content_map = {specific_category: content_map[specific_category]}
                print(f"🎯 Publishing only {specific_category} category")
            else:
                print(f"❌ Category '{specific_category}' not found")
                return False
        
        # Ensure all categories exist
        category_ids = {}
        for category_name in content_map.keys():
            category_info = self.category_mapping[category_name]
            category_ids[category_name] = self.ensure_category(
                category_info['wp_category'],
                category_info['description']
            )
        
        print()
        
        # Process each category
        total_published = 0
        total_files = sum(len(files) for files in content_map.values())
        
        for category_name, files in content_map.items():
            print(f"📂 Processing {category_name} ({len(files)} files)")
            print("-" * 30)
            
            category_id = category_ids[category_name]
            
            for file_path in sorted(files):
                print(f"📄 Processing: {file_path.name}")
                
                # Parse markdown file
                front_matter, content = self.parse_markdown_file(file_path)
                
                # Extract title
                title = front_matter.get('title') or file_path.stem.replace('-', ' ').title()
                
                # Determine category
                category = front_matter.get('category') or category_name
                
                # Optimize image URL
                if front_matter.get('image'):
                    front_matter['image'] = self.optimize_image_url(
                        front_matter['image'], 
                        category
                    )
                
                # Enhance content with SEO
                enhanced_content = self.enhance_content_seo(content, category, title)
                
                # Determine publish status
                should_publish = publish or front_matter.get('publish', False)
                
                # Create post
                post = self.create_wordpress_post(
                    title=title,
                    content=enhanced_content,
                    category_id=category_id,
                    front_matter=front_matter,
                    publish=should_publish
                )
                
                if post:
                    total_published += 1
                
                print()
        
        # Summary
        print("🎉 Republishing Complete!")
        print("=" * 25)
        print(f"📊 Files processed: {total_files}")
        print(f"✅ Posts created: {total_published}")
        print(f"📈 Success rate: {(total_published/total_files)*100:.1f}%")
        
        if total_published > 0:
            print(f"\n🔗 WordPress Admin: {self.wp_site}/wp-admin/edit.php")
            print(f"🎯 Categories: {self.wp_site}/wp-admin/edit-tags.php?taxonomy=category")
            
            if not publish:
                print(f"\n💡 Posts created as DRAFTS. To publish:")
                print(f"   1. Review content in WordPress admin")
                print(f"   2. Use --publish flag to publish directly")
                print(f"   3. Or publish manually from WordPress")
        
        return total_published > 0

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Republish SphereVista360 week1_final content')
    parser.add_argument('--content-path', default='./spherevista360_week1_final',
                      help='Path to week1_final content directory')
    parser.add_argument('--publish', action='store_true',
                      help='Publish posts immediately (default: create as drafts)')
    parser.add_argument('--category', 
                      help='Only republish specific category (Finance, Technology, etc.)')
    
    args = parser.parse_args()
    
    # Check environment variables
    required_vars = ['WP_SITE', 'WP_USER', 'WP_APP_PASS']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your_value'")
        print("\n💡 Set these first, then run the script again")
        return False
    
    try:
        publisher = SphereVistaContentPublisher()
        return publisher.republish_content(
            content_path=args.content_path,
            publish=args.publish,
            specific_category=args.category
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()