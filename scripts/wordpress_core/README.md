# WordPress Core Library

Core WordPress REST API wrapper used by all tools.

## Files

- `wordpress_utils.py` - Main library with `WordPressAPI` class

## Features

- WordPress REST API authentication
- Page CRUD operations (Create, Read, Update, Delete)
- Search and list pages
- Pretty print utilities

## Usage in Other Tools

```python
import sys
import os

# Add wordpress_core to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
wordpress_core_path = os.path.join(os.path.dirname(script_dir), 'wordpress_core')
sys.path.insert(0, wordpress_core_path)

# Import the library
from wordpress_utils import WordPressAPI, print_success, print_error

# Use it
api = WordPressAPI()
page = api.get_page(2412)
api.update_page(2412, "<h1>New Content</h1>")
```

## Configuration

Credentials are stored in `wordpress_utils.py`:
- `WP_URL` - WordPress site URL
- `WP_USER` - WordPress username
- `WP_APP_PASSWORD` - Application password

## API Methods

### `WordPressAPI` Class

- `get_page(page_id)` - Get page by ID
- `search_pages(search_term)` - Search for pages
- `find_page_by_slug(slug)` - Find page by slug
- `update_page(page_id, content, title=None)` - Update page
- `create_page(title, content, slug=None)` - Create new page
- `delete_page(page_id, force=False)` - Delete page
- `list_pages(per_page=100)` - List all pages

### Utility Functions

- `read_content_file(filepath)` - Read HTML content from file
- `print_success(message)` - Print success message
- `print_error(message)` - Print error message
- `print_info(message)` - Print info message
- `print_warning(message)` - Print warning message

## Testing

Test the library:
```bash
cd wordpress_core
python3 wordpress_utils.py
```

This will test connection and list first 5 pages.
