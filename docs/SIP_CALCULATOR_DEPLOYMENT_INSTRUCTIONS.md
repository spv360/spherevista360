# SIP Calculator Deployment Instructions

## Method 1: WordPress Admin Upload (Recommended)

1. **Login to WordPress Admin**
   - Go to https://spherevista360.com/wp-admin/
   - Login with your admin credentials

2. **Upload Plugin**
   - Navigate to Plugins → Add New
   - Click "Upload Plugin"
   - Choose the `sip-calculator.zip` file
   - Click "Install Now"
   - Activate the plugin

3. **Add Calculator to Page**
   - Create a new page or edit existing page
   - Add the shortcode: `[sip_calculator]`
   - Publish the page

## Method 2: Manual FTP Upload

1. **Upload Files**
   - Upload the `sip-calculator-plugin` folder to `/wp-content/plugins/`
   - Rename folder to `sip-calculator`

2. **Activate Plugin**
   - Login to WordPress admin
   - Go to Plugins
   - Activate "SIP Calculator"

3. **Add to Page**
   - Use shortcode `[sip_calculator]` in any page/post

## Method 3: Direct HTML Embed

If you prefer not to use a plugin, you can embed the calculator directly:

1. Copy the content from `sip_calculator_wordpress_page.html`
2. Create a new WordPress page
3. Switch to "HTML" editor mode
4. Paste the content
5. Publish the page

## Testing

After deployment:

1. Visit the page with the calculator
2. Test with default values (should show ~$103K final value for $500/month at 10% for 10 years)
3. Test export functionality
4. Test advanced options

## Customization

You can customize the calculator by modifying the shortcode parameters:

```
[sip_calculator monthly_investment="1000" return_rate="12" investment_period="20"]
```

## Troubleshooting

- **Calculator not loading**: Check if plugin is activated
- **Styles not working**: Clear browser cache and WordPress cache
- **Shortcode not working**: Make sure you're using the correct shortcode format

## Support

For issues or questions, check the plugin's README.md file or contact the developer.
