#!/usr/bin/env python3
"""
Interactive WordPress Setup Configurator
Helps configure WordPress credentials and run theme setup
"""

import os
import sys
import subprocess

def get_user_input():
    """Get WordPress credentials from user"""
    print("🔧 WordPress Theme Setup Configuration")
    print("=" * 50)
    print()
    
    print("Please provide your WordPress site details:")
    print()
    
    # Get site URL
    site_url = input("🌐 WordPress Site URL (e.g., https://yoursite.com): ").strip()
    if not site_url.startswith(('http://', 'https://')):
        site_url = 'https://' + site_url
    
    # Remove trailing slash
    site_url = site_url.rstrip('/')
    
    # Get username
    username = input("👤 WordPress Admin Username: ").strip()
    
    # Get password
    print("\n🔐 WordPress Password Options:")
    print("   A) Regular WordPress password")
    print("   B) Application Password (recommended for security)")
    print("      Create one at: WordPress Admin > Users > Profile > Application Passwords")
    
    password = input("\n🔑 WordPress Password: ").strip()
    
    return site_url, username, password

def create_env_file(site_url, username, password):
    """Create .env file with user credentials"""
    env_content = f"""# WordPress API Configuration for SphereVista360
WORDPRESS_BASE_URL={site_url}
WORDPRESS_USERNAME={username}
WORDPRESS_PASSWORD={password}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env configuration file")

def run_theme_setup():
    """Run the WordPress theme setup script"""
    print("\n🚀 Running WordPress Theme Setup...")
    print("=" * 50)
    
    try:
        # Make sure we have the required dependencies
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'python-dotenv'], 
                      capture_output=True, check=True)
        
        # Run the setup script
        result = subprocess.run([sys.executable, 'wordpress_theme_setup.py'], 
                              capture_output=False, text=True)
        
        return result.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running setup: {e}")
        return False
    except FileNotFoundError:
        print("❌ Python not found. Please ensure Python 3 is installed.")
        return False

def main():
    """Main configuration and setup process"""
    print("🎯 SphereVista360 WordPress Theme Auto-Setup")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("📁 Found existing .env file")
        use_existing = input("Use existing configuration? (y/n): ").lower()
        if use_existing != 'y':
            # Get new credentials
            site_url, username, password = get_user_input()
            create_env_file(site_url, username, password)
    else:
        # Get credentials from user
        site_url, username, password = get_user_input()
        create_env_file(site_url, username, password)
    
    print("\n📋 What this setup will do:")
    print("✅ Create Homepage with professional content")
    print("✅ Create About, Services, and Contact pages")
    print("✅ Add 3 sample blog posts about finance/tech")
    print("✅ Set up professional content structure")
    print("📝 Provide instructions for manual menu setup")
    
    proceed = input("\nProceed with automated setup? (y/n): ").lower()
    
    if proceed == 'y':
        success = run_theme_setup()
        
        if success:
            print("\n🎉 Setup completed successfully!")
            print("\nNext steps:")
            print("1. Visit your website to see the new content")
            print("2. Go to WordPress Admin > Appearance > Menus to set up navigation")
            print("3. Upload your logo in Appearance > Customize")
            print("4. Test all theme features")
        else:
            print("\n❌ Setup encountered issues. Check the output above for details.")
    else:
        print("\n📄 Setup cancelled. You can run this again anytime.")
        print("Manual setup instructions are available in wordpress_setup_guide.md")

if __name__ == "__main__":
    main()