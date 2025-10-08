#!/usr/bin/env python3
"""
WordPress Comment Display Troubleshooter
Fixes issues where comments exist in admin but don't show on posts
"""

import os
import requests
import base64
import re

class CommentDisplayFixer:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
    
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def check_comment_visibility_issues(self):
        """Check common reasons why comments don't display"""
        print("🔍 COMMENT DISPLAY TROUBLESHOOTING")
        print("=" * 38)
        
        print("📋 COMMON REASONS COMMENTS DON'T SHOW:")
        print("1. 🎨 Theme doesn't include comment template")
        print("2. ⚙️  Comment display disabled in theme settings")
        print("3. 🚫 Comments closed on individual posts")
        print("4. 🔧 WordPress settings blocking comment display")
        print("5. 🏗️  Theme conflicts or missing functions")
        print("6. 📱 Mobile theme hiding comments")
        print()
    
    def check_posts_comment_status(self):
        """Check if posts actually allow comments to be displayed"""
        print("📝 CHECKING POST COMMENT SETTINGS")
        print("=" * 35)
        
        try:
            posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 100})
            
            if posts_response.status_code == 200:
                posts = posts_response.json()
                
                print(f"Checking {len(posts)} posts for comment settings...")
                print()
                
                for post in posts[:10]:  # Check first 10 posts
                    title = post['title']['rendered'][:50] + "..."
                    comment_status = post.get('comment_status', 'unknown')
                    
                    status_emoji = "✅" if comment_status == 'open' else "❌"
                    print(f"{status_emoji} {title}")
                    print(f"   Comment Status: {comment_status}")
                    print(f"   Post ID: {post['id']}")
                    print(f"   URL: {post['link']}")
                    print()
                    
        except Exception as e:
            print(f"❌ Error checking posts: {e}")
    
    def get_specific_comment_details(self):
        """Try to get comment details with different API approaches"""
        print("💬 ATTEMPTING TO RETRIEVE COMMENT DETAILS")
        print("=" * 43)
        
        # Try different comment API endpoints
        endpoints_to_try = [
            f"{self.api}/comments",
            f"{self.api}/comments?status=approved",
            f"{self.api}/comments?status=hold",
            f"{self.api}/comments?per_page=100"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                print(f"Trying: {endpoint}")
                response = requests.get(endpoint, headers=self.headers)
                
                if response.status_code == 200:
                    comments = response.json()
                    print(f"   ✅ Found {len(comments)} comments")
                    
                    if comments:
                        for comment in comments[:3]:  # Show first 3
                            print(f"      Comment ID: {comment['id']}")
                            print(f"      Status: {comment['status']}")
                            print(f"      Post ID: {comment['post']}")
                            print(f"      Author: {comment['author_name']}")
                            print(f"      Content: {comment['content']['rendered'][:100]}...")
                            print()
                    else:
                        print("   ℹ️  No comments returned")
                elif response.status_code == 403:
                    print("   ❌ Access forbidden - API permissions issue")
                else:
                    print(f"   ❌ Failed: Status {response.status_code}")
                print()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
    
    def check_theme_comment_support(self):
        """Check if theme supports comments properly"""
        print("🎨 THEME COMMENT SUPPORT CHECK")
        print("=" * 30)
        
        print("🔧 WORDPRESS ADMIN CHECKS NEEDED:")
        print("1. Appearance → Customize → look for comment settings")
        print("2. Comments → Settings → verify comment display options")
        print("3. Individual posts → Quick Edit → ensure 'Allow Comments' is checked")
        print()
        
        print("📱 FRONTEND CHECKS:")
        print("1. Visit a post that should have comments")
        print("2. Scroll to bottom of post content")
        print("3. Look for comment form or 'Comments are closed' message")
        print("4. Check page source for comment-related HTML")
        print()
    
    def provide_manual_verification_steps(self):
        """Provide steps to manually verify comment display"""
        print("✅ MANUAL VERIFICATION STEPS")
        print("=" * 30)
        
        print("🌐 FRONTEND TESTING:")
        print("1. Visit a specific post URL (e.g., one with approved comment)")
        print("2. Scroll to the bottom of the post")
        print("3. Look for:")
        print("   • Comment form (Name, Email, Message fields)")
        print("   • Existing comments section")
        print("   • 'Leave a Reply' or 'Add Comment' button")
        print("   • 'Comments are closed' message")
        print()
        
        print("🔍 BROWSER DEVELOPER TOOLS:")
        print("1. Right-click on page → 'Inspect Element'")
        print("2. Search for 'comment' in HTML")
        print("3. Look for elements like:")
        print("   • <div id='comments'>")
        print("   • <form class='comment-form'>")
        print("   • <ol class='commentlist'>")
        print()
        
        print("⚙️  WORDPRESS ADMIN VERIFICATION:")
        print("1. Go to WordPress Admin → Comments")
        print("2. Note the Post ID of approved comment")
        print("3. Go to Posts → All Posts")
        print("4. Find that specific post and visit it")
        print("5. Check if the approved comment appears")
    
    def suggest_fixes(self):
        """Suggest potential fixes for comment display issues"""
        print("🛠️  POTENTIAL FIXES")
        print("=" * 20)
        
        print("🎨 THEME-RELATED FIXES:")
        print("1. Switch to default WordPress theme temporarily")
        print("2. Check if comments appear with default theme")
        print("3. If yes, your theme has comment display issues")
        print()
        
        print("⚙️  SETTINGS FIXES:")
        print("1. WordPress Admin → Settings → Discussion")
        print("2. Ensure 'Allow people to submit comments' is checked")
        print("3. Check 'Comment must be manually approved' setting")
        print("4. Review comment blacklist and moderation settings")
        print()
        
        print("📝 POST-SPECIFIC FIXES:")
        print("1. Edit individual posts")
        print("2. In post editor, check 'Discussion' meta box")
        print("3. Ensure 'Allow comments' is checked")
        print("4. Update the post")
        print()
        
        print("🧹 CACHE-RELATED FIXES:")
        print("1. Clear all WordPress caches")
        print("2. Clear browser cache (Ctrl+Shift+R)")
        print("3. Disable caching plugins temporarily")
        print("4. Check if comments appear")
    
    def create_comment_test_script(self):
        """Create a script to test comment functionality"""
        print("🧪 COMMENT FUNCTIONALITY TEST")
        print("=" * 30)
        
        try:
            # Get the first post to test with
            posts_response = requests.get(f"{self.api}/posts", headers=self.headers, params={'per_page': 1})
            
            if posts_response.status_code == 200:
                posts = posts_response.json()
                if posts:
                    test_post = posts[0]
                    print(f"📌 TEST POST:")
                    print(f"   Title: {test_post['title']['rendered']}")
                    print(f"   URL: {test_post['link']}")
                    print(f"   Comment Status: {test_post.get('comment_status', 'unknown')}")
                    print()
                    
                    print("🔬 TEST INSTRUCTIONS:")
                    print(f"1. Visit: {test_post['link']}")
                    print("2. Scroll to bottom of page")
                    print("3. Look for comment form or existing comments")
                    print("4. Try to submit a test comment")
                    print("5. Check if it appears or goes to moderation")
            else:
                print("❌ Could not fetch test post")
                
        except Exception as e:
            print(f"❌ Error creating test: {e}")
    
    def run_complete_diagnosis(self):
        """Run complete comment display diagnosis"""
        print("🔧 WORDPRESS COMMENT DISPLAY DIAGNOSIS")
        print("=" * 42)
        
        self.check_comment_visibility_issues()
        print("\n" + "="*50)
        self.check_posts_comment_status()
        print("\n" + "="*50)
        self.get_specific_comment_details()
        print("\n" + "="*50)
        self.check_theme_comment_support()
        print("\n" + "="*50)
        self.provide_manual_verification_steps()
        print("\n" + "="*50)
        self.suggest_fixes()
        print("\n" + "="*50)
        self.create_comment_test_script()
        
        print(f"\n🎯 SUMMARY:")
        print("You have comments in WordPress admin but they're not showing on posts.")
        print("This is typically a theme or settings issue, not a content problem.")
        print("Follow the verification steps above to identify the specific cause.")

if __name__ == "__main__":
    fixer = CommentDisplayFixer()
    fixer.run_complete_diagnosis()