#!/usr/bin/env python3
"""
Final SEO Compliance Check
Comprehensive verification that all SEO title and meta issues are resolved
"""

import requests
from bs4 import BeautifulSoup

# WordPress configuration
WP_BASE_URL = "https://spherevista360.com/wp-json/wp/v2"

def check_post_seo_compliance(post_id):
    """Check all SEO elements for a post"""
    try:
        # Get API data
        api_response = requests.get(f"{WP_BASE_URL}/posts/{post_id}")
        if api_response.status_code != 200:
            return {'error': f'Could not fetch post {post_id}'}
        
        api_data = api_response.json()
        page_url = api_data.get('link', '')
        
        # Get page content
        page_response = requests.get(page_url)
        if page_response.status_code != 200:
            return {'error': f'Could not fetch page content for post {post_id}'}
        
        soup = BeautifulSoup(page_response.text, 'html.parser')
        
        # Check all title elements
        wp_title = api_data.get('title', {}).get('rendered', '')
        
        page_title_tag = soup.find('title')
        page_title = page_title_tag.get_text().strip() if page_title_tag else ''
        
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag.get('content', '').strip() if meta_desc_tag else ''
        
        og_title_tag = soup.find('meta', attrs={'property': 'og:title'})
        og_title = og_title_tag.get('content', '').strip() if og_title_tag else ''
        
        twitter_title_tag = soup.find('meta', attrs={'name': 'twitter:title'})
        twitter_title = twitter_title_tag.get('content', '').strip() if twitter_title_tag else ''
        
        # Check compliance
        issues = []
        
        # Title checks (60 character limit)
        if len(wp_title) > 60:
            issues.append(f'WordPress title too long: {len(wp_title)} chars')
        if len(page_title) > 60:
            issues.append(f'Page title too long: {len(page_title)} chars')
        if len(og_title) > 60:
            issues.append(f'OG title too long: {len(og_title)} chars')
        if len(twitter_title) > 60:
            issues.append(f'Twitter title too long: {len(twitter_title)} chars')
        
        # Meta description check (120 character limit)
        if len(meta_desc) > 120:
            issues.append(f'Meta description too long: {len(meta_desc)} chars')
        
        return {
            'post_id': post_id,
            'wp_title': wp_title,
            'wp_title_length': len(wp_title),
            'page_title': page_title,
            'page_title_length': len(page_title),
            'meta_desc': meta_desc,
            'meta_desc_length': len(meta_desc),
            'og_title': og_title,
            'og_title_length': len(og_title),
            'twitter_title': twitter_title,
            'twitter_title_length': len(twitter_title),
            'issues': issues,
            'compliant': len(issues) == 0
        }
        
    except Exception as e:
        return {'error': f'Error checking post {post_id}: {str(e)}'}

def main():
    """Check all recent posts for SEO compliance"""
    print("Final SEO Compliance Check")
    print("=" * 60)
    print("Verifying all titles ≤60 chars and meta descriptions ≤120 chars")
    print()
    
    post_ids = [1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838]
    
    all_compliant = True
    total_issues = 0
    
    for post_id in post_ids:
        result = check_post_seo_compliance(post_id)
        
        if 'error' in result:
            print(f"Post {post_id}: ❌ {result['error']}")
            all_compliant = False
            continue
        
        if result['compliant']:
            print(f"Post {post_id}: ✅ FULLY COMPLIANT")
            print(f"  WordPress Title: {result['wp_title_length']}/60 chars")
            print(f"  Page Title: {result['page_title_length']}/60 chars")
            print(f"  Meta Description: {result['meta_desc_length']}/120 chars")
            print(f"  OG Title: {result['og_title_length']}/60 chars")
            print(f"  Twitter Title: {result['twitter_title_length']}/60 chars")
        else:
            print(f"Post {post_id}: ❌ ISSUES FOUND")
            for issue in result['issues']:
                print(f"    - {issue}")
            all_compliant = False
            total_issues += len(result['issues'])
        
        print()
    
    # Final summary
    print("=" * 60)
    print("FINAL SEO COMPLIANCE REPORT")
    print("=" * 60)
    
    if all_compliant:
        print("🎉 ALL POSTS ARE FULLY SEO COMPLIANT!")
        print()
        print("✅ All titles ≤60 characters")
        print("✅ All meta descriptions ≤120 characters")
        print("✅ All Open Graph titles ≤60 characters")
        print("✅ All Twitter titles ≤60 characters")
        print()
        print("The 'Search engine title exceeds 60 characters' warnings should now be resolved.")
        print()
        print("Recommended next steps:")
        print("1. Clear your SEO plugin cache")
        print("2. Run a fresh SEO audit")
        print("3. Check your SEO dashboard for remaining warnings")
        
    else:
        print(f"⚠️ Found {total_issues} remaining SEO issues")
        print("Please review the issues above and address them manually.")
    
    print(f"\nTotal posts checked: {len(post_ids)}")
    print(f"Compliant posts: {sum(1 for pid in post_ids if check_post_seo_compliance(pid).get('compliant', False))}")

if __name__ == "__main__":
    main()