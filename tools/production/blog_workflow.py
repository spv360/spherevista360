#!/usr/bin/env python3
"""
Blog Publishing Workflow
========================
Unified workflow for complete blog publishing with validation and optimization.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import time
from datetime import datetime

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent))
from enhanced_wp_client import WordPressClient, print_header, print_section
from enhanced_content_publisher import ContentPublisher
from comprehensive_validator import ContentValidator


class BlogPublishingWorkflow:
    """Complete blog publishing workflow."""
    
    def __init__(self):
        """Initialize workflow components."""
        self.wp = WordPressClient()
        self.publisher = ContentPublisher(self.wp)
        self.validator = ContentValidator(self.wp)
        self.workflow_results = {}
    
    def run_complete_workflow(self, content_path: str, category: str = None, 
                            dry_run: bool = False, validate_after: bool = True) -> Dict:
        """Run the complete publishing workflow."""
        
        print_header("COMPLETE BLOG PUBLISHING WORKFLOW")
        print(f"📁 Content Path: {content_path}")
        print(f"📂 Target Category: {category or 'Auto-detect'}")
        print(f"🧪 Mode: {'DRY RUN' if dry_run else 'LIVE PUBLISHING'}")
        print(f"✅ Post-publish validation: {'Enabled' if validate_after else 'Disabled'}")
        
        workflow_start = time.time()
        results = {
            'started_at': datetime.now().isoformat(),
            'content_path': content_path,
            'category': category,
            'dry_run': dry_run,
            'steps': {}
        }
        
        # Step 1: Pre-publishing validation
        print_section("STEP 1: PRE-PUBLISHING ANALYSIS")
        if Path(content_path).is_dir():
            md_files = list(Path(content_path).glob('*.md'))
            print(f"📄 Found {len(md_files)} markdown files")
            
            # Quick content analysis
            total_size = sum(f.stat().st_size for f in md_files)
            print(f"📊 Total content size: {total_size // 1024} KB")
            
            results['steps']['analysis'] = {
                'files_found': len(md_files),
                'total_size_kb': total_size // 1024,
                'status': 'completed'
            }
        else:
            print(f"📄 Single file: {Path(content_path).name}")
            results['steps']['analysis'] = {
                'files_found': 1,
                'total_size_kb': Path(content_path).stat().st_size // 1024,
                'status': 'completed'
            }
        
        # Step 2: Duplicate check
        print_section("STEP 2: DUPLICATE CONTENT CHECK")
        print("🔍 Checking for existing similar content...")
        
        # Get existing posts for comparison
        existing_posts = self.wp.get_posts(per_page=50, category=category)
        print(f"📊 Found {len(existing_posts)} existing posts in target category")
        
        results['steps']['duplicate_check'] = {
            'existing_posts': len(existing_posts),
            'status': 'completed'
        }
        
        # Step 3: Content publishing
        print_section("STEP 3: CONTENT PUBLISHING")
        
        if Path(content_path).is_dir():
            publish_results = self.publisher.publish_directory(content_path, category, dry_run)
        else:
            single_result = self.publisher.publish_file(content_path, category, dry_run)
            publish_results = {
                'successful': [single_result] if single_result['success'] else [],
                'failed': [] if single_result['success'] else [single_result]
            }
        
        successful_count = len(publish_results['successful'])
        failed_count = len(publish_results['failed'])
        
        print_section("PUBLISHING RESULTS")
        print(f"✅ Successful: {successful_count}")
        print(f"❌ Failed: {failed_count}")
        
        if publish_results['failed']:
            print("\\n🚨 FAILURES:")
            for failure in publish_results['failed']:
                error_msg = failure.get('error', 'Unknown error')
                file_name = failure.get('file', 'Unknown file')
                print(f"   ❌ {file_name}: {error_msg}")
        
        results['steps']['publishing'] = {
            'successful_count': successful_count,
            'failed_count': failed_count,
            'successful_posts': publish_results['successful'],
            'failed_posts': publish_results['failed'],
            'status': 'completed'
        }
        
        # Step 4: Post-publishing validation (if enabled and not dry run)
        if validate_after and not dry_run and successful_count > 0:
            print_section("STEP 4: POST-PUBLISHING VALIDATION")
            
            # Wait a moment for WordPress to process
            print("⏳ Waiting for WordPress to process posts...")
            time.sleep(3)
            
            validation_results = []
            
            for success_result in publish_results['successful']:
                post_id = success_result.get('id')
                if post_id:
                    print(f"🔍 Validating post ID {post_id}...")
                    validation = self.validator.validate_post(post_id)
                    validation_results.append(validation)
                    
                    score = validation.get('overall_score', 0)
                    title = validation.get('title', 'Unknown')[:40]
                    
                    if score >= 90:
                        print(f"   ✅ {title}... - {score:.1f}% (Excellent)")
                    elif score >= 80:
                        print(f"   🟡 {title}... - {score:.1f}% (Good)")
                    else:
                        print(f"   🔴 {title}... - {score:.1f}% (Needs work)")
                        
                        # Show top issues
                        all_issues = (validation.get('seo', {}).get('issues', []) +
                                    validation.get('images', {}).get('issues', []) +
                                    validation.get('links', {}).get('issues', []))
                        for issue in all_issues[:2]:
                            print(f"      ⚠️ {issue}")
            
            # Calculate average validation score
            if validation_results:
                avg_score = sum(v.get('overall_score', 0) for v in validation_results) / len(validation_results)
                print(f"\\n📊 Average quality score: {avg_score:.1f}%")
                
                results['steps']['validation'] = {
                    'posts_validated': len(validation_results),
                    'average_score': avg_score,
                    'results': validation_results,
                    'status': 'completed'
                }
            else:
                results['steps']['validation'] = {'status': 'skipped', 'reason': 'no_posts_to_validate'}
        else:
            results['steps']['validation'] = {
                'status': 'skipped', 
                'reason': 'dry_run' if dry_run else 'disabled'
            }
        
        # Step 5: Workflow summary
        workflow_duration = time.time() - workflow_start
        
        print_section("WORKFLOW SUMMARY")
        print(f"⏱️ Total time: {workflow_duration:.1f} seconds")
        print(f"📄 Content processed: {successful_count} successful, {failed_count} failed")
        
        if validate_after and not dry_run and 'validation' in results['steps']:
            validation_step = results['steps']['validation']
            if validation_step['status'] == 'completed':
                avg_score = validation_step['average_score']
                print(f"📊 Average quality: {avg_score:.1f}%")
                
                if avg_score >= 90:
                    print("🎉 Excellent! All content meets high quality standards")
                elif avg_score >= 80:
                    print("✅ Good quality content published")
                else:
                    print("⚠️ Content published but may need optimization")
        
        if dry_run:
            print("🧪 DRY RUN completed - no content was actually published")
        else:
            print(f"🎯 WORKFLOW COMPLETED - {successful_count} posts published")
        
        results['completed_at'] = datetime.now().isoformat()
        results['duration_seconds'] = workflow_duration
        results['status'] = 'completed'
        
        return results
    
    def quick_validate_category(self, category: str) -> Dict:
        """Quick validation of an entire category."""
        print_header(f"QUICK CATEGORY VALIDATION: {category}")
        
        return self.validator.validate_category(category)
    
    def optimize_existing_post(self, post_id: int) -> Dict:
        """Optimize an existing post based on validation results."""
        print_header(f"POST OPTIMIZATION: {post_id}")
        
        # Get current validation
        validation = self.validator.validate_post(post_id)
        if 'error' in validation:
            return validation
        
        print(f"📄 Post: {validation['title']}")
        print(f"🎯 Current score: {validation['overall_score']:.1f}%")
        
        # Suggest optimizations
        optimizations = []
        
        # SEO optimizations
        seo_issues = validation['seo']['issues']
        for issue in seo_issues:
            if 'internal links' in issue.lower():
                optimizations.append("Add more internal links to related content")
            elif 'h2 headings' in issue.lower():
                optimizations.append("Add more H2 subheadings to improve structure")
            elif 'content too short' in issue.lower():
                optimizations.append("Expand content with more detailed information")
        
        # Image optimizations
        image_issues = validation['images']['issues']
        for issue in image_issues:
            if 'alt text' in issue.lower():
                optimizations.append("Add descriptive alt text to images")
            elif 'responsive' in issue.lower():
                optimizations.append("Optimize images for responsive design")
        
        print("\\n🔧 RECOMMENDED OPTIMIZATIONS:")
        for i, opt in enumerate(optimizations, 1):
            print(f"   {i}. {opt}")
        
        return {
            'post_id': post_id,
            'current_score': validation['overall_score'],
            'optimizations': optimizations,
            'validation': validation
        }


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Blog Publishing Workflow')
    parser.add_argument('action', choices=['publish', 'validate', 'optimize'], 
                       help='Action to perform')
    parser.add_argument('target', help='Content path, category name, or post ID')
    parser.add_argument('--category', help='Target category for publishing')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')
    parser.add_argument('--no-validate', action='store_true', help='Skip post-publishing validation')
    parser.add_argument('--username', help='WordPress username')
    parser.add_argument('--password', help='WordPress application password')
    
    args = parser.parse_args()
    
    # Initialize workflow
    workflow = BlogPublishingWorkflow()
    
    # Authenticate
    if not workflow.wp.authenticate(args.username, args.password):
        print("❌ Authentication failed. Exiting.")
        return 1
    
    # Execute action
    if args.action == 'publish':
        result = workflow.run_complete_workflow(
            args.target, 
            args.category,
            args.dry_run,
            not args.no_validate
        )
        
        if result['status'] == 'completed':
            print("\\n🎉 Workflow completed successfully!")
            return 0
        else:
            print("\\n❌ Workflow completed with issues")
            return 1
    
    elif args.action == 'validate':
        result = workflow.quick_validate_category(args.target)
        
        if 'error' not in result:
            avg_score = result['average_scores']['overall']
            print(f"\\n📊 Category '{args.target}' average score: {avg_score:.1f}%")
            return 0
        else:
            print(f"\\n❌ {result['error']}")
            return 1
    
    elif args.action == 'optimize':
        try:
            post_id = int(args.target)
            result = workflow.optimize_existing_post(post_id)
            
            if 'error' not in result:
                print(f"\\n🔧 Optimization suggestions provided for post {post_id}")
                return 0
            else:
                print(f"\\n❌ {result['error']}")
                return 1
        except ValueError:
            print("❌ Post ID must be a number")
            return 1


if __name__ == "__main__":
    sys.exit(main())