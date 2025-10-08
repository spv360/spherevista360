#!/usr/bin/env python3
"""
WordPress Comment Management System
Comprehensive tool for managing WordPress comments
"""

import os
import requests
import base64
import re
from datetime import datetime

class WordPressCommentManager:
    def __init__(self):
        self.site = os.getenv("WP_SITE", "https://spherevista360.com")
        self.user = os.getenv("WP_USER", "JK")
        self.app_pass = os.getenv("WP_APP_PASS", "R8sj tOZG 8ORr ntSZ XlPt qTE9")
        self.api = f"{self.site.rstrip('/')}/wp-json/wp/v2"
        
        self.headers = self.auth_header()
    
    def auth_header(self):
        token = base64.b64encode(f"{self.user}:{self.app_pass}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    
    def get_all_comments(self, status='all'):
        """Get all comments with specified status"""
        try:
            params = {'per_page': 100}
            if status != 'all':
                params['status'] = status
                
            comments_response = requests.get(f"{self.api}/comments", headers=self.headers, params=params)
            
            if comments_response.status_code == 200:
                return comments_response.json()
            else:
                print(f"❌ Failed to fetch comments: {comments_response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error fetching comments: {e}")
            return []
    
    def get_post_title(self, post_id):
        """Get post title by ID"""
        try:
            post_response = requests.get(f"{self.api}/posts/{post_id}", headers=self.headers)
            if post_response.status_code == 200:
                return post_response.json()['title']['rendered']
        except:
            pass
        return f"Post ID: {post_id}"
    
    def approve_comment(self, comment_id):
        """Approve a comment"""
        try:
            response = requests.post(
                f"{self.api}/comments/{comment_id}",
                headers=self.headers,
                json={'status': 'approved'}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error approving comment {comment_id}: {e}")
            return False
    
    def spam_comment(self, comment_id):
        """Mark comment as spam"""
        try:
            response = requests.post(
                f"{self.api}/comments/{comment_id}",
                headers=self.headers,
                json={'status': 'spam'}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error marking comment {comment_id} as spam: {e}")
            return False
    
    def delete_comment(self, comment_id, force=True):
        """Delete a comment permanently"""
        try:
            params = {'force': force} if force else {}
            response = requests.delete(f"{self.api}/comments/{comment_id}", headers=self.headers, params=params)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error deleting comment {comment_id}: {e}")
            return False
    
    def is_spam_comment(self, comment):
        """Check if comment appears to be spam"""
        content = comment['content']['rendered'].lower()
        author_name = comment['author_name'].lower()
        author_email = comment['author_email'].lower()
        
        # Common spam indicators
        spam_keywords = [
            'casino', 'poker', 'viagra', 'cialis', 'loan', 'debt', 'weight loss',
            'make money', 'work from home', 'buy now', 'click here', 'free trial',
            'limited time', 'act now', 'guaranteed', 'risk free', 'no strings attached'
        ]
        
        # Check for spam patterns
        spam_indicators = 0
        
        # Excessive links
        if content.count('http') > 2:
            spam_indicators += 1
        
        # Spam keywords
        for keyword in spam_keywords:
            if keyword in content or keyword in author_name:
                spam_indicators += 1
        
        # Suspicious email patterns
        suspicious_domains = ['gmail.com', 'hotmail.com', 'yahoo.com']
        if any(domain in author_email for domain in suspicious_domains) and len(author_name) < 3:
            spam_indicators += 1
        
        # Generic/promotional content
        if any(phrase in content for phrase in ['great post', 'nice article', 'thanks for sharing']) and len(content) < 50:
            spam_indicators += 1
        
        return spam_indicators >= 2
    
    def analyze_comments(self):
        """Analyze all comments and provide recommendations"""
        print("📬 COMPREHENSIVE COMMENT ANALYSIS")
        print("=" * 40)
        
        # Get comments by status
        all_comments = self.get_all_comments('all')
        approved = self.get_all_comments('approved')
        pending = self.get_all_comments('hold')
        spam = self.get_all_comments('spam')
        
        print(f"📊 COMMENT STATISTICS:")
        print(f"   Total Comments: {len(all_comments)}")
        print(f"   ✅ Approved: {len(approved)}")
        print(f"   ⏳ Pending: {len(pending)}")
        print(f"   🚫 Spam: {len(spam)}")
        print()
        
        if not all_comments:
            print("✅ No comments found via API")
            print("💡 This could mean:")
            print("   • Comments are disabled on the site")
            print("   • Comments exist but API access is restricted")
            print("   • Comments are managed by a plugin")
            return
        
        # Analyze pending comments
        if pending:
            print(f"⏳ PENDING COMMENTS REQUIRING REVIEW ({len(pending)}):")
            for comment in pending:
                post_title = self.get_post_title(comment['post'])
                is_spam = self.is_spam_comment(comment)
                
                print(f"\n   Comment ID: {comment['id']}")
                print(f"   Post: {post_title}")
                print(f"   Author: {comment['author_name']} ({comment['author_email']})")
                print(f"   Content: {comment['content']['rendered'][:100]}...")
                print(f"   Spam Risk: {'🚫 HIGH' if is_spam else '✅ LOW'}")
        
        # Analyze approved comments
        if approved:
            print(f"\n✅ APPROVED COMMENTS ({len(approved)}):")
            recent_approved = approved[:5]  # Show 5 most recent
            for comment in recent_approved:
                post_title = self.get_post_title(comment['post'])
                print(f"   • {comment['author_name']} on '{post_title}'")
    
    def moderate_pending_comments(self):
        """Interactive moderation of pending comments"""
        pending = self.get_all_comments('hold')
        
        if not pending:
            print("✅ No pending comments to moderate")
            return
        
        print(f"🛡️  MODERATING {len(pending)} PENDING COMMENTS")
        print("=" * 45)
        
        for comment in pending:
            post_title = self.get_post_title(comment['post'])
            is_spam = self.is_spam_comment(comment)
            
            print(f"\nComment ID: {comment['id']}")
            print(f"Post: {post_title}")
            print(f"Author: {comment['author_name']} ({comment['author_email']})")
            print(f"Date: {comment['date']}")
            print(f"Content: {comment['content']['rendered']}")
            print(f"Spam Risk: {'🚫 HIGH' if is_spam else '✅ LOW'}")
            
            # Auto-moderate obvious spam
            if is_spam:
                print("🤖 AUTO-MODERATING: Marking as spam due to suspicious content")
                if self.spam_comment(comment['id']):
                    print("   ✅ Marked as spam")
                else:
                    print("   ❌ Failed to mark as spam")
            else:
                print("✅ LOOKS LEGITIMATE: Auto-approving")
                if self.approve_comment(comment['id']):
                    print("   ✅ Approved")
                else:
                    print("   ❌ Failed to approve")
            
            print("-" * 50)
    
    def cleanup_spam_comments(self):
        """Clean up spam comments"""
        spam_comments = self.get_all_comments('spam')
        
        if not spam_comments:
            print("✅ No spam comments to clean up")
            return
        
        print(f"🧹 CLEANING UP {len(spam_comments)} SPAM COMMENTS")
        print("=" * 45)
        
        deleted_count = 0
        for comment in spam_comments:
            if self.delete_comment(comment['id']):
                deleted_count += 1
                print(f"✅ Deleted spam comment {comment['id']}")
            else:
                print(f"❌ Failed to delete comment {comment['id']}")
        
        print(f"\n🎉 Cleanup complete: {deleted_count}/{len(spam_comments)} spam comments deleted")
    
    def setup_comment_guidelines(self):
        """Provide comment management guidelines"""
        print("\n📋 COMMENT MANAGEMENT GUIDELINES")
        print("=" * 35)
        print("✅ APPROVE COMMENTS THAT:")
        print("   • Add value to the discussion")
        print("   • Ask legitimate questions")
        print("   • Share relevant experiences")
        print("   • Are respectful and constructive")
        print()
        print("❌ REJECT/SPAM COMMENTS THAT:")
        print("   • Contain excessive links")
        print("   • Promote unrelated products/services")
        print("   • Use generic phrases like 'great post'")
        print("   • Come from suspicious email addresses")
        print("   • Contain offensive or inappropriate content")
        print()
        print("🛡️  BEST PRACTICES:")
        print("   • Review comments regularly (daily/weekly)")
        print("   • Respond to legitimate questions promptly")
        print("   • Use spam filters and moderation rules")
        print("   • Consider requiring registration for commenting")
        print("   • Monitor for link spam and promotional content")
    
    def run_complete_management(self):
        """Run complete comment management process"""
        print("🛡️  WORDPRESS COMMENT MANAGEMENT SYSTEM")
        print("=" * 45)
        
        self.analyze_comments()
        print("\n" + "="*50)
        self.moderate_pending_comments()
        print("\n" + "="*50)
        self.cleanup_spam_comments()
        self.setup_comment_guidelines()
        
        print(f"\n🎯 COMMENT MANAGEMENT COMPLETE")
        print(f"Site: {self.site}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    manager = WordPressCommentManager()
    manager.run_complete_management()