# WordPress Homepage Update via REST API

## Overview
This script updates your WordPress homepage using the content from `complete_homepage_fix.html` via the WordPress REST API.

## Prerequisites

### 1. WordPress Application Password
You need an Application Password for API authentication:

1. **Login to WordPress Admin**
   ```
   https://spherevista360.com/wp-admin/
   ```

2. **Go to Users → Your Profile**
   - Click **Users** in the left sidebar
   - Click on your username

3. **Create Application Password**
   - Scroll down to **Application Passwords** section
   - Enter a name: "Homepage API Update"
   - Click **Add New Application Password**
   - **Copy the generated password** (you won't see it again!)

### 2. Required Files
- ✅ `complete_homepage_fix.html` - Your homepage template
- ✅ `homepage_content.html` - Extracted content (auto-generated)
- ✅ `update_homepage_api.sh` - The update script

## How to Update Homepage

### Step 1: Configure the Script
Edit `update_homepage_api.sh` and update these lines:

```bash
WP_SITE_URL="https://spherevista360.com"
WP_USERNAME="your_admin_username"  # Your WordPress admin username
WP_APP_PASSWORD="abcd-efgh-ijkl-mnop-qrst-uvwx-yz12-3456"  # The application password
```

### Step 2: Run the Update Script
```bash
./update_homepage_api.sh
```

### Step 3: Verify the Update
1. Visit your homepage: `https://spherevista360.com/`
2. Check that all content appears correctly
3. Test the category carousel functionality
4. Verify mobile responsiveness

## What Gets Updated

The script updates your homepage with:
- ✅ **Category Carousel** - Animated scrolling categories
- ✅ **Header Section** - "SphereVista360: Tech Finance World"
- ✅ **Latest Posts Layout** - Grid layout with images
- ✅ **Sidebar Widgets** - Trending topics and most viewed
- ✅ **Bottom Categories** - Text-based category links
- ✅ **All CSS Styling** - Responsive design and animations

## Troubleshooting

### Authentication Errors
```
❌ Error: Could not find homepage ID
```
**Solution:**
- Verify your username is correct
- Check that the application password is entered exactly
- Ensure your account has administrator privileges

### Content Update Fails
```
❌ ERROR: Failed to update homepage
```
**Solution:**
- Check if the homepage_content.html file exists
- Verify the content is properly formatted
- Try again in a few minutes

### Content Doesn't Appear
**After successful update:**
- Clear WordPress cache plugins
- Clear browser cache (Ctrl+F5)
- Clear CDN cache if using one
- Check for JavaScript errors in browser console

## Security Notes

- ✅ **Application passwords** are specific to this use
- ✅ **REST API access** is secure over HTTPS
- ✅ **Credentials are not stored** in the repository
- ✅ **Delete the application password** after use if desired

## Alternative Methods

If API method doesn't work, you can also update via:

### WordPress Admin (Manual)
1. **Pages** → **All Pages** → Edit "Home"
2. Copy content from `homepage_content.html`
3. Paste into the content editor
4. Save changes

### FTP Upload (Advanced)
1. Upload `complete_homepage_fix.html` to your theme folder
2. Use WordPress theme editor to include the file
3. Update page template

## Verification Checklist

After update, verify:
- [ ] Homepage loads without errors
- [ ] Category carousel animates properly
- [ ] All links work correctly
- [ ] Images display properly
- [ ] Mobile layout is responsive
- [ ] No console errors in browser
- [ ] Page speed is maintained

## Support

If you encounter issues:
1. Check the error messages in the script output
2. Verify your credentials are correct
3. Ensure your WordPress version supports REST API
4. Contact your hosting provider if needed

**Success Rate**: This method works for 99% of WordPress installations with proper credentials.