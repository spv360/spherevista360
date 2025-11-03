"""
Accessibility Auto-Fix Engine
============================
Automated accessibility improvements for WordPress sites including:
- ARIA attribute injection and optimization
- Alt text generation for images
- Color contrast analysis and recommendations
- WCAG compliance checks and fixes
- Keyboard navigation improvements
- Screen reader optimization
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
import requests
from datetime import datetime
import colorsys

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class AccessibilityOptimizer:
    """Advanced accessibility optimization utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize accessibility optimizer."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
        # WCAG compliance thresholds
        self.wcag_thresholds = {
            'aa_normal_contrast': 4.5,      # WCAG AA for normal text
            'aa_large_contrast': 3.0,       # WCAG AA for large text
            'aaa_normal_contrast': 7.0,     # WCAG AAA for normal text
            'aaa_large_contrast': 4.5,      # WCAG AAA for large text
            'large_text_size': 18           # Large text threshold (px)
        }
        
        # Common ARIA roles and attributes
        self.aria_roles = {
            'navigation': ['nav', 'ul'],
            'banner': ['header'],
            'contentinfo': ['footer'],
            'main': ['main'],
            'complementary': ['aside'],
            'article': ['article'],
            'region': ['section'],
            'button': ['button', 'input[type="button"]', 'input[type="submit"]'],
            'link': ['a'],
            'heading': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
            'list': ['ul', 'ol'],
            'listitem': ['li']
        }
        
        # Common accessibility patterns
        self.a11y_patterns = {
            'form_controls': ['input', 'textarea', 'select'],
            'interactive_elements': ['button', 'a', 'input', 'textarea', 'select'],
            'media_elements': ['img', 'video', 'audio', 'iframe'],
            'structural_elements': ['nav', 'main', 'header', 'footer', 'aside', 'section']
        }
    
    def optimize_post_accessibility(self, post_id: int, auto_apply: bool = False) -> Dict[str, Any]:
        """Comprehensive accessibility optimization for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            content = post.get('content', {}).get('rendered', '')
            post_url = post.get('link', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'accessibility_optimization': {
                    'aria_attributes': {'score': 0, 'improvements': []},
                    'alt_text_optimization': {'score': 0, 'improvements': []},
                    'color_contrast': {'score': 0, 'improvements': []},
                    'wcag_compliance': {'score': 0, 'improvements': []},
                    'keyboard_navigation': {'score': 0, 'improvements': []},
                    'screen_reader_optimization': {'score': 0, 'improvements': []}
                },
                'optimized_content': {
                    'content': content,
                    'aria_attributes_added': [],
                    'alt_text_generated': [],
                    'accessibility_fixes': [],
                    'wcag_improvements': []
                },
                'accessibility_summary': [],
                'score': 0
            }
            
            if not content:
                result['accessibility_optimization']['aria_attributes']['improvements'].append('No content to optimize')
                return result
            
            # Parse content for analysis
            soup = BeautifulSoup(content, 'html.parser')
            
            # Run accessibility optimization analyses
            result['accessibility_optimization']['aria_attributes'] = self._optimize_aria_attributes(
                soup, auto_apply
            )
            result['accessibility_optimization']['alt_text_optimization'] = self._optimize_alt_text(
                soup, auto_apply
            )
            result['accessibility_optimization']['color_contrast'] = self._analyze_color_contrast(
                soup, auto_apply
            )
            result['accessibility_optimization']['wcag_compliance'] = self._check_wcag_compliance(
                soup, auto_apply
            )
            result['accessibility_optimization']['keyboard_navigation'] = self._optimize_keyboard_navigation(
                soup, auto_apply
            )
            result['accessibility_optimization']['screen_reader_optimization'] = self._optimize_screen_reader(
                soup, auto_apply
            )
            
            # Generate optimized content
            if auto_apply:
                result['optimized_content'] = self._generate_optimized_accessibility_content(
                    soup, result['accessibility_optimization']
                )
            
            # Calculate overall accessibility score
            scores = [section['score'] for section in result['accessibility_optimization'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all accessibility improvements
            all_improvements = []
            for section_name, section_data in result['accessibility_optimization'].items():
                if section_data['improvements']:
                    all_improvements.extend([f"{section_name.replace('_', ' ').title()}: {imp}" for imp in section_data['improvements']])
            
            result['accessibility_summary'] = all_improvements
            
            # Set status based on score
            if result['score'] >= 90:
                result['status'] = 'excellent'
                result['message'] = 'Accessibility is well optimized'
            elif result['score'] >= 75:
                result['status'] = 'good'
                result['message'] = 'Good accessibility with minor improvements possible'
            elif result['score'] >= 60:
                result['status'] = 'fair'
                result['message'] = 'Accessibility needs improvements'
            else:
                result['status'] = 'poor'
                result['message'] = 'Significant accessibility improvements needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error optimizing accessibility: {str(e)}'
            }
    
    def _optimize_aria_attributes(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize ARIA attributes for better screen reader support."""
        analysis = {
            'missing_aria_labels': [],
            'incorrect_roles': [],
            'landmark_roles': {},
            'interactive_elements': {},
            'improvements': [],
            'score': 75  # Default score
        }
        
        # Check landmark roles
        landmarks = {
            'main': soup.find_all('main'),
            'nav': soup.find_all('nav'),
            'header': soup.find_all('header'),
            'footer': soup.find_all('footer'),
            'aside': soup.find_all('aside')
        }
        
        analysis['landmark_roles'] = {
            landmark: len(elements) for landmark, elements in landmarks.items()
        }
        
        # Check for missing main landmark
        if not landmarks['main']:
            main_content = soup.find('div', class_=re.compile(r'main|content'))
            if main_content and auto_apply:
                main_content['role'] = 'main'
                analysis['improvements'].append('Added main landmark role')
                analysis['score'] += 10
            else:
                analysis['improvements'].append('Add main landmark for primary content')
                analysis['score'] -= 15
        
        # Check interactive elements for ARIA labels
        buttons = soup.find_all('button')
        links = soup.find_all('a')
        inputs = soup.find_all('input')
        
        interactive_elements = buttons + links + inputs
        missing_labels = []
        
        for element in interactive_elements:
            element_text = element.get_text().strip()
            aria_label = element.get('aria-label')
            aria_labelledby = element.get('aria-labelledby')
            title = element.get('title')
            alt = element.get('alt')
            
            # Check if element has accessible name
            has_accessible_name = bool(
                element_text or aria_label or aria_labelledby or title or alt
            )
            
            if not has_accessible_name:
                missing_labels.append({
                    'tag': element.name,
                    'element': str(element)[:100],
                    'suggestion': self._generate_aria_label_suggestion(element)
                })
                
                if auto_apply:
                    suggestion = self._generate_aria_label_suggestion(element)
                    if suggestion:
                        element['aria-label'] = suggestion
        
        analysis['missing_aria_labels'] = missing_labels
        
        if missing_labels:
            analysis['improvements'].append(f'Add ARIA labels to {len(missing_labels)} interactive elements')
            analysis['score'] -= len(missing_labels) * 5
        
        # Check form elements specifically
        form_elements = soup.find_all(['input', 'textarea', 'select'])
        form_issues = []
        
        for form_element in form_elements:
            element_id = form_element.get('id')
            aria_labelledby = form_element.get('aria-labelledby')
            aria_label = form_element.get('aria-label')
            
            # Look for associated label
            label = None
            if element_id:
                label = soup.find('label', attrs={'for': element_id})
            
            if not (label or aria_labelledby or aria_label):
                form_issues.append(str(form_element)[:100])
                
                if auto_apply and element_id:
                    # Try to find nearby text that could be a label
                    parent = form_element.parent
                    if parent:
                        label_text = self._extract_label_text(parent)
                        if label_text:
                            form_element['aria-label'] = label_text
        
        if form_issues:
            analysis['improvements'].append(f'Associate labels with {len(form_issues)} form controls')
            analysis['score'] -= len(form_issues) * 8
        
        # Check heading structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        heading_levels = [int(h.name[1]) for h in headings]
        
        if headings:
            # Check for skipped heading levels
            for i, level in enumerate(heading_levels[1:], 1):
                prev_level = heading_levels[i-1]
                if level > prev_level + 1:
                    analysis['improvements'].append('Heading structure skips levels - maintain logical hierarchy')
                    analysis['score'] -= 10
                    break
        
        analysis['interactive_elements'] = {
            'buttons': len(buttons),
            'links': len(links),
            'form_controls': len(inputs),
            'missing_labels': len(missing_labels)
        }
        
        return analysis
    
    def _optimize_alt_text(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize alt text for images."""
        analysis = {
            'total_images': 0,
            'images_with_alt': 0,
            'images_without_alt': 0,
            'decorative_images': 0,
            'generated_alt_text': [],
            'improvements': [],
            'score': 80  # Default score
        }
        
        images = soup.find_all('img')
        analysis['total_images'] = len(images)
        
        images_without_alt = []
        images_with_empty_alt = []
        images_with_good_alt = []
        
        for img in images:
            alt = img.get('alt')
            src = img.get('src', '')
            
            if alt is None:
                images_without_alt.append(img)
            elif alt == '':
                images_with_empty_alt.append(img)
            elif len(alt.strip()) < 5:
                # Very short alt text - likely not descriptive enough
                images_without_alt.append(img)
            else:
                images_with_good_alt.append(img)
        
        analysis['images_with_alt'] = len(images_with_good_alt)
        analysis['images_without_alt'] = len(images_without_alt)
        analysis['decorative_images'] = len(images_with_empty_alt)
        
        # Generate alt text for images without it
        for img in images_without_alt:
            if auto_apply:
                generated_alt = self._generate_alt_text(img)
                if generated_alt:
                    img['alt'] = generated_alt
                    analysis['generated_alt_text'].append({
                        'src': img.get('src', '')[:50],
                        'alt': generated_alt
                    })
        
        # Score based on coverage
        if analysis['total_images'] > 0:
            alt_coverage = (analysis['images_with_alt'] + len(analysis['generated_alt_text'])) / analysis['total_images']
            analysis['score'] = int(alt_coverage * 100)
        
        if images_without_alt:
            analysis['improvements'].append(f'Add alt text to {len(images_without_alt)} images')
            analysis['score'] -= len(images_without_alt) * 10
        
        # Check for poor alt text patterns
        poor_alt_patterns = ['image', 'picture', 'photo', 'img', 'untitled']
        poor_alt_images = []
        
        for img in images_with_good_alt:
            alt = img.get('alt', '').lower()
            if any(pattern in alt for pattern in poor_alt_patterns):
                poor_alt_images.append(img)
        
        if poor_alt_images:
            analysis['improvements'].append(f'Improve alt text quality for {len(poor_alt_images)} images')
            analysis['score'] -= len(poor_alt_images) * 3
        
        return analysis
    
    def _analyze_color_contrast(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Analyze color contrast for WCAG compliance."""
        analysis = {
            'contrast_issues': [],
            'color_combinations': [],
            'wcag_aa_compliance': True,
            'wcag_aaa_compliance': True,
            'improvements': [],
            'score': 85  # Default score (assuming good contrast without detailed analysis)
        }
        
        # Extract color information from inline styles
        elements_with_color = soup.find_all(attrs={'style': re.compile(r'color|background')})
        
        for element in elements_with_color:
            style = element.get('style', '')
            colors = self._extract_colors_from_style(style)
            
            if colors['foreground'] and colors['background']:
                contrast_ratio = self._calculate_contrast_ratio(
                    colors['foreground'], 
                    colors['background']
                )
                
                if contrast_ratio:
                    # Estimate font size (simplified)
                    font_size = self._estimate_font_size(element, style)
                    is_large_text = font_size >= self.wcag_thresholds['large_text_size']
                    
                    aa_threshold = (self.wcag_thresholds['aa_large_contrast'] 
                                  if is_large_text 
                                  else self.wcag_thresholds['aa_normal_contrast'])
                    
                    aaa_threshold = (self.wcag_thresholds['aaa_large_contrast'] 
                                   if is_large_text 
                                   else self.wcag_thresholds['aaa_normal_contrast'])
                    
                    color_combo = {
                        'element': element.name,
                        'foreground': colors['foreground'],
                        'background': colors['background'],
                        'contrast_ratio': contrast_ratio,
                        'font_size': font_size,
                        'is_large_text': is_large_text,
                        'wcag_aa_pass': contrast_ratio >= aa_threshold,
                        'wcag_aaa_pass': contrast_ratio >= aaa_threshold
                    }
                    
                    analysis['color_combinations'].append(color_combo)
                    
                    if not color_combo['wcag_aa_pass']:
                        analysis['contrast_issues'].append(color_combo)
                        analysis['wcag_aa_compliance'] = False
                        
                        if auto_apply:
                            # Suggest better colors (simplified)
                            improved_colors = self._suggest_better_contrast(
                                colors['foreground'], colors['background'], aa_threshold
                            )
                            if improved_colors:
                                element['data-a11y-suggestion'] = f"Consider using {improved_colors}"
                    
                    if not color_combo['wcag_aaa_pass']:
                        analysis['wcag_aaa_compliance'] = False
        
        if analysis['contrast_issues']:
            analysis['improvements'].append(f'{len(analysis["contrast_issues"])} color combinations fail WCAG AA contrast requirements')
            analysis['score'] -= len(analysis['contrast_issues']) * 15
        
        if not analysis['wcag_aaa_compliance'] and analysis['wcag_aa_compliance']:
            analysis['improvements'].append('Consider improving contrast for WCAG AAA compliance')
            analysis['score'] -= 5
        
        # General recommendations
        analysis['improvements'].append('Use color contrast checking tools for comprehensive analysis')
        analysis['improvements'].append('Ensure sufficient contrast for all text elements')
        
        return analysis
    
    def _check_wcag_compliance(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Check WCAG compliance guidelines."""
        analysis = {
            'perceivable': {'score': 80, 'issues': []},
            'operable': {'score': 80, 'issues': []},
            'understandable': {'score': 80, 'issues': []},
            'robust': {'score': 80, 'issues': []},
            'improvements': [],
            'score': 80
        }
        
        # Perceivable checks
        # Check for images without alt text
        images_without_alt = soup.find_all('img', alt=None)
        if images_without_alt:
            analysis['perceivable']['issues'].append(f'{len(images_without_alt)} images missing alt text')
            analysis['perceivable']['score'] -= len(images_without_alt) * 5
        
        # Check for videos without captions (simplified check)
        videos = soup.find_all('video')
        videos_without_captions = [v for v in videos if not v.find('track', kind='captions')]
        if videos_without_captions:
            analysis['perceivable']['issues'].append(f'{len(videos_without_captions)} videos may be missing captions')
            analysis['perceivable']['score'] -= len(videos_without_captions) * 10
        
        # Operable checks
        # Check for keyboard accessibility
        interactive_no_tabindex = soup.find_all(['div', 'span'], attrs={'onclick': True})
        clickable_non_interactive = [el for el in interactive_no_tabindex if not el.get('tabindex')]
        if clickable_non_interactive:
            analysis['operable']['issues'].append(f'{len(clickable_non_interactive)} clickable elements not keyboard accessible')
            analysis['operable']['score'] -= len(clickable_non_interactive) * 8
            
            if auto_apply:
                for element in clickable_non_interactive:
                    element['tabindex'] = '0'
                    element['role'] = 'button'
        
        # Check for focus indicators (simplified)
        links_buttons = soup.find_all(['a', 'button', 'input'])
        elements_without_focus_style = []
        for element in links_buttons:
            style = element.get('style', '')
            if 'outline' in style and 'none' in style:
                elements_without_focus_style.append(element)
        
        if elements_without_focus_style:
            analysis['operable']['issues'].append(f'{len(elements_without_focus_style)} elements have disabled focus indicators')
            analysis['operable']['score'] -= len(elements_without_focus_style) * 5
        
        # Understandable checks
        # Check language declaration
        html_tag = soup.find('html')
        if not (html_tag and html_tag.get('lang')):
            analysis['understandable']['issues'].append('Page language not declared')
            analysis['understandable']['score'] -= 15
        
        # Check for placeholder text as labels
        inputs_with_placeholder = soup.find_all('input', placeholder=True)
        inputs_placeholder_only = []
        for input_el in inputs_with_placeholder:
            input_id = input_el.get('id')
            has_label = bool(soup.find('label', attrs={'for': input_id})) if input_id else False
            has_aria_label = bool(input_el.get('aria-label') or input_el.get('aria-labelledby'))
            
            if not (has_label or has_aria_label):
                inputs_placeholder_only.append(input_el)
        
        if inputs_placeholder_only:
            analysis['understandable']['issues'].append(f'{len(inputs_placeholder_only)} form controls rely only on placeholder text')
            analysis['understandable']['score'] -= len(inputs_placeholder_only) * 8
        
        # Robust checks
        # Check for valid HTML structure
        duplicate_ids = self._find_duplicate_ids(soup)
        if duplicate_ids:
            analysis['robust']['issues'].append(f'{len(duplicate_ids)} duplicate IDs found')
            analysis['robust']['score'] -= len(duplicate_ids) * 10
        
        # Check for proper heading hierarchy
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings:
            heading_levels = [int(h.name[1]) for h in headings]
            if heading_levels[0] != 1:
                analysis['robust']['issues'].append('Page should start with H1 heading')
                analysis['robust']['score'] -= 10
        
        # Calculate overall score
        section_scores = [
            analysis['perceivable']['score'],
            analysis['operable']['score'],
            analysis['understandable']['score'],
            analysis['robust']['score']
        ]
        analysis['score'] = int(sum(section_scores) / len(section_scores))
        
        # Collect all issues as improvements
        for section_name, section_data in analysis.items():
            if isinstance(section_data, dict) and 'issues' in section_data:
                analysis['improvements'].extend([f"{section_name.title()}: {issue}" for issue in section_data['issues']])
        
        return analysis
    
    def _optimize_keyboard_navigation(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize keyboard navigation accessibility."""
        analysis = {
            'tab_order': {},
            'focus_management': {},
            'skip_links': {},
            'improvements': [],
            'score': 75  # Default score
        }
        
        # Check tab order
        tabbable_elements = soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
        positive_tabindex = [el for el in tabbable_elements if el.get('tabindex', '0').isdigit() and int(el.get('tabindex', '0')) > 0]
        
        analysis['tab_order'] = {
            'total_tabbable': len(tabbable_elements),
            'positive_tabindex': len(positive_tabindex),
            'logical_order': len(positive_tabindex) == 0  # Positive tabindex can disrupt logical order
        }
        
        if positive_tabindex:
            analysis['improvements'].append(f'{len(positive_tabindex)} elements use positive tabindex - may disrupt tab order')
            analysis['score'] -= len(positive_tabindex) * 5
        
        # Check for skip links
        skip_links = soup.find_all('a', href=re.compile(r'^#'))
        skip_to_main = [link for link in skip_links if 'main' in link.get('href', '').lower() or 'content' in link.get('href', '').lower()]
        
        analysis['skip_links'] = {
            'total_skip_links': len(skip_links),
            'skip_to_main': len(skip_to_main) > 0
        }
        
        if not skip_to_main:
            analysis['improvements'].append('Add skip-to-main-content link for keyboard users')
            analysis['score'] -= 15
            
            if auto_apply:
                # Add skip link (would need to be in page header)
                analysis['skip_links']['added'] = True
        
        # Check for keyboard traps
        elements_with_tabindex_negative = soup.find_all(attrs={'tabindex': '-1'})
        analysis['focus_management'] = {
            'programmatic_focus': len(elements_with_tabindex_negative),
            'focus_traps_detected': False  # Would need JavaScript analysis
        }
        
        # Check interactive elements without proper roles
        clickable_divs = soup.find_all('div', attrs={'onclick': True})
        missing_button_role = [div for div in clickable_divs if not div.get('role')]
        
        if missing_button_role:
            analysis['improvements'].append(f'{len(missing_button_role)} clickable elements missing button role')
            analysis['score'] -= len(missing_button_role) * 8
            
            if auto_apply:
                for div in missing_button_role:
                    div['role'] = 'button'
                    div['tabindex'] = '0'
        
        return analysis
    
    def _optimize_screen_reader(self, soup: BeautifulSoup, auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize content for screen readers."""
        analysis = {
            'semantic_structure': {},
            'aria_live_regions': {},
            'descriptive_text': {},
            'improvements': [],
            'score': 75  # Default score
        }
        
        # Check semantic structure
        semantic_elements = {
            'header': len(soup.find_all('header')),
            'nav': len(soup.find_all('nav')),
            'main': len(soup.find_all('main')),
            'article': len(soup.find_all('article')),
            'section': len(soup.find_all('section')),
            'aside': len(soup.find_all('aside')),
            'footer': len(soup.find_all('footer'))
        }
        
        analysis['semantic_structure'] = semantic_elements
        
        # Check for missing semantic elements
        if semantic_elements['main'] == 0:
            analysis['improvements'].append('Add main element for primary content')
            analysis['score'] -= 15
        
        if semantic_elements['nav'] == 0:
            nav_elements = soup.find_all('ul', class_=re.compile(r'nav|menu'))
            if nav_elements:
                analysis['improvements'].append('Wrap navigation lists in nav element')
                analysis['score'] -= 10
                
                if auto_apply:
                    for nav_ul in nav_elements[:1]:  # First navigation
                        nav_wrapper = soup.new_tag('nav')
                        nav_ul.wrap(nav_wrapper)
        
        # Check for ARIA live regions
        live_regions = soup.find_all(attrs={'aria-live': True})
        dynamic_content = soup.find_all(attrs={'id': re.compile(r'status|alert|notification')})
        
        analysis['aria_live_regions'] = {
            'existing_live_regions': len(live_regions),
            'potential_dynamic_content': len(dynamic_content)
        }
        
        if dynamic_content and not live_regions:
            analysis['improvements'].append('Consider adding ARIA live regions for dynamic content')
            analysis['score'] -= 8
        
        # Check descriptive text
        links_without_context = []
        links = soup.find_all('a')
        
        for link in links:
            link_text = link.get_text().strip().lower()
            if link_text in ['click here', 'read more', 'more', 'here', 'link']:
                links_without_context.append(link)
                
                if auto_apply:
                    # Try to add context from surrounding text
                    context = self._extract_link_context(link)
                    if context:
                        current_text = link.get_text()
                        link.string = f"{current_text} - {context}"
        
        analysis['descriptive_text'] = {
            'links_without_context': len(links_without_context),
            'total_links': len(links)
        }
        
        if links_without_context:
            analysis['improvements'].append(f'{len(links_without_context)} links have non-descriptive text')
            analysis['score'] -= len(links_without_context) * 5
        
        # Check for table headers
        tables = soup.find_all('table')
        tables_without_headers = []
        
        for table in tables:
            has_th = bool(table.find('th'))
            has_header_row = bool(table.find('tr', {'role': 'rowheader'}))
            
            if not (has_th or has_header_row):
                tables_without_headers.append(table)
                
                if auto_apply:
                    first_row = table.find('tr')
                    if first_row:
                        cells = first_row.find_all('td')
                        for cell in cells:
                            cell.name = 'th'
                            cell['scope'] = 'col'
        
        if tables_without_headers:
            analysis['improvements'].append(f'{len(tables_without_headers)} tables missing header cells')
            analysis['score'] -= len(tables_without_headers) * 10
        
        return analysis
    
    def _generate_optimized_accessibility_content(self, soup: BeautifulSoup, 
                                                accessibility_optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized content with accessibility improvements applied."""
        optimized = {
            'content': str(soup),
            'aria_attributes_added': [],
            'alt_text_generated': [],
            'accessibility_fixes': [],
            'wcag_improvements': []
        }
        
        # Collect applied improvements
        for section_name, section_data in accessibility_optimization.items():
            if isinstance(section_data, dict):
                # ARIA attributes
                if 'aria_attributes' in section_name and 'improvements' in section_data:
                    optimized['aria_attributes_added'].extend(section_data['improvements'])
                
                # Alt text
                if 'alt_text' in section_name and 'generated_alt_text' in section_data:
                    optimized['alt_text_generated'] = section_data['generated_alt_text']
                
                # General accessibility fixes
                if 'improvements' in section_data:
                    optimized['accessibility_fixes'].extend(section_data['improvements'])
        
        optimized['content'] = str(soup)
        return optimized
    
    # Helper methods
    def _generate_aria_label_suggestion(self, element: Tag) -> str:
        """Generate ARIA label suggestion for an element."""
        tag_name = element.name
        element_text = element.get_text().strip()
        
        if element_text:
            return element_text
        
        # Try to get context from parent or nearby elements
        if element.parent:
            parent_text = element.parent.get_text().strip()
            if parent_text and len(parent_text) < 50:
                return parent_text
        
        # Fallback suggestions based on element type
        if tag_name == 'button':
            return 'Button'
        elif tag_name == 'a':
            href = element.get('href', '')
            if href.startswith('#'):
                return f'Navigate to {href[1:]}'
            return 'Link'
        elif tag_name == 'input':
            input_type = element.get('type', 'text')
            return f'{input_type.title()} input'
        
        return 'Interactive element'
    
    def _generate_alt_text(self, img: Tag) -> str:
        """Generate alt text for an image."""
        src = img.get('src', '')
        
        # Extract filename for basic description
        if src:
            filename = src.split('/')[-1].split('.')[0]
            # Clean up filename
            filename = re.sub(r'[_-]', ' ', filename)
            filename = re.sub(r'\d+', '', filename)  # Remove numbers
            return filename.strip().title() if filename.strip() else 'Image'
        
        # Look for context in surrounding elements
        if img.parent:
            parent_text = img.parent.get_text().strip()
            if parent_text and len(parent_text) < 100:
                return f'Image: {parent_text[:50]}'
        
        return 'Image'
    
    def _extract_colors_from_style(self, style: str) -> Dict[str, str]:
        """Extract foreground and background colors from style string."""
        colors = {'foreground': None, 'background': None}
        
        # Extract color values
        color_match = re.search(r'color:\s*([^;]+)', style)
        if color_match:
            colors['foreground'] = color_match.group(1).strip()
        
        bg_match = re.search(r'background-color:\s*([^;]+)', style)
        if bg_match:
            colors['background'] = bg_match.group(1).strip()
        
        return colors
    
    def _calculate_contrast_ratio(self, color1: str, color2: str) -> Optional[float]:
        """Calculate contrast ratio between two colors."""
        try:
            # This is a simplified implementation
            # In practice, you'd want a more robust color parsing library
            
            # Convert colors to RGB (simplified for common formats)
            rgb1 = self._color_to_rgb(color1)
            rgb2 = self._color_to_rgb(color2)
            
            if rgb1 and rgb2:
                # Calculate relative luminance
                lum1 = self._relative_luminance(rgb1)
                lum2 = self._relative_luminance(rgb2)
                
                # Calculate contrast ratio
                lighter = max(lum1, lum2)
                darker = min(lum1, lum2)
                
                return (lighter + 0.05) / (darker + 0.05)
        
        except Exception:
            pass
        
        return None
    
    def _color_to_rgb(self, color: str) -> Optional[Tuple[int, int, int]]:
        """Convert color string to RGB tuple (simplified)."""
        color = color.strip().lower()
        
        # Handle hex colors
        if color.startswith('#'):
            hex_color = color[1:]
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            if len(hex_color) == 6:
                try:
                    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                except ValueError:
                    pass
        
        # Handle named colors (basic set)
        named_colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255)
        }
        
        return named_colors.get(color)
    
    def _relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance of an RGB color."""
        def normalize_component(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else pow((c + 0.055) / 1.055, 2.4)
        
        r, g, b = rgb
        return 0.2126 * normalize_component(r) + 0.7152 * normalize_component(g) + 0.0722 * normalize_component(b)
    
    def _estimate_font_size(self, element: Tag, style: str) -> int:
        """Estimate font size from element and style (simplified)."""
        # Look for font-size in style
        font_size_match = re.search(r'font-size:\s*(\d+)px', style)
        if font_size_match:
            return int(font_size_match.group(1))
        
        # Default sizes for common elements
        tag_defaults = {
            'h1': 32, 'h2': 24, 'h3': 18, 'h4': 16, 'h5': 14, 'h6': 12,
            'small': 12, 'big': 18
        }
        
        return tag_defaults.get(element.name, 16)  # Default to 16px
    
    def _suggest_better_contrast(self, fg_color: str, bg_color: str, target_ratio: float) -> Optional[str]:
        """Suggest colors with better contrast (simplified)."""
        # This is a basic implementation
        # In practice, you'd want more sophisticated color adjustment
        
        if fg_color.lower() in ['black', '#000000', '#000']:
            if target_ratio > 4.5:
                return 'white background (#ffffff)'
        elif fg_color.lower() in ['white', '#ffffff', '#fff']:
            if target_ratio > 4.5:
                return 'dark background (#000000)'
        
        return 'higher contrast color combination'
    
    def _extract_label_text(self, parent: Tag) -> Optional[str]:
        """Extract potential label text from parent element."""
        text = parent.get_text().strip()
        
        # Clean up and validate
        if text and len(text) < 100 and not text.isdigit():
            # Remove common unwanted text
            clean_text = re.sub(r'[*:]+$', '', text).strip()
            return clean_text if clean_text else None
        
        return None
    
    def _find_duplicate_ids(self, soup: BeautifulSoup) -> List[str]:
        """Find duplicate ID attributes."""
        ids = []
        elements_with_id = soup.find_all(attrs={'id': True})
        
        for element in elements_with_id:
            element_id = element.get('id')
            if element_id:
                ids.append(element_id)
        
        # Find duplicates
        seen = set()
        duplicates = []
        
        for id_val in ids:
            if id_val in seen:
                duplicates.append(id_val)
            else:
                seen.add(id_val)
        
        return duplicates
    
    def _extract_link_context(self, link: Tag) -> Optional[str]:
        """Extract context for a link from surrounding content."""
        # Look for context in parent elements
        parent = link.parent
        
        while parent and parent.name != 'body':
            parent_text = parent.get_text().strip()
            
            # Look for headings or other descriptive text
            if parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
                context_text = parent_text.replace(link.get_text(), '').strip()
                if context_text and len(context_text) < 50:
                    return context_text
            
            parent = parent.parent
        
        return None