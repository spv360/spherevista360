"""
Performance Validation Module
============================
Comprehensive performance validation for WordPress sites including:
- Page speed analysis
- Image optimization checks  
- Loading time metrics
- Core Web Vitals assessment
- Resource optimization recommendations
"""

import requests
import time
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
import json
from bs4 import BeautifulSoup
from PIL import Image
import io

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class PerformanceValidator:
    """Performance validation utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize performance validator."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
    def validate_page_speed(self, post_id: int) -> Dict[str, Any]:
        """Analyze page speed and loading performance for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            post_url = post.get('link', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'performance': {
                    'load_time': 0,
                    'page_size': 0,
                    'requests_count': 0,
                    'images_count': 0,
                    'js_files': 0,
                    'css_files': 0
                },
                'core_web_vitals': {
                    'lcp_estimate': 0,  # Largest Contentful Paint
                    'fid_estimate': 0,  # First Input Delay  
                    'cls_estimate': 0   # Cumulative Layout Shift
                },
                'optimizations': {
                    'image_optimization': 0,
                    'compression': False,
                    'caching': False,
                    'minification': False
                },
                'issues': [],
                'recommendations': [],
                'score': 0
            }
            
            # Measure page load time
            start_time = time.time()
            try:
                response = requests.get(post_url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; PerformanceValidator/1.0)'
                })
                load_time = time.time() - start_time
                result['performance']['load_time'] = round(load_time, 2)
                
                if response.status_code == 200:
                    # Analyze page content
                    content = response.text
                    content_size = len(content.encode('utf-8'))
                    result['performance']['page_size'] = content_size
                    
                    # Parse HTML for resource analysis
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Count resources
                    images = soup.find_all('img')
                    js_files = soup.find_all('script', src=True)
                    css_files = soup.find_all('link', rel='stylesheet')
                    
                    result['performance']['images_count'] = len(images)
                    result['performance']['js_files'] = len(js_files)
                    result['performance']['css_files'] = len(css_files)
                    result['performance']['requests_count'] = len(images) + len(js_files) + len(css_files)
                    
                    # Analyze images for optimization
                    image_analysis = self._analyze_images(images, post_url)
                    result['optimizations']['image_optimization'] = image_analysis['optimization_score']
                    
                    # Check for performance optimizations
                    result['optimizations']['compression'] = self._check_compression(response)
                    result['optimizations']['caching'] = self._check_caching(response)
                    result['optimizations']['minification'] = self._check_minification(content)
                    
                    # Estimate Core Web Vitals
                    result['core_web_vitals'] = self._estimate_core_web_vitals(
                        load_time, content_size, len(images)
                    )
                    
                    # Calculate performance score
                    result['score'] = self._calculate_performance_score(result)
                    
                    # Generate recommendations
                    result = self._generate_performance_recommendations(result)
                    
                else:
                    result['issues'].append(f'Failed to load page (HTTP {response.status_code})')
                    
            except requests.exceptions.Timeout:
                result['issues'].append('Page load timeout (>30 seconds)')
                result['performance']['load_time'] = 30
            except Exception as e:
                result['issues'].append(f'Error loading page: {str(e)}')
            
            # Set status based on score
            if result['score'] >= 90:
                result['status'] = 'excellent'
                result['message'] = 'Excellent page performance'
            elif result['score'] >= 75:
                result['status'] = 'good'
                result['message'] = 'Good page performance'
            elif result['score'] >= 60:
                result['status'] = 'fair'
                result['message'] = 'Page performance needs improvement'
            else:
                result['status'] = 'poor'
                result['message'] = 'Poor page performance - optimization needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error validating page speed: {str(e)}'
            }
    
    def _analyze_images(self, images: List, base_url: str) -> Dict[str, Any]:
        """Analyze images for optimization opportunities."""
        analysis = {
            'total_images': len(images),
            'large_images': 0,
            'missing_alt': 0,
            'unoptimized_format': 0,
            'optimization_score': 100
        }
        
        for img in images[:10]:  # Analyze first 10 images to avoid timeout
            # Check alt text
            if not img.get('alt'):
                analysis['missing_alt'] += 1
            
            # Check image size and format
            src = img.get('src')
            if src:
                try:
                    if src.startswith('/'):
                        src = urljoin(base_url, src)
                    
                    # Quick head request to get image info
                    img_response = requests.head(src, timeout=5)
                    content_length = img_response.headers.get('content-length')
                    content_type = img_response.headers.get('content-type', '')
                    
                    if content_length:
                        size_kb = int(content_length) / 1024
                        if size_kb > 500:  # Large image > 500KB
                            analysis['large_images'] += 1
                    
                    # Check format optimization
                    if 'image/jpeg' in content_type or 'image/png' in content_type:
                        # These could potentially be WebP
                        analysis['unoptimized_format'] += 1
                        
                except Exception:
                    continue
        
        # Calculate optimization score
        total_issues = analysis['large_images'] + analysis['missing_alt'] + analysis['unoptimized_format']
        if analysis['total_images'] > 0:
            analysis['optimization_score'] = max(0, 100 - (total_issues * 20))
        
        return analysis
    
    def _check_compression(self, response) -> bool:
        """Check if compression is enabled."""
        return 'gzip' in response.headers.get('content-encoding', '').lower()
    
    def _check_caching(self, response) -> bool:
        """Check if caching headers are present."""
        cache_headers = ['cache-control', 'expires', 'etag', 'last-modified']
        return any(header in response.headers for header in cache_headers)
    
    def _check_minification(self, content: str) -> bool:
        """Basic check for minified content."""
        # Simple heuristic: minified content has fewer line breaks
        lines = content.count('\n')
        chars = len(content)
        if chars > 0:
            line_density = lines / chars
            return line_density < 0.01  # Less than 1% line breaks suggests minification
        return False
    
    def _estimate_core_web_vitals(self, load_time: float, page_size: int, image_count: int) -> Dict[str, float]:
        """Estimate Core Web Vitals based on available metrics."""
        # These are rough estimates based on common correlations
        
        # LCP (Largest Contentful Paint) - correlates with load time
        lcp_estimate = min(load_time * 1.2, 10.0)  # Usually 20% longer than total load
        
        # FID (First Input Delay) - estimate based on page complexity
        complexity_factor = min((page_size / 100000) + (image_count / 10), 5.0)
        fid_estimate = complexity_factor * 20  # ms
        
        # CLS (Cumulative Layout Shift) - estimate based on image count
        cls_estimate = min(image_count * 0.02, 0.5)  # Images without dimensions cause shifts
        
        return {
            'lcp_estimate': round(lcp_estimate, 2),
            'fid_estimate': round(fid_estimate, 2),
            'cls_estimate': round(cls_estimate, 3)
        }
    
    def _calculate_performance_score(self, result: Dict[str, Any]) -> int:
        """Calculate overall performance score."""
        score = 100
        
        # Load time scoring
        load_time = result['performance']['load_time']
        if load_time > 3:
            score -= 30
        elif load_time > 2:
            score -= 20
        elif load_time > 1:
            score -= 10
        
        # Page size scoring
        page_size_mb = result['performance']['page_size'] / (1024 * 1024)
        if page_size_mb > 5:
            score -= 20
        elif page_size_mb > 3:
            score -= 15
        elif page_size_mb > 2:
            score -= 10
        
        # Requests count scoring
        requests = result['performance']['requests_count']
        if requests > 100:
            score -= 15
        elif requests > 50:
            score -= 10
        elif requests > 30:
            score -= 5
        
        # Image optimization scoring
        image_score = result['optimizations']['image_optimization']
        score += (image_score - 100) * 0.2  # Adjust by 20% of image score difference
        
        # Optimization bonuses
        if result['optimizations']['compression']:
            score += 5
        if result['optimizations']['caching']:
            score += 5
        if result['optimizations']['minification']:
            score += 3
        
        # Core Web Vitals penalties
        cwv = result['core_web_vitals']
        if cwv['lcp_estimate'] > 4:
            score -= 15
        elif cwv['lcp_estimate'] > 2.5:
            score -= 10
        
        if cwv['fid_estimate'] > 300:
            score -= 10
        elif cwv['fid_estimate'] > 100:
            score -= 5
        
        if cwv['cls_estimate'] > 0.25:
            score -= 10
        elif cwv['cls_estimate'] > 0.1:
            score -= 5
        
        return max(0, min(100, int(score)))
    
    def _generate_performance_recommendations(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific performance recommendations."""
        recommendations = []
        
        # Load time recommendations
        load_time = result['performance']['load_time']
        if load_time > 3:
            recommendations.append('Page load time is slow (>3s) - optimize images and reduce server response time')
        elif load_time > 2:
            recommendations.append('Consider optimizing page load time - current: {:.1f}s'.format(load_time))
        
        # Page size recommendations
        page_size_mb = result['performance']['page_size'] / (1024 * 1024)
        if page_size_mb > 3:
            recommendations.append('Page size is large ({:.1f}MB) - compress images and minify resources'.format(page_size_mb))
        
        # Image optimization recommendations
        if result['optimizations']['image_optimization'] < 80:
            recommendations.append('Images need optimization - compress large images and add missing alt text')
        
        # Compression recommendations
        if not result['optimizations']['compression']:
            recommendations.append('Enable GZIP compression to reduce page size')
        
        # Caching recommendations
        if not result['optimizations']['caching']:
            recommendations.append('Implement browser caching with proper cache headers')
        
        # Minification recommendations
        if not result['optimizations']['minification']:
            recommendations.append('Minify CSS and JavaScript files to reduce page size')
        
        # Core Web Vitals recommendations
        cwv = result['core_web_vitals']
        if cwv['lcp_estimate'] > 2.5:
            recommendations.append('Improve Largest Contentful Paint (LCP) - optimize images and server response')
        
        if cwv['fid_estimate'] > 100:
            recommendations.append('Reduce First Input Delay (FID) - optimize JavaScript execution')
        
        if cwv['cls_estimate'] > 0.1:
            recommendations.append('Improve Cumulative Layout Shift (CLS) - add dimensions to images')
        
        result['recommendations'] = recommendations
        return result
    
    def validate_image_optimization(self, post_id: int) -> Dict[str, Any]:
        """Detailed image optimization analysis for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            content = post.get('content', {}).get('rendered', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'image_analysis': {
                    'total_images': 0,
                    'optimized_images': 0,
                    'large_images': [],
                    'missing_alt_text': [],
                    'format_recommendations': []
                },
                'issues': [],
                'recommendations': [],
                'score': 100
            }
            
            if not content:
                result['issues'].append('No content to analyze')
                return result
            
            # Parse content for images
            soup = BeautifulSoup(content, 'html.parser')
            images = soup.find_all('img')
            result['image_analysis']['total_images'] = len(images)
            
            if len(images) == 0:
                result['message'] = 'No images found in post content'
                return result
            
            optimized_count = 0
            
            for img in images:
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                # Check alt text
                if not alt.strip():
                    result['image_analysis']['missing_alt_text'].append(src)
                
                # Analyze image if accessible
                if src:
                    try:
                        if src.startswith('/'):
                            full_url = urljoin(self.base_url, src)
                        else:
                            full_url = src
                        
                        # Get image metadata
                        img_response = requests.head(full_url, timeout=10)
                        
                        if img_response.status_code == 200:
                            content_length = img_response.headers.get('content-length')
                            content_type = img_response.headers.get('content-type', '')
                            
                            is_optimized = True
                            
                            # Check file size
                            if content_length:
                                size_kb = int(content_length) / 1024
                                if size_kb > 500:  # Large image
                                    result['image_analysis']['large_images'].append({
                                        'src': src,
                                        'size_kb': round(size_kb, 1)
                                    })
                                    is_optimized = False
                            
                            # Check format
                            if 'image/jpeg' in content_type or 'image/png' in content_type:
                                result['image_analysis']['format_recommendations'].append({
                                    'src': src,
                                    'current_format': content_type,
                                    'recommended': 'WebP or AVIF for better compression'
                                })
                                is_optimized = False
                            
                            if is_optimized and alt.strip():
                                optimized_count += 1
                                
                    except Exception:
                        continue
            
            result['image_analysis']['optimized_images'] = optimized_count
            
            # Calculate score
            if result['image_analysis']['total_images'] > 0:
                optimization_ratio = optimized_count / result['image_analysis']['total_images']
                result['score'] = int(optimization_ratio * 100)
            
            # Generate recommendations
            if result['image_analysis']['missing_alt_text']:
                result['recommendations'].append(f"Add alt text to {len(result['image_analysis']['missing_alt_text'])} images")
            
            if result['image_analysis']['large_images']:
                result['recommendations'].append(f"Optimize {len(result['image_analysis']['large_images'])} large images (>500KB)")
            
            if result['image_analysis']['format_recommendations']:
                result['recommendations'].append(f"Consider modern formats (WebP/AVIF) for {len(result['image_analysis']['format_recommendations'])} images")
            
            # Set status
            if result['score'] >= 90:
                result['status'] = 'excellent'
                result['message'] = 'Images are well optimized'
            elif result['score'] >= 70:
                result['status'] = 'good'
                result['message'] = 'Most images are optimized'
            elif result['score'] >= 50:
                result['status'] = 'fair'
                result['message'] = 'Images need optimization'
            else:
                result['status'] = 'poor'
                result['message'] = 'Significant image optimization needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error validating image optimization: {str(e)}'
            }