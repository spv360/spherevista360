#!/usr/bin/env python3
"""
Smart WordPress Content Removal Script
Handles permissions properly and protects critical pages
"""

import os
import sys
import requests
import base64
import json
from typing import Dict, List, Optional

class SmartContentRemover:
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
        
        # Pages/posts that should NEVER be deleted
        self.protected_items = {
            'titles': [
                'home', 'blog', 'about', 'contact', 'privacy policy', 
                'terms of service', 'terms and conditions', 'sitemap',
                'main page', 'front page', 'landing page'
            ],
            'slugs': [
                'home', 'blog', 'about', 'contact', 'privacy', 'terms',
                'sitemap', 'main', 'front-page', 'landing'
            ]
        }
    
    def is_protected_content(self, item: Dict) -> tuple[bool, str]:
        """Check if content should be protected from deletion"""
        title = item.get('title', '').lower().strip()
        slug = item.get('slug', '').lower().strip()
        content_type = item.get('type', '')
        
        # Check if it's a protected title
        for protected_title in self.protected_items['titles']:
            if protected_title in title:
                return True, f"Protected page: {protected_title}"
        
        # Check if it's a protected slug
        for protected_slug in self.protected_items['slugs']:
            if protected_slug in slug:
                return True, f"Protected slug: {protected_slug}"
        
        # Check if it's the front page or blog page
        if content_type == 'page':
            try:
                # Get WordPress settings to check front page
                settings_response = requests.get(
                    f"{self.wp_site}/wp-json/wp/v2/settings",
                    headers=self.headers
                )
                if settings_response.status_code == 200:
                    settings = settings_response.json()
                    front_page_id = settings.get('page_on_front', 0)
                    blog_page_id = settings.get('page_for_posts', 0)
                    
                    if item.get('id') == front_page_id:
                        return True, "WordPress front page"
                    if item.get('id') == blog_page_id:
                        return True, "WordPress blog page"
            except:
                pass  # Continue with other checks
        
        return False, ""
    
    def can_delete_item(self, item: Dict) -> tuple[bool, str]:
        """Check if user has permission to delete this specific item"""
        item_type = item.get('type', '')
        item_id = item.get('id')
        
        # First check if it's protected
        is_protected, reason = self.is_protected_content(item)
        if is_protected:
            return False, f"Protected content: {reason}"
        
        # Check deletion permissions by trying to get the item with edit context
        try:
            if item_type == 'post':
                url = f"{self.wp_site}/wp-json/wp/v2/posts/{item_id}?context=edit"
            elif item_type == 'page':
                url = f"{self.wp_site}/wp-json/wp/v2/pages/{item_id}?context=edit"
            else:
                return False, f"Unknown content type: {item_type}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                item_data = response.json()
                # Check if the item has a delete capability
                if item_data.get('status') == 'trash':
                    return False, "Already in trash"
                return True, "Can delete"
            elif response.status_code == 403:
                return False, "No edit permission"
            elif response.status_code == 401:
                return False, "Authentication required"
            else:
                return False, f"Cannot access (Status: {response.status_code})"
                
        except Exception as e:
            return False, f"Permission check failed: {e}"
    
    def safely_remove_item(self, item: Dict) -> tuple[bool, str]:
        """Safely remove a content item with proper error handling"""
        item_type = item.get('type', '')
        item_id = item.get('id')
        item_title = item.get('title', 'Unknown')
        
        # Check if we can delete this item
        can_delete, reason = self.can_delete_item(item)
        if not can_delete:
            return False, reason
        
        try:
            # Determine the correct API endpoint
            if item_type == 'post':
                url = f"{self.wp_site}/wp-json/wp/v2/posts/{item_id}"
            elif item_type == 'page':
                url = f"{self.wp_site}/wp-json/wp/v2/pages/{item_id}"
            else:
                return False, f"Unknown content type: {item_type}"
            
            # Move to trash (safer than permanent deletion)
            response = requests.delete(url, headers=self.headers)
            
            if response.status_code == 200:
                return True, "Successfully moved to trash"
            elif response.status_code == 403:
                return False, "Permission denied (protected content)"
            elif response.status_code == 401:
                return False, "Authentication failed"
            elif response.status_code == 404:
                return False, "Content not found (may already be deleted)"
            else:
                return False, f"Failed (Status: {response.status_code})"
                
        except Exception as e:
            return False, f"Error: {e}"
    
    def load_removal_plan(self) -> List[Dict]:
        """Load the removal plan from the audit report"""
        try:
            with open('wordpress-enhancements/configs/content_audit_report.json', 'r') as f:
                report = json.load(f)
                return report.get('removal_plan', [])
        except FileNotFoundError:
            print("❌ No audit report found. Please run the content audit first:")
            print("   ./wordpress-enhancements/scripts/quick_content_audit.sh")
            return []
        except Exception as e:
            print(f"❌ Error loading audit report: {e}")
            return []
    
    def run_smart_removal(self):
        """Run the smart content removal process"""
        print("🧠 Smart WordPress Content Removal")
        print("=" * 35)
        print(f"🌐 Site: {self.wp_site}")
        print(f"👤 User: {self.wp_user}")
        print()
        
        # Load removal plan
        removal_plan = self.load_removal_plan()
        if not removal_plan:
            return False
        
        print(f"📋 Loaded {len(removal_plan)} items for review")
        print()
        
        # Categorize items
        can_remove = []
        protected_items = []
        permission_denied = []
        
        print("🔍 Analyzing removal permissions...")
        for item in removal_plan:
            can_delete, reason = self.can_delete_item(item)
            
            if can_delete:
                can_remove.append(item)
            elif "protected" in reason.lower():
                protected_items.append((item, reason))
            else:
                permission_denied.append((item, reason))
        
        # Display categorized results
        print(f"\n📊 Removal Analysis:")
        print(f"   ✅ Can safely remove: {len(can_remove)}")
        print(f"   🛡️  Protected (will skip): {len(protected_items)}")
        print(f"   ❌ Permission denied: {len(permission_denied)}")
        print()
        
        # Show protected items
        if protected_items:
            print("🛡️  PROTECTED ITEMS (will be skipped):")
            for item, reason in protected_items:
                print(f"   • {item['title']} - {reason}")
            print()
        
        # Show permission denied items
        if permission_denied:
            print("❌ PERMISSION DENIED (will be skipped):")
            for item, reason in permission_denied:
                print(f"   • {item['title']} - {reason}")
            print()
        
        # Show items that will be removed
        if can_remove:
            print("🗑️  ITEMS TO BE REMOVED:")
            for i, item in enumerate(can_remove, 1):
                print(f"   {i:2d}. {item['title']} ({item['type']})")
                print(f"       Reason: {item['reason']}")
            print()
            
            # Confirmation
            if len(can_remove) > 0:
                response = input(f"Proceed with removing {len(can_remove)} items? (type 'yes' to confirm): ")
                if response.lower() != 'yes':
                    print("❌ Operation cancelled")
                    return False
                
                # Remove items
                print(f"\n🗑️  Removing {len(can_remove)} items...")
                success_count = 0
                
                for item in can_remove:
                    success, message = self.safely_remove_item(item)
                    if success:
                        print(f"✅ {item['title']}")
                        success_count += 1
                    else:
                        print(f"❌ {item['title']} - {message}")
                
                print(f"\n🎉 Removal complete!")
                print(f"   ✅ Successfully removed: {success_count}")
                print(f"   🛡️  Protected (skipped): {len(protected_items)}")
                print(f"   ❌ Failed/denied: {len(permission_denied) + len(can_remove) - success_count}")
                print(f"\n💡 Removed items are in WordPress trash and can be restored if needed")
                
                return True
        else:
            print("ℹ️  No items can be safely removed at this time.")
            print("   All items are either protected or you lack permissions.")
            return False

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
        remover = SmartContentRemover()
        return remover.run_smart_removal()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()