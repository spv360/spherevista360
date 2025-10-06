#!/usr/bin/env python3
"""
Quick SEO Enhancement Script for SphereVista360.com
Optimizes meta descriptions and basic SEO elements
"""

import sys
import os
import re
import requests
import base64
from typing import Dict, List

class QuickSEOEnhancer:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_APP_PASS')
        
        # WordPress API endpoints
        self.posts_endpoint = f"{self.wp_site}/wp-json/wp/v2/posts"
        
        # Authentication
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
    
    def get_posts(self, per_page=10) -> List[Dict]:
        """Fetch published posts"""
        try:
            response = requests.get(
                self.posts_endpoint, 
                params={'per_page': per_page, 'status': 'publish'},
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []
    
    def clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        return re.sub(r'<[^>]+>', '', text)
    
    def generate_meta_description(self, title: str, content: str) -> str:
        """Generate SEO-optimized meta description"""
        # Clean content
        clean_content = self.clean_html(content)
        
        # Extract first meaningful paragraph
        paragraphs = [p.strip() for p in clean_content.split('\n') if len(p.strip()) > 30]
        
        if paragraphs:
            first_para = paragraphs[0]
            # Truncate to 155 characters (Google's recommended length)
            if len(first_para) > 155:
                meta_desc = first_para[:152] + "..."
            else:
                meta_desc = first_para
        else:
            # Fallback: create description from title
            topic_words = [word for word in title.split() if len(word) > 3]
            meta_desc = f"Discover insights about {' '.join(topic_words[:3])}. Expert analysis and practical information for informed decision-making."
        
        return meta_desc
    
    def enhance_post_excerpt(self, post: Dict) -> str:
        """Create or enhance post excerpt"""
        content = post['content']['rendered']
        current_excerpt = post.get('excerpt', {}).get('rendered', '')
        
        if current_excerpt and len(current_excerpt.strip()) > 50:
            return current_excerpt
        
        # Generate new excerpt from content
        clean_content = self.clean_html(content)
        sentences = re.split(r'[.!?]+', clean_content)
        
        excerpt = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                if len(excerpt + sentence) < 150:
                    excerpt += sentence + ". "
                else:
                    break
        
        return excerpt.strip()
    
    def optimize_post(self, post: Dict) -> Dict:
        """Optimize a single post"""
        post_id = post['id']
        title = post['title']['rendered']
        
        print(f"🔧 Optimizing: {title[:50]}...")
        
        # Generate optimizations
        meta_description = self.generate_meta_description(title, post['content']['rendered'])
        enhanced_excerpt = self.enhance_post_excerpt(post)
        
        # Prepare update data
        update_data = {
            'excerpt': enhanced_excerpt
        }
        
        # Update the post
        try:
            response = requests.post(
                f"{self.posts_endpoint}/{post_id}",
                json=update_data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                print(f"  ✅ Success")
                print(f"  📝 Excerpt: {enhanced_excerpt[:60]}...")
                print(f"  🎯 Meta: {meta_description[:60]}...")
                return {
                    'id': post_id,
                    'title': title,
                    'status': 'success',
                    'meta_description': meta_description,
                    'excerpt': enhanced_excerpt
                }
            else:
                print(f"  ❌ Failed (Status: {response.status_code})")
                return {'id': post_id, 'title': title, 'status': 'failed'}
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return {'id': post_id, 'title': title, 'status': 'error', 'error': str(e)}
    
    def analyze_current_seo(self, posts: List[Dict]) -> Dict:
        """Analyze current SEO status"""
        analysis = {
            'total_posts': len(posts),
            'posts_with_excerpts': 0,
            'posts_without_excerpts': 0,
            'average_title_length': 0,
            'titles_too_long': 0,
            'titles_too_short': 0
        }
        
        title_lengths = []
        
        for post in posts:
            title = post['title']['rendered']
            excerpt = post.get('excerpt', {}).get('rendered', '')
            
            title_length = len(title)
            title_lengths.append(title_length)
            
            if excerpt and len(excerpt.strip()) > 20:
                analysis['posts_with_excerpts'] += 1
            else:
                analysis['posts_without_excerpts'] += 1
            
            if title_length > 60:
                analysis['titles_too_long'] += 1
            elif title_length < 30:
                analysis['titles_too_short'] += 1
        
        analysis['average_title_length'] = sum(title_lengths) / len(title_lengths) if title_lengths else 0
        
        return analysis
    
    def run_optimization(self):
        """Run the optimization process"""
        print("🚀 Quick SEO Enhancement for SphereVista360")
        print("=" * 45)
        
        # Fetch posts
        posts = self.get_posts(per_page=15)  # Optimize latest 15 posts
        
        if not posts:
            print("❌ No posts found to optimize")
            return False
        
        print(f"📊 Found {len(posts)} posts to optimize\n")
        
        # Analyze current SEO status
        analysis = self.analyze_current_seo(posts)
        
        print("📈 CURRENT SEO STATUS:")
        print("-" * 25)
        print(f"📝 Total posts: {analysis['total_posts']}")
        print(f"✅ Posts with excerpts: {analysis['posts_with_excerpts']}")
        print(f"❌ Posts without excerpts: {analysis['posts_without_excerpts']}")
        print(f"📏 Average title length: {analysis['average_title_length']:.1f} chars")
        print(f"⚠️  Titles too long (>60): {analysis['titles_too_long']}")
        print(f"⚠️  Titles too short (<30): {analysis['titles_too_short']}")
        print()
        
        # Optimize posts
        results = []
        for i, post in enumerate(posts, 1):
            print(f"📄 Post {i}/{len(posts)}:")
            result = self.optimize_post(post)
            results.append(result)
            print()
        
        # Summary
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] != 'success']
        
        print("🎯 OPTIMIZATION SUMMARY:")
        print("=" * 25)
        print(f"✅ Successfully optimized: {len(successful)}")
        print(f"❌ Failed to optimize: {len(failed)}")
        print(f"📈 Success rate: {len(successful)/len(results)*100:.1f}%")
        
        if successful:
            print(f"\n💡 NEXT STEPS:")
            print("- Install Yoast SEO plugin for advanced optimization")
            print("- Add focus keywords to each post")
            print("- Create internal links between related posts")
            print("- Submit sitemap to Google Search Console")
            print("- Monitor search rankings")
        
        return True

def main():
    """Main execution function"""
    # Check environment variables
    required_vars = ['WP_SITE', 'WP_USER', 'WP_APP_PASS']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your_value'")
        return False
    
    try:
        enhancer = QuickSEOEnhancer()
        return enhancer.run_optimization()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()