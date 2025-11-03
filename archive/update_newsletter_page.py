#!/usr/bin/env python3
"""
Update Newsletter page with comprehensive educational finance content
"""
import requests
import base64

# WordPress API details
WP_URL = "https://spherevista360.com"
WP_USER = "JK"
WP_APP_PASSWORD = "R8sj tOZG 8ORr ntSZ XlPt qTE9"

def find_newsletter_page():
    """Find the newsletter page by searching"""
    credentials = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }
    
    # Search for newsletter page
    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/pages",
        headers=headers,
        params={"search": "newsletter", "per_page": 20}
    )
    
    if response.status_code == 200:
        pages = response.json()
        for page in pages:
            if 'newsletter' in page['slug'].lower():
                return page['id']
    
    return None

def create_newsletter_page():
    """Create a new newsletter page"""
    credentials = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }
    
    # Read the newsletter content
    with open("newsletter_page_content.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Create the page
    page_data = {
        "title": "Newsletter",
        "content": content,
        "status": "publish",
        "slug": "newsletter"
    }
    
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages",
        headers=headers,
        json=page_data
    )
    
    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"❌ Error creating newsletter page: {response.status_code}")
        print(response.text)
        return None

def update_newsletter_page(page_id):
    """Update existing newsletter page"""
    # Read the newsletter content
    with open("newsletter_page_content.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Prepare the update data
    update_data = {
        "content": content,
        "status": "publish"
    }
    
    # Create authorization header
    credentials = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }
    
    # Update the page
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{page_id}",
        headers=headers,
        json=update_data
    )
    
    if response.status_code == 200:
        print(f"✅ Newsletter page updated successfully!")
        print(f"   View at: {WP_URL}/newsletter/")
        return True
    else:
        print(f"❌ Error updating newsletter page: {response.status_code}")
        print(response.text)
        return False

def main():
    print("🔍 Searching for newsletter page...")
    page_id = find_newsletter_page()
    
    if page_id:
        print(f"✅ Found newsletter page (ID: {page_id})")
        print("📝 Updating content...")
        update_newsletter_page(page_id)
    else:
        print("📄 Newsletter page not found. Creating new page...")
        page_id = create_newsletter_page()
        if page_id:
            print(f"✅ Newsletter page created successfully (ID: {page_id})")
            print(f"   View at: {WP_URL}/newsletter/")

if __name__ == "__main__":
    main()
