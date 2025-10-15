#!/usr/bin/env python3
"""
Master Toolkit Optimization CLI
===============================
Command-line interface for WordPress content optimization engines.

Usage:
    python -m master_toolkit.optimization.cli optimize-content <post_id> [options]
    python -m master_toolkit.optimization.cli optimize-images <post_id> [options]
    python -m master_toolkit.optimization.cli optimize-seo <post_id> [options]
    python -m master_toolkit.optimization.cli optimize-performance <post_id> [options]
    python -m master_toolkit.optimization.cli optimize-accessibility <post_id> [options]
    python -m master_toolkit.optimization.cli optimize-all <post_id> [options]
    python -m master_toolkit.optimization.cli batch-optimize [options]

Examples:
    # Optimize single post content
    python -m master_toolkit.optimization.cli optimize-content 123 --auto-apply --keywords "wordpress,seo"
    
    # Optimize all aspects of a post
    python -m master_toolkit.optimization.cli optimize-all 123 --auto-apply --report-format json
    
    # Batch optimize multiple posts
    python -m master_toolkit.optimization.cli batch-optimize --post-ids 123,124,125 --engines content,seo
"""

import argparse
import json
import sys
import time
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from master_toolkit.optimization import (
    ContentOptimizer, 
    ImageOptimizer, 
    SEOOptimizer, 
    PerformanceOptimizer, 
    AccessibilityOptimizer
)
from master_toolkit.core import WordPressClient
from master_toolkit.utils import print_success, print_error, print_warning, print_info


class OptimizationCLI:
    """Command-line interface for optimization engines."""
    
    def __init__(self):
        """Initialize CLI with optimization engines."""
        try:
            self.wp = WordPressClient()
            self.optimizers = {
                'content': ContentOptimizer(self.wp),
                'images': ImageOptimizer(self.wp),
                'seo': SEOOptimizer(self.wp),
                'performance': PerformanceOptimizer(self.wp),
                'accessibility': AccessibilityOptimizer(self.wp)
            }
            self.available_engines = list(self.optimizers.keys())
        except Exception as e:
            print_error(f"Failed to initialize optimization engines: {str(e)}")
            sys.exit(1)
    
    def optimize_content(self, args) -> None:
        """Optimize content for a specific post."""
        print_info(f"Optimizing content for post {args.post_id}...")
        
        keywords = args.keywords.split(',') if args.keywords else None
        
        try:
            result = self.optimizers['content'].optimize_post_content(
                post_id=args.post_id,
                target_keywords=keywords,
                auto_apply=args.auto_apply
            )
            
            self._display_optimization_result('Content Optimization', result, args.report_format)
            
            if args.auto_apply and result.get('success', True):
                print_success(f"Content optimization applied to post {args.post_id}")
            
        except Exception as e:
            print_error(f"Content optimization failed: {str(e)}")
    
    def optimize_images(self, args) -> None:
        """Optimize images for a specific post."""
        print_info(f"Optimizing images for post {args.post_id}...")
        
        try:
            result = self.optimizers['images'].optimize_post_images(
                post_id=args.post_id,
                auto_apply=args.auto_apply
            )
            
            self._display_optimization_result('Image Optimization', result, args.report_format)
            
            if args.auto_apply and result.get('success', True):
                print_success(f"Image optimization applied to post {args.post_id}")
            
        except Exception as e:
            print_error(f"Image optimization failed: {str(e)}")
    
    def optimize_seo(self, args) -> None:
        """Optimize SEO for a specific post."""
        print_info(f"Optimizing SEO for post {args.post_id}...")
        
        keywords = args.keywords.split(',') if args.keywords else None
        
        try:
            result = self.optimizers['seo'].optimize_post_seo(
                post_id=args.post_id,
                target_keywords=keywords,
                auto_apply=args.auto_apply
            )
            
            self._display_optimization_result('SEO Optimization', result, args.report_format)
            
            if args.auto_apply and result.get('success', True):
                print_success(f"SEO optimization applied to post {args.post_id}")
            
        except Exception as e:
            print_error(f"SEO optimization failed: {str(e)}")
    
    def optimize_performance(self, args) -> None:
        """Optimize performance for a specific post."""
        print_info(f"Optimizing performance for post {args.post_id}...")
        
        try:
            result = self.optimizers['performance'].optimize_post_performance(
                post_id=args.post_id,
                auto_apply=args.auto_apply
            )
            
            self._display_optimization_result('Performance Optimization', result, args.report_format)
            
            if args.auto_apply and result.get('success', True):
                print_success(f"Performance optimization applied to post {args.post_id}")
            
        except Exception as e:
            print_error(f"Performance optimization failed: {str(e)}")
    
    def optimize_accessibility(self, args) -> None:
        """Optimize accessibility for a specific post."""
        print_info(f"Optimizing accessibility for post {args.post_id}...")
        
        try:
            result = self.optimizers['accessibility'].optimize_post_accessibility(
                post_id=args.post_id,
                auto_apply=args.auto_apply
            )
            
            self._display_optimization_result('Accessibility Optimization', result, args.report_format)
            
            if args.auto_apply and result.get('success', True):
                print_success(f"Accessibility optimization applied to post {args.post_id}")
            
        except Exception as e:
            print_error(f"Accessibility optimization failed: {str(e)}")
    
    def optimize_all(self, args) -> None:
        """Run all optimization engines for a specific post."""
        print_info(f"Running comprehensive optimization for post {args.post_id}...")
        
        keywords = args.keywords.split(',') if args.keywords else None
        all_results = {}
        optimization_summary = {
            'post_id': args.post_id,
            'engines_run': [],
            'overall_score': 0,
            'total_improvements': 0,
            'execution_time': 0
        }
        
        start_time = time.time()
        
        # Run each optimization engine
        engines_to_run = args.engines.split(',') if args.engines else self.available_engines
        
        for engine_name in engines_to_run:
            if engine_name not in self.available_engines:
                print_warning(f"Unknown engine: {engine_name}")
                continue
            
            print_info(f"Running {engine_name} optimization...")
            
            try:
                if engine_name == 'content':
                    result = self.optimizers[engine_name].optimize_post_content(
                        post_id=args.post_id, target_keywords=keywords, auto_apply=args.auto_apply
                    )
                elif engine_name == 'images':
                    result = self.optimizers[engine_name].optimize_post_images(
                        post_id=args.post_id, auto_apply=args.auto_apply
                    )
                elif engine_name == 'seo':
                    result = self.optimizers[engine_name].optimize_post_seo(
                        post_id=args.post_id, target_keywords=keywords, auto_apply=args.auto_apply
                    )
                elif engine_name == 'performance':
                    result = self.optimizers[engine_name].optimize_post_performance(
                        post_id=args.post_id, auto_apply=args.auto_apply
                    )
                elif engine_name == 'accessibility':
                    result = self.optimizers[engine_name].optimize_post_accessibility(
                        post_id=args.post_id, auto_apply=args.auto_apply
                    )
                
                all_results[engine_name] = result
                optimization_summary['engines_run'].append(engine_name)
                
                # Add to summary
                if 'score' in result:
                    optimization_summary['overall_score'] += result['score']
                
                # Count improvements
                improvements_key = self._get_improvements_key(engine_name)
                if improvements_key in result:
                    optimization_summary['total_improvements'] += len(result[improvements_key])
                
                print_success(f"{engine_name.title()} optimization completed (Score: {result.get('score', 'N/A')})")
                
            except Exception as e:
                print_error(f"{engine_name.title()} optimization failed: {str(e)}")
                all_results[engine_name] = {'error': str(e)}
        
        optimization_summary['execution_time'] = time.time() - start_time
        
        # Calculate average score
        if optimization_summary['engines_run']:
            optimization_summary['overall_score'] = int(
                optimization_summary['overall_score'] / len(optimization_summary['engines_run'])
            )
        
        # Display comprehensive results
        self._display_comprehensive_results(all_results, optimization_summary, args.report_format)
        
        if args.auto_apply:
            print_success(f"All optimizations applied to post {args.post_id}")
    
    def batch_optimize(self, args) -> None:
        """Run batch optimization on multiple posts."""
        print_info("Starting batch optimization...")
        
        # Get post IDs
        if args.post_ids:
            post_ids = [int(pid.strip()) for pid in args.post_ids.split(',')]
        else:
            # Get all published posts
            try:
                posts = self.wp.get_posts(status='publish', per_page=args.limit or 10)
                post_ids = [post['id'] for post in posts]
            except Exception as e:
                print_error(f"Failed to fetch posts: {str(e)}")
                return
        
        engines_to_run = args.engines.split(',') if args.engines else self.available_engines
        keywords = args.keywords.split(',') if args.keywords else None
        
        batch_results = {
            'total_posts': len(post_ids),
            'processed_posts': 0,
            'successful_optimizations': 0,
            'failed_optimizations': 0,
            'results': {}
        }
        
        print_info(f"Processing {len(post_ids)} posts with engines: {', '.join(engines_to_run)}")
        
        for i, post_id in enumerate(post_ids, 1):
            print_info(f"Processing post {post_id} ({i}/{len(post_ids)})...")
            
            post_results = {}
            post_success = True
            
            for engine_name in engines_to_run:
                try:
                    if engine_name == 'content':
                        result = self.optimizers[engine_name].optimize_post_content(
                            post_id=post_id, target_keywords=keywords, auto_apply=args.auto_apply
                        )
                    elif engine_name == 'images':
                        result = self.optimizers[engine_name].optimize_post_images(
                            post_id=post_id, auto_apply=args.auto_apply
                        )
                    elif engine_name == 'seo':
                        result = self.optimizers[engine_name].optimize_post_seo(
                            post_id=post_id, target_keywords=keywords, auto_apply=args.auto_apply
                        )
                    elif engine_name == 'performance':
                        result = self.optimizers[engine_name].optimize_post_performance(
                            post_id=post_id, auto_apply=args.auto_apply
                        )
                    elif engine_name == 'accessibility':
                        result = self.optimizers[engine_name].optimize_post_accessibility(
                            post_id=post_id, auto_apply=args.auto_apply
                        )
                    
                    post_results[engine_name] = result
                    
                except Exception as e:
                    print_error(f"Engine {engine_name} failed for post {post_id}: {str(e)}")
                    post_results[engine_name] = {'error': str(e)}
                    post_success = False
            
            batch_results['results'][post_id] = post_results
            batch_results['processed_posts'] += 1
            
            if post_success:
                batch_results['successful_optimizations'] += 1
                print_success(f"Post {post_id} optimized successfully")
            else:
                batch_results['failed_optimizations'] += 1
                print_warning(f"Post {post_id} had optimization issues")
            
            # Small delay to avoid overwhelming the server
            if i < len(post_ids):
                time.sleep(0.5)
        
        # Display batch results
        self._display_batch_results(batch_results, args.report_format)
    
    def _display_optimization_result(self, title: str, result: Dict[str, Any], 
                                   report_format: str = 'table') -> None:
        """Display optimization results in specified format."""
        if report_format == 'json':
            print(json.dumps(result, indent=2))
            return
        
        print(f"\n{'=' * 60}")
        print(f"{title} Results")
        print('=' * 60)
        
        if 'error' in result:
            print_error(f"Error: {result['error']}")
            return
        
        # Display basic info
        print(f"Post ID: {result.get('post_id', 'N/A')}")
        print(f"Post Title: {result.get('post_title', 'N/A')}")
        print(f"Overall Score: {result.get('score', 'N/A')}/100")
        print(f"Status: {result.get('status', 'N/A').upper()}")
        
        if 'message' in result:
            print(f"Message: {result['message']}")
        
        # Display improvements/recommendations
        improvements_key = self._get_improvements_key_from_result(result)
        if improvements_key and result.get(improvements_key):
            print(f"\n{improvements_key.replace('_', ' ').title()}:")
            for i, improvement in enumerate(result[improvements_key], 1):
                print(f"  {i}. {improvement}")
        
        print('=' * 60)
    
    def _display_comprehensive_results(self, all_results: Dict[str, Any], 
                                     summary: Dict[str, Any], 
                                     report_format: str = 'table') -> None:
        """Display comprehensive optimization results."""
        if report_format == 'json':
            output = {
                'summary': summary,
                'detailed_results': all_results
            }
            print(json.dumps(output, indent=2))
            return
        
        print(f"\n{'=' * 80}")
        print("COMPREHENSIVE OPTIMIZATION RESULTS")
        print('=' * 80)
        
        # Display summary
        print(f"Post ID: {summary['post_id']}")
        print(f"Engines Run: {', '.join(summary['engines_run'])}")
        print(f"Overall Score: {summary['overall_score']}/100")
        print(f"Total Improvements: {summary['total_improvements']}")
        print(f"Execution Time: {summary['execution_time']:.2f} seconds")
        
        # Display individual engine results
        print("\nIndividual Engine Results:")
        print("-" * 40)
        
        for engine_name, result in all_results.items():
            if 'error' in result:
                print(f"{engine_name.title()}: ERROR - {result['error']}")
            else:
                score = result.get('score', 'N/A')
                status = result.get('status', 'N/A')
                print(f"{engine_name.title()}: {score}/100 ({status.upper()})")
        
        print('=' * 80)
    
    def _display_batch_results(self, batch_results: Dict[str, Any], 
                             report_format: str = 'table') -> None:
        """Display batch optimization results."""
        if report_format == 'json':
            print(json.dumps(batch_results, indent=2))
            return
        
        print(f"\n{'=' * 80}")
        print("BATCH OPTIMIZATION RESULTS")
        print('=' * 80)
        
        print(f"Total Posts: {batch_results['total_posts']}")
        print(f"Processed: {batch_results['processed_posts']}")
        print(f"Successful: {batch_results['successful_optimizations']}")
        print(f"Failed: {batch_results['failed_optimizations']}")
        
        success_rate = (batch_results['successful_optimizations'] / 
                       batch_results['processed_posts'] * 100) if batch_results['processed_posts'] > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        print('=' * 80)
    
    def _get_improvements_key(self, engine_name: str) -> str:
        """Get the improvements key for a specific engine."""
        improvements_keys = {
            'content': 'improvements_summary',
            'images': 'optimization_summary',
            'seo': 'improvements_summary',
            'performance': 'recommendations',
            'accessibility': 'accessibility_summary'
        }
        return improvements_keys.get(engine_name, 'improvements')
    
    def _get_improvements_key_from_result(self, result: Dict[str, Any]) -> Optional[str]:
        """Get the improvements key from result structure."""
        possible_keys = [
            'improvements_summary', 'optimization_summary', 'recommendations', 
            'accessibility_summary', 'improvements'
        ]
        
        for key in possible_keys:
            if key in result and result[key]:
                return key
        
        return None


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description='WordPress Content Optimization CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Common arguments
    def add_common_args(sub_parser):
        sub_parser.add_argument('--auto-apply', action='store_true',
                               help='Automatically apply optimizations')
        sub_parser.add_argument('--report-format', choices=['table', 'json'], 
                               default='table', help='Output format')
        sub_parser.add_argument('--keywords', type=str,
                               help='Comma-separated target keywords')
    
    # Individual optimization commands
    content_parser = subparsers.add_parser('optimize-content', help='Optimize content')
    content_parser.add_argument('post_id', type=int, help='Post ID to optimize')
    add_common_args(content_parser)
    
    images_parser = subparsers.add_parser('optimize-images', help='Optimize images')
    images_parser.add_argument('post_id', type=int, help='Post ID to optimize')
    add_common_args(images_parser)
    
    seo_parser = subparsers.add_parser('optimize-seo', help='Optimize SEO')
    seo_parser.add_argument('post_id', type=int, help='Post ID to optimize')
    add_common_args(seo_parser)
    
    performance_parser = subparsers.add_parser('optimize-performance', help='Optimize performance')
    performance_parser.add_argument('post_id', type=int, help='Post ID to optimize')
    add_common_args(performance_parser)
    
    accessibility_parser = subparsers.add_parser('optimize-accessibility', help='Optimize accessibility')
    accessibility_parser.add_argument('post_id', type=int, help='Post ID to optimize')
    add_common_args(accessibility_parser)
    
    # Comprehensive optimization
    all_parser = subparsers.add_parser('optimize-all', help='Run all optimizations')
    all_parser.add_argument('post_id', type=int, help='Post ID to optimize')
    all_parser.add_argument('--engines', type=str,
                           help='Comma-separated list of engines to run')
    add_common_args(all_parser)
    
    # Batch optimization
    batch_parser = subparsers.add_parser('batch-optimize', help='Batch optimize multiple posts')
    batch_parser.add_argument('--post-ids', type=str,
                             help='Comma-separated post IDs')
    batch_parser.add_argument('--limit', type=int, default=10,
                             help='Maximum number of posts to process')
    batch_parser.add_argument('--engines', type=str,
                             help='Comma-separated list of engines to run')
    add_common_args(batch_parser)
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize CLI
    cli = OptimizationCLI()
    
    # Route to appropriate command
    command_map = {
        'optimize-content': cli.optimize_content,
        'optimize-images': cli.optimize_images,
        'optimize-seo': cli.optimize_seo,
        'optimize-performance': cli.optimize_performance,
        'optimize-accessibility': cli.optimize_accessibility,
        'optimize-all': cli.optimize_all,
        'batch-optimize': cli.batch_optimize
    }
    
    if args.command in command_map:
        try:
            command_map[args.command](args)
        except KeyboardInterrupt:
            print_warning("\nOperation cancelled by user")
            sys.exit(0)
        except Exception as e:
            print_error(f"Command failed: {str(e)}")
            sys.exit(1)
    else:
        print_error(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()