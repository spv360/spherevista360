#!/bin/bash
# WordPress Tools Setup Script
# Quick setup for production-ready blog publishing tools

echo "🔧 Setting up WordPress Tools..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r tools/production/requirements.txt

# Make scripts executable
echo "⚙️ Setting up executable permissions..."
chmod +x tools/production/*.py
chmod +x tools/utilities/*.py

echo "✅ Setup completed!"
echo ""
echo "📋 USAGE EXAMPLES:"
echo ""
echo "🚀 Complete publishing workflow:"
echo "   python3 tools/production/blog_workflow.py publish content_to_publish/Technology --category Technology"
echo ""
echo "🧪 Dry run (preview only):"
echo "   python3 tools/production/blog_workflow.py publish content_to_publish/Entertainment --dry-run"
echo ""
echo "🔍 Validate existing category:"
echo "   python3 tools/production/blog_workflow.py validate Entertainment"
echo ""
echo "🔧 Optimize existing post:"
echo "   python3 tools/production/blog_workflow.py optimize 1234"
echo ""
echo "📄 Publish single file:"
echo "   python3 tools/production/enhanced_content_publisher.py my-article.md --category Technology"
echo ""
echo "✅ Validate specific post:"
echo "   python3 tools/production/comprehensive_validator.py --post-id 1234"
echo ""
echo "📊 Content analysis:"
echo "   python3 tools/utilities/content_manager.py analyze"
echo ""
echo "📝 Create missing pages:"
echo "   python3 tools/utilities/create_missing_pages.py"
echo ""
echo "🎯 Ready to publish! Use the commands above to get started."