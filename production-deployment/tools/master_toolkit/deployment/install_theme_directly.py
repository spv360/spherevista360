#!/usr/bin/env python3
"""
WordPress Theme Direct Installer
Installs theme files directly via WordPress REST API
"""

import os
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# WordPress REST API doesn't have theme file write endpoints by default
# We'll create a custom installer that uses the file manager if available

def create_installer_plugin():
    """Create a simple plugin that can install themes via REST API"""
    print("🔌 Creating theme installer plugin...")
    
    plugin_code = '''<?php
/**
 * Plugin Name: SphereVista360 Theme Installer
 * Description: REST API endpoint to install and activate themes
 * Version: 1.0
 */

add_action('rest_api_init', function() {
    register_rest_route('installer/v1', '/theme', array(
        'methods' => 'POST',
        'callback' => 'install_spherevista_theme',
        'permission_callback' => function() {
            return current_user_can('install_themes');
        }
    ));
    
    register_rest_route('installer/v1', '/activate', array(
        'methods' => 'POST',
        'callback' => 'activate_spherevista_theme',
        'permission_callback' => function() {
            return current_user_can('switch_themes');
        }
    ));
});

function install_spherevista_theme($request) {
    $zip_url = $request->get_param('zip_url');
    
    if (empty($zip_url)) {
        return new WP_Error('no_url', 'ZIP URL is required', array('status' => 400));
    }
    
    require_once(ABSPATH . 'wp-admin/includes/file.php');
    require_once(ABSPATH . 'wp-admin/includes/class-wp-upgrader.php');
    require_once(ABSPATH . 'wp-admin/includes/theme.php');
    
    // Download and install theme
    $upgrader = new Theme_Upgrader(new WP_Ajax_Upgrader_Skin());
    $result = $upgrader->install($zip_url);
    
    if (is_wp_error($result)) {
        return new WP_Error('install_failed', $result->get_error_message(), array('status' => 500));
    }
    
    return array(
        'success' => true,
        'message' => 'Theme installed successfully',
        'theme' => $upgrader->theme_info()
    );
}

function activate_spherevista_theme($request) {
    $theme_slug = $request->get_param('theme_slug') ?: 'spherevista-theme';
    
    $theme = wp_get_theme($theme_slug);
    
    if (!$theme->exists()) {
        return new WP_Error('theme_not_found', 'Theme not found', array('status' => 404));
    }
    
    switch_theme($theme_slug);
    
    return array(
        'success' => true,
        'message' => 'Theme activated successfully',
        'theme' => array(
            'name' => $theme->get('Name'),
            'version' => $theme->get('Version'),
            'author' => $theme->get('Author')
        )
    );
}
?>'''
    
    return plugin_code

def install_plugin():
    """Install the theme installer plugin"""
    print("🔌 Installing theme installer plugin...")
    
    plugin_code = create_installer_plugin()
    
    # We need to upload this as a PHP file
    # For now, let's provide instructions
    print("\n⚠️  Plugin code generated. To use it:")
    print("\n1. Create file: wp-content/plugins/spherevista-installer.php")
    print("2. Copy the code below:")
    print("=" * 60)
    print(plugin_code)
    print("=" * 60)
    print("\n3. Or upload via FTP/cPanel")
    
    return plugin_code

def install_theme_via_api():
    """Install theme using the custom REST API endpoint"""
    print("\n📦 Installing theme via REST API...")
    
    zip_url = "https://spherevista360.com/wp-content/uploads/2025/10/spherevista360-theme.zip"
    url = f"{WORDPRESS_URL}/wp-json/installer/v1/theme"
    
    data = {
        'zip_url': zip_url
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        if response.status_code == 200:
            print("✅ Theme installed successfully!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Installation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def activate_theme_via_api():
    """Activate theme using the custom REST API endpoint"""
    print("\n🎨 Activating theme via REST API...")
    
    url = f"{WORDPRESS_URL}/wp-json/installer/v1/activate"
    
    data = {
        'theme_slug': 'spherevista-theme'
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        if response.status_code == 200:
            print("✅ Theme activated successfully!")
            data = response.json()
            if 'theme' in data:
                print(f"   Theme: {data['theme'].get('name', 'Unknown')}")
                print(f"   Version: {data['theme'].get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Activation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 WordPress Theme Direct Installer")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    # For now, provide manual instructions since we can't directly write PHP files
    print("\n📋 EASIEST METHOD - Manual Upload:")
    print("=" * 60)
    print("\n1. Go to WordPress Admin:")
    print(f"   {WORDPRESS_URL}/wp-admin/theme-install.php")
    print("\n2. Click 'Upload Theme' button")
    print("\n3. Choose file:")
    print("   /home/kddevops/projects/spherevista360/spherevista360-theme.zip")
    print("   (Already available in your downloads folder)")
    print("\n4. Click 'Install Now'")
    print("\n5. Click 'Activate'")
    print("\n6. ✨ Theme will auto-configure:")
    print("   • Sets Homepage as front page")
    print("   • Creates main navigation menu")
    print("   • Sets Blog page for posts")
    print("   • Configures permalinks")
    
    print("\n" + "=" * 60)
    print("📥 ALTERNATIVE - Download from Media Library:")
    print("=" * 60)
    print("\n The theme ZIP is already uploaded to:")
    print(" https://spherevista360.com/wp-content/uploads/2025/10/spherevista360-theme.zip")
    print("\n You can download it and install via WordPress admin.")
    
    print("\n" + "=" * 60)
    print("🎉 Ready to Install!")
    print("=" * 60)

if __name__ == "__main__":
    main()
