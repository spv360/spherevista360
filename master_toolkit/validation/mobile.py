"""
Mobile Responsiveness Validation Module
=======================================
Comprehensive mobile responsiveness validation for WordPress sites including:
- Viewport configuration validation
- Mobile-friendly content analysis
- Touch target size validation
- Font size and readability checks
- Mobile layout validation
"""

import requests
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class MobileValidator:
    """Mobile responsiveness validation utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize mobile validator."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
        # Mobile-friendly criteria
        self.min_font_size = 12  # pixels
        self.min_touch_target = 44  # pixels (Apple HIG & Material Design)
        self.max_content_width = 100  # viewport width percentage
    
    def validate_mobile_responsiveness(self, post_id: int) -> Dict[str, Any]:
        """Comprehensive mobile responsiveness validation for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            post_url = post.get('link', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'mobile': {
                    'viewport': {'score': 0, 'issues': []},
                    'content': {'score': 0, 'issues': []},
                    'touch_targets': {'score': 0, 'issues': []},
                    'typography': {'score': 0, 'issues': []},
                    'layout': {'score': 0, 'issues': []},
                    'performance': {'score': 0, 'issues': []}
                },
                'issues': [],
                'recommendations': [],
                'score': 0
            }
            
            # Get page content
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
                }
                response = requests.get(post_url, timeout=15, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Run mobile validations
                    result['mobile']['viewport'] = self._validate_viewport_configuration(soup)
                    result['mobile']['content'] = self._validate_mobile_content(soup)
                    result['mobile']['touch_targets'] = self._validate_touch_targets(soup)
                    result['mobile']['typography'] = self._validate_mobile_typography(soup)
                    result['mobile']['layout'] = self._validate_mobile_layout(soup)
                    result['mobile']['performance'] = self._validate_mobile_performance(response)
                    
                else:
                    result['issues'].append(f'Failed to load page (HTTP {response.status_code})')
                    
            except Exception as e:
                result['issues'].append(f'Error loading page: {str(e)}')
            
            # Calculate overall score
            scores = [section['score'] for section in result['mobile'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all issues
            all_issues = []
            for section_name, section_data in result['mobile'].items():
                if section_data['issues']:
                    all_issues.extend([f"{section_name.replace('_', ' ').title()}: {issue}" for issue in section_data['issues']])
            
            result['issues'] = all_issues
            
            # Generate recommendations
            result = self._generate_mobile_recommendations(result)
            
            # Set status based on score
            if result['score'] >= 85:
                result['status'] = 'excellent'
                result['message'] = 'Excellent mobile responsiveness'
            elif result['score'] >= 70:
                result['status'] = 'good'
                result['message'] = 'Good mobile responsiveness'
            elif result['score'] >= 50:
                result['status'] = 'fair'
                result['message'] = 'Fair mobile responsiveness - improvements needed'
            else:
                result['status'] = 'poor'
                result['message'] = 'Poor mobile responsiveness - significant improvements needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error validating mobile responsiveness: {str(e)}'
            }
    
    def _validate_viewport_configuration(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate viewport meta tag configuration."""
        analysis = {
            'viewport_present': False,
            'viewport_content': '',
            'width_device': False,
            'initial_scale': False,
            'user_scalable': True,
            'issues': [],
            'score': 0
        }
        
        # Find viewport meta tag
        viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
        
        if viewport_tag:
            analysis['viewport_present'] = True
            analysis['score'] += 30
            
            content = viewport_tag.get('content', '').lower()
            analysis['viewport_content'] = content
            
            # Check for device width
            if 'width=device-width' in content:
                analysis['width_device'] = True
                analysis['score'] += 25
            else:
                analysis['issues'].append('Viewport should include width=device-width')
            
            # Check initial scale
            if 'initial-scale=1' in content:
                analysis['initial_scale'] = True
                analysis['score'] += 25
            else:
                analysis['issues'].append('Viewport should include initial-scale=1')
            
            # Check user scalability (accessibility consideration)
            if 'user-scalable=no' in content or 'maximum-scale=1' in content:
                analysis['user_scalable'] = False
                analysis['issues'].append('Viewport prevents user scaling - accessibility concern')
                analysis['score'] -= 10
            else:
                analysis['score'] += 20
                
        else:
            analysis['issues'].append('Missing viewport meta tag')
        
        return analysis
    
    def _validate_mobile_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate mobile-friendly content characteristics."""
        analysis = {
            'horizontal_scroll': False,
            'fixed_width_elements': 0,
            'small_content': 0,
            'large_images': 0,
            'mobile_navigation': False,
            'issues': [],
            'score': 100
        }
        
        # Check for fixed width elements that might cause horizontal scrolling
        elements_with_width = soup.find_all(attrs={'style': re.compile(r'width\s*:\s*\d+px')})
        for element in elements_with_width:
            style = element.get('style', '')
            width_match = re.search(r'width\s*:\s*(\d+)px', style)
            if width_match:
                width = int(width_match.group(1))
                if width > 320:  # Larger than smallest mobile viewport
                    analysis['fixed_width_elements'] += 1
        
        if analysis['fixed_width_elements'] > 0:
            analysis['issues'].append(f'Found {analysis["fixed_width_elements"]} elements with fixed width that may cause horizontal scrolling')
            analysis['score'] -= analysis['fixed_width_elements'] * 10
        
        # Check for mobile navigation patterns
        nav_elements = soup.find_all(['nav', 'div'], class_=re.compile(r'(menu|nav|mobile)', re.I))
        hamburger_buttons = soup.find_all(['button', 'div'], class_=re.compile(r'(hamburger|menu-toggle|mobile-menu)', re.I))
        
        if nav_elements or hamburger_buttons:
            analysis['mobile_navigation'] = True
            analysis['score'] += 20
        else:
            analysis['issues'].append('No mobile navigation patterns detected')
        
        # Check for responsive images
        images = soup.find_all('img')
        for img in images:
            # Check for responsive image attributes
            if not any(attr in img.attrs for attr in ['srcset', 'sizes']):
                width = img.get('width')
                if width and width.isdigit() and int(width) > 320:
                    analysis['large_images'] += 1
        
        if analysis['large_images'] > 0:
            analysis['issues'].append(f'Found {analysis["large_images"]} large images without responsive attributes')
            analysis['score'] -= analysis['large_images'] * 5
        
        return analysis
    
    def _validate_touch_targets(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate touch target sizes and spacing."""
        analysis = {
            'total_links': 0,
            'small_touch_targets': 0,
            'close_targets': 0,
            'button_elements': 0,
            'proper_buttons': 0,
            'issues': [],
            'score': 90  # Start with good score, deduct for issues
        }
        
        # Find interactive elements
        interactive_elements = soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
        clickable_divs = soup.find_all('div', attrs={'onclick': True})
        interactive_elements.extend(clickable_divs)
        
        analysis['total_links'] = len(interactive_elements)
        
        if analysis['total_links'] == 0:
            return analysis
        
        # Check button elements specifically
        buttons = soup.find_all(['button', 'input'])
        analysis['button_elements'] = len(buttons)
        
        for button in buttons:
            # Check if button has proper type or role
            btn_type = button.get('type', '')
            btn_role = button.get('role', '')
            if btn_type in ['button', 'submit', 'reset'] or btn_role == 'button':
                analysis['proper_buttons'] += 1
        
        # Estimate touch target issues (simplified analysis)
        # In a real implementation, this would require CSS parsing and layout calculation
        
        # Check for elements that might be too small
        small_elements = soup.find_all(['a', 'button'], string=re.compile(r'^\w{1,2}$'))  # Very short text
        analysis['small_touch_targets'] = len(small_elements)
        
        if analysis['small_touch_targets'] > 0:
            analysis['issues'].append(f'Found {analysis["small_touch_targets"]} potentially small touch targets')
            analysis['score'] -= analysis['small_touch_targets'] * 5
        
        # Check for proper button usage
        if analysis['button_elements'] > 0:
            button_ratio = analysis['proper_buttons'] / analysis['button_elements']
            if button_ratio < 0.8:
                analysis['issues'].append('Some interactive elements should use proper button elements')
                analysis['score'] -= 10
        
        return analysis
    
    def _validate_mobile_typography(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate typography for mobile readability."""
        analysis = {
            'readable_font_size': True,
            'relative_units': False,
            'line_height': False,
            'text_blocks': 0,
            'long_lines': 0,
            'issues': [],
            'score': 80  # Start with good score
        }
        
        # Check for font-size in inline styles (basic check)
        elements_with_font_size = soup.find_all(attrs={'style': re.compile(r'font-size')})
        small_fonts = 0
        
        for element in elements_with_font_size:
            style = element.get('style', '')
            font_size_match = re.search(r'font-size\s*:\s*(\d+(?:\.\d+)?)px', style)
            if font_size_match:
                font_size = float(font_size_match.group(1))
                if font_size < self.min_font_size:
                    small_fonts += 1
        
        if small_fonts > 0:
            analysis['readable_font_size'] = False
            analysis['issues'].append(f'Found {small_fonts} elements with font size below {self.min_font_size}px')
            analysis['score'] -= small_fonts * 10
        
        # Check for relative units usage
        relative_unit_elements = soup.find_all(attrs={'style': re.compile(r'font-size\s*:\s*\d+(?:\.\d+)?(?:em|rem|%)')})
        if relative_unit_elements:
            analysis['relative_units'] = True
            analysis['score'] += 10
        
        # Check text content blocks
        text_blocks = soup.find_all(['p', 'div', 'article', 'section'])
        analysis['text_blocks'] = len(text_blocks)
        
        # Check for very long text lines (heuristic)
        for block in text_blocks[:10]:  # Check first 10 blocks
            text = block.get_text(strip=True)
            if len(text) > 500:  # Very long text block
                analysis['long_lines'] += 1
        
        if analysis['long_lines'] > 0:
            analysis['issues'].append(f'Found {analysis["long_lines"]} very long text blocks - consider shorter paragraphs')
            analysis['score'] -= analysis['long_lines'] * 5
        
        return analysis
    
    def _validate_mobile_layout(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate mobile-friendly layout patterns."""
        analysis = {
            'responsive_framework': False,
            'grid_system': False,
            'flex_usage': False,
            'media_queries': False,
            'mobile_first': False,
            'issues': [],
            'score': 70  # Default score
        }
        
        # Check for responsive framework classes
        responsive_classes = ['container', 'row', 'col-', 'grid', 'flex', 'mobile', 'responsive']
        all_classes = ' '.join([elem.get('class', []) for elem in soup.find_all(class_=True) if isinstance(elem.get('class'), list)])
        
        for class_pattern in responsive_classes:
            if class_pattern in all_classes.lower():
                if class_pattern in ['container', 'row', 'col-']:
                    analysis['responsive_framework'] = True
                elif class_pattern in ['grid']:
                    analysis['grid_system'] = True
                elif class_pattern in ['flex']:
                    analysis['flex_usage'] = True
        
        # Check CSS for media queries (in style tags)
        style_tags = soup.find_all('style')
        for style_tag in style_tags:
            if style_tag.string:
                if '@media' in style_tag.string:
                    analysis['media_queries'] = True
                    analysis['score'] += 15
                    
                    # Check for mobile-first approach
                    if 'min-width' in style_tag.string:
                        analysis['mobile_first'] = True
                        analysis['score'] += 10
        
        # Score adjustments
        if analysis['responsive_framework']:
            analysis['score'] += 15
        
        if analysis['grid_system'] or analysis['flex_usage']:
            analysis['score'] += 10
        
        if not analysis['media_queries']:
            analysis['issues'].append('No media queries detected - may not be responsive')
        
        return analysis
    
    def _validate_mobile_performance(self, response) -> Dict[str, Any]:
        """Validate mobile-specific performance considerations."""
        analysis = {
            'page_size': 0,
            'compression': False,
            'mobile_optimized': False,
            'amp_version': False,
            'issues': [],
            'score': 80
        }
        
        # Check page size
        content_length = response.headers.get('content-length')
        if content_length:
            analysis['page_size'] = int(content_length)
            size_mb = analysis['page_size'] / (1024 * 1024)
            
            if size_mb > 2:  # Large for mobile
                analysis['issues'].append(f'Large page size ({size_mb:.1f}MB) for mobile connections')
                analysis['score'] -= 20
            elif size_mb > 1:
                analysis['issues'].append(f'Consider optimizing page size ({size_mb:.1f}MB) for mobile')
                analysis['score'] -= 10
        
        # Check compression
        if 'gzip' in response.headers.get('content-encoding', '').lower():
            analysis['compression'] = True
            analysis['score'] += 10
        
        # Check for AMP version
        content = response.text
        if 'amp-' in content.lower() or 'accelerated mobile pages' in content.lower():
            analysis['amp_version'] = True
            analysis['score'] += 10
        
        return analysis
    
    def _generate_mobile_recommendations(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific mobile responsiveness recommendations."""
        recommendations = []
        mobile = result['mobile']
        
        # Viewport recommendations
        if not mobile['viewport']['viewport_present']:
            recommendations.append('Add viewport meta tag for mobile responsiveness')
        elif not mobile['viewport']['width_device']:
            recommendations.append('Set viewport width to device-width')
        elif not mobile['viewport']['initial_scale']:
            recommendations.append('Set initial-scale=1 in viewport meta tag')
        
        # Content recommendations
        if mobile['content']['fixed_width_elements'] > 0:
            recommendations.append('Use responsive units instead of fixed pixel widths')
        
        if mobile['content']['large_images'] > 0:
            recommendations.append('Implement responsive images with srcset and sizes attributes')
        
        if not mobile['content']['mobile_navigation']:
            recommendations.append('Implement mobile-friendly navigation patterns')
        
        # Touch target recommendations
        if mobile['touch_targets']['small_touch_targets'] > 0:
            recommendations.append('Increase touch target sizes to at least 44px')
        
        # Typography recommendations
        if not mobile['typography']['readable_font_size']:
            recommendations.append('Increase font sizes for better mobile readability')
        
        if not mobile['typography']['relative_units']:
            recommendations.append('Use relative units (em, rem, %) for scalable typography')
        
        # Layout recommendations
        if not mobile['layout']['media_queries']:
            recommendations.append('Add CSS media queries for responsive layout')
        
        if not mobile['layout']['mobile_first']:
            recommendations.append('Consider mobile-first responsive design approach')
        
        # Performance recommendations
        if mobile['performance']['page_size'] > 1024 * 1024:  # > 1MB
            recommendations.append('Optimize page size for mobile connections')
        
        if not mobile['performance']['compression']:
            recommendations.append('Enable compression for faster mobile loading')
        
        result['recommendations'] = recommendations
        return result