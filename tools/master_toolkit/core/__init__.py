"""
Core Module
==========
Core WordPress functionality - client, authentication, and configuration.
"""

from .config import config, Config
from .auth import auth, WordPressAuth
from .client import WordPressClient, WordPressAPIError, create_client

__all__ = [
    'config',
    'Config', 
    'auth',
    'WordPressAuth',
    'WordPressClient',
    'WordPressAPIError',
    'create_client'
]