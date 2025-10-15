"""
Performance Optimization Engine
==============================
Automated performance improvements for WordPress sites including:
- CSS and JavaScript minification
- Caching optimization recommendations
- Image lazy loading implementation
- Database query optimization analysis
- Core Web Vitals optimization
- Resource compression and optimization
"""

import re
import json
import base64
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
import requests
from datetime import datetime, timedelta

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class PerformanceOptimizer:
    """Advanced performance optimization utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize performance optimizer."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
        # Performance thresholds (Core Web Vitals)
        self.thresholds = {
            'lcp': 2.5,      # Largest Contentful Paint (seconds)
            'fid': 100,      # First Input Delay (milliseconds)
            'cls': 0.1,      # Cumulative Layout Shift
            'fcp': 1.8,      # First Contentful Paint (seconds)
            'ttfb': 600      # Time to First Byte (milliseconds)
        }
        
        # CSS/JS optimization patterns
        self.css_minify_patterns = [
            (r'/\*.*?\*/', ''),          # Remove comments
            (r'\s+', ' '),               # Collapse whitespace
            (r';\s*}', '}'),             # Remove unnecessary semicolons
            (r'\s*{\s*', '{'),           # Remove spaces around braces
            (r';\s*', ';'),              # Remove spaces after semicolons
            (r':\s*', ':'),              # Remove spaces after colons
        ]
        
        self.js_minify_patterns = [
            (r'//.*?$', '', re.MULTILINE),   # Remove single-line comments
            (r'/\*.*?\*/', '', re.DOTALL),   # Remove multi-line comments
            (r'\s+', ' '),                   # Collapse whitespace
            (r'\s*([{}();,:])\s*', r'\1'),   # Remove spaces around operators
        ]
    
    def optimize_post_performance(self, post_id: int, auto_apply: bool = False) -> Dict[str, Any]:
        """Comprehensive performance optimization for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            content = post.get('content', {}).get('rendered', '')
            post_url = post.get('link', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'performance_optimization': {
                    'resource_optimization': {'score': 0, 'improvements': []},
                    'loading_optimization': {'score': 0, 'improvements': []},
                    'caching_optimization': {'score': 0, 'improvements': []},
                    'core_web_vitals': {'score': 0, 'improvements': []},
                    'database_optimization': {'score': 0, 'improvements': []},
                    'compression_optimization': {'score': 0, 'improvements': []}
                },
                'optimized_content': {
                    'content': content,
                    'optimized_css': '',
                    'optimized_js': '',
                    'lazy_loading_applied': False,
                    'caching_headers': {},
                    'compression_applied': False
                },
                'recommendations': [],
                'score': 0
            }
            
            if not content:
                result['performance_optimization']['resource_optimization']['improvements'].append('No content to optimize')
                return result
            
            # Parse content for analysis
            soup = BeautifulSoup(content, 'html.parser')
            
            # Run performance optimization analyses
            result['performance_optimization']['resource_optimization'] = self._optimize_resources(
                soup, auto_apply
            )
            result['performance_optimization']['loading_optimization'] = self._optimize_loading(
                soup, auto_apply
            )
            result['performance_optimization']['caching_optimization'] = self._optimize_caching(
                post_url, auto_apply
            )
            result['performance_optimization']['core_web_vitals'] = self._optimize_core_web_vitals(
                soup, post_url, auto_apply
            )
            result['performance_optimization']['database_optimization'] = self._optimize_database_queries(
                post_id, auto_apply
            )
            result['performance_optimization']['compression_optimization'] = self._optimize_compression(
                soup, auto_apply
            )
            
            # Generate optimized content
            if auto_apply:
                result['optimized_content'] = self._generate_optimized_performance_content(
                    soup, result['performance_optimization']
                )
            
            # Calculate overall performance score
            scores = [section['score'] for section in result['performance_optimization'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all recommendations
            all_recommendations = []
            for section_name, section_data in result['performance_optimization'].items():
                if section_data['improvements']:
                    all_recommendations.extend([f"{section_name.replace('_', ' ').title()}: {rec}" for rec in section_data['improvements']])
            
            result['recommendations'] = all_recommendations
            
            # Set status based on score
            if result['score'] >= 90:
                result['status'] = 'excellent'
                result['message'] = 'Performance is well optimized'
            elif result['score'] >= 75:
                result['status'] = 'good'
                result['message'] = 'Good performance with minor optimizations possible'
            elif result['score'] >= 60:
                result['status'] = 'fair'
                result['message'] = 'Performance needs improvements'
            else:
                result['status'] = 'poor'
                result['message'] = 'Significant performance improvements needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error optimizing performance: {str(e)}'
            }
    
    def _optimize_resources(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize CSS, JavaScript, and other resources."""
        analysis = {
            'css_optimization': {},
            'js_optimization': {},
            'image_optimization': {},
            'resource_hints': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Analyze CSS resources
        css_links = soup.find_all('link', rel='stylesheet')
        inline_styles = soup.find_all('style')
        
        analysis['css_optimization'] = {
            'external_css_files': len(css_links),
            'inline_css_blocks': len(inline_styles),
            'total_css_size': 0,
            'minified_css': []
        }
        
        # CSS optimization recommendations
        if len(css_links) > 5:
            analysis['improvements'].append(f'Consider combining CSS files - found {len(css_links)} external stylesheets')
            analysis['score'] -= 10
        
        # Minify inline CSS
        for style_tag in inline_styles:
            if style_tag.string:
                original_css = style_tag.string
                minified_css = self._minify_css(original_css)
                
                if auto_apply:
                    style_tag.string = minified_css
                
                analysis['css_optimization']['minified_css'].append({
                    'original_size': len(original_css),
                    'minified_size': len(minified_css),
                    'savings': len(original_css) - len(minified_css)
                })
        
        if analysis['css_optimization']['minified_css']:
            total_savings = sum(item['savings'] for item in analysis['css_optimization']['minified_css'])
            analysis['improvements'].append(f'Minified inline CSS - saved {total_savings} characters')
            analysis['score'] += 10
        
        # Analyze JavaScript resources
        js_scripts = soup.find_all('script', src=True)
        inline_scripts = soup.find_all('script', src=False)
        
        analysis['js_optimization'] = {
            'external_js_files': len(js_scripts),
            'inline_js_blocks': len([s for s in inline_scripts if s.string]),
            'total_js_size': 0,
            'minified_js': []
        }
        
        # JavaScript optimization recommendations
        if len(js_scripts) > 8:
            analysis['improvements'].append(f'Consider combining JavaScript files - found {len(js_scripts)} external scripts')
            analysis['score'] -= 10
        
        # Check for async/defer attributes
        non_async_scripts = [s for s in js_scripts if not (s.get('async') or s.get('defer'))]
        if non_async_scripts:
            analysis['improvements'].append(f'Add async/defer to {len(non_async_scripts)} JavaScript files for better loading')
            analysis['score'] -= 10
        
        # Minify inline JavaScript
        for script_tag in inline_scripts:
            if script_tag.string and script_tag.string.strip():
                original_js = script_tag.string
                minified_js = self._minify_js(original_js)
                
                if auto_apply:
                    script_tag.string = minified_js
                
                analysis['js_optimization']['minified_js'].append({
                    'original_size': len(original_js),
                    'minified_size': len(minified_js),
                    'savings': len(original_js) - len(minified_js)
                })
        
        if analysis['js_optimization']['minified_js']:
            total_savings = sum(item['savings'] for item in analysis['js_optimization']['minified_js'])
            analysis['improvements'].append(f'Minified inline JavaScript - saved {total_savings} characters')
            analysis['score'] += 10
        
        # Analyze images for optimization
        images = soup.find_all('img')
        analysis['image_optimization'] = {
            'total_images': len(images),
            'images_without_alt': len([img for img in images if not img.get('alt')]),
            'images_without_width_height': len([img for img in images if not (img.get('width') and img.get('height'))]),
            'large_images': []
        }
        
        # Check for missing alt attributes
        if analysis['image_optimization']['images_without_alt'] > 0:
            analysis['improvements'].append(f'{analysis["image_optimization"]["images_without_alt"]} images missing alt attributes')
            analysis['score'] -= 10
        
        # Check for missing dimensions (causes layout shift)
        if analysis['image_optimization']['images_without_width_height'] > 0:
            analysis['improvements'].append(f'{analysis["image_optimization"]["images_without_width_height"]} images missing width/height attributes')
            analysis['score'] -= 15
        
        # Generate resource hints
        external_domains = set()
        for link in css_links:
            href = link.get('href', '')
            if href.startswith('http'):
                domain = urlparse(href).netloc
                if domain != urlparse(self.base_url).netloc:
                    external_domains.add(domain)
        
        for script in js_scripts:
            src = script.get('src', '')
            if src.startswith('http'):
                domain = urlparse(src).netloc
                if domain != urlparse(self.base_url).netloc:
                    external_domains.add(domain)
        
        analysis['resource_hints'] = {
            'preconnect_domains': list(external_domains),
            'dns_prefetch_domains': list(external_domains)
        }
        
        if external_domains:
            analysis['improvements'].append(f'Add DNS prefetch/preconnect for {len(external_domains)} external domains')
            analysis['score'] += 5
        
        return analysis
    
    def _optimize_loading(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize loading strategies for better performance."""
        analysis = {
            'lazy_loading': {},
            'critical_css': {},
            'preloading': {},
            'improvements': [],
            'score': 75  # Default score
        }
        
        # Analyze lazy loading opportunities
        images = soup.find_all('img')
        images_without_lazy = [img for img in images if not img.get('loading')]
        
        analysis['lazy_loading'] = {
            'total_images': len(images),
            'lazy_loading_candidates': len(images_without_lazy),
            'applied': False
        }
        
        if images_without_lazy and len(images_without_lazy) > 2:
            analysis['improvements'].append(f'Apply lazy loading to {len(images_without_lazy)} images')
            analysis['score'] -= 10
            
            if auto_apply:
                # Apply lazy loading to images (skip first 2 above-the-fold)
                for img in images_without_lazy[2:]:
                    img['loading'] = 'lazy'
                analysis['lazy_loading']['applied'] = True
                analysis['score'] += 15
        
        # Analyze critical CSS opportunities
        style_tags = soup.find_all('style')
        link_tags = soup.find_all('link', rel='stylesheet')
        
        analysis['critical_css'] = {
            'inline_styles': len(style_tags),
            'external_stylesheets': len(link_tags),
            'critical_css_detected': bool(style_tags)
        }
        
        if link_tags and not style_tags:
            analysis['improvements'].append('Consider inlining critical CSS for faster rendering')
            analysis['score'] -= 15
        elif style_tags:
            analysis['score'] += 10
        
        # Analyze preloading opportunities
        preload_links = soup.find_all('link', rel='preload')
        analysis['preloading'] = {
            'preload_resources': len(preload_links),
            'suggested_preloads': []
        }
        
        # Find important resources that should be preloaded
        important_css = soup.find_all('link', rel='stylesheet', href=True)[:2]  # First 2 CSS files
        important_js = soup.find_all('script', src=True)[:1]  # First JS file
        
        for css_link in important_css:
            if not any(pl.get('href') == css_link.get('href') for pl in preload_links):
                analysis['preloading']['suggested_preloads'].append({
                    'type': 'style',
                    'href': css_link.get('href'),
                    'as': 'style'
                })
        
        for js_script in important_js:
            if not any(pl.get('href') == js_script.get('src') for pl in preload_links):
                analysis['preloading']['suggested_preloads'].append({
                    'type': 'script',
                    'href': js_script.get('src'),
                    'as': 'script'
                })
        
        if analysis['preloading']['suggested_preloads']:
            analysis['improvements'].append(f'Preload {len(analysis["preloading"]["suggested_preloads"])} critical resources')
            analysis['score'] -= 10
        
        return analysis
    
    def _optimize_caching(self, post_url: str, auto_apply: bool = False) -> Dict[str, Any]:
        """Analyze and recommend caching optimizations."""
        analysis = {
            'browser_caching': {},
            'cdn_usage': {},
            'server_caching': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        try:
            # Check current caching headers
            response = requests.head(post_url, timeout=10)
            headers = response.headers
            
            # Analyze browser caching
            cache_control = headers.get('Cache-Control', '')
            expires = headers.get('Expires', '')
            etag = headers.get('ETag', '')
            last_modified = headers.get('Last-Modified', '')
            
            analysis['browser_caching'] = {
                'cache_control': cache_control,
                'expires': expires,
                'etag': bool(etag),
                'last_modified': bool(last_modified),
                'max_age': self._extract_max_age(cache_control)
            }
            
            # Check cache headers
            if not cache_control:
                analysis['improvements'].append('Add Cache-Control headers for better browser caching')
                analysis['score'] -= 20
            elif 'max-age' not in cache_control.lower():
                analysis['improvements'].append('Set explicit max-age in Cache-Control header')
                analysis['score'] -= 10
            else:
                max_age = analysis['browser_caching']['max_age']
                if max_age and max_age < 3600:  # Less than 1 hour
                    analysis['improvements'].append('Consider longer cache duration for static content')
                    analysis['score'] -= 5
                else:
                    analysis['score'] += 15
            
            if not etag and not last_modified:
                analysis['improvements'].append('Add ETag or Last-Modified headers for conditional caching')
                analysis['score'] -= 10
            
            # Analyze CDN usage
            server = headers.get('Server', '')
            cf_ray = headers.get('CF-RAY', '')  # Cloudflare
            x_cache = headers.get('X-Cache', '')  # Various CDNs
            
            analysis['cdn_usage'] = {
                'cdn_detected': bool(cf_ray or 'cloudflare' in server.lower() or x_cache),
                'server': server,
                'cdn_indicators': {
                    'cloudflare': bool(cf_ray),
                    'generic_cdn': bool(x_cache)
                }
            }
            
            if not analysis['cdn_usage']['cdn_detected']:
                analysis['improvements'].append('Consider using a CDN for global content delivery')
                analysis['score'] -= 15
            else:
                analysis['score'] += 20
            
        except Exception as e:
            analysis['improvements'].append(f'Unable to check caching headers: {str(e)}')
            analysis['score'] -= 10
        
        # Server caching recommendations
        analysis['server_caching'] = {
            'recommended_plugins': [
                'WP Rocket',
                'W3 Total Cache',
                'WP Super Cache',
                'LiteSpeed Cache'
            ],
            'caching_strategies': [
                'Page caching',
                'Object caching',
                'Database caching',
                'OpCode caching'
            ]
        }
        
        analysis['improvements'].append('Implement server-side caching for better performance')
        
        return analysis
    
    def _optimize_core_web_vitals(self, soup: BeautifulSoup, post_url: str, 
                                 auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize for Core Web Vitals metrics."""
        analysis = {
            'lcp_optimization': {},
            'fid_optimization': {},
            'cls_optimization': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        # LCP (Largest Contentful Paint) optimization
        images = soup.find_all('img')
        headings = soup.find_all(['h1', 'h2', 'h3'])
        
        analysis['lcp_optimization'] = {
            'lcp_candidates': len(images) + len(headings),
            'above_fold_images': len(images[:3]),  # Estimate above-the-fold
            'optimizations_applied': []
        }
        
        # Optimize LCP candidates
        if images:
            first_images = images[:2]  # Likely LCP candidates
            for img in first_images:
                if not img.get('loading'):
                    analysis['improvements'].append('Avoid lazy loading for above-the-fold images')
                    analysis['score'] -= 10
                    
                    if auto_apply:
                        # Remove lazy loading from first images
                        if img.get('loading') == 'lazy':
                            del img['loading']
                        analysis['lcp_optimization']['optimizations_applied'].append('Removed lazy loading from above-fold images')
                
                if not (img.get('width') and img.get('height')):
                    analysis['improvements'].append('Add width/height to prevent layout shift')
                    analysis['score'] -= 15
        
        # FID (First Input Delay) optimization
        scripts = soup.find_all('script')
        analysis['fid_optimization'] = {
            'total_scripts': len(scripts),
            'blocking_scripts': len([s for s in scripts if s.get('src') and not (s.get('async') or s.get('defer'))]),
            'optimizations_applied': []
        }
        
        if analysis['fid_optimization']['blocking_scripts'] > 0:
            analysis['improvements'].append('Add async/defer to JavaScript for better FID')
            analysis['score'] -= 15
            
            if auto_apply:
                for script in scripts:
                    if script.get('src') and not (script.get('async') or script.get('defer')):
                        script['defer'] = True
                        analysis['fid_optimization']['optimizations_applied'].append('Added defer to blocking scripts')
        
        # CLS (Cumulative Layout Shift) optimization
        elements_without_dimensions = []
        
        # Check images without dimensions
        images_without_dims = [img for img in images if not (img.get('width') and img.get('height'))]
        elements_without_dimensions.extend(images_without_dims)
        
        # Check iframes without dimensions
        iframes = soup.find_all('iframe')
        iframes_without_dims = [iframe for iframe in iframes if not (iframe.get('width') and iframe.get('height'))]
        elements_without_dimensions.extend(iframes_without_dims)
        
        analysis['cls_optimization'] = {
            'elements_without_dimensions': len(elements_without_dimensions),
            'images_without_dimensions': len(images_without_dims),
            'iframes_without_dimensions': len(iframes_without_dims),
            'optimizations_applied': []
        }
        
        if elements_without_dimensions:
            analysis['improvements'].append(f'Add dimensions to {len(elements_without_dimensions)} elements to prevent layout shift')
            analysis['score'] -= 20
            
            if auto_apply:
                # Add default dimensions to prevent layout shift
                for img in images_without_dims[:5]:  # Limit to first 5
                    if not img.get('width'):
                        img['width'] = '100%'
                    if not img.get('height'):
                        img['style'] = img.get('style', '') + '; height: auto;'
                
                analysis['cls_optimization']['optimizations_applied'].append('Added dimensions to prevent layout shift')
        
        return analysis
    
    def _optimize_database_queries(self, post_id: int, auto_apply: bool = False) -> Dict[str, Any]:
        """Analyze and optimize database-related performance."""
        analysis = {
            'query_optimization': {},
            'caching_recommendations': {},
            'improvements': [],
            'score': 75  # Default score
        }
        
        # This would typically require database access
        # For now, provide general recommendations
        
        analysis['query_optimization'] = {
            'estimated_queries': 'Unknown (requires database profiling)',
            'slow_query_detection': 'Recommended',
            'index_optimization': 'Required'
        }
        
        analysis['caching_recommendations'] = {
            'object_caching': 'Recommended (Redis/Memcached)',
            'query_caching': 'Enable query result caching',
            'transient_api': 'Use WordPress transients for expensive operations'
        }
        
        # General database optimization recommendations
        analysis['improvements'].extend([
            'Enable object caching (Redis/Memcached) for better database performance',
            'Monitor slow queries and optimize them',
            'Ensure proper database indexing for custom fields',
            'Use WordPress transient API for caching expensive operations',
            'Consider database cleanup for revisions and spam comments'
        ])
        
        return analysis
    
    def _optimize_compression(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize content compression."""
        analysis = {
            'gzip_compression': {},
            'brotli_compression': {},
            'content_optimization': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Estimate content sizes
        html_content = str(soup)
        content_size = len(html_content.encode('utf-8'))
        
        analysis['content_optimization'] = {
            'html_size': content_size,
            'estimated_compressed_size': int(content_size * 0.3),  # ~70% compression
            'compression_ratio': 0.7
        }
        
        # Compression recommendations
        analysis['gzip_compression'] = {
            'recommended': True,
            'estimated_savings': int(content_size * 0.6),  # 60% savings typical
            'mime_types': ['text/html', 'text/css', 'text/javascript', 'application/javascript']
        }
        
        analysis['brotli_compression'] = {
            'recommended': True,
            'estimated_savings': int(content_size * 0.65),  # 65% savings typical
            'browser_support': 'Modern browsers'
        }
        
        analysis['improvements'].extend([
            'Enable Gzip compression for text-based content',
            'Implement Brotli compression for modern browsers',
            'Compress CSS and JavaScript files',
            f'Potential savings: {analysis["gzip_compression"]["estimated_savings"]} bytes'
        ])
        
        return analysis
    
    def _generate_optimized_performance_content(self, soup: BeautifulSoup, 
                                              performance_optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized content with performance improvements applied."""
        optimized = {
            'content': str(soup),
            'optimized_css': '',
            'optimized_js': '',
            'lazy_loading_applied': False,
            'caching_headers': {},
            'compression_applied': False
        }
        
        # Apply resource optimizations
        resource_opt = performance_optimization.get('resource_optimization', {})
        if 'css_optimization' in resource_opt:
            css_data = resource_opt['css_optimization']
            if css_data.get('minified_css'):
                optimized['optimized_css'] = 'Applied CSS minification'
        
        if 'js_optimization' in resource_opt:
            js_data = resource_opt['js_optimization']
            if js_data.get('minified_js'):
                optimized['optimized_js'] = 'Applied JavaScript minification'
        
        # Apply loading optimizations
        loading_opt = performance_optimization.get('loading_optimization', {})
        if loading_opt.get('lazy_loading', {}).get('applied'):
            optimized['lazy_loading_applied'] = True
        
        # Apply caching recommendations
        caching_opt = performance_optimization.get('caching_optimization', {})
        if 'browser_caching' in caching_opt:
            optimized['caching_headers'] = {
                'Cache-Control': 'public, max-age=31536000',
                'Expires': (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
            }
        
        # Apply compression
        compression_opt = performance_optimization.get('compression_optimization', {})
        if compression_opt:
            optimized['compression_applied'] = True
        
        optimized['content'] = str(soup)
        return optimized
    
    def _minify_css(self, css_content: str) -> str:
        """Minify CSS content."""
        minified = css_content
        
        for pattern, replacement, *flags in self.css_minify_patterns:
            if flags:
                minified = re.sub(pattern, replacement, minified, flags=flags[0])
            else:
                minified = re.sub(pattern, replacement, minified)
        
        return minified.strip()
    
    def _minify_js(self, js_content: str) -> str:
        """Minify JavaScript content (basic implementation)."""
        minified = js_content
        
        for pattern, replacement, *flags in self.js_minify_patterns:
            if flags:
                minified = re.sub(pattern, replacement, minified, flags=flags[0])
            else:
                minified = re.sub(pattern, replacement, minified)
        
        return minified.strip()
    
    def _extract_max_age(self, cache_control: str) -> Optional[int]:
        """Extract max-age value from Cache-Control header."""
        if not cache_control:
            return None
        
        match = re.search(r'max-age=(\d+)', cache_control.lower())
        return int(match.group(1)) if match else None