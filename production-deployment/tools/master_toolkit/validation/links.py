"""
Link Validation and Fixing
==========================
Comprehensive link validation and broken link fixing utilities.
"""

import requests
import re
from typing import Dict, List, Tuple, Optional, Any
from urllib.parse import urljoin, urlparse
import time

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning, extract_internal_links, clean_url


class LinkValidator:
    """Link validation and fixing utilities."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize link validator."""
        self.wp = wp_client or WordPressClient()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (WordPress-Toolkit/1.0)'
        })
        
        # Known broken link mappings from successful fixes
        self.known_broken_links = {
            'https://spherevista360.com/product-analytics-2025/': 
                'https://spherevista360.com/product-analytics-in-2025-from-dashboards-to-decisions/',
            'https://spherevista360.com/on-device-vs-cloud-ai-2025/': 
                'https://spherevista360.com/on-device-ai-vs-cloud-ai-where-each-wins-in-2025/',
            'https://spherevista360.com/tech-innovation-2025/':
                'https://spherevista360.com/tech-innovations-that-will-transform-2025/',
            'https://spherevista360.com/data-privacy-future/':
                'https://spherevista360.com/the-future-of-data-privacy-new-laws-and-technologies/',
            'https://spherevista360.com/cloud-computing-evolution/':
                'https://spherevista360.com/cloud-computing-evolution-trends-and-predictions/'
        }
    
    def validate_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Validate a single URL."""
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            
            return {
                'url': url,
                'valid': response.status_code < 400,
                'status_code': response.status_code,
                'final_url': response.url,
                'redirected': response.url != url
            }
            
        except requests.RequestException as e:
            return {
                'url': url,
                'valid': False,
                'status_code': None,
                'error': str(e),
                'final_url': None,
                'redirected': False
            }
    
    def validate_links_in_content(self, content: str, domain: str = "spherevista360.com") -> Dict[str, Any]:
        """Validate all links in content."""
        internal_links = extract_internal_links(content, domain)
        
        results = {
            'total_links': len(internal_links),
            'broken_links': [],
            'valid_links': [],
            'validation_results': []
        }
        
        for link in internal_links:
            clean_link = clean_url(link)
            validation = self.validate_url(clean_link)
            results['validation_results'].append(validation)
            
            if validation['valid']:
                results['valid_links'].append(link)
            else:
                results['broken_links'].append(link)
        
        return results
    
    def validate_post_links(self, post_id: int) -> Dict[str, Any]:
        """Validate all links in a specific post."""
        try:
            post = self.wp.get_post(post_id)
            content = post['content']['rendered']
            
            results = self.validate_links_in_content(content)
            results['post_id'] = post_id
            results['post_title'] = post['title']['rendered']
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'post_id': post_id
            }
    
    def fix_broken_links_in_content(self, content: str) -> Tuple[str, List[str]]:
        """Fix broken links in content using known mappings."""
        fixed_content = content
        fixes_applied = []
        
        for broken_url, correct_url in self.known_broken_links.items():
            if broken_url in content:
                fixed_content = fixed_content.replace(broken_url, correct_url)
                fixes_applied.append(f"{broken_url} → {correct_url}")
        
        return fixed_content, fixes_applied
    
    def fix_post_links(self, post_id: int, dry_run: bool = False) -> Dict[str, Any]:
        """Fix broken links in a specific post."""
        try:
            # Get post content
            post = self.wp.get_post(post_id, context='edit')
            
            # Try to get raw content, fallback to rendered
            if 'raw' in post.get('content', {}):
                current_content = post['content']['raw']
                content_source = 'raw'
            else:
                current_content = post['content']['rendered']
                content_source = 'rendered'
            
            # Fix links
            fixed_content, fixes_applied = self.fix_broken_links_in_content(current_content)
            
            result = {
                'post_id': post_id,
                'post_title': post['title']['rendered'],
                'content_source': content_source,
                'fixes_applied': fixes_applied,
                'changes_made': len(fixes_applied) > 0
            }
            
            if not fixes_applied:
                result['message'] = 'No broken links found to fix'
                return result
            
            if dry_run:
                result['message'] = f'Would fix {len(fixes_applied)} broken links'
                return result
            
            # Update post
            update_data = {'content': fixed_content}
            self.wp.update_post(post_id, update_data)
            
            result['success'] = True
            result['message'] = f'Fixed {len(fixes_applied)} broken links'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }
    
    def scan_all_posts_for_broken_links(self, per_page: int = 10) -> Dict[str, Any]:
        """Scan all posts for broken links."""
        results = {
            'posts_scanned': 0,
            'posts_with_broken_links': 0,
            'total_broken_links': 0,
            'broken_links_by_post': []
        }
        
        page = 1
        while True:
            try:
                posts = self.wp.get_posts(per_page=per_page, page=page)
                if not posts:
                    break
                
                for post in posts:
                    post_id = post['id']
                    validation_result = self.validate_post_links(post_id)
                    
                    results['posts_scanned'] += 1
                    
                    if validation_result.get('broken_links'):
                        results['posts_with_broken_links'] += 1
                        results['total_broken_links'] += len(validation_result['broken_links'])
                        results['broken_links_by_post'].append({
                            'post_id': post_id,
                            'title': validation_result.get('post_title', 'Unknown'),
                            'broken_links': validation_result['broken_links']
                        })
                
                page += 1
                
            except Exception as e:
                print_error(f"Error scanning posts: {e}")
                break
        
        return results
    
    def fix_all_broken_links(self, post_ids: List[int] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Fix broken links in multiple posts."""
        if post_ids is None:
            # Get posts with known broken links
            post_ids = [1833, 1832, 1831, 1838, 1829, 1828]  # Known problematic posts
        
        results = {
            'total_posts': len(post_ids),
            'fixed_posts': 0,
            'failed_posts': 0,
            'total_fixes': 0,
            'results': []
        }
        
        for post_id in post_ids:
            print(f"Processing post {post_id}...")
            
            try:
                result = self.fix_post_links(post_id, dry_run)
                
                if result.get('success', True):  # Consider no changes as success
                    if result.get('changes_made'):
                        results['fixed_posts'] += 1
                        results['total_fixes'] += len(result.get('fixes_applied', []))
                else:
                    results['failed_posts'] += 1
                
                results['results'].append(result)
                
            except Exception as e:
                print_error(f"Error processing post {post_id}: {e}")
                results['failed_posts'] += 1
                results['results'].append({
                    'post_id': post_id,
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def verify_fixes(self, post_ids: List[int] = None) -> Dict[str, Any]:
        """Verify that broken links have been fixed."""
        if post_ids is None:
            post_ids = [1833, 1832, 1831, 1838, 1829, 1828]
        
        results = {
            'posts_checked': 0,
            'posts_clean': 0,
            'remaining_broken_links': 0,
            'verification_results': []
        }
        
        for post_id in post_ids:
            try:
                post = self.wp.get_post(post_id)
                content = post['content']['rendered']
                
                # Check for known broken URLs
                broken_found = []
                for broken_url in self.known_broken_links.keys():
                    if broken_url in content:
                        broken_found.append(broken_url)
                
                results['posts_checked'] += 1
                
                if not broken_found:
                    results['posts_clean'] += 1
                else:
                    results['remaining_broken_links'] += len(broken_found)
                
                results['verification_results'].append({
                    'post_id': post_id,
                    'title': post['title']['rendered'],
                    'broken_links_found': broken_found,
                    'is_clean': len(broken_found) == 0
                })
                
            except Exception as e:
                print_error(f"Error verifying post {post_id}: {e}")
        
        return results