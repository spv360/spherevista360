#!/usr/bin/env python3
"""
Link Validation and Menu Checker Module
=======================================
Tools for validating links and checking menu structure in WordPress.
"""

import requests
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class LinkValidator:
    """Link validation and menu checking for WordPress."""
    
    def __init__(self, wp_client=None, domain: str = "spherevista360.com"):
        """Initialize link validator.
        
        Args:
            wp_client: WordPress client instance
            domain: Domain for internal link detection
        """
        self.wp_client = wp_client
        self.domain = domain
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WordPress Link Validator 1.0'
        })
    
    def validate_page_links(self, content: str, base_url: str) -> Dict:
        """Validate all links on a page.
        
        Args:
            content: HTML content
            base_url: Base URL for relative links
            
        Returns:
            Dict with link validation results
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        results = {
            'total_links': len(links),
            'internal_links': [],
            'external_links': [],
            'broken_links': [],
            'working_links': [],
            'email_links': [],
            'anchor_links': [],
            'validation_summary': {}
        }
        
        # Process each link
        for link in links:
            href = link.get('href', '').strip()
            text = link.get_text().strip()
            
            if not href:
                continue
            
            link_data = {
                'url': href,
                'text': text,
                'type': self._classify_link(href),
                'status_code': 0,
                'response_time': 0,
                'is_working': False,
                'error': None
            }
            
            # Skip email and anchor links for HTTP testing
            if link_data['type'] in ['email', 'anchor']:
                if link_data['type'] == 'email':
                    results['email_links'].append(link_data)
                else:
                    results['anchor_links'].append(link_data)
                continue
            
            # Resolve relative URLs
            if href.startswith('/') or not href.startswith('http'):
                full_url = urljoin(base_url, href)
                link_data['url'] = full_url
            
            # Test link
            status = self._test_link(link_data['url'])
            link_data.update(status)
            
            # Categorize link
            if link_data['is_working']:
                results['working_links'].append(link_data)
            else:
                results['broken_links'].append(link_data)
            
            if link_data['type'] == 'internal':
                results['internal_links'].append(link_data)
            else:
                results['external_links'].append(link_data)
        
        # Generate summary
        results['validation_summary'] = {
            'total_tested': len(results['working_links']) + len(results['broken_links']),
            'working_count': len(results['working_links']),
            'broken_count': len(results['broken_links']),
            'internal_count': len(results['internal_links']),
            'external_count': len(results['external_links']),
            'email_count': len(results['email_links']),
            'anchor_count': len(results['anchor_links']),
            'success_rate': self._calculate_success_rate(results)
        }
        
        return results
    
    def validate_menu_structure(self) -> Dict:
        """Validate WordPress menu structure.
        
        Returns:
            Dict with menu validation results
        """
        if not self.wp_client:
            return {'error': 'WordPress client not available'}
        
        try:
            # Get homepage to find menu
            homepage_content = self.wp_client.get_page_content(f"https://{self.domain}/")
            soup = BeautifulSoup(homepage_content, 'html.parser')
            
            # Find menu elements
            menu_elements = soup.find_all(['nav', 'ul'], class_=re.compile(r'menu|nav', re.I))
            
            results = {
                'menus_found': len(menu_elements),
                'menu_data': [],
                'all_menu_links': [],
                'broken_menu_links': [],
                'duplicate_links': [],
                'menu_summary': {}
            }
            
            all_urls = []
            
            for i, menu in enumerate(menu_elements):
                menu_links = menu.find_all('a', href=True)
                
                menu_data = {
                    'menu_index': i + 1,
                    'link_count': len(menu_links),
                    'links': []
                }
                
                for link in menu_links:
                    href = link.get('href', '').strip()
                    text = link.get_text().strip()
                    
                    if not href or not text:
                        continue
                    
                    # Test link
                    status = self._test_link(href)
                    
                    link_data = {
                        'url': href,
                        'text': text,
                        'menu_index': i + 1,
                        **status
                    }
                    
                    menu_data['links'].append(link_data)
                    results['all_menu_links'].append(link_data)
                    
                    # Track for duplicates
                    all_urls.append(href)
                    
                    # Track broken links
                    if not status['is_working']:
                        results['broken_menu_links'].append(link_data)
                
                results['menu_data'].append(menu_data)
            
            # Find duplicates
            url_counts = {}
            for url in all_urls:
                url_counts[url] = url_counts.get(url, 0) + 1
            
            duplicates = {url: count for url, count in url_counts.items() if count > 1}
            results['duplicate_links'] = [
                {'url': url, 'count': count} for url, count in duplicates.items()
            ]
            
            # Generate summary
            total_menu_links = len(results['all_menu_links'])
            working_menu_links = sum(1 for link in results['all_menu_links'] if link['is_working'])
            
            results['menu_summary'] = {
                'total_menu_links': total_menu_links,
                'working_menu_links': working_menu_links,
                'broken_menu_links': len(results['broken_menu_links']),
                'duplicate_count': len(results['duplicate_links']),
                'menu_success_rate': (working_menu_links / total_menu_links * 100) if total_menu_links > 0 else 0
            }
            
            return results
            
        except Exception as e:
            return {'error': f'Failed to validate menu: {str(e)}'}
    
    def scan_site_for_broken_links(self, max_pages: int = 10) -> Dict:
        """Scan multiple pages for broken links.
        
        Args:
            max_pages: Maximum number of pages to scan
            
        Returns:
            Dict with comprehensive broken link results
        """
        if not self.wp_client:
            return {'error': 'WordPress client not available'}
        
        results = {
            'pages_scanned': 0,
            'total_links_found': 0,
            'broken_links': [],
            'pages_with_issues': [],
            'summary': {}
        }
        
        try:
            # Get posts and pages to scan
            posts = self.wp_client.get_posts(per_page=max_pages // 2)
            pages = self.wp_client.get_pages(per_page=max_pages // 2)
            
            all_content = []
            
            # Add posts
            for post in posts:
                all_content.append({
                    'type': 'post',
                    'id': post['id'],
                    'title': post['title']['rendered'],
                    'url': post['link']
                })
            
            # Add pages
            for page in pages:
                all_content.append({
                    'type': 'page',
                    'id': page['id'],
                    'title': page['title']['rendered'],
                    'url': page['link']
                })
            
            # Scan each piece of content
            for content_item in all_content[:max_pages]:
                try:
                    # Get page content
                    page_content = self.wp_client.get_page_content(content_item['url'])
                    
                    # Validate links
                    link_results = self.validate_page_links(page_content, content_item['url'])
                    
                    results['pages_scanned'] += 1
                    results['total_links_found'] += link_results['total_links']
                    
                    # Add broken links with context
                    for broken_link in link_results['broken_links']:
                        broken_link['source_page'] = content_item['title']
                        broken_link['source_url'] = content_item['url']
                        broken_link['source_type'] = content_item['type']
                        results['broken_links'].append(broken_link)
                    
                    # Track pages with issues
                    if link_results['broken_links']:
                        results['pages_with_issues'].append({
                            'title': content_item['title'],
                            'url': content_item['url'],
                            'type': content_item['type'],
                            'broken_count': len(link_results['broken_links'])
                        })
                
                except Exception as e:
                    print(f"⚠️ Error scanning {content_item['title']}: {e}")
            
            # Generate summary
            results['summary'] = {
                'pages_scanned': results['pages_scanned'],
                'pages_with_issues': len(results['pages_with_issues']),
                'total_broken_links': len(results['broken_links']),
                'health_score': self._calculate_site_health_score(results)
            }
            
            return results
            
        except Exception as e:
            return {'error': f'Failed to scan site: {str(e)}'}
    
    def _classify_link(self, href: str) -> str:
        """Classify link type."""
        if href.startswith('mailto:'):
            return 'email'
        elif href.startswith('#'):
            return 'anchor'
        elif self.domain in href:
            return 'internal'
        elif href.startswith('http'):
            return 'external'
        else:
            return 'relative'
    
    def _test_link(self, url: str, timeout: int = 10) -> Dict:
        """Test if a link is working.
        
        Args:
            url: URL to test
            timeout: Request timeout in seconds
            
        Returns:
            Dict with test results
        """
        start_time = time.time()
        
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            response_time = time.time() - start_time
            
            return {
                'status_code': response.status_code,
                'response_time': response_time,
                'is_working': response.status_code < 400,
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {
                'status_code': 0,
                'response_time': timeout,
                'is_working': False,
                'error': 'Timeout'
            }
            
        except requests.exceptions.ConnectionError:
            return {
                'status_code': 0,
                'response_time': time.time() - start_time,
                'is_working': False,
                'error': 'Connection Error'
            }
            
        except Exception as e:
            return {
                'status_code': 0,
                'response_time': time.time() - start_time,
                'is_working': False,
                'error': str(e)[:50]
            }
    
    def _calculate_success_rate(self, results: Dict) -> float:
        """Calculate link success rate."""
        total_tested = results['validation_summary']['total_tested']
        working = results['validation_summary']['working_count']
        
        return (working / total_tested * 100) if total_tested > 0 else 0
    
    def _calculate_site_health_score(self, results: Dict) -> float:
        """Calculate overall site health score based on broken links."""
        pages_scanned = results['pages_scanned']
        pages_with_issues = len(results['pages_with_issues'])
        
        if pages_scanned == 0:
            return 0
        
        # Score based on percentage of pages without issues
        clean_pages = pages_scanned - pages_with_issues
        return (clean_pages / pages_scanned * 100)


def validate_post_links(wp_client, post_id: int) -> Dict:
    """Validate links for a specific post.
    
    Args:
        wp_client: WordPress client instance
        post_id: Post ID
        
    Returns:
        Link validation results
    """
    validator = LinkValidator(wp_client)
    
    # Get post data
    post = wp_client.get_post(post_id)
    
    # Get full content
    content = wp_client.get_page_content(post['link'])
    
    # Validate links
    results = validator.validate_page_links(content, post['link'])
    results['post_title'] = post['title']['rendered']
    results['post_url'] = post['link']
    
    return results


def validate_site_menu(wp_client) -> Dict:
    """Validate site menu structure.
    
    Args:
        wp_client: WordPress client instance
        
    Returns:
        Menu validation results
    """
    validator = LinkValidator(wp_client)
    return validator.validate_menu_structure()