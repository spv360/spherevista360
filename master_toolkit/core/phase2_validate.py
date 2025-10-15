#!/usr/bin/env python3
"""
Phase 2 Validation CLI Extension
================================
Enhanced validation commands for performance, accessibility, security, and mobile responsiveness.
Usage: python phase2_validate.py <command> [options]
"""

import argparse
import sys
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from master_toolkit.core import WordPressClient, WordPressAPIError
from master_toolkit.validation import (
    PerformanceValidator,
    AccessibilityValidator, 
    SecurityValidator,
    MobileValidator
)
from master_toolkit.utils import print_header, print_error, print_success, print_warning


def print_validation_result(result):
    """Print formatted validation result."""
    if not result:
        print_error("No result to display")
        return
    
    status = result.get('status', 'unknown')
    score = result.get('score', 0)
    post_title = result.get('post_title', result.get('site_url', 'Unknown'))
    
    # Status indicators
    status_icons = {
        'excellent': '🟢',
        'good': '🟡', 
        'fair': '🟠',
        'poor': '🔴',
        'unknown': '⚪'
    }
    
    icon = status_icons.get(status, '⚪')
    print(f"\n{icon} {post_title} (Score: {score}/100)")
    print(f"   Status: {status.title()}")
    
    if result.get('message'):
        print(f"   {result['message']}")
    
    # Show issues
    issues = result.get('issues', [])
    if issues:
        print(f"   ⚠️  Issues Found:")
        for issue in issues[:3]:  # Show first 3 issues
            print(f"      • {issue}")
        if len(issues) > 3:
            print(f"      ... and {len(issues) - 3} more")
    
    # Show recommendations
    recommendations = result.get('recommendations', [])
    if recommendations:
        print(f"   💡 Recommendations:")
        for rec in recommendations[:2]:  # Show first 2 recommendations
            print(f"      • {rec}")
        if len(recommendations) > 2:
            print(f"      ... and {len(recommendations) - 2} more")


def run_performance_validation(args):
    """Run performance validation."""
    print_header("🚀 Performance Validation")
    
    try:
        validator = PerformanceValidator()
        
        if args.post_id:
            print(f"Running performance validation for post {args.post_id}...")
            
            # Page speed validation
            if args.page_speed or args.all:
                print(f"\n⚡ Analyzing page speed for post {args.post_id}...")
                speed_result = validator.validate_page_speed(args.post_id)
                if speed_result.get('success', True):
                    print_validation_result(speed_result)
                else:
                    print_error(f"Page speed error: {speed_result.get('error', 'Unknown error')}")
            
            # Image optimization validation
            if args.images or args.all:
                print(f"\n🖼️  Analyzing image optimization for post {args.post_id}...")
                image_result = validator.validate_image_optimization(args.post_id)
                if image_result.get('success', True):
                    print_validation_result(image_result)
                else:
                    print_error(f"Image optimization error: {image_result.get('error', 'Unknown error')}")
        
        else:
            print_warning("Performance validation requires --post-id")
            print("Available flags: --page-speed, --images, --all")
            
    except Exception as e:
        print_error(f"Performance validation failed: {str(e)}")


def run_accessibility_validation(args):
    """Run accessibility validation."""
    print_header("♿ Accessibility Validation")
    
    try:
        validator = AccessibilityValidator()
        
        if args.post_id:
            print(f"Running accessibility validation for post {args.post_id}...")
            wcag_level = args.wcag_level or 'AA'
            
            result = validator.validate_accessibility(args.post_id, wcag_level)
            if result.get('success', True):
                print_validation_result(result)
                
                # Show detailed accessibility breakdown
                if args.detailed:
                    accessibility = result.get('accessibility', {})
                    print(f"\n📊 Detailed Accessibility Analysis (WCAG {wcag_level}):")
                    for section, data in accessibility.items():
                        score = data.get('score', 0)
                        icon = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
                        print(f"   {icon} {section.replace('_', ' ').title()}: {score}/100")
            else:
                print_error(f"Accessibility validation error: {result.get('error', 'Unknown error')}")
        
        else:
            print_warning("Accessibility validation requires --post-id")
            
    except Exception as e:
        print_error(f"Accessibility validation failed: {str(e)}")


def run_security_validation(args):
    """Run security validation."""
    print_header("🔒 Security Validation")
    
    try:
        validator = SecurityValidator()
        
        print("Running comprehensive site security validation...")
        result = validator.validate_site_security()
        
        if result.get('success', True):
            print_validation_result(result)
            
            # Show detailed security breakdown
            if args.detailed:
                security = result.get('security', {})
                print(f"\n🛡️  Detailed Security Analysis:")
                for section, data in security.items():
                    score = data.get('score', 0)
                    icon = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
                    print(f"   {icon} {section.replace('_', ' ').title()}: {score}/100")
        else:
            print_error(f"Security validation error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print_error(f"Security validation failed: {str(e)}")


def run_mobile_validation(args):
    """Run mobile responsiveness validation."""
    print_header("📱 Mobile Responsiveness Validation")
    
    try:
        validator = MobileValidator()
        
        if args.post_id:
            print(f"Running mobile validation for post {args.post_id}...")
            
            result = validator.validate_mobile_responsiveness(args.post_id)
            if result.get('success', True):
                print_validation_result(result)
                
                # Show detailed mobile breakdown
                if args.detailed:
                    mobile = result.get('mobile', {})
                    print(f"\n📲 Detailed Mobile Analysis:")
                    for section, data in mobile.items():
                        score = data.get('score', 0)
                        icon = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
                        print(f"   {icon} {section.replace('_', ' ').title()}: {score}/100")
            else:
                print_error(f"Mobile validation error: {result.get('error', 'Unknown error')}")
        
        else:
            print_warning("Mobile validation requires --post-id")
            
    except Exception as e:
        print_error(f"Mobile validation failed: {str(e)}")


def run_comprehensive_phase2_validation(args):
    """Run all Phase 2 validations."""
    print_header("🔍 Comprehensive Phase 2 Validation")
    
    try:
        if not args.post_id:
            print_warning("Comprehensive Phase 2 validation requires --post-id")
            return
        
        print(f"Running comprehensive validation for post {args.post_id}...")
        
        # Performance validation
        print("\n🚀 Performance Analysis...")
        perf_validator = PerformanceValidator()
        perf_result = perf_validator.validate_page_speed(args.post_id)
        if perf_result.get('success', True):
            print(f"   Performance Score: {perf_result.get('score', 0)}/100")
        
        # Accessibility validation  
        print("\n♿ Accessibility Analysis...")
        acc_validator = AccessibilityValidator()
        acc_result = acc_validator.validate_accessibility(args.post_id)
        if acc_result.get('success', True):
            print(f"   Accessibility Score: {acc_result.get('score', 0)}/100")
        
        # Mobile validation
        print("\n📱 Mobile Analysis...")
        mobile_validator = MobileValidator()
        mobile_result = mobile_validator.validate_mobile_responsiveness(args.post_id)
        if mobile_result.get('success', True):
            print(f"   Mobile Score: {mobile_result.get('score', 0)}/100")
        
        # Security validation (site-wide)
        print("\n🔒 Security Analysis...")
        sec_validator = SecurityValidator()
        sec_result = sec_validator.validate_site_security()
        if sec_result.get('success', True):
            print(f"   Security Score: {sec_result.get('score', 0)}/100")
        
        # Calculate overall Phase 2 score
        scores = []
        for result in [perf_result, acc_result, mobile_result, sec_result]:
            if result.get('success', True):
                scores.append(result.get('score', 0))
        
        if scores:
            overall_score = int(sum(scores) / len(scores))
            print(f"\n📊 Overall Phase 2 Score: {overall_score}/100")
            
            if overall_score >= 85:
                print_success("🎉 Excellent overall validation results!")
            elif overall_score >= 70:
                print_success("✅ Good overall validation results")
            else:
                print_warning("⚠️  Areas for improvement identified")
        
    except Exception as e:
        print_error(f"Comprehensive validation failed: {str(e)}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Phase 2 Enhanced WordPress Validation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s performance --post-id 123 --page-speed --images
  %(prog)s accessibility --post-id 123 --wcag-level AAA
  %(prog)s security
  %(prog)s mobile --post-id 123
  %(prog)s comprehensive --post-id 123
        """
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Validation types')
    
    # Performance validation
    perf_parser = subparsers.add_parser('performance', help='Run performance validation')
    perf_parser.add_argument('--post-id', type=int, help='Validate specific post ID')
    perf_parser.add_argument('--page-speed', action='store_true', help='Analyze page speed and Core Web Vitals')
    perf_parser.add_argument('--images', action='store_true', help='Analyze image optimization')
    perf_parser.add_argument('--all', action='store_true', help='Run all performance validations')
    
    # Accessibility validation
    acc_parser = subparsers.add_parser('accessibility', help='Run accessibility validation')
    acc_parser.add_argument('--post-id', type=int, required=True, help='Validate specific post ID')
    acc_parser.add_argument('--wcag-level', choices=['A', 'AA', 'AAA'], default='AA', help='WCAG compliance level')
    acc_parser.add_argument('--detailed', action='store_true', help='Show detailed breakdown')
    
    # Security validation
    sec_parser = subparsers.add_parser('security', help='Run security validation')
    sec_parser.add_argument('--detailed', action='store_true', help='Show detailed breakdown')
    
    # Mobile validation
    mobile_parser = subparsers.add_parser('mobile', help='Run mobile responsiveness validation')
    mobile_parser.add_argument('--post-id', type=int, required=True, help='Validate specific post ID')
    mobile_parser.add_argument('--detailed', action='store_true', help='Show detailed breakdown')
    
    # Comprehensive validation
    comp_parser = subparsers.add_parser('comprehensive', help='Run all Phase 2 validations')
    comp_parser.add_argument('--post-id', type=int, required=True, help='Validate specific post ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to appropriate validation function
    if args.command == 'performance':
        run_performance_validation(args)
    elif args.command == 'accessibility':
        run_accessibility_validation(args)
    elif args.command == 'security':
        run_security_validation(args)
    elif args.command == 'mobile':
        run_mobile_validation(args)
    elif args.command == 'comprehensive':
        run_comprehensive_phase2_validation(args)
    else:
        print_error(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()