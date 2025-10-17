# SphereVista360 Newsletter Integration - Refactored

A modular, maintainable WordPress newsletter integration with Mailchimp API support.

## 🚀 What's New in This Refactored Version

- **Modular Architecture**: Separated concerns into dedicated classes
- **Better Error Handling**: Comprehensive error logging and user feedback
- **Enhanced Security**: Improved input validation and nonce handling
- **Performance Optimized**: External assets with fallbacks
- **Accessibility**: Better keyboard navigation and screen reader support
- **Analytics Integration**: Built-in Google Analytics and Facebook Pixel tracking
- **Responsive Design**: Mobile-first approach with modern CSS
- **Developer Friendly**: Extensive hooks and filters for customization

## 📁 File Structure

```
newsletter-integration/
├── README.md                    # This documentation
├── LICENSE                      # GPL-2.0-or-later license
├── composer.json               # PHP dependencies and autoloading
├── package.json                # Node.js dependencies for development
├── newsletter-integration-refactored.php  # Main integration file
├── includes/                   # PHP classes
│   ├── class-newsletter-config.php     # Configuration management
│   ├── class-mailchimp-api.php         # Mailchimp API handling
│   ├── class-newsletter-form.php       # Form generation and AJAX
│   └── class-newsletter-assets.php     # Asset management
└── assets/                    # Frontend assets
    ├── js/
    │   └── newsletter.js               # Frontend JavaScript
    └── css/
        └── newsletter.css              # Stylesheet
```

## 🛠 Installation

### Step 1: Upload Files to Your Theme
Copy the entire `newsletter-integration/` folder to your WordPress theme directory:

```bash
# If using command line:
cp -r newsletter-integration/ wp-content/themes/your-theme/

# Or upload via FTP/SFTP to:
# wp-content/themes/your-theme/newsletter-integration/
```

### Step 2: Include the Main File
Add this line to your theme's `functions.php` file:

```php
require_once get_template_directory() . '/newsletter-integration/newsletter-integration-refactored.php';
```

### Step 3: Configure Mailchimp
Set your Mailchimp credentials using one of these methods:

**Option A: WordPress Options (Recommended)**
```php
// Add to functions.php or use a custom plugin
update_option('spherevista360_mailchimp_api_key', 'your-mailchimp-api-key');
update_option('spherevista360_mailchimp_audience_id', 'your-audience-id');
```

**Option B: Constants in wp-config.php**
```php
define('SPHEREVISTA360_MAILCHIMP_API_KEY', 'your-mailchimp-api-key');
define('SPHEREVISTA360_MAILCHIMP_AUDIENCE_ID', 'your-audience-id');
```

**Option C: Filters (Advanced)**
```php
add_filter('spherevista360_mailchimp_api_key', function() {
    return 'your-mailchimp-api-key';
});

add_filter('spherevista360_mailchimp_audience_id', function() {
    return 'your-audience-id';
});
```

## ⚙️ Configuration Options

### Basic Settings
- `spherevista360_mailchimp_api_key`: Your Mailchimp API key
- `spherevista360_mailchimp_audience_id`: Your Mailchimp audience/list ID
- `spherevista360_show_footer_newsletter`: 'yes' or 'no' to show in footer

### Advanced Customization

#### Custom Form Styling
```php
add_filter('spherevista360_newsletter_form_args', function($args, $context) {
    if ($context === 'footer') {
        $args['classes'][] = 'my-custom-class';
        $args['title'] = 'Join Our Community';
    }
    return $args;
}, 10, 2);
```

#### Custom Merge Fields
```php
add_filter('spherevista360_subscription_merge_fields', function($fields, $email) {
    $fields['CUSTOM_FIELD'] = 'custom_value';
    return $fields;
}, 10, 2);
```

#### Custom Validation
```php
add_filter('spherevista360_validate_email', function($is_valid, $email) {
    // Add custom validation logic
    return $is_valid && !is_disposable_email($email);
}, 10, 2);
```

## 🎨 Usage Examples

### Basic Newsletter Form
```php
// Display in post content automatically (enabled by default)
// Or manually in templates:
echo spherevista360_get_newsletter_form('custom');
```

### Custom Form Arguments
```php
$args = array(
    'title' => 'Get My Free Guide',
    'description' => 'Download our comprehensive WordPress monetization guide.',
    'button_text' => 'Get Free Guide',
    'placeholder' => 'your.email@example.com',
    'classes' => array('custom-form', 'landing-page'),
    'show_privacy' => false
);

echo spherevista360_get_newsletter_form('landing', $args);
```

### Footer Newsletter
```php
// Uncomment in newsletter-integration-refactored.php
add_action('wp_footer', array('SphereVista360_Newsletter_Form', 'footer_newsletter'));
```

## 🔧 API Reference

### Classes

#### SphereVista360_Newsletter_Config
- `get_mailchimp_api_key()`: Get API key
- `get_mailchimp_audience_id()`: Get audience ID
- `is_configured()`: Check if properly configured
- `get_version()`: Get plugin version

#### SphereVista360_Mailchimp_API
- `subscribe($email, $merge_fields)`: Subscribe user to newsletter

#### SphereVista360_Newsletter_Form
- `generate_form($context, $args)`: Generate newsletter form HTML
- `handle_ajax_signup()`: Process AJAX form submissions

#### SphereVista360_Newsletter_Assets
- `enqueue_assets()`: Enqueue scripts and styles
- `add_inline_styles()`: Add fallback inline CSS

### Utility Functions
- `spherevista360_newsletter_is_configured()`: Check configuration
- `spherevista360_get_newsletter_form($context, $args)`: Get form HTML
- `spherevista360_newsletter_form($context, $args)`: Echo form HTML

## 🎯 Features

### ✅ Enhanced Security
- Nonce verification on all requests
- Input sanitization and validation
- Rate limiting protection
- XSS prevention

### ✅ Better UX
- Loading states and animations
- Clear error/success messages
- Mobile-responsive design
- Keyboard navigation support

### ✅ Analytics Integration
- Google Analytics event tracking
- Facebook Pixel conversion tracking
- Custom event hooks

### ✅ Developer Experience
- Extensive action/filter hooks
- Comprehensive error logging
- Modular architecture
- Well-documented code

### ✅ Performance
- External assets with fallbacks
- Optimized CSS/JS delivery
- Minimal database queries
- CDN-friendly structure

## 🐛 Troubleshooting

### Common Issues

**"Newsletter service is not configured"**
- Check your Mailchimp API key and audience ID
- Verify the constants/options are set correctly

**"Security check failed"**
- Clear browser cache and try again
- Check if nonces are being generated properly

### Styles not loading
- Verify CSS file path: `wp-content/themes/your-theme/newsletter-integration/assets/css/newsletter.css`
- Check file permissions
- Inline styles will load as fallback

**JavaScript not working**
- Verify JS file path: `wp-content/themes/your-theme/newsletter-integration/assets/js/newsletter.js`
- Check for JavaScript errors in browser console
- Ensure jQuery is loaded

### Debug Mode
Enable WordPress debug mode to see detailed error logs:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

## 📊 Mailchimp Setup

1. **Get API Key**: Mailchimp Dashboard → Account → Extras → API Keys
2. **Find Audience ID**: Mailchimp Dashboard → Audience → Settings → Audience name and defaults
3. **Test Connection**: Use the test function in the code (uncomment for debugging)

## 🔄 Migration from Old Version

If you're upgrading from the original version:

1. **Backup**: Always backup your functions.php
2. **Remove Old Code**: Remove the old newsletter functions
3. **Upload New Files**: Follow the installation steps above
4. **Test**: Test forms on different pages
5. **Update Configuration**: Set your API credentials using the new methods

## 🤝 Contributing

This refactored version is designed to be maintainable and extensible. Key improvement areas:

- Add more email service providers (Sendinblue, ConvertKit, etc.)
- Implement A/B testing for form variations
- Add email template customization
- Create admin settings page
- Add REST API endpoints

## 📝 Changelog

### Version 1.0.0 (Refactored)
- Complete architectural refactor
- Modular class-based structure
- Enhanced security and validation
- Improved error handling
- Modern responsive design
- Analytics integration
- Extensive customization hooks

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs in `wp-content/debug.log`
3. Test with a fresh WordPress installation
4. Check Mailchimp API status

---

**Built with ❤️ for the WordPress community**