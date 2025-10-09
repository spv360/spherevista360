#!/usr/bin/env python3
"""
Image Validation and Optimization Module
========================================
Tools for validating and optimizing images in WordPress content.
"""

import requests
import re
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import base64
from io import BytesIO


class ImageValidator:
    """Image validation and optimization for WordPress content."""
    
    def __init__(self, wp_client=None):
        """Initialize image validator.
        
        Args:
            wp_client: WordPress client instance for API operations
        """
        self.wp_client = wp_client
        self.default_images = [
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
        ]
        
    def validate_content_images(self, content: str, title: str) -> Dict:
        """Validate images in content.
        
        Args:
            content: HTML content
            title: Content title for context
            
        Returns:
            Dict with image validation results
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all images
        img_tags = soup.find_all('img')
        
        images = []
        issues = []
        
        for i, img in enumerate(img_tags):
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Validate image
            img_data = {
                'index': i,
                'src': src,
                'alt': alt,
                'has_src': bool(src),
                'has_alt': bool(alt.strip()),
                'alt_length': len(alt),
                'is_external': self._is_external_url(src),
                'is_accessible': False,
                'file_size': 0,
                'dimensions': None
            }
            
            # Test image accessibility
            if src:
                try:
                    response = requests.head(src, timeout=10)
                    img_data['is_accessible'] = response.status_code == 200
                    img_data['file_size'] = int(response.headers.get('content-length', 0))
                except:
                    img_data['is_accessible'] = False
            
            # Check for issues
            if not src:
                issues.append(f"Image {i+1}: Missing src attribute")
            elif not img_data['is_accessible']:
                issues.append(f"Image {i+1}: Not accessible ({src})")
            
            if not alt.strip():
                issues.append(f"Image {i+1}: Missing alt text")
            elif len(alt) < 5:
                issues.append(f"Image {i+1}: Alt text too short")
            
            images.append(img_data)
        
        return {
            'title': title,
            'total_images': len(images),
            'images_with_alt': sum(1 for img in images if img['has_alt']),
            'accessible_images': sum(1 for img in images if img['is_accessible']),
            'external_images': sum(1 for img in images if img['is_external']),
            'images': images,
            'issues': issues,
            'needs_images': len(images) == 0,
            'needs_alt_text': any(not img['has_alt'] for img in images),
            'has_broken_images': any(not img['is_accessible'] for img in images if img['src']),
            'score': self._calculate_image_score(images),
            'recommendations': self._get_image_recommendations(images, issues)
        }
    
    def add_images_to_content(self, content: str, title: str, num_images: int = 3) -> str:
        """Add images to content that lacks them.
        
        Args:
            content: HTML content
            title: Content title for alt text generation
            num_images: Number of images to add
            
        Returns:
            Updated HTML content with images
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if content already has enough images
        existing_images = len(soup.find_all('img'))
        if existing_images >= num_images:
            return content
        
        # Find H2 headings to insert images after
        h2_tags = soup.find_all('h2')
        
        images_to_add = min(num_images - existing_images, len(h2_tags))
        
        for i in range(images_to_add):
            if i < len(h2_tags):
                # Create image element
                img_tag = soup.new_tag('img')
                img_tag['src'] = self.default_images[i % len(self.default_images)]
                img_tag['alt'] = self._generate_alt_text(title, i + 1)
                img_tag['style'] = "width: 100%; max-width: 600px; height: auto; margin: 15px 0; border-radius: 8px;"
                
                # Create paragraph wrapper
                p_tag = soup.new_tag('p')
                p_tag.append(img_tag)
                
                # Insert after H2
                h2_tags[i].insert_after(p_tag)
        
        return str(soup)
    
    def optimize_existing_images(self, content: str) -> str:
        """Optimize existing images in content.
        
        Args:
            content: HTML content
            
        Returns:
            Optimized HTML content
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        for img in soup.find_all('img'):
            # Add responsive styling if missing
            current_style = img.get('style', '')
            if 'width' not in current_style:
                base_style = "width: 100%; max-width: 600px; height: auto; margin: 15px 0; border-radius: 8px;"
                img['style'] = f"{current_style}; {base_style}".strip('; ')
            
            # Improve alt text if too short
            alt = img.get('alt', '')
            if len(alt) < 5:
                # Try to generate better alt text from surrounding context
                parent = img.parent
                if parent:
                    context = parent.get_text()[:100]
                    img['alt'] = f"Related image: {context[:50]}..."
        
        return str(soup)
    
    def _is_external_url(self, url: str) -> bool:
        """Check if URL is external."""
        if not url:
            return False
        return url.startswith('http') and 'spherevista360.com' not in url
    
    def _calculate_image_score(self, images: List[Dict]) -> Dict:
        """Calculate image quality score."""
        if not images:
            return {
                'score': 0,
                'max_score': 100,
                'percentage': 0,
                'grade': 'F'
            }
        
        # Scoring criteria
        has_images_score = 40 if images else 0  # 40% for having images
        alt_text_score = (sum(1 for img in images if img['has_alt']) / len(images)) * 30  # 30% for alt text
        accessibility_score = (sum(1 for img in images if img['is_accessible']) / len(images)) * 30  # 30% for accessibility
        
        total_score = has_images_score + alt_text_score + accessibility_score
        percentage = min(total_score, 100)
        
        # Grade calculation
        if percentage >= 90:
            grade = 'A+'
        elif percentage >= 80:
            grade = 'A'
        elif percentage >= 70:
            grade = 'B'
        elif percentage >= 60:
            grade = 'C'
        else:
            grade = 'F'
        
        return {
            'score': total_score,
            'max_score': 100,
            'percentage': percentage,
            'grade': grade,
            'breakdown': {
                'has_images': has_images_score,
                'alt_text': alt_text_score,
                'accessibility': accessibility_score
            }
        }
    
    def _get_image_recommendations(self, images: List[Dict], issues: List[str]) -> List[str]:
        """Get image optimization recommendations."""
        recommendations = []
        
        if not images:
            recommendations.append("Add images to improve content engagement")
        else:
            # Alt text recommendations
            images_without_alt = sum(1 for img in images if not img['has_alt'])
            if images_without_alt > 0:
                recommendations.append(f"Add alt text to {images_without_alt} images for accessibility")
            
            # Accessibility recommendations
            broken_images = sum(1 for img in images if img['src'] and not img['is_accessible'])
            if broken_images > 0:
                recommendations.append(f"Fix {broken_images} broken image links")
            
            # External image recommendations
            external_images = sum(1 for img in images if img['is_external'])
            if external_images > 0:
                recommendations.append(f"Consider hosting {external_images} external images locally")
        
        return recommendations
    
    def _generate_alt_text(self, title: str, image_number: int) -> str:
        """Generate appropriate alt text based on title and context."""
        # Clean title for alt text
        clean_title = re.sub(r'[^\w\s-]', '', title).strip()
        
        alt_templates = [
            f"Illustration related to {clean_title}",
            f"Visual representation of {clean_title}",
            f"Informative image about {clean_title}",
            f"Relevant graphic for {clean_title}"
        ]
        
        return alt_templates[(image_number - 1) % len(alt_templates)]


def validate_post_images(wp_client, post_id: int) -> Dict:
    """Validate images for a specific post.
    
    Args:
        wp_client: WordPress client instance
        post_id: Post ID
        
    Returns:
        Image validation results
    """
    validator = ImageValidator(wp_client)
    
    # Get post data
    post = wp_client.get_post(post_id)
    
    # Get full content
    content = wp_client.get_page_content(post['link'])
    
    return validator.validate_content_images(content, post['title']['rendered'])


def fix_post_images(wp_client, post_id: int, add_images: bool = True) -> bool:
    """Fix images for a specific post.
    
    Args:
        wp_client: WordPress client instance
        post_id: Post ID
        add_images: Whether to add images if missing
        
    Returns:
        True if successful
    """
    validator = ImageValidator(wp_client)
    
    try:
        # Get post data
        post = wp_client.get_post(post_id)
        original_content = post['content']['rendered']
        
        # Get current content validation
        validation = validator.validate_content_images(
            original_content, post['title']['rendered']
        )
        
        updated_content = original_content
        
        # Add images if needed and requested
        if validation['needs_images'] and add_images:
            updated_content = validator.add_images_to_content(
                updated_content, post['title']['rendered']
            )
        
        # Optimize existing images
        updated_content = validator.optimize_existing_images(updated_content)
        
        # Update post if content changed
        if updated_content != original_content:
            update_data = {
                'content': updated_content
            }
            wp_client.update_post(post_id, update_data)
            print(f"✅ Updated images for post {post_id}")
            return True
        else:
            print(f"ℹ️ No image updates needed for post {post_id}")
            return True
            
    except Exception as e:
        print(f"❌ Error fixing images for post {post_id}: {e}")
        return False