#!/usr/bin/env python3
"""
Navigation Implementation Verification Tool
==========================================
Verify that the AdSense-optimized navigation was successfully implemented
and provide final optimization recommendations.
"""

import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from master_toolkit.core import WordPressClient
from master_toolkit.core.config import config
from master_toolkit.utils import print_success, print_error, print_warning, print_info


class NavigationVerifier:
    """Verify navigation implementation and provide final optimizations."""
    
    def __init__(self):
        """Initialize the verifier."""
        self.wp = None
        self.site_url = config.get('base_url')
        self.verification_results = {}
        
    def setup_client(self):
        """Setup WordPress client."""
        print_info("🔧 Setting up WordPress client...")
        
        try:
            self.wp = WordPressClient()
            self.wp.authenticate()
            print_success("✅ WordPress connected successfully")
            return True
        except Exception as e:
            print_error(f"❌ WordPress setup failed: {str(e)}")
            return False
    
    def verify_categories(self):
        """Verify category structure is optimized."""
        print_info("\n📂 Verifying category structure...")
        
        try:
            categories = self.wp.get_categories()
            
            # Check for high-value categories
            high_value_cats = []
            empty_cats = []
            content_cats = []
            
            for cat in categories:
                count = cat.get('count', 0)
                name = cat.get('name', '')
                
                if count > 0:
                    content_cats.append(cat)
                    
                    # Check if it's a high-value category
                    high_value_keywords = [
                        'technology', 'finance', 'business', 'travel', 'health',
                        'education', 'entertainment', 'investment', 'crypto', 'ai'
                    ]
                    
                    if any(keyword in name.lower() for keyword in high_value_keywords):
                        high_value_cats.append(cat)
                else:
                    empty_cats.append(cat)
            
            print_success(f"✅ Total categories: {len(categories)}")
            print_info(f"   Categories with content: {len(content_cats)}")
            print_info(f"   High-value categories: {len(high_value_cats)}")
            print_warning(f"   Empty categories remaining: {len(empty_cats)}")
            
            print_info(f"\n📈 High-Value Categories:")
            for cat in sorted(high_value_cats, key=lambda x: x.get('count', 0), reverse=True):
                print_info(f"   - {cat.get('name')}: {cat.get('count')} posts")
            
            self.verification_results['categories'] = {
                'total': len(categories),
                'with_content': len(content_cats),
                'high_value': len(high_value_cats),
                'empty': len(empty_cats),
                'optimization_score': min(100, (len(high_value_cats) * 15) + max(0, 100 - len(empty_cats) * 5))
            }
            
            return True
            
        except Exception as e:
            print_error(f"❌ Category verification failed: {str(e)}")
            return False
    
    def verify_pages(self):
        """Verify compliance pages exist."""
        print_info("\n📄 Verifying compliance pages...")
        
        try:
            pages = self.wp.get_pages(per_page=50)
            
            required_pages = ['privacy', 'terms', 'disclaimer', 'about', 'contact']
            found_pages = []
            
            for page in pages:
                title = page.get('title', {}).get('rendered', '').lower()
                for required in required_pages:
                    if required in title:
                        found_pages.append({
                            'type': required,
                            'title': page.get('title', {}).get('rendered'),
                            'url': page.get('link'),
                            'status': page.get('status')
                        })
                        break
            
            print_info(f"📋 Compliance Pages Status:")
            for page in found_pages:
                status_icon = "✅" if page['status'] == 'publish' else "⚠️"
                print_info(f"   {status_icon} {page['title']} - {page['url']}")
            
            missing_pages = [req for req in required_pages 
                           if not any(req in found['type'] for found in found_pages)]
            
            if missing_pages:
                print_warning(f"⚠️  Missing pages: {', '.join(missing_pages)}")
            
            self.verification_results['pages'] = {
                'total_pages': len(pages),
                'compliance_pages': len(found_pages),
                'missing_pages': missing_pages,
                'compliance_score': (len(found_pages) / len(required_pages)) * 100
            }
            
            return True
            
        except Exception as e:
            print_error(f"❌ Pages verification failed: {str(e)}")
            return False
    
    def test_frontend_navigation(self):
        """Test if navigation is working on the frontend."""
        print_info("\n🌐 Testing frontend navigation...")
        
        try:
            # Test homepage
            response = requests.get(self.site_url, timeout=10)
            homepage_status = response.status_code == 200
            
            if homepage_status:
                print_success(f"✅ Homepage accessible: {self.site_url}")
                
                # Check if navigation HTML is present
                content = response.text.lower()
                
                nav_indicators = [
                    'nav', 'menu', 'navigation', 'entertainment', 'technology', 'finance'
                ]
                
                nav_present = sum(1 for indicator in nav_indicators if indicator in content)
                
                print_info(f"   Navigation indicators found: {nav_present}/{len(nav_indicators)}")
                
            else:
                print_error(f"❌ Homepage not accessible: {response.status_code}")
            
            # Test category pages
            test_categories = ['entertainment', 'technology', 'finance']
            category_results = []
            
            for cat_slug in test_categories:
                cat_url = f"{self.site_url}/category/{cat_slug}/"
                try:
                    cat_response = requests.get(cat_url, timeout=10)
                    cat_status = cat_response.status_code == 200
                    category_results.append({
                        'category': cat_slug,
                        'url': cat_url,
                        'status': cat_status,
                        'status_code': cat_response.status_code
                    })
                    
                    status_icon = "✅" if cat_status else "❌"
                    print_info(f"   {status_icon} {cat_slug}: {cat_url}")
                    
                except Exception as e:
                    print_warning(f"   ⚠️  {cat_slug}: Could not test - {str(e)}")
                    category_results.append({
                        'category': cat_slug,
                        'url': cat_url,
                        'status': False,
                        'error': str(e)
                    })
            
            self.verification_results['frontend'] = {
                'homepage_accessible': homepage_status,
                'navigation_indicators': nav_present,
                'category_pages': category_results,
                'frontend_score': (nav_present / len(nav_indicators)) * 100
            }
            
            return True
            
        except Exception as e:
            print_error(f"❌ Frontend testing failed: {str(e)}")
            return False
    
    def check_adsense_readiness(self):
        """Check overall AdSense readiness."""
        print_info("\n💰 Checking AdSense readiness...")
        
        readiness_criteria = {
            'content_categories': self.verification_results.get('categories', {}).get('high_value', 0) >= 5,
            'compliance_pages': self.verification_results.get('pages', {}).get('compliance_pages', 0) >= 4,
            'clean_navigation': self.verification_results.get('categories', {}).get('empty', 10) <= 5,
            'frontend_working': self.verification_results.get('frontend', {}).get('homepage_accessible', False),
            'category_pages_working': len([r for r in self.verification_results.get('frontend', {}).get('category_pages', []) if r.get('status', False)]) >= 2
        }
        
        passed_criteria = sum(readiness_criteria.values())
        total_criteria = len(readiness_criteria)
        readiness_score = (passed_criteria / total_criteria) * 100
        
        print_info(f"📊 AdSense Readiness Checklist:")
        for criterion, passed in readiness_criteria.items():
            status_icon = "✅" if passed else "❌"
            criterion_name = criterion.replace('_', ' ').title()
            print_info(f"   {status_icon} {criterion_name}")
        
        print_info(f"\n🎯 Overall Readiness Score: {readiness_score:.1f}%")
        
        if readiness_score >= 80:
            print_success("🎉 EXCELLENT! Your site is AdSense-ready!")
        elif readiness_score >= 60:
            print_warning("👍 GOOD! Minor improvements needed for optimal AdSense performance")
        else:
            print_error("⚠️  NEEDS WORK! Several improvements required before AdSense application")
        
        self.verification_results['adsense_readiness'] = {
            'criteria': readiness_criteria,
            'score': readiness_score,
            'status': 'ready' if readiness_score >= 80 else 'needs_improvement'
        }
        
        return readiness_score >= 60
    
    def generate_final_recommendations(self):
        """Generate final optimization recommendations."""
        print_info("\n💡 Generating final recommendations...")
        
        recommendations = []
        
        # Category recommendations
        cat_data = self.verification_results.get('categories', {})
        if cat_data.get('empty', 0) > 5:
            recommendations.append({
                'priority': 'high',
                'category': 'cleanup',
                'title': 'Remove Empty Categories',
                'description': f"Remove {cat_data.get('empty')} empty categories to clean up navigation",
                'action': "Go to Posts > Categories and delete unused categories"
            })
        
        if cat_data.get('high_value', 0) < 6:
            recommendations.append({
                'priority': 'high',
                'category': 'content',
                'title': 'Add High-Value Categories',
                'description': "Create content for Education, Health, Investment categories",
                'action': "Write 2-3 posts for each high-value category"
            })
        
        # Content recommendations
        uncategorized_count = 0
        try:
            categories = self.wp.get_categories()
            for cat in categories:
                if cat.get('name') == 'Uncategorized':
                    uncategorized_count = cat.get('count', 0)
                    break
        except:
            pass
        
        if uncategorized_count > 5:
            recommendations.append({
                'priority': 'medium',
                'category': 'organization',
                'title': 'Categorize Uncategorized Posts',
                'description': f"Move {uncategorized_count} posts from 'Uncategorized' to proper categories",
                'action': "Edit posts and assign appropriate categories"
            })
        
        # Page recommendations
        page_data = self.verification_results.get('pages', {})
        if page_data.get('missing_pages'):
            recommendations.append({
                'priority': 'high',
                'category': 'compliance',
                'title': 'Create Missing Pages',
                'description': f"Create: {', '.join(page_data.get('missing_pages', []))}",
                'action': "Create these pages with proper content for AdSense compliance"
            })
        
        # Frontend recommendations
        frontend_data = self.verification_results.get('frontend', {})
        if not frontend_data.get('homepage_accessible', True):
            recommendations.append({
                'priority': 'critical',
                'category': 'technical',
                'title': 'Fix Homepage Access',
                'description': "Homepage is not accessible",
                'action': "Check server configuration and WordPress settings"
            })
        
        # AdSense specific recommendations
        recommendations.extend([
            {
                'priority': 'medium',
                'category': 'adsense',
                'title': 'Add ads.txt File',
                'description': "Create ads.txt file for AdSense verification",
                'action': "Upload ads.txt to website root directory"
            },
            {
                'priority': 'low',
                'category': 'optimization',
                'title': 'Optimize Page Speed',
                'description': "Improve Core Web Vitals for better ad performance",
                'action': "Use caching plugins and optimize images"
            },
            {
                'priority': 'low',
                'category': 'content',
                'title': 'Increase Content Length',
                'description': "Aim for 1000+ words per article for better ad placement",
                'action': "Expand existing articles with more detailed content"
            }
        ])
        
        return recommendations
    
    def create_action_plan(self, recommendations):
        """Create prioritized action plan."""
        print_info("\n📋 Creating action plan...")
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        action_plan = {
            'immediate_actions': [r for r in recommendations if r['priority'] in ['critical', 'high']],
            'short_term': [r for r in recommendations if r['priority'] == 'medium'],
            'long_term': [r for r in recommendations if r['priority'] == 'low']
        }
        
        print_info(f"🔴 IMMEDIATE ACTIONS ({len(action_plan['immediate_actions'])}):")
        for action in action_plan['immediate_actions']:
            print_info(f"   • {action['title']}: {action['description']}")
        
        print_info(f"\n🟡 SHORT-TERM ({len(action_plan['short_term'])}):")
        for action in action_plan['short_term']:
            print_info(f"   • {action['title']}: {action['description']}")
        
        print_info(f"\n🟢 LONG-TERM ({len(action_plan['long_term'])}):")
        for action in action_plan['long_term']:
            print_info(f"   • {action['title']}: {action['description']}")
        
        return action_plan
    
    def save_verification_report(self, recommendations, action_plan):
        """Save complete verification report."""
        print_info("\n💾 Saving verification report...")
        
        report = {
            'verification_date': datetime.now().isoformat(),
            'site_url': self.site_url,
            'verification_results': self.verification_results,
            'recommendations': recommendations,
            'action_plan': action_plan,
            'next_steps': [
                "Complete immediate actions within 24 hours",
                "Implement short-term improvements within 1 week", 
                "Work on long-term optimizations over next month",
                "Apply for Google AdSense once immediate actions are complete",
                "Monitor site performance and ad revenue"
            ],
            'adsense_application_ready': self.verification_results.get('adsense_readiness', {}).get('status') == 'ready'
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'navigation_verification_report_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print_success(f"✅ Verification report saved: {report_file}")
        return report_file


def main():
    """Main verification execution."""
    print_info("🔍 NAVIGATION IMPLEMENTATION VERIFICATION")
    print_info("AdSense Readiness Assessment")
    print_info("=" * 60)
    
    verifier = NavigationVerifier()
    
    # Setup
    if not verifier.setup_client():
        return False
    
    # Run verifications
    verifier.verify_categories()
    verifier.verify_pages()
    verifier.test_frontend_navigation()
    
    # Check AdSense readiness
    adsense_ready = verifier.check_adsense_readiness()
    
    # Generate recommendations
    recommendations = verifier.generate_final_recommendations()
    
    # Create action plan
    action_plan = verifier.create_action_plan(recommendations)
    
    # Save report
    report_file = verifier.save_verification_report(recommendations, action_plan)
    
    # Final summary
    print_info("\n" + "="*70)
    print_info("🎉 NAVIGATION VERIFICATION COMPLETE!")
    print_info("="*70)
    
    readiness_score = verifier.verification_results.get('adsense_readiness', {}).get('score', 0)
    
    if readiness_score >= 80:
        print_success("🏆 EXCELLENT! Your site is ready for Google AdSense!")
        print_info("💰 You can apply for AdSense immediately!")
    elif readiness_score >= 60:
        print_warning("👍 GOOD! Complete immediate actions first, then apply for AdSense")
        print_info(f"📊 Current score: {readiness_score:.1f}% - Target: 80%+")
    else:
        print_error("⚠️  NEEDS IMPROVEMENT! Complete all recommendations before AdSense application")
        print_info(f"📊 Current score: {readiness_score:.1f}% - Target: 80%+")
    
    print_info(f"\n📄 Complete analysis: {report_file}")
    print_info("\n🚀 Next: Complete the immediate actions and your site will be AdSense-ready!")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)