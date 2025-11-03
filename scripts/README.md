# Scripts Directory - Tool Organization

All WordPress management tools organized by function.

## 📂 Directory Structure

```
scripts/
├── wordpress_core/     # Core WordPress API library
├── page_updater/       # Page creation and update tools
├── calculators/        # Financial calculator deployment
├── duplicates/         # Duplicate page cleanup
├── maintenance/        # Site maintenance and utilities
└── newsletter/         # Newsletter management (future)
```

## 🚀 Quick Start

### Update a Page
```bash
cd page_updater
python3 update_page.py 2412 ../../content/homepage.html
```

### List All Pages
```bash
cd maintenance
python3 list_pages_simple.py
```

### Deploy Calculators
```bash
cd calculators
python3 deploy_tax_calculators.py
```

### Find Duplicates
```bash
cd duplicates
python3 analyze_wordpress_duplicates.py
```

## 📚 Tool Documentation

Each folder contains:
- Tool scripts
- `README.md` with usage instructions
- Any tool-specific documentation

See individual folder READMEs for detailed usage.

## 🔧 Shared Library

All tools use `wordpress_core/wordpress_utils.py` for WordPress API operations.

Import example:
```python
import sys
sys.path.insert(0, '../wordpress_core')
from wordpress_utils import WordPressAPI
```

## 💡 Best Practices

1. Always run tools from their respective directories
2. Use relative paths (`../../content/`) for content files
3. Check tool README before first use
4. Test on non-production pages first

## 📞 Support

For issues or questions, check:
- Tool-specific README in each folder
- Main project README: `/README.md`
- Quick reference: `/QUICK_REFERENCE.md`
