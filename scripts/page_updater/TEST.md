# Page Updater Tests

Quick smoke test to verify the `update_page.py` tool still works after moving files.

From repository root:

```bash
cd scripts/page_updater
python3 update_page.py --slug newsletter ../content/newsletter.html
```

Expect: `✅ Page updated successfully!` and printed view URL.
