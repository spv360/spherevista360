#!/usr/bin/env python3
"""
SEO Validation Module
====================
Comprehensive SEO validation and scoring for WordPress content.
"""

import re
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class SEOValidator:
    """SEO validation and scoring for WordPress content."""
    
    def __init__(self, domain: str = "spherevista360.com"):
        """Initialize SEO validator.
        
        Args:
            domain: Primary domain for internal link detection
        """
        self.domain = domain
        
    def validate_content(self, content: str, title: str, url: str) -> Dict:
        """Comprehensive SEO validation for content.
        
        Args:
            content: HTML content
            title: Page/post title
            url: Page/post URL
            
        Returns:
            Dict with SEO metrics and score
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        # H2 headings validation
        h2_data = self._validate_headings(soup)
        
        # Image validation
        image_data = self._validate_images(soup)
        
        # Title validation
        title_data = self._validate_title(title)
        
        # Internal links validation
        links_data = self._validate_internal_links(soup)
        
        # Meta description validation
        meta_data = self._validate_meta_description(soup)
        
        # Calculate overall score
        score_data = self._calculate_seo_score(
            h2_data, image_data, title_data, links_data, meta_data
        )
        
        return {
            'url': url,
            'title': title,
            'h2_headings': h2_data,
            'images': image_data,
            'title_validation': title_data,
            'internal_links': links_data,
            'meta_description': meta_data,
            'seo_score': score_data,
            'timestamp': self._get_timestamp()
        }
    
    def _validate_headings(self, soup: BeautifulSoup) -> Dict:
        """Validate H2 headings structure."""
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        
        headings = []
        for h2 in h2_tags:
            text = h2.get_text().strip()
            if text:
                headings.append(text)
        
        return {
            'count': len(headings),
            'h3_count': len(h3_tags),
            'headings': headings,
            'meets_requirement': len(headings) >= 2,
            'score': 1 if len(headings) >= 2 else 0,
            'recommendation': "Add more H2 headings" if len(headings) < 2 else "Good heading structure"
        }
    
    def _validate_images(self, soup: BeautifulSoup) -> Dict:
        """Validate images and alt text."""
        img_tags = soup.find_all('img')
        
        images = []
        images_with_alt = 0
        
        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt', '')
            if alt.strip():
                images_with_alt += 1
            
            images.append({
                'src': src,
                'alt': alt,
                'has_alt': bool(alt.strip())
            })
        
        return {
            'count': len(images),
            'images_with_alt': images_with_alt,
            'alt_percentage': (images_with_alt / len(images) * 100) if images else 0,
            'images': images,
            'meets_requirement': len(images) >= 1,
            'score': 1 if len(images) >= 1 else 0,
            'recommendation': "Add images to content" if len(images) < 1 else "Good image usage"
        }
    
    def _validate_title(self, title: str) -> Dict:
        """Validate title length and quality."""
        title_length = len(title) if title else 0
        is_optimal = 30 <= title_length <= 60
        is_acceptable = title_length <= 60
        exceeds_seo_limit = title_length > 60
        
        return {
            'title': title,
            'length': title_length,
            'is_optimal': is_optimal,
            'is_acceptable': is_acceptable,
            'exceeds_seo_limit': exceeds_seo_limit,
            'meets_requirement': is_acceptable,
            'score': 1 if is_acceptable else 0,
            'recommendation': self._get_title_recommendation(title_length),
            'seo_warning': f"Title exceeds 60 characters ({title_length} chars)" if exceeds_seo_limit else None
        }
    
    def _validate_internal_links(self, soup: BeautifulSoup) -> Dict:
        """Validate internal linking structure."""
        links = soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            if self.domain in href:
                internal_links.append({
                    'url': href,
                    'text': text,
                    'is_internal': True
                })
            elif href.startswith('http'):
                external_links.append({
                    'url': href,
                    'text': text,
                    'is_internal': False
                })
        
        return {
            'internal_count': len(internal_links),
            'external_count': len(external_links),
            'total_count': len(internal_links) + len(external_links),
            'internal_links': internal_links,
            'external_links': external_links,
            'meets_requirement': len(internal_links) >= 2,
            'score': 1 if len(internal_links) >= 2 else 0,
            'recommendation': "Add more internal links" if len(internal_links) < 2 else "Good internal linking"
        }
    
    def _validate_meta_description(self, soup: BeautifulSoup) -> Dict:
        """Validate meta description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ''
        
        desc_length = len(description)
        is_optimal = 120 <= desc_length <= 160
        is_acceptable = desc_length <= 160
        
        return {
            'description': description,
            'length': desc_length,
            'has_description': bool(description),
            'is_optimal': is_optimal,
            'is_acceptable': is_acceptable,
            'meets_requirement': bool(description),
            'score': 1 if description else 0,
            'recommendation': self._get_meta_recommendation(desc_length, description)
        }
    
    def _calculate_seo_score(self, h2_data: Dict, image_data: Dict, 
                           title_data: Dict, links_data: Dict, meta_data: Dict) -> Dict:
        """Calculate overall SEO score."""
        # Core scoring (required elements)
        core_score = (
            h2_data['score'] +
            image_data['score'] +
            title_data['score'] +
            links_data['score']
        )
        core_max = 4
        
        # Bonus scoring (nice to have)
        bonus_score = meta_data['score']
        bonus_max = 1
        
        # Calculate percentages
        core_percentage = (core_score / core_max) * 100
        total_score = core_score + bonus_score
        total_max = core_max + bonus_max
        total_percentage = (total_score / total_max) * 100
        
        return {
            'core_score': core_score,
            'core_max': core_max,
            'core_percentage': core_percentage,
            'bonus_score': bonus_score,
            'bonus_max': bonus_max,
            'total_score': total_score,
            'total_max': total_max,
            'total_percentage': total_percentage,
            'grade': self._get_seo_grade(core_percentage),
            'breakdown': f"{core_score}/{core_max} core + {bonus_score}/{bonus_max} bonus"
        }
    
    def _get_title_recommendation(self, length: int) -> str:
        """Get title length recommendation."""
        if length == 0:
            return "Add a title"
        elif length < 30:
            return "Title too short - expand to 30-60 characters"
        elif length > 60:
            return "⚠️ CRITICAL: Title exceeds 60 characters - shorten for SEO"
        else:
            return "Title length is optimal"
    
    def _get_meta_recommendation(self, length: int, description: str) -> str:
        """Get meta description recommendation."""
        if not description:
            return "Add meta description"
        elif length < 120:
            return "Meta description too short - expand to 120-160 characters"
        elif length > 160:
            return "Meta description too long - shorten to under 160 characters"
        else:
            return "Meta description length is optimal"
    
    def _get_seo_grade(self, percentage: float) -> str:
        """Get SEO grade based on percentage."""
        if percentage >= 100:
            return "A+"
        elif percentage >= 75:
            return "A"
        elif percentage >= 50:
            return "B"
        elif percentage >= 25:
            return "C"
        else:
            return "F"
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate SEO report from validation results.
        
        Args:
            results: List of SEO validation results
            
        Returns:
            Formatted report string
        """
        if not results:
            return "No results to report."
        
        # Calculate summary statistics
        total_items = len(results)
        avg_score = sum(r['seo_score']['core_percentage'] for r in results) / total_items
        perfect_scores = sum(1 for r in results if r['seo_score']['core_percentage'] == 100)
        
        report = []
        report.append("📊 SEO VALIDATION REPORT")
        report.append("=" * 50)
        report.append(f"🕒 Generated: {self._get_timestamp()}")
        report.append(f"📄 Total Items: {total_items}")
        report.append(f"📈 Average Score: {avg_score:.1f}%")
        report.append(f"🎯 Perfect Scores: {perfect_scores}/{total_items}")
        report.append("")
        
        # Individual results
        for i, result in enumerate(results, 1):
            score = result['seo_score']
            title_val = result['title_validation']
            
            # Check for SEO warnings
            seo_warning = ""
            if title_val.get('exceeds_seo_limit'):
                seo_warning = f" ⚠️ TITLE TOO LONG ({title_val['length']} chars)"
            
            report.append(f"{i}. {result['title'][:60]}...{seo_warning}")
            report.append(f"   📊 Score: {score['core_percentage']:.1f}% ({score['breakdown']})")
            report.append(f"   📝 H2 Headings: {result['h2_headings']['count']}")
            report.append(f"   🖼️ Images: {result['images']['count']}")
            report.append(f"   📏 Title: {result['title_validation']['length']}/60")
            report.append(f"   🔗 Internal Links: {result['internal_links']['internal_count']}")
            
            # Add specific warnings
            if title_val.get('seo_warning'):
                report.append(f"   ⚠️ {title_val['seo_warning']}")
            
            report.append("")
        
        return "\n".join(report)


def validate_single_post(wp_client, post_id: int) -> Dict:
    """Validate SEO for a single post.
    
    Args:
        wp_client: WordPress client instance
        post_id: Post ID
        
    Returns:
        SEO validation result
    """
    validator = SEOValidator()
    
    # Get post data
    post = wp_client.get_post(post_id)
    
    # Get full content
    content = wp_client.get_page_content(post['link'])
    
    # Validate SEO
    return validator.validate_content(content, post['title']['rendered'], post['link'])


def validate_all_posts(wp_client, category_filter: str = None) -> List[Dict]:
    """Validate SEO for all posts.
    
    Args:
        wp_client: WordPress client instance
        category_filter: Optional category name to filter by
        
    Returns:
        List of SEO validation results
    """
    validator = SEOValidator()
    results = []
    
    # Get posts
    posts = wp_client.get_posts(per_page=50)
    
    for post in posts:
        # Filter by category if specified
        if category_filter:
            categories = []
            for cat_id in post.get('categories', []):
                try:
                    cat = wp_client.get_category(cat_id)
                    categories.append(cat['name'])
                except:
                    continue
            
            if category_filter not in categories:
                continue
        
        # Get full content and validate
        try:
            content = wp_client.get_page_content(post['link'])
            result = validator.validate_content(
                content, post['title']['rendered'], post['link']
            )
            result['post_id'] = post['id']
            result['categories'] = categories if category_filter else []
            results.append(result)
        except Exception as e:
            print(f"⚠️ Error validating post {post['id']}: {e}")
    
    return results