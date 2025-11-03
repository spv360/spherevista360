# Page Updater Tool

Contains `update_page.py` — generic CLI tool to create/update WordPress pages from HTML files.

Usage examples:

```bash
# Update by page ID
python3 update_page.py 2412 ../content/homepage.html

# Update by slug
python3 update_page.py --slug newsletter ../content/newsletter.html

# Create new page
python3 update_page.py --create "New Page" ../content/new.html --slug new-page
```
