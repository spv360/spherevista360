"""
Content Quality Enhancement
===========================
Content quality enhancement utilities for WordPress posts.
"""

import re
import requests
from typing import Dict, List, Any, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import statistics

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class ContentQualityEnhancer:
    """Content quality enhancement and optimization."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize content quality enhancer."""
        self.wp = wp_client
        
        # Quality scoring weights
        self.quality_weights = {
            'word_count': 0.25,
            'readability': 0.20,
            'structure': 0.20,
            'links': 0.15,
            'images': 0.10,
            'headings': 0.10
        }
        
        # Content guidelines
        self.min_word_count = 300
        self.optimal_word_count = 1000
        self.max_word_count = 3000
        
    def analyze_content_quality(self, post_id: int) -> Dict[str, Any]:
        """Comprehensive content quality analysis."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            if 'raw' in post.get('content', {}):
                content = post['content']['raw']
                rendered_content = post['content']['rendered']
            else:
                content = post['content']['rendered']
                rendered_content = content
            
            soup = BeautifulSoup(rendered_content, 'html.parser')
            text = soup.get_text()
            
            # Basic metrics
            word_count = len(text.split())
            char_count = len(text)
            
            # Structure analysis
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            paragraphs = soup.find_all('p')
            lists = soup.find_all(['ul', 'ol'])
            images = soup.find_all('img')
            links = soup.find_all('a')
            
            # Readability analysis
            readability_score = self._calculate_readability_score(text)
            
            # Content structure score
            structure_score = self._analyze_content_structure(soup, word_count)
            
            # Link analysis
            internal_links = []
            external_links = []
            for link in links:
                href = link.get('href', '')
                if href:
                    if any(domain in href for domain in ['spherevista360.com', 'localhost']):
                        internal_links.append(href)
                    elif href.startswith('http'):
                        external_links.append(href)
            
            # Calculate overall quality score
            scores = {
                'word_count': self._score_word_count(word_count),
                'readability': readability_score,
                'structure': structure_score,
                'links': self._score_links(len(internal_links), len(external_links), word_count),
                'images': self._score_images(len(images), word_count),
                'headings': self._score_headings(len(headings), word_count)
            }
            
            overall_score = sum(scores[key] * self.quality_weights[key] for key in scores)
            
            return {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'overall_score': round(overall_score, 2),
                'grade': self._get_grade(overall_score),
                'metrics': {
                    'word_count': word_count,
                    'char_count': char_count,
                    'headings_count': len(headings),
                    'paragraphs_count': len(paragraphs),
                    'lists_count': len(lists),
                    'images_count': len(images),
                    'internal_links_count': len(internal_links),
                    'external_links_count': len(external_links)
                },
                'scores': scores,
                'headings': [{'tag': h.name, 'text': h.get_text()[:50]} for h in headings],
                'recommendations': self._get_recommendations(scores, overall_score),
                'issues': self._identify_issues(scores, word_count, len(headings), len(internal_links))
            }
            
        except Exception as e:
            return {
                'post_id': post_id,
                'error': str(e)
            }

    def enhance_content_structure(self, post_id: int, dry_run: bool = False) -> Dict[str, Any]:
        """Enhance content structure by adding headings and improving formatting."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            if 'raw' in post.get('content', {}):
                content = post['content']['raw']
            else:
                content = post['content']['rendered']
            
            original_content = content
            enhanced_content = content
            improvements = []
            
            # Parse content
            soup = BeautifulSoup(content, 'html.parser')
            
            # Add missing headings if content is long
            text = soup.get_text()
            word_count = len(text.split())
            
            if word_count > 500:
                paragraphs = soup.find_all('p')
                if len(paragraphs) > 4 and not soup.find_all(['h2', 'h3']):
                    # Try to identify potential headings
                    potential_headings = self._identify_potential_headings(paragraphs)
                    
                    for p, heading_text in potential_headings:
                        if len(heading_text.split()) <= 8:  # Reasonable heading length
                            new_heading = soup.new_tag('h2')
                            new_heading.string = heading_text
                            p.replace_with(new_heading)
                            improvements.append(f"Added H2 heading: {heading_text[:30]}...")
            
            # Improve paragraph structure
            long_paragraphs = soup.find_all('p')
            for p in long_paragraphs:
                p_text = p.get_text()
                if len(p_text) > 200:  # Long paragraph
                    # Try to split on sentences
                    sentences = re.split(r'[.!?]+', p_text)
                    if len(sentences) > 4:
                        improvements.append(f"Identified long paragraph for potential splitting")
            
            # Add introduction paragraph if missing
            if word_count > 300:
                first_p = soup.find('p')
                if first_p and len(first_p.get_text()) < 50:
                    improvements.append("Consider adding a more substantial introduction paragraph")
            
            enhanced_content = str(soup)
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'improvements': improvements,
                'changes_made': len(improvements) > 0
            }
            
            if not improvements:
                result['message'] = 'Content structure is already well-organized'
                return result
            
            if dry_run:
                result['message'] = f'Would apply {len(improvements)} structure improvements'
                return result
            
            # Update post if changes were made
            if enhanced_content != original_content:
                update_data = {'content': enhanced_content}
                self.wp.update_post(post_id, update_data)
                result['success'] = True
                result['message'] = f'Applied {len(improvements)} structure improvements'
            else:
                result['message'] = 'No structural changes needed'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def add_internal_links(self, post_id: int, max_links: int = 3, dry_run: bool = False) -> Dict[str, Any]:
        """Add relevant internal links to improve SEO and user experience."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            if 'raw' in post.get('content', {}):
                content = post['content']['raw']
            else:
                content = post['content']['rendered']
            
            # Get post categories for finding related content
            categories = post.get('categories', [])
            
            # Find potential link targets
            related_posts = self._find_related_posts(post_id, categories, max_links * 2)
            
            if not related_posts:
                return {
                    'post_id': post_id,
                    'message': 'No related posts found for internal linking'
                }
            
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text().lower()
            
            links_added = []
            
            # Try to add links for related posts
            for related_post in related_posts[:max_links]:
                post_title = related_post.get('title', {}).get('rendered', '')
                post_link = related_post.get('link', '')
                
                # Find potential anchor text
                title_words = post_title.lower().split()
                if len(title_words) >= 2:
                    # Look for partial matches in content
                    for i in range(len(title_words) - 1):
                        phrase = ' '.join(title_words[i:i+2])
                        if phrase in text and len(phrase) > 4:
                            # Add link if not already linked
                            if post_link not in content:
                                # Find the text node and add link
                                paragraphs = soup.find_all('p')
                                for p in paragraphs:
                                    p_text = p.get_text().lower()
                                    if phrase in p_text:
                                        # Replace first occurrence
                                        original_phrase = self._find_original_case(p.get_text(), phrase)
                                        if original_phrase:
                                            p.string = p.get_text().replace(
                                                original_phrase,
                                                f'<a href="{post_link}">{original_phrase}</a>',
                                                1
                                            )
                                            links_added.append({
                                                'anchor_text': original_phrase,
                                                'url': post_link,
                                                'target_title': post_title
                                            })
                                            break
                                break
                
                if len(links_added) >= max_links:
                    break
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'links_added': links_added,
                'changes_made': len(links_added) > 0
            }
            
            if not links_added:
                result['message'] = 'No suitable anchor text found for internal linking'
                return result
            
            if dry_run:
                result['message'] = f'Would add {len(links_added)} internal links'
                return result
            
            # Update post
            enhanced_content = str(soup)
            update_data = {'content': enhanced_content}
            self.wp.update_post(post_id, update_data)
            
            result.update({
                'success': True,
                'message': f'Added {len(links_added)} internal links'
            })
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def bulk_content_enhancement(self, post_ids: List[int] = None, per_page: int = 10, dry_run: bool = False) -> Dict[str, Any]:
        """Apply bulk content quality enhancements."""
        try:
            if post_ids:
                posts_to_enhance = [{'id': pid} for pid in post_ids]
            else:
                # Get posts with low quality scores
                posts_to_enhance = self.wp.get_posts(
                    status='publish',
                    per_page=per_page,
                    orderby='date',
                    order='desc'
                )
            
            results = {
                'total_posts': len(posts_to_enhance),
                'posts_processed': [],
                'posts_enhanced': [],
                'total_improvements': 0,
                'errors': []
            }
            
            for post in posts_to_enhance:
                post_id = post['id']
                post_improvements = []
                
                try:
                    # Analyze current quality
                    quality_analysis = self.analyze_content_quality(post_id)
                    
                    # Skip if already high quality
                    if quality_analysis.get('overall_score', 0) >= 80:
                        continue
                    
                    # Enhance structure
                    structure_result = self.enhance_content_structure(post_id, dry_run=dry_run)
                    if structure_result.get('success', False):
                        post_improvements.extend(structure_result.get('improvements', []))
                    
                    # Add internal links
                    links_result = self.add_internal_links(post_id, dry_run=dry_run)
                    if links_result.get('success', False):
                        post_improvements.append(f"Added {len(links_result.get('links_added', []))} internal links")
                    
                    results['posts_processed'].append({
                        'post_id': post_id,
                        'initial_score': quality_analysis.get('overall_score', 0),
                        'improvements': post_improvements,
                        'structure_result': structure_result,
                        'links_result': links_result
                    })
                    
                    if post_improvements:
                        results['posts_enhanced'].append(post_id)
                        results['total_improvements'] += len(post_improvements)
                    
                except Exception as e:
                    results['errors'].append({
                        'post_id': post_id,
                        'error': str(e)
                    })
            
            results.update({
                'posts_enhanced_count': len(results['posts_enhanced']),
                'errors_count': len(results['errors'])
            })
            
            if dry_run:
                results['message'] = f'Dry run: Would enhance {results["posts_enhanced_count"]} posts with {results["total_improvements"]} improvements'
            else:
                results['message'] = f'Enhanced {results["posts_enhanced_count"]} posts with {results["total_improvements"]} improvements'
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score using Flesch Reading Ease."""
        try:
            sentences = len(re.split(r'[.!?]+', text))
            words = len(text.split())
            syllables = sum(self._count_syllables(word) for word in text.split())
            
            if sentences == 0 or words == 0:
                return 0
            
            # Flesch Reading Ease
            score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            
            # Normalize to 0-100 scale
            return max(0, min(100, score))
            
        except:
            return 50  # Default score

    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count in a word."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not previous_was_vowel:
                    syllable_count += 1
                previous_was_vowel = True
            else:
                previous_was_vowel = False
        
        # Handle silent e
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)

    def _analyze_content_structure(self, soup: BeautifulSoup, word_count: int) -> float:
        """Analyze content structure quality."""
        score = 0
        
        # Check for headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings:
            score += 30
            if len(headings) >= 2:
                score += 20
        
        # Check for lists
        lists = soup.find_all(['ul', 'ol'])
        if lists:
            score += 15
        
        # Check paragraph structure
        paragraphs = soup.find_all('p')
        if paragraphs:
            avg_p_length = sum(len(p.get_text().split()) for p in paragraphs) / len(paragraphs)
            if 20 <= avg_p_length <= 50:  # Good paragraph length
                score += 20
            elif avg_p_length > 0:
                score += 10
        
        # Check for images
        images = soup.find_all('img')
        if images and word_count > 300:
            score += 15
        
        return min(100, score)

    def _score_word_count(self, word_count: int) -> float:
        """Score based on word count."""
        if word_count < 100:
            return 0
        elif word_count < self.min_word_count:
            return (word_count / self.min_word_count) * 60
        elif word_count <= self.optimal_word_count:
            return 60 + ((word_count - self.min_word_count) / (self.optimal_word_count - self.min_word_count)) * 40
        elif word_count <= self.max_word_count:
            return 100 - ((word_count - self.optimal_word_count) / (self.max_word_count - self.optimal_word_count)) * 20
        else:
            return 80

    def _score_links(self, internal_links: int, external_links: int, word_count: int) -> float:
        """Score based on link structure."""
        target_internal = max(1, word_count // 500)  # 1 internal link per 500 words
        target_external = max(1, word_count // 1000)  # 1 external link per 1000 words
        
        internal_score = min(100, (internal_links / target_internal) * 100)
        external_score = min(100, (external_links / target_external) * 100)
        
        return (internal_score * 0.7) + (external_score * 0.3)

    def _score_images(self, image_count: int, word_count: int) -> float:
        """Score based on image usage."""
        if word_count < 300:
            return 100 if image_count >= 1 else 50
        
        target_images = max(1, word_count // 400)  # 1 image per 400 words
        return min(100, (image_count / target_images) * 100)

    def _score_headings(self, heading_count: int, word_count: int) -> float:
        """Score based on heading usage."""
        if word_count < 300:
            return 100 if heading_count >= 1 else 50
        
        target_headings = max(1, word_count // 300)  # 1 heading per 300 words
        return min(100, (heading_count / target_headings) * 100)

    def _get_grade(self, score: float) -> str:
        """Get letter grade from score."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def _get_recommendations(self, scores: Dict[str, float], overall_score: float) -> List[str]:
        """Get improvement recommendations."""
        recommendations = []
        
        if scores['word_count'] < 60:
            recommendations.append("Increase content length for better SEO")
        
        if scores['readability'] < 60:
            recommendations.append("Improve readability with shorter sentences and simpler words")
        
        if scores['structure'] < 70:
            recommendations.append("Add more headings and improve content structure")
        
        if scores['links'] < 50:
            recommendations.append("Add more internal links to related content")
        
        if scores['images'] < 50:
            recommendations.append("Add relevant images to break up text")
        
        if scores['headings'] < 60:
            recommendations.append("Use more headings to organize content")
        
        return recommendations

    def _identify_issues(self, scores: Dict[str, float], word_count: int, heading_count: int, internal_links: int) -> List[str]:
        """Identify specific content issues."""
        issues = []
        
        if word_count < 200:
            issues.append("Content too short for good SEO")
        
        if heading_count == 0:
            issues.append("No headings found")
        
        if internal_links == 0:
            issues.append("No internal links found")
        
        if scores['readability'] < 40:
            issues.append("Content may be difficult to read")
        
        return issues

    def _identify_potential_headings(self, paragraphs: List) -> List[Tuple]:
        """Identify paragraphs that could be headings."""
        potential_headings = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            
            # Check if paragraph could be a heading
            if (len(text.split()) <= 8 and 
                len(text) < 100 and 
                not text.endswith('.') and
                not text.endswith('!') and
                not text.endswith('?')):
                potential_headings.append((p, text))
        
        return potential_headings[:3]  # Max 3 potential headings

    def _find_related_posts(self, post_id: int, categories: List[int], limit: int = 5) -> List[Dict]:
        """Find related posts for internal linking."""
        try:
            # Get posts from same categories
            related_posts = []
            
            if categories:
                posts = self.wp.get_posts(
                    categories=categories,
                    per_page=limit + 5,  # Get extra to filter current post
                    exclude=[post_id]
                )
                related_posts.extend(posts)
            
            # If not enough related posts, get recent posts
            if len(related_posts) < limit:
                recent_posts = self.wp.get_posts(
                    per_page=limit * 2,
                    exclude=[post_id] + [p['id'] for p in related_posts]
                )
                related_posts.extend(recent_posts)
            
            return related_posts[:limit]
            
        except Exception:
            return []

    def _find_original_case(self, text: str, phrase: str) -> Optional[str]:
        """Find original case version of phrase in text."""
        words = text.split()
        phrase_words = phrase.split()
        
        for i in range(len(words) - len(phrase_words) + 1):
            if ' '.join(words[i:i+len(phrase_words)]).lower() == phrase:
                return ' '.join(words[i:i+len(phrase_words)])
        
        return None