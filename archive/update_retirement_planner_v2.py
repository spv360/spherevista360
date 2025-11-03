#!/usr/bin/env python3
import requests
import sys
from requests.auth import HTTPBasicAuth
from getpass import getpass

def read_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract body content
    start = content.find('<body>')
    end = content.find('</body>')
    
    if start != -1 and end != -1:
        return content[start+6:end].strip()
    return content

def update_page(page_id, content, password):
    url = f'https://spherevista360.com/wp-json/wp/v2/pages/{page_id}'
    
    data = {
        'content': content,
        'status': 'publish'
    }
    
    response = requests.put(
        url,
        json=data,
        auth=HTTPBasicAuth('Sphere Vista', password),
        headers={'Content-Type': 'application/json'}
    )
    
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
        print('Usage: python3 update_retirement_planner_v2.py <html_file>')
        sys.exit(1)
    
    html_file = sys.argv[1]
    password = getpass('Enter WordPress password: ')
    
    content = read_html_content(html_file)
    update_page(3173, content, password)
