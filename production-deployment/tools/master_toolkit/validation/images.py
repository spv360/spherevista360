"""
Image Validation and Optimization
=================================
Image validation and optimization utilities for WordPress content.
"""

import requests
import re
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class ImageValidator:
    """Image validation and optimization utilities."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize image validator."""
        self.wp = wp_client or WordPressClient()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (WordPress-Toolkit/1.0)'
        })
        
        # Default replacement images by category
        self.replacement_images = {
            'technology': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'entertainment': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'finance': 'https://images.unsplash.com/photo-1559589688-f26e20a6c987?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'business': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80',
            'default': 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80'
        }
    
    def validate_image_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Validate a single image URL."""
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            
            # Check if response is an image
            content_type = response.headers.get('content-type', '').lower()
            is_image = content_type.startswith('image/')
            
            return {
                'url': url,
                'valid': response.status_code < 400 and is_image,
                'status_code': response.status_code,
                'content_type': content_type,
                'is_image': is_image,
                'final_url': response.url,
                'redirected': response.url != url
            }
            
        except requests.RequestException as e:
            return {
                'url': url,
                'valid': False,
                'status_code': None,
                'error': str(e),
                'content_type': None,
                'is_image': False,
                'final_url': None,
                'redirected': False
            }
    
    def extract_images_from_content(self, content: str) -> List[Dict[str, str]]:
        """Extract all images from HTML content."""
        # Pattern to match img tags
        img_pattern = r'<img[^>]*src=["\']([^"\']*)["\'][^>]*>'
        matches = re.finditer(img_pattern, content, re.IGNORECASE)
        
        images = []
        for match in matches:
            img_tag = match.group(0)
            src = match.group(1)
            
            # Extract alt text
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
            alt_text = alt_match.group(1) if alt_match else ''
            
            # Extract class
            class_match = re.search(r'class=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
            css_class = class_match.group(1) if class_match else ''
            
            images.append({
                'src': src,
                'alt': alt_text,
                'class': css_class,
                'full_tag': img_tag
            })
        
        return images
    
    def validate_images_in_content(self, content: str) -> Dict[str, Any]:
        """Validate all images in content."""
        images = self.extract_images_from_content(content)
        
        results = {
            'total_images': len(images),
            'valid_images': 0,
            'broken_images': 0,
            'images_without_alt': 0,
            'validation_results': []
        }
        
        for image in images:
            src = image['src']
            
            # Validate URL
            validation = self.validate_image_url(src)
            
            # Check alt text
            has_alt = bool(image['alt'].strip())
            if not has_alt:
                results['images_without_alt'] += 1
            
            validation.update({
                'alt_text': image['alt'],
                'has_alt': has_alt,
                'css_class': image['class'],
                'full_tag': image['full_tag']
            })
            
            if validation['valid']:
                results['valid_images'] += 1
            else:
                results['broken_images'] += 1
            
            results['validation_results'].append(validation)
        
        return results
    
    def validate_post_images(self, post_id: int) -> Dict[str, Any]:
        """Validate all images in a specific post."""
        try:
            post = self.wp.get_post(post_id)
            content = post['content']['rendered']
            
            results = self.validate_images_in_content(content)
            results['post_id'] = post_id
            results['post_title'] = post['title']['rendered']
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'post_id': post_id
            }
    
    def fix_broken_images_in_content(self, content: str, category: str = 'default') -> Tuple[str, List[str]]:
        """Fix broken images in content by replacing with working alternatives."""
        images = self.extract_images_from_content(content)
        fixed_content = content
        fixes_applied = []
        
        replacement_url = self.replacement_images.get(category.lower(), self.replacement_images['default'])
        
        for image in images:
            src = image['src']
            
            # Validate image
            validation = self.validate_image_url(src)
            
            if not validation['valid']:
                # Replace with working image
                old_tag = image['full_tag']
                new_src = replacement_url
                
                # Create new img tag preserving alt text and class
                new_tag = f'<img src="{new_src}"'
                
                if image['alt']:
                    new_tag += f' alt="{image["alt"]}"'
                else:
                    new_tag += f' alt="Image for {category} content"'
                
                if image['class']:
                    new_tag += f' class="{image["class"]}"'
                
                new_tag += '>'
                
                fixed_content = fixed_content.replace(old_tag, new_tag)
                fixes_applied.append(f"Replaced broken image: {src} → {new_src}")
        
        return fixed_content, fixes_applied
    
    def fix_post_images(self, post_id: int, category: str = 'default', dry_run: bool = False) -> Dict[str, Any]:
        """Fix broken images in a specific post."""
        try:
            # Get post content
            post = self.wp.get_post(post_id, context='edit')
            
            # Try to get raw content, fallback to rendered
            if 'raw' in post.get('content', {}):
                current_content = post['content']['raw']
                content_source = 'raw'
            else:
                current_content = post['content']['rendered']
                content_source = 'rendered'
            
            # Fix images
            fixed_content, fixes_applied = self.fix_broken_images_in_content(current_content, category)
            
            result = {
                'post_id': post_id,
                'post_title': post['title']['rendered'],
                'content_source': content_source,
                'fixes_applied': fixes_applied,
                'changes_made': len(fixes_applied) > 0
            }
            
            if not fixes_applied:
                result['message'] = 'No broken images found to fix'
                return result
            
            if dry_run:
                result['message'] = f'Would fix {len(fixes_applied)} broken images'
                return result
            
            # Update post
            update_data = {'content': fixed_content}
            self.wp.update_post(post_id, update_data)
            
            result['success'] = True
            result['message'] = f'Fixed {len(fixes_applied)} broken images'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }
    
    def add_missing_alt_text(self, content: str, default_alt: str = "Content image") -> Tuple[str, List[str]]:
        """Add alt text to images that are missing it."""
        images = self.extract_images_from_content(content)
        fixed_content = content
        fixes_applied = []
        
        for image in images:
            if not image['alt'].strip():
                old_tag = image['full_tag']
                
                # Add alt text
                if 'alt=' in old_tag:
                    # Replace empty alt
                    new_tag = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{default_alt}"', old_tag, flags=re.IGNORECASE)
                else:
                    # Add alt attribute
                    new_tag = old_tag[:-1] + f' alt="{default_alt}">'
                
                fixed_content = fixed_content.replace(old_tag, new_tag)
                fixes_applied.append(f"Added alt text to image: {image['src']}")
        
        return fixed_content, fixes_applied
    
    def optimize_post_images(self, post_id: int, category: str = 'default', dry_run: bool = False) -> Dict[str, Any]:
        """Comprehensive image optimization for a post."""
        try:
            # Get current validation
            validation = self.validate_post_images(post_id)
            
            if 'error' in validation:
                return validation
            
            # Get post content for fixing
            post = self.wp.get_post(post_id, context='edit')
            
            if 'raw' in post.get('content', {}):
                current_content = post['content']['raw']
            else:
                current_content = post['content']['rendered']
            
            all_fixes = []
            fixed_content = current_content
            
            # Fix broken images
            if validation['broken_images'] > 0:
                fixed_content, image_fixes = self.fix_broken_images_in_content(fixed_content, category)
                all_fixes.extend(image_fixes)
            
            # Add missing alt text
            if validation['images_without_alt'] > 0:
                fixed_content, alt_fixes = self.add_missing_alt_text(fixed_content)
                all_fixes.extend(alt_fixes)
            
            result = {
                'post_id': post_id,
                'post_title': validation['post_title'],
                'fixes_applied': all_fixes,
                'changes_made': len(all_fixes) > 0
            }
            
            if not all_fixes:
                result['message'] = 'No image optimizations needed'
                return result
            
            if dry_run:
                result['message'] = f'Would apply {len(all_fixes)} image optimizations'
                return result
            
            # Update post
            update_data = {'content': fixed_content}
            self.wp.update_post(post_id, update_data)
            
            result['success'] = True
            result['message'] = f'Applied {len(all_fixes)} image optimizations'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def check_featured_image(self, post_id: int) -> Dict[str, Any]:
        """Check if post has a featured image."""
        try:
            post = self.wp.get_post(post_id)
            has_featured_image = post.get('featured_media', 0) > 0
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'has_featured_image': has_featured_image,
                'featured_media_id': post.get('featured_media', 0)
            }
            
            if has_featured_image:
                # Get featured image details
                try:
                    media = self.wp.get_media(post['featured_media'])
                    result['featured_image'] = {
                        'id': media['id'],
                        'url': media['source_url'],
                        'alt_text': media.get('alt_text', ''),
                        'title': media.get('title', {}).get('rendered', ''),
                        'caption': media.get('caption', {}).get('rendered', '')
                    }
                except Exception:
                    result['featured_image_error'] = 'Failed to get featured image details'
            
            return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'error': str(e)
            }

    def set_featured_image_from_content(self, post_id: int, dry_run: bool = False) -> Dict[str, Any]:
        """Set featured image from the first image found in post content."""
        try:
            post = self.wp.get_post(post_id, context='edit')
            
            # Check if already has featured image
            if post.get('featured_media', 0) > 0:
                return {
                    'post_id': post_id,
                    'message': 'Post already has a featured image',
                    'featured_media_id': post['featured_media']
                }
            
            # Get content and extract images
            if 'raw' in post.get('content', {}):
                content = post['content']['raw']
            else:
                content = post['content']['rendered']
            
            images = self.extract_images_from_content(content)
            
            if not images:
                return {
                    'post_id': post_id,
                    'message': 'No images found in post content to use as featured image'
                }
            
            # Use the first valid image
            first_image = images[0]
            image_url = first_image['src']
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'image_url': image_url,
                'image_alt': first_image.get('alt', '')
            }
            
            if dry_run:
                result['message'] = f'Would set featured image from: {image_url}'
                return result
            
            # Upload image to WordPress media library
            try:
                # Download image
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                
                # Extract filename
                import os
                from urllib.parse import urlparse
                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path) or f'featured_image_{post_id}.jpg'
                
                # Upload to WordPress
                media_response = self.wp.upload_media(
                    file_content=response.content,
                    filename=filename,
                    alt_text=first_image.get('alt', ''),
                    caption=f'Featured image for post {post_id}'
                )
                
                media_id = media_response['id']
                
                # Set as featured image
                self.wp.update_post(post_id, {'featured_media': media_id})
                
                result.update({
                    'success': True,
                    'media_id': media_id,
                    'message': f'Successfully set featured image from content'
                })
                
                return result
                
            except requests.RequestException as e:
                result.update({
                    'success': False,
                    'error': f'Failed to download image: {str(e)}'
                })
                return result
            except Exception as e:
                result.update({
                    'success': False,
                    'error': f'Failed to upload image: {str(e)}'
                })
                return result
            
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def download_and_set_featured_image(self, post_id: int, image_url: str, dry_run: bool = False) -> Dict[str, Any]:
        """Download an external image and set it as featured image."""
        try:
            post = self.wp.get_post(post_id)
            
            result = {
                'post_id': post_id,
                'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                'image_url': image_url
            }
            
            # Check if already has featured image
            if post.get('featured_media', 0) > 0:
                result['message'] = 'Post already has a featured image'
                result['featured_media_id'] = post['featured_media']
                return result
            
            if dry_run:
                result['message'] = f'Would download and set featured image: {image_url}'
                return result
            
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Extract filename
            import os
            from urllib.parse import urlparse
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path) or f'featured_image_{post_id}.jpg'
            
            # Upload to WordPress
            media_response = self.wp.upload_media(
                file_content=response.content,
                filename=filename,
                alt_text=f'Featured image for {post.get("title", {}).get("rendered", "post")}',
                caption=f'Featured image for post {post_id}'
            )
            
            media_id = media_response['id']
            
            # Set as featured image
            self.wp.update_post(post_id, {'featured_media': media_id})
            
            result.update({
                'success': True,
                'media_id': media_id,
                'message': 'Successfully downloaded and set featured image'
            })
            
            return result
            
        except requests.RequestException as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': f'Failed to download image: {str(e)}'
            }
        except Exception as e:
            return {
                'post_id': post_id,
                'success': False,
                'error': str(e)
            }

    def bulk_fix_featured_images(self, post_ids: List[int] = None, per_page: int = 10, dry_run: bool = False) -> Dict[str, Any]:
        """Bulk fix missing featured images for multiple posts."""
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
                'posts_skipped': [],
                'errors': []
            }
            
            for post in posts_to_check:
                post_id = post['id']
                
                try:
                    # Check if post needs featured image
                    check_result = self.check_featured_image(post_id)
                    
                    if check_result.get('has_featured_image', False):
                        results['posts_skipped'].append({
                            'post_id': post_id,
                            'reason': 'Already has featured image'
                        })
                        continue
                    
                    # Try to set featured image from content
                    fix_result = self.set_featured_image_from_content(post_id, dry_run=dry_run)
                    
                    results['posts_processed'].append({
                        'post_id': post_id,
                        'result': fix_result
                    })
                    
                    if fix_result.get('success', False):
                        results['posts_fixed'].append(post_id)
                    
                except Exception as e:
                    results['errors'].append({
                        'post_id': post_id,
                        'error': str(e)
                    })
            
            results.update({
                'posts_fixed_count': len(results['posts_fixed']),
                'posts_skipped_count': len(results['posts_skipped']),
                'errors_count': len(results['errors'])
            })
            
            if dry_run:
                results['message'] = f'Dry run: Would fix {results["posts_fixed_count"]} posts'
            else:
                results['message'] = f'Fixed featured images for {results["posts_fixed_count"]} posts'
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
