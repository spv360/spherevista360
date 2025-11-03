#!/usr/bin/env python3
import requests
import base64

# WordPress API details
WP_URL = "https://spherevista360.com"
WP_USER = "JK"
WP_APP_PASSWORD = "R8sj tOZG 8ORr ntSZ XlPt qTE9"

# Homepage ID
homepage_id = 2412

# Read the new homepage HTML
with open("updated_homepage_with_sidebar.html", "r", encoding="utf-8") as f:
    new_content = f.read()

# Prepare the update data
update_data = {
    "content": new_content,
    "status": "publish"
}

# Create authorization header
credentials = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}

# Update the homepage
response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages/{homepage_id}",
    headers=headers,
    json=update_data
)

if response.status_code == 200:
    print("✅ Homepage updated successfully with sticky sidebar!")
else:
    print(f"❌ Error updating homepage: {response.status_code}")
    print(response.text)