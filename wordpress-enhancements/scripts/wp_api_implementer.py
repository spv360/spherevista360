#!/usr/bin/env python3
"""
WordPress API Implementation Helper for SphereVista360.com
Automates the application of functionality enhancements via WordPress REST API
"""

import os
import sys
import requests
import base64
import json
from typing import Dict, List, Optional, Tuple

class WordPressAPIImplementer:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_APP_PASS')
        
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
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        print("🔌 Testing WordPress API connection...")
        
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"  ✅ Connected as: {user_data.get('name', 'Unknown')}")
                print(f"  ✅ Capabilities: {len(user_data.get('capabilities', {}))}")
                return True
            else:
                print(f"  ❌ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Connection error: {e}")
            return False
    
    def create_custom_css_customizer_setting(self) -> bool:
        """Add custom CSS via Customizer API"""
        print("🎨 Adding custom CSS styles...")
        
        try:
            # Read the custom CSS file
            with open('custom_styles.css', 'r') as f:
                custom_css = f.read()
            
            # Update theme customizer with custom CSS
            # Note: This requires additional permissions and may need a different approach
            print("  ⚠️ Custom CSS needs manual application to theme")
            print("  📝 File location: custom_styles.css")
            return True
            
        except FileNotFoundError:
            print("  ❌ custom_styles.css not found")
            return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def update_site_settings(self) -> bool:
        """Update general site settings"""
        print("⚙️ Updating site settings...")
        
        settings_updates = {
            'title': 'SphereVista360 - 360-Degree Global Insights',
            'description': 'Comprehensive insights on finance, technology, politics, travel, and global affairs from every angle.',
            'timezone_string': 'UTC',
            'date_format': 'F j, Y',
            'time_format': 'g:i a',
            'start_of_week': 1  # Monday
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/settings",
                headers=self.headers,
                json=settings_updates
            )
            
            if response.status_code == 200:
                print("  ✅ Site settings updated")
                return True
            else:
                print(f"  ⚠️ Settings update may require different permissions: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error updating settings: {e}")
            return False
    
    def create_navigation_menu(self) -> bool:
        """Create and configure navigation menu"""
        print("🧭 Setting up navigation menu...")
        
        # Note: WordPress REST API doesn't directly support menu creation
        # This would typically require a custom endpoint or direct database access
        
        menu_structure = [
            {'title': 'Home', 'url': self.wp_site},
            {'title': 'Finance', 'url': f"{self.wp_site}/category/finance/"},
            {'title': 'Technology', 'url': f"{self.wp_site}/category/tech/"},
            {'title': 'Politics', 'url': f"{self.wp_site}/category/politics/"},
            {'title': 'Travel', 'url': f"{self.wp_site}/category/travel/"},
            {'title': 'World', 'url': f"{self.wp_site}/category/world/"},
            {'title': 'About', 'url': f"{self.wp_site}/about-3/"},
            {'title': 'Contact', 'url': f"{self.wp_site}/contact-3/"}
        ]
        
        print("  📋 Menu structure defined:")
        for item in menu_structure:
            print(f"    • {item['title']}")
        
        print("  ⚠️ Menu creation requires manual setup in WordPress Admin")
        print("  📍 Go to: Appearance → Menus")
        
        return True
    
    def optimize_existing_posts_seo(self) -> Dict:
        """Enhance SEO for existing posts"""
        print("🔍 Optimizing existing posts for SEO...")
        
        try:
            # Get all published posts
            response = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={'status': 'publish', 'per_page': 100}
            )
            
            if response.status_code != 200:
                print(f"  ❌ Failed to fetch posts: {response.status_code}")
                return {'success': False, 'updated': 0}
            
            posts = response.json()
            updated_count = 0
            
            for post in posts:
                post_id = post['id']
                title = post['title']['rendered']
                
                # Generate SEO-friendly excerpt if missing
                if not post.get('excerpt', {}).get('rendered', '').strip():
                    content = post['content']['rendered']
                    # Create excerpt from content (first 150 chars)
                    import re
                    clean_content = re.sub(r'<[^>]+>', '', content)
                    excerpt = clean_content[:150].strip() + '...'
                    
                    # Update post with excerpt
                    update_data = {'excerpt': excerpt}
                    
                    update_response = requests.post(
                        f"{self.base_url}/posts/{post_id}",
                        headers=self.headers,
                        json=update_data
                    )
                    
                    if update_response.status_code == 200:
                        updated_count += 1
                        print(f"  ✅ Updated: {title[:50]}...")
                    else:
                        print(f"  ⚠️ Failed to update: {title[:50]}...")
            
            print(f"  📊 Updated {updated_count} posts")
            return {'success': True, 'updated': updated_count}
            
        except Exception as e:
            print(f"  ❌ Error optimizing posts: {e}")
            return {'success': False, 'updated': 0}
    
    def setup_categories_and_tags(self) -> bool:
        """Ensure all required categories exist"""
        print("📂 Setting up categories...")
        
        required_categories = [
            {'name': 'Finance', 'slug': 'finance', 'description': 'Financial markets, investment insights, and economic analysis'},
            {'name': 'Technology', 'slug': 'tech', 'description': 'Latest in AI, cybersecurity, and digital transformation'},
            {'name': 'Politics', 'slug': 'politics', 'description': 'Global elections, policy analysis, and governance trends'},
            {'name': 'Travel', 'slug': 'travel', 'description': 'Destination guides, visa information, and travel insights'},
            {'name': 'World', 'slug': 'world', 'description': 'Global affairs, international relations, and world events'}
        ]
        
        created_count = 0
        
        try:
            for category in required_categories:
                # Check if category exists
                response = requests.get(
                    f"{self.base_url}/categories",
                    headers=self.headers,
                    params={'slug': category['slug']}
                )
                
                if response.status_code == 200 and response.json():
                    print(f"  ✅ Category exists: {category['name']}")
                else:
                    # Create category
                    create_response = requests.post(
                        f"{self.base_url}/categories",
                        headers=self.headers,
                        json=category
                    )
                    
                    if create_response.status_code == 201:
                        print(f"  ✅ Created category: {category['name']}")
                        created_count += 1
                    else:
                        print(f"  ⚠️ Failed to create: {category['name']}")
            
            print(f"  📊 Created {created_count} new categories")
            return True
            
        except Exception as e:
            print(f"  ❌ Error setting up categories: {e}")
            return False
    
    def create_essential_widgets(self) -> bool:
        """Set up essential widgets via API"""
        print("🧩 Configuring widgets...")
        
        # Note: WordPress REST API has limited widget support
        # This is primarily for informational/configuration purposes
        
        widget_config = {
            'sidebar-1': [
                {'type': 'categories', 'title': 'Browse Categories'},
                {'type': 'recent-posts', 'title': 'Latest Updates'},
                {'type': 'search', 'title': 'Search Site'},
                {'type': 'text', 'title': 'About SphereVista360', 
                 'content': 'Exploring the world from every angle with comprehensive insights on finance, technology, politics, travel, and global affairs.'}
            ]
        }
        
        print("  📋 Widget configuration prepared:")
        for area, widgets in widget_config.items():
            print(f"    📍 {area}:")
            for widget in widgets:
                print(f"      • {widget.get('title', widget['type'])}")
        
        print("  ⚠️ Widget setup requires manual configuration")
        print("  📍 Go to: Appearance → Widgets")
        
        return True
    
    def generate_implementation_report(self) -> Dict:
        """Generate comprehensive implementation report"""
        print("📋 Generating implementation report...")
        
        # Test all connections and gather status
        api_connected = self.test_connection()
        
        if api_connected:
            # Run optimizations that can be automated
            seo_results = self.optimize_existing_posts_seo()
            categories_setup = self.setup_categories_and_tags()
            settings_updated = self.update_site_settings()
        else:
            seo_results = {'success': False, 'updated': 0}
            categories_setup = False
            settings_updated = False
        
        report = {
            'connection_status': api_connected,
            'automated_tasks': {
                'seo_optimization': seo_results,
                'categories_setup': categories_setup,
                'settings_updated': settings_updated
            },
            'manual_tasks_required': [
                'Apply custom CSS from custom_styles.css',
                'Create navigation menu structure',
                'Configure sidebar widgets',
                'Install recommended plugins',
                'Apply security hardening measures',
                'Set up footer content'
            ],
            'next_steps': [
                'Review WORDPRESS_IMPLEMENTATION_GUIDE.md',
                'Install essential plugins from install_plugins.sh',
                'Apply security settings from security files',
                'Configure theme customizations',
                'Set up automated backups',
                'Configure Google Analytics'
            ],
            'files_available': [
                'custom_styles.css',
                'footer_content.html',
                'wp_functionality_config.json',
                'plugin_recommendations.json',
                'install_plugins.sh',
                'security_htaccess.txt',
                'wp_config_security.txt',
                'security_checklist.json'
            ]
        }
        
        return report
    
    def run_implementation(self):
        """Execute WordPress functionality implementation"""
        print("🚀 WordPress API Implementation")
        print("=" * 35)
        print(f"🌐 Target site: {self.wp_site}")
        print()
        
        # Generate comprehensive report
        report = self.generate_implementation_report()
        
        # Save report
        with open('implementation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Implementation Summary:")
        print("=" * 25)
        
        if report['connection_status']:
            print("✅ WordPress API connection successful")
            
            automated = report['automated_tasks']
            if automated['seo_optimization']['success']:
                print(f"✅ SEO optimized {automated['seo_optimization']['updated']} posts")
            
            if automated['categories_setup']:
                print("✅ Categories verified/created")
            
            if automated['settings_updated']:
                print("✅ Site settings updated")
        else:
            print("❌ WordPress API connection failed")
            print("   Manual implementation required")
        
        print(f"\n📋 Manual Tasks Required ({len(report['manual_tasks_required'])}):")
        for i, task in enumerate(report['manual_tasks_required'], 1):
            print(f"   {i}. {task}")
        
        print(f"\n🎯 Next Steps ({len(report['next_steps'])}):")
        for i, step in enumerate(report['next_steps'], 1):
            print(f"   {i}. {step}")
        
        print(f"\n📁 Generated Files ({len(report['files_available'])}):")
        for file in report['files_available']:
            if os.path.exists(file):
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} (missing)")
        
        print(f"\n💾 Implementation report saved to: implementation_report.json")
        
        return True

def main():
    """Main execution function"""
    # Check environment variables
    required_vars = ['WP_SITE', 'WP_USER', 'WP_APP_PASS']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your_value'")
        print("\n⚠️ Cannot proceed without WordPress credentials")
        return False
    
    try:
        implementer = WordPressAPIImplementer()
        return implementer.run_implementation()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()