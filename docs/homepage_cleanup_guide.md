# WordPress Homepage Cleanup Guide

## Method 1: Manual Cleanup (Recommended)

### Step 1: Access WordPress Admin
1. Go to your WordPress admin dashboard
2. Navigate to **Pages** → **All Pages**
3. Find and edit your homepage (usually titled "Home")

### Step 2: Clear Existing Blocks
1. In the Gutenberg editor, select all blocks (Ctrl+A / Cmd+A)
2. Click the **three dots menu** (⋮) → **Remove Block**
3. Confirm removal of all blocks

### Step 3: Add New Homepage Content
1. Click **+ Add Block** 
2. Search for and add a **Custom HTML** block
3. Copy the entire content from `complete_homepage_fix.html`
4. Paste it into the Custom HTML block
5. Click **Update** to save

## Method 2: Using the API Script

### Step 1: Update Credentials
Edit `clear_homepage.py` and replace:
```python
WP_USER = "your_username"  # Your WordPress username
WP_APP_PASSWORD = "your_app_password"  # Your app password
```

### Step 2: Generate App Password
1. In WordPress admin → **Users** → **Profile**
2. Scroll to **Application Passwords**
3. Create new password with name "Homepage Update"
4. Copy the generated password

### Step 3: Run the Script
```bash
python3 clear_homepage.py
```

## What Gets Replaced

**Before:** Multiple blocks (carousel, text, latest posts, etc.)
**After:** Single Custom HTML block with:
- Carousel as homepage title
- Latest articles section  
- Trending topics sidebar

## Troubleshooting

- If images don't load, check Unsplash URLs
- If shortcodes don't work, verify plugin installation
- If layout breaks, ensure Custom HTML block is the only block

## Final Result

Your homepage will now have:
1. **Site Logo/Header**
2. **Carousel as Title** (scrolling category cards)
3. **Latest Articles** section
4. **Trending Topics** sidebar
