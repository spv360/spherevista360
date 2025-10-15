# How to Fix Homepage Meta Description (Rank Math SEO)

## Current Problem:
Your homepage meta description contains CSS code instead of a proper description:
```html
<meta name="description" content=".category-card:hover img { transform: scale(1.08); }"/>
```

## Solution: Use Rank Math SEO Plugin (Already Installed)

### Step 1: Access WordPress Admin
1. Go to your WordPress admin: `https://spherevista360.com/wp-admin/`
2. Login with your credentials

### Step 2: Go to Rank Math SEO
1. In the left sidebar, click **Rank Math** (or **SEO**)
2. Click **Titles & Meta**

### Step 3: Edit Homepage Settings
1. Look for the **Homepage** tab/section
2. Find the **Homepage Description** field
3. Replace the current content with a proper description

### Step 4: Set Proper Description
Use this recommended description:
```
SphereVista360 - Your trusted source for technology insights, AI trends, and digital innovation. Discover expert analysis on product analytics, cloud computing, and emerging technologies.
```

### Alternative: Edit Homepage Directly
If Rank Math isn't controlling the homepage:

1. Go to **Pages** → **All Pages**
2. Find and edit your **Homepage** (usually "Home" or "Front Page")
3. Scroll down to **Rank Math SEO** meta box
4. Set the **Description** field there

## Verify the Fix
After saving, test your homepage:
```
https://spherevista360.com/
```

Check the page source (Ctrl+U) and look for:
```html
<meta name="description" content="SphereVista360 - Your trusted source for..."/>
```

## Why This Matters for AdSense
- ✅ **SEO Improvement**: Better search result snippets
- ✅ **AdSense Compliance**: Shows site has proper meta tags
- ✅ **User Experience**: Better description in search results
- ✅ **Review Safety**: Safe change during AdSense review

## If Rank Math Isn't Working
If you can't find the setting, the meta description might be hardcoded in your theme. In that case:

1. Go to **Appearance** → **Theme Editor**
2. Edit **header.php**
3. Find: `<meta name="description"`
4. Replace the content with proper description
5. Save changes

## Test After Changes
1. Clear any caching (WP plugins, browser cache)
2. Test the homepage URL
3. Check Google Search Console for indexing updates
4. Verify the meta description appears correctly

This is a **safe change** during AdSense review and will improve your site's SEO and AdSense approval chances.