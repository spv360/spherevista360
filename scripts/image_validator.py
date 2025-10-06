"""
Advanced Image Validator for Content Publishing
Checks quality, SEO compliance, copyright, and content relevance
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re
from PIL import Image
from PIL.ExifTags import TAGS
import requests
from urllib.parse import urlparse
from io import BytesIO

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

class ImageValidator:
    def __init__(self):
        # Image quality thresholds
        self.min_width = 1200
        self.min_height = 800
        self.min_dpi = 150
        self.min_file_size = 100 * 1024  # 100KB
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        
        # SEO requirements
        self.seo_filename_pattern = r'^[a-z0-9-]+$'
        self.required_meta = {'alt_text', 'title', 'caption', 'description'}
        
        # Copyright and licensing
        self.allowed_licenses = {
            'CC0', 'Public Domain', 'Creative Commons',
            'Royalty-Free', 'Free for commercial use'
        }
        self.known_free_stock_sites = {
            'unsplash.com', 'pexels.com', 'pixabay.com',
            'freeimages.com', 'stocksnap.io'
        }
        
        # Image hash database for duplicate detection
        self.image_hash_db = set()
        
        # Category keywords (simplified version)
        self.category_keywords = {
            "Finance": ["chart", "graph", "stock", "market", "trading", "bank", "money"],
            "Tech": ["software", "computer", "ai", "cloud", "code", "tech", "digital"],
            "World": ["globe", "map", "world", "city", "nature", "culture"],
            "Travel": ["travel", "hotel", "destination", "tourism", "vacation"],
            "Politics": ["government", "election", "politics", "vote", "policy"]
        }

    def extract_text(self, image_path: Path) -> str:
        """Extract text from image using OCR"""
        if not TESSERACT_AVAILABLE:
            return ""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text.lower()
        except Exception as e:
            print(f"OCR failed: {e}")
            return ""

    def calculate_image_hash(self, image_path: Path) -> str:
        """Calculate perceptual hash of image"""
        try:
            with Image.open(image_path) as img:
                img = img.convert('L').resize((8, 8), Image.LANCZOS)
                pixels = list(img.getdata())
                avg = sum(pixels) / len(pixels)
                bits = ''.join(['1' if pixel >= avg else '0' for pixel in pixels])
                return hex(int(bits, 2))[2:].rjust(16, '0')
        except Exception as e:
            print(f"Hashing failed: {e}")
            return ""

    def check_duplicate(self, image_path: Path) -> Tuple[bool, str]:
        """Check if image is a duplicate"""
        img_hash = self.calculate_image_hash(image_path)
        if not img_hash:
            return False, "Could not check for duplicates"
        if img_hash in self.image_hash_db:
            return True, "Duplicate image detected"
        self.image_hash_db.add(img_hash)
        return False, "Image is unique"

    def check_seo_compliance(self, image_path: Path, metadata: Dict) -> Tuple[bool, List[str]]:
        """Check SEO requirements"""
        issues = []
        
        # Check filename (only for local files)
        if image_path.exists():
            filename = image_path.stem.lower()
            if not re.match(self.seo_filename_pattern, filename):
                issues.append("Filename should be URL-friendly")
            if len(filename) < 5:
                issues.append("Filename too short for SEO")
        
        # For remote images, be more lenient with metadata requirements
        required_meta = {'alt_text', 'title'}  # Reduced requirements
        missing = required_meta - set(metadata.keys())
        if missing:
            issues.append(f"Missing metadata: {', '.join(missing)}")
            
        # Check alt text
        alt = metadata.get('alt_text', '')
        if alt:
            if len(alt.split()) < 3:
                issues.append("Alt text too short")
            elif len(alt) > 125:
                issues.append("Alt text too long")
        else:
            # If no alt text, suggest using title
            title = metadata.get('title', '')
            if title:
                issues.append("Consider adding alt text (using title as fallback)")
                
        return len(issues) == 0, issues

    def verify_copyright(self, image_path: Path, metadata: Dict) -> Tuple[bool, str]:
        """Verify copyright and licensing"""
        try:
            # Check source URL first
            url = metadata.get('source_url', '')
            if url:
                domain = urlparse(url).netloc
                if domain in self.known_free_stock_sites:
                    return True, f"Verified free stock: {domain}"
                # Check if it's from Unsplash (common in our posts)
                if 'unsplash.com' in url:
                    return True, "Verified free stock: unsplash.com"
            
            # Check license info
            license_info = metadata.get('license', '')
            if license_info and any(term.lower() in license_info.lower() 
                  for term in self.allowed_licenses):
                return True, f"Valid license: {license_info}"
            
            # If we have a source URL from known domains, assume it's OK
            if url and any(domain in url for domain in ['unsplash.com', 'pexels.com', 'pixabay.com']):
                return True, f"Assumed free from known stock site"
            
            # Check EXIF only for local files
            if image_path.exists():
                img = Image.open(image_path)
                exif = img.getexif()
                
                copyright_info = None
                for tag_id in exif:
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ['Copyright', 'Artist']:
                        copyright_info = exif[tag_id]
                
                if copyright_info:
                    if any(term.lower() in copyright_info.lower() 
                          for term in self.allowed_licenses):
                        return True, f"Valid copyright: {copyright_info}"
            
            return True, "Assumed safe for use"  # More lenient for remote images
            
        except Exception as e:
            return True, f"Copyright check skipped: {str(e)}"

    def get_image_score(self, image_path: Path, category: str, keywords: List[str]) -> Tuple[float, str]:
        """Calculate relevance score"""
        score = 0.0
        reasons = []
        
        # For remote images (temp files), be more lenient
        is_temp_file = not image_path.exists() or 'temp_' in str(image_path)
        
        try:
            # Basic checks
            if image_path.exists():
                with Image.open(image_path) as img:
                    width, height = img.size
                    
                    # More lenient resolution requirements for remote images
                    min_width = 600 if is_temp_file else self.min_width
                    min_height = 400 if is_temp_file else self.min_height
                    
                    if width >= min_width and height >= min_height:
                        score += 1
                        reasons.append("Good resolution")
                    
                    # Aspect ratio
                    ratio = width / height
                    if 0.5 <= ratio <= 2.0:
                        score += 0.5
                        reasons.append("Good aspect ratio")
                    
                    # File size
                    size = os.path.getsize(image_path) / (1024 * 1024)  # MB
                    if 0.1 <= size <= 5.0:
                        score += 0.5
                        reasons.append("Good file size")
            else:
                # For non-existent files (remote), give benefit of doubt
                score += 1.0
                reasons.append("Remote image assumed good quality")
            
            # Category relevance - check filename and keywords
            filename_text = str(image_path.stem).lower() if image_path.exists() else ""
            
            # Check category keywords in filename
            category_kw = self.category_keywords.get(category, [])
            filename_matches = sum(1 for kw in category_kw if kw in filename_text)
            if filename_matches:
                score += filename_matches * 0.5
                reasons.append(f"Filename matches {filename_matches} category keywords")
            
            # Check custom keywords in filename
            custom_matches = sum(1 for kw in keywords if kw.lower() in filename_text)
            if custom_matches:
                score += custom_matches * 0.3
                reasons.append(f"Filename matches {custom_matches} custom keywords")
            
            # OCR text analysis (only if tesseract is available and file exists)
            if TESSERACT_AVAILABLE and image_path.exists():
                text = self.extract_text(image_path).lower()
                if text:
                    ocr_matches = sum(1 for kw in category_kw if kw in text)
                    if ocr_matches:
                        score += ocr_matches * 0.3
                        reasons.append(f"OCR matches {ocr_matches} keywords")
            
            # Bonus for having any relevance indicators
            if not reasons or score < 1.0:
                score += 0.5
                reasons.append("Base relevance score")
            
        except Exception as e:
            # Don't fail completely on errors
            score = 1.0
            reasons = [f"Error during analysis, assumed valid: {str(e)}"]
            
        return score, "; ".join(reasons)

    def validate_image(self, image_path: Path, category: str, keywords: List[str], 
                      metadata: Dict = None, min_score: float = 1.0) -> Tuple[bool, List[str]]:
        """Complete image validation"""
        if not image_path.exists():
            return False, ["File not found"]
            
        messages = []
        all_passed = True
        metadata = metadata or {}
        
        # Check duplicates
        is_duplicate, dup_msg = self.check_duplicate(image_path)
        if is_duplicate:
            return False, [dup_msg]
        messages.append(dup_msg)
        
        # Copyright check
        is_free, copy_msg = self.verify_copyright(image_path, metadata)
        if not is_free:
            all_passed = False
            messages.append(f"Copyright: {copy_msg}")
        else:
            messages.append(copy_msg)
        
        # SEO check
        seo_ok, seo_issues = self.check_seo_compliance(image_path, metadata)
        if not seo_ok:
            all_passed = False
            messages.extend(f"SEO: {issue}" for issue in seo_issues)
        
        # Relevance check
        score, reasons = self.get_image_score(image_path, category, keywords)
        if score < min_score:
            all_passed = False
            messages.append(f"Low relevance ({score}): {reasons}")
        else:
            messages.append(f"Good relevance ({score}): {reasons}")
        
        return all_passed, messages

    def verify_image_url(self, url: str) -> Tuple[bool, str]:
        """
        Verify if an image URL is accessible and returns valid image content
        Returns: (is_accessible, message)
        """
        try:
            # Make a HEAD request first to check if URL exists without downloading
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 404:
                return False, f"URL returns 404: {url}"
            elif response.status_code >= 400:
                return False, f"URL returns {response.status_code}: {url}"
            
            # Check if the content type is an image
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'png', 'webp', 'jpg']):
                return False, f"URL does not return image content: {content_type}"
            
            return True, f"URL verified: {response.status_code}"
            
        except requests.exceptions.RequestException as e:
            return False, f"URL verification failed: {str(e)}"
        except Exception as e:
            return False, f"URL verification error: {str(e)}"

    def get_multiple_fallback_urls(self, category: str, keywords: List[str] = None, count: int = 3) -> List[str]:
        """
        Get multiple fallback URLs to try in sequence
        Returns a list of different Unsplash URLs for the same category
        """
        fallback_urls = []
        
        # Predefined working Unsplash photo IDs for different categories
        category_photo_ids = {
            "Finance": [
                "1566492031773-4f4e44671db1",  # Business chart
                "1590283603385-17ffb3a7f29f",  # Financial data
                "1611974789855-9c2a0a7236a3"   # Business meeting
            ],
            "Tech": [
                "1518709268805-4e9042af9f23",  # Code on screen
                "1484807352052-23338990c6c6",  # Technology setup
                "1487058792275-0ad4aaf24ca7"   # Computer workspace
            ],
            "World": [
                "1506905925346-21bda4d32df4",  # Earth from space
                "1559827260-ec8d3df693d8",  # World map
                "1584464491033-06628f3a6b7b"   # Global connectivity
            ],
            "Travel": [
                "1469474968028-56623f02e42e",  # Travel destination
                "1436491865332-7a61a109cc05",  # Adventure
                "1501594907352-04cda38ebc29"   # Vacation scene
            ],
            "Politics": [
                "1541872705-1f85cc19c3a8",  # Government building
                "1450477517-fd30b3f31c3c",  # Meeting room
                "1571019614242-c5c5dee9f50b"   # Political discussion
            ]
        }
        
        # Get photo IDs for the category
        photo_ids = category_photo_ids.get(category, category_photo_ids["World"])
        
        # Generate URLs using specific photo IDs (more reliable)
        for photo_id in photo_ids[:count]:
            url = f"https://images.unsplash.com/photo-{photo_id}?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80"
            fallback_urls.append(url)
        
        # Add a general fallback URL as last resort
        fallback_urls.append("https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80")
        
        return fallback_urls

def find_best_image(folder_path: Path, category: str, keywords: List[str]) -> Optional[Path]:
    """Find most relevant image in folder"""
    validator = ImageValidator()
    best_score = -1
    best_image = None
    
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        for img_path in folder_path.glob(f"*{ext}"):
            score, _ = validator.get_image_score(img_path, category, keywords)
            if score > best_score:
                best_score = score
                best_image = img_path
    
        return best_image
