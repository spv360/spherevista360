#!/usr/bin/env python3
"""
Comprehensive Validation Suite
==============================
Unified validation system for SEO, images, links, and content quality.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import concurrent.futures
import re

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))
from enhanced_wp_client import WordPressClient, print_header, print_section, format_percentage


class ContentValidator:
    """Comprehensive content validation system."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize validator."""
        self.wp = wp_client or WordPressClient()
        self.validation_results = {}
    
    def validate_seo(self, post: Dict) -> Dict:
        """Validate SEO elements of a post."""
        content = post.get('content', {}).get('rendered', '')
        title = post.get('title', {}).get('rendered', '')
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Core SEO checks
        h2_headings = len(soup.find_all('h2'))
        images = len(soup.find_all('img'))
        title_length = len(title)
        internal_links = len([a for a in soup.find_all('a') if 'spherevista360.com' in a.get('href', '')])
        
        # Calculate SEO score
        score = 0
        max_score = 5
        issues = []
        
        # Title length (10-60 characters optimal)
        if 10 <= title_length <= 60:
            score += 1
        else:
            issues.append(f"Title length: {title_length}/60 chars")
        
        # H2 headings (2+ recommended)
        if h2_headings >= 2:
            score += 1
        else:
            issues.append(f"Only {h2_headings} H2 headings (need 2+)")
        
        # Images (1+ required)
        if images >= 1:
            score += 1
        else:
            issues.append("No images found")
        
        # Internal links (3+ recommended)
        if internal_links >= 3:
            score += 1
        else:
            issues.append(f"Only {internal_links} internal links (need 3+)")
        
        # Content length (500+ words recommended)
        word_count = len(soup.get_text().split())
        if word_count >= 500:
            score += 1
        else:
            issues.append(f"Content too short: {word_count} words (need 500+)")
        
        percentage = (score / max_score) * 100
        
        return {
            'score': percentage,
            'grade': self._get_grade(percentage),
            'issues': issues,
            'metrics': {
                'title_length': title_length,
                'h2_headings': h2_headings,
                'images': images,
                'internal_links': internal_links,
                'word_count': word_count
            }
        }
    
    def validate_images(self, post: Dict) -> Dict:
        """Validate images in a post."""
        content = post.get('content', {}).get('rendered', '')
        soup = BeautifulSoup(content, 'html.parser')
        images = soup.find_all('img')
        
        issues = []
        score = 0
        max_score = 3
        
        if not images:
            return {
                'score': 0,
                'grade': 'F',
                'issues': ['No images found'],
                'metrics': {'total_images': 0, 'images_with_alt': 0, 'broken_images': 0}
            }
        
        # Check alt text
        images_with_alt = len([img for img in images if img.get('alt', '').strip()])
        if images_with_alt == len(images):
            score += 1
        else:
            issues.append(f"{len(images) - images_with_alt} images missing alt text")
        
        # Check image accessibility
        responsive_images = len([img for img in images if 'width: 100%' in img.get('style', '') or 'responsive' in img.get('class', '')])
        if responsive_images >= len(images) * 0.8:  # 80% responsive
            score += 1
        else:
            issues.append("Images not optimized for responsive design")
        
        # Check for broken images (basic check)
        external_images = len([img for img in images if img.get('src', '').startswith('http')])
        if external_images < len(images) * 0.5:  # Less than 50% external
            score += 1
        else:
            issues.append("Too many external images (hosting recommended)")
        
        percentage = (score / max_score) * 100
        
        return {
            'score': percentage,
            'grade': self._get_grade(percentage),
            'issues': issues,
            'metrics': {
                'total_images': len(images),
                'images_with_alt': images_with_alt,
                'external_images': external_images,
                'responsive_images': responsive_images
            }
        }
    
    def validate_links(self, post: Dict, check_external: bool = False) -> Dict:
        """Validate links in a post."""
        content = post.get('content', {}).get('rendered', '')
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)
        
        issues = []
        score = 0
        max_score = 2
        
        internal_links = [link for link in links if 'spherevista360.com' in link.get('href', '')]
        external_links = [link for link in links if link not in internal_links and link.get('href', '').startswith('http')]
        
        # Check internal link distribution
        if len(internal_links) >= 3:
            score += 1
        else:
            issues.append(f"Only {len(internal_links)} internal links (need 3+)")
        
        # Check for anchor text quality
        good_anchor_texts = 0
        for link in links:
            text = link.get_text().strip()
            if len(text) > 3 and not text.lower() in ['here', 'click', 'link', 'more']:
                good_anchor_texts += 1
        
        if good_anchor_texts >= len(links) * 0.8:  # 80% good anchor texts
            score += 1
        else:
            issues.append("Poor anchor text quality detected")
        
        # Optional: Check external links
        broken_links = 0
        if check_external and external_links:
            print("   🔗 Checking external links...")
            for link in external_links[:5]:  # Limit to 5 to avoid timeout
                try:
                    response = requests.head(link.get('href'), timeout=5)
                    if response.status_code >= 400:
                        broken_links += 1
                except:
                    broken_links += 1
            
            if broken_links > 0:
                issues.append(f"{broken_links} potentially broken external links")
        
        percentage = (score / max_score) * 100
        
        return {
            'score': percentage,
            'grade': self._get_grade(percentage),
            'issues': issues,
            'metrics': {
                'total_links': len(links),
                'internal_links': len(internal_links),
                'external_links': len(external_links),
                'broken_links': broken_links,
                'good_anchor_texts': good_anchor_texts
            }
        }
    
    def validate_post(self, post_id: int, check_external_links: bool = False) -> Dict:
        """Comprehensive validation of a single post."""
        post = self.wp.get_post(post_id)
        if not post:
            return {'error': f'Post {post_id} not found'}
        
        title = post.get('title', {}).get('rendered', 'Unknown')
        
        # Run all validations
        seo_result = self.validate_seo(post)
        image_result = self.validate_images(post)
        link_result = self.validate_links(post, check_external_links)
        
        # Calculate overall score
        overall_score = (seo_result['score'] + image_result['score'] + link_result['score']) / 3
        
        return {
            'post_id': post_id,
            'title': title,
            'overall_score': overall_score,
            'overall_grade': self._get_grade(overall_score),
            'seo': seo_result,
            'images': image_result,
            'links': link_result,
            'url': post.get('link', '')
        }
    
    def validate_category(self, category: str, check_external_links: bool = False) -> Dict:
        """Validate all posts in a category."""
        posts = self.wp.get_posts(per_page=50, category=category)
        if not posts:
            return {'error': f'No posts found in category: {category}'}
        
        results = []
        total_scores = {'seo': 0, 'images': 0, 'links': 0, 'overall': 0}
        
        print_section(f"VALIDATING CATEGORY: {category}")
        print(f"📄 Found {len(posts)} posts to validate")
        
        for post in posts:
            post_id = post.get('id')
            title = post.get('title', {}).get('rendered', 'Unknown')
            
            print(f"   🔍 Validating: {title[:50]}...")
            
            result = self.validate_post(post_id, check_external_links)
            if 'error' not in result:
                results.append(result)
                total_scores['seo'] += result['seo']['score']
                total_scores['images'] += result['images']['score']
                total_scores['links'] += result['links']['score']
                total_scores['overall'] += result['overall_score']
        
        # Calculate averages
        count = len(results)
        if count > 0:
            averages = {key: value / count for key, value in total_scores.items()}
        else:
            averages = {key: 0 for key in total_scores.keys()}
        
        return {
            'category': category,
            'total_posts': count,
            'average_scores': averages,
            'results': results
        }
    
    def generate_report(self, validation_data: Dict, output_file: str = None) -> str:
        """Generate a comprehensive validation report."""
        report_lines = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_lines.append("=" * 60)
        report_lines.append("📊 COMPREHENSIVE VALIDATION REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"🕒 Generated: {timestamp}")
        
        if 'category' in validation_data:
            # Category report
            data = validation_data
            report_lines.append(f"📂 Category: {data['category']}")
            report_lines.append(f"📄 Posts analyzed: {data['total_posts']}")
            report_lines.append("")
            
            # Average scores
            report_lines.append("📈 AVERAGE SCORES:")
            avg = data['average_scores']
            report_lines.append(f"   🎯 Overall: {format_percentage(avg['overall'])}")
            report_lines.append(f"   🔍 SEO: {format_percentage(avg['seo'])}")
            report_lines.append(f"   🖼️ Images: {format_percentage(avg['images'])}")
            report_lines.append(f"   🔗 Links: {format_percentage(avg['links'])}")
            report_lines.append("")
            
            # Individual post results
            report_lines.append("📋 INDIVIDUAL RESULTS:")
            for result in data['results']:
                score = result['overall_score']
                title = result['title'][:50]
                report_lines.append(f"   {format_percentage(score)} {title}...")
                
                # Add issues if score < 90%
                if score < 90:
                    all_issues = (result['seo']['issues'] + 
                                result['images']['issues'] + 
                                result['links']['issues'])
                    for issue in all_issues[:3]:  # Show top 3 issues
                        report_lines.append(f"      ⚠️ {issue}")
                report_lines.append("")
        
        else:
            # Single post report
            data = validation_data
            report_lines.append(f"📄 Post: {data['title']}")
            report_lines.append(f"🎯 Overall Score: {format_percentage(data['overall_score'])}")
            report_lines.append("")
            
            # Detailed breakdown
            for section, result in [('SEO', data['seo']), ('Images', data['images']), ('Links', data['links'])]:
                report_lines.append(f"📊 {section.upper()}: {format_percentage(result['score'])}")
                if result['issues']:
                    for issue in result['issues']:
                        report_lines.append(f"   ⚠️ {issue}")
                report_lines.append("")
        
        report = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Report saved to: {output_file}")
        
        return report
    
    def _get_grade(self, percentage: float) -> str:
        """Convert percentage to letter grade."""
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Comprehensive Content Validator')
    parser.add_argument('--post-id', type=int, help='Validate specific post by ID')
    parser.add_argument('--category', help='Validate all posts in category')
    parser.add_argument('--check-external', action='store_true', help='Check external links (slower)')
    parser.add_argument('--report', help='Save report to file')
    parser.add_argument('--username', help='WordPress username')
    parser.add_argument('--password', help='WordPress application password')
    
    args = parser.parse_args()
    
    if not args.post_id and not args.category:
        print("❌ Specify --post-id or --category")
        return 1
    
    print_header("COMPREHENSIVE CONTENT VALIDATOR")
    
    # Initialize WordPress client
    wp = WordPressClient()
    if not wp.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    # Initialize validator
    validator = ContentValidator(wp)
    
    # Run validation
    if args.post_id:
        result = validator.validate_post(args.post_id, args.check_external)
        if 'error' in result:
            print(f"❌ {result['error']}")
            return 1
        
        print(f"📄 Post: {result['title']}")
        print(f"🎯 Overall Score: {format_percentage(result['overall_score'])}")
        print(f"🔍 SEO: {format_percentage(result['seo']['score'])}")
        print(f"🖼️ Images: {format_percentage(result['images']['score'])}")
        print(f"🔗 Links: {format_percentage(result['links']['score'])}")
        
        # Generate report
        if args.report:
            validator.generate_report(result, args.report)
    
    elif args.category:
        result = validator.validate_category(args.category, args.check_external)
        if 'error' in result:
            print(f"❌ {result['error']}")
            return 1
        
        avg = result['average_scores']
        print_section("VALIDATION SUMMARY")
        print(f"📂 Category: {result['category']}")
        print(f"📄 Posts: {result['total_posts']}")
        print(f"🎯 Overall: {format_percentage(avg['overall'])}")
        print(f"🔍 SEO: {format_percentage(avg['seo'])}")
        print(f"🖼️ Images: {format_percentage(avg['images'])}")
        print(f"🔗 Links: {format_percentage(avg['links'])}")
        
        # Generate report
        if args.report:
            validator.generate_report(result, args.report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())