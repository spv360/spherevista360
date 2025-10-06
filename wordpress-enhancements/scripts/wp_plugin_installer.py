#!/usr/bin/env python3
"""
WordPress Plugin Installer via REST API
Alternative to WP-CLI for plugin management
"""

import os
import sys
import requests
import base64
import json
import time
from typing import Dict, List, Optional

class WordPressPluginInstaller:
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
        
        # Essential plugins to install
        self.essential_plugins = [
            {
                'slug': 'wordpress-seo',
                'name': 'Yoast SEO',
                'description': 'Complete SEO solution'
            },
            {
                'slug': 'wp-smushit',
                'name': 'Smush',
                'description': 'Image compression and optimization'
            },
            {
                'slug': 'wordfence',
                'name': 'Wordfence Security',
                'description': 'Comprehensive security protection'
            },
            {
                'slug': 'updraftplus',
                'name': 'UpdraftPlus',
                'description': 'Backup and restoration'
            },
            {
                'slug': 'contact-form-7',
                'name': 'Contact Form 7',
                'description': 'Contact form builder'
            },
            {
                'slug': 'google-analytics-for-wordpress',
                'name': 'MonsterInsights',
                'description': 'Google Analytics integration'
            }
        ]
    
    def test_connection(self) -> bool:
        """Test WordPress API connection"""
        print("🔌 Testing WordPress connection...")
        
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"  ✅ Connected as: {user_data.get('name', 'Unknown')}")
                return True
            else:
                print(f"  ❌ Connection failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Connection error: {e}")
            return False
    
    def get_installed_plugins(self) -> List[Dict]:
        """Get list of currently installed plugins"""
        print("📦 Checking installed plugins...")
        
        # Note: WordPress REST API doesn't provide plugin management by default
        # This would require a custom endpoint or plugin
        
        print("  ⚠️ Plugin status check requires WordPress admin access")
        print("  📍 Manual verification needed in WordPress Admin → Plugins")
        
        return []
    
    def create_manual_installation_guide(self) -> str:
        """Create detailed manual installation guide"""
        print("📋 Creating manual installation guide...")
        
        guide = """# WordPress Plugin Installation Guide for SphereVista360

## 🚨 Essential Plugins (Install in this order)

### 1. Wordfence Security (CRITICAL - Install First)
- **Plugin Name**: Wordfence Security
- **WordPress Repository**: https://wordpress.org/plugins/wordfence/
- **Installation**:
  1. Go to WordPress Admin → Plugins → Add New
  2. Search for "Wordfence Security"
  3. Click "Install Now" → "Activate"
- **Configuration**:
  - Enable Web Application Firewall
  - Set up email alerts
  - Run initial scan

### 2. UpdraftPlus (CRITICAL - Install Second)
- **Plugin Name**: UpdraftPlus WordPress Backup Plugin
- **WordPress Repository**: https://wordpress.org/plugins/updraftplus/
- **Installation**:
  1. Go to WordPress Admin → Plugins → Add New
  2. Search for "UpdraftPlus"
  3. Click "Install Now" → "Activate"
- **Configuration**:
  - Set up automated daily backups
  - Configure cloud storage (Google Drive, Dropbox, etc.)
  - Test backup restoration

### 3. Yoast SEO (Essential)
- **Plugin Name**: Yoast SEO
- **WordPress Repository**: https://wordpress.org/plugins/wordpress-seo/
- **Installation**:
  1. Go to WordPress Admin → Plugins → Add New
  2. Search for "Yoast SEO"
  3. Click "Install Now" → "Activate"
- **Configuration**:
  - Run SEO configuration wizard
  - Set up XML sitemaps
  - Configure meta templates

### 4. Smush (Essential)
- **Plugin Name**: Smush – Compress, Optimize and Lazy Load Images
- **WordPress Repository**: https://wordpress.org/plugins/wp-smushit/
- **Installation**:
  1. Go to WordPress Admin → Plugins → Add New
  2. Search for "Smush"
  3. Click "Install Now" → "Activate"
- **Configuration**:
  - Enable automatic compression
  - Run bulk optimization
  - Enable lazy loading

### 5. Contact Form 7 (Essential)
- **Plugin Name**: Contact Form 7
- **WordPress Repository**: https://wordpress.org/plugins/contact-form-7/
- **Installation**:
  1. Go to WordPress Admin → Plugins → Add New
  2. Search for "Contact Form 7"
  3. Click "Install Now" → "Activate"
- **Configuration**:
  - Create contact form for Contact page
  - Configure email notifications
  - Add CAPTCHA protection

### 6. MonsterInsights (Essential)
- **Plugin Name**: Google Analytics for WordPress by MonsterInsights
- **WordPress Repository**: https://wordpress.org/plugins/google-analytics-for-wordpress/
- **Installation**:
  1. Go to WordPress Admin → Plugins → Add New
  2. Search for "MonsterInsights"
  3. Click "Install Now" → "Activate"
- **Configuration**:
  - Connect Google Analytics account
  - Enable enhanced eCommerce tracking
  - Configure goal tracking

## 🌟 Recommended Plugins (Install after essentials)

### 7. W3 Total Cache (Performance)
- **Plugin Name**: W3 Total Cache
- **WordPress Repository**: https://wordpress.org/plugins/w3-total-cache/
- **Purpose**: Page caching and performance optimization

### 8. Social Warfare (Social Media)
- **Plugin Name**: Social Warfare
- **WordPress Repository**: https://wordpress.org/plugins/social-warfare/
- **Purpose**: Social sharing buttons

### 9. Elementor (Page Builder)
- **Plugin Name**: Elementor Website Builder
- **WordPress Repository**: https://wordpress.org/plugins/elementor/
- **Purpose**: Visual page builder for custom layouts

## 📱 Installation Steps (General Process)

1. **Login to WordPress Admin**
   - Go to: https://spherevista360.com/wp-admin/
   - Use your administrator credentials

2. **Navigate to Plugins**
   - Click "Plugins" in the left sidebar
   - Click "Add New"

3. **Search and Install**
   - Type plugin name in search box
   - Find the correct plugin (verify author/ratings)
   - Click "Install Now"
   - Click "Activate" after installation

4. **Configure Plugin**
   - Look for new menu items in WordPress admin
   - Follow plugin's setup wizard if available
   - Configure settings according to your needs

## ⚠️ Important Notes

- **Install plugins one at a time** to avoid conflicts
- **Always backup your site** before installing new plugins
- **Test functionality** after each plugin installation
- **Only install plugins from trusted sources** (WordPress.org repository)
- **Keep plugins updated** for security and compatibility

## 🔧 Alternative Installation Methods

### Method 1: Upload ZIP File
1. Download plugin ZIP from WordPress.org
2. Go to Plugins → Add New → Upload Plugin
3. Choose ZIP file and upload
4. Activate after installation

### Method 2: FTP Upload (Advanced)
1. Download and extract plugin
2. Upload folder to `/wp-content/plugins/` via FTP
3. Activate in WordPress admin

## 📊 Plugin Priority Schedule

### Week 1 (Critical)
- [ ] Wordfence Security
- [ ] UpdraftPlus
- [ ] Yoast SEO

### Week 2 (Essential)
- [ ] Smush
- [ ] Contact Form 7
- [ ] MonsterInsights

### Week 3 (Performance)
- [ ] W3 Total Cache
- [ ] Social Warfare

### Week 4 (Enhancement)
- [ ] Elementor
- [ ] Additional plugins as needed

## 🎯 Success Checklist

After installing all essential plugins, verify:
- [ ] Security scan completed successfully
- [ ] Backup created and tested
- [ ] XML sitemap generated
- [ ] Images compressed and optimized
- [ ] Contact form working
- [ ] Google Analytics tracking active

## 📞 Support Resources

- **WordPress Plugin Directory**: https://wordpress.org/plugins/
- **Plugin Documentation**: Check each plugin's documentation tab
- **WordPress Support**: https://wordpress.org/support/
- **Security Help**: Wordfence support documentation

---

*Manual Installation Guide for SphereVista360.com*
*Generated: October 5, 2025*
"""
        
        return guide
    
    def create_plugin_verification_script(self) -> str:
        """Create script to verify plugin installations"""
        verification_script = """#!/bin/bash
# WordPress Plugin Verification Script
# Checks if essential plugins are installed and active

echo "🔍 WordPress Plugin Verification for SphereVista360"
echo "================================================="

# Check if we can access WordPress directory
if [ ! -f "wp-config.php" ]; then
    echo "❌ WordPress installation not found in current directory"
    echo "📍 Please run this script from your WordPress root directory"
    exit 1
fi

echo "✅ WordPress installation found"
echo ""

# List of essential plugins to check
declare -a plugins=(
    "wordfence/wordfence.php"
    "updraftplus/updraftplus.php"
    "wordpress-seo/wp-seo.php"
    "wp-smushit/wp-smush.php"
    "contact-form-7/wp-contact-form-7.php"
    "google-analytics-for-wordpress/googleanalytics.php"
)

declare -a plugin_names=(
    "Wordfence Security"
    "UpdraftPlus"
    "Yoast SEO"
    "Smush"
    "Contact Form 7"
    "MonsterInsights"
)

echo "🔌 Checking essential plugins:"
echo "-----------------------------"

for i in "${!plugins[@]}"; do
    plugin_path="wp-content/plugins/${plugins[$i]}"
    plugin_name="${plugin_names[$i]}"
    
    if [ -f "$plugin_path" ]; then
        echo "  ✅ $plugin_name - Installed"
    else
        echo "  ❌ $plugin_name - Not found"
    fi
done

echo ""
echo "📋 Next Steps:"
echo "1. Install any missing plugins via WordPress Admin"
echo "2. Activate all installed plugins"
echo "3. Configure each plugin according to setup guide"
echo "4. Run security scan with Wordfence"
echo "5. Create backup with UpdraftPlus"

echo ""
echo "🌐 WordPress Admin: https://spherevista360.com/wp-admin/"
echo "📖 Setup Guide: See manual installation guide"
"""
        
        return verification_script
    
    def run_installation_helper(self):
        """Run the complete installation helper process"""
        print("🔌 WordPress Plugin Installation Helper")
        print("=" * 40)
        print(f"🌐 Target site: {self.wp_site}")
        print()
        
        # Test connection
        connected = self.test_connection()
        
        if not connected:
            print("⚠️ Cannot connect to WordPress API")
            print("💡 Proceeding with manual installation guide creation")
        
        print()
        
        # Create manual installation guide
        guide_content = self.create_manual_installation_guide()
        verification_script = self.create_plugin_verification_script()
        
        # Save files
        with open('PLUGIN_INSTALLATION_GUIDE.md', 'w') as f:
            f.write(guide_content)
        print("💾 Manual installation guide saved: PLUGIN_INSTALLATION_GUIDE.md")
        
        with open('verify_plugins.sh', 'w') as f:
            f.write(verification_script)
        os.chmod('verify_plugins.sh', 0o755)
        print("💾 Plugin verification script saved: verify_plugins.sh")
        
        # Create quick reference
        quick_ref = {
            'essential_plugins': self.essential_plugins,
            'installation_order': [
                '1. Wordfence Security (CRITICAL)',
                '2. UpdraftPlus (CRITICAL)', 
                '3. Yoast SEO',
                '4. Smush',
                '5. Contact Form 7',
                '6. MonsterInsights'
            ],
            'wordpress_admin_url': f"{self.wp_site}/wp-admin/",
            'plugin_installation_path': 'Plugins → Add New',
            'verification_command': './verify_plugins.sh'
        }
        
        with open('plugin_quick_reference.json', 'w') as f:
            json.dump(quick_ref, f, indent=2)
        print("💾 Quick reference saved: plugin_quick_reference.json")
        
        print(f"\n🎯 Manual Installation Required")
        print("=" * 30)
        print("📋 Essential Plugins (6):")
        for i, plugin in enumerate(self.essential_plugins, 1):
            print(f"  {i}. {plugin['name']} - {plugin['description']}")
        
        print(f"\n🌐 WordPress Admin: {self.wp_site}/wp-admin/")
        print("📖 Detailed Guide: PLUGIN_INSTALLATION_GUIDE.md")
        print("🔍 Verification: ./verify_plugins.sh")
        
        print(f"\n⚡ Quick Start:")
        print("1. Open WordPress Admin in browser")
        print("2. Go to Plugins → Add New")
        print("3. Install plugins in the order listed above")
        print("4. Run ./verify_plugins.sh to check installation")
        
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
        print("\n⚠️ Running in documentation-only mode")
        
        # Create installer without credentials for documentation
        installer = WordPressPluginInstaller.__new__(WordPressPluginInstaller)
        installer.wp_site = "https://spherevista360.com"
        installer.essential_plugins = [
            {'slug': 'wordpress-seo', 'name': 'Yoast SEO', 'description': 'Complete SEO solution'},
            {'slug': 'wp-smushit', 'name': 'Smush', 'description': 'Image compression'},
            {'slug': 'wordfence', 'name': 'Wordfence Security', 'description': 'Security protection'},
            {'slug': 'updraftplus', 'name': 'UpdraftPlus', 'description': 'Backup solution'},
            {'slug': 'contact-form-7', 'name': 'Contact Form 7', 'description': 'Contact forms'},
            {'slug': 'google-analytics-for-wordpress', 'name': 'MonsterInsights', 'description': 'Analytics'}
        ]
        return installer.run_installation_helper()
    
    try:
        installer = WordPressPluginInstaller()
        return installer.run_installation_helper()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()