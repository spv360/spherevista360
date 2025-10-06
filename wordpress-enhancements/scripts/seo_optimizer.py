#!/usr/bin/env python3
"""
SEO Optimization Script for SphereVista360.com
Enhances existing content for better search engine performance
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import requests
import json

# Add scripts directory to path
sys.path.append('./scripts')

class SEOOptimizer:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_APP_PASS')
        
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            raise ValueError("WordPress credentials not set")
    
    def get_auth_headers(self):
        """Get authentication headers for WordPress API"""
        import base64
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
    
    def get_all_posts(self) -> List[Dict]:
        """Fetch all published posts from WordPress"""
        print("🔍 Fetching all published posts...")
        
        posts = []
        page = 1
        per_page = 10
        
        while True:
            url = f"{self.wp_site}/wp-json/wp/v2/posts"
            params = {
                'page': page,
                'per_page': per_page,
                'status': 'publish'
            }
            
            response = requests.get(url, params=params, headers=self.get_auth_headers())
            
            if response.status_code != 200:
                break
                
            page_posts = response.json()
            if not page_posts:
                break
                
            posts.extend(page_posts)
            page += 1
            
            # Limit to prevent infinite loop
            if page > 10:
                break
        
        print(f"📊 Found {len(posts)} published posts")
        return posts
    
    def generate_meta_description(self, title: str, content: str, max_length: int = 155) -> str:
        """Generate optimized meta description from content"""
        # Clean HTML tags from content
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        # Extract first meaningful sentence
        sentences = re.split(r'[.!?]+', clean_content)
        
        description = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Skip very short sentences
                if len(description + sentence) < max_length - 10:
                    description += sentence + ". "
                else:
                    break
        
        # If no good sentences found, use title-based description
        if len(description) < 50:
            # Extract key topics from title
            title_words = title.lower().split()
            key_topics = [word for word in title_words if len(word) > 4]
            
            if any(word in title.lower() for word in ['2025', 'finance', 'tech', 'ai']):
                description = f"Discover insights on {', '.join(key_topics[:3])} and their impact in 2025. Expert analysis and trends you need to know."
            else:
                description = f"Expert insights on {', '.join(key_topics[:3])}. In-depth analysis and practical information for informed decision-making."
        
        # Ensure it ends properly and fits length limit
        description = description.strip()
        if not description.endswith('.'):
            description += '.'
            
        if len(description) > max_length:
            description = description[:max_length-3] + '...'
            
        return description
    
    def extract_focus_keywords(self, title: str, content: str) -> List[str]:
        """Extract focus keywords from title and content"""
        # Common important keywords based on your content categories
        category_keywords = {
            'finance': ['finance', 'investment', 'market', 'economy', 'trading', 'fintech'],
            'tech': ['technology', 'ai', 'cybersecurity', 'cloud', 'digital', 'automation'],
            'politics': ['politics', 'election', 'policy', 'government', 'democratic'],
            'travel': ['travel', 'visa', 'destination', 'tourism', 'nomad'],
            'world': ['global', 'international', 'world', 'emerging', 'cooperation']
        }
        
        title_lower = title.lower()
        content_lower = content.lower()
        
        keywords = []
        
        # Extract from title (highest priority)
        title_words = re.findall(r'\b\w{4,}\b', title_lower)
        keywords.extend(title_words[:3])
        
        # Add category-specific keywords if relevant
        for category, cat_keywords in category_keywords.items():
            if any(kw in title_lower or kw in content_lower for kw in cat_keywords):
                relevant_keywords = [kw for kw in cat_keywords if kw in content_lower]
                keywords.extend(relevant_keywords[:2])
        
        # Remove duplicates and return top 5
        return list(dict.fromkeys(keywords))[:5]
    
    def optimize_content_structure(self, content: str) -> str:
        """Optimize content structure for SEO"""
        # Ensure proper heading hierarchy
        content = re.sub(r'<h([1-6])>', lambda m: f'<h{min(int(m.group(1)), 3)}>', content)
        
        # Add proper paragraph spacing
        content = re.sub(r'</p>\s*<p>', '</p>\n\n<p>', content)
        
        # Ensure lists are properly formatted
        content = re.sub(r'</li>\s*<li>', '</li>\n<li>', content)
        
        return content
    
    def update_post_seo(self, post: Dict) -> Dict:
        """Update a single post with SEO optimizations"""
        post_id = post['id']
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        print(f"🔧 Optimizing: {title}")
        
        # Generate optimized meta description
        meta_description = self.generate_meta_description(title, content)
        
        # Extract focus keywords
        focus_keywords = self.extract_focus_keywords(title, content)
        
        # Optimize content structure
        optimized_content = self.optimize_content_structure(content)
        
        # Create update payload
        update_data = {
            'content': optimized_content,
            'meta': {
                '_yoast_wpseo_metadesc': meta_description,
                '_yoast_wpseo_focuskw': focus_keywords[0] if focus_keywords else title.split()[0],
                '_yoast_wpseo_meta-robots-noindex': '0',
                '_yoast_wpseo_meta-robots-nofollow': '0'
            }
        }
        
        # Update post via WordPress API
        url = f"{self.wp_site}/wp-json/wp/v2/posts/{post_id}"
        response = requests.post(url, json=update_data, headers=self.get_auth_headers())
        
        result = {
            'id': post_id,
            'title': title,
            'meta_description': meta_description,
            'focus_keywords': focus_keywords,
            'status': 'success' if response.status_code == 200 else 'failed',
            'response_code': response.status_code
        }
        
        if result['status'] == 'success':
            print(f"  ✅ Updated successfully")
            print(f"  📝 Meta: {meta_description[:50]}...")
            print(f"  🎯 Keywords: {', '.join(focus_keywords[:3])}")
        else:
            print(f"  ❌ Failed to update (Status: {response.status_code})")
        
        return result
    
    def generate_sitemap_suggestions(self, posts: List[Dict]) -> List[str]:
        """Generate sitemap optimization suggestions"""
        suggestions = []
        
        # Group posts by category
        categories = {}
        for post in posts:
            post_categories = post.get('categories', [])
            for cat_id in post_categories:
                if cat_id not in categories:
                    categories[cat_id] = []
                categories[cat_id].append(post)
        
        suggestions.append("📍 Sitemap Optimization Suggestions:")
        suggestions.append("=" * 40)
        suggestions.append("1. Create category-specific sitemaps")
        suggestions.append("2. Submit XML sitemap to Google Search Console")
        suggestions.append("3. Add breadcrumb navigation")
        suggestions.append("4. Create topic clusters for related articles")
        
        return suggestions
    
    def analyze_internal_linking(self, posts: List[Dict]) -> List[str]:
        """Analyze and suggest internal linking improvements"""
        suggestions = []
        
        # Extract all internal links
        internal_links = {}
        for post in posts:
            post_id = post['id']
            content = post['content']['rendered']
            
            # Find internal links in content
            site_domain = self.wp_site.replace('https://', '').replace('http://', '')
            internal_link_pattern = rf'href=["\']https?://{re.escape(site_domain)}[^"\']*["\']'
            links = re.findall(internal_link_pattern, content)
            internal_links[post_id] = len(links)
        
        # Generate suggestions
        low_linking_posts = [pid for pid, count in internal_links.items() if count < 2]
        
        suggestions.append("🔗 Internal Linking Analysis:")
        suggestions.append("=" * 30)
        suggestions.append(f"📊 Average internal links per post: {sum(internal_links.values()) / len(internal_links):.1f}")
        suggestions.append(f"⚠️  Posts with <2 internal links: {len(low_linking_posts)}")
        suggestions.append("")
        suggestions.append("💡 Recommendations:")
        suggestions.append("- Add 2-4 relevant internal links per post")
        suggestions.append("- Link to related articles in same category")
        suggestions.append("- Create 'Related Posts' sections")
        suggestions.append("- Link to pillar content from supporting posts")
        
        return suggestions
    
    def run_full_optimization(self):
        """Run complete SEO optimization process"""
        print("🚀 Starting SEO Optimization for SphereVista360")
        print("=" * 50)
        
        try:
            # Get all posts
            posts = self.get_all_posts()
            
            if not posts:
                print("❌ No posts found to optimize")
                return
            
            # Optimize each post
            results = []
            for i, post in enumerate(posts, 1):
                print(f"\n📄 Processing post {i}/{len(posts)}")
                result = self.update_post_seo(post)
                results.append(result)
            
            # Generate summary
            successful = [r for r in results if r['status'] == 'success']
            failed = [r for r in results if r['status'] == 'failed']
            
            print(f"\n📊 OPTIMIZATION SUMMARY")
            print("=" * 30)
            print(f"✅ Successfully optimized: {len(successful)}")
            print(f"❌ Failed to optimize: {len(failed)}")
            print(f"📈 Success rate: {len(successful)/len(results)*100:.1f}%")
            
            if failed:
                print(f"\n⚠️  Failed posts:")
                for fail in failed:
                    print(f"  - {fail['title']} (Status: {fail['response_code']})")
            
            # Additional recommendations
            print(f"\n💡 ADDITIONAL RECOMMENDATIONS")
            print("=" * 30)
            
            sitemap_suggestions = self.generate_sitemap_suggestions(posts)
            for suggestion in sitemap_suggestions:
                print(suggestion)
            
            print("")
            linking_suggestions = self.analyze_internal_linking(posts)
            for suggestion in linking_suggestions:
                print(suggestion)
            
            print(f"\n🎉 SEO optimization completed!")
            print(f"🔍 Next steps:")
            print(f"  1. Install Yoast SEO plugin for ongoing optimization")
            print(f"  2. Submit sitemap to Google Search Console")
            print(f"  3. Monitor search rankings and traffic")
            print(f"  4. Add more internal links between related posts")
            
        except Exception as e:
            print(f"❌ Error during optimization: {str(e)}")
            return False
        
        return True

def main():
    """Main function to run SEO optimization"""
    try:
        optimizer = SEOOptimizer()
        optimizer.run_full_optimization()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please ensure WordPress credentials are set:")
        print('export WP_SITE="https://spherevista360.com"')
        print('export WP_USER="your_username"')
        print('export WP_APP_PASS="your_app_password"')
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()