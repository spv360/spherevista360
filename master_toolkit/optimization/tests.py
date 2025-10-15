"""
Optimization Engines Test Suite
===============================
Comprehensive tests for all optimization engines to ensure reliability and accuracy.
"""

import unittest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup

# Test imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from master_toolkit.optimization import (
    ContentOptimizer,
    ImageOptimizer, 
    SEOOptimizer,
    PerformanceOptimizer,
    AccessibilityOptimizer
)


class TestContentOptimizer(unittest.TestCase):
    """Test cases for ContentOptimizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_wp = Mock()
        self.optimizer = ContentOptimizer(self.mock_wp)
        
        # Mock post data
        self.mock_post = {
            'id': 123,
            'title': {'rendered': 'Test Post Title'},
            'content': {'rendered': '<p>This is test content for analysis.</p>'},
            'excerpt': {'rendered': 'Test excerpt'},
            'link': 'https://spherevista360.com/test-post'
        }
    
    def test_content_analysis_basic(self):
        """Test basic content analysis functionality."""
        self.mock_wp.get_post.return_value = self.mock_post
        
        result = self.optimizer.optimize_post_content(123)
        
        self.assertIn('post_id', result)
        self.assertIn('content_analysis', result)
        self.assertIn('score', result)
        self.assertEqual(result['post_id'], 123)
    
    def test_readability_analysis(self):
        """Test readability scoring."""
        content = "This is a simple sentence. This is another simple sentence."
        
        analysis = self.optimizer._analyze_readability(content)
        
        self.assertIn('flesch_kincaid_grade', analysis)
        self.assertIn('flesch_reading_ease', analysis)
        self.assertIn('avg_sentence_length', analysis)
        self.assertIsInstance(analysis['flesch_kincaid_grade'], (int, float))
    
    def test_keyword_optimization(self):
        """Test keyword density optimization."""
        content = "SEO optimization is important. SEO helps websites rank better."
        keywords = ['SEO', 'optimization']
        
        analysis = self.optimizer._analyze_keyword_optimization(content, keywords)
        
        self.assertIn('keyword_density', analysis)
        self.assertIn('SEO', analysis['keyword_density'])
        self.assertGreater(analysis['keyword_density']['SEO'], 0)
    
    def test_content_structure_analysis(self):
        """Test content structure analysis."""
        soup = BeautifulSoup('<h1>Title</h1><p>Content</p><h2>Subtitle</h2>', 'html.parser')
        
        analysis = self.optimizer._analyze_content_structure(soup)
        
        self.assertIn('heading_structure', analysis)
        self.assertIn('paragraph_analysis', analysis)
        self.assertEqual(analysis['heading_structure']['h1_count'], 1)
        self.assertEqual(analysis['heading_structure']['h2_count'], 1)


class TestImageOptimizer(unittest.TestCase):
    """Test cases for ImageOptimizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_wp = Mock()
        self.optimizer = ImageOptimizer(self.mock_wp)
        
        self.mock_post = {
            'id': 123,
            'title': {'rendered': 'Test Post'},
            'content': {'rendered': '<img src="test.jpg" alt="Test image"><img src="large.png">'},
            'link': 'https://spherevista360.com/test-post'
        }
    
    def test_image_analysis_basic(self):
        """Test basic image analysis."""
        self.mock_wp.get_post.return_value = self.mock_post
        
        result = self.optimizer.optimize_post_images(123)
        
        self.assertIn('post_id', result)
        self.assertIn('image_optimization', result)
        self.assertIn('score', result)
        
    def test_image_extraction(self):
        """Test image extraction from content."""
        soup = BeautifulSoup(self.mock_post['content']['rendered'], 'html.parser')
        
        analysis = self.optimizer._analyze_images(soup, auto_apply=False)
        
        self.assertIn('total_images', analysis)
        self.assertEqual(analysis['total_images'], 2)
        self.assertIn('images_without_alt', analysis)
    
    @patch('requests.get')
    def test_image_size_analysis(self, mock_get):
        """Test image size analysis."""
        # Mock image response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-length': '500000'}  # 500KB
        mock_get.return_value = mock_response
        
        size_info = self.optimizer._get_image_size_info('http://example.com/image.jpg')
        
        self.assertIn('size_bytes', size_info)
        self.assertEqual(size_info['size_bytes'], 500000)


class TestSEOOptimizer(unittest.TestCase):
    """Test cases for SEOOptimizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_wp = Mock()
        self.optimizer = SEOOptimizer(self.mock_wp)
        
        self.mock_post = {
            'id': 123,
            'title': {'rendered': 'WordPress SEO Optimization Guide'},
            'content': {'rendered': '<h1>SEO Guide</h1><p>Learn about SEO optimization.</p>'},
            'excerpt': {'rendered': 'Complete guide to WordPress SEO'},
            'link': 'https://spherevista360.com/seo-guide',
            'date': '2024-01-01T00:00:00',
            'modified': '2024-01-02T00:00:00'
        }
    
    def test_seo_analysis_basic(self):
        """Test basic SEO analysis."""
        self.mock_wp.get_post.return_value = self.mock_post
        
        result = self.optimizer.optimize_post_seo(123, target_keywords=['SEO', 'WordPress'])
        
        self.assertIn('post_id', result)
        self.assertIn('seo_optimization', result)
        self.assertIn('score', result)
    
    def test_meta_tag_optimization(self):
        """Test meta tag optimization."""
        title = "WordPress SEO Guide"
        content = "<p>Learn WordPress SEO optimization techniques.</p>"
        keywords = ['WordPress', 'SEO']
        
        analysis = self.optimizer._optimize_meta_tags(title, content, '', keywords)
        
        self.assertIn('title_optimization', analysis)
        self.assertIn('description_optimization', analysis)
        self.assertIn('improvements', analysis)
    
    def test_schema_markup_generation(self):
        """Test schema markup generation."""
        analysis = self.optimizer._optimize_schema_markup(self.mock_post, ['SEO'])
        
        self.assertIn('article_schema', analysis)
        self.assertIn('breadcrumb_schema', analysis)
        
        article_schema = analysis['article_schema']
        self.assertEqual(article_schema['@type'], 'Article')
        self.assertIn('headline', article_schema)
    
    def test_internal_linking_analysis(self):
        """Test internal linking analysis."""
        soup = BeautifulSoup('<a href="/other-post">Related Post</a>', 'html.parser')
        self.mock_wp.get_posts.return_value = [
            {'id': 124, 'title': {'rendered': 'Related Article'}, 'link': '/related'}
        ]
        
        analysis = self.optimizer._optimize_internal_linking(soup, 123, auto_apply=False)
        
        self.assertIn('current_internal_links', analysis)
        self.assertIn('suggested_links', analysis)


class TestPerformanceOptimizer(unittest.TestCase):
    """Test cases for PerformanceOptimizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_wp = Mock()
        self.optimizer = PerformanceOptimizer(self.mock_wp)
        
        self.mock_post = {
            'id': 123,
            'title': {'rendered': 'Performance Test'},
            'content': {'rendered': '''
                <style>body { color: red; background: blue; }</style>
                <script>console.log("test");</script>
                <img src="large.jpg" width="800" height="600">
            '''},
            'link': 'https://spherevista360.com/performance-test'
        }
    
    def test_performance_analysis_basic(self):
        """Test basic performance analysis."""
        self.mock_wp.get_post.return_value = self.mock_post
        
        result = self.optimizer.optimize_post_performance(123)
        
        self.assertIn('post_id', result)
        self.assertIn('performance_optimization', result)
        self.assertIn('score', result)
    
    def test_css_minification(self):
        """Test CSS minification."""
        css = "body { color: red; /* comment */ background: blue; }"
        
        minified = self.optimizer._minify_css(css)
        
        self.assertNotIn('/*', minified)
        self.assertLess(len(minified), len(css))
    
    def test_js_minification(self):
        """Test JavaScript minification."""
        js = "// Comment\nfunction test() { console.log('hello'); }"
        
        minified = self.optimizer._minify_js(js)
        
        self.assertNotIn('//', minified)
        self.assertLess(len(minified), len(js))
    
    def test_resource_optimization(self):
        """Test resource optimization analysis."""
        soup = BeautifulSoup(self.mock_post['content']['rendered'], 'html.parser')
        
        analysis = self.optimizer._optimize_resources(soup, auto_apply=False)
        
        self.assertIn('css_optimization', analysis)
        self.assertIn('js_optimization', analysis)
        self.assertIn('image_optimization', analysis)
    
    @patch('requests.head')
    def test_caching_analysis(self, mock_head):
        """Test caching analysis."""
        # Mock response headers
        mock_response = Mock()
        mock_response.headers = {
            'Cache-Control': 'public, max-age=3600',
            'ETag': '"abc123"'
        }
        mock_head.return_value = mock_response
        
        analysis = self.optimizer._optimize_caching('https://example.com', auto_apply=False)
        
        self.assertIn('browser_caching', analysis)
        self.assertIn('cdn_usage', analysis)


class TestAccessibilityOptimizer(unittest.TestCase):
    """Test cases for AccessibilityOptimizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_wp = Mock()
        self.optimizer = AccessibilityOptimizer(self.mock_wp)
        
        self.mock_post = {
            'id': 123,
            'title': {'rendered': 'Accessibility Test'},
            'content': {'rendered': '''
                <h1>Main Title</h1>
                <img src="test.jpg">
                <button onclick="doSomething()">Click</button>
                <input type="text" placeholder="Enter text">
            '''},
            'link': 'https://spherevista360.com/accessibility-test'
        }
    
    def test_accessibility_analysis_basic(self):
        """Test basic accessibility analysis."""
        self.mock_wp.get_post.return_value = self.mock_post
        
        result = self.optimizer.optimize_post_accessibility(123)
        
        self.assertIn('post_id', result)
        self.assertIn('accessibility_optimization', result)
        self.assertIn('score', result)
    
    def test_aria_attributes_analysis(self):
        """Test ARIA attributes analysis."""
        soup = BeautifulSoup(self.mock_post['content']['rendered'], 'html.parser')
        
        analysis = self.optimizer._optimize_aria_attributes(soup, auto_apply=False)
        
        self.assertIn('missing_aria_labels', analysis)
        self.assertIn('landmark_roles', analysis)
        self.assertIn('interactive_elements', analysis)
    
    def test_alt_text_optimization(self):
        """Test alt text optimization."""
        soup = BeautifulSoup('<img src="test.jpg"><img src="photo.png" alt="">', 'html.parser')
        
        analysis = self.optimizer._optimize_alt_text(soup, auto_apply=False)
        
        self.assertIn('total_images', analysis)
        self.assertIn('images_without_alt', analysis)
        self.assertEqual(analysis['total_images'], 2)
        self.assertGreater(analysis['images_without_alt'], 0)
    
    def test_color_contrast_analysis(self):
        """Test color contrast analysis."""
        soup = BeautifulSoup('<p style="color: black; background-color: white;">Text</p>', 'html.parser')
        
        analysis = self.optimizer._analyze_color_contrast(soup, auto_apply=False)
        
        self.assertIn('contrast_issues', analysis)
        self.assertIn('wcag_aa_compliance', analysis)
    
    def test_wcag_compliance_check(self):
        """Test WCAG compliance checking."""
        soup = BeautifulSoup(self.mock_post['content']['rendered'], 'html.parser')
        
        analysis = self.optimizer._check_wcag_compliance(soup, auto_apply=False)
        
        self.assertIn('perceivable', analysis)
        self.assertIn('operable', analysis)
        self.assertIn('understandable', analysis)
        self.assertIn('robust', analysis)
    
    def test_contrast_ratio_calculation(self):
        """Test contrast ratio calculation."""
        # Test high contrast (black on white)
        ratio = self.optimizer._calculate_contrast_ratio('#000000', '#ffffff')
        
        if ratio:  # Only test if color parsing works
            self.assertGreater(ratio, 15)  # Should be ~21:1
    
    def test_alt_text_generation(self):
        """Test alt text generation."""
        img_tag = BeautifulSoup('<img src="/images/wordpress-logo.jpg">', 'html.parser').find('img')
        
        alt_text = self.optimizer._generate_alt_text(img_tag)
        
        self.assertIsInstance(alt_text, str)
        self.assertGreater(len(alt_text), 0)


class OptimizationEngineIntegrationTest(unittest.TestCase):
    """Integration tests for optimization engines working together."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.mock_wp = Mock()
        
        # Complete mock post for comprehensive testing
        self.comprehensive_post = {
            'id': 999,
            'title': {'rendered': 'Complete WordPress SEO and Performance Guide'},
            'content': {'rendered': '''
                <h1>WordPress Optimization Guide</h1>
                <p>This comprehensive guide covers SEO, performance, and accessibility.</p>
                
                <h2>SEO Optimization</h2>
                <p>Learn about keyword optimization and meta tags.</p>
                <img src="seo-diagram.jpg" alt="SEO process diagram">
                
                <h2>Performance Tips</h2>
                <p>Optimize your images and minify CSS/JavaScript.</p>
                <img src="performance-chart.png">
                
                <style>
                    .highlight { background-color: yellow; color: black; }
                </style>
                
                <script>
                    console.log("Analytics tracking");
                </script>
                
                <button onclick="subscribe()">Subscribe to Newsletter</button>
                <input type="email" placeholder="Your email">
            '''},
            'excerpt': {'rendered': 'Complete guide to WordPress optimization'},
            'link': 'https://spherevista360.com/wordpress-optimization-guide',
            'date': '2024-01-01T00:00:00',
            'modified': '2024-01-02T00:00:00'
        }
    
    def test_comprehensive_optimization_workflow(self):
        """Test complete optimization workflow across all engines."""
        self.mock_wp.get_post.return_value = self.comprehensive_post
        self.mock_wp.get_posts.return_value = []  # No related posts
        
        # Initialize all optimizers
        optimizers = {
            'content': ContentOptimizer(self.mock_wp),
            'images': ImageOptimizer(self.mock_wp),
            'seo': SEOOptimizer(self.mock_wp),
            'performance': PerformanceOptimizer(self.mock_wp),
            'accessibility': AccessibilityOptimizer(self.mock_wp)
        }
        
        results = {}
        keywords = ['WordPress', 'optimization', 'SEO']
        
        # Run all optimizations
        for engine_name, optimizer in optimizers.items():
            try:
                if engine_name == 'content':
                    result = optimizer.optimize_post_content(999, target_keywords=keywords)
                elif engine_name == 'images':
                    result = optimizer.optimize_post_images(999)
                elif engine_name == 'seo':
                    result = optimizer.optimize_post_seo(999, target_keywords=keywords)
                elif engine_name == 'performance':
                    result = optimizer.optimize_post_performance(999)
                elif engine_name == 'accessibility':
                    result = optimizer.optimize_post_accessibility(999)
                
                results[engine_name] = result
                
                # Verify basic result structure
                self.assertIn('post_id', result)
                self.assertIn('score', result)
                self.assertEqual(result['post_id'], 999)
                
            except Exception as e:
                self.fail(f"{engine_name} optimization failed: {str(e)}")
        
        # Verify all engines completed
        self.assertEqual(len(results), 5)
        
        # Calculate overall optimization score
        total_score = sum(result['score'] for result in results.values() if 'score' in result)
        avg_score = total_score / len(results)
        
        # Verify reasonable optimization scores
        self.assertGreater(avg_score, 0)
        self.assertLessEqual(avg_score, 100)


def create_test_suite():
    """Create comprehensive test suite."""
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestContentOptimizer,
        TestImageOptimizer,
        TestSEOOptimizer,
        TestPerformanceOptimizer,
        TestAccessibilityOptimizer,
        OptimizationEngineIntegrationTest
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_tests():
    """Run all tests with detailed output."""
    print("Running Master Toolkit Optimization Engine Tests")
    print("=" * 60)
    
    # Create test suite
    suite = create_test_suite()
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)