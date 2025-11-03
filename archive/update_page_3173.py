#!/usr/bin/env python3
import requests
import base64
import getpass
import sys

def get_auth_header(username, password, site_url):
    """Get authentication header for WordPress API"""
    # Try JWT first
    jwt_url = f"{site_url}/wp-json/jwt-auth/v1/token"
    jwt_data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(jwt_url, json=jwt_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                return f"Bearer {token}"
    except:
        pass

    # Fall back to basic auth
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return f"Basic {credentials}"

def read_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract body content
    start = content.find('<body>')
    end = content.find('</body>')
    
    if start != -1 and end != -1:
        return content[start+6:end].strip()
    return content

def update_page(page_id, content, username, password, site_url):
    auth_header = get_auth_header(username, password, site_url)
    
    session = requests.Session()
    session.headers.update({'Authorization': auth_header})
    
    # Test connection
    test_url = f"{site_url}/wp-json/wp/v2/users/me"
    test_response = session.get(test_url)
    
    if test_response.status_code == 200:
        user_data = test_response.json()
        print(f"✅ Connected to WordPress as: {user_data.get('name', 'Unknown')}")
    else:
        print(f"❌ API connection failed: {test_response.status_code}")
        return False
    
    # Update page
    url = f"{site_url}/wp-json/wp/v2/pages/{page_id}"
    
    data = {
        'content': content,
        'status': 'publish'
    }
    
    response = session.post(url, json=data)
    
    if response.status_code == 200:
        print(f'✅ Successfully updated page {page_id}')
        print(f'🔗 View at: https://spherevista360.com/retirement-planner-estimator/')
        return True
    else:
        print(f'❌ Failed to update page {page_id}')
        print(f'Status: {response.status_code}')
        print(f'Response: {response.text[:500]}')
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 update_page_3173.py <html_file>')
        sys.exit(1)
    
    html_file = sys.argv[1]
    username = 'Sphere Vista'
    password = getpass.getpass('Enter WordPress password: ')
    site_url = 'https://spherevista360.com'
    
    content = read_html_content(html_file)
    update_page(3173, content, username, password, site_url)
