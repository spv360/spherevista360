"""
Optimization Module
==================
Automated optimization utilities for WordPress content including:
- Content optimization and enhancement
- Image optimization and compression
- Performance optimization
- SEO optimization algorithms
- Accessibility auto-fixes
- Advanced features: scheduling, batch processing, monitoring
"""

from .content import ContentOptimizer
from .images import ImageOptimizer
from .seo import SEOOptimizer
from .performance import PerformanceOptimizer
from .accessibility import AccessibilityOptimizer
from .advanced import (
    OptimizationScheduler,
    BatchOptimizationProcessor, 
    OptimizationMonitor,
    AdvancedReporting,
    AdvancedOptimizationManager
)

__all__ = [
    'ContentOptimizer',
    'ImageOptimizer', 
    'SEOOptimizer',
    'PerformanceOptimizer',
    'AccessibilityOptimizer',
    'OptimizationScheduler',
    'BatchOptimizationProcessor',
    'OptimizationMonitor',
    'AdvancedReporting',
    'AdvancedOptimizationManager'
]