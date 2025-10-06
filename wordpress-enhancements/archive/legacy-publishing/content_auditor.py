#!/usr/bin/env python3
"""
WordPress Content Audit and Duplicate Removal Tool
Analyzes website content to identify and remove duplicate or low-quality posts
"""

import os
import sys
import requests
import base64
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict

class WordPressContentAuditor:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_APP_PASS')
        
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
        self.posts = []
        self.pages = []
        self.duplicates = []
        
    def fetch_all_content(self) -> Dict:
        """Fetch all posts and pages from WordPress"""
        print("📊 Fetching all content from WordPress...")
        
        try:
            # Fetch all posts
            posts_response = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={'per_page': 100, 'status': 'publish'}
            )
            
            if posts_response.status_code == 200:
                self.posts = posts_response.json()
                print(f"  ✅ Found {len(self.posts)} published posts")
            else:
                print(f"  ❌ Failed to fetch posts: {posts_response.status_code}")
                
            # Fetch all pages
            pages_response = requests.get(
                f"{self.base_url}/pages",
                headers=self.headers,
                params={'per_page': 100, 'status': 'publish'}
            )
            
            if pages_response.status_code == 200:
                self.pages = pages_response.json()
                print(f"  ✅ Found {len(self.pages)} published pages")
            else:
                print(f"  ❌ Failed to fetch pages: {pages_response.status_code}")
                
            return {
                'posts': self.posts,
                'pages': self.pages,
                'total_content': len(self.posts) + len(self.pages)
            }
            
        except Exception as e:
            print(f"  ❌ Error fetching content: {e}")
            return {'posts': [], 'pages': [], 'total_content': 0}
    
    def analyze_content_quality(self, content_item: Dict) -> Dict:
        """Analyze individual content piece for quality metrics"""
        title = content_item.get('title', {}).get('rendered', '')
        content = content_item.get('content', {}).get('rendered', '')
        excerpt = content_item.get('excerpt', {}).get('rendered', '')
        
        # Remove HTML tags for analysis
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_title = re.sub(r'<[^>]+>', '', title)
        
        # Calculate metrics
        word_count = len(clean_content.split())
        title_length = len(clean_title)
        has_excerpt = bool(excerpt.strip())
        
        # Quality scoring
        quality_score = 0
        
        # Word count scoring (300-2000 words is good)
        if 300 <= word_count <= 2000:
            quality_score += 3
        elif 100 <= word_count < 300:
            quality_score += 1
        elif word_count > 2000:
            quality_score += 2
        
        # Title length scoring (30-60 characters is good)
        if 30 <= title_length <= 60:
            quality_score += 2
        elif 20 <= title_length < 30 or 60 < title_length <= 80:
            quality_score += 1
        
        # Has excerpt
        if has_excerpt:
            quality_score += 1
            
        # Published date (newer is better)
        published_date = content_item.get('date', '')
        if published_date:
            try:
                pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                days_old = (datetime.now().replace(tzinfo=pub_date.tzinfo) - pub_date).days
                if days_old <= 30:
                    quality_score += 2
                elif days_old <= 90:
                    quality_score += 1
            except:
                pass
        
        return {
            'id': content_item.get('id'),
            'title': clean_title,
            'slug': content_item.get('slug', ''),
            'word_count': word_count,
            'title_length': title_length,
            'has_excerpt': has_excerpt,
            'published_date': published_date,
            'quality_score': quality_score,
            'link': content_item.get('link', ''),
            'type': content_item.get('type', 'post')
        }
    
    def find_duplicate_content(self) -> List[Dict]:
        """Identify potential duplicate content"""
        print("🔍 Analyzing content for duplicates...")
        
        all_content = self.posts + self.pages
        content_analysis = []
        
        # Analyze each piece of content
        for item in all_content:
            analysis = self.analyze_content_quality(item)
            content_analysis.append(analysis)
        
        # Group by similar titles and topics
        duplicates = []
        title_groups = defaultdict(list)
        
        for analysis in content_analysis:
            # Group by similar title words
            title_words = set(analysis['title'].lower().split())
            # Remove common words
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
            title_words = title_words - common_words
            
            # Create a key from significant title words
            if title_words:
                key = ' '.join(sorted(list(title_words)[:3]))  # Use top 3 significant words
                title_groups[key].append(analysis)
        
        # Find groups with multiple items (potential duplicates)
        for key, group in title_groups.items():
            if len(group) > 1:
                # Sort by quality score (best first)
                group.sort(key=lambda x: x['quality_score'], reverse=True)
                duplicates.append({
                    'topic': key,
                    'count': len(group),
                    'items': group
                })
        
        # Sort duplicates by count (most duplicates first)
        duplicates.sort(key=lambda x: x['count'], reverse=True)
        
        print(f"  ✅ Found {len(duplicates)} potential duplicate topic groups")
        
        return duplicates
    
    def identify_low_quality_content(self) -> List[Dict]:
        """Identify low-quality content for potential removal"""
        print("📉 Identifying low-quality content...")
        
        all_content = self.posts + self.pages
        low_quality = []
        
        for item in all_content:
            analysis = self.analyze_content_quality(item)
            
            # Flag as low quality if:
            # - Quality score <= 2
            # - Word count < 100
            # - Very old content (>1 year) with low engagement
            
            is_low_quality = False
            reasons = []
            
            if analysis['quality_score'] <= 2:
                is_low_quality = True
                reasons.append(f"Low quality score: {analysis['quality_score']}/8")
            
            if analysis['word_count'] < 100:
                is_low_quality = True
                reasons.append(f"Very short content: {analysis['word_count']} words")
            
            if analysis['title_length'] < 10:
                is_low_quality = True
                reasons.append(f"Very short title: {analysis['title_length']} characters")
            
            # Check if it's a default WordPress page/post
            default_titles = ['hello world', 'sample page', 'privacy policy', 'about', 'contact']
            if any(default in analysis['title'].lower() for default in default_titles):
                if analysis['word_count'] < 200:  # Unless it's been customized
                    is_low_quality = True
                    reasons.append("Default WordPress content")
            
            if is_low_quality:
                analysis['removal_reasons'] = reasons
                low_quality.append(analysis)
        
        # Sort by quality score (worst first)
        low_quality.sort(key=lambda x: x['quality_score'])
        
        print(f"  ✅ Found {len(low_quality)} low-quality items")
        
        return low_quality
    
    def generate_removal_recommendations(self) -> Dict:
        """Generate recommendations for content removal"""
        print("📋 Generating removal recommendations...")
        
        duplicates = self.find_duplicate_content()
        low_quality = self.identify_low_quality_content()
        
        recommendations = {
            'duplicate_groups': duplicates,
            'low_quality_items': low_quality,
            'total_items_for_removal': 0,
            'removal_plan': []
        }
        
        removal_plan = []
        
        # Process duplicate groups
        for group in duplicates:
            # Keep the best quality item, mark others for removal
            items = group['items']
            keep_item = items[0]  # Already sorted by quality score
            remove_items = items[1:]
            
            for item in remove_items:
                removal_plan.append({
                    'id': item['id'],
                    'title': item['title'],
                    'type': item['type'],
                    'reason': f"Duplicate of '{keep_item['title']}' (lower quality)",
                    'quality_score': item['quality_score'],
                    'keep_instead_id': keep_item['id'],
                    'keep_instead_title': keep_item['title']
                })
        
        # Process low quality items
        for item in low_quality:
            # Check if it's not already in removal plan due to duplicates
            if not any(plan['id'] == item['id'] for plan in removal_plan):
                removal_plan.append({
                    'id': item['id'],
                    'title': item['title'],
                    'type': item['type'],
                    'reason': '; '.join(item['removal_reasons']),
                    'quality_score': item['quality_score'],
                    'keep_instead_id': None,
                    'keep_instead_title': None
                })
        
        recommendations['removal_plan'] = removal_plan
        recommendations['total_items_for_removal'] = len(removal_plan)
        
        print(f"  ✅ Recommended {len(removal_plan)} items for removal")
        
        return recommendations
    
    def create_removal_script(self, recommendations: Dict) -> str:
        """Create a script to safely remove recommended content"""
        script_content = """#!/usr/bin/env python3
'''
WordPress Content Removal Script
IMPORTANT: Review all recommendations before executing!
'''

import requests
import base64
import os
import json

# WordPress credentials (ensure these are set)
WP_SITE = os.environ.get('WP_SITE')
WP_USER = os.environ.get('WP_USER')
WP_APP_PASS = os.environ.get('WP_APP_PASS')

if not all([WP_SITE, WP_USER, WP_APP_PASS]):
    print("❌ WordPress credentials not set!")
    exit(1)

credentials = f"{WP_USER}:{WP_APP_PASS}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json'
}

# Items to remove (review this list carefully!)
ITEMS_TO_REMOVE = [
"""
        
        for item in recommendations['removal_plan']:
            script_content += f"""    {{
        'id': {item['id']},
        'title': '{item['title'].replace("'", "\\'")}',
        'type': '{item['type']}',
        'reason': '{item['reason'].replace("'", "\\'")}'
    }},
"""
        
        script_content += """]

def remove_content_item(item):
    '''Remove a single content item'''
    item_type = item['type']
    item_id = item['id']
    
    if item_type == 'post':
        url = f"{WP_SITE}/wp-json/wp/v2/posts/{item_id}"
    elif item_type == 'page':
        url = f"{WP_SITE}/wp-json/wp/v2/pages/{item_id}"
    else:
        print(f"❌ Unknown content type: {item_type}")
        return False
    
    # Move to trash (safer than permanent deletion)
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Moved to trash: {item['title']}")
        return True
    else:
        print(f"❌ Failed to remove: {item['title']} (Status: {response.status_code})")
        return False

def main():
    print("🗑️ WordPress Content Cleanup")
    print("=" * 30)
    print(f"Items to remove: {len(ITEMS_TO_REMOVE)}")
    print()
    
    # Display items for review
    print("📋 Items scheduled for removal:")
    for i, item in enumerate(ITEMS_TO_REMOVE, 1):
        print(f"{i:2d}. {item['title']} ({item['type']})")
        print(f"    Reason: {item['reason']}")
        print()
    
    # Confirmation
    response = input("Do you want to proceed with removal? (type 'yes' to confirm): ")
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        return
    
    # Remove items
    success_count = 0
    for item in ITEMS_TO_REMOVE:
        if remove_content_item(item):
            success_count += 1
    
    print(f"\\n✅ Removal complete: {success_count}/{len(ITEMS_TO_REMOVE)} items moved to trash")
    print("💡 Items are moved to trash and can be restored if needed")

if __name__ == "__main__":
    main()
"""
        
        return script_content
    
    def run_content_audit(self):
        """Run complete content audit"""
        print("🔍 WordPress Content Audit & Cleanup")
        print("=" * 40)
        print(f"🌐 Analyzing: {self.wp_site}")
        print()
        
        # Fetch all content
        content_summary = self.fetch_all_content()
        
        if content_summary['total_content'] == 0:
            print("❌ No content found or unable to connect")
            return False
        
        print(f"📊 Total content found: {content_summary['total_content']}")
        print(f"   Posts: {len(self.posts)}")
        print(f"   Pages: {len(self.pages)}")
        print()
        
        # Generate recommendations
        recommendations = self.generate_removal_recommendations()
        
        # Save detailed analysis
        with open('wordpress-enhancements/configs/content_audit_report.json', 'w') as f:
            json.dump(recommendations, f, indent=2)
        print("💾 Detailed report saved: wordpress-enhancements/configs/content_audit_report.json")
        
        # Create removal script
        removal_script = self.create_removal_script(recommendations)
        with open('wordpress-enhancements/scripts/remove_duplicate_content.py', 'w') as f:
            f.write(removal_script)
        os.chmod('wordpress-enhancements/scripts/remove_duplicate_content.py', 0o755)
        print("💾 Removal script created: wordpress-enhancements/scripts/remove_duplicate_content.py")
        
        # Display summary
        print(f"\\n📋 Audit Summary:")
        print("=" * 20)
        print(f"🔍 Total content analyzed: {content_summary['total_content']}")
        print(f"🔄 Duplicate topic groups: {len(recommendations['duplicate_groups'])}")
        print(f"📉 Low-quality items: {len(recommendations['low_quality_items'])}")
        print(f"🗑️ Items recommended for removal: {recommendations['total_items_for_removal']}")
        
        if recommendations['total_items_for_removal'] > 0:
            print(f"\\n🎯 Potential space savings:")
            print(f"   Remove {recommendations['total_items_for_removal']} items")
            print(f"   Keep {content_summary['total_content'] - recommendations['total_items_for_removal']} high-quality items")
            
            percentage_reduction = (recommendations['total_items_for_removal'] / content_summary['total_content']) * 100
            print(f"   Reduction: {percentage_reduction:.1f}%")
            
            print(f"\\n🚀 Next Steps:")
            print("1. Review the audit report: wordpress-enhancements/configs/content_audit_report.json")
            print("2. Examine recommended removals carefully")
            print("3. Run removal script if satisfied: python wordpress-enhancements/scripts/remove_duplicate_content.py")
            print("4. Items will be moved to trash (can be restored if needed)")
        else:
            print(f"\\n✅ Your content looks good! No duplicates or low-quality items found.")
        
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
        auditor = WordPressContentAuditor()
        return auditor.run_content_audit()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()