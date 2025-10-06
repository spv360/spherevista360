#!/bin/bash

# SphereVista360 Content Publishing Script
# Uses wp_agent_bulk.py to republish week1_final content

echo "🚀 SphereVista360 Content Publisher - wp_agent_bulk.py"
echo "=================================================="
echo ""

# Check if in correct directory
if [ ! -f "scripts/wp_agent_bulk.py" ]; then
    echo "❌ Error: wp_agent_bulk.py not found"
    echo "   Please run from: /home/kddevops/projects/spherevista360"
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
    echo "⚙️  Setting up WordPress credentials..."
    echo ""
    
    # Get site URL
    if [ -z "$WP_SITE" ]; then
        read -p "🌐 WordPress Site URL [https://spherevista360.com]: " wp_site
        export WP_SITE=${wp_site:-https://spherevista360.com}
    fi
    
    # Get username
    if [ -z "$WP_USER" ]; then
        read -p "👤 WordPress Username: " wp_user
        export WP_USER="$wp_user"
    fi
    
    # Get application password
    if [ -z "$WP_APP_PASS" ]; then
        echo "🔑 WordPress Application Password:"
        echo "   (Go to Users > Profile > Application Passwords to create one)"
        read -s wp_pass
        export WP_APP_PASS="$wp_pass"
        echo ""
    fi
fi

echo ""
echo "📊 Configuration:"
echo "  Site: $WP_SITE"
echo "  User: $WP_USER"
echo "  Pass: [SET]"
echo ""

# Look for week1_final content
CONTENT_PATHS=(
    "./spherevista360_week1_final"
    "../spherevista360_week1_final"
    "../../spherevista360_week1_final"
)

FOUND_PATH=""
for path in "${CONTENT_PATHS[@]}"; do
    if [ -d "$path" ]; then
        FOUND_PATH="$path"
        echo "✅ Found content at: $FOUND_PATH"
        break
    fi
done

if [ -z "$FOUND_PATH" ]; then
    echo "❌ Could not find spherevista360_week1_final directory"
    echo ""
    read -p "📁 Enter path to week1_final content: " user_path
    if [ -d "$user_path" ]; then
        FOUND_PATH="$user_path"
    else
        echo "❌ Directory not found: $user_path"
        exit 1
    fi
fi

echo ""
echo "🎯 Publishing Options:"
echo "====================="
echo "1. 🧪 Test with Finance category only (recommended first step)"
echo "2. 📝 Create all content as DRAFTS (safe, review first)"
echo "3. 🚀 PUBLISH all content immediately"
echo "4. 🎯 Publish specific category"
echo "5. ⚡ Advanced options (images, UTM tracking)"
echo "6. 📖 Show all available commands"
echo ""

read -p "Choose option (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🧪 Testing with Finance category ONLY..."
        echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH/Finance --category Finance"
        echo ""
        if [ -d "$FOUND_PATH/Finance" ]; then
            python scripts/wp_agent_bulk.py "$FOUND_PATH/Finance" --category Finance
        else
            echo "❌ Finance directory not found at: $FOUND_PATH/Finance"
            echo "Available directories:"
            ls -la "$FOUND_PATH/"
        fi
        ;;
    2)
        echo ""
        echo "📝 Creating all content as drafts..."
        echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH"
        echo ""
        python scripts/wp_agent_bulk.py "$FOUND_PATH"
        ;;
    3)
        echo ""
        echo "⚠️  This will PUBLISH all content immediately!"
        read -p "Are you sure? (type 'yes' to confirm): " confirm
        if [ "$confirm" = "yes" ]; then
            echo ""
            echo "🚀 Publishing all content..."
            echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH --publish"
            echo ""
            python scripts/wp_agent_bulk.py "$FOUND_PATH" --publish
        else
            echo "❌ Publishing cancelled"
            exit 1
        fi
        ;;
    4)
        echo ""
        echo "Available categories:"
        for cat_dir in "$FOUND_PATH"/*; do
            if [ -d "$cat_dir" ]; then
                cat_name=$(basename "$cat_dir")
                file_count=$(find "$cat_dir" -name "*.md" -type f | wc -l)
                if [ $file_count -gt 0 ]; then
                    echo "  • $cat_name ($file_count files)"
                fi
            fi
        done
        echo ""
        read -p "📁 Enter category name: " category
        read -p "📝 Publish immediately? (y/N): " publish_now
        
        if [[ $publish_now == [yY] ]]; then
            echo ""
            echo "🚀 Publishing $category category..."
            echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH/$category --category $category --publish"
            echo ""
            python scripts/wp_agent_bulk.py "$FOUND_PATH/$category" --category "$category" --publish
        else
            echo ""
            echo "📝 Creating $category as drafts..."
            echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH/$category --category $category"
            echo ""
            python scripts/wp_agent_bulk.py "$FOUND_PATH/$category" --category "$category"
        fi
        ;;
    5)
        echo ""
        echo "⚡ Advanced Options:"
        echo "=================="
        echo "a) Publish with images at top + UTM tracking"
        echo "b) Publish without images (text only)"
        echo "c) Force all into specific category"
        echo ""
        read -p "Choose advanced option (a-c): " adv_choice
        
        case $adv_choice in
            a)
                echo ""
                echo "🖼️ Publishing with top images and UTM tracking..."
                echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH --publish --top-image --utm \"?utm_source=spherevista360&utm_medium=republish\""
                echo ""
                python scripts/wp_agent_bulk.py "$FOUND_PATH" --publish --top-image --utm "?utm_source=spherevista360&utm_medium=republish"
                ;;
            b)
                echo ""
                echo "📝 Publishing text-only (no images)..."
                echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH --publish --no-image"
                echo ""
                python scripts/wp_agent_bulk.py "$FOUND_PATH" --publish --no-image
                ;;
            c)
                read -p "📁 Enter category name for all posts: " force_cat
                echo ""
                echo "🎯 Forcing all content into '$force_cat' category..."
                echo "Command: python scripts/wp_agent_bulk.py $FOUND_PATH --publish --category \"$force_cat\""
                echo ""
                python scripts/wp_agent_bulk.py "$FOUND_PATH" --publish --category "$force_cat"
                ;;
            *)
                echo "❌ Invalid option"
                exit 1
                ;;
        esac
        ;;
    6)
        echo ""
        echo "📖 Available Commands Reference:"
        echo "==============================="
        echo ""
        echo "🔧 Setup:"
        echo "  source wpagent-venv/bin/activate"
        echo ""
        echo "🧪 Test Commands:"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH/Finance --category Finance"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH/Technology --category Technology"
        echo ""
        echo "📝 Draft Commands:"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH/Finance --category Finance"
        echo ""
        echo "🚀 Publish Commands:"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH --publish"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH/Finance --category Finance --publish"
        echo ""
        echo "⚡ Advanced Commands:"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH --publish --top-image"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH --publish --no-image"
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH --publish --utm \"?utm_source=spherevista360\""
        echo "  python scripts/wp_agent_bulk.py $FOUND_PATH --publish --category \"Featured\""
        echo ""
        echo "🔍 Help:"
        echo "  python scripts/wp_agent_bulk.py --help"
        echo ""
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

# Check if command completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Publishing complete!"
    echo ""
    echo "🔗 Next Steps:"
    echo "  1. Visit WordPress admin: $WP_SITE/wp-admin/"
    echo "  2. Review posts: $WP_SITE/wp-admin/edit.php"
    echo "  3. Check categories: $WP_SITE/wp-admin/edit-tags.php?taxonomy=category"
    echo ""
    echo "💡 Tips:"
    echo "  • Review drafts before publishing"
    echo "  • Check image loading and formatting"
    echo "  • Verify SEO titles and descriptions"
    echo "  • Test internal links between posts"
else
    echo ""
    echo "❌ Publishing failed"
    echo "💡 Check the error messages above"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  • Verify WordPress credentials"
    echo "  • Check application password is correct"
    echo "  • Ensure user has admin permissions"
    echo "  • Try with a single file first"
fi