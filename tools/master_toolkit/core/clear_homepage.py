
import requests
import json
import base64

# WordPress API details - UPDATE THESE VALUES
WP_URL = "https://spherevista360.com"
WP_USER = "your_username"  # Replace with your WordPress username
WP_APP_PASSWORD = "your_app_password"  # Replace with your app password

# Homepage ID from previous check
homepage_id = 2412

# Read the new homepage HTML
with open("complete_homepage_fix.html", "r", encoding="utf-8") as f:
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
    print("The carousel is now your homepage title.")
else:
    print(f"❌ Error updating homepage: {response.status_code}")
    print(response.text)
