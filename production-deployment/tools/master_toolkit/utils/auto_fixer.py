"""
Auto-Fixer Workflow
===================
Unified workflow to automatically fix website issues using all validation tools.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning
from ..validation.images import ImageValidator
from ..validation.seo import SEOValidator
from ..validation.content_quality import ContentQualityEnhancer


class AutoFixer:
    """Unified auto-fixer for website issues."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize auto-fixer with all validation tools."""
        self.wp = wp_client
        self.image_validator = ImageValidator(wp_client)
        self.seo_validator = SEOValidator(wp_client)
        self.content_enhancer = ContentQualityEnhancer(wp_client)
        
        # Issue priorities (higher = more critical)
        self.issue_priorities = {
            'missing_featured_image': 90,
            'broken_images': 85,
            'missing_alt_text': 70,
            'missing_meta_description': 80,
            'no_social_meta': 60,
            'no_schema_markup': 50,
            'poor_content_quality': 65,
            'no_internal_links': 55,
            'poor_structure': 60
        }

    def analyze_all_issues(self, post_ids: List[int] = None, per_page: int = 20) -> Dict[str, Any]:
        """Comprehensive analysis of all website issues."""
        try:
            if post_ids:
                posts_to_analyze = [{'id': pid} for pid in post_ids]
            else:
                # Get all published posts
                posts_to_analyze = self.wp.get_posts(
                    status='publish',
                    per_page=per_page,
                    orderby='date',
                    order='desc'
                )
            
            analysis_results = {
                'total_posts': len(posts_to_analyze),
                'posts_analyzed': [],
                'issue_summary': {
                    'missing_featured_image': [],
                    'broken_images': [],
                    'missing_alt_text': [],
                    'missing_meta_description': [],
                    'no_social_meta': [],
                    'no_schema_markup': [],
                    'poor_content_quality': [],
                    'no_internal_links': [],
                    'poor_structure': []
                },
                'severity_breakdown': {
                    'critical': [],    # Score < 40
                    'high': [],        # Score 40-60
                    'medium': [],      # Score 60-80
                    'low': []          # Score 80+
                },
                'timestamp': datetime.now().isoformat()
            }
            
            for post in posts_to_analyze:
                post_id = post['id']
                post_issues = []
                post_score = 100  # Start with perfect score
                
                try:
                    # Image analysis
                    image_check = self.image_validator.check_featured_image(post_id)
                    if not image_check.get('has_featured_image', False):
                        post_issues.append('missing_featured_image')
                        post_score -= 15
                        analysis_results['issue_summary']['missing_featured_image'].append(post_id)
                    
                    image_validation = self.image_validator.validate_post_images(post_id)
                    if image_validation.get('broken_images', 0) > 0:
                        post_issues.append('broken_images')
                        post_score -= 10
                        analysis_results['issue_summary']['broken_images'].append(post_id)
                    
                    if image_validation.get('images_without_alt', 0) > 0:
                        post_issues.append('missing_alt_text')
                        post_score -= 8
                        analysis_results['issue_summary']['missing_alt_text'].append(post_id)
                    
                    # SEO analysis
                    seo_validation = self.seo_validator.validate_post(post_id)
                    
                    # Check for meta description
                    post_meta = self.wp.get_post(post_id).get('meta', {})
                    if not post_meta.get('_yoast_wpseo_metadesc', ''):
                        post_issues.append('missing_meta_description')
                        post_score -= 12
                        analysis_results['issue_summary']['missing_meta_description'].append(post_id)
                    
                    # Check for social meta
                    if not post_meta.get('_yoast_wpseo_opengraph-title', ''):
                        post_issues.append('no_social_meta')
                        post_score -= 8
                        analysis_results['issue_summary']['no_social_meta'].append(post_id)
                    
                    # Check for schema markup
                    if not post_meta.get('_yoast_wpseo_schema_article_type', ''):
                        post_issues.append('no_schema_markup')
                        post_score -= 6
                        analysis_results['issue_summary']['no_schema_markup'].append(post_id)
                    
                    # Content quality analysis
                    content_analysis = self.content_enhancer.analyze_content_quality(post_id)
                    content_score = content_analysis.get('overall_score', 100)
                    
                    if content_score < 60:
                        post_issues.append('poor_content_quality')
                        post_score -= (80 - content_score) * 0.3
                        analysis_results['issue_summary']['poor_content_quality'].append(post_id)
                    
                    metrics = content_analysis.get('metrics', {})
                    if metrics.get('internal_links_count', 0) == 0:
                        post_issues.append('no_internal_links')
                        post_score -= 5
                        analysis_results['issue_summary']['no_internal_links'].append(post_id)
                    
                    if metrics.get('headings_count', 0) == 0 and metrics.get('word_count', 0) > 300:
                        post_issues.append('poor_structure')
                        post_score -= 7
                        analysis_results['issue_summary']['poor_structure'].append(post_id)
                    
                    # Categorize by severity
                    post_severity = self._get_severity(post_score)
                    analysis_results['severity_breakdown'][post_severity].append(post_id)
                    
                    analysis_results['posts_analyzed'].append({
                        'post_id': post_id,
                        'post_title': post.get('title', {}).get('rendered', 'Untitled'),
                        'issues': post_issues,
                        'issue_count': len(post_issues),
                        'overall_score': round(max(0, post_score), 2),
                        'severity': post_severity,
                        'content_score': content_score
                    })
                    
                except Exception as e:
                    analysis_results['posts_analyzed'].append({
                        'post_id': post_id,
                        'error': str(e)
                    })
            
            # Calculate totals
            analysis_results['total_issues'] = sum(len(issues) for issues in analysis_results['issue_summary'].values())
            analysis_results['posts_with_issues'] = len([p for p in analysis_results['posts_analyzed'] if p.get('issue_count', 0) > 0])
            
            # Priority ranking
            analysis_results['high_priority_posts'] = [
                p['post_id'] for p in analysis_results['posts_analyzed'] 
                if p.get('severity') in ['critical', 'high']
            ]
            
            return analysis_results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def fix_all_issues(self, post_ids: List[int] = None, per_page: int = 10, dry_run: bool = False, priority_only: bool = False) -> Dict[str, Any]:
        """Automatically fix all identified issues."""
        try:
            # First analyze issues
            analysis = self.analyze_all_issues(post_ids, per_page)
            
            if 'error' in analysis:
                return analysis
            
            # Determine which posts to fix
            if priority_only:
                posts_to_fix = analysis['high_priority_posts']
            else:
                posts_to_fix = [p['post_id'] for p in analysis['posts_analyzed'] if p.get('issue_count', 0) > 0]
            
            fix_results = {
                'analysis_summary': {
                    'total_posts_analyzed': analysis['total_posts'],
                    'total_issues_found': analysis['total_issues'],
                    'posts_with_issues': analysis['posts_with_issues']
                },
                'fix_summary': {
                    'posts_to_fix': len(posts_to_fix),
                    'posts_fixed': [],
                    'fixes_applied': {
                        'featured_images': 0,
                        'image_optimizations': 0,
                        'meta_descriptions': 0,
                        'social_meta': 0,
                        'schema_markup': 0,
                        'content_enhancements': 0
                    },
                    'errors': []
                },
                'detailed_results': [],
                'timestamp': datetime.now().isoformat()
            }
            
            for post_id in posts_to_fix:
                post_fixes = {
                    'post_id': post_id,
                    'fixes_applied': [],
                    'errors': []
                }
                
                try:
                    # Fix featured images
                    featured_result = self.image_validator.set_featured_image_from_content(post_id, dry_run=dry_run)
                    if featured_result.get('success', False):
                        post_fixes['fixes_applied'].append('featured_image')
                        fix_results['fix_summary']['fixes_applied']['featured_images'] += 1
                    elif 'error' in featured_result:
                        post_fixes['errors'].append(f"Featured image: {featured_result['error']}")
                    
                    # Fix image issues
                    image_result = self.image_validator.optimize_post_images(post_id, dry_run=dry_run)
                    if image_result.get('success', False):
                        post_fixes['fixes_applied'].append('image_optimization')
                        fix_results['fix_summary']['fixes_applied']['image_optimizations'] += 1
                    elif 'error' in image_result:
                        post_fixes['errors'].append(f"Image optimization: {image_result['error']}")
                    
                    # Fix SEO issues
                    meta_result = self.seo_validator.add_meta_description(post_id, dry_run=dry_run)
                    if meta_result.get('success', False):
                        post_fixes['fixes_applied'].append('meta_description')
                        fix_results['fix_summary']['fixes_applied']['meta_descriptions'] += 1
                    
                    social_result = self.seo_validator.add_social_meta_tags(post_id, dry_run=dry_run)
                    if social_result.get('success', False):
                        post_fixes['fixes_applied'].append('social_meta')
                        fix_results['fix_summary']['fixes_applied']['social_meta'] += 1
                    
                    schema_result = self.seo_validator.add_schema_markup(post_id, dry_run=dry_run)
                    if schema_result.get('success', False):
                        post_fixes['fixes_applied'].append('schema_markup')
                        fix_results['fix_summary']['fixes_applied']['schema_markup'] += 1
                    
                    # Fix content quality issues
                    content_result = self.content_enhancer.enhance_content_structure(post_id, dry_run=dry_run)
                    links_result = self.content_enhancer.add_internal_links(post_id, dry_run=dry_run)
                    
                    if content_result.get('success', False) or links_result.get('success', False):
                        post_fixes['fixes_applied'].append('content_enhancement')
                        fix_results['fix_summary']['fixes_applied']['content_enhancements'] += 1
                    
                    # Track fixed posts
                    if post_fixes['fixes_applied']:
                        fix_results['fix_summary']['posts_fixed'].append(post_id)
                    
                    fix_results['detailed_results'].append(post_fixes)
                    
                except Exception as e:
                    fix_results['fix_summary']['errors'].append({
                        'post_id': post_id,
                        'error': str(e)
                    })
            
            # Calculate summary statistics
            fix_results['fix_summary']['posts_fixed_count'] = len(fix_results['fix_summary']['posts_fixed'])
            fix_results['fix_summary']['total_fixes'] = sum(fix_results['fix_summary']['fixes_applied'].values())
            fix_results['fix_summary']['errors_count'] = len(fix_results['fix_summary']['errors'])
            
            if dry_run:
                fix_results['message'] = f"Dry run: Would fix {fix_results['fix_summary']['posts_fixed_count']} posts with {fix_results['fix_summary']['total_fixes']} total fixes"
            else:
                fix_results['message'] = f"Fixed {fix_results['fix_summary']['posts_fixed_count']} posts with {fix_results['fix_summary']['total_fixes']} total fixes"
            
            return fix_results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def fix_specific_issues(self, issue_types: List[str], post_ids: List[int] = None, per_page: int = 20, dry_run: bool = False) -> Dict[str, Any]:
        """Fix only specific types of issues."""
        try:
            # Get posts to process
            if post_ids:
                posts_to_process = post_ids
            else:
                analysis = self.analyze_all_issues(per_page=per_page)
                posts_to_process = []
                for issue_type in issue_types:
                    if issue_type in analysis['issue_summary']:
                        posts_to_process.extend(analysis['issue_summary'][issue_type])
                posts_to_process = list(set(posts_to_process))  # Remove duplicates
            
            fix_results = {
                'issue_types': issue_types,
                'posts_processed': len(posts_to_process),
                'fixes_applied': {},
                'posts_fixed': [],
                'errors': [],
                'detailed_results': []
            }
            
            for issue_type in issue_types:
                fix_results['fixes_applied'][issue_type] = 0
            
            for post_id in posts_to_process:
                post_fixes = []
                
                try:
                    for issue_type in issue_types:
                        if issue_type == 'missing_featured_image':
                            result = self.image_validator.set_featured_image_from_content(post_id, dry_run=dry_run)
                        elif issue_type == 'broken_images' or issue_type == 'missing_alt_text':
                            result = self.image_validator.optimize_post_images(post_id, dry_run=dry_run)
                        elif issue_type == 'missing_meta_description':
                            result = self.seo_validator.add_meta_description(post_id, dry_run=dry_run)
                        elif issue_type == 'no_social_meta':
                            result = self.seo_validator.add_social_meta_tags(post_id, dry_run=dry_run)
                        elif issue_type == 'no_schema_markup':
                            result = self.seo_validator.add_schema_markup(post_id, dry_run=dry_run)
                        elif issue_type == 'poor_content_quality' or issue_type == 'poor_structure':
                            result = self.content_enhancer.enhance_content_structure(post_id, dry_run=dry_run)
                        elif issue_type == 'no_internal_links':
                            result = self.content_enhancer.add_internal_links(post_id, dry_run=dry_run)
                        else:
                            continue
                        
                        if result.get('success', False):
                            post_fixes.append(issue_type)
                            fix_results['fixes_applied'][issue_type] += 1
                    
                    if post_fixes:
                        fix_results['posts_fixed'].append(post_id)
                    
                    fix_results['detailed_results'].append({
                        'post_id': post_id,
                        'fixes_applied': post_fixes
                    })
                    
                except Exception as e:
                    fix_results['errors'].append({
                        'post_id': post_id,
                        'error': str(e)
                    })
            
            fix_results['posts_fixed_count'] = len(fix_results['posts_fixed'])
            fix_results['total_fixes'] = sum(fix_results['fixes_applied'].values())
            
            if dry_run:
                fix_results['message'] = f"Dry run: Would apply {fix_results['total_fixes']} fixes to {fix_results['posts_fixed_count']} posts"
            else:
                fix_results['message'] = f"Applied {fix_results['total_fixes']} fixes to {fix_results['posts_fixed_count']} posts"
            
            return fix_results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_fix_report(self, results: Dict[str, Any], save_to_file: bool = True) -> str:
        """Generate a comprehensive fix report."""
        try:
            report_lines = []
            report_lines.append("Website Auto-Fix Report")
            report_lines.append("=" * 50)
            report_lines.append(f"Generated: {results.get('timestamp', datetime.now().isoformat())}")
            report_lines.append("")
            
            # Analysis summary
            if 'analysis_summary' in results:
                summary = results['analysis_summary']
                report_lines.append("Analysis Summary:")
                report_lines.append(f"  • Total posts analyzed: {summary.get('total_posts_analyzed', 0)}")
                report_lines.append(f"  • Total issues found: {summary.get('total_issues_found', 0)}")
                report_lines.append(f"  • Posts with issues: {summary.get('posts_with_issues', 0)}")
                report_lines.append("")
            
            # Fix summary
            if 'fix_summary' in results:
                fix_summary = results['fix_summary']
                report_lines.append("Fix Summary:")
                report_lines.append(f"  • Posts fixed: {fix_summary.get('posts_fixed_count', 0)}")
                
                fixes = fix_summary.get('fixes_applied', {})
                for fix_type, count in fixes.items():
                    if count > 0:
                        report_lines.append(f"  • {fix_type.replace('_', ' ').title()}: {count}")
                
                if fix_summary.get('errors_count', 0) > 0:
                    report_lines.append(f"  • Errors encountered: {fix_summary['errors_count']}")
                report_lines.append("")
            
            # Detailed results
            if 'detailed_results' in results:
                report_lines.append("Detailed Results:")
                for result in results['detailed_results'][:10]:  # Show first 10
                    post_id = result.get('post_id')
                    fixes = result.get('fixes_applied', [])
                    if fixes:
                        report_lines.append(f"  Post {post_id}: {', '.join(fixes)}")
                
                if len(results['detailed_results']) > 10:
                    report_lines.append(f"  ... and {len(results['detailed_results']) - 10} more posts")
                report_lines.append("")
            
            # Recommendations
            report_lines.append("Recommendations:")
            if results.get('fix_summary', {}).get('total_fixes', 0) > 0:
                report_lines.append("  • Run site health audit again to verify improvements")
                report_lines.append("  • Monitor site performance and SEO metrics")
                report_lines.append("  • Consider implementing automated fixing schedule")
            else:
                report_lines.append("  • No issues found or fixes needed")
            
            report_content = "\n".join(report_lines)
            
            if save_to_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"auto_fix_report_{timestamp}.txt"
                with open(filename, 'w') as f:
                    f.write(report_content)
                print_success(f"Report saved to {filename}")
            
            return report_content
            
        except Exception as e:
            return f"Error generating report: {str(e)}"

    def _get_severity(self, score: float) -> str:
        """Get severity level based on score."""
        if score < 40:
            return 'critical'
        elif score < 60:
            return 'high'
        elif score < 80:
            return 'medium'
        else:
            return 'low'

    def get_fix_recommendations(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get prioritized fix recommendations based on analysis."""
        try:
            recommendations = {
                'immediate_actions': [],
                'high_priority': [],
                'medium_priority': [],
                'low_priority': [],
                'estimated_time': {
                    'immediate': 0,
                    'high': 0,
                    'medium': 0,
                    'low': 0
                }
            }
            
            issue_summary = analysis_results.get('issue_summary', {})
            
            # Categorize by priority and estimate time
            for issue_type, post_ids in issue_summary.items():
                count = len(post_ids)
                if count == 0:
                    continue
                
                priority = self.issue_priorities.get(issue_type, 50)
                time_per_fix = {
                    'missing_featured_image': 2,
                    'broken_images': 3,
                    'missing_alt_text': 1,
                    'missing_meta_description': 2,
                    'no_social_meta': 1,
                    'no_schema_markup': 1,
                    'poor_content_quality': 10,
                    'no_internal_links': 5,
                    'poor_structure': 8
                }.get(issue_type, 5)
                
                total_time = count * time_per_fix
                
                recommendation = {
                    'issue_type': issue_type,
                    'affected_posts': count,
                    'estimated_time_minutes': total_time,
                    'description': self._get_issue_description(issue_type)
                }
                
                if priority >= 85:
                    recommendations['immediate_actions'].append(recommendation)
                    recommendations['estimated_time']['immediate'] += total_time
                elif priority >= 70:
                    recommendations['high_priority'].append(recommendation)
                    recommendations['estimated_time']['high'] += total_time
                elif priority >= 55:
                    recommendations['medium_priority'].append(recommendation)
                    recommendations['estimated_time']['medium'] += total_time
                else:
                    recommendations['low_priority'].append(recommendation)
                    recommendations['estimated_time']['low'] += total_time
            
            # Calculate total time
            recommendations['total_estimated_time'] = sum(recommendations['estimated_time'].values())
            
            return recommendations
            
        except Exception as e:
            return {
                'error': str(e)
            }

    def _get_issue_description(self, issue_type: str) -> str:
        """Get human-readable description of issue type."""
        descriptions = {
            'missing_featured_image': 'Posts without featured images affect social sharing and SEO',
            'broken_images': 'Broken images create poor user experience',
            'missing_alt_text': 'Missing alt text hurts accessibility and SEO',
            'missing_meta_description': 'Missing meta descriptions reduce click-through rates',
            'no_social_meta': 'Missing social media meta tags affect sharing appearance',
            'no_schema_markup': 'Schema markup helps search engines understand content',
            'poor_content_quality': 'Low-quality content affects user engagement and SEO',
            'no_internal_links': 'Internal links improve navigation and SEO',
            'poor_structure': 'Poor content structure affects readability'
        }
        return descriptions.get(issue_type, 'Issue affects website quality')