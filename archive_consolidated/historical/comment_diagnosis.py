#!/usr/bin/env python3
"""
WordPress Comment Settings and Management Guide
Handles comments that might not be visible via API
"""

import os
import requests
import base64

class CommentSettingsManager:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
    
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def check_comment_settings(self):
        """Check WordPress comment settings"""
        print("🔧 WORDPRESS COMMENT SETTINGS CHECK")
        print("=" * 40)
        
        try:
            # Check site settings
            settings_response = requests.get(f"{self.api}/settings", headers=self.headers)
            
            if settings_response.status_code == 200:
                settings = settings_response.json()
                
                # Check comment-related settings
                comment_status = settings.get('default_comment_status', 'unknown')
                ping_status = settings.get('default_ping_status', 'unknown')
                
                print(f"📊 CURRENT SETTINGS:")
                print(f"   Default Comment Status: {comment_status}")
                print(f"   Default Ping Status: {ping_status}")
                
                if comment_status == 'closed':
                    print("   ⚠️  Comments are DISABLED by default")
                elif comment_status == 'open':
                    print("   ✅ Comments are ENABLED by default")
                else:
                    print(f"   ❓ Unknown comment status: {comment_status}")
            else:
                print(f"❌ Could not fetch settings: {settings_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking settings: {e}")
    
    def check_individual_posts_comments(self):
        """Check comment status on individual posts"""
        print(f"\n📝 INDIVIDUAL POST COMMENT STATUS")
        print("=" * 35)
        
        try:
            # Get all posts
            posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
            
            if posts_response.status_code == 200:
                posts = posts_response.json()
                
                print(f"Checking {len(posts)} posts...")
                
                comment_enabled_posts = []
                comment_disabled_posts = []
                
                for post in posts:
                    title = post['title']['rendered']
                    comment_status = post.get('comment_status', 'unknown')
                    
                    if comment_status == 'open':
                        comment_enabled_posts.append(title)
                    elif comment_status == 'closed':
                        comment_disabled_posts.append(title)
                
                print(f"\n✅ COMMENTS ENABLED ({len(comment_enabled_posts)} posts):")
                for title in comment_enabled_posts[:10]:  # Show first 10
                    print(f"   • {title}")
                if len(comment_enabled_posts) > 10:
                    print(f"   ... and {len(comment_enabled_posts) - 10} more")
                
                print(f"\n❌ COMMENTS DISABLED ({len(comment_disabled_posts)} posts):")
                for title in comment_disabled_posts[:5]:  # Show first 5
                    print(f"   • {title}")
                if len(comment_disabled_posts) > 5:
                    print(f"   ... and {len(comment_disabled_posts) - 5} more")
                    
            else:
                print(f"❌ Could not fetch posts: {posts_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking posts: {e}")
    
    def enable_comments_on_all_posts(self):
        """Enable comments on all posts"""
        print(f"\n🔓 ENABLING COMMENTS ON ALL POSTS")
        print("=" * 35)
        
        try:
            posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
            
            if posts_response.status_code == 200:
                posts = posts_response.json()
                updated_count = 0
                
                for post in posts:
                    if post.get('comment_status') != 'open':
                        # Enable comments on this post
                        update_response = requests.post(
                            f"{self.api}/posts/{post['id']}",
                            headers=self.headers,
                            json={'comment_status': 'open'}
                        )
                        
                        if update_response.status_code == 200:
                            updated_count += 1
                            print(f"   ✅ Enabled comments on: {post['title']['rendered']}")
                        else:
                            print(f"   ❌ Failed to enable comments on: {post['title']['rendered']}")
                
                print(f"\n🎉 Comments enabled on {updated_count}/{len(posts)} posts")
                
        except Exception as e:
            print(f"❌ Error enabling comments: {e}")
    
    def disable_comments_on_all_posts(self):
        """Disable comments on all posts"""
        print(f"\n🔒 DISABLING COMMENTS ON ALL POSTS")
        print("=" * 35)
        
        try:
            posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
            
            if posts_response.status_code == 200:
                posts = posts_response.json()
                updated_count = 0
                
                for post in posts:
                    if post.get('comment_status') != 'closed':
                        # Disable comments on this post
                        update_response = requests.post(
                            f"{self.api}/posts/{post['id']}",
                            headers=self.headers,
                            json={'comment_status': 'closed'}
                        )
                        
                        if update_response.status_code == 200:
                            updated_count += 1
                            print(f"   ✅ Disabled comments on: {post['title']['rendered']}")
                        else:
                            print(f"   ❌ Failed to disable comments on: {post['title']['rendered']}")
                
                print(f"\n🎉 Comments disabled on {updated_count}/{len(posts)} posts")
                
        except Exception as e:
            print(f"❌ Error disabling comments: {e}")
    
    def provide_comment_management_options(self):
        """Provide comprehensive comment management guidance"""
        print(f"\n🎯 COMMENT MANAGEMENT OPTIONS")
        print("=" * 32)
        print("📍 Where to manage comments:")
        print("   1. WordPress Admin → Comments")
        print("   2. WordPress Admin → Settings → Discussion")
        print("   3. Individual posts → Quick Edit → Allow Comments")
        print()
        print("🛡️  RECOMMENDED COMMENT POLICY:")
        print("   • Enable comments for engagement")
        print("   • Use moderation (require approval)")
        print("   • Install anti-spam plugins (Akismet)")
        print("   • Set up email notifications for new comments")
        print("   • Regular monitoring and response")
        print()
        print("⚙️  WORDPRESS ADMIN ACTIONS:")
        print("   • Go to WordPress Admin Dashboard")
        print("   • Comments → View all comments")
        print("   • Bulk actions: Approve/Spam/Trash")
        print("   • Settings → Discussion → Comment settings")
        print()
        print("🤖 AUTOMATED SOLUTIONS:")
        print("   • Install Akismet for spam protection")
        print("   • Use comment moderation rules")
        print("   • Set up keyword filtering")
        print("   • Enable CAPTCHA for comment forms")
    
    def run_comment_diagnosis(self):
        """Run complete comment system diagnosis"""
        print("🔍 WORDPRESS COMMENT SYSTEM DIAGNOSIS")
        print("=" * 42)
        
        self.check_comment_settings()
        self.check_individual_posts_comments()
        self.provide_comment_management_options()
        
        print(f"\n💡 NEXT STEPS:")
        print("   1. Check WordPress Admin → Comments for any comments")
        print("   2. Review Settings → Discussion for comment settings")
        print("   3. Consider enabling/disabling comments based on your needs")
        print("   4. Install comment moderation tools if needed")

if __name__ == "__main__":
    manager = CommentSettingsManager()
    manager.run_comment_diagnosis()