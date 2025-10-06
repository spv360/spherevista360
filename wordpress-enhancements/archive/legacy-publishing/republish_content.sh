#!/bin/bash

# SphereVista360 Content Republisher - Quick Start
# Republish week1_final content after cleanup

echo "🚀 SphereVista360 Content Republisher"
echo "===================================="
echo ""

# Check if in correct directory
if [ ! -d "wordpress-enhancements" ]; then
    echo "❌ Error: Please run from the spherevista360 project root"
    exit 1
fi

# Check for WordPress credentials
if [ -z "$WP_SITE" ] || [ -z "$WP_USER" ] || [ -z "$WP_APP_PASS" ]; then
    echo "⚙️  WordPress credentials needed..."
    echo ""
    echo "Please set your WordPress credentials:"
    echo "  export WP_SITE='https://spherevista360.com'"
    echo "  export WP_USER='your_username'"
    echo "  export WP_APP_PASS='your_app_password'"
    echo ""
    exit 1
fi

echo "🔍 Looking for week1_final content..."

# Common locations for week1_final content
CONTENT_PATHS=(
    "./spherevista360_week1_final"
    "../spherevista360_week1_final"
    "../../spherevista360_week1_final"
    "./week1_final"
    "../week1_final"
)

FOUND_PATH=""
for path in "${CONTENT_PATHS[@]}"; do
    if [ -d "$path" ]; then
        echo "✅ Found content at: $path"
        FOUND_PATH="$path"
        break
    fi
done

if [ -z "$FOUND_PATH" ]; then
    echo "❌ Could not find week1_final content directory"
    echo ""
    echo "💡 Please specify the path manually:"
    read -p "📁 Enter path to spherevista360_week1_final: " user_path
    if [ -d "$user_path" ]; then
        FOUND_PATH="$user_path"
        echo "✅ Using: $FOUND_PATH"
    else
        echo "❌ Directory not found: $user_path"
        exit 1
    fi
fi

echo ""
echo "📊 Content Analysis:"
echo "==================="

# Count content files by category
for category in "Finance" "Technology" "Politics" "Travel" "World" "Business"; do
    if [ -d "$FOUND_PATH/$category" ]; then
        count=$(find "$FOUND_PATH/$category" -name "*.md" | wc -l)
        if [ $count -gt 0 ]; then
            echo "  📁 $category: $count files"
        fi
    fi
done

echo ""
echo "🎯 Republishing Options:"
echo "======================="
echo "1. 📝 Create as DRAFTS (safe, review first)"
echo "2. 🚀 PUBLISH immediately (live on site)"
echo "3. 🎯 Specific category only"
echo "4. 💡 Help and documentation"
echo ""

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📝 Creating content as DRAFTS..."
        python wordpress-enhancements/scripts/content_republisher.py --content-path "$FOUND_PATH"
        ;;
    2)
        echo ""
        echo "⚠️  This will PUBLISH content immediately to your live site!"
        read -p "Are you sure? (type 'yes' to confirm): " confirm
        if [ "$confirm" = "yes" ]; then
            echo "🚀 Publishing content immediately..."
            python wordpress-enhancements/scripts/content_republisher.py --content-path "$FOUND_PATH" --publish
        else
            echo "❌ Publishing cancelled"
            exit 1
        fi
        ;;
    3)
        echo ""
        echo "Available categories:"
        for category in "Finance" "Technology" "Politics" "Travel" "World" "Business"; do
            if [ -d "$FOUND_PATH/$category" ]; then
                count=$(find "$FOUND_PATH/$category" -name "*.md" | wc -l)
                if [ $count -gt 0 ]; then
                    echo "  • $category ($count files)"
                fi
            fi
        done
        echo ""
        read -p "📁 Enter category name: " category
        
        echo "📝 Publishing $category category as drafts..."
        python wordpress-enhancements/scripts/content_republisher.py --content-path "$FOUND_PATH" --category "$category"
        ;;
    4)
        echo ""
        echo "📖 Content Republisher Documentation"
        echo "===================================="
        echo ""
        echo "🎯 Purpose:"
        echo "  Republish your high-quality week1_final content after cleanup"
        echo "  Includes enhanced SEO, categorization, and WordPress optimization"
        echo ""
        echo "📝 Draft Mode (Recommended):"
        echo "  • Creates posts as drafts for review"
        echo "  • Safe to test and modify before publishing"
        echo "  • Review in WordPress admin before going live"
        echo ""
        echo "🚀 Publish Mode:"
        echo "  • Posts go live immediately"
        echo "  • Use only when content is finalized"
        echo "  • Good for batch publishing reviewed content"
        echo ""
        echo "🎯 Category Mode:"
        echo "  • Publish specific category only"
        echo "  • Good for gradual content rollout"
        echo "  • Test with Finance category first"
        echo ""
        echo "✨ Features:"
        echo "  • SEO optimization with meta titles/descriptions"
        echo "  • Automatic category creation and mapping"
        echo "  • Image optimization with fallbacks"
        echo "  • Internal linking for better SEO"
        echo "  • WordPress-compatible HTML formatting"
        echo ""
        echo "🔗 Manual Usage:"
        echo "  python wordpress-enhancements/scripts/content_republisher.py --help"
        echo ""
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

# Check if the script completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Content republishing complete!"
    echo ""
    echo "🔗 Next Steps:"
    echo "  1. Visit WordPress admin: $WP_SITE/wp-admin/"
    echo "  2. Review posts: $WP_SITE/wp-admin/edit.php"
    echo "  3. Check categories: $WP_SITE/wp-admin/edit-tags.php?taxonomy=category"
    echo ""
    echo "💡 Tips:"
    echo "  • Review drafts before publishing"
    echo "  • Customize categories and tags as needed"
    echo "  • Update internal links between related posts"
    echo "  • Monitor SEO performance with Yoast"
else
    echo ""
    echo "❌ Content republishing failed"
    echo "💡 Check the error messages above and try again"
fi