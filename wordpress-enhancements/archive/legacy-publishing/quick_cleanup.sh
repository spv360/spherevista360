#!/bin/bash

# WordPress Content Cleanup Helper
# Quick cleanup for unwanted published posts

echo "🧹 WordPress Content Cleanup Helper"
echo "==================================="
echo ""

# Check if in correct directory
if [ ! -f "scripts/wp_agent_bulk.py" ]; then
    echo "❌ Error: Please run from the spherevista360 project root"
    exit 1
fi

# Activate Python environment
echo "🔧 Activating Python environment..."
if [ -d "wpagent-venv" ]; then
    source wpagent-venv/bin/activate
    echo "✅ Python environment activated"
else
    echo "❌ Error: wpagent-venv directory not found"
    exit 1
fi

# Check WordPress credentials
if [ -z "$WP_SITE" ] || [ -z "$WP_USER" ] || [ -z "$WP_APP_PASS" ]; then
    echo ""
    echo "⚙️  WordPress credentials needed..."
    echo ""
    echo "Please set your WordPress credentials:"
    echo "  export WP_SITE='https://spherevista360.com'"
    echo "  export WP_USER='your_username'"
    echo "  export WP_APP_PASS='your_app_password'"
    echo ""
    exit 1
fi

echo "🌐 Site: $WP_SITE"
echo "👤 User: $WP_USER"
echo ""

echo "🔍 Cleanup Options:"
echo "=================="
echo "1. 🎯 Interactive cleanup tool (recommended)"
echo "2. 🗑️ Quick category cleanup"
echo "3. 🌐 Open WordPress admin in browser"
echo "4. 📊 Show recent posts only (no cleanup)"
echo "5. 💡 Manual cleanup instructions"
echo ""

read -p "Choose option (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Starting interactive cleanup tool..."
        echo ""
        python wordpress-enhancements/scripts/content_cleanup_tool.py
        ;;
    2)
        echo ""
        echo "🗑️ Quick Category Cleanup"
        echo "========================"
        echo ""
        echo "Common categories that might need cleanup:"
        echo "  • Technology"
        echo "  • Politics" 
        echo "  • Travel"
        echo "  • World"
        echo "  • Business"
        echo ""
        read -p "Enter category name to delete ALL posts from: " category
        
        if [ -n "$category" ]; then
            echo ""
            echo "⚠️  This will DELETE ALL posts from '$category' category!"
            read -p "Are you absolutely sure? (type 'DELETE' to confirm): " confirm
            
            if [ "$confirm" = "DELETE" ]; then
                echo ""
                echo "🗑️ Deleting all posts from '$category' category..."
                
                # Get category ID and delete posts
                python -c "
import requests, base64, os, sys
wp_site = os.environ.get('WP_SITE')
wp_user = os.environ.get('WP_USER')
wp_pass = os.environ.get('WP_APP_PASS')

credentials = f'{wp_user}:{wp_pass}'
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded_credentials}', 'Content-Type': 'application/json'}

# Get categories
cats_response = requests.get(f'{wp_site}/wp-json/wp/v2/categories', headers=headers, params={'per_page': 100})
if cats_response.status_code != 200:
    print('❌ Failed to fetch categories')
    sys.exit(1)

categories = cats_response.json()
category_id = None
for cat in categories:
    if cat['name'].lower() == '$category'.lower():
        category_id = cat['id']
        break

if not category_id:
    print(f'❌ Category \"$category\" not found')
    sys.exit(1)

# Get posts from category
posts_response = requests.get(f'{wp_site}/wp-json/wp/v2/posts', headers=headers, params={'categories': category_id, 'per_page': 100})
if posts_response.status_code != 200:
    print('❌ Failed to fetch posts')
    sys.exit(1)

posts = posts_response.json()
deleted_count = 0

for post in posts:
    delete_response = requests.delete(f'{wp_site}/wp-json/wp/v2/posts/{post[\"id\"]}', headers=headers)
    if delete_response.status_code == 200:
        print(f'✅ Deleted: {post[\"title\"][\"rendered\"]}')
        deleted_count += 1
    else:
        print(f'❌ Failed to delete: {post[\"title\"][\"rendered\"]}')

print(f'\\n✅ Cleanup complete: {deleted_count} posts deleted from \"$category\" category')
"
            else
                echo "❌ Cleanup cancelled"
            fi
        else
            echo "❌ No category specified"
        fi
        ;;
    3)
        echo ""
        echo "🌐 Opening WordPress admin..."
        echo ""
        echo "WordPress Admin URLs:"
        echo "  📝 All Posts: $WP_SITE/wp-admin/edit.php"
        echo "  📁 Categories: $WP_SITE/wp-admin/edit-tags.php?taxonomy=category"
        echo "  🗑️ Trash: $WP_SITE/wp-admin/edit.php?post_status=trash&post_type=post"
        echo ""
        echo "💡 Manual cleanup steps:"
        echo "  1. Go to Posts → All Posts"
        echo "  2. Filter by category (dropdown at top)"
        echo "  3. Select unwanted posts (checkboxes)"
        echo "  4. Choose 'Move to Trash' from Bulk Actions"
        echo "  5. Click Apply"
        echo ""
        ;;
    4)
        echo ""
        echo "📊 Showing recent posts..."
        echo ""
        python -c "
import requests, base64, os
from datetime import datetime

wp_site = os.environ.get('WP_SITE')
wp_user = os.environ.get('WP_USER')
wp_pass = os.environ.get('WP_APP_PASS')

credentials = f'{wp_user}:{wp_pass}'
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded_credentials}'}

# Get recent posts
response = requests.get(f'{wp_site}/wp-json/wp/v2/posts', headers=headers, params={'per_page': 20})
if response.status_code != 200:
    print('❌ Failed to fetch posts')
    exit(1)

posts = response.json()
today = datetime.now().date()

print(f'📊 Recent Posts (showing last 20):')
print('=' * 40)

for i, post in enumerate(posts, 1):
    pub_date = datetime.fromisoformat(post['date'].replace('Z', '+00:00')).date()
    status_icon = '🟢' if post['status'] == 'publish' else '📝'
    date_str = pub_date.strftime('%Y-%m-%d')
    is_today = '🆕' if pub_date == today else '   '
    
    print(f'{i:2d}. {status_icon} {is_today} {post[\"title\"][\"rendered\"]} ({date_str})')
"
        ;;
    5)
        echo ""
        echo "💡 Manual Cleanup Instructions"
        echo "=============================="
        echo ""
        echo "🌐 WordPress Admin Method:"
        echo "  1. Go to: $WP_SITE/wp-admin/edit.php"
        echo "  2. Look for posts published today"
        echo "  3. Use category filter to see specific categories"
        echo "  4. Select unwanted posts (checkboxes)"
        echo "  5. Bulk Actions → Move to Trash → Apply"
        echo ""
        echo "🎯 Targeted Cleanup:"
        echo "  • Keep only Finance category posts (if that's what you wanted)"
        echo "  • Delete Technology, Politics, Travel, World categories"
        echo "  • Check publication dates to identify recent bulk uploads"
        echo ""
        echo "🔄 After Cleanup:"
        echo "  • Re-run wp_agent_bulk.py with correct single category paths"
        echo "  • Example: python scripts/wp_agent_bulk.py ./spherevista360_week1_final/Finance --category Finance"
        echo ""
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Cleanup operation completed!"
    echo ""
    echo "🔗 Next Steps:"
    echo "  1. Verify cleanup in WordPress admin: $WP_SITE/wp-admin/edit.php"
    echo "  2. Re-publish content with correct single-category commands"
    echo "  3. Use: python scripts/wp_agent_bulk.py ./spherevista360_week1_final/Finance --category Finance"
    echo ""
fi