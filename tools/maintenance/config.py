"""
Core Configuration Module
=========================
Centralized configuration management for WordPress Toolkit.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for WordPress operations."""
    
    def __init__(self):
        """Initialize configuration with defaults."""
        self.config = {
            'base_url': 'https://spherevista360.com',
            'api_endpoint': '/wp-json/wp/v2',
            'timeout': 30,
            'retry_attempts': 3,
            'user_agent': 'WordPress-Toolkit/1.0',
            'per_page_limit': 100,
            'default_status': 'publish'
        }
        
        # Load from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'WP_BASE_URL': 'base_url',
            'WP_TIMEOUT': 'timeout',
            'WP_USER_AGENT': 'user_agent'
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Convert numeric values
                if config_key in ['timeout', 'retry_attempts', 'per_page_limit']:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                self.config[config_key] = value
        
        # Check for AIOpsVista specific configuration
        aiops_url = os.getenv('AIOPSVISTA_BASE_URL')
        if aiops_url:
            self.config['aiopsvista_base_url'] = aiops_url
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values."""
        self.config.update(updates)
    
    def get_api_url(self, endpoint: str = '') -> str:
        """Get full API URL for endpoint."""
        base = self.config['base_url'].rstrip('/')
        api = self.config['api_endpoint'].strip('/')
        endpoint = endpoint.lstrip('/')
        
        if endpoint:
            return f"{base}/{api}/{endpoint}"
        return f"{base}/{api}"


# Global configuration instance
config = Config()