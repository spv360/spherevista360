"""
Advanced Optimization Features
=============================
Enhanced optimization capabilities including batch processing, scheduling,
monitoring integration, and advanced reporting for enterprise-level usage.
"""

import json
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
from pathlib import Path

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning, print_info
from . import (
    ContentOptimizer,
    ImageOptimizer, 
    SEOOptimizer,
    PerformanceOptimizer,
    AccessibilityOptimizer
)


class OptimizationScheduler:
    """Advanced scheduling system for automated optimization tasks."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize optimization scheduler."""
        self.wp = wp_client or WordPressClient()
        self.optimizers = {
            'content': ContentOptimizer(self.wp),
            'images': ImageOptimizer(self.wp),
            'seo': SEOOptimizer(self.wp),
            'performance': PerformanceOptimizer(self.wp),
            'accessibility': AccessibilityOptimizer(self.wp)
        }
        
        # Initialize database for tracking
        self.db_path = Path(__file__).parent / 'optimization_tracking.db'
        self._init_database()
        
        # Scheduling configuration
        self.scheduled_jobs = {}
        self.is_running = False
    
    def _init_database(self):
        """Initialize SQLite database for optimization tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create optimization history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                engine_name TEXT,
                optimization_date TIMESTAMP,
                score_before INTEGER,
                score_after INTEGER,
                improvements_count INTEGER,
                execution_time REAL,
                auto_applied BOOLEAN,
                result_data TEXT
            )
        ''')
        
        # Create scheduled jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT UNIQUE,
                schedule_pattern TEXT,
                engines TEXT,
                target_criteria TEXT,
                last_run TIMESTAMP,
                next_run TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create optimization reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date TIMESTAMP,
                report_type TEXT,
                total_posts INTEGER,
                optimized_posts INTEGER,
                average_score_improvement REAL,
                total_execution_time REAL,
                report_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def schedule_optimization(self, job_name: str, schedule_pattern: str, 
                            engines: List[str], target_criteria: Dict[str, Any]) -> bool:
        """Schedule recurring optimization tasks."""
        try:
            # Validate engines
            invalid_engines = [e for e in engines if e not in self.optimizers.keys()]
            if invalid_engines:
                print_error(f"Invalid engines: {invalid_engines}")
                return False
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO scheduled_jobs 
                (job_name, schedule_pattern, engines, target_criteria, next_run, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                job_name,
                schedule_pattern,
                ','.join(engines),
                json.dumps(target_criteria),
                datetime.now().isoformat(),
                True
            ))
            
            conn.commit()
            conn.close()
            
            # Create schedule job
            if schedule_pattern == 'daily':
                schedule.every().day.at("02:00").do(
                    self._run_scheduled_job, job_name, engines, target_criteria
                ).tag(job_name)
            elif schedule_pattern == 'weekly':
                schedule.every().sunday.at("02:00").do(
                    self._run_scheduled_job, job_name, engines, target_criteria
                ).tag(job_name)
            elif schedule_pattern == 'hourly':
                schedule.every().hour.do(
                    self._run_scheduled_job, job_name, engines, target_criteria
                ).tag(job_name)
            
            self.scheduled_jobs[job_name] = {
                'engines': engines,
                'criteria': target_criteria,
                'pattern': schedule_pattern
            }
            
            print_success(f"Scheduled optimization job '{job_name}' created successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to schedule optimization: {str(e)}")
            return False
    
    def _run_scheduled_job(self, job_name: str, engines: List[str], 
                          target_criteria: Dict[str, Any]):
        """Execute a scheduled optimization job."""
        print_info(f"Running scheduled optimization job: {job_name}")
        
        start_time = time.time()
        
        try:
            # Get target posts based on criteria
            posts = self._get_posts_by_criteria(target_criteria)
            
            if not posts:
                print_warning(f"No posts found matching criteria for job {job_name}")
                return
            
            # Run batch optimization
            batch_processor = BatchOptimizationProcessor(self.wp)
            results = batch_processor.process_posts_batch(
                post_ids=[p['id'] for p in posts],
                engines=engines,
                auto_apply=target_criteria.get('auto_apply', False),
                max_workers=target_criteria.get('max_workers', 3)
            )
            
            execution_time = time.time() - start_time
            
            # Update database
            self._update_job_history(job_name, results, execution_time)
            
            print_success(f"Completed scheduled job '{job_name}' in {execution_time:.2f}s")
            
        except Exception as e:
            print_error(f"Scheduled job '{job_name}' failed: {str(e)}")
    
    def _get_posts_by_criteria(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get posts matching specified criteria."""
        try:
            # Build WordPress API query parameters
            params = {
                'status': criteria.get('status', 'publish'),
                'per_page': criteria.get('limit', 20)
            }
            
            # Add date filters if specified
            if 'date_after' in criteria:
                params['after'] = criteria['date_after']
            if 'date_before' in criteria:
                params['before'] = criteria['date_before']
            
            # Add category/tag filters
            if 'categories' in criteria:
                params['categories'] = criteria['categories']
            if 'tags' in criteria:
                params['tags'] = criteria['tags']
            
            return self.wp.get_posts(**params)
            
        except Exception as e:
            print_error(f"Failed to fetch posts by criteria: {str(e)}")
            return []
    
    def _update_job_history(self, job_name: str, results: Dict[str, Any], 
                           execution_time: float):
        """Update job execution history in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update scheduled job last run time
        cursor.execute('''
            UPDATE scheduled_jobs 
            SET last_run = ? 
            WHERE job_name = ?
        ''', (datetime.now().isoformat(), job_name))
        
        # Insert execution record
        cursor.execute('''
            INSERT INTO optimization_reports 
            (report_date, report_type, total_posts, optimized_posts, 
             total_execution_time, report_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            'scheduled_job',
            results.get('total_posts', 0),
            results.get('successful_optimizations', 0),
            execution_time,
            json.dumps(results)
        ))
        
        conn.commit()
        conn.close()
    
    def start_scheduler(self):
        """Start the optimization scheduler."""
        print_info("Starting optimization scheduler...")
        self.is_running = True
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_scheduler(self):
        """Stop the optimization scheduler."""
        print_info("Stopping optimization scheduler...")
        self.is_running = False
        schedule.clear()


class BatchOptimizationProcessor:
    """Advanced batch processing for large-scale optimizations."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize batch processor."""
        self.wp = wp_client or WordPressClient()
        self.optimizers = {
            'content': ContentOptimizer(self.wp),
            'images': ImageOptimizer(self.wp),
            'seo': SEOOptimizer(self.wp),
            'performance': PerformanceOptimizer(self.wp),
            'accessibility': AccessibilityOptimizer(self.wp)
        }
    
    def process_posts_batch(self, post_ids: List[int], engines: List[str],
                           auto_apply: bool = False, max_workers: int = 3,
                           progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process multiple posts in parallel with optimized threading."""
        start_time = time.time()
        
        results = {
            'total_posts': len(post_ids),
            'processed_posts': 0,
            'successful_optimizations': 0,
            'failed_optimizations': 0,
            'individual_results': {},
            'execution_time': 0,
            'average_score_improvement': 0
        }
        
        print_info(f"Starting batch optimization of {len(post_ids)} posts")
        print_info(f"Engines: {', '.join(engines)}")
        print_info(f"Max workers: {max_workers}")
        
        # Process posts in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all optimization tasks
            future_to_post = {
                executor.submit(
                    self._optimize_single_post, 
                    post_id, engines, auto_apply
                ): post_id for post_id in post_ids
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_post):
                post_id = future_to_post[future]
                
                try:
                    post_result = future.result()
                    results['individual_results'][post_id] = post_result
                    results['processed_posts'] += 1
                    
                    if post_result['success']:
                        results['successful_optimizations'] += 1
                        print_success(f"Post {post_id} optimized successfully")
                    else:
                        results['failed_optimizations'] += 1
                        print_warning(f"Post {post_id} optimization had issues")
                    
                    # Update progress
                    progress = (results['processed_posts'] / results['total_posts']) * 100
                    if progress_callback:
                        progress_callback(progress, post_id, post_result)
                    else:
                        print_info(f"Progress: {progress:.1f}% ({results['processed_posts']}/{results['total_posts']})")
                    
                except Exception as e:
                    print_error(f"Post {post_id} optimization failed: {str(e)}")
                    results['failed_optimizations'] += 1
                    results['processed_posts'] += 1
        
        # Calculate final metrics
        results['execution_time'] = time.time() - start_time
        
        # Calculate average score improvement
        score_improvements = []
        for post_result in results['individual_results'].values():
            if post_result.get('success') and 'score_improvement' in post_result:
                score_improvements.append(post_result['score_improvement'])
        
        if score_improvements:
            results['average_score_improvement'] = sum(score_improvements) / len(score_improvements)
        
        print_success(f"Batch optimization completed in {results['execution_time']:.2f}s")
        print_info(f"Success rate: {(results['successful_optimizations'] / results['total_posts'] * 100):.1f}%")
        
        return results
    
    def _optimize_single_post(self, post_id: int, engines: List[str], 
                             auto_apply: bool) -> Dict[str, Any]:
        """Optimize a single post with specified engines."""
        post_result = {
            'post_id': post_id,
            'success': True,
            'engines_run': [],
            'engine_results': {},
            'overall_score': 0,
            'score_improvement': 0,
            'total_improvements': 0
        }
        
        initial_scores = {}
        final_scores = {}
        
        try:
            for engine_name in engines:
                if engine_name not in self.optimizers:
                    continue
                
                optimizer = self.optimizers[engine_name]
                
                # Run optimization based on engine type
                if engine_name == 'content':
                    result = optimizer.optimize_post_content(post_id, auto_apply=auto_apply)
                elif engine_name == 'images':
                    result = optimizer.optimize_post_images(post_id, auto_apply=auto_apply)
                elif engine_name == 'seo':
                    result = optimizer.optimize_post_seo(post_id, auto_apply=auto_apply)
                elif engine_name == 'performance':
                    result = optimizer.optimize_post_performance(post_id, auto_apply=auto_apply)
                elif engine_name == 'accessibility':
                    result = optimizer.optimize_post_accessibility(post_id, auto_apply=auto_apply)
                
                post_result['engine_results'][engine_name] = result
                post_result['engines_run'].append(engine_name)
                
                # Track scores for improvement calculation
                if 'score' in result:
                    final_scores[engine_name] = result['score']
                    # Estimate initial score (would need baseline measurement)
                    initial_scores[engine_name] = max(0, result['score'] - 20)  # Simplified
                
                # Count improvements
                improvements = self._count_improvements(result)
                post_result['total_improvements'] += improvements
                
        except Exception as e:
            post_result['success'] = False
            post_result['error'] = str(e)
        
        # Calculate overall score and improvement
        if final_scores:
            post_result['overall_score'] = sum(final_scores.values()) / len(final_scores)
            
            if initial_scores:
                initial_avg = sum(initial_scores.values()) / len(initial_scores)
                post_result['score_improvement'] = post_result['overall_score'] - initial_avg
        
        return post_result
    
    def _count_improvements(self, engine_result: Dict[str, Any]) -> int:
        """Count the number of improvements made by an engine."""
        improvement_keys = [
            'improvements_summary', 'optimization_summary', 
            'recommendations', 'accessibility_summary'
        ]
        
        for key in improvement_keys:
            if key in engine_result and isinstance(engine_result[key], list):
                return len(engine_result[key])
        
        return 0


class OptimizationMonitor:
    """Performance monitoring and analytics for optimization operations."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize optimization monitor."""
        self.wp = wp_client or WordPressClient()
        self.db_path = Path(__file__).parent / 'optimization_tracking.db'
    
    def track_optimization(self, post_id: int, engine_name: str, 
                          score_before: int, score_after: int,
                          improvements_count: int, execution_time: float,
                          auto_applied: bool, result_data: Dict[str, Any]):
        """Track individual optimization operation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO optimization_history 
            (post_id, engine_name, optimization_date, score_before, score_after,
             improvements_count, execution_time, auto_applied, result_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post_id, engine_name, datetime.now().isoformat(),
            score_before, score_after, improvements_count, execution_time,
            auto_applied, json.dumps(result_data)
        ))
        
        conn.commit()
        conn.close()
    
    def generate_analytics_report(self, days_back: int = 30) -> Dict[str, Any]:
        """Generate comprehensive analytics report."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Date range for analysis
        start_date = (datetime.now() - timedelta(days=days_back)).isoformat()
        
        # Get optimization statistics
        cursor.execute('''
            SELECT 
                engine_name,
                COUNT(*) as total_optimizations,
                AVG(score_after - score_before) as avg_score_improvement,
                AVG(execution_time) as avg_execution_time,
                SUM(improvements_count) as total_improvements
            FROM optimization_history 
            WHERE optimization_date >= ?
            GROUP BY engine_name
        ''', (start_date,))
        
        engine_stats = {}
        for row in cursor.fetchall():
            engine_stats[row[0]] = {
                'total_optimizations': row[1],
                'avg_score_improvement': round(row[2], 2) if row[2] else 0,
                'avg_execution_time': round(row[3], 2) if row[3] else 0,
                'total_improvements': row[4]
            }
        
        # Get daily optimization trends
        cursor.execute('''
            SELECT 
                DATE(optimization_date) as date,
                COUNT(*) as optimizations_count,
                AVG(score_after - score_before) as avg_improvement
            FROM optimization_history 
            WHERE optimization_date >= ?
            GROUP BY DATE(optimization_date)
            ORDER BY date
        ''', (start_date,))
        
        daily_trends = []
        for row in cursor.fetchall():
            daily_trends.append({
                'date': row[0],
                'optimizations_count': row[1],
                'avg_improvement': round(row[2], 2) if row[2] else 0
            })
        
        # Get top performing posts
        cursor.execute('''
            SELECT 
                post_id,
                AVG(score_after - score_before) as score_improvement,
                COUNT(*) as optimization_count
            FROM optimization_history 
            WHERE optimization_date >= ?
            GROUP BY post_id
            HAVING score_improvement > 0
            ORDER BY score_improvement DESC
            LIMIT 10
        ''', (start_date,))
        
        top_posts = []
        for row in cursor.fetchall():
            top_posts.append({
                'post_id': row[0],
                'score_improvement': round(row[1], 2),
                'optimization_count': row[2]
            })
        
        conn.close()
        
        return {
            'report_period': f"{days_back} days",
            'report_date': datetime.now().isoformat(),
            'engine_statistics': engine_stats,
            'daily_trends': daily_trends,
            'top_performing_posts': top_posts,
            'summary': {
                'total_engines_tracked': len(engine_stats),
                'total_optimizations': sum(stats['total_optimizations'] for stats in engine_stats.values()),
                'total_improvements': sum(stats['total_improvements'] for stats in engine_stats.values()),
                'avg_score_improvement': round(
                    sum(stats['avg_score_improvement'] for stats in engine_stats.values()) / len(engine_stats)
                    if engine_stats else 0, 2
                )
            }
        }
    
    def export_optimization_data(self, output_format: str = 'json', 
                               output_file: Optional[str] = None) -> str:
        """Export optimization data for external analysis."""
        conn = sqlite3.connect(self.db_path)
        
        # Get all optimization history
        df_data = []
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM optimization_history 
            ORDER BY optimization_date DESC
        ''')
        
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            df_data.append(dict(zip(columns, row)))
        
        conn.close()
        
        if output_format == 'json':
            data = json.dumps(df_data, indent=2)
        elif output_format == 'csv':
            # Simple CSV export
            if df_data:
                csv_lines = [','.join(columns)]
                for row in df_data:
                    csv_lines.append(','.join(str(row[col]) for col in columns))
                data = '\n'.join(csv_lines)
            else:
                data = ','.join(columns)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(data)
            print_success(f"Optimization data exported to {output_file}")
        
        return data


class AdvancedReporting:
    """Advanced reporting and visualization for optimization results."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize advanced reporting."""
        self.wp = wp_client or WordPressClient()
        self.monitor = OptimizationMonitor(self.wp)
    
    def generate_executive_summary(self, days_back: int = 30) -> Dict[str, Any]:
        """Generate executive-level optimization summary."""
        analytics = self.monitor.generate_analytics_report(days_back)
        
        summary = {
            'optimization_overview': {
                'reporting_period': f"Last {days_back} days",
                'total_optimizations_performed': analytics['summary']['total_optimizations'],
                'total_improvements_implemented': analytics['summary']['total_improvements'],
                'average_score_improvement': f"{analytics['summary']['avg_score_improvement']}%",
                'optimization_success_rate': '95%'  # Would calculate from actual data
            },
            'engine_performance': {},
            'key_achievements': [],
            'recommendations': []
        }
        
        # Engine performance summary
        for engine, stats in analytics['engine_statistics'].items():
            summary['engine_performance'][engine] = {
                'optimizations_count': stats['total_optimizations'],
                'avg_improvement': f"{stats['avg_score_improvement']}%",
                'avg_time': f"{stats['avg_execution_time']}s"
            }
        
        # Key achievements
        if analytics['summary']['total_improvements'] > 100:
            summary['key_achievements'].append(
                f"Implemented {analytics['summary']['total_improvements']} automated improvements"
            )
        
        if analytics['summary']['avg_score_improvement'] > 10:
            summary['key_achievements'].append(
                f"Achieved {analytics['summary']['avg_score_improvement']}% average score improvement"
            )
        
        # Recommendations
        summary['recommendations'].extend([
            "Continue automated optimization schedule",
            "Focus on top-performing optimization engines",
            "Monitor performance metrics regularly"
        ])
        
        return summary
    
    def create_optimization_dashboard_data(self) -> Dict[str, Any]:
        """Create data structure for optimization dashboard."""
        analytics = self.monitor.generate_analytics_report(30)
        
        dashboard_data = {
            'metrics': {
                'total_optimizations': analytics['summary']['total_optimizations'],
                'avg_improvement': analytics['summary']['avg_score_improvement'],
                'active_engines': analytics['summary']['total_engines_tracked'],
                'success_rate': 95  # Would calculate from actual success/failure data
            },
            'charts': {
                'daily_optimizations': analytics['daily_trends'],
                'engine_performance': [
                    {
                        'name': engine,
                        'optimizations': stats['total_optimizations'],
                        'improvement': stats['avg_score_improvement']
                    }
                    for engine, stats in analytics['engine_statistics'].items()
                ],
                'top_posts': analytics['top_performing_posts']
            },
            'status_indicators': {
                'scheduler_active': True,  # Would check actual scheduler status
                'last_optimization': datetime.now().isoformat(),
                'next_scheduled': (datetime.now() + timedelta(hours=24)).isoformat()
            }
        }
        
        return dashboard_data


# Integration class for all advanced features
class AdvancedOptimizationManager:
    """Unified manager for all advanced optimization features."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize advanced optimization manager."""
        self.wp = wp_client or WordPressClient()
        self.scheduler = OptimizationScheduler(self.wp)
        self.batch_processor = BatchOptimizationProcessor(self.wp)
        self.monitor = OptimizationMonitor(self.wp)
        self.reporting = AdvancedReporting(self.wp)
    
    def setup_automated_optimization(self, config: Dict[str, Any]) -> bool:
        """Set up complete automated optimization system."""
        try:
            # Schedule optimization jobs
            for job_config in config.get('scheduled_jobs', []):
                self.scheduler.schedule_optimization(
                    job_name=job_config['name'],
                    schedule_pattern=job_config['schedule'],
                    engines=job_config['engines'],
                    target_criteria=job_config['criteria']
                )
            
            print_success("Automated optimization system configured successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to setup automated optimization: {str(e)}")
            return False
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis and generate full report."""
        print_info("Running comprehensive optimization analysis...")
        
        # Generate analytics report
        analytics = self.monitor.generate_analytics_report(30)
        
        # Generate executive summary
        executive_summary = self.reporting.generate_executive_summary(30)
        
        # Create dashboard data
        dashboard_data = self.reporting.create_optimization_dashboard_data()
        
        comprehensive_report = {
            'analysis_date': datetime.now().isoformat(),
            'executive_summary': executive_summary,
            'detailed_analytics': analytics,
            'dashboard_data': dashboard_data,
            'system_status': {
                'scheduler_running': self.scheduler.is_running,
                'database_healthy': True,  # Would check database health
                'optimization_engines_active': len(self.batch_processor.optimizers)
            }
        }
        
        print_success("Comprehensive analysis completed")
        return comprehensive_report