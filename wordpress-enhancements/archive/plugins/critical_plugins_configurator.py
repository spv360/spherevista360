#!/usr/bin/env python3
"""
WordPress Critical Plugins Configuration Guide
Post-installation configuration for Wordfence Security and UpdraftPlus
"""

import os
import sys
import requests
import base64
import json
from datetime import datetime
from typing import Dict, List, Optional

class CriticalPluginsConfigurator:
    def __init__(self):
        self.wp_site = os.environ.get('WP_SITE', 'https://spherevista360.com')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_APP_PASS')
        
        if self.wp_user and self.wp_pass:
            credentials = f"{self.wp_user}:{self.wp_pass}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            self.headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
        
        self.configuration_steps = {}
    
    def create_wordfence_configuration_guide(self) -> Dict:
        """Create comprehensive Wordfence configuration guide"""
        print("🛡️ Creating Wordfence Security configuration guide...")
        
        wordfence_config = {
            "immediate_setup": [
                {
                    "step": 1,
                    "title": "Run Initial Security Scan",
                    "location": "Wordfence → Scan",
                    "action": "Click 'Start New Scan'",
                    "description": "Perform comprehensive malware and security scan",
                    "expected_time": "5-15 minutes"
                },
                {
                    "step": 2,
                    "title": "Enable Web Application Firewall (WAF)",
                    "location": "Wordfence → Firewall → All Firewall Options",
                    "action": "Set 'Web Application Firewall Status' to 'Enabled and Protecting'",
                    "description": "Activate real-time traffic filtering",
                    "important": "May require .htaccess modification"
                },
                {
                    "step": 3,
                    "title": "Configure Email Alerts",
                    "location": "Wordfence → All Options → Alert Options",
                    "action": "Enter admin email and enable critical alerts",
                    "description": "Get notified of security events",
                    "recommended_alerts": [
                        "Security scan issues found",
                        "Someone is locked out",
                        "New user created",
                        "User logged in with administrator access",
                        "File changes detected"
                    ]
                }
            ],
            "firewall_settings": {
                "protection_level": "Extended Protection",
                "learning_mode": "Disable after 1 week",
                "brute_force_protection": "Enable",
                "rate_limiting": "Enable",
                "block_fake_google_crawlers": "Enable",
                "hide_wp_version": "Enable"
            },
            "scan_settings": {
                "scan_frequency": "Daily at 2:00 AM",
                "scan_includes": [
                    "Core files",
                    "Plugin files", 
                    "Theme files",
                    "Posts and comments for URLs",
                    "Check file contents"
                ],
                "email_summary": "Daily if issues found"
            },
            "login_security": {
                "enable_2fa": "Highly recommended",
                "login_attempt_limit": "5 attempts",
                "lockout_duration": "20 minutes",
                "enforce_strong_passwords": "Enable",
                "immediately_lock_invalid_usernames": "Enable"
            },
            "advanced_settings": {
                "country_blocking": "Optional - block high-risk countries",
                "scheduled_scans": "Enable automatic scheduling",
                "whitelisted_ips": "Add your static IP if available",
                "security_headers": "Let Wordfence manage"
            }
        }
        
        print("  ✅ Initial security scan procedure")
        print("  ✅ Web Application Firewall setup")
        print("  ✅ Email alert configuration")
        print("  ✅ Login security hardening")
        print("  ✅ Advanced protection settings")
        
        return wordfence_config
    
    def create_updraftplus_configuration_guide(self) -> Dict:
        """Create comprehensive UpdraftPlus configuration guide"""
        print("💾 Creating UpdraftPlus backup configuration guide...")
        
        updraftplus_config = {
            "immediate_setup": [
                {
                    "step": 1,
                    "title": "Create Manual Backup",
                    "location": "UpdraftPlus → Backup/Restore",
                    "action": "Click 'Backup Now'",
                    "description": "Create initial baseline backup",
                    "options": "Include files and database"
                },
                {
                    "step": 2,
                    "title": "Configure Automatic Backups",
                    "location": "UpdraftPlus → Settings",
                    "action": "Set backup schedule",
                    "recommended_schedule": {
                        "files": "Weekly",
                        "database": "Daily",
                        "retain": "4 complete sets"
                    }
                },
                {
                    "step": 3,
                    "title": "Set Up Remote Storage",
                    "location": "UpdraftPlus → Settings → Remote Storage",
                    "action": "Configure cloud storage destination",
                    "recommended_options": [
                        "Google Drive (Free 15GB)",
                        "Dropbox (Free 2GB)",
                        "Amazon S3 (Pay per use)",
                        "Microsoft OneDrive"
                    ]
                }
            ],
            "backup_schedule": {
                "database_backups": {
                    "frequency": "Daily",
                    "time": "3:00 AM",
                    "retain": "30 backups"
                },
                "file_backups": {
                    "frequency": "Weekly", 
                    "time": "Sunday 4:00 AM",
                    "retain": "4 backups"
                },
                "exclusions": [
                    "Cache files",
                    "Temporary files",
                    "Log files",
                    "wp-content/uploads/backup*"
                ]
            },
            "cloud_storage_setup": {
                "google_drive": {
                    "steps": [
                        "Click 'Google Drive' in Remote Storage",
                        "Authenticate with Google account",
                        "Create 'WordPress-Backups' folder",
                        "Test connection"
                    ],
                    "benefits": "15GB free storage, reliable"
                },
                "dropbox": {
                    "steps": [
                        "Click 'Dropbox' in Remote Storage",
                        "Authenticate with Dropbox account", 
                        "Create backup folder",
                        "Test upload"
                    ],
                    "benefits": "Easy setup, good integration"
                }
            },
            "backup_testing": {
                "frequency": "Monthly",
                "process": [
                    "Download recent backup",
                    "Verify file integrity",
                    "Test database restore on staging",
                    "Document restoration process"
                ]
            },
            "email_notifications": {
                "enable": "Yes",
                "events": [
                    "Backup completion",
                    "Backup failures",
                    "Storage quota warnings"
                ],
                "email": "Your admin email address"
            }
        }
        
        print("  ✅ Manual backup creation")
        print("  ✅ Automated backup scheduling")
        print("  ✅ Cloud storage integration")
        print("  ✅ Backup testing procedures")
        print("  ✅ Email notification setup")
        
        return updraftplus_config
    
    def create_next_steps_guide(self) -> Dict:
        """Create guide for remaining plugin installations"""
        print("📋 Creating next steps for remaining plugins...")
        
        next_steps = {
            "priority_2_plugins": [
                {
                    "plugin": "Yoast SEO",
                    "search_term": "Yoast SEO",
                    "priority": "Essential",
                    "description": "Complete SEO solution with meta tags and sitemaps",
                    "configuration_time": "15-20 minutes",
                    "immediate_benefits": [
                        "XML sitemap generation",
                        "Meta title and description optimization",
                        "Content readability analysis"
                    ]
                },
                {
                    "plugin": "Smush",
                    "search_term": "Smush",
                    "priority": "Essential", 
                    "description": "Image compression and optimization",
                    "configuration_time": "5-10 minutes",
                    "immediate_benefits": [
                        "Automatic image compression",
                        "Bulk optimization of existing images",
                        "Improved page load speeds"
                    ]
                }
            ],
            "priority_3_plugins": [
                {
                    "plugin": "Contact Form 7",
                    "search_term": "Contact Form 7", 
                    "priority": "Important",
                    "description": "Professional contact forms",
                    "configuration_time": "10-15 minutes",
                    "immediate_benefits": [
                        "Professional contact page functionality",
                        "Spam protection",
                        "Email notifications"
                    ]
                },
                {
                    "plugin": "MonsterInsights",
                    "search_term": "MonsterInsights",
                    "priority": "Important",
                    "description": "Google Analytics integration",
                    "configuration_time": "10-15 minutes",
                    "immediate_benefits": [
                        "Visitor tracking and analytics",
                        "Traffic source analysis",
                        "Content performance metrics"
                    ]
                }
            ],
            "installation_workflow": {
                "step_1": "Complete Wordfence and UpdraftPlus configuration (current)",
                "step_2": "Install and configure Yoast SEO",
                "step_3": "Install and configure Smush",
                "step_4": "Install Contact Form 7 and create contact form",
                "step_5": "Install MonsterInsights and connect Google Analytics",
                "step_6": "Optional: Install performance and enhancement plugins"
            }
        }
        
        print("  ✅ Priority 2 plugins identified")
        print("  ✅ Priority 3 plugins identified") 
        print("  ✅ Installation workflow planned")
        
        return next_steps
    
    def create_security_checklist(self) -> Dict:
        """Create post-installation security checklist"""
        print("🔒 Creating security verification checklist...")
        
        security_checklist = {
            "wordfence_verification": [
                {
                    "task": "Initial Security Scan Completed",
                    "check": "Go to Wordfence → Scan and verify scan completed successfully",
                    "expected": "Green 'Clean' status or resolved issues",
                    "action_if_failed": "Review and fix any identified issues"
                },
                {
                    "task": "Firewall Status Active", 
                    "check": "Go to Wordfence → Firewall and verify status",
                    "expected": "'Extended Protection' enabled",
                    "action_if_failed": "Enable firewall and configure .htaccess"
                },
                {
                    "task": "Email Alerts Configured",
                    "check": "Go to Wordfence → All Options → Alert Options",
                    "expected": "Admin email set and critical alerts enabled",
                    "action_if_failed": "Configure email notifications"
                },
                {
                    "task": "Login Security Enabled",
                    "check": "Go to Wordfence → Login Security",
                    "expected": "Brute force protection active",
                    "action_if_failed": "Enable login attempt limiting"
                }
            ],
            "updraftplus_verification": [
                {
                    "task": "Manual Backup Created",
                    "check": "Go to UpdraftPlus → Existing Backups",
                    "expected": "Recent backup listed with files and database",
                    "action_if_failed": "Create manual backup immediately"
                },
                {
                    "task": "Automatic Backups Scheduled",
                    "check": "Go to UpdraftPlus → Settings",
                    "expected": "Database: Daily, Files: Weekly schedules set",
                    "action_if_failed": "Configure backup scheduling"
                },
                {
                    "task": "Remote Storage Connected",
                    "check": "Go to UpdraftPlus → Settings → Remote Storage",
                    "expected": "Cloud storage authenticated and tested",
                    "action_if_failed": "Set up Google Drive or Dropbox storage"
                },
                {
                    "task": "Email Notifications Active",
                    "check": "Go to UpdraftPlus → Settings → Email",
                    "expected": "Email address set for backup notifications",
                    "action_if_failed": "Configure email alerts"
                }
            ],
            "general_security": [
                {
                    "task": "WordPress Core Updated",
                    "check": "Go to Dashboard → Updates",
                    "expected": "WordPress is up to date",
                    "action_if_failed": "Update WordPress core immediately"
                },
                {
                    "task": "Plugin Updates Applied",
                    "check": "Go to Plugins → Installed Plugins",
                    "expected": "No available updates shown",
                    "action_if_failed": "Update all plugins"
                },
                {
                    "task": "Strong Admin Password",
                    "check": "Verify admin account password strength",
                    "expected": "12+ characters with mixed case, numbers, symbols",
                    "action_if_failed": "Update to stronger password"
                }
            ]
        }
        
        print("  ✅ Wordfence verification steps")
        print("  ✅ UpdraftPlus verification steps")
        print("  ✅ General security checks")
        
        return security_checklist
    
    def generate_configuration_report(self):
        """Generate comprehensive configuration report"""
        print("📊 WordPress Critical Plugins Configuration")
        print("=" * 45)
        print(f"🌐 Site: {self.wp_site}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Generate all configuration guides
        wordfence_config = self.create_wordfence_configuration_guide()
        updraftplus_config = self.create_updraftplus_configuration_guide()
        next_steps = self.create_next_steps_guide()
        security_checklist = self.create_security_checklist()
        
        # Compile complete configuration
        complete_config = {
            "status": "Plugins installed - Configuration required",
            "installed_plugins": [
                "Wordfence Security",
                "UpdraftPlus"
            ],
            "wordfence_configuration": wordfence_config,
            "updraftplus_configuration": updraftplus_config,
            "next_plugin_installations": next_steps,
            "security_verification": security_checklist,
            "estimated_configuration_time": "30-45 minutes",
            "priority_actions": [
                "Run Wordfence security scan",
                "Create UpdraftPlus backup",
                "Configure cloud storage",
                "Set up email notifications",
                "Install Yoast SEO next"
            ]
        }
        
        # Save configuration files
        with open('critical_plugins_configuration.json', 'w') as f:
            json.dump(complete_config, f, indent=2)
        print("💾 Configuration guide saved: critical_plugins_configuration.json")
        
        # Create quick setup guide
        quick_setup = self.create_quick_setup_guide(wordfence_config, updraftplus_config)
        with open('QUICK_SETUP_GUIDE.md', 'w') as f:
            f.write(quick_setup)
        print("💾 Quick setup guide saved: QUICK_SETUP_GUIDE.md")
        
        # Display immediate next steps
        print(f"\n🎯 Immediate Next Steps:")
        print("=" * 25)
        print("1. 🛡️ Configure Wordfence Security (15-20 minutes)")
        print("   • Go to: https://spherevista360.com/wp-admin/admin.php?page=Wordfence")
        print("   • Run initial security scan")
        print("   • Enable Web Application Firewall")
        print("   • Configure email alerts")
        print()
        print("2. 💾 Configure UpdraftPlus Backups (10-15 minutes)")
        print("   • Go to: https://spherevista360.com/wp-admin/admin.php?page=updraftplus")
        print("   • Create manual backup")
        print("   • Set up automatic scheduling")
        print("   • Connect cloud storage (Google Drive recommended)")
        print()
        print("3. 📋 Verify Installation Success")
        print("   • Use security_checklist from configuration file")
        print("   • Ensure all features are working properly")
        print()
        print("4. 🔄 Install Next Priority Plugins")
        print("   • Yoast SEO (Essential)")
        print("   • Smush (Essential)")
        
        return complete_config
    
    def create_quick_setup_guide(self, wordfence_config: Dict, updraftplus_config: Dict) -> str:
        """Create a concise quick setup guide"""
        guide = f"""# 🚀 Quick Setup Guide - Critical Plugins Configuration

## ✅ Status: Wordfence Security & UpdraftPlus Installed!

Congratulations! You've installed the two most critical WordPress plugins. Now let's configure them properly.

## 🛡️ Wordfence Security Setup (15-20 minutes)

### Step 1: Run Initial Security Scan
1. **Go to**: WordPress Admin → Wordfence → Scan
2. **Click**: "Start New Scan"
3. **Wait**: 5-15 minutes for completion
4. **Review**: Any issues found and follow recommendations

### Step 2: Enable Web Application Firewall
1. **Go to**: Wordfence → Firewall → All Firewall Options
2. **Set**: Web Application Firewall Status to "Enabled and Protecting"
3. **Choose**: "Extended Protection" (recommended)
4. **Save**: Changes and test website functionality

### Step 3: Configure Email Alerts
1. **Go to**: Wordfence → All Options → Alert Options
2. **Enter**: Your admin email address
3. **Enable**: These critical alerts:
   - Security scan issues found
   - Someone is locked out
   - New user created
   - User logged in with administrator access
   - File changes detected

### Step 4: Set Up Login Security
1. **Go to**: Wordfence → Login Security
2. **Enable**: Brute Force Protection
3. **Set**: Maximum login attempts to 5
4. **Set**: Lockout duration to 20 minutes
5. **Enable**: "Immediately lock out invalid usernames"

## 💾 UpdraftPlus Backup Setup (10-15 minutes)

### Step 1: Create Manual Backup
1. **Go to**: WordPress Admin → UpdraftPlus → Backup/Restore
2. **Click**: "Backup Now"
3. **Select**: Include files and database
4. **Wait**: For backup completion
5. **Verify**: Backup appears in "Existing Backups"

### Step 2: Configure Automatic Backups
1. **Go to**: UpdraftPlus → Settings
2. **Set Database Backup Schedule**:
   - Frequency: Daily
   - Time: 3:00 AM
   - Retain: 30 backups
3. **Set File Backup Schedule**:
   - Frequency: Weekly
   - Day: Sunday
   - Time: 4:00 AM  
   - Retain: 4 backups

### Step 3: Set Up Cloud Storage (Highly Recommended)
**Option A: Google Drive (Recommended)**
1. **Go to**: UpdraftPlus → Settings → Remote Storage
2. **Click**: Google Drive
3. **Click**: "Authenticate with Google"
4. **Follow**: Google authentication process
5. **Create**: "WordPress-Backups" folder
6. **Click**: "Test Connection"

**Option B: Dropbox**
1. **Click**: Dropbox in Remote Storage
2. **Authenticate**: with Dropbox account
3. **Test**: connection and folder access

### Step 4: Configure Email Notifications
1. **Go to**: UpdraftPlus → Settings → Email
2. **Enter**: Your admin email
3. **Enable**: Backup completion notifications
4. **Enable**: Backup failure alerts
5. **Save**: Settings

## ✅ Verification Checklist

### Wordfence Verification
- [ ] Security scan completed successfully
- [ ] Web Application Firewall showing "Extended Protection"
- [ ] Email alerts configured and tested
- [ ] Login security enabled with attempt limiting

### UpdraftPlus Verification  
- [ ] Manual backup created and visible
- [ ] Automatic backup scheduling configured
- [ ] Cloud storage connected and tested
- [ ] Email notifications enabled

## 🔄 Next Steps

### Immediate (Today)
1. **Complete** Wordfence and UpdraftPlus configuration above
2. **Test** that both plugins are working correctly
3. **Verify** email notifications are received

### Next Priority Plugins (This Week)
1. **Yoast SEO** - Search engine optimization
   - Search: "Yoast SEO" in Plugins → Add New
   - Essential for Google visibility

2. **Smush** - Image optimization  
   - Search: "Smush" in Plugins → Add New
   - Improves site speed significantly

### Plugin Installation Order
```
✅ Wordfence Security (DONE)
✅ UpdraftPlus (DONE)
🔄 Yoast SEO (NEXT)
🔄 Smush (NEXT)
⏳ Contact Form 7 (AFTER)
⏳ MonsterInsights (AFTER)
```

## 🆘 Troubleshooting

### Wordfence Issues
- **Scan stuck**: Wait longer or restart scan
- **Firewall conflicts**: Temporarily disable, test site, re-enable
- **Email not received**: Check spam folder, verify email address

### UpdraftPlus Issues
- **Backup failed**: Check disk space, increase PHP memory limit
- **Cloud storage error**: Re-authenticate and test connection
- **Large backup size**: Exclude uploads folder temporarily

## 📞 Quick Access Links

- **WordPress Admin**: {self.wp_site}/wp-admin/
- **Wordfence Dashboard**: {self.wp_site}/wp-admin/admin.php?page=Wordfence
- **UpdraftPlus Dashboard**: {self.wp_site}/wp-admin/admin.php?page=updraftplus
- **Plugin Installation**: {self.wp_site}/wp-admin/plugin-install.php

## 🎯 Success Metrics

After completing this setup, you'll have:
- ✅ **Real-time security protection** against malware and attacks
- ✅ **Automated daily backups** with cloud storage
- ✅ **Email alerts** for security events and backup status
- ✅ **Professional security baseline** for your WordPress site

**Estimated total setup time: 25-35 minutes**

---

*Quick Setup Guide for SphereVista360.com Critical Plugins*  
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return guide

def main():
    """Main execution function"""
    configurator = CriticalPluginsConfigurator()
    
    print("🎉 Critical Plugins Successfully Installed!")
    print("=" * 45)
    print("✅ Wordfence Security - Installed & Activated")
    print("✅ UpdraftPlus - Installed & Activated")
    print()
    
    # Generate comprehensive configuration guide
    config_data = configurator.generate_configuration_report()
    
    print(f"\n📁 Configuration Files Created:")
    print("📄 critical_plugins_configuration.json - Complete configuration data")
    print("📖 QUICK_SETUP_GUIDE.md - Step-by-step setup instructions")
    print()
    
    print("🚀 Ready for Configuration!")
    print("Next: Follow the QUICK_SETUP_GUIDE.md for immediate setup steps")
    
    return True

if __name__ == "__main__":
    main()