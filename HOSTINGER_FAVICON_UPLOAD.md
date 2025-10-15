# Hostinger Favicon Upload Guide

## Method 1: File Manager (Easiest)
1. **Login to Hostinger Control Panel**
   - Go to https://www.hostinger.com/
   - Click "Login" → Select your hosting account

2. **Access File Manager**
   - In hPanel, go to **Files** → **File Manager**
   - Navigate to your WordPress root directory (usually `public_html` or domain folder)

3. **Upload Files**
   - Click **Upload** button
   - Select your `favicon.ico` and `apple-touch-icon.png` files
   - Upload to the root directory (same level as `wp-admin`, `wp-content`, etc.)

## Method 2: FTP/SFTP
1. **Get FTP Credentials**
   - In Hostinger hPanel → **Files** → **FTP Accounts**
   - Note down: Host, Username, Password, Port (usually 21 for FTP, 22 for SFTP)

2. **Connect via FTP Client**
   - Use FileZilla, WinSCP, or any FTP client
   - Connect using your credentials
   - Navigate to WordPress root directory
   - Upload the favicon files

## Method 3: WordPress Media Library + Manual Move
1. **Upload via WordPress**
   - Go to **Media** → **Add New**
   - Upload your favicon files
   - Note the URLs

2. **Move Files via File Manager**
   - Use Hostinger File Manager to move files from `wp-content/uploads/` to root directory
   - Update the HTML code with correct paths if needed

## Verification Steps:
1. **Clear Cache**: Clear your browser cache and any caching plugins
2. **Test URLs**:
   - Visit: `https://yourdomain.com/favicon.ico`
   - Visit: `https://yourdomain.com/apple-touch-icon.png`
3. **Browser Test**: Open your site in a new tab - favicon should appear
4. **Mobile Test**: Check on iOS devices for Apple touch icon

## Important Notes:
- Files must be in the **root directory** of your WordPress installation
- Ensure files are publicly accessible (permissions usually 644)
- If using a CDN, you may need to purge the cache there too
- Test on multiple browsers and devices