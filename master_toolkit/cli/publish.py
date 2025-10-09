#!/usr/bin/env python3
"""
WordPress Publishing CLI
========================
Command-line interface for WordPress content publishing.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from wordpress_toolkit.core import create_client, WordPressAPIError
from wordpress_toolkit.content import ContentPublisher, ContentWorkflow
from wordpress_toolkit.utils import print_header, print_error, print_success


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='WordPress Content Publishing Tool')
    parser.add_argument('--username', '-u', help='WordPress username')
    parser.add_argument('--password', '-p', help='WordPress application password')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Publish file command
    publish_parser = subparsers.add_parser('publish', help='Publish a single markdown file')
    publish_parser.add_argument('file', help='Path to markdown file')
    publish_parser.add_argument('--category', '-c', help='Post category')
    publish_parser.add_argument('--status', '-s', default='publish', help='Post status')
    publish_parser.add_argument('--validate', action='store_true', help='Validate after publishing')
    
    # Batch publish command
    batch_parser = subparsers.add_parser('batch', help='Publish all markdown files in directory')
    batch_parser.add_argument('directory', help='Directory containing markdown files')
    batch_parser.add_argument('--category', '-c', help='Post category')
    batch_parser.add_argument('--status', '-s', default='publish', help='Post status')
    batch_parser.add_argument('--validate', action='store_true', help='Validate after publishing')
    
    # Workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Complete publishing workflow')
    workflow_parser.add_argument('file', help='Path to markdown file')
    workflow_parser.add_argument('--category', '-c', help='Post category')
    workflow_parser.add_argument('--status', '-s', default='publish', help='Post status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Create and authenticate client
        client = create_client()
        
        # Try authentication
        if not client.authenticate(args.username, args.password):
            print_error("Authentication failed. Please check credentials.")
            return 1
        
        # Execute command
        if args.command == 'publish':
            return publish_file(client, args)
        elif args.command == 'batch':
            return batch_publish(client, args)
        elif args.command == 'workflow':
            return workflow_publish(client, args)
        
    except WordPressAPIError as e:
        print_error(f"WordPress API error: {e}")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


def publish_file(client, args):
    """Publish a single file."""
    publisher = ContentPublisher(client)
    
    result = publisher.publish_from_file(
        args.file,
        category=args.category,
        status=args.status,
        dry_run=args.dry_run
    )
    
    if result['success']:
        if args.dry_run:
            print_success("Dry run completed successfully!")
        else:
            print_success(f"Published: {result.get('post_url', 'Post created')}")
        
        # Optional validation
        if args.validate and not args.dry_run and result.get('post_id'):
            from wordpress_toolkit.validation import ComprehensiveValidator
            validator = ComprehensiveValidator(client)
            validation = validator.validate_post_comprehensive(result['post_id'])
            
            if 'error' not in validation:
                score = validation['overall_score']
                print(f"📊 Quality Score: {score}%")
        
        return 0
    else:
        print_error(f"Publishing failed: {result.get('error', 'Unknown error')}")
        return 1


def batch_publish(client, args):
    """Batch publish files."""
    publisher = ContentPublisher(client)
    
    result = publisher.publish_from_directory(
        args.directory,
        category=args.category,
        status=args.status,
        dry_run=args.dry_run
    )
    
    if result.get('published', 0) > 0 or args.dry_run:
        print_success(f"Batch publish completed: {result['published']} published, {result['failed']} failed")
        return 0
    else:
        print_error("Batch publishing failed")
        return 1


def workflow_publish(client, args):
    """Complete workflow publishing."""
    workflow = ContentWorkflow(client)
    
    result = workflow.publish_with_validation(
        args.file,
        category=args.category,
        status=args.status,
        validate_after=True,
        dry_run=args.dry_run
    )
    
    if result['success']:
        print_success("Workflow completed successfully!")
        
        # Show quality score if available
        if 'validation' in result['steps']:
            score = result['steps']['validation'].get('overall_score', 0)
            print(f"📊 Final Quality Score: {score}%")
        
        return 0
    else:
        print_error(f"Workflow failed: {result.get('error', 'Unknown error')}")
        return 1


if __name__ == '__main__':
    sys.exit(main())