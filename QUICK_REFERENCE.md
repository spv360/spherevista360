# Quick Reference Guide

## 📌 Common Commands

### Update Existing Pages

```bash
# Update homepage (ID: 2412)
cd scripts/page_updater && python3 update_page.py 2412 ../../content/homepage.html

# Update newsletter page
cd scripts/page_updater && python3 update_page.py --slug newsletter ../../content/newsletter.html

# Update tools page
cd scripts/page_updater && python3 update_page.py --slug tools ../../content/tools_page_content.html
```

### List & Search Pages

```bash
# List all pages
cd scripts/maintenance && python3 list_wordpress_pages.py

# Search for specific page
cd scripts/maintenance && python3 list_wordpress_pages.py | grep -i "newsletter"
```

### Create New Page

```bash
# Create new page
cd scripts/page_updater && python3 update_page.py --create "Page Title" ../../content/file.html --slug page-slug
```

## 🔑 Important Page IDs

| Page | ID | Slug | URL |
|------|-----|------|-----|
| Homepage | 2412 | home | https://spherevista360.com/ |
| Newsletter | 1658 | newsletter | https://spherevista360.com/newsletter/ |
| Tools | TBD | tools | https://spherevista360.com/tools/ |

## 📁 File Locations

```
content/
├── homepage.html          # Main homepage
├── newsletter.html        # Newsletter page
├── stock_ticker.html      # Stock ticker widget
└── tools_page_content.html # Tools listing

scripts/
├── wordpress_core/
│   └── wordpress_utils.py     # Core WordPress API library
├── page_updater/
│   └── update_page.py         # Page updater tool
├── maintenance/
│   └── list_wordpress_pages.py # List pages
├── calculators/               # Calculator tools
├── duplicates/                # Cleanup tools
└── newsletter/                # Newsletter tools
```

## 🚀 Workflow

1. Edit HTML in `content/`
2. Run update script from `scripts/<tool>/`
3. Verify on live site
4. Commit changes

## 💡 Tips

- Always work from `/scripts` directory when running tools
- Use `--slug` when you don't know the page ID
- Keep content files in `/content` directory
- Check `/docs` for detailed documentation

## 🐛 Quick Fixes

**Can't find page?**
```bash
cd scripts/maintenance && python3 list_wordpress_pages.py
```

**Update not working?**
- Check file path is correct
- Verify you're in `/scripts/<tool>` directory
- Ensure HTML file exists in `/content`

**Need page ID?**
```bash
cd scripts/maintenance && python3 list_wordpress_pages.py | grep "Page Name"
```
