#!/usr/bin/env python3
import requests
import base64
import getpass
from collections import defaultdict

def get_auth_header(username, password, site_url):
    """Get authentication header for WordPress API"""
    jwt_url = f"{site_url}/wp-json/jwt-auth/v1/token"
    jwt_data = {"username": username, "password": password}
    
    try:
        response = requests.post(jwt_url, json=jwt_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                return f"Bearer {token}"
    except:
        pass
    
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return f"Basic {credentials}"

def list_all_pages(username, password, site_url):
    auth_header = get_auth_header(username, password, site_url)
    session = requests.Session()
    session.headers.update({'Authorization': auth_header})
    
    # Test connection
    test_url = f"{site_url}/wp-json/wp/v2/users/me"
    test_response = session.get(test_url)
    
    if test_response.status_code == 200:
        user_data = test_response.json()
        print(f"✅ Connected as: {user_data.get('name', 'Unknown')}\n")
    else:
        print(f"❌ Authentication failed: {test_response.status_code}\n")
        return
    
    # Get all pages (100 per page, multiple requests if needed)
    all_pages = []
    page = 1
    per_page = 100
    
    while True:
        url = f"{site_url}/wp-json/wp/v2/pages?per_page={per_page}&page={page}&status=publish,draft"
        response = session.get(url)
        
        if response.status_code != 200:
            break
        
        pages = response.json()
        if not pages:
            break
        
        all_pages.extend(pages)
        page += 1
    
    print(f"📊 Found {len(all_pages)} total pages\n")
    print("=" * 100)
    
    # Group by title/slug to find duplicates
    by_title = defaultdict(list)
    by_slug = defaultdict(list)
    
    # List all calculator/tool pages
    calculator_keywords = [
        'calculator', 'planner', 'estimator', 'tax', 'investment',
        'retirement', 'income', 'capital', 'gains', 'withholding',
        'employment', 'lump', 'sum', 'federal', 'state'
    ]
    
    calculator_pages = []
    
    for page in all_pages:
        page_id = page.get('id')
        title = page.get('title', {}).get('rendered', 'Untitled')
        slug = page.get('slug', '')
        status = page.get('status', 'unknown')
        modified = page.get('modified', '')
        link = page.get('link', '')
        
        # Check if it's a calculator/tool page
        is_calculator = any(keyword in title.lower() or keyword in slug.lower() 
                          for keyword in calculator_keywords)
        
        if is_calculator:
            calculator_pages.append({
                'id': page_id,
                'title': title,
                'slug': slug,
                'status': status,
                'modified': modified,
                'link': link
            })
            
            by_title[title.lower()].append(page_id)
            by_slug[slug].append(page_id)
    
    # Sort by modification date (newest first)
    calculator_pages.sort(key=lambda x: x['modified'], reverse=True)
    
    print("\n🔧 CALCULATOR & TOOL PAGES:")
    print("=" * 100)
    
    for page in calculator_pages:
        print(f"\nID: {page['id']}")
        print(f"Title: {page['title']}")
        print(f"Slug: {page['slug']}")
        print(f"Status: {page['status']}")
        print(f"Modified: {page['modified']}")
        print(f"URL: {page['link']}")
        print("-" * 100)
    
    # Find duplicates
    print("\n\n⚠️  DUPLICATE PAGES (Same Title):")
    print("=" * 100)
    
    duplicates_found = False
    for title, page_ids in by_title.items():
        if len(page_ids) > 1:
            duplicates_found = True
            print(f"\n'{title.title()}' - {len(page_ids)} copies:")
            for pid in page_ids:
                page_info = next(p for p in calculator_pages if p['id'] == pid)
                print(f"  - ID {pid}: {page_info['status']} | Modified: {page_info['modified']}")
                print(f"    URL: {page_info['link']}")
    
    if not duplicates_found:
        print("No duplicate titles found!")
    
    print("\n\n⚠️  DUPLICATE SLUGS:")
    print("=" * 100)
    
    slug_duplicates = False
    for slug, page_ids in by_slug.items():
        if len(page_ids) > 1:
            slug_duplicates = True
            print(f"\nSlug '{slug}' - {len(page_ids)} copies:")
            for pid in page_ids:
                page_info = next(p for p in calculator_pages if p['id'] == pid)
                print(f"  - ID {pid}: {page_info['title']} | {page_info['status']}")
    
    if not slug_duplicates:
        print("No duplicate slugs found!")
    
    # Generate cleanup recommendations
    print("\n\n💡 CLEANUP RECOMMENDATIONS:")
    print("=" * 100)
    
    pages_to_delete = []
    pages_to_keep = []
    
    for title, page_ids in by_title.items():
        if len(page_ids) > 1:
            # Sort by modification date, keep the newest
            pages_data = [next(p for p in calculator_pages if p['id'] == pid) for pid in page_ids]
            pages_data.sort(key=lambda x: x['modified'], reverse=True)
            
            keep = pages_data[0]
            delete = pages_data[1:]
            
            pages_to_keep.append(keep['id'])
            
            print(f"\n'{title.title()}':")
            print(f"  ✅ KEEP: ID {keep['id']} (newest, modified {keep['modified']})")
            print(f"     URL: {keep['link']}")
            
            for page in delete:
                pages_to_delete.append(page['id'])
                print(f"  ❌ DELETE: ID {page['id']} (older, modified {page['modified']})")
                print(f"     URL: {page['link']}")
    
    # Save cleanup script
    if pages_to_delete:
        print(f"\n\n📝 Total pages to delete: {len(pages_to_delete)}")
        print(f"📝 Total pages to keep: {len(set(pages_to_keep))}")
        
        with open('pages_to_delete.txt', 'w') as f:
            f.write("# WordPress Pages to Delete\n")
            f.write(f"# Generated on: {page_modified}\n\n")
            for pid in pages_to_delete:
                page_info = next(p for p in calculator_pages if p['id'] == pid)
                f.write(f"{pid} | {page_info['title']} | {page_info['slug']}\n")
        
        print("\n✅ Saved deletion list to: pages_to_delete.txt")

if __name__ == '__main__':
    username = 'Sphere Vista'
    password = getpass.getpass('Enter WordPress password: ')
    site_url = 'https://spherevista360.com'
    
    list_all_pages(username, password, site_url)
