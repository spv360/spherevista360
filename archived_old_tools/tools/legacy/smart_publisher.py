#!/usr/bin/env python3
"""
Smart WordPress Publisher - Prevents Duplicates
Checks for existing posts before publishing to avoid duplicates
"""

import os
import sys
import requests
import base64
import json
import subprocess
from typing import Dict, List, Optional
from datetime import datetime

class SmartWordPressPublisher:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', '').rstrip('/')
        self.wp_user = os.environ.get('WP_USER', '')
        self.wp_pass = os.environ.get('WP_APP_PASS', '')
        
        if not all([self.wp_site, self.wp_user, self.wp_pass]):
            raise ValueError("WordPress credentials not set")
        
        # Set up authentication
        credentials = f"{self.wp_user}:{self.wp_pass}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        self.base_url = f"{self.wp_site}/wp-json/wp/v2"
        
        # Available categories and their directories
        self.categories = {
            'Finance': './spherevista360_week1_final/Finance',
            'Technology': './spherevista360_week1_final/Tech', 
            'Politics': './spherevista360_week1_final/Politics',
            'Travel': './spherevista360_week1_final/Travel',
            'World': './spherevista360_week1_final/World',
            'Business': './spherevista360_week1_final/Business'
        }
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected as {user_data.get('name')} with roles: {user_data.get('roles')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_existing_posts(self) -> List[Dict]:
        """Get all existing posts from WordPress"""
        all_posts = []
        page = 1
        per_page = 50
        
        while True:
            try:
                response = requests.get(
                    f"{self.base_url}/posts",
                    headers=self.headers,
                    params={
                        'per_page': per_page, 
                        'page': page,
                        'status': 'publish,draft'
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    posts = response.json()
                    if not posts:  # No more posts
                        break
                    all_posts.extend(posts)
                    page += 1
                else:
                    print(f"❌ Failed to fetch posts page {page}: {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"❌ Error fetching posts: {e}")
                break
        
        return all_posts
    
    def get_content_files(self, category_path: str) -> List[str]:
        """Get list of markdown files in category directory"""
        if not os.path.exists(category_path):
            return []
        
        files = []
        for file in os.listdir(category_path):
            if file.endswith('.md'):
                files.append(file)
        
        return sorted(files)
    
    def extract_title_from_file(self, file_path: str) -> str:
        """Extract title from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Look for YAML front matter title
                if content.startswith('---'):
                    lines = content.split('\n')
                    for line in lines[1:]:
                        if line.startswith('title:'):
                            return line.replace('title:', '').strip().strip('"\'')
                        if line.strip() == '---':
                            break
                
                # Look for first # heading
                for line in content.split('\n'):
                    if line.startswith('# '):
                        return line[2:].strip()
                
                # Use filename as fallback
                return os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
                
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            return os.path.basename(file_path).replace('.md', '')
    
    def check_post_exists(self, title: str, existing_posts: List[Dict]) -> Optional[Dict]:
        """Check if a post with similar title already exists"""
        title_lower = title.lower()
        
        for post in existing_posts:
            post_title = post['title']['rendered'].lower()
            
            # Exact match
            if title_lower == post_title:
                return post
            
            # Similar match (80% of words match)
            title_words = set(title_lower.split())
            post_words = set(post_title.split())
            
            if len(title_words) > 0:
                similarity = len(title_words.intersection(post_words)) / len(title_words)
                if similarity >= 0.8:
                    return post
        
        return None
    
    def publish_category(self, category: str, force: bool = False, as_draft: bool = False) -> Dict:
        """Publish content for a specific category with duplicate checking"""
        
        if category not in self.categories:
            return {'error': f"Category '{category}' not found. Available: {list(self.categories.keys())}"}
        
        category_path = self.categories[category]
        
        if not os.path.exists(category_path):
            return {'error': f"Directory not found: {category_path}"}
        
        print(f"\n🎯 Publishing {category} Category")
        print("=" * 40)
        print(f"📁 Source: {category_path}")
        print(f"🎨 Mode: {'DRAFT' if as_draft else 'PUBLISH'}")
        print(f"🔄 Force: {'Yes (ignore duplicates)' if force else 'No (check duplicates)'}")
        
        # Get existing posts
        if not force:
            print("🔍 Checking for existing posts...")
            existing_posts = self.get_existing_posts()
            print(f"📊 Found {len(existing_posts)} existing posts")
        else:
            existing_posts = []
        
        # Get content files
        content_files = self.get_content_files(category_path)
        if not content_files:
            return {'error': f"No markdown files found in {category_path}"}
        
        print(f"📝 Found {len(content_files)} content files")
        
        # Check each file
        to_publish = []
        skipped = []
        
        for file in content_files:
            file_path = os.path.join(category_path, file)
            title = self.extract_title_from_file(file_path)
            
            if not force:
                existing = self.check_post_exists(title, existing_posts)
                if existing:
                    skipped.append({
                        'file': file,
                        'title': title,
                        'existing_title': existing['title']['rendered'],
                        'existing_id': existing['id'],
                        'existing_link': existing['link']
                    })
                    continue
            
            to_publish.append({
                'file': file,
                'title': title,
                'file_path': file_path
            })
        
        # Show summary
        print(f"\n📊 Publishing Summary:")
        print(f"  ✅ To publish: {len(to_publish)} files")
        print(f"  ⏭️ Skipped (duplicates): {len(skipped)} files")
        
        if skipped:
            print(f"\n⏭️ Skipped Files (already exist):")
            for item in skipped:
                print(f"   • {item['file']} → '{item['existing_title']}' (ID: {item['existing_id']})")
        
        if to_publish:
            print(f"\n✅ Files to publish:")
            for item in to_publish:
                print(f"   • {item['file']} → '{item['title']}'")
        
        if not to_publish:
            print("\n🎉 No new content to publish! All files already exist.")
            return {
                'success': True,
                'published': 0,
                'skipped': len(skipped),
                'skipped_files': skipped,
                'category': category
            }
        
        # Confirm publication
        if not force:
            print(f"\n⚠️ Ready to publish {len(to_publish)} new posts to {category} category")
            confirm = input("Continue? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Publication cancelled")
                return {'cancelled': True, 'category': category}
        
        # Build wp_agent_bulk command
        draft_flag = "--draft" if as_draft else ""
        command = f"python scripts/wp_agent_bulk.py {category_path} --category {category} {draft_flag}".strip()
        
        print(f"\n🚀 Running: {command}")
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                print("✅ Publication successful!")
                print(result.stdout)
                
                return {
                    'success': True,
                    'published': len(to_publish),
                    'skipped': len(skipped),
                    'command': command,
                    'output': result.stdout,
                    'category': category
                }
            else:
                print("❌ Publication failed!")
                print(result.stderr)
                return {
                    'error': result.stderr,
                    'command': command,
                    'category': category
                }
                
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return {'error': str(e), 'category': category}
    
    def publish_all_categories(self, force: bool = False, as_draft: bool = False, interactive: bool = True) -> Dict:
        """Publish content for all categories with duplicate checking"""
        
        print(f"\n🌐 Publishing ALL Categories")
        print("=" * 50)
        print(f"🎨 Mode: {'DRAFT' if as_draft else 'PUBLISH'}")
        print(f"🔄 Force: {'Yes (ignore duplicates)' if force else 'No (check duplicates)'}")
        print(f"🤝 Interactive: {'Yes (ask confirmation)' if interactive else 'No (automatic)'}")
        
        # Get existing posts once for efficiency
        if not force:
            print("🔍 Checking for existing posts across all categories...")
            existing_posts = self.get_existing_posts()
            print(f"📊 Found {len(existing_posts)} existing posts")
        else:
            existing_posts = []
        
        # Analyze all categories
        all_analysis = {}
        total_to_publish = 0
        total_skipped = 0
        
        print(f"\n📊 Category Analysis:")
        print("=" * 30)
        
        for category, path in self.categories.items():
            if not os.path.exists(path):
                print(f"⚠️ {category}: Directory not found ({path})")
                continue
            
            content_files = self.get_content_files(path)
            if not content_files:
                print(f"📁 {category}: No files found")
                continue
            
            to_publish = []
            skipped = []
            
            for file in content_files:
                file_path = os.path.join(path, file)
                title = self.extract_title_from_file(file_path)
                
                if not force:
                    existing = self.check_post_exists(title, existing_posts)
                    if existing:
                        skipped.append({
                            'file': file,
                            'title': title,
                            'existing_title': existing['title']['rendered'],
                            'existing_id': existing['id']
                        })
                        continue
                
                to_publish.append({
                    'file': file,
                    'title': title,
                    'file_path': file_path
                })
            
            all_analysis[category] = {
                'path': path,
                'to_publish': to_publish,
                'skipped': skipped,
                'total_files': len(content_files)
            }
            
            total_to_publish += len(to_publish)
            total_skipped += len(skipped)
            
            status_icon = "✅" if to_publish else "⏭️" if skipped else "📁"
            print(f"{status_icon} {category}: {len(to_publish)} new, {len(skipped)} existing, {len(content_files)} total")
        
        print(f"\n🎯 Overall Summary:")
        print(f"  📝 Total to publish: {total_to_publish} posts")
        print(f"  ⏭️ Total skipped: {total_skipped} posts")
        print(f"  📁 Categories with new content: {len([c for c in all_analysis.values() if c['to_publish']])}")
        
        # Show detailed breakdown
        categories_with_new_content = {k: v for k, v in all_analysis.items() if v['to_publish']}
        
        if categories_with_new_content:
            print(f"\n✅ New Content to Publish:")
            for category, data in categories_with_new_content.items():
                print(f"\n  📁 {category} ({len(data['to_publish'])} posts):")
                for item in data['to_publish']:
                    print(f"     • {item['title']}")
        
        if not total_to_publish:
            print("\n🎉 All content is already published! No new posts to add.")
            return {
                'success': True,
                'total_published': 0,
                'total_skipped': total_skipped,
                'categories_processed': 0,
                'results': all_analysis
            }
        
        # Confirmation
        if interactive:
            print(f"\n⚠️ Ready to publish {total_to_publish} new posts across {len(categories_with_new_content)} categories")
            if not force and total_skipped > 0:
                print(f"   (Will skip {total_skipped} existing posts)")
            
            confirm = input("Continue with bulk publication? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Bulk publication cancelled")
                return {'cancelled': True, 'total_to_publish': total_to_publish}
        
        # Publish each category with new content
        results = {}
        total_published = 0
        total_errors = 0
        
        print(f"\n🚀 Starting bulk publication...")
        
        for category, data in categories_with_new_content.items():
            print(f"\n" + "="*60)
            result = self.publish_category(category, force=True, as_draft=as_draft)  # Force to skip individual confirmations
            results[category] = result
            
            if result.get('success'):
                total_published += result.get('published', 0)
                print(f"✅ {category}: Published {result.get('published', 0)} posts")
            else:
                total_errors += 1
                print(f"❌ {category}: Failed - {result.get('error', 'Unknown error')}")
        
        # Final summary
        print(f"\n" + "="*60)
        print(f"🎉 Bulk Publication Complete!")
        print(f"=" * 30)
        print(f"✅ Successfully published: {total_published} posts")
        print(f"⏭️ Skipped (duplicates): {total_skipped} posts") 
        print(f"❌ Categories with errors: {total_errors}")
        print(f"📁 Categories processed: {len(categories_with_new_content)}")
        
        return {
            'success': total_errors == 0,
            'total_published': total_published,
            'total_skipped': total_skipped,
            'total_errors': total_errors,
            'categories_processed': len(categories_with_new_content),
            'results': results,
            'analysis': all_analysis
        }
    
    def interactive_menu(self):
        """Interactive menu for smart publishing"""
        print("🎯 Smart WordPress Publisher")
        print("============================")
        print(f"🌐 Site: {self.wp_site}")
        print()
        
        # Test connection
        if not self.test_connection():
            return False
        
        while True:
            print("\n📁 Available Categories:")
            for i, category in enumerate(self.categories.keys(), 1):
                path = self.categories[category]
                file_count = len(self.get_content_files(path)) if os.path.exists(path) else 0
                print(f"  {i}. {category} ({file_count} files)")
            
            print(f"\n🛠️ Publishing Options:")
            print(f"  A. 📝 Publish as DRAFTS (safe)")
            print(f"  B. 🚀 Publish LIVE posts")
            print(f"  C. 🔄 Force publish (ignore duplicates)")
            print(f"  D. 🔍 Check existing posts only")
            print(f"  E. 🌐 Publish ALL categories (smart)")
            print(f"  F. 🌐 Publish ALL as drafts (safe)")
            print(f"  G. 🌐 Force publish ALL (ignore duplicates)")
            print(f"  H. 📊 Analyze ALL categories (no publishing)")
            print(f"  X. ❌ Exit")
            
            choice = input("\nSelect category (1-6) or option (A-H/X): ").strip().upper()
            
            if choice == 'X':
                print("👋 Goodbye!")
                break
            
            elif choice == 'D':
                # Just show existing posts
                existing = self.get_existing_posts()
                print(f"\n📊 Found {len(existing)} existing posts:")
                for post in existing[:10]:  # Show first 10
                    print(f"   • {post['title']['rendered']} ({post['status']})")
                if len(existing) > 10:
                    print(f"   ... and {len(existing) - 10} more")
                continue
            
            elif choice == 'E':
                # Publish all categories (smart)
                result = self.publish_all_categories(force=False, as_draft=False, interactive=True)
                self._show_bulk_result(result)
            
            elif choice == 'F':
                # Publish all as drafts
                result = self.publish_all_categories(force=False, as_draft=True, interactive=True)
                self._show_bulk_result(result)
            
            elif choice == 'G':
                # Force publish all
                print("\n⚠️ WARNING: This will publish ALL content, including existing posts!")
                confirm = input("Are you sure? Type 'FORCE ALL' to confirm: ").strip()
                if confirm == 'FORCE ALL':
                    result = self.publish_all_categories(force=True, as_draft=False, interactive=False)
                    self._show_bulk_result(result)
                else:
                    print("❌ Force publication cancelled")
            
            elif choice == 'H':
                # Analyze all categories
                result = self.publish_all_categories(force=False, as_draft=False, interactive=False)
                # This will show analysis but not publish (user will decline)
                continue
            
            elif choice in ['A', 'B', 'C']:
                # Select category
                cat_choice = input("Select category number (1-6): ").strip()
                try:
                    cat_index = int(cat_choice) - 1
                    if 0 <= cat_index < len(list(self.categories.keys())):
                        category = list(self.categories.keys())[cat_index]
                        
                        as_draft = choice == 'A'
                        force = choice == 'C'
                        
                        result = self.publish_category(category, force=force, as_draft=as_draft)
                        self._show_single_result(result)
                    else:
                        print("❌ Invalid category number")
                except ValueError:
                    print("❌ Invalid number")
            
            elif choice.isdigit():
                cat_index = int(choice) - 1
                if 0 <= cat_index < len(list(self.categories.keys())):
                    category = list(self.categories.keys())[cat_index]
                    
                    # Quick publish menu
                    print(f"\n🎯 Publishing {category}:")
                    print("  1. 📝 As drafts")
                    print("  2. 🚀 Live posts") 
                    print("  3. 🔄 Force (ignore duplicates)")
                    
                    pub_choice = input("Publishing mode (1-3): ").strip()
                    
                    if pub_choice == '1':
                        result = self.publish_category(category, as_draft=True)
                    elif pub_choice == '2':
                        result = self.publish_category(category)
                    elif pub_choice == '3':
                        result = self.publish_category(category, force=True)
                    else:
                        print("❌ Invalid choice")
                        continue
                    
                    self._show_single_result(result)
                else:
                    print("❌ Invalid category number")
            else:
                print("❌ Invalid choice")
        
        return True
    
    def _show_single_result(self, result: Dict):
        """Show result of single category publishing"""
        if result.get('success'):
            print(f"\n🎉 Success! Published {result['published']} posts, skipped {result['skipped']} duplicates")
        elif result.get('cancelled'):
            print("❌ Publication cancelled")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    def _show_bulk_result(self, result: Dict):
        """Show result of bulk publishing"""
        if result.get('cancelled'):
            print("❌ Bulk publication cancelled")
        elif result.get('success'):
            print(f"\n🎉 Bulk publication successful!")
            print(f"   ✅ Published: {result['total_published']} posts")
            print(f"   ⏭️ Skipped: {result['total_skipped']} duplicates")
            print(f"   📁 Categories: {result['categories_processed']}")
        else:
            print(f"\n⚠️ Bulk publication completed with some errors:")
            print(f"   ✅ Published: {result['total_published']} posts")
            print(f"   ⏭️ Skipped: {result['total_skipped']} duplicates")
            print(f"   ❌ Errors: {result['total_errors']}")
            print(f"   📁 Categories: {result['categories_processed']}")

def main():
    """Main execution function"""
    # Check environment variables
    required_vars = ['WP_SITE', 'WP_USER', 'WP_APP_PASS']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your_value'")
        return False
    
    try:
        publisher = SmartWordPressPublisher()
        return publisher.interactive_menu()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()