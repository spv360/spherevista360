# SphereVista360 - WordPress Content Management

## 📁 Project Structure

```
spherevista360/
├── content/          # Active HTML content files
│   ├── homepage.html
│   ├── newsletter.html
│   ├── stock_ticker.html
│   ├── tools_page_content.html
│   └── updated_tools_page.html
│
├── scripts/          # Reusable WordPress management tools
│   ├── wordpress_core/                 # Core WordPress API library
│   │   └── wordpress_utils.py          # WordPress REST API wrapper
│   ├── page_updater/                   # Generic page updater tool
│   │   ├── update_page.py              # CLI tool to update/create pages
│   │   ├── README.md                   # Usage documentation
│   │   └── TEST.md                     # Smoke tests
│   ├── calculators/                    # Calculator deployment tools
│   │   ├── deploy_tax_calculators.py   # Deploy calculator tools
│   │   ├── embed_calculator.py         # Embed calculators in pages
│   │   ├── update_calculator_page.py   # Update calculator pages
│   │   ├── validate_calculator.py      # Validate calculator deployment
│   │   └── README.md                   # Calculator tools docs
│   ├── duplicates/                     # Duplicate cleanup tools
│   │   ├── analyze_wordpress_duplicates.py # Find duplicate pages
│   │   ├── wp_api_trash_duplicates.py  # Clean up duplicate pages
│   │   └── README.md                   # Cleanup tools docs
│   ├── maintenance/                    # Site maintenance tools
│   │   ├── list_wordpress_pages.py     # List all WordPress pages
│   │   └── README.md                   # Maintenance tools docs
│   └── newsletter/                     # Newsletter tools (future)
│
├── archive/          # Deprecated/old files (not in use)
│   ├── homepage_simple_clean.html
│   ├── professional_homepage*.html
│   ├── stock_ticker_code.html
│   ├── update_homepage_sticky.py
│   └── ... (other deprecated files)
│
├── docs/             # Documentation and notes
│   ├── README.md
│   └── ... (text files and markdown docs)
│
└── tools/            # Calculator tools and other utilities
    └── calculators/
```

---

## 🚀 Quick Start Guide

- **Config Validation**: Verifies credentials before making changes

### 1. Update Homepage- **Dry Run Mode**: Test operations without publishing

```bash- **Backup Integration**: Creates backups before major changes

cd scripts

python update_page.py 2412 ../content/homepage.html

```

### 2. Update Newsletter Page
```bash
cd scripts
python update_page.py --slug newsletter ../content/newsletter.html
```

### 3. Create New Page
```bash
cd scripts
python update_page.py --create "Page Title" ../content/new_page.html --slug page-slug
```

---

## 🔧 Main Tools

### `wordpress_core/wordpress_utils.py` - Core WordPress API Library

A reusable Python module providing WordPress REST API functionality.

**Location:** `scripts/wordpress_core/wordpress_utils.py`

**Features:**
- ✅ Get page by ID or slug
- ✅ Search pages
- ✅ Update page content
- ✅ Create new pages
- ✅ Delete pages
- ✅ List all pages

**Usage Example:**
```python
import sys
sys.path.insert(0, 'scripts/wordpress_core')
from wordpress_utils import WordPressAPI

api = WordPressAPI()

# Get a page
page = api.get_page(2412)

# Update page content
content = "<h1>New Content</h1><p>Hello world</p>"
api.update_page(2412, content)

# Find page by slug
page = api.find_page_by_slug('newsletter')

# Create new page
page_id = api.create_page('New Page', content, slug='new-page')
```

---

### `page_updater/update_page.py` - Generic Page Updater Tool

Universal tool for updating or creating WordPress pages from HTML content files.

**Location:** `scripts/page_updater/update_page.py`

**Command Syntax:**
```bash
cd scripts/page_updater
python3 update_page.py <options> <arguments>
```

**Usage Examples:**

**Update by Page ID:**
```bash
python3 update_page.py 2412 ../../content/homepage.html
```

**Update by Slug:**
```bash
python3 update_page.py --slug newsletter ../../content/newsletter.html
```

**Create New Page:**
```bash
python3 update_page.py --create "New Page Title" ../../content/new_page.html --slug new-slug
```

**Update Page Title:**
```bash
python3 update_page.py 2412 ../../content/homepage.html --title "New Homepage Title"
```

**Options:**
- `--slug <slug>` - Find page by slug instead of ID
- `--create <title>` - Create new page with specified title
- `--title <title>` - Update page title along with content

---

### `maintenance/list_wordpress_pages.py` - Page Listing Tool

List all WordPress pages with their IDs, titles, and URLs.

**Location:** `scripts/maintenance/list_wordpress_pages.py`

**Usage:**
```bash
cd scripts/maintenance
python3 list_wordpress_pages.py
```

**Output:**
```
📄 WordPress Pages:
   ID: 2412 | Homepage | https://spherevista360.com/
   ID: 1658 | Newsletter | https://spherevista360.com/newsletter/
   ...
```

---

### `duplicates/` - Duplicate Management Tools

Identify and remove duplicate pages on your WordPress site.

**Location:** `scripts/duplicates/`

**Usage:**
```bash
cd scripts/duplicates

# Find duplicates
python3 analyze_wordpress_duplicates.py

# Remove duplicates
python3 wp_api_trash_duplicates.py
```

---

### `calculators/` - Calculator Deployment Tools

Deploy and manage financial calculator tools.

**Location:** `scripts/calculators/`

**Usage:**
```bash
cd scripts/calculators

# Deploy calculators
python3 deploy_tax_calculators.py

# Embed calculator
python3 embed_calculator.py

# Validate deployment
python3 validate_calculator.py
```

---

## 📝 Content Files

### Active Content Files (in `/content`)

| File | Purpose | Page ID | URL |
|------|---------|---------|-----|
| `homepage.html` | Main homepage content | 2412 | / |
| `newsletter.html` | Newsletter signup page | 1658 | /newsletter/ |
| `stock_ticker.html` | Stock ticker widget code | - | (Header injection) |
| `tools_page_content.html` | Tools listing page | - | /tools/ |

### Updating Content

1. **Edit the HTML file** in `/content` directory
2. **Run the update script**:
   ```bash
   cd scripts
   python update_page.py <page_id> ../content/<filename>.html
   ```
3. **Verify on live site**

---

## 🔐 Configuration

WordPress credentials are stored in `scripts/wordpress_utils.py`:

```python
WP_URL = "https://spherevista360.com"
WP_USER = "JK"
WP_APP_PASSWORD = "R8sj tOZG 8ORr ntSZ XlPt qTE9"
```

**Security Note:** For production, consider using environment variables or a config file.

---

## 🎯 Common Tasks

### Update Homepage
```bash
cd scripts
python update_page.py 2412 ../content/homepage.html
```

### Update Newsletter Page
```bash
cd scripts
python update_page.py --slug newsletter ../content/newsletter.html
```

### List All Pages
```bash
cd scripts
python list_wordpress_pages.py
```

### Find Page ID by Name
```bash
cd scripts
python list_wordpress_pages.py | grep "Newsletter"
```

### Create New Landing Page
```bash
cd scripts
# Create HTML file first
echo "<h1>New Landing Page</h1>" > ../content/landing.html
# Deploy to WordPress
python update_page.py --create "Landing Page" ../content/landing.html --slug landing
```

---

## 📦 Calculator Tools

Located in `/tools/calculators/` - separate tools for financial calculators.

**Deployment scripts in `/scripts`:**
- `deploy_tax_calculators.py` - Deploy calculator tools
- `embed_calculator.py` - Embed calculators in pages
- `update_calculator_page.py` - Update calculator pages
- `validate_calculator.py` - Validate calculator deployment

---

## 🗂️ Archive Directory

Contains deprecated and old files that are no longer in use but kept for reference:

- Old homepage versions
- Deprecated update scripts
- Test files
- Legacy content

**Do not use files from archive directory for active development.**

---

## 💡 Best Practices

1. **Always test locally** before deploying to production
2. **Keep content files** organized in `/content` directory
3. **Use the generic `update_page.py`** tool instead of creating new scripts
4. **Document page IDs** when creating new pages
5. **Archive old files** instead of deleting them
6. **Use meaningful commit messages** when updating content

---

## 🐛 Troubleshooting

### "Page not found" Error
- Verify page ID with `list_wordpress_pages.py`
- Check if page exists on WordPress admin panel

### "Authentication failed" Error
- Verify credentials in `wordpress_utils.py`
- Check WordPress app password is still valid

### "Content not updating" Error
- Clear WordPress cache
- Check file permissions
- Verify HTML file exists and is readable

### Script Import Errors
- Ensure you're running scripts from the `/scripts` directory
- Check Python path includes parent directory

---

## 📚 Additional Resources

- WordPress REST API: https://developer.wordpress.org/rest-api/
- Python Requests: https://requests.readthedocs.io/

---

## 🔄 Workflow Summary

1. **Edit content** → Modify HTML files in `/content`
2. **Update page** → Run `update_page.py` with appropriate arguments
3. **Verify** → Check live site
4. **Commit** → Save changes to git repository

---

## 📞 Support

For issues or questions about this project structure, refer to documentation in `/docs` directory.

---

**Last Updated:** November 3, 2025  
**Project:** SphereVista360 WordPress Content Management  
**Status:** Active Development
