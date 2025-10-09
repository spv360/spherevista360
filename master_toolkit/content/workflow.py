"""
Content Workflow
===============
Complete content publishing and management workflows.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_header, print_section, print_success, print_error, ResultFormatter
from ..validation import ComprehensiveValidator
from .publisher import ContentPublisher


class ContentWorkflow:
    """Complete content management workflow."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize workflow."""
        self.wp = wp_client or WordPressClient()
        self.publisher = ContentPublisher(self.wp)
        self.validator = ComprehensiveValidator(self.wp)
    
    def publish_with_validation(self, file_path: str, category: str = None,
                              status: str = 'publish', validate_after: bool = True,
                              dry_run: bool = False) -> Dict[str, Any]:
        """Publish content with automatic validation."""
        print_header(f"Publishing Workflow: {Path(file_path).name}")
        
        result = {
            'file_path': file_path,
            'category': category,
            'dry_run': dry_run,
            'steps': {}
        }
        
        try:
            # Step 1: Publish content
            print_section("Step 1: Publishing Content")
            publish_result = self.publisher.publish_from_file(
                file_path, category, status, dry_run
            )
            result['steps']['publish'] = publish_result
            
            if not publish_result['success']:
                return result
            
            print_success("Content published successfully!")
            
            # Step 2: Validate (if not dry run and validation enabled)
            if not dry_run and validate_after and publish_result.get('post_id'):
                print_section("Step 2: Post-Publish Validation")
                
                post_id = publish_result['post_id']
                validation_result = self.validator.validate_post_comprehensive(post_id)
                result['steps']['validation'] = validation_result
                
                if 'error' not in validation_result:
                    score = validation_result['overall_score']
                    print(f"📊 Content Quality Score: {score}%")
                    
                    if score >= 80:
                        print_success("Excellent content quality!")
                    elif score >= 60:
                        print("👍 Good content quality with minor improvements possible")
                    else:
                        print("⚠️ Content quality could be improved")
                
                # Step 3: Auto-fix issues if score is low
                if validation_result.get('overall_score', 0) < 70:
                    print_section("Step 3: Auto-Fixing Issues")
                    
                    fix_result = self.validator.fix_all_issues([post_id])
                    result['steps']['fixes'] = fix_result
                    
                    if fix_result.get('total_fixes', 0) > 0:
                        print_success(f"Applied {fix_result['total_fixes']} automatic fixes")
                        
                        # Re-validate after fixes
                        final_validation = self.validator.validate_post_comprehensive(post_id)
                        result['steps']['final_validation'] = final_validation
                        
                        if 'error' not in final_validation:
                            final_score = final_validation['overall_score']
                            print(f"📈 Updated Quality Score: {final_score}%")
            
            result['success'] = True
            return result
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            print_error(f"Workflow failed: {e}")
            return result
    
    def batch_publish_with_validation(self, directory: str, category: str = None,
                                    status: str = 'publish', validate_after: bool = True,
                                    dry_run: bool = False) -> Dict[str, Any]:
        """Batch publish with validation workflow."""
        print_header(f"Batch Publishing Workflow: {directory}")
        
        directory_path = Path(directory)
        if not directory_path.exists():
            return {'success': False, 'error': f'Directory not found: {directory}'}
        
        markdown_files = list(directory_path.glob("*.md"))
        if not markdown_files:
            return {'success': False, 'error': 'No markdown files found'}
        
        results = {
            'total_files': len(markdown_files),
            'successful': 0,
            'failed': 0,
            'average_quality_score': 0,
            'workflow_results': []
        }
        
        total_score = 0
        scored_posts = 0
        
        for file_path in markdown_files:
            print_section(f"Processing {file_path.name}")
            
            workflow_result = self.publish_with_validation(
                str(file_path), category, status, validate_after, dry_run
            )
            
            if workflow_result['success']:
                results['successful'] += 1
                
                # Track quality scores
                if 'validation' in workflow_result['steps']:
                    score = workflow_result['steps']['validation'].get('overall_score', 0)
                    total_score += score
                    scored_posts += 1
            else:
                results['failed'] += 1
            
            results['workflow_results'].append(workflow_result)
        
        if scored_posts > 0:
            results['average_quality_score'] = round(total_score / scored_posts, 1)
        
        # Print summary
        self._print_batch_summary(results, dry_run)
        
        return results
    
    def quality_audit_workflow(self, post_ids: List[int] = None) -> Dict[str, Any]:
        """Complete quality audit and fixing workflow."""
        print_header("Quality Audit Workflow")
        
        # Step 1: Comprehensive validation
        print_section("Step 1: Quality Assessment")
        validation_results = self.validator.validate_multiple_posts(post_ids)
        
        if 'error' in validation_results:
            return {'success': False, 'error': validation_results['error']}
        
        # Step 2: Identify issues
        posts_needing_attention = [
            result for result in validation_results.get('validation_results', [])
            if result['summary']['needs_attention']
        ]
        
        print_section("Step 2: Issue Analysis")
        print(f"📊 Posts analyzed: {validation_results['validated_posts']}")
        print(f"📈 Average quality: {validation_results['average_score']}%")
        print(f"⚠️ Posts needing attention: {len(posts_needing_attention)}")
        
        if not posts_needing_attention:
            print_success("🎉 All posts meet quality standards!")
            return {
                'success': True,
                'validation_results': validation_results,
                'posts_fixed': 0,
                'message': 'No fixes needed'
            }
        
        # Step 3: Fix issues
        print_section("Step 3: Automatic Fixes")
        post_ids_to_fix = [post['post_id'] for post in posts_needing_attention]
        fix_results = self.validator.fix_all_issues(post_ids_to_fix)
        
        # Step 4: Re-validate
        print_section("Step 4: Post-Fix Validation")
        final_validation = self.validator.validate_multiple_posts(post_ids_to_fix)
        
        return {
            'success': True,
            'initial_validation': validation_results,
            'fix_results': fix_results,
            'final_validation': final_validation,
            'improvement': {
                'initial_score': validation_results['average_score'],
                'final_score': final_validation.get('average_score', 0),
                'posts_fixed': fix_results.get('posts_fixed', 0),
                'total_fixes': fix_results.get('total_fixes', 0)
            }
        }
    
    def _print_batch_summary(self, results: Dict[str, Any], dry_run: bool):
        """Print batch workflow summary."""
        mode = " (DRY RUN)" if dry_run else ""
        print_header(f"Batch Workflow Summary{mode}")
        
        print(f"📁 Total files: {results['total_files']}")
        print(f"✅ Successful: {results['successful']}")
        print(f"❌ Failed: {results['failed']}")
        
        if results['average_quality_score'] > 0:
            print(f"📊 Average quality score: {results['average_quality_score']}%")
        
        success_rate = (results['successful'] / results['total_files']) * 100
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 Excellent batch processing results!")
        elif success_rate >= 70:
            print("👍 Good batch processing results!")
        else:
            print("⚠️ Batch processing needs improvement.")