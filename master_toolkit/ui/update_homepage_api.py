import requests

# WordPress credentials
wp_url = "https://spherevista360.com"
username = "JK"
app_password = "BT1I iKXv 6bYv EUuS P2vk K9hV"

# Homepage page ID
page_id = 2412

# Read the updated content from HOMEPAGE-CONTENT.html
with open('HOMEPAGE-CONTENT.html', 'r') as f:
    new_content = f.read()

print("=" * 80)
print("🔄 UPDATING HOMEPAGE VIA API")
print("=" * 80)

endpoint = f"{wp_url}/wp-json/wp/v2/pages/{page_id}"

response = requests.post(
    endpoint,
    auth=(username, app_password),
    json={
        'content': new_content
    }
)

if response.status_code == 200:
    print("\n✅ Homepage updated successfully!")
    print("\n📋 Changes applied:")
    print("  ✓ Page title 'Home' hidden")
    print("  ✓ Breadcrumbs hidden")
    print("  ✓ Category carousel now appears at the very top")
    print("  ✓ 'Latest Articles' section below carousel")
    print("  ✓ Article list on LEFT, Trending sidebar on RIGHT")
    print("\n🌐 View your homepage:")
    print(f"  {wp_url}/")
    print("\n🎯 Layout structure:")
    print("  1. Site Header (Logo, Menu)")
    print("  2. Category Carousel ← First visible content!")
    print("  3. Latest Articles heading")
    print("  4. Articles (left) + Trending (right)")
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.text)

print("=" * 80)
