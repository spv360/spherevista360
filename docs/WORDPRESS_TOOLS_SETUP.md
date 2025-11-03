# WordPress Tools Setup Guide

## Step 1: Create SIP Calculator Page

1. **Login to WordPress Admin**
   - Go to your WordPress dashboard

2. **Create New Page**
   - Pages → Add New
   - Title: "SIP Calculator"
   - Permalink: `/sip-calculator/` (WordPress will auto-generate this)

3. **Add Calculator Content**
   - Switch to "Code Editor" (or use shortcode block)
   - Add this shortcode: `[sip_calculator]`
   - Optional: Add introductory text above the shortcode

4. **Publish Page**
   - Click "Publish"

## Step 2: Create Tools Page

1. **Create New Page**
   - Pages → Add New
   - Title: "Tools"
   - Permalink: `/tools/`

2. **Add Tools Content**
   - Copy the content from `tools_page_content.html`
   - Switch to "Code Editor" and paste the content
   - Or use the visual editor and recreate the layout

3. **Publish Page**
   - Click "Publish"

## Step 3: Add to Navigation Menu

1. **Go to Menus**
   - Appearance → Menus

2. **Add Pages to Menu**
   - Check "Tools" page
   - Check "SIP Calculator" page
   - Click "Add to Menu"

3. **Organize Menu Structure**
   - Drag "Tools" to be a top-level menu item
   - Drag "SIP Calculator" under "Tools" (make it a submenu item)
   - Or keep both as top-level items

4. **Save Menu**
   - Click "Save Menu"

## Step 4: Test Navigation

1. **Visit Your Site**
   - Go to your homepage
   - Check that "Tools" appears in navigation
   - Click "Tools" → should show tools listing page
   - Click "SIP Calculator" → should show the calculator

## Step 5: SEO Optimization (Optional)

1. **Add Meta Descriptions**
   - Install Yoast SEO or similar plugin
   - Add compelling meta descriptions for both pages

2. **Internal Linking**
   - Link to tools from your homepage or blog posts
   - Add "Try our SIP Calculator" links in relevant content

## Troubleshooting

### Calculator Not Showing
- Verify plugin is activated
- Check shortcode syntax: `[sip_calculator]`
- Clear WordPress cache if using caching plugin

### Menu Not Appearing
- Check theme supports menus
- Verify menu is assigned to correct location
- Clear browser cache

### Pages Not Found (404)
- Go to Settings → Permalinks
- Click "Save Changes" to refresh permalinks

## Customization Options

### Shortcode Parameters
```
[sip_calculator monthly_investment="500" return_rate="10" investment_period="10"]
```

### Custom CSS
Add to Appearance → Customize → Additional CSS:
```css
/* Custom styling for tools pages */
.tools-page-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
}
```

## Next Steps

1. **Add More Tools**: Expand your tools section with additional calculators
2. **Track Usage**: Use Google Analytics to monitor tool engagement
3. **User Feedback**: Add feedback forms to improve tools
4. **Mobile Optimization**: Ensure all tools work perfectly on mobile devices

## Support

If you encounter issues:
1. Check this guide first
2. Verify plugin compatibility with your WordPress version
3. Test with default WordPress theme (Twenty Twenty-One)
4. Contact plugin developer if issues persist
