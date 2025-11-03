#!/usr/bin/env python3
"""
Individual Post Publishing & Validation Tool
===========================================
Publish individual posts with comprehensive validation and quality checks.
"""

import os
import re
import requests
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from PIL import Image
import hashlib
from io import BytesIO

from ..core import WordPressClient, WordPressAPIError
from ..content.publisher import ContentPublisher
from ..validation.seo import SEOValidator
from ..utils import print_header, print_section, print_success, print_error, print_warning


class IndividualPostValidator:
    """Comprehensive validator for individual posts."""

    def __init__(self, wp_client: WordPressClient = None):
        """Initialize validator."""
        self.wp = wp_client or WordPressClient()
        self.seo_validator = SEOValidator(self.wp)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def validate_post_comprehensive(self, post_id: int, focus_keyword: str = None) -> Dict[str, Any]:
        """Run comprehensive validation on a single post."""
        print_section(f"🔍 Comprehensive Validation: Post {post_id}")

        try:
            post = self.wp.get_post(post_id)
            post_url = post.get('link', '')
            content = post.get('content', {}).get('rendered', '')
            title = post.get('title', {}).get('rendered', '')

            results = {
                'post_id': post_id,
                'post_title': title,
                'post_url': post_url,
                'validations': {},
                'score': 0,
                'max_score': 0,
                'issues': [],
                'warnings': [],
                'recommendations': []
            }

            # 1. URL Length Check (≤90 characters)
            results['validations']['url_length'] = self._validate_url_length(post_url)
            results['max_score'] += 10

            # 2. Search Engine Title Length (≤60 characters)
            results['validations']['title_length'] = self._validate_title_length(title)
            results['max_score'] += 10

            # 3. Internal Links Check
            results['validations']['internal_links'] = self._validate_internal_links(content, post_url)
            results['max_score'] += 15

            # 4. Broken Links Check
            results['validations']['broken_links'] = self._validate_broken_links(content)
            results['max_score'] += 15

            # 5. Missing Images Check
            results['validations']['missing_images'] = self._validate_missing_images(content)
            results['max_score'] += 10

            # 6. Content Quality Check
            results['validations']['content_quality'] = self._validate_content_quality(content)
            results['max_score'] += 10

            # 7. Featured Image Check
            results['validations']['featured_image'] = self._validate_featured_image(post)
            results['max_score'] += 15

            # 8. Category Distribution Check
            results['validations']['category_distribution'] = self._validate_category_distribution()
            results['max_score'] += 5

            # 9. SEO Focus Keyword Analysis (if provided)
            if focus_keyword:
                results['validations']['focus_keyword'] = self._validate_focus_keyword(
                    title, content, post_url, focus_keyword
                )
                results['max_score'] += 10

            # Calculate total score
            for validation in results['validations'].values():
                if validation.get('passed', False):
                    results['score'] += validation.get('points', 0)

                if validation.get('issues'):
                    results['issues'].extend(validation['issues'])
                if validation.get('warnings'):
                    results['warnings'].extend(validation['warnings'])
                if validation.get('recommendations'):
                    results['recommendations'].extend(validation['recommendations'])

            # Calculate percentage
            results['percentage'] = round((results['score'] / results['max_score']) * 100, 1) if results['max_score'] > 0 else 0

            return results

        except Exception as e:
            return {
                'post_id': post_id,
                'error': f'Validation failed: {str(e)}',
                'score': 0,
                'percentage': 0
            }

    def _validate_url_length(self, url: str) -> Dict[str, Any]:
        """Validate URL length (≤90 characters)."""
        url_path = urlparse(url).path
        length = len(url_path)

        result = {
            'passed': length <= 90,
            'length': length,
            'limit': 90,
            'points': 10 if length <= 90 else 0,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if length > 90:
            result['issues'].append(f'URL too long ({length} chars, max 90)')
            result['recommendations'].append('Shorten the post slug to reduce URL length')

        return result

    def _validate_title_length(self, title: str) -> Dict[str, Any]:
        """Validate title length for SEO (≤60 characters)."""
        length = len(title)

        result = {
            'passed': length <= 60,
            'length': length,
            'limit': 60,
            'points': 10 if length <= 60 else 0,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if length > 60:
            result['issues'].append(f'Title too long ({length} chars, max 60)')
            result['recommendations'].append('Shorten the title for better SEO')

        return result

    def _validate_internal_links(self, content: str, post_url: str) -> Dict[str, Any]:
        """Validate internal links are present."""
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)

        base_domain = urlparse(post_url).netloc
        internal_links = []

        for link in links:
            href = link['href']
            if href.startswith('/') or base_domain in href:
                internal_links.append(href)

        has_internal_links = len(internal_links) > 0

        result = {
            'passed': has_internal_links,
            'internal_links_count': len(internal_links),
            'points': 15 if has_internal_links else 0,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if not has_internal_links:
            result['issues'].append('No internal links found')
            result['recommendations'].append('Add internal links to related content for better navigation')

        return result

    def _validate_broken_links(self, content: str) -> Dict[str, Any]:
        """Check for broken links in content."""
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)

        broken_links = []
        total_links = len(links)

        for link in links[:10]:  # Check first 10 links to avoid too many requests
            href = link['href']
            if href.startswith('http'):
                try:
                    response = self.session.head(href, timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        broken_links.append((href, response.status_code))
                except:
                    broken_links.append((href, 'timeout'))

        no_broken_links = len(broken_links) == 0

        result = {
            'passed': no_broken_links,
            'total_links_checked': min(total_links, 10),
            'broken_links': broken_links,
            'points': 15 if no_broken_links else 0,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if broken_links:
            result['issues'].append(f'Found {len(broken_links)} broken links')
            result['recommendations'].append('Fix or remove broken links')

        return result

    def _validate_missing_images(self, content: str) -> Dict[str, Any]:
        """Check for missing or broken images."""
        soup = BeautifulSoup(content, 'html.parser')
        images = soup.find_all('img', src=True)

        missing_images = []
        total_images = len(images)

        for img in images:
            src = img['src']
            if src.startswith('http'):
                try:
                    response = self.session.head(src, timeout=5)
                    if response.status_code >= 400:
                        missing_images.append(src)
                except:
                    missing_images.append(src)

        no_missing_images = len(missing_images) == 0

        result = {
            'passed': no_missing_images,
            'total_images': total_images,
            'missing_images': missing_images,
            'points': 10 if no_missing_images else 0,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if missing_images:
            result['issues'].append(f'Found {len(missing_images)} missing/broken images')
            result['recommendations'].append('Replace or remove broken images')

        return result

    def _validate_content_quality(self, content: str) -> Dict[str, Any]:
        """Validate content quality and structure."""
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text()

        # Word count
        words = re.findall(r'\b\w+\b', text_content)
        word_count = len(words)

        # Headings structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        h1_count = len(soup.find_all('h1'))

        # Check for text overlap issues (basic check)
        has_text_overlap = bool(re.search(r'<div[^>]*position:\s*absolute[^>]*>.*?</div>', content, re.DOTALL | re.IGNORECASE))

        quality_checks = [
            word_count >= 500,
            h1_count == 1,  # Should have exactly one H1
            len(headings) >= 3,  # Should have some headings
            not has_text_overlap
        ]

        passed_checks = sum(quality_checks)
        total_checks = len(quality_checks)

        result = {
            'passed': passed_checks == total_checks,
            'word_count': word_count,
            'headings_count': len(headings),
            'h1_count': h1_count,
            'has_text_overlap': has_text_overlap,
            'quality_score': passed_checks / total_checks,
            'points': 10 if passed_checks == total_checks else (passed_checks / total_checks) * 10,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if word_count < 500:
            result['issues'].append(f'Content too short ({word_count} words, minimum 500)')
        if h1_count == 0:
            result['issues'].append('Missing H1 heading')
        if h1_count > 1:
            result['warnings'].append('Multiple H1 headings found')
        if has_text_overlap:
            result['issues'].append('Potential text overlap on images detected')

        return result

    def _validate_featured_image(self, post: Dict) -> Dict[str, Any]:
        """Validate featured image quality and relevance."""
        featured_media_id = post.get('featured_media')

        if not featured_media_id:
            return {
                'passed': False,
                'has_featured_image': False,
                'points': 0,
                'issues': ['No featured image set'],
                'warnings': [],
                'recommendations': ['Add a relevant featured image']
            }

        try:
            # Get media details
            media = self.wp._make_request('GET', f'media/{featured_media_id}').json()

            image_url = media.get('source_url', '')
            alt_text = media.get('alt_text', '')
            title = post.get('title', {}).get('rendered', '')

            # Basic quality checks
            quality_checks = {
                'has_alt_text': bool(alt_text),
                'url_accessible': False,
                'reasonable_size': False,
                'relevant_alt': False
            }

            # Check if image is accessible
            try:
                response = self.session.get(image_url, timeout=5)
                quality_checks['url_accessible'] = response.status_code == 200

                # Check image dimensions if accessible
                if response.status_code == 200:
                    try:
                        img = Image.open(BytesIO(response.content))
                        w, h = img.size
                        # Heuristic: at least 800x450 for featured quality
                        quality_checks['reasonable_size'] = (w >= 800 and h >= 450)
                    except Exception:
                        quality_checks['reasonable_size'] = False
            except:
                pass

            # Check if alt text is relevant
            if alt_text and title:
                title_words = set(title.lower().split())
                alt_words = set(alt_text.lower().split())
                common_words = title_words.intersection(alt_words)
                quality_checks['relevant_alt'] = len(common_words) > 0

            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)

            result = {
                'passed': passed_checks >= 3,  # Pass if at least 3/4 checks pass
                'has_featured_image': True,
                'image_url': image_url,
                'alt_text': alt_text,
                'quality_checks': quality_checks,
                'quality_score': passed_checks / total_checks,
                'points': 15 if passed_checks >= 3 else (passed_checks / total_checks) * 15,
                'issues': [],
                'warnings': [],
                'recommendations': []
            }

            if not quality_checks['has_alt_text']:
                result['issues'].append('Featured image missing alt text')
            if not quality_checks['url_accessible']:
                result['issues'].append('Featured image URL not accessible')
            if not quality_checks['reasonable_size']:
                result['warnings'].append('Featured image may be too small')
            if not quality_checks['relevant_alt']:
                result['warnings'].append('Alt text may not be relevant to content')

            return result

        except Exception as e:
            return {
                'passed': False,
                'has_featured_image': True,
                'points': 0,
                'issues': [f'Error checking featured image: {str(e)}'],
                'warnings': [],
                'recommendations': ['Verify featured image is properly configured']
            }

    def _validate_category_distribution(self) -> Dict[str, Any]:
        """Validate that categories have minimum posts."""
        try:
            # Get all categories
            categories = self.wp.get_categories()

            # Get recent posts to check distribution
            posts = self.wp.get_posts(per_page=50)

            category_counts = {}
            for post in posts:
                for cat_id in post.get('categories', []):
                    category_counts[cat_id] = category_counts.get(cat_id, 0) + 1

            # Check categories with posts
            categories_with_posts = [cat for cat in categories if cat['id'] in category_counts]
            categories_with_min_posts = [cat for cat in categories_with_posts if category_counts.get(cat['id'], 0) >= 2]

            result = {
                'passed': len(categories_with_min_posts) >= len(categories_with_posts) * 0.8,  # 80% have min posts
                'total_categories': len(categories),
                'categories_with_posts': len(categories_with_posts),
                'categories_with_min_posts': len(categories_with_min_posts),
                'points': 5 if len(categories_with_min_posts) >= len(categories_with_posts) * 0.8 else 0,
                'issues': [],
                'warnings': [],
                'recommendations': []
            }

            if len(categories_with_posts) > len(categories_with_min_posts):
                under_min = len(categories_with_posts) - len(categories_with_min_posts)
                result['warnings'].append(f'{under_min} categories have fewer than 2 posts')
                result['recommendations'].append('Add more content to categories with few posts')

            return result

        except Exception as e:
            return {
                'passed': False,
                'points': 0,
                'issues': [f'Error checking category distribution: {str(e)}'],
                'warnings': [],
                'recommendations': []
            }

    def _validate_focus_keyword(self, title: str, content: str, url: str, keyword: str) -> Dict[str, Any]:
        """Validate focus keyword usage across title, content, URL, and meta."""
        keyword_lower = keyword.lower()

        checks = {
            'in_title': keyword_lower in title.lower(),
            'in_url': keyword_lower in url.lower(),
            'in_content': keyword_lower in content.lower(),
            'title_density': False,
            'content_density': False
        }

        # Check keyword density in title (should be reasonable)
        title_words = title.lower().split()
        title_density = title_words.count(keyword_lower) / len(title_words) if title_words else 0
        checks['title_density'] = 0.1 <= title_density <= 0.3  # 10-30% density

        # Check keyword density in content
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text().lower()
        content_words = text_content.split()
        content_density = content_words.count(keyword_lower) / len(content_words) if content_words else 0
        checks['content_density'] = 0.01 <= content_density <= 0.03  # 1-3% density

        passed_checks = sum(checks.values())
        total_checks = len(checks)

        result = {
            'passed': passed_checks >= 4,  # Pass if at least 4/5 checks pass
            'keyword': keyword,
            'checks': checks,
            'keyword_score': passed_checks / total_checks,
            'points': 10 if passed_checks >= 4 else (passed_checks / total_checks) * 10,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }

        if not checks['in_title']:
            result['issues'].append('Focus keyword not found in title')
        if not checks['in_url']:
            result['warnings'].append('Focus keyword not found in URL')
        if not checks['in_content']:
            result['issues'].append('Focus keyword not found in content')
        if not checks['title_density']:
            result['warnings'].append('Keyword density in title not optimal')
        if not checks['content_density']:
            result['warnings'].append('Keyword density in content not optimal')

        return result



class IndividualPostPublisher:
#     """Individual post publishing with comprehensive validation."""

    def __init__(self, wp_client: WordPressClient = None):
        """Initialize publisher."""
        self.wp = wp_client or WordPressClient()
        self.publisher = ContentPublisher(self.wp)
        self.validator = IndividualPostValidator(self.wp)

    def publish_and_validate(self, file_path: str, category: str = None,
                           status: str = 'publish', focus_keyword: str = None,
                           dry_run: bool = False) -> Dict[str, Any]:
        """Publish individual post with comprehensive validation."""
        # print_header(f"🎯 Individual Post Publishing: {Path(file_path).name}")

        result = {
            'file_path': file_path,
            'category': category,
            'status': status,
            'focus_keyword': focus_keyword,
            'dry_run': dry_run,
            'steps': {}
        }

        try:
            # Step 1: Pre-publish validation
            # print_section("Step 1: Pre-Publish Validation")
            pre_validation = self._validate_file_content(file_path, focus_keyword)
            result['steps']['pre_validation'] = pre_validation

            if not pre_validation['passed']:
                # print_error("Pre-publish validation failed")
                result['success'] = False
                result['error'] = 'Pre-publish validation failed'
                return result

            # print_success("Pre-publish validation passed!")

            # Step 2: Check for existing post by slug/title before publishing
            print_section("Step 2: Pre-publish duplicate check")
            title = pre_validation.get('title')
            slug = pre_validation.get('slug')

            exists_check = self._post_exists(title=title, slug=slug)
            result['steps']['exists_check'] = exists_check

            if exists_check.get('exists'):
                result['success'] = False
                result['error'] = 'Post with same title/slug already exists'
                result['existing_posts'] = exists_check.get('posts', [])
                print_error('Aborting: post already exists with same title/slug')
                return result

            # Step 3: Publish content
            # (was Step 2)
            # print_section("Step 2: Publishing Content")
            publish_result = self.publisher.publish_from_file(
                file_path, category, status, dry_run
            )
            result['steps']['publish'] = publish_result

            if not publish_result['success']:
                result['success'] = False
                result['error'] = publish_result.get('error', 'Publishing failed')
                return result

            # print_success(f"Content published successfully! ID: {publish_result.get('post_id')}")

            # Step 3: Post-publish validation
            if not dry_run and publish_result.get('post_id'):
                # print_section("Step 3: Post-Publish Validation")

                post_validation = self.validator.validate_post_comprehensive(
                    publish_result['post_id'], focus_keyword
                )
                result['steps']['post_validation'] = post_validation

                if 'error' not in post_validation:
                    score = post_validation['percentage']
                    # print(f"📊 Quality Score: {score}%")

                    if score >= 90:
                        # print_success("Excellent quality!")
                        pass
                    elif score >= 80:
                        # print_success("Very good quality!")
                        pass
                    elif score >= 70:
                        # print("Good quality with minor improvements possible")
                        pass
                    else:
                        # print_warning("Quality could be improved")
                        pass

                    # Show top issues
                    if post_validation.get('issues'):
                        # print("\nTop Issues:")
                        for issue in post_validation['issues'][:3]:
                            # print(f"  • {issue}")
                            pass

            result['success'] = True
            return result

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            # print_error(f"Publishing failed: {e}")
            return result

    def _validate_file_content(self, file_path: str, focus_keyword: str = None) -> Dict[str, Any]:
        """Validate file content before publishing."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse front matter
            front_matter = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    import yaml
                    front_matter = yaml.safe_load(parts[1]) or {}

            markdown_content = content.split('---', 2)[-1] if content.startswith('---') else content
            # Derive slug from front matter or title
            slug = None
            if front_matter.get('slug'):
                slug = front_matter.get('slug')
            elif front_matter.get('title'):
                slug = self._slugify(front_matter.get('title'))
            else:
                # fallback: generate from first line or filename
                slug = None

            result = {
                'passed': True,
                'file_size': len(content),
                'has_front_matter': bool(front_matter),
                'title': front_matter.get('title'),
                'slug': slug,
                'word_count': len(re.findall(r'\b\w+\b', markdown_content)),
                'issues': [],
                'warnings': [],
                'recommendations': []
            }

            # Basic validations
            if not front_matter.get('title'):
                result['issues'].append('Missing title in front matter')
                result['passed'] = False

            if result['word_count'] < 300:
                result['warnings'].append(f'Content may be short ({result["word_count"]} words)')

            if focus_keyword and focus_keyword.lower() not in markdown_content.lower():
                result['warnings'].append('Focus keyword not found in content')

            return result

        except Exception as e:
            return {
                'passed': False,
                'error': f'File validation failed: {str(e)}'
            }

    def validate_existing_post(self, post_id: int, focus_keyword: str = None) -> Dict[str, Any]:
        """Validate an existing post without publishing."""
        validation = self.validator.validate_post_comprehensive(post_id, focus_keyword)

        if 'error' in validation:
            return {'success': False, 'error': validation['error']}

        return {
            'success': True,
            'validation': validation
        }

    # --- Helper methods for publish checks ---
    def _slugify(self, text: str) -> str:
        """Create a URL-friendly slug from text."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s-]", "", text)
        text = re.sub(r"[\s-]+", "-", text).strip('-')
        return text

    def _post_exists(self, title: str = None, slug: str = None) -> Dict[str, Any]:
        """Check whether a post exists with same title or slug.

        Returns dict with keys: exists (bool), posts (list)
        """
        try:
            posts = []
            # Check by slug if provided
            if slug:
                found = self.wp.get_posts(per_page=5, slug=slug)
                if found:
                    posts.extend(found)

            # Check by title (simple contains search across recent posts)
            if title and not posts:
                # get recent posts and search titles
                recent = self.wp.get_posts(per_page=50)
                for p in recent:
                    p_title = p.get('title', {}).get('rendered', '')
                    if p_title and title.strip().lower() == p_title.strip().lower():
                        posts.append(p)

            return {'exists': len(posts) > 0, 'posts': posts}

        except Exception as e:
            return {'exists': False, 'posts': [], 'error': str(e)}
