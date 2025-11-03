"""
Comprehensive Validation Suite
==============================
Unified validation system combining SEO, links, images, and content quality.
"""

from typing import Dict, List, Any, Optional
from ..core import WordPressClient, WordPressAPIError
from ..utils import print_header, print_section, print_success, print_error, ResultFormatter
from .links import LinkValidator
from .images import ImageValidator
from .seo import SEOValidator


class ComprehensiveValidator:
    """Comprehensive validation combining all validation types."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize comprehensive validator."""
        self.wp = wp_client or WordPressClient()
        self.link_validator = LinkValidator(self.wp)
        self.image_validator = ImageValidator(self.wp)
        self.seo_validator = SEOValidator(self.wp)
    
    def validate_post_comprehensive(self, post_id: int) -> Dict[str, Any]:
        """Run comprehensive validation on a single post."""
        try:
            post = self.wp.get_post(post_id)
            post_title = post['title']['rendered']
            
            print_section(f"Validating Post {post_id}: {post_title}")
            
            # Run all validations
            seo_result = self.seo_validator.validate_post(post_id)
            link_result = self.link_validator.validate_post_links(post_id)
            image_result = self.image_validator.validate_post_images(post_id)
            
            # Calculate overall scores
            seo_score = seo_result.get('score', 0) if 'error' not in seo_result else 0
            
            # Link score (percentage of valid links)
            link_score = 0
            if 'error' not in link_result and link_result['total_links'] > 0:
                link_score = (len(link_result['valid_links']) / link_result['total_links']) * 100
            elif link_result['total_links'] == 0:
                link_score = 100  # No links is okay
            
            # Image score (percentage of valid images with alt text)
            image_score = 0
            if 'error' not in image_result and image_result['total_images'] > 0:
                valid_with_alt = sum(1 for img in image_result['validation_results'] 
                                   if img['valid'] and img['has_alt'])
                image_score = (valid_with_alt / image_result['total_images']) * 100
            elif image_result['total_images'] == 0:
                image_score = 100  # No images is okay
            
            # Overall score (weighted average)
            overall_score = (seo_score * 0.4) + (link_score * 0.3) + (image_score * 0.3)
            
            return {
                'post_id': post_id,
                'post_title': post_title,
                'overall_score': round(overall_score, 1),
                'seo': seo_result,
                'links': link_result,
                'images': image_result,
                'summary': {
                    'seo_score': round(seo_score, 1),
                    'link_score': round(link_score, 1),
                    'image_score': round(image_score, 1),
                    'total_issues': self._count_total_issues(seo_result, link_result, image_result),
                    'needs_attention': overall_score < 70
                }
            }
            
        except Exception as e:
            return {
                'post_id': post_id,
                'error': str(e)
            }
    
    def validate_multiple_posts(self, post_ids: List[int] = None, per_page: int = 10) -> Dict[str, Any]:
        """Run comprehensive validation on multiple posts."""
        print_header("Comprehensive Post Validation")
        
        if post_ids:
            posts_to_validate = [{'id': pid} for pid in post_ids]
        else:
            try:
                posts_to_validate = self.wp.get_posts(per_page=per_page)
            except Exception as e:
                return {'error': f'Failed to get posts: {e}'}
        
        results = {
            'total_posts': len(posts_to_validate),
            'validated_posts': 0,
            'average_score': 0,
            'posts_needing_attention': 0,
            'validation_results': []
        }
        
        total_score = 0
        
        for post in posts_to_validate:
            post_id = post['id']
            validation = self.validate_post_comprehensive(post_id)
            
            if 'error' not in validation:
                results['validated_posts'] += 1
                total_score += validation['overall_score']
                
                if validation['summary']['needs_attention']:
                    results['posts_needing_attention'] += 1
                
                results['validation_results'].append(validation)
                
                # Progress indicator
                print(f"✅ Post {post_id}: {validation['overall_score']:.1f}% overall")
            else:
                print_error(f"Failed to validate post {post_id}: {validation['error']}")
        
        if results['validated_posts'] > 0:
            results['average_score'] = round(total_score / results['validated_posts'], 1)
        
        self._print_validation_summary(results)
        return results
    
    def fix_all_issues(self, post_ids: List[int] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Fix all issues found in posts."""
        print_header("Comprehensive Issue Fixing")
        
        if post_ids is None:
            # Get posts that need attention
            validation_result = self.validate_multiple_posts(per_page=20)
            post_ids = [
                result['post_id'] for result in validation_result.get('validation_results', [])
                if result['summary']['needs_attention']
            ]
        
        if not post_ids:
            print_success("No posts need fixing!")
            return {'message': 'No posts need fixing'}
        
        results = {
            'total_posts': len(post_ids),
            'posts_fixed': 0,
            'posts_failed': 0,
            'total_fixes': 0,
            'fix_results': []
        }
        
        for post_id in post_ids:
            print_section(f"Fixing Post {post_id}")
            
            post_fixes = {
                'post_id': post_id,
                'seo_fixes': [],
                'link_fixes': [],
                'image_fixes': []
            }
            
            try:
                # Fix SEO issues
                seo_result = self.seo_validator.optimize_post_seo(post_id, dry_run)
                if seo_result.get('optimizations'):
                    post_fixes['seo_fixes'] = seo_result['optimizations']
                
                # Fix broken links
                link_result = self.link_validator.fix_post_links(post_id, dry_run)
                if link_result.get('fixes_applied'):
                    post_fixes['link_fixes'] = link_result['fixes_applied']
                
                # Fix image issues
                image_result = self.image_validator.optimize_post_images(post_id, dry_run=dry_run)
                if image_result.get('fixes_applied'):
                    post_fixes['image_fixes'] = image_result['fixes_applied']
                
                # Count total fixes
                total_post_fixes = (
                    len(post_fixes['seo_fixes']) +
                    len(post_fixes['link_fixes']) +
                    len(post_fixes['image_fixes'])
                )
                
                if total_post_fixes > 0:
                    results['posts_fixed'] += 1
                    results['total_fixes'] += total_post_fixes
                    print_success(f"Applied {total_post_fixes} fixes to post {post_id}")
                else:
                    print_success(f"No fixes needed for post {post_id}")
                
                post_fixes['success'] = True
                post_fixes['fixes_count'] = total_post_fixes
                
            except Exception as e:
                print_error(f"Error fixing post {post_id}: {e}")
                results['posts_failed'] += 1
                post_fixes['success'] = False
                post_fixes['error'] = str(e)
            
            results['fix_results'].append(post_fixes)
        
        self._print_fixing_summary(results, dry_run)
        return results
    
    def generate_quality_report(self, post_ids: List[int] = None) -> str:
        """Generate a comprehensive quality report."""
        validation_results = self.validate_multiple_posts(post_ids)
        
        if 'error' in validation_results:
            return f"Error generating report: {validation_results['error']}"
        
        report = []
        report.append("WordPress Content Quality Report")
        report.append("=" * 50)
        report.append(f"Generated: {self._get_timestamp()}")
        report.append("")
        
        # Summary
        report.append("📊 SUMMARY")
        report.append("-" * 20)
        report.append(f"Total Posts: {validation_results['total_posts']}")
        report.append(f"Validated: {validation_results['validated_posts']}")
        report.append(f"Average Score: {validation_results['average_score']}%")
        report.append(f"Posts Needing Attention: {validation_results['posts_needing_attention']}")
        report.append("")
        
        # Top issues
        all_issues = []
        for result in validation_results.get('validation_results', []):
            if 'seo' in result and 'issues' in result['seo']:
                all_issues.extend(result['seo']['title']['issues'])
                all_issues.extend(result['seo']['content']['issues'])
            if 'links' in result:
                all_issues.extend([f"Broken link: {link}" for link in result['links'].get('broken_links', [])])
            if 'images' in result:
                broken_count = result['images'].get('broken_images', 0)
                if broken_count > 0:
                    all_issues.append(f"{broken_count} broken images")
        
        if all_issues:
            report.append("🔍 COMMON ISSUES")
            report.append("-" * 20)
            issue_counts = {}
            for issue in all_issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                report.append(f"• {issue} ({count} occurrences)")
            report.append("")
        
        # Detailed results
        report.append("📝 DETAILED RESULTS")
        report.append("-" * 20)
        
        for result in validation_results.get('validation_results', [])[:10]:  # Top 10
            post_id = result['post_id']
            title = result['post_title'][:50] + "..." if len(result['post_title']) > 50 else result['post_title']
            score = result['overall_score']
            
            report.append(f"Post {post_id}: {title}")
            report.append(f"  Overall Score: {score}%")
            report.append(f"  SEO: {result['summary']['seo_score']}%")
            report.append(f"  Links: {result['summary']['link_score']}%")
            report.append(f"  Images: {result['summary']['image_score']}%")
            report.append("")
        
        return "\n".join(report)
    
    def _count_total_issues(self, seo_result: Dict, link_result: Dict, image_result: Dict) -> int:
        """Count total issues across all validations."""
        total = 0
        
        if 'error' not in seo_result:
            total += seo_result.get('total_issues', 0)
        
        if 'error' not in link_result:
            total += len(link_result.get('broken_links', []))
        
        if 'error' not in image_result:
            total += image_result.get('broken_images', 0)
            total += image_result.get('images_without_alt', 0)
        
        return total
    
    def _print_validation_summary(self, results: Dict[str, Any]):
        """Print validation summary."""
        print_header("Validation Summary")
        print(f"📊 Posts validated: {results['validated_posts']}/{results['total_posts']}")
        print(f"📈 Average score: {results['average_score']}%")
        print(f"⚠️ Posts needing attention: {results['posts_needing_attention']}")
        
        if results['average_score'] >= 80:
            print("🎉 Great! Overall content quality is good.")
        elif results['average_score'] >= 60:
            print("👍 Content quality is acceptable, but there's room for improvement.")
        else:
            print("🔧 Content quality needs significant improvement.")
    
    def _print_fixing_summary(self, results: Dict[str, Any], dry_run: bool):
        """Print fixing summary."""
        mode = "DRY RUN" if dry_run else "LIVE"
        print_header(f"Fixing Summary ({mode})")
        print(f"📊 Posts processed: {results['total_posts']}")
        print(f"✅ Posts fixed: {results['posts_fixed']}")
        print(f"❌ Posts failed: {results['posts_failed']}")
        print(f"🔧 Total fixes applied: {results['total_fixes']}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")