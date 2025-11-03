"""
Technical SEO Validation
=======================
Technical SEO validation including sitemaps, robots.txt, and duplicate content detection.
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
import hashlib
from difflib import SequenceMatcher

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class TechnicalValidator:
    """Technical SEO validation utilities."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize technical validator."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
    
    def validate_sitemap_inclusion(self, post_id: int) -> Dict[str, Any]:
        """Check if a post is included in the XML sitemap."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            post_url = post.get('link', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'sitemap': {
                    'found_in_sitemap': False,
                    'sitemap_accessible': False,
                    'lastmod_present': False
                },
                'issues': [],
                'recommendations': [],
                'score': 0
            }
            
            # Try common sitemap URLs
            sitemap_urls = [
                f"{self.base_url}/sitemap.xml",
                f"{self.base_url}/sitemap_index.xml",
                f"{self.base_url}/wp-sitemap.xml"
            ]
            
            sitemap_content = None
            working_sitemap_url = None
            
            for sitemap_url in sitemap_urls:
                try:
                    response = requests.get(sitemap_url, timeout=10)
                    if response.status_code == 200:
                        sitemap_content = response.text
                        working_sitemap_url = sitemap_url
                        result['sitemap']['sitemap_accessible'] = True
                        result['score'] += 30
                        break
                except Exception:
                    continue
            
            if not sitemap_content:
                result['issues'].append('No accessible sitemap found')
                result['recommendations'].append('Create and submit XML sitemap to search engines')
                return result
            
            # Parse XML sitemap
            try:
                root = ET.fromstring(sitemap_content)
                
                # Handle sitemap index
                if 'sitemapindex' in root.tag:
                    # Get individual sitemaps
                    sitemaps = []
                    for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                        loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                        if loc is not None:
                            sitemaps.append(loc.text)
                    
                    # Check each sitemap for the post
                    for sitemap_url in sitemaps:
                        try:
                            response = requests.get(sitemap_url, timeout=10)
                            if response.status_code == 200:
                                if self._check_url_in_sitemap(response.text, post_url):
                                    result['sitemap']['found_in_sitemap'] = True
                                    result['score'] += 50
                                    break
                        except Exception:
                            continue
                
                else:
                    # Direct sitemap
                    if self._check_url_in_sitemap(sitemap_content, post_url):
                        result['sitemap']['found_in_sitemap'] = True
                        result['score'] += 50
                
            except ET.ParseError:
                result['issues'].append('Sitemap XML is malformed')
                result['recommendations'].append('Fix sitemap XML syntax errors')
            
            # Generate recommendations
            if not result['sitemap']['found_in_sitemap']:
                result['recommendations'].append('Post not found in sitemap - may affect search engine discovery')
            
            if result['score'] >= 80:
                result['status'] = 'excellent'
                result['message'] = 'Post properly included in sitemap'
            elif result['score'] >= 50:
                result['status'] = 'good'
                result['message'] = 'Post found in sitemap'
            elif result['score'] >= 30:
                result['status'] = 'fair'
                result['message'] = 'Sitemap accessible but post not included'
            else:
                result['status'] = 'poor'
                result['message'] = 'Sitemap issues detected'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error validating sitemap inclusion: {str(e)}'
            }
    
    def _check_url_in_sitemap(self, sitemap_content: str, target_url: str) -> bool:
        """Check if a URL is present in sitemap content."""
        try:
            root = ET.fromstring(sitemap_content)
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None and target_url in loc.text:
                    return True
            return False
        except Exception:
            return False
    
    def validate_robots_txt(self) -> Dict[str, Any]:
        """Validate robots.txt file."""
        try:
            robots_url = f"{self.base_url}/robots.txt"
            
            result = {
                'robots_txt': {
                    'accessible': False,
                    'has_sitemap': False,
                    'allows_crawling': True,
                    'blocks_important_paths': False
                },
                'issues': [],
                'recommendations': [],
                'score': 0
            }
            
            try:
                response = requests.get(robots_url, timeout=10)
                if response.status_code == 200:
                    result['robots_txt']['accessible'] = True
                    result['score'] += 25
                    
                    robots_content = response.text.lower()
                    
                    # Check for sitemap reference
                    if 'sitemap:' in robots_content:
                        result['robots_txt']['has_sitemap'] = True
                        result['score'] += 25
                    else:
                        result['recommendations'].append('Add sitemap reference to robots.txt')
                    
                    # Check for problematic disallows
                    problematic_disallows = ['/wp-content/', '/wp-admin/admin-ajax.php', '/wp-json/']
                    for disallow in problematic_disallows:
                        if f'disallow: {disallow}' in robots_content:
                            result['robots_txt']['blocks_important_paths'] = True
                            result['issues'].append(f'Robots.txt blocks important path: {disallow}')
                    
                    # Check if crawling is completely blocked
                    if 'disallow: /' in robots_content and 'user-agent: *' in robots_content:
                        result['robots_txt']['allows_crawling'] = False
                        result['issues'].append('Robots.txt blocks all crawling')
                    else:
                        result['score'] += 50
                
                else:
                    result['issues'].append(f'Robots.txt not accessible (HTTP {response.status_code})')
                    
            except Exception as e:
                result['issues'].append(f'Error accessing robots.txt: {str(e)}')
            
            if result['score'] >= 75:
                result['status'] = 'excellent'
                result['message'] = 'Robots.txt properly configured'
            elif result['score'] >= 50:
                result['status'] = 'good'
                result['message'] = 'Robots.txt accessible with minor issues'
            elif result['score'] >= 25:
                result['status'] = 'fair'
                result['message'] = 'Robots.txt needs improvement'
            else:
                result['status'] = 'poor'
                result['message'] = 'Robots.txt has significant issues'
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error validating robots.txt: {str(e)}'
            }
    
    def check_duplicate_content(self, post_id: int, similarity_threshold: float = 0.8) -> Dict[str, Any]:
        """Check for duplicate content across the site."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            post_content = post.get('content', {}).get('rendered', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'duplicate_check': {
                    'similar_posts': [],
                    'similarity_scores': {},
                    'highest_similarity': 0.0
                },
                'issues': [],
                'recommendations': [],
                'score': 100  # Start with perfect score, deduct for issues
            }
            
            if not post_content:
                result['issues'].append('No content to analyze')
                return result
            
            # Get all other posts for comparison
            all_posts = self.wp.get_posts(per_page=100)
            
            # Clean content for comparison
            clean_content = self._clean_content_for_comparison(post_content)
            content_hash = hashlib.md5(clean_content.encode()).hexdigest()
            
            for other_post in all_posts:
                if other_post['id'] == post_id:
                    continue
                
                other_content = other_post.get('content', {}).get('rendered', '')
                if not other_content:
                    continue
                
                other_clean = self._clean_content_for_comparison(other_content)
                other_hash = hashlib.md5(other_clean.encode()).hexdigest()
                
                # Check for exact duplicates first
                if content_hash == other_hash:
                    result['duplicate_check']['similar_posts'].append({
                        'id': other_post['id'],
                        'title': other_post.get('title', {}).get('rendered', 'Untitled'),
                        'similarity': 1.0,
                        'type': 'exact_duplicate'
                    })
                    result['score'] = 0
                    result['issues'].append(f'Exact duplicate found: {other_post.get("title", {}).get("rendered", "Untitled")}')
                    continue
                
                # Check similarity
                similarity = self._calculate_similarity(clean_content, other_clean)
                
                if similarity >= similarity_threshold:
                    result['duplicate_check']['similar_posts'].append({
                        'id': other_post['id'],
                        'title': other_post.get('title', {}).get('rendered', 'Untitled'),
                        'similarity': similarity,
                        'type': 'high_similarity'
                    })
                    
                    result['duplicate_check']['similarity_scores'][other_post['id']] = similarity
                    
                    if similarity > result['duplicate_check']['highest_similarity']:
                        result['duplicate_check']['highest_similarity'] = similarity
                    
                    # Deduct score based on similarity
                    score_deduction = int((similarity - similarity_threshold) * 100)
                    result['score'] = max(0, result['score'] - score_deduction)
                    
                    result['issues'].append(f'High similarity ({similarity:.2%}) with: {other_post.get("title", {}).get("rendered", "Untitled")}')
            
            # Generate recommendations
            if result['duplicate_check']['similar_posts']:
                result['recommendations'].append('Review similar content and add unique value or consolidate posts')
                result['recommendations'].append('Consider using canonical tags to specify preferred version')
            
            if result['score'] >= 90:
                result['status'] = 'excellent'
                result['message'] = 'No duplicate content issues detected'
            elif result['score'] >= 70:
                result['status'] = 'good'
                result['message'] = 'Minor content similarity detected'
            elif result['score'] >= 50:
                result['status'] = 'fair'
                result['message'] = 'Some content similarity issues found'
            else:
                result['status'] = 'poor'
                result['message'] = 'Significant duplicate content issues'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error checking duplicate content: {str(e)}'
            }
    
    def _clean_content_for_comparison(self, content: str) -> str:
        """Clean content for duplicate comparison."""
        from bs4 import BeautifulSoup
        import re
        
        # Remove HTML tags
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common words and normalize
        text = text.lower().strip()
        
        return text
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings."""
        return SequenceMatcher(None, text1, text2).ratio()