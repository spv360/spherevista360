"""
Content Optimization Engine
===========================
AI-powered content optimization for WordPress sites including:
- Automated content analysis and improvement suggestions
- Readability optimization and enhancement
- SEO content optimization algorithms
- Keyword density and distribution optimization
- Content structure and formatting improvements
- Meta description and title generation
"""

import re
import math
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import statistics
from bs4 import BeautifulSoup, Tag

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class ContentOptimizer:
    """Advanced content optimization utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize content optimizer."""
        self.wp = wp_client or WordPressClient()
        
        # Content optimization parameters
        self.target_reading_level = 8  # Grade level (Flesch-Kincaid)
        self.ideal_sentence_length = 20  # Words per sentence
        self.ideal_paragraph_length = 150  # Words per paragraph
        self.min_content_length = 300  # Minimum words for SEO
        self.max_keyword_density = 0.03  # 3% maximum keyword density
        
        # Common stop words for analysis
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
    
    def optimize_content(self, post_id: int, target_keywords: List[str] = None, 
                        auto_apply: bool = False) -> Dict[str, Any]:
        """Comprehensive content optimization for a specific post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post.get('title', {}).get('rendered', 'Untitled')
            content = post.get('content', {}).get('rendered', '')
            excerpt = post.get('excerpt', {}).get('rendered', '')
            
            result = {
                'post_id': post_id,
                'post_title': post_title,
                'original_content_length': len(content),
                'optimization': {
                    'readability': {'score': 0, 'improvements': []},
                    'seo_content': {'score': 0, 'improvements': []},
                    'structure': {'score': 0, 'improvements': []},
                    'keywords': {'score': 0, 'improvements': []},
                    'meta_optimization': {'score': 0, 'improvements': []}
                },
                'optimized_content': {
                    'title': post_title,
                    'content': content,
                    'excerpt': excerpt,
                    'meta_description': '',
                    'focus_keywords': target_keywords or []
                },
                'improvements_summary': [],
                'score': 0
            }
            
            if not content:
                result['optimization']['seo_content']['improvements'].append('No content to optimize')
                return result
            
            # Parse content for analysis
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()
            
            # Run optimization analyses
            result['optimization']['readability'] = self._optimize_readability(text_content, soup)
            result['optimization']['seo_content'] = self._optimize_seo_content(text_content, target_keywords)
            result['optimization']['structure'] = self._optimize_content_structure(soup)
            result['optimization']['keywords'] = self._optimize_keyword_usage(text_content, target_keywords)
            result['optimization']['meta_optimization'] = self._optimize_meta_elements(post_title, text_content, excerpt)
            
            # Generate optimized content
            if auto_apply:
                result['optimized_content'] = self._generate_optimized_content(
                    soup, result['optimization'], target_keywords
                )
            
            # Calculate overall optimization score
            scores = [section['score'] for section in result['optimization'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all improvements
            all_improvements = []
            for section_name, section_data in result['optimization'].items():
                if section_data['improvements']:
                    all_improvements.extend([f"{section_name.title()}: {imp}" for imp in section_data['improvements']])
            
            result['improvements_summary'] = all_improvements
            
            # Set status based on score
            if result['score'] >= 85:
                result['status'] = 'excellent'
                result['message'] = 'Content is well optimized'
            elif result['score'] >= 70:
                result['status'] = 'good'
                result['message'] = 'Content has good optimization'
            elif result['score'] >= 50:
                result['status'] = 'fair'
                result['message'] = 'Content needs optimization improvements'
            else:
                result['status'] = 'poor'
                result['message'] = 'Content requires significant optimization'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Error optimizing content: {str(e)}'
            }
    
    def _optimize_readability(self, text: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Optimize content readability using various metrics."""
        analysis = {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0,
            'avg_sentence_length': 0,
            'avg_syllables_per_word': 0,
            'complex_words': 0,
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Clean text for analysis
        sentences = self._split_into_sentences(text)
        words = self._extract_words(text)
        
        if not sentences or not words:
            analysis['improvements'].append('Content too short for readability analysis')
            analysis['score'] = 30
            return analysis
        
        # Calculate readability metrics
        total_sentences = len(sentences)
        total_words = len(words)
        total_syllables = sum(self._count_syllables(word) for word in words)
        
        analysis['avg_sentence_length'] = total_words / total_sentences
        analysis['avg_syllables_per_word'] = total_syllables / total_words
        
        # Flesch Reading Ease
        analysis['flesch_reading_ease'] = (
            206.835 - 1.015 * (total_words / total_sentences) - 
            84.6 * (total_syllables / total_words)
        )
        
        # Flesch-Kincaid Grade Level
        analysis['flesch_kincaid_grade'] = (
            0.39 * (total_words / total_sentences) + 
            11.8 * (total_syllables / total_words) - 15.59
        )
        
        # Complex words (3+ syllables)
        analysis['complex_words'] = sum(1 for word in words if self._count_syllables(word) >= 3)
        complex_word_ratio = analysis['complex_words'] / total_words
        
        # Generate improvements based on analysis
        if analysis['avg_sentence_length'] > 25:
            analysis['improvements'].append(f'Average sentence length is {analysis["avg_sentence_length"]:.1f} words - consider shorter sentences')
            analysis['score'] -= 10
        
        if analysis['flesch_kincaid_grade'] > 12:
            analysis['improvements'].append(f'Reading level is grade {analysis["flesch_kincaid_grade"]:.1f} - simplify language for broader audience')
            analysis['score'] -= 15
        
        if complex_word_ratio > 0.15:  # More than 15% complex words
            analysis['improvements'].append(f'{analysis["complex_words"]} complex words found - consider simpler alternatives')
            analysis['score'] -= 10
        
        if analysis['flesch_reading_ease'] < 60:
            analysis['improvements'].append('Text is difficult to read - use shorter sentences and simpler words')
            analysis['score'] -= 10
        
        # Check paragraph structure
        paragraphs = soup.find_all('p')
        long_paragraphs = 0
        for p in paragraphs:
            p_text = p.get_text()
            p_words = self._extract_words(p_text)
            if len(p_words) > 200:  # Very long paragraph
                long_paragraphs += 1
        
        if long_paragraphs > 0:
            analysis['improvements'].append(f'{long_paragraphs} paragraphs are too long - break into shorter sections')
            analysis['score'] -= 5
        
        return analysis
    
    def _optimize_seo_content(self, text: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Optimize content for SEO performance."""
        analysis = {
            'word_count': 0,
            'keyword_density': {},
            'keyword_distribution': {},
            'content_depth': 0,
            'improvements': [],
            'score': 80  # Default score
        }
        
        words = self._extract_words(text)
        analysis['word_count'] = len(words)
        
        # Check minimum content length
        if analysis['word_count'] < self.min_content_length:
            analysis['improvements'].append(f'Content is {analysis["word_count"]} words - add {self.min_content_length - analysis["word_count"]} more words for better SEO')
            analysis['score'] -= 20
        
        # Analyze target keywords if provided
        if target_keywords:
            for keyword in target_keywords:
                keyword_lower = keyword.lower()
                keyword_count = text.lower().count(keyword_lower)
                density = keyword_count / analysis['word_count'] if analysis['word_count'] > 0 else 0
                
                analysis['keyword_density'][keyword] = {
                    'count': keyword_count,
                    'density': density
                }
                
                # Check keyword density
                if density == 0:
                    analysis['improvements'].append(f'Target keyword "{keyword}" not found in content')
                    analysis['score'] -= 15
                elif density < 0.005:  # Less than 0.5%
                    analysis['improvements'].append(f'Keyword "{keyword}" density is low ({density:.1%}) - consider adding more mentions')
                    analysis['score'] -= 10
                elif density > self.max_keyword_density:
                    analysis['improvements'].append(f'Keyword "{keyword}" density is high ({density:.1%}) - may be over-optimized')
                    analysis['score'] -= 10
        
        # Analyze content depth (unique word ratio)
        unique_words = len(set(word.lower() for word in words if word.lower() not in self.stop_words))
        analysis['content_depth'] = unique_words / analysis['word_count'] if analysis['word_count'] > 0 else 0
        
        if analysis['content_depth'] < 0.3:  # Less than 30% unique words
            analysis['improvements'].append('Content has low lexical diversity - add more varied vocabulary')
            analysis['score'] -= 10
        
        return analysis
    
    def _optimize_content_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Optimize content structure and formatting."""
        analysis = {
            'heading_structure': {},
            'list_usage': 0,
            'image_distribution': 0,
            'internal_links': 0,
            'improvements': [],
            'score': 75  # Default score
        }
        
        # Analyze heading structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            level = heading.name
            analysis['heading_structure'][level] = analysis['heading_structure'].get(level, 0) + 1
        
        # Check heading hierarchy
        if not headings:
            analysis['improvements'].append('Add headings to improve content structure')
            analysis['score'] -= 15
        elif 'h1' not in analysis['heading_structure']:
            analysis['improvements'].append('Add H1 heading for main topic')
            analysis['score'] -= 10
        elif 'h2' not in analysis['heading_structure'] and len(headings) > 1:
            analysis['improvements'].append('Use H2 headings to break content into sections')
            analysis['score'] -= 5
        
        # Analyze list usage
        lists = soup.find_all(['ul', 'ol'])
        analysis['list_usage'] = len(lists)
        
        # Check for scannable content
        text_length = len(soup.get_text())
        if text_length > 1000 and analysis['list_usage'] == 0:
            analysis['improvements'].append('Add bullet points or numbered lists to improve scannability')
            analysis['score'] -= 10
        
        # Analyze image distribution
        images = soup.find_all('img')
        analysis['image_distribution'] = len(images)
        
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 5 and analysis['image_distribution'] == 0:
            analysis['improvements'].append('Add images to break up text and improve engagement')
            analysis['score'] -= 10
        
        # Analyze internal linking
        links = soup.find_all('a', href=True)
        internal_links = [link for link in links if not link.get('href', '').startswith('http')]
        analysis['internal_links'] = len(internal_links)
        
        if text_length > 500 and analysis['internal_links'] == 0:
            analysis['improvements'].append('Add internal links to improve SEO and user navigation')
            analysis['score'] -= 10
        
        return analysis
    
    def _optimize_keyword_usage(self, text: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Optimize keyword usage and semantic relevance."""
        analysis = {
            'keyword_placement': {},
            'semantic_keywords': [],
            'keyword_variations': {},
            'improvements': [],
            'score': 80  # Default score
        }
        
        if not target_keywords:
            analysis['improvements'].append('Define target keywords for better optimization')
            analysis['score'] = 60
            return analysis
        
        text_lower = text.lower()
        
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            
            # Check keyword placement in different sections
            first_100_words = ' '.join(text.split()[:100]).lower()
            last_100_words = ' '.join(text.split()[-100:]).lower()
            
            placement = {
                'first_100_words': keyword_lower in first_100_words,
                'last_100_words': keyword_lower in last_100_words,
                'throughout_content': keyword_lower in text_lower
            }
            
            analysis['keyword_placement'][keyword] = placement
            
            # Generate improvement suggestions
            if not placement['first_100_words']:
                analysis['improvements'].append(f'Include "{keyword}" in the first paragraph')
                analysis['score'] -= 5
            
            if not placement['throughout_content']:
                analysis['improvements'].append(f'Use "{keyword}" naturally throughout the content')
                analysis['score'] -= 10
            
            # Look for keyword variations
            variations = self._find_keyword_variations(keyword, text)
            analysis['keyword_variations'][keyword] = variations
            
            if len(variations) < 2:
                analysis['improvements'].append(f'Use variations of "{keyword}" for natural language')
                analysis['score'] -= 5
        
        return analysis
    
    def _optimize_meta_elements(self, title: str, content: str, excerpt: str) -> Dict[str, Any]:
        """Optimize meta elements like title and description."""
        analysis = {
            'title_optimization': {},
            'description_optimization': {},
            'generated_meta': {},
            'improvements': [],
            'score': 70  # Default score
        }
        
        # Analyze title
        title_length = len(title)
        analysis['title_optimization'] = {
            'length': title_length,
            'word_count': len(title.split()),
            'optimal_length': 50 <= title_length <= 60
        }
        
        if title_length < 30:
            analysis['improvements'].append('Title is too short - expand for better SEO')
            analysis['score'] -= 15
        elif title_length > 70:
            analysis['improvements'].append('Title is too long - may be truncated in search results')
            analysis['score'] -= 10
        else:
            analysis['score'] += 10
        
        # Analyze/generate meta description
        if excerpt:
            description = excerpt
        else:
            # Generate meta description from content
            description = self._generate_meta_description(content)
            analysis['improvements'].append('Generated meta description from content')
        
        desc_length = len(description)
        analysis['description_optimization'] = {
            'length': desc_length,
            'word_count': len(description.split()),
            'optimal_length': 140 <= desc_length <= 160
        }
        
        if desc_length < 120:
            analysis['improvements'].append('Meta description is too short - expand for better click-through rates')
            analysis['score'] -= 10
        elif desc_length > 180:
            analysis['improvements'].append('Meta description is too long - may be truncated')
            analysis['score'] -= 5
        else:
            analysis['score'] += 15
        
        analysis['generated_meta'] = {
            'title': title,
            'description': description
        }
        
        return analysis
    
    def _generate_optimized_content(self, soup: BeautifulSoup, optimization: Dict[str, Any], 
                                   target_keywords: List[str] = None) -> Dict[str, Any]:
        """Generate optimized version of content based on analysis."""
        optimized = {
            'title': '',
            'content': '',
            'excerpt': '',
            'meta_description': '',
            'focus_keywords': target_keywords or []
        }
        
        # Get base content
        optimized['content'] = str(soup)
        
        # Apply structural improvements
        if optimization['structure']['score'] < 70:
            optimized['content'] = self._improve_content_structure(soup, optimization['structure'])
        
        # Generate optimized meta description
        meta_opt = optimization['meta_optimization']
        if 'generated_meta' in meta_opt:
            optimized['meta_description'] = meta_opt['generated_meta']['description']
        
        return optimized
    
    def _improve_content_structure(self, soup: BeautifulSoup, structure_analysis: Dict[str, Any]) -> str:
        """Apply structural improvements to content."""
        # This is a simplified implementation
        # In a full implementation, this would apply various structural improvements
        
        # Add heading suggestions as comments
        if not structure_analysis.get('heading_structure'):
            # Add a comment suggesting headings
            comment = soup.new_string('\n<!-- Consider adding H2 headings to break up content sections -->\n')
            if soup.find('p'):
                soup.find('p').insert_before(comment)
        
        return str(soup)
    
    def _generate_meta_description(self, content: str) -> str:
        """Generate an optimized meta description from content."""
        # Remove HTML tags
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        
        # Get first meaningful sentences
        sentences = self._split_into_sentences(text)
        description = ''
        
        for sentence in sentences:
            if len(description + sentence) < 150:
                description += sentence + ' '
            else:
                break
        
        return description.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text."""
        # Remove HTML and extract words
        soup = BeautifulSoup(text, 'html.parser')
        clean_text = soup.get_text()
        words = re.findall(r'\b[a-zA-Z]+\b', clean_text.lower())
        return words
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent e
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _find_keyword_variations(self, keyword: str, text: str) -> List[str]:
        """Find variations of a keyword in text."""
        # Simple implementation - would be enhanced with NLP libraries
        variations = []
        keyword_lower = keyword.lower()
        
        # Look for plural forms
        if keyword_lower + 's' in text.lower():
            variations.append(keyword + 's')
        
        # Look for different word order (for multi-word keywords)
        if ' ' in keyword:
            words = keyword.split()
            if len(words) == 2:
                reversed_keyword = f"{words[1]} {words[0]}"
                if reversed_keyword.lower() in text.lower():
                    variations.append(reversed_keyword)
        
        return variations