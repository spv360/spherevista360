"""
SEO Validation and Optimization
===============================
SEO validation and optimization utilities for WordPress content.
"""

import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class SEOValidator:
    """SEO validation and optimization utilities."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize SEO validator."""
        self.wp = wp_client or WordPressClient()
        
        # SEO guidelines
        self.title_max_length = 60
        self.meta_description_max_length = 155
        self.slug_max_length = 50
        self.min_word_count = 300
        self.max_word_count = 2500
    
    def validate_title(self, title: str) -> Dict[str, Any]:
        """Validate post title for SEO."""
        issues = []
        recommendations = []
        
        length = len(title)
        
        # Length validation
        if length == 0:
            issues.append("Title is empty")
        elif length < 30:
            recommendations.append("Title is short, consider adding more descriptive words")
        elif length > self.title_max_length:
            issues.append(f"Title too long ({length} chars, max {self.title_max_length})")
        
        # Content validation
        if title and not any(char.isalpha() for char in title):
            issues.append("Title contains no alphabetic characters")
        
        if title and title.isupper():
            recommendations.append("Avoid all-caps titles")
        
        # Check for common SEO issues
        if "..." in title:
            recommendations.append("Avoid truncation indicators in title")
        
        return {
            'valid': len(issues) == 0,
            'length': length,
            'issues': issues,
            'recommendations': recommendations,
            'optimized_title': self._optimize_title(title)
        }
    
    def validate_meta_description(self, description: str) -> Dict[str, Any]:
        """Validate meta description for SEO."""
        issues = []
        recommendations = []
        
        length = len(description) if description else 0
        
        # Length validation
        if length == 0:
            recommendations.append("Add a meta description")
        elif length < 120:
            recommendations.append("Meta description is short, consider expanding")
        elif length > self.meta_description_max_length:
            issues.append(f"Meta description too long ({length} chars, max {self.meta_description_max_length})")
        
        return {
            'valid': len(issues) == 0,
            'length': length,
            'issues': issues,
            'recommendations': recommendations
        }
    
    def validate_slug(self, slug: str) -> Dict[str, Any]:
        """Validate URL slug for SEO."""
        issues = []
        recommendations = []
        
        length = len(slug) if slug else 0
        
        # Length validation
        if length == 0:
            issues.append("Slug is empty")
        elif length > self.slug_max_length:
            issues.append(f"Slug too long ({length} chars, max {self.slug_max_length})")
        
        # Format validation
        if slug:
            if not re.match(r'^[a-z0-9-]+$', slug):
                issues.append("Slug should only contain lowercase letters, numbers, and hyphens")
            
            if slug.startswith('-') or slug.endswith('-'):
                issues.append("Slug should not start or end with hyphens")
            
            if '--' in slug:
                recommendations.append("Avoid consecutive hyphens in slug")
        
        return {
            'valid': len(issues) == 0,
            'length': length,
            'issues': issues,
            'recommendations': recommendations,
            'optimized_slug': self._optimize_slug(slug)
        }
    
    def validate_content(self, content: str) -> Dict[str, Any]:
        """Validate content for SEO."""
        issues = []
        recommendations = []
        
        # Strip HTML for word count
        text_content = re.sub(r'<[^>]+>', '', content)
        words = text_content.split()
        word_count = len(words)
        
        # Word count validation
        if word_count < self.min_word_count:
            recommendations.append(f"Content is short ({word_count} words, recommended min {self.min_word_count})")
        elif word_count > self.max_word_count:
            recommendations.append(f"Content is very long ({word_count} words, recommended max {self.max_word_count})")
        
        # Heading structure
        headings = re.findall(r'<h([1-6])[^>]*>([^<]+)</h[1-6]>', content, re.IGNORECASE)
        h1_count = len([h for h in headings if h[0] == '1'])
        
        if h1_count == 0:
            recommendations.append("Add an H1 heading")
        elif h1_count > 1:
            recommendations.append("Use only one H1 heading per post")
        
        # Image alt text
        images = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        images_without_alt = [img for img in images if 'alt=' not in img]
        
        if images_without_alt:
            recommendations.append(f"{len(images_without_alt)} images missing alt text")
        
        # Internal/external links
        internal_links = len(re.findall(r'href=["\']https://spherevista360\.com[^"\']*["\']', content, re.IGNORECASE))
        external_links = len(re.findall(r'href=["\']https://(?!spherevista360\.com)[^"\']*["\']', content, re.IGNORECASE))
        
        if internal_links == 0:
            recommendations.append("Add internal links to related content")
        
        return {
            'valid': len(issues) == 0,
            'word_count': word_count,
            'headings_count': len(headings),
            'h1_count': h1_count,
            'images_count': len(images),
            'images_without_alt': len(images_without_alt),
            'internal_links': internal_links,
            'external_links': external_links,
            'issues': issues,
            'recommendations': recommendations
        }
    
    def validate_post(self, post_id: int) -> Dict[str, Any]:
        """Comprehensive SEO validation for a post."""
        try:
            post = self.wp.get_post(post_id)
            
            title = post['title']['rendered']
            content = post['content']['rendered']
            slug = post['slug']
            excerpt = post.get('excerpt', {}).get('rendered', '')
            
            # Validate components
            title_validation = self.validate_title(title)
            content_validation = self.validate_content(content)
            slug_validation = self.validate_slug(slug)
            meta_validation = self.validate_meta_description(excerpt)
            
            # Calculate overall score
            total_issues = (
                len(title_validation['issues']) +
                len(content_validation['issues']) +
                len(slug_validation['issues']) +
                len(meta_validation['issues'])
            )
            
            total_recommendations = (
                len(title_validation['recommendations']) +
                len(content_validation['recommendations']) +
                len(slug_validation['recommendations']) +
                len(meta_validation['recommendations'])
            )
            
            # Score calculation (100 - issues*10 - recommendations*2)
            score = max(0, 100 - (total_issues * 10) - (total_recommendations * 2))
            
            return {
                'post_id': post_id,
                'post_title': title,
                'score': score,
                'grade': self._get_grade(score),
                'title': title_validation,
                'content': content_validation,
                'slug': slug_validation,
                'meta_description': meta_validation,
                'total_issues': total_issues,
                'total_recommendations': total_recommendations
            }
            
        except Exception as e:
            return {
                'post_id': post_id,
                'error': str(e)
            }
    
    def optimize_post_seo(self, post_id: int, dry_run: bool = False) -> Dict[str, Any]:
        """Optimize post SEO by fixing common issues."""
        try:
            validation = self.validate_post(post_id)
            
            if 'error' in validation:
                return validation
            
            updates = {}
            optimizations = []
            
            # Optimize title if needed
            title_issues = validation['title']['issues']
            if title_issues:
                optimized_title = validation['title']['optimized_title']
                if optimized_title != validation['post_title']:
                    updates['title'] = optimized_title
                    optimizations.append(f"Optimized title length")
            
            # Optimize slug if needed
            slug_issues = validation['slug']['issues']
            if slug_issues:
                optimized_slug = validation['slug']['optimized_slug']
                updates['slug'] = optimized_slug
                optimizations.append(f"Optimized URL slug")
            
            result = {
                'post_id': post_id,
                'optimizations': optimizations,
                'updates': updates
            }
            
            if not optimizations:
                result['message'] = 'No optimizations needed'
                return result
            
            if dry_run:
                result['message'] = f'Would apply {len(optimizations)} optimizations'
                return result
            
            # Apply updates
            if updates:
                self.wp.update_post(post_id, updates)
                result['success'] = True
                result['message'] = f'Applied {len(optimizations)} optimizations'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }
    
    def scan_posts_seo(self, post_ids: List[int] = None, per_page: int = 10) -> Dict[str, Any]:
        """Scan multiple posts for SEO issues."""
        if post_ids:
            posts_to_check = [{'id': pid} for pid in post_ids]
        else:
            try:
                posts_to_check = self.wp.get_posts(per_page=per_page)
            except Exception as e:
                return {'error': f'Failed to get posts: {e}'}
        
        results = {
            'posts_scanned': 0,
            'average_score': 0,
            'posts_with_issues': 0,
            'total_issues': 0,
            'post_results': []
        }
        
        total_score = 0
        
        for post in posts_to_check:
            post_id = post['id']
            validation = self.validate_post(post_id)
            
            if 'error' not in validation:
                results['posts_scanned'] += 1
                total_score += validation['score']
                
                if validation['total_issues'] > 0:
                    results['posts_with_issues'] += 1
                
                results['total_issues'] += validation['total_issues']
                results['post_results'].append(validation)
        
        if results['posts_scanned'] > 0:
            results['average_score'] = total_score / results['posts_scanned']
        
        return results
    
    def _optimize_title(self, title: str) -> str:
        """Optimize title for SEO."""
        if not title:
            return title
        
        # Truncate if too long
        if len(title) > self.title_max_length:
            # Try to truncate at word boundary
            truncated = title[:self.title_max_length - 3].rsplit(' ', 1)[0]
            return truncated + "..."
        
        return title
    
    def _optimize_slug(self, slug: str) -> str:
        """Optimize slug for SEO."""
        if not slug:
            return slug
        
        # Convert to lowercase and replace spaces/underscores with hyphens
        optimized = slug.lower().replace(' ', '-').replace('_', '-')
        
        # Remove special characters except hyphens
        optimized = re.sub(r'[^a-z0-9-]', '', optimized)
        
        # Remove consecutive hyphens
        optimized = re.sub(r'-+', '-', optimized)
        
        # Remove leading/trailing hyphens
        optimized = optimized.strip('-')
        
        # Truncate if too long
        if len(optimized) > self.slug_max_length:
            optimized = optimized[:self.slug_max_length].rstrip('-')
        
        return optimized
    
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

    def add_meta_description(self, post_id: int, meta_description: str = None, dry_run: bool = False) -> Dict[str, Any]:
        """Add or update meta description for a post."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled')
            }
            
            # Check if meta description already exists
            current_meta = post.get('meta', {})
            existing_desc = current_meta.get('_yoast_wpseo_metadesc', '')
            
            if existing_desc and not meta_description:
                result['message'] = 'Post already has meta description'
                result['current_meta_description'] = existing_desc
                return result
            
            # Generate meta description if not provided
            if not meta_description:
                content = post.get('content', {}).get('rendered', '')
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                text = soup.get_text()
                
                # Extract first paragraph or first 155 characters
                paragraphs = text.split('\n\n')
                if paragraphs and len(paragraphs[0]) > 50:
                    meta_description = paragraphs[0][:155].strip()
                else:
                    meta_description = text[:155].strip()
                
                # Add ellipsis if truncated
                if len(text) > 155:
                    meta_description += '...'
            
            # Validate the meta description
            validation = self.validate_meta_description(meta_description)
            if validation['issues']:
                meta_description = meta_description[:160]  # Truncate if too long
            
            result['new_meta_description'] = meta_description
            
            if dry_run:
                result['message'] = f'Would set meta description: {meta_description[:50]}...'
                return result
            
            # Update post meta
            meta_updates = {
                '_yoast_wpseo_metadesc': meta_description
            }
            
            update_data = {'meta': meta_updates}
            self.wp.update_post(post_id, update_data)
            
            result.update({
                'success': True,
                'message': 'Successfully added meta description'
            })
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def add_social_meta_tags(self, post_id: int, dry_run: bool = False) -> Dict[str, Any]:
        """Add social media meta tags (Open Graph, Twitter) to a post."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled')
            }
            
            current_meta = post.get('meta', {})
            
            # Prepare social meta updates
            meta_updates = {}
            
            # Open Graph tags
            og_title = current_meta.get('_yoast_wpseo_opengraph-title', '')
            if not og_title:
                meta_updates['_yoast_wpseo_opengraph-title'] = post.get('title', {}).get('rendered', '')
            
            og_description = current_meta.get('_yoast_wpseo_opengraph-description', '')
            if not og_description:
                meta_desc = current_meta.get('_yoast_wpseo_metadesc', '')
                if meta_desc:
                    meta_updates['_yoast_wpseo_opengraph-description'] = meta_desc
                else:
                    # Generate from content
                    content = post.get('content', {}).get('rendered', '')
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    text = soup.get_text()[:155].strip()
                    meta_updates['_yoast_wpseo_opengraph-description'] = text
            
            # Twitter Card tags
            twitter_title = current_meta.get('_yoast_wpseo_twitter-title', '')
            if not twitter_title:
                meta_updates['_yoast_wpseo_twitter-title'] = post.get('title', {}).get('rendered', '')
            
            twitter_description = current_meta.get('_yoast_wpseo_twitter-description', '')
            if not twitter_description:
                meta_desc = current_meta.get('_yoast_wpseo_metadesc', '')
                if meta_desc:
                    meta_updates['_yoast_wpseo_twitter-description'] = meta_desc
                else:
                    meta_updates['_yoast_wpseo_twitter-description'] = meta_updates.get('_yoast_wpseo_opengraph-description', '')
            
            result['meta_updates'] = meta_updates
            
            if not meta_updates:
                result['message'] = 'Social meta tags already exist'
                return result
            
            if dry_run:
                result['message'] = f'Would add {len(meta_updates)} social meta tags'
                return result
            
            # Update post
            update_data = {'meta': meta_updates}
            self.wp.update_post(post_id, update_data)
            
            result.update({
                'success': True,
                'message': f'Added {len(meta_updates)} social meta tags'
            })
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def add_schema_markup(self, post_id: int, schema_type: str = 'Article', dry_run: bool = False) -> Dict[str, Any]:
        """Add structured data (schema.org) markup to a post."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'schema_type': schema_type
            }
            
            current_meta = post.get('meta', {})
            
            # Check if schema already exists
            existing_schema = current_meta.get('_yoast_wpseo_schema_article_type', '')
            if existing_schema:
                result['message'] = f'Schema markup already exists: {existing_schema}'
                return result
            
            # Prepare schema updates
            meta_updates = {
                '_yoast_wpseo_schema_article_type': schema_type,
                '_yoast_wpseo_schema_page_type': 'WebPage'
            }
            
            # Add author schema if available
            author_id = post.get('author', 0)
            if author_id:
                meta_updates['_yoast_wpseo_schema_author'] = str(author_id)
            
            result['meta_updates'] = meta_updates
            
            if dry_run:
                result['message'] = f'Would add {schema_type} schema markup'
                return result
            
            # Update post
            update_data = {'meta': meta_updates}
            self.wp.update_post(post_id, update_data)
            
            result.update({
                'success': True,
                'message': f'Added {schema_type} schema markup'
            })
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def bulk_seo_fixes(self, post_ids: List[int] = None, per_page: int = 10, dry_run: bool = False) -> Dict[str, Any]:
        """Apply comprehensive SEO fixes to multiple posts."""
        try:
            if post_ids:
                posts_to_check = [{'id': pid} for pid in post_ids]
            else:
                # Get all published posts
                posts_to_check = self.wp.get_posts(
                    status='publish',
                    per_page=per_page,
                    orderby='date',
                    order='desc'
                )
            
            results = {
                'total_posts': len(posts_to_check),
                'posts_processed': [],
                'posts_fixed': [],
                'fixes_applied': [],
                'errors': []
            }
            
            for post in posts_to_check:
                post_id = post['id']
                post_fixes = []
                
                try:
                    # Fix meta description
                    meta_result = self.add_meta_description(post_id, dry_run=dry_run)
                    if meta_result.get('success', False):
                        post_fixes.append('meta_description')
                    
                    # Fix social meta tags
                    social_result = self.add_social_meta_tags(post_id, dry_run=dry_run)
                    if social_result.get('success', False):
                        post_fixes.append('social_meta')
                    
                    # Fix schema markup
                    schema_result = self.add_schema_markup(post_id, dry_run=dry_run)
                    if schema_result.get('success', False):
                        post_fixes.append('schema_markup')
                    
                    # Optimize existing SEO
                    seo_result = self.optimize_post_seo(post_id, dry_run=dry_run)
                    if seo_result.get('success', False):
                        post_fixes.append('seo_optimization')
                    
                    results['posts_processed'].append({
                        'post_id': post_id,
                        'fixes': post_fixes,
                        'meta_result': meta_result,
                        'social_result': social_result,
                        'schema_result': schema_result,
                        'seo_result': seo_result
                    })
                    
                    if post_fixes:
                        results['posts_fixed'].append(post_id)
                        results['fixes_applied'].extend(post_fixes)
                    
                except Exception as e:
                    results['errors'].append({
                        'post_id': post_id,
                        'error': str(e)
                    })
            
            results.update({
                'posts_fixed_count': len(results['posts_fixed']),
                'total_fixes': len(results['fixes_applied']),
                'errors_count': len(results['errors'])
            })
            
            if dry_run:
                results['message'] = f'Dry run: Would apply {results["total_fixes"]} SEO fixes to {results["posts_fixed_count"]} posts'
            else:
                results['message'] = f'Applied {results["total_fixes"]} SEO fixes to {results["posts_fixed_count"]} posts'
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            return 'F'