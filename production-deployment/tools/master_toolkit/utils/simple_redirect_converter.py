#!/usr/bin/env python3
"""
Simple Redirect to Content Converter
====================================
Convert redirect posts to full content articles.
"""

import json
import requests
from datetime import datetime


def print_info(msg):
    print(f"ℹ️  {msg}")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")


class RedirectConverter:
    """Convert redirect posts to full content articles."""
    
    def __init__(self):
        """Initialize the converter."""
        self.redirect_posts = []
        
    def find_redirect_posts(self):
        """Find all redirect posts."""
        print_info("🔍 Finding redirect posts...")
        
        try:
            # Get all posts using direct API calls
            all_posts = []
            page = 1
            
            while True:
                url = f"https://spherevista360.com/wp-json/wp/v2/posts?per_page=50&page={page}"
                print_info(f"   Fetching page {page}...")
                
                response = requests.get(url, timeout=10)
                
                if response.status_code != 200:
                    print_error(f"   API returned status {response.status_code}")
                    break
                    
                posts = response.json()
                if not posts:
                    break
                    
                all_posts.extend(posts)
                page += 1
                
                if page > 10:  # Safety limit
                    break
            
            print_success(f"📊 Retrieved {len(all_posts)} total posts")
            
            # Find redirect posts by title or content
            redirect_posts = []
            
            for post in all_posts:
                title = post.get('title', {}).get('rendered', '')
                content = post.get('content', {}).get('rendered', '')
                post_id = post.get('id')
                
                # Check for redirect indicators or specific posts we know are redirects
                is_redirect = (
                    title.lower().startswith('redirect:') or
                    'redirect' in title.lower() or
                    len(content.strip()) < 300 or  # Very short content
                    'coming soon' in content.lower() or
                    'placeholder' in content.lower() or
                    post_id in [1918, 1919, 1920, 1921]  # The specific posts we identified
                )
                
                if is_redirect:
                    redirect_posts.append(post)
            
            self.redirect_posts = redirect_posts
            print_success(f"✅ Found {len(redirect_posts)} redirect posts")
            
            print_info("\n📄 REDIRECT POSTS FOUND:")
            for post in redirect_posts:
                title = post.get('title', {}).get('rendered', '')
                post_id = post.get('id')
                content_length = len(post.get('content', {}).get('rendered', ''))
                print_info(f"   • {title} (ID: {post_id}, Content: {content_length} chars)")
            
            return redirect_posts
            
        except Exception as e:
            print_error(f"❌ Failed to find redirect posts: {str(e)}")
            return []
    
    def generate_conversion_plan(self):
        """Generate conversion plan for redirect posts."""
        print_info("\n📋 Generating conversion plan...")
        
        conversion_plan = {
            'conversion_date': datetime.now().isoformat(),
            'redirect_posts_found': len(self.redirect_posts),
            'conversions': []
        }
        
        # Content templates for specific posts
        content_templates = {
            'Tech Innovation 2025': {
                'category': 'Technology',
                'excerpt': 'Discover the groundbreaking technological innovations shaping 2025 and their impact on industries worldwide.',
                'tags': ['innovation', 'technology', '2025', 'trends', 'AI', 'blockchain'],
                'word_count': 1500
            },
            'On Device Vs Cloud Ai 2025': {
                'category': 'Technology',
                'excerpt': 'Compare on-device AI versus cloud AI solutions, analyzing performance, privacy, and cost considerations for 2025.',
                'tags': ['AI', 'cloud computing', 'edge computing', 'machine learning', '2025'],
                'word_count': 1800
            },
            'Data Privacy Future': {
                'category': 'Technology',
                'excerpt': 'Explore the future of data privacy, emerging regulations, and how businesses can adapt to protect user information.',
                'tags': ['data privacy', 'GDPR', 'technology', 'security', 'regulations'],
                'word_count': 1600
            },
            'Product Analytics 2025': {
                'category': 'Business',
                'excerpt': 'Master product analytics in 2025 with advanced tools, methodologies, and data-driven insights for business growth.',
                'tags': ['analytics', 'product management', 'data science', 'business intelligence', '2025'],
                'word_count': 1700
            }
        }
        
        for post in self.redirect_posts:
            post_id = post.get('id')
            title = post.get('title', {}).get('rendered', '')
            current_content = post.get('content', {}).get('rendered', '')
            
            # Find matching template
            template = None
            new_title = title.replace('Redirect:', '').strip()
            
            for topic, tmpl in content_templates.items():
                if any(word.lower() in new_title.lower() for word in topic.split()):
                    template = tmpl
                    break
            
            if not template:
                template = {
                    'category': 'Business',
                    'excerpt': f'Comprehensive analysis and insights on {new_title.lower()}.',
                    'tags': ['analysis', 'insights', '2025'],
                    'word_count': 1200
                }
            
            conversion = {
                'post_id': post_id,
                'original_title': title,
                'new_title': new_title,
                'current_content_length': len(current_content),
                'suggested_category': template['category'],
                'new_excerpt': template['excerpt'],
                'suggested_tags': template['tags'],
                'target_word_count': template['word_count'],
                'url': post.get('link', ''),
                'status': 'needs_conversion'
            }
            
            conversion_plan['conversions'].append(conversion)
        
        # Save conversion plan
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_file = f'redirect_conversion_plan_{timestamp}.json'
        
        with open(plan_file, 'w') as f:
            json.dump(conversion_plan, f, indent=2)
        
        print_success(f"✅ Conversion plan saved: {plan_file}")
        
        # Display summary
        print_info("\n📊 CONVERSION PLAN SUMMARY:")
        for conversion in conversion_plan['conversions']:
            print_info(f"   📄 {conversion['new_title']}")
            print_info(f"      → Category: {conversion['suggested_category']}")
            print_info(f"      → Current: {conversion['current_content_length']} chars")
            print_info(f"      → Target: {conversion['target_word_count']} words")
            print_info(f"      → Tags: {', '.join(conversion['suggested_tags'])}")
            print_info("")
        
        return plan_file
    
    def generate_content_samples(self):
        """Generate sample content for each redirect post."""
        print_info("\n✍️ Generating content samples...")
        
        samples = {}
        
        # Sample content outlines
        content_outlines = {
            'Tech Innovation 2025': [
                "Introduction to 2025 tech landscape",
                "Breakthrough Technologies (AI Evolution, Quantum Computing, Biotechnology)",
                "Industry Transformation (Healthcare, Sustainability)",
                "Emerging Paradigms (Ambient Computing, Decentralization)",
                "Innovation Hotspots and Investment Trends",
                "Challenges and Ethical Considerations",
                "Future Outlook and Predictions",
                "Conclusion and Strategic Recommendations"
            ],
            'On Device Vs Cloud Ai 2025': [
                "Understanding AI Computing Paradigms",
                "Comparative Analysis (Performance, Privacy, Cost)",
                "Use Case Optimization",
                "Hybrid Architectures and Best Practices",
                "Technology Enablers and Market Trends",
                "Decision Framework for Organizations",
                "Future Evolution and Recommendations"
            ],
            'Data Privacy Future': [
                "Current Privacy Landscape",
                "Emerging Regulations and Compliance",
                "Technology-Driven Privacy Solutions",
                "Consumer Expectations and Business Impact",
                "Global Privacy Frameworks",
                "Implementation Strategies",
                "Future Trends and Conclusion"
            ],
            'Product Analytics 2025': [
                "Evolution of Product Analytics",
                "Core Analytics Frameworks",
                "AI-Powered Capabilities",
                "Industry-Specific Applications",
                "Privacy-First Analytics",
                "Organizational Excellence",
                "Tools and Future Trends",
                "Implementation Best Practices"
            ]
        }
        
        for post in self.redirect_posts:
            title = post.get('title', {}).get('rendered', '').replace('Redirect:', '').strip()
            
            outline = None
            for topic, content_outline in content_outlines.items():
                if any(word.lower() in title.lower() for word in topic.split()):
                    outline = content_outline
                    break
            
            if outline:
                samples[title] = {
                    'outline': outline,
                    'estimated_sections': len(outline),
                    'estimated_words': len(outline) * 200,  # ~200 words per section
                    'content_type': 'comprehensive_analysis'
                }
        
        # Save samples
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        samples_file = f'content_samples_{timestamp}.json'
        
        with open(samples_file, 'w') as f:
            json.dump(samples, f, indent=2)
        
        print_success(f"✅ Content samples saved: {samples_file}")
        
        return samples_file


def main():
    """Main conversion execution."""
    print_info("🔄 REDIRECT TO CONTENT CONVERTER")
    print_info("=" * 50)
    
    converter = RedirectConverter()
    
    # Find redirect posts
    redirect_posts = converter.find_redirect_posts()
    
    if not redirect_posts:
        print_success("🎉 No redirect posts found! All posts have substantial content.")
        return True
    
    print_info(f"\n🎯 Found {len(redirect_posts)} posts that need content conversion")
    
    # Generate conversion plan
    plan_file = converter.generate_conversion_plan()
    
    # Generate content samples
    samples_file = converter.generate_content_samples()
    
    print_info(f"\n🚀 NEXT STEPS:")
    print_info("1. Review the conversion plan and content samples")
    print_info("2. Use WordPress admin to edit each post")
    print_info("3. Replace redirect content with comprehensive articles")
    print_info("4. Update categories and tags as suggested")
    print_info("5. Ensure each article has 1000+ words")
    print_info("6. Add proper headings, images, and SEO optimization")
    print_info("7. Run final verification to confirm completion")
    
    print_success(f"\n✅ Analysis complete!")
    print_info(f"📄 Conversion plan: {plan_file}")
    print_info(f"📝 Content samples: {samples_file}")
    
    return True


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)