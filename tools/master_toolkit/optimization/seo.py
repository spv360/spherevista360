"""
SEO Optimization Engine
=======================
Automated SEO improvements for WordPress sites including:
- Meta tag generation and optimization
- Schema markup injection and enhancement
- Internal linking optimization
- URL structure improvements
- Content SEO enhancements
- XML sitemap optimization
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
from datetime import datetime

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class SEOOptimizer:
    """Advanced SEO optimization utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize SEO optimizer."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
        # SEO optimization parameters
        self.ideal_title_length = 60
        self.ideal_description_length = 155
        self.max_h1_count = 1
        self.ideal_keyword_density = 0.015  # 1.5%
        
        # Schema.org templates
        self.schema_templates = {
            'Article': {
                '@context': 'https://schema.org',
                '@type': 'Article',
                'headline': '',
                'author': {'@type': 'Person', 'name': ''},
                'datePublished': '',
                'dateModified': '',
                'description': '',
                'mainEntityOfPage': {'@type': 'WebPage', '@id': ''},
                'publisher': {
                    '@type': 'Organization',
                    'name': 'SphereVista360',
                    'logo': {'@type': 'ImageObject', 'url': ''}
                }
            },
            'BreadcrumbList': {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': []
            }
        }
    
    def optimize_post_seo(self, post_id: int, target_keywords: List[str] = None, 
                         auto_apply: bool = False) -> Dict[str, Any]:
        """Comprehensive SEO optimization for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            content = post.get('content', {}).get('rendered', '')
            excerpt = post.get('excerpt', {}).get('rendered', '')
            post_url = post.get('link', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'seo_optimization': {
                    'meta_tags': {'score': 0, 'improvements': []},
                    'schema_markup': {'score': 0, 'improvements': []},
                    'internal_linking': {'score': 0, 'improvements': []},
                    'content_seo': {'score': 0, 'improvements': []},
                    'url_optimization': {'score': 0, 'improvements': []},
                    'technical_seo': {'score': 0, 'improvements': []}
                },
                'optimized_content': {
                    'title': post_title,
                    'content': content,
                    'excerpt': excerpt,
                    'meta_description': '',
                    'schema_markup': {},
                    'internal_links_added': []
                },
                'improvements_summary': [],
                'score': 0
            }
            
            if not content:
                result['seo_optimization']['content_seo']['improvements'].append('No content to optimize')
                return result
            
            # Parse content for analysis
            soup = BeautifulSoup(content, 'html.parser')
            
            # Run SEO optimization analyses
            result['seo_optimization']['meta_tags'] = self._optimize_meta_tags(
                post_title, content, excerpt, target_keywords
            )
            result['seo_optimization']['schema_markup'] = self._optimize_schema_markup(
                post, target_keywords
            )
            result['seo_optimization']['internal_linking'] = self._optimize_internal_linking(
                soup, post_id, auto_apply
            )
            result['seo_optimization']['content_seo'] = self._optimize_content_seo(
                soup, target_keywords, auto_apply
            )
            result['seo_optimization']['url_optimization'] = self._optimize_url_structure(
                post_url, post_title
            )
            result['seo_optimization']['technical_seo'] = self._optimize_technical_seo(
                soup, post_url, auto_apply
            )
            
            # Generate optimized content
            if auto_apply:
                result['optimized_content'] = self._generate_optimized_seo_content(
                    post, soup, result['seo_optimization'], target_keywords
                )
            
            # Calculate overall SEO score
            scores = [section['score'] for section in result['seo_optimization'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all improvements
            all_improvements = []
            for section_name, section_data in result['seo_optimization'].items():
                if section_data['improvements']:
                    all_improvements.extend([f"{section_name.replace('_', ' ').title()}: {imp}" for imp in section_data['improvements']])
            
            result['improvements_summary'] = all_improvements
            
            # Set status based on score
            if result['score'] >= 85:
                result['status'] = 'excellent'
                result['message'] = 'SEO is well optimized'
            elif result['score'] >= 70:
                result['status'] = 'good'
                result['message'] = 'Good SEO with minor improvements possible'
            elif result['score'] >= 50:
                result['status'] = 'fair'
                result['message'] = 'SEO needs improvements'
            else:
                result['status'] = 'poor'
                result['message'] = 'Significant SEO improvements needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error optimizing SEO: {str(e)}'
            }
    
    def _optimize_meta_tags(self, title: str, content: str, excerpt: str, 
                           target_keywords: List[str] = None) -> Dict[str, Any]:
        """Optimize meta tags including title and description."""
        analysis = {
            'title_optimization': {},
            'description_optimization': {},
            'keyword_optimization': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Analyze title
        title_length = len(title)
        analysis['title_optimization'] = {
            'current_title': title,
            'length': title_length,
            'optimal_length': 50 <= title_length <= 60,
            'keyword_in_title': False,
            'optimized_title': title
        }
        
        # Check for keywords in title
        if target_keywords:
            for keyword in target_keywords:
                if keyword.lower() in title.lower():
                    analysis['title_optimization']['keyword_in_title'] = True
                    break
            
            if not analysis['title_optimization']['keyword_in_title']:
                analysis['improvements'].append('Include target keyword in title')
                analysis['score'] -= 15
                
                # Generate optimized title
                if target_keywords:
                    primary_keyword = target_keywords[0]
                    if len(title + ' - ' + primary_keyword) <= 60:
                        analysis['title_optimization']['optimized_title'] = f"{title} - {primary_keyword}"
        
        # Title length optimization
        if title_length < 30:
            analysis['improvements'].append('Title is too short - expand for better SEO')
            analysis['score'] -= 15
        elif title_length > 70:
            analysis['improvements'].append('Title is too long - may be truncated in search results')
            analysis['score'] -= 10
        else:
            analysis['score'] += 10
        
        # Optimize meta description
        if excerpt:
            description = excerpt
        else:
            description = self._generate_meta_description_from_content(content, target_keywords)
            analysis['improvements'].append('Generated meta description from content')
        
        desc_length = len(description)
        analysis['description_optimization'] = {
            'current_description': description,
            'length': desc_length,
            'optimal_length': 140 <= desc_length <= 160,
            'keyword_in_description': False,
            'optimized_description': description
        }
        
        # Check keywords in description
        if target_keywords:
            for keyword in target_keywords:
                if keyword.lower() in description.lower():
                    analysis['description_optimization']['keyword_in_description'] = True
                    break
            
            if not analysis['description_optimization']['keyword_in_description']:
                analysis['improvements'].append('Include target keyword in meta description')
                analysis['score'] -= 10
        
        # Description length optimization
        if desc_length < 120:
            analysis['improvements'].append('Meta description is too short')
            analysis['score'] -= 10
        elif desc_length > 180:
            analysis['improvements'].append('Meta description is too long - may be truncated')
            analysis['score'] -= 5
        else:
            analysis['score'] += 15
        
        return analysis
    
    def _optimize_schema_markup(self, post: Dict[str, Any], 
                               target_keywords: List[str] = None) -> Dict[str, Any]:
        """Generate and optimize Schema.org markup."""
        analysis = {
            'article_schema': {},
            'breadcrumb_schema': {},
            'improvements': [],
            'score': 60  # Default score
        }
        
        # Generate Article schema
        post_title = post.get('title', {}).get('rendered', 'Untitled')
        content = post.get('content', {}).get('rendered', '')
        post_url = post.get('link', '')
        
        # Extract publish and modified dates
        date_published = post.get('date', datetime.now().isoformat())
        date_modified = post.get('modified', date_published)
        
        # Create Article schema
        article_schema = self.schema_templates['Article'].copy()
        article_schema['headline'] = post_title[:110]  # Google truncates at ~110 chars
        article_schema['datePublished'] = date_published
        article_schema['dateModified'] = date_modified
        article_schema['mainEntityOfPage']['@id'] = post_url
        
        # Generate description from content
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text()
        description = ' '.join(text_content.split()[:25])  # First 25 words
        article_schema['description'] = description
        
        # Add author information (would be enhanced with actual author data)
        article_schema['author']['name'] = 'SphereVista360 Team'
        
        analysis['article_schema'] = article_schema
        analysis['score'] += 25
        analysis['improvements'].append('Generated comprehensive Article schema markup')
        
        # Generate Breadcrumb schema
        breadcrumb_schema = self._generate_breadcrumb_schema(post_url, post_title)
        if breadcrumb_schema:
            analysis['breadcrumb_schema'] = breadcrumb_schema
            analysis['score'] += 15
            analysis['improvements'].append('Generated breadcrumb navigation schema')
        
        return analysis
    
    def _optimize_internal_linking(self, soup: BeautifulSoup, post_id: int, 
                                  auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize internal linking structure."""
        analysis = {
            'current_internal_links': 0,
            'suggested_links': [],
            'link_opportunities': [],
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Count existing internal links
        links = soup.find_all('a', href=True)
        internal_links = [link for link in links if self._is_internal_link(link.get('href', ''))]
        analysis['current_internal_links'] = len(internal_links)
        
        # Analyze content for linking opportunities
        content_text = soup.get_text().lower()
        
        # Get related posts for internal linking
        try:
            all_posts = self.wp.get_posts(per_page=50)
            related_posts = []
            
            for other_post in all_posts:
                if other_post['id'] == post_id:
                    continue
                
                other_title = other_post.get('title', {}).get('rendered', '').lower()
                other_url = other_post.get('link', '')
                
                # Simple relevance check based on title words in content
                title_words = other_title.split()
                relevance_score = sum(1 for word in title_words if word in content_text and len(word) > 3)
                
                if relevance_score >= 2:  # At least 2 relevant words
                    related_posts.append({
                        'id': other_post['id'],
                        'title': other_post.get('title', {}).get('rendered', ''),
                        'url': other_url,
                        'relevance': relevance_score
                    })
            
            # Sort by relevance and take top 5
            related_posts.sort(key=lambda x: x['relevance'], reverse=True)
            analysis['suggested_links'] = related_posts[:5]
            
            if auto_apply and related_posts:
                # Add internal links to content (simplified implementation)
                analysis['link_opportunities'] = self._add_internal_links(soup, related_posts[:3])
                analysis['score'] += 15
                
        except Exception:
            analysis['improvements'].append('Unable to fetch related posts for internal linking')
        
        # Scoring based on internal link density
        content_length = len(content_text.split())
        if content_length > 300:
            ideal_links = max(2, content_length // 150)  # ~1 link per 150 words
            
            if analysis['current_internal_links'] == 0:
                analysis['improvements'].append('Add internal links to improve SEO and user navigation')
                analysis['score'] -= 20
            elif analysis['current_internal_links'] < ideal_links:
                analysis['improvements'].append(f'Consider adding {ideal_links - analysis["current_internal_links"]} more internal links')
                analysis['score'] -= 10
        
        return analysis
    
    def _optimize_content_seo(self, soup: BeautifulSoup, target_keywords: List[str] = None, 
                             auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize content structure and keyword usage for SEO."""
        analysis = {
            'heading_structure': {},
            'keyword_optimization': {},
            'content_structure': {},
            'improvements': [],
            'score': 75  # Default score
        }
        
        # Analyze heading structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        h1_count = len(soup.find_all('h1'))
        
        analysis['heading_structure'] = {
            'total_headings': len(headings),
            'h1_count': h1_count,
            'proper_hierarchy': True
        }
        
        # Check H1 optimization
        if h1_count == 0:
            analysis['improvements'].append('Add H1 heading for main topic')
            analysis['score'] -= 15
        elif h1_count > 1:
            analysis['improvements'].append('Use only one H1 heading per page')
            analysis['score'] -= 10
        
        # Check heading hierarchy
        prev_level = 0
        for heading in headings:
            level = int(heading.name[1])
            if prev_level > 0 and level > prev_level + 1:
                analysis['heading_structure']['proper_hierarchy'] = False
                break
            prev_level = level
        
        if not analysis['heading_structure']['proper_hierarchy']:
            analysis['improvements'].append('Fix heading hierarchy - avoid skipping heading levels')
            analysis['score'] -= 10
        
        # Analyze keyword optimization
        if target_keywords:
            content_text = soup.get_text().lower()
            
            for keyword in target_keywords:
                keyword_lower = keyword.lower()
                keyword_count = content_text.count(keyword_lower)
                
                # Check keyword in headings
                keyword_in_headings = any(keyword_lower in heading.get_text().lower() for heading in headings)
                
                analysis['keyword_optimization'][keyword] = {
                    'count': keyword_count,
                    'in_headings': keyword_in_headings
                }
                
                if keyword_count == 0:
                    analysis['improvements'].append(f'Include target keyword "{keyword}" in content')
                    analysis['score'] -= 15
                elif not keyword_in_headings:
                    analysis['improvements'].append(f'Include keyword "{keyword}" in headings')
                    analysis['score'] -= 5
        
        # Analyze content structure
        paragraphs = soup.find_all('p')
        lists = soup.find_all(['ul', 'ol'])
        
        analysis['content_structure'] = {
            'paragraph_count': len(paragraphs),
            'list_count': len(lists),
            'has_intro': bool(paragraphs),
            'scannable': len(lists) > 0 or len(headings) > 2
        }
        
        if len(paragraphs) > 5 and len(lists) == 0:
            analysis['improvements'].append('Add bullet points or numbered lists for better readability')
            analysis['score'] -= 5
        
        return analysis
    
    def _optimize_url_structure(self, post_url: str, post_title: str) -> Dict[str, Any]:
        """Analyze and suggest URL structure improvements."""
        analysis = {
            'current_url': post_url,
            'url_length': len(post_url),
            'suggested_improvements': [],
            'improvements': [],
            'score': 80  # Default score
        }
        
        parsed_url = urlparse(post_url)
        path = parsed_url.path
        
        # Check URL length
        if len(path) > 75:
            analysis['improvements'].append('URL is too long - consider shorter, descriptive URLs')
            analysis['score'] -= 10
        
        # Check for stop words in URL
        stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with']
        path_words = re.findall(r'\b\w+\b', path.lower())
        
        if any(word in stop_words for word in path_words):
            analysis['improvements'].append('Remove stop words from URL for better SEO')
            analysis['score'] -= 5
        
        # Check for numbers/dates in URL (can become outdated)
        if re.search(r'\d{4}', path):  # Year in URL
            analysis['improvements'].append('Consider removing dates from URLs to avoid content appearing outdated')
            analysis['score'] -= 5
        
        return analysis
    
    def _optimize_technical_seo(self, soup: BeautifulSoup, post_url: str, 
                               auto_apply: bool = False) -> Dict[str, Any]:
        """Optimize technical SEO elements."""
        analysis = {
            'canonical_url': None,
            'meta_robots': None,
            'open_graph': {},
            'twitter_cards': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Add canonical URL if missing
        canonical = soup.find('link', rel='canonical')
        if canonical:
            analysis['canonical_url'] = canonical.get('href')
        else:
            analysis['improvements'].append('Add canonical URL to prevent duplicate content issues')
            analysis['score'] -= 10
            
            if auto_apply:
                # Add canonical tag (would need to be in <head>)
                analysis['canonical_url'] = post_url
        
        # Check meta robots
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        if robots_meta:
            analysis['meta_robots'] = robots_meta.get('content')
        
        # Generate Open Graph tags
        analysis['open_graph'] = self._generate_open_graph_tags(soup, post_url)
        analysis['score'] += 10
        
        # Generate Twitter Card tags
        analysis['twitter_cards'] = self._generate_twitter_card_tags(soup, post_url)
        analysis['score'] += 10
        
        return analysis
    
    def _generate_optimized_seo_content(self, post: Dict[str, Any], soup: BeautifulSoup,
                                       seo_optimization: Dict[str, Any], 
                                       target_keywords: List[str] = None) -> Dict[str, Any]:
        """Generate optimized content with SEO improvements applied."""
        optimized = {
            'title': post.get('title', {}).get('rendered', ''),
            'content': str(soup),
            'excerpt': post.get('excerpt', {}).get('rendered', ''),
            'meta_description': '',
            'schema_markup': {},
            'internal_links_added': []
        }
        
        # Apply meta tag optimizations
        meta_opt = seo_optimization.get('meta_tags', {})
        if 'title_optimization' in meta_opt:
            optimized['title'] = meta_opt['title_optimization'].get('optimized_title', optimized['title'])
        
        if 'description_optimization' in meta_opt:
            optimized['meta_description'] = meta_opt['description_optimization'].get('optimized_description', '')
        
        # Apply schema markup
        schema_opt = seo_optimization.get('schema_markup', {})
        if 'article_schema' in schema_opt:
            optimized['schema_markup']['article'] = schema_opt['article_schema']
        
        if 'breadcrumb_schema' in schema_opt:
            optimized['schema_markup']['breadcrumb'] = schema_opt['breadcrumb_schema']
        
        # Apply internal linking improvements
        internal_opt = seo_optimization.get('internal_linking', {})
        if 'link_opportunities' in internal_opt:
            optimized['internal_links_added'] = internal_opt['link_opportunities']
        
        return optimized
    
    def _generate_meta_description_from_content(self, content: str, 
                                               target_keywords: List[str] = None) -> str:
        """Generate optimized meta description from content."""
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        
        # Get first meaningful sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        description = ''
        
        # Try to include target keyword in description
        if target_keywords:
            primary_keyword = target_keywords[0]
            for sentence in sentences:
                if primary_keyword.lower() in sentence.lower():
                    if len(sentence) <= 155:
                        return sentence
                    else:
                        # Truncate but try to keep keyword
                        words = sentence.split()
                        truncated = ''
                        for word in words:
                            if len(truncated + ' ' + word) <= 150:
                                truncated += ' ' + word if truncated else word
                            else:
                                break
                        return truncated + '...'
        
        # Fallback: use first sentences up to 155 characters
        for sentence in sentences:
            if len(description + sentence) < 150:
                description += sentence + '. '
            else:
                break
        
        return description.strip() or text[:150] + '...'
    
    def _generate_breadcrumb_schema(self, post_url: str, post_title: str) -> Dict[str, Any]:
        """Generate breadcrumb schema markup."""
        breadcrumb = self.schema_templates['BreadcrumbList'].copy()
        
        # Simple breadcrumb based on URL structure
        parsed_url = urlparse(post_url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        
        breadcrumb_items = []
        current_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Home page
        breadcrumb_items.append({
            '@type': 'ListItem',
            'position': 1,
            'name': 'Home',
            'item': current_url
        })
        
        # Add path components
        for i, part in enumerate(path_parts[:-1], 2):
            current_url += '/' + part
            breadcrumb_items.append({
                '@type': 'ListItem',
                'position': i,
                'name': part.replace('-', ' ').title(),
                'item': current_url
            })
        
        # Current page
        breadcrumb_items.append({
            '@type': 'ListItem',
            'position': len(breadcrumb_items) + 1,
            'name': post_title,
            'item': post_url
        })
        
        breadcrumb['itemListElement'] = breadcrumb_items
        return breadcrumb
    
    def _generate_open_graph_tags(self, soup: BeautifulSoup, post_url: str) -> Dict[str, str]:
        """Generate Open Graph meta tags."""
        title = soup.find('title')
        title_text = title.get_text() if title else 'SphereVista360'
        
        # Find first image
        first_image = soup.find('img')
        image_url = ''
        if first_image and first_image.get('src'):
            img_src = first_image.get('src')
            if img_src.startswith('/'):
                image_url = urljoin(self.base_url, img_src)
            else:
                image_url = img_src
        
        return {
            'og:title': title_text,
            'og:type': 'article',
            'og:url': post_url,
            'og:image': image_url,
            'og:site_name': 'SphereVista360'
        }
    
    def _generate_twitter_card_tags(self, soup: BeautifulSoup, post_url: str) -> Dict[str, str]:
        """Generate Twitter Card meta tags."""
        title = soup.find('title')
        title_text = title.get_text() if title else 'SphereVista360'
        
        return {
            'twitter:card': 'summary_large_image',
            'twitter:title': title_text,
            'twitter:url': post_url,
            'twitter:site': '@spherevista360'
        }
    
    def _is_internal_link(self, href: str) -> bool:
        """Check if a link is internal."""
        if not href:
            return False
        
        # Relative links are internal
        if href.startswith('/') or not href.startswith('http'):
            return True
        
        # Check if domain matches
        parsed_href = urlparse(href)
        parsed_base = urlparse(self.base_url)
        
        return parsed_href.netloc == parsed_base.netloc
    
    def _add_internal_links(self, soup: BeautifulSoup, related_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add internal links to content."""
        opportunities = []
        content_text = soup.get_text().lower()
        
        for post in related_posts:
            post_title = post['title'].lower()
            post_url = post['url']
            
            # Find first occurrence of title words in content
            title_words = post_title.split()
            for i in range(len(title_words) - 1):
                phrase = ' '.join(title_words[i:i+2])
                if phrase in content_text and len(phrase) > 5:
                    opportunities.append({
                        'phrase': phrase,
                        'url': post_url,
                        'title': post['title']
                    })
                    break
        
        return opportunities