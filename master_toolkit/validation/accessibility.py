"""
Accessibility Validation Module
==============================
Comprehensive accessibility validation for WordPress sites including:
- ARIA labels and attributes validation
- Alt text and image accessibility
- Heading structure analysis
- Color contrast assessment
- Keyboard navigation support
- Screen reader compatibility
"""

import requests
import re
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag
import colorsys

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class AccessibilityValidator:
    """Accessibility validation utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize accessibility validator."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
        # WCAG 2.1 compliance levels
        self.wcag_levels = {
            'A': {'contrast_ratio': 3.0, 'large_text_ratio': 3.0},
            'AA': {'contrast_ratio': 4.5, 'large_text_ratio': 3.0},
            'AAA': {'contrast_ratio': 7.0, 'large_text_ratio': 4.5}
        }
        
    def validate_accessibility(self, post_id: int, wcag_level: str = 'AA') -> Dict[str, Any]:
        """Comprehensive accessibility validation for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            post_url = post.get('link', '')
            content = post.get('content', {}).get('rendered', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'wcag_level': wcag_level,
                'accessibility': {
                    'images': {'score': 0, 'issues': []},
                    'headings': {'score': 0, 'issues': []},
                    'links': {'score': 0, 'issues': []},
                    'forms': {'score': 0, 'issues': []},
                    'aria': {'score': 0, 'issues': []},
                    'color_contrast': {'score': 0, 'issues': []}
                },
                'issues': [],
                'recommendations': [],
                'score': 0
            }
            
            if not content:
                result['issues'].append('No content to analyze')
                return result
            
            # Get full page content for comprehensive analysis
            try:
                response = requests.get(post_url, timeout=15)
                if response.status_code == 200:
                    full_content = response.text
                    soup = BeautifulSoup(full_content, 'html.parser')
                else:
                    # Fallback to post content only
                    soup = BeautifulSoup(content, 'html.parser')
            except Exception:
                soup = BeautifulSoup(content, 'html.parser')
            
            # Run accessibility checks
            result['accessibility']['images'] = self._validate_image_accessibility(soup)
            result['accessibility']['headings'] = self._validate_heading_structure(soup)
            result['accessibility']['links'] = self._validate_link_accessibility(soup)
            result['accessibility']['forms'] = self._validate_form_accessibility(soup)
            result['accessibility']['aria'] = self._validate_aria_attributes(soup)
            result['accessibility']['color_contrast'] = self._validate_color_contrast(soup, wcag_level)
            
            # Calculate overall score
            scores = [section['score'] for section in result['accessibility'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all issues and recommendations
            all_issues = []
            all_recommendations = []
            
            for section_name, section_data in result['accessibility'].items():
                if section_data['issues']:
                    all_issues.extend([f"{section_name.title()}: {issue}" for issue in section_data['issues']])
                    
            result['issues'] = all_issues
            
            # Generate recommendations based on issues
            result = self._generate_accessibility_recommendations(result)
            
            # Set status based on score
            if result['score'] >= 90:
                result['status'] = 'excellent'
                result['message'] = f'Excellent WCAG {wcag_level} compliance'
            elif result['score'] >= 75:
                result['status'] = 'good'
                result['message'] = f'Good WCAG {wcag_level} compliance'
            elif result['score'] >= 60:
                result['status'] = 'fair'
                result['message'] = f'Fair accessibility - improvements needed for WCAG {wcag_level}'
            else:
                result['status'] = 'poor'
                result['message'] = f'Poor accessibility - significant improvements needed for WCAG {wcag_level}'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error validating accessibility: {str(e)}'
            }
    
    def _validate_image_accessibility(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate image accessibility including alt text and descriptions."""
        images = soup.find_all('img')
        
        analysis = {
            'total_images': len(images),
            'missing_alt': 0,
            'empty_alt': 0,
            'descriptive_alt': 0,
            'decorative_images': 0,
            'issues': [],
            'score': 100
        }
        
        if len(images) == 0:
            return analysis
        
        for img in images:
            alt_text = img.get('alt', None)
            src = img.get('src', '')
            
            if alt_text is None:
                analysis['missing_alt'] += 1
                analysis['issues'].append(f'Image missing alt attribute: {src[:50]}...')
            elif alt_text.strip() == '':
                # Empty alt is acceptable for decorative images
                analysis['decorative_images'] += 1
            else:
                # Check if alt text is descriptive
                if len(alt_text.strip()) > 5 and not self._is_generic_alt_text(alt_text):
                    analysis['descriptive_alt'] += 1
                else:
                    analysis['empty_alt'] += 1
                    analysis['issues'].append(f'Non-descriptive alt text: "{alt_text}" for {src[:50]}...')
        
        # Calculate score
        good_images = analysis['descriptive_alt'] + analysis['decorative_images']
        if analysis['total_images'] > 0:
            analysis['score'] = int((good_images / analysis['total_images']) * 100)
        
        return analysis
    
    def _is_generic_alt_text(self, alt_text: str) -> bool:
        """Check if alt text is generic/non-descriptive."""
        generic_patterns = [
            r'^image\d*$', r'^photo\d*$', r'^picture\d*$', r'^img\d*$',
            r'^untitled', r'^dsc\d+', r'^img_\d+', r'^photo_\d+'
        ]
        
        alt_lower = alt_text.lower().strip()
        return any(re.match(pattern, alt_lower) for pattern in generic_patterns)
    
    def _validate_heading_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate heading hierarchy and structure."""
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        analysis = {
            'total_headings': len(headings),
            'heading_levels': {},
            'hierarchy_issues': [],
            'empty_headings': 0,
            'issues': [],
            'score': 100
        }
        
        if len(headings) == 0:
            analysis['issues'].append('No headings found - add heading structure for better accessibility')
            analysis['score'] = 50
            return analysis
        
        previous_level = 0
        h1_count = 0
        
        for heading in headings:
            level = int(heading.name[1])
            text = heading.get_text(strip=True)
            
            # Count heading levels
            analysis['heading_levels'][f'h{level}'] = analysis['heading_levels'].get(f'h{level}', 0) + 1
            
            # Check for empty headings
            if not text:
                analysis['empty_headings'] += 1
                analysis['issues'].append(f'Empty {heading.name.upper()} heading found')
            
            # Count H1 tags
            if level == 1:
                h1_count += 1
            
            # Check hierarchy
            if previous_level > 0 and level > previous_level + 1:
                analysis['hierarchy_issues'].append(f'Heading hierarchy skip: {heading.name.upper()} after H{previous_level}')
            
            previous_level = level
        
        # H1 validation
        if h1_count == 0:
            analysis['issues'].append('No H1 heading found - add main heading for page structure')
        elif h1_count > 1:
            analysis['issues'].append(f'Multiple H1 headings found ({h1_count}) - use only one H1 per page')
        
        # Add hierarchy issues to main issues
        analysis['issues'].extend(analysis['hierarchy_issues'])
        
        # Calculate score
        score_deductions = 0
        score_deductions += analysis['empty_headings'] * 10
        score_deductions += len(analysis['hierarchy_issues']) * 15
        if h1_count == 0 or h1_count > 1:
            score_deductions += 20
        
        analysis['score'] = max(0, 100 - score_deductions)
        
        return analysis
    
    def _validate_link_accessibility(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate link accessibility and descriptiveness."""
        links = soup.find_all('a', href=True)
        
        analysis = {
            'total_links': len(links),
            'descriptive_links': 0,
            'generic_links': 0,
            'missing_text': 0,
            'external_links_marked': 0,
            'issues': [],
            'score': 100
        }
        
        if len(links) == 0:
            return analysis
        
        generic_link_text = [
            'click here', 'read more', 'more', 'here', 'link', 'this',
            'click', 'view', 'see', 'check', 'visit'
        ]
        
        for link in links:
            link_text = link.get_text(strip=True).lower()
            href = link.get('href', '')
            
            # Check for missing link text
            if not link_text:
                # Check for image links
                img = link.find('img')
                if img and img.get('alt'):
                    link_text = img.get('alt').lower()
                else:
                    analysis['missing_text'] += 1
                    analysis['issues'].append(f'Link with no accessible text: {href[:50]}...')
                    continue
            
            # Check for generic link text
            if link_text in generic_link_text:
                analysis['generic_links'] += 1
                analysis['issues'].append(f'Generic link text: "{link_text}" for {href[:50]}...')
            else:
                analysis['descriptive_links'] += 1
            
            # Check external links
            if href.startswith('http') and self.base_url not in href:
                # Should have indication it's external
                if not any(indicator in link_text for indicator in ['external', 'opens', 'new window']):
                    rel = link.get('rel', [])
                    target = link.get('target', '')
                    if target == '_blank' and 'noopener' not in rel:
                        analysis['issues'].append(f'External link missing security attributes: {href[:50]}...')
        
        # Calculate score
        good_links = analysis['descriptive_links']
        total_valid_links = analysis['total_links'] - analysis['missing_text']
        if total_valid_links > 0:
            analysis['score'] = int((good_links / total_valid_links) * 100)
        
        return analysis
    
    def _validate_form_accessibility(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate form accessibility including labels and descriptions."""
        forms = soup.find_all('form')
        inputs = soup.find_all(['input', 'textarea', 'select'])
        
        analysis = {
            'total_forms': len(forms),
            'total_inputs': len(inputs),
            'labeled_inputs': 0,
            'required_marked': 0,
            'fieldsets_used': 0,
            'issues': [],
            'score': 100
        }
        
        if len(inputs) == 0:
            return analysis
        
        for input_elem in inputs:
            input_type = input_elem.get('type', 'text')
            input_id = input_elem.get('id', '')
            name = input_elem.get('name', '')
            
            # Skip hidden inputs and buttons
            if input_type in ['hidden', 'submit', 'button']:
                continue
            
            # Check for labels
            has_label = False
            
            # Method 1: Check for label with 'for' attribute
            if input_id:
                label = soup.find('label', {'for': input_id})
                if label:
                    has_label = True
            
            # Method 2: Check if input is wrapped in label
            if not has_label:
                parent_label = input_elem.find_parent('label')
                if parent_label:
                    has_label = True
            
            # Method 3: Check for aria-label or aria-labelledby
            if not has_label:
                if input_elem.get('aria-label') or input_elem.get('aria-labelledby'):
                    has_label = True
            
            if has_label:
                analysis['labeled_inputs'] += 1
            else:
                analysis['issues'].append(f'Input missing label: {input_type} input "{name}"')
            
            # Check required fields
            if input_elem.get('required') or input_elem.get('aria-required'):
                analysis['required_marked'] += 1
        
        # Check for fieldsets in forms with multiple inputs
        for form in forms:
            form_inputs = form.find_all(['input', 'textarea', 'select'])
            if len(form_inputs) > 3:  # Forms with many inputs should use fieldsets
                fieldsets = form.find_all('fieldset')
                if fieldsets:
                    analysis['fieldsets_used'] += 1
                else:
                    analysis['issues'].append('Complex form should use fieldsets for grouping')
        
        # Calculate score
        valid_inputs = len([i for i in inputs if i.get('type', 'text') not in ['hidden', 'submit', 'button']])
        if valid_inputs > 0:
            analysis['score'] = int((analysis['labeled_inputs'] / valid_inputs) * 100)
        
        return analysis
    
    def _validate_aria_attributes(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate ARIA attributes and landmarks."""
        elements_with_aria = soup.find_all(attrs={'aria-label': True}) + \
                           soup.find_all(attrs={'aria-labelledby': True}) + \
                           soup.find_all(attrs={'aria-describedby': True}) + \
                           soup.find_all(attrs={'role': True})
        
        landmarks = soup.find_all(attrs={'role': lambda x: x in [
            'main', 'navigation', 'banner', 'contentinfo', 'complementary', 'search'
        ] if x else False})
        
        analysis = {
            'aria_elements': len(elements_with_aria),
            'landmarks': len(landmarks),
            'invalid_aria': 0,
            'missing_landmarks': [],
            'issues': [],
            'score': 100
        }
        
        # Check for main landmarks
        required_landmarks = ['main']
        found_landmarks = [elem.get('role') for elem in landmarks]
        
        for required in required_landmarks:
            if required not in found_landmarks:
                analysis['missing_landmarks'].append(required)
                analysis['issues'].append(f'Missing {required} landmark for page structure')
        
        # Validate ARIA attributes
        for elem in elements_with_aria:
            # Check for common ARIA attribute issues
            aria_label = elem.get('aria-label', '')
            if aria_label and len(aria_label.strip()) < 3:
                analysis['invalid_aria'] += 1
                analysis['issues'].append(f'ARIA label too short: "{aria_label}"')
        
        # Calculate score based on proper ARIA usage
        base_score = 80 if analysis['aria_elements'] > 0 else 60
        landmark_bonus = min(len(landmarks) * 10, 20)
        penalty = len(analysis['missing_landmarks']) * 15 + analysis['invalid_aria'] * 10
        
        analysis['score'] = max(0, base_score + landmark_bonus - penalty)
        
        return analysis
    
    def _validate_color_contrast(self, soup: BeautifulSoup, wcag_level: str) -> Dict[str, Any]:
        """Validate color contrast ratios (basic implementation)."""
        analysis = {
            'contrast_issues': 0,
            'elements_checked': 0,
            'low_contrast_elements': [],
            'issues': [],
            'score': 85  # Default good score - full contrast checking requires advanced tools
        }
        
        # This is a simplified implementation
        # Full color contrast validation requires:
        # 1. Computed CSS styles
        # 2. Background color detection (including images)
        # 3. Color ratio calculations
        
        # Check for obvious contrast issues in inline styles
        elements_with_style = soup.find_all(attrs={'style': True})
        
        for elem in elements_with_style:
            style = elem.get('style', '')
            if 'color:' in style and 'background' in style:
                analysis['elements_checked'] += 1
                # This would require CSS parsing and color contrast calculation
                # For now, we'll flag potential issues
                if 'white' in style and 'yellow' in style:
                    analysis['contrast_issues'] += 1
                    analysis['issues'].append('Potential low contrast: white text on yellow background')
        
        # Check for common problematic color combinations in classes
        problematic_classes = soup.find_all(class_=re.compile(r'light.*text|yellow.*bg|gray.*light'))
        if problematic_classes:
            analysis['issues'].append(f'Found {len(problematic_classes)} elements with potentially low contrast classes')
        
        return analysis
    
    def _generate_accessibility_recommendations(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific accessibility recommendations."""
        recommendations = []
        accessibility = result['accessibility']
        
        # Image recommendations
        if accessibility['images']['missing_alt'] > 0:
            recommendations.append(f"Add alt attributes to {accessibility['images']['missing_alt']} images")
        
        if accessibility['images']['empty_alt'] > 0:
            recommendations.append(f"Improve alt text descriptions for {accessibility['images']['empty_alt']} images")
        
        # Heading recommendations
        if accessibility['headings']['hierarchy_issues']:
            recommendations.append("Fix heading hierarchy - avoid skipping heading levels")
        
        if accessibility['headings']['empty_headings'] > 0:
            recommendations.append(f"Add content to {accessibility['headings']['empty_headings']} empty headings")
        
        # Link recommendations
        if accessibility['links']['generic_links'] > 0:
            recommendations.append(f"Make {accessibility['links']['generic_links']} link texts more descriptive")
        
        if accessibility['links']['missing_text'] > 0:
            recommendations.append(f"Add accessible text to {accessibility['links']['missing_text']} links")
        
        # Form recommendations
        if accessibility['forms']['total_inputs'] > accessibility['forms']['labeled_inputs']:
            missing_labels = accessibility['forms']['total_inputs'] - accessibility['forms']['labeled_inputs']
            recommendations.append(f"Add labels to {missing_labels} form inputs")
        
        # ARIA recommendations
        if accessibility['aria']['missing_landmarks']:
            landmarks = ', '.join(accessibility['aria']['missing_landmarks'])
            recommendations.append(f"Add ARIA landmarks: {landmarks}")
        
        # Color contrast recommendations
        if accessibility['color_contrast']['contrast_issues'] > 0:
            recommendations.append("Review and improve color contrast ratios for better readability")
        
        result['recommendations'] = recommendations
        return result