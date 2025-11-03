"""
WordPress Toolkit
================
Comprehensive WordPress content management and validation toolkit.

This toolkit provides:
- WordPress REST API client with authentication
- Content publishing from markdown files  
- Comprehensive validation (SEO, links, images)
- Automated fixing of common issues
- CLI tools for easy automation

Usage:
    from wordpress_toolkit import create_client, ContentWorkflow, ComprehensiveValidator
    
    # Authenticate and create client
    client = create_client()
    client.authenticate("username", "password")
    
    # Publish content with validation
    workflow = ContentWorkflow(client)
    result = workflow.publish_with_validation("article.md", category="technology")
    
    # Validate and fix existing content
    validator = ComprehensiveValidator(client)
    result = validator.quality_audit_workflow()
"""

__version__ = "1.0.0"
__author__ = "WordPress Toolkit"

# Core imports for easy access
from .core import create_client, WordPressClient, WordPressAPIError, config, auth
from .content import ContentPublisher, ContentWorkflow
from .validation import ComprehensiveValidator, LinkValidator, SEOValidator, ImageValidator
from .utils import print_header, print_success, print_error, print_warning

__all__ = [
    # Core
    'create_client',
    'WordPressClient', 
    'WordPressAPIError',
    'config',
    'auth',
    # Content
    'ContentPublisher',
    'ContentWorkflow',
    # Validation
    'ComprehensiveValidator',
    'LinkValidator',
    'SEOValidator', 
    'ImageValidator',
    # Utils
    'print_header',
    'print_success',
    'print_error',
    'print_warning'
]