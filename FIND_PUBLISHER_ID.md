# How to Find Your Google AdSense Publisher ID

## Method 1: From AdSense Dashboard (Recommended)

1. **Sign in to Google AdSense**
   - Go to [adsense.google.com](https://adsense.google.com)
   - Sign in with your Google account

2. **Check the Account Tab**
   - Click on **Account** in the left sidebar
   - Look for **Publisher ID** - it will be in format: `pub-XXXXXXXXXXXXXXXX`
   - Copy this ID (including the "pub-" prefix)

## Method 2: From Ad Code

1. **Go to Ads → By site**
   - Click **Ads** → **By site** in the left sidebar

2. **Get ad code for any site**
   - Click **Ad code** for any of your sites
   - Look for the `data-ad-client` attribute in the code
   - The publisher ID is the value: `ca-pub-XXXXXXXXXXXXXXXX`

## Method 3: From Settings

1. **Go to Settings**
   - Click the gear icon (Settings) in the top right

2. **Check Account Information**
   - Look under **Account information**
   - Your Publisher ID should be listed there

## Method 4: Check Existing Ad Code on Your Site

If you already have AdSense ads on your site:
1. View source code of any page with ads
2. Search for `data-ad-client`
3. The value will be your publisher ID: `ca-pub-XXXXXXXXXXXXXXXX`

## Important Notes:

- **Format**: Publisher ID always starts with `pub-` or `ca-pub-`
- **Length**: Usually 16 characters after the prefix
- **Example**: `pub-1234567890123456` or `ca-pub-1234567890123456`

## Update ads.txt

Once you have your publisher ID, edit the `ads.txt` file and replace:
```
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
```

With your actual ID:
```
google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0
```

## Verification

After updating and uploading ads.txt:
- Visit: `https://yourdomain.com/ads.txt`
- Check AdSense: The warning should disappear within a few days