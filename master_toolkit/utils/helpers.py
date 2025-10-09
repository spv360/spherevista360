"""
Common Utilities
===============
Shared utilities for WordPress operations.
"""

import re
import time
from typing import Dict, List, Any, Optional
from datetime import datetime


def print_header(title: str, width: int = 50):
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f"🔧 {title}")
    print("=" * width)


def print_section(title: str, width: int = 40):
    """Print a formatted section."""
    print(f"\n📊 {title}")
    print("-" * width)


def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"⚠️ {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"ℹ️ {message}")


def format_percentage(value: float) -> str:
    """Format percentage with color coding."""
    if value >= 90:
        return f"🟢 {value:.1f}%"
    elif value >= 70:
        return f"🟡 {value:.1f}%"
    else:
        return f"🔴 {value:.1f}%"


def extract_urls_from_content(content: str) -> List[str]:
    """Extract all URLs from content."""
    url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+|[^\s<>"\']+\.[a-z]{2,}'
    return re.findall(url_pattern, content, re.IGNORECASE)


def extract_internal_links(content: str, domain: str = "spherevista360.com") -> List[str]:
    """Extract internal links from content."""
    pattern = rf'https?://{re.escape(domain)}[^\s<>"\'\)]*'
    return re.findall(pattern, content, re.IGNORECASE)


def clean_url(url: str) -> str:
    """Clean URL by removing trailing slashes and fragments."""
    url = url.rstrip('/')
    if '#' in url:
        url = url.split('#')[0]
    if '?' in url:
        url = url.split('?')[0]
    return url


def is_valid_url(url: str) -> bool:
    """Check if URL is valid format."""
    url_pattern = r'^https?://[^\s<>"\']+$'
    return bool(re.match(url_pattern, url))


def safe_get(data: Dict, path: str, default: Any = None) -> Any:
    """Safely get nested dictionary value using dot notation."""
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rstrip() + suffix


def get_timestamp() -> str:
    """Get current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def retry_operation(func, max_attempts: int = 3, delay: float = 1.0):
    """Retry an operation with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            time.sleep(delay * (2 ** attempt))


def validate_post_content(content: str) -> Dict[str, Any]:
    """Validate post content and return metrics."""
    if not content:
        return {
            'valid': False,
            'issues': ['Content is empty'],
            'word_count': 0,
            'char_count': 0
        }
    
    issues = []
    word_count = len(content.split())
    char_count = len(content)
    
    # Basic validation
    if word_count < 50:
        issues.append('Content is too short (< 50 words)')
    
    if char_count > 100000:
        issues.append('Content is very long (> 100k characters)')
    
    # Check for basic HTML issues
    if '<script' in content.lower():
        issues.append('Contains script tags')
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'word_count': word_count,
        'char_count': char_count
    }