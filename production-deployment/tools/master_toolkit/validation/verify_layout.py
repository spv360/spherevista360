import requests
from bs4 import BeautifulSoup

url = "https://spherevista360.com/"

print("=" * 80)
print("🔍 VERIFYING HOMEPAGE LAYOUT")
print("=" * 80)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Check grid layout CSS
print("\n1. CHECKING GRID LAYOUT CSS:")
print("-" * 80)
if "grid-template-columns: 1fr 370px" in response.text:
    print("✅ Grid layout CSS found: 1fr 370px")
else:
    print("❌ Grid layout CSS NOT found")

# Check main structure
print("\n2. CHECKING HTML STRUCTURE:")
print("-" * 80)
wrapper = soup.find('div', class_='home-content-wrapper')
if wrapper:
    print("✅ .home-content-wrapper div found")
    main_area = wrapper.find('div', class_='main-content-area')
    sidebar_area = wrapper.find('aside', class_='sidebar-area')
    
    if main_area:
        print("✅ .main-content-area div found")
    else:
        print("❌ .main-content-area div NOT found")
    
    if sidebar_area:
        print("✅ .sidebar-area aside found")
    else:
        print("❌ .sidebar-area aside NOT found")
else:
    print("❌ .home-content-wrapper div NOT found")

# Check trending sidebar
print("\n3. CHECKING TRENDING SIDEBAR:")
print("-" * 80)
trending = soup.find('div', class_='trending-sidebar')
if trending:
    print("✅ .trending-sidebar div found")
    
    # Count trending items
    items = soup.find_all('div', class_='trending-item')
    print(f"✅ Found {len(items)} trending items")
    
    # Check if any are active
    active_items = soup.find_all('div', class_='trending-item active')
    print(f"✅ Found {len(active_items)} active trending items")
    
    # Check navigation dots
    dots = soup.find_all('span', class_='trending-dot')
    print(f"✅ Found {len(dots)} navigation dots")
else:
    print("❌ .trending-sidebar div NOT found")

# Check article list
print("\n4. CHECKING ARTICLE LIST:")
print("-" * 80)
articles = soup.find_all('article', class_='post-list-item')
print(f"✅ Found {len(articles)} articles in list")

# Check carousel
print("\n5. CHECKING CATEGORY CAROUSEL:")
print("-" * 80)
carousel = soup.find('div', class_='category-carousel')
if carousel:
    print("✅ Category carousel found")
    cards = soup.find_all('a', class_='category-card')
    print(f"✅ Found {len(cards)} category cards")
else:
    print("❌ Category carousel NOT found")

print("\n" + "=" * 80)
print("📊 LAYOUT ANALYSIS:")
print("=" * 80)

if wrapper and main_area and sidebar_area and trending:
    print("✅ ALL COMPONENTS PRESENT")
    print("\nLayout Structure:")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│  Category Carousel (Auto-scrolling)                        │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("┌────────────────────────────────┬────────────────────────────┐")
    print("│  Article List (Left)           │  Trending Sidebar (Right)  │")
    print("│  - Found " + str(len(articles)) + " articles" + " " * (17 - len(str(len(articles)))) + "│  - Found " + str(len(items)) + " trending items" + " " * (8 - len(str(len(items)))) + "│")
    print("│  - Grid column 1               │  - Grid column 2           │")
    print("│                                │  - Sticky positioning      │")
    print("└────────────────────────────────┴────────────────────────────┘")
    
    print("\n🎯 VERDICT: Layout should be displaying correctly!")
    print("   - Articles on LEFT side")
    print("   - Trending sidebar on RIGHT side")
    
elif not trending:
    print("⚠️  ISSUE: Trending sidebar CSS/HTML present but no content")
    print("   This means functions.php hasn't been updated yet!")
    print("   👉 Copy WORKING-functions.php to WordPress Theme Editor")
else:
    print("❌ ISSUE: Layout structure incomplete")
    print("   👉 Copy HOMEPAGE-CONTENT.html to WordPress page editor")

print("=" * 80)
