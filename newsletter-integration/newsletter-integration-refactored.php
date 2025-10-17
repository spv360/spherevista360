<?php
/**
 * SPHEREVISTA360 NEWSLETTER INTEGRATION FOR KADENCE THEME
 * =================================================================
 *
 * REFACTORED VERSION - Modular and Maintainable
 *
 * IMPORTANT: Do NOT replace your entire Kadence functions.php file!
 * Instead, ADD these functions to your existing functions.php file.
 *
 * NEW FILE STRUCTURE:
 * ===================
 * - includes/class-newsletter-config.php    - Configuration management
 * - includes/class-mailchimp-api.php        - Mailchimp API handling
 * - includes/class-newsletter-form.php      - Form generation and AJAX
 * - includes/class-newsletter-assets.php    - Asset management
 * - newsletter/js/newsletter.js             - Frontend JavaScript
 * - newsletter/css/newsletter.css           - Stylesheet
 *
 * SETUP INSTRUCTIONS:
 * ===================
 * 1. Create the folder structure in your theme:
 *    wp-content/themes/kadence/newsletter/
 *    wp-content/themes/kadence/newsletter/js/
 *    wp-content/themes/kadence/newsletter/css/
 *    wp-content/themes/kadence/includes/
 *
 * 2. Upload all the include files to wp-content/themes/kadence/includes/
 *
 * 3. Upload newsletter.js to wp-content/themes/kadence/newsletter/js/
 *
 * 4. Upload newsletter.css to wp-content/themes/kadence/newsletter/css/
 *
 * 5. Add the code below to your functions.php file
 *
 * 6. Configure your Mailchimp settings (see configuration options below)
 *
 * =================================================================
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Include required classes
$includes_path = get_template_directory() . '/includes/';

$required_files = array(
    'class-newsletter-config.php',
    'class-mailchimp-api.php',
    'class-newsletter-form.php',
    'class-newsletter-assets.php'
);

foreach ($required_files as $file) {
    $file_path = $includes_path . $file;
    if (file_exists($file_path)) {
        require_once $file_path;
    } else {
        // Log error if file is missing
        if (defined('WP_DEBUG') && WP_DEBUG) {
            error_log('[SphereVista360 Newsletter] Missing required file: ' . $file_path);
        }
        return; // Exit if required files are missing
    }
}

/**
 * Initialize SphereVista360 Newsletter
 */
function spherevista360_newsletter_init() {
    // Initialize components
    SphereVista360_Newsletter_Form::init();
    SphereVista360_Newsletter_Assets::init();

    // Add newsletter after post content
    add_filter('the_content', array('SphereVista360_Newsletter_Form', 'add_after_post'));

    // Add inline styles as fallback
    add_action('wp_head', array('SphereVista360_Newsletter_Assets', 'add_inline_styles'));
}
add_action('init', 'spherevista360_newsletter_init');

/**
 * Add newsletter to footer (optional)
 * Uncomment the line below to show newsletter in footer
 */
// add_action('wp_footer', array('SphereVista360_Newsletter_Form', 'footer_newsletter'));

/**
 * CONFIGURATION OPTIONS
 * =====================
 *
 * You can configure the newsletter using WordPress options or constants:
 *
 * 1. Via WordPress Admin (recommended):
 *    - Go to Admin > Settings > General
 *    - Add these options with your values:
 *      - spherevista360_mailchimp_api_key: Your Mailchimp API key
 *      - spherevista360_mailchimp_audience_id: Your audience ID
 *      - spherevista360_show_footer_newsletter: 'yes' or 'no'
 *
 * 2. Via wp-config.php constants:
 *    define('SPHEREVISTA360_MAILCHIMP_API_KEY', 'your-api-key-here');
 *    define('SPHEREVISTA360_MAILCHIMP_AUDIENCE_ID', 'your-audience-id');
 *
 * 3. Via filters (for advanced customization):
 *    add_filter('spherevista360_mailchimp_api_key', function($key) { return 'your-key'; });
 *    add_filter('spherevista360_mailchimp_audience_id', function($id) { return 'your-id'; });
 */

/**
 * Admin notice for configuration
 */
function spherevista360_newsletter_admin_notice() {
    if (!current_user_can('manage_options')) {
        return;
    }

    if (SphereVista360_Newsletter_Config::is_configured()) {
        return; // Already configured
    }

    $class = 'notice notice-warning is-dismissible';
    $message = sprintf(
        __('SphereVista360 Newsletter is not configured. Please set your Mailchimp API key. <a href="%s">Configure now</a>.'),
        admin_url('options-general.php')
    );

    printf('<div class="%1$s"><p>%2$s</p></div>', esc_attr($class), wp_kses_post($message));
}
add_action('admin_notices', 'spherevista360_newsletter_admin_notice');

/**
 * UTILITY FUNCTIONS
 * =================
 */

/**
 * Check if newsletter is configured
 */
function spherevista360_newsletter_is_configured() {
    return SphereVista360_Newsletter_Config::is_configured();
}

/**
 * Manually generate newsletter form
 */
function spherevista360_get_newsletter_form($context = 'custom', $args = array()) {
    return SphereVista360_Newsletter_Form::generate_form($context, $args);
}

/**
 * Echo newsletter form
 */
function spherevista360_newsletter_form($context = 'custom', $args = array()) {
    echo spherevista360_get_newsletter_form($context, $args);
}

/**
 * DEVELOPMENT HELPERS
 * ===================
 */

/**
 * Test Mailchimp connection
 */
function spherevista360_test_mailchimp_connection() {
    if (!current_user_can('manage_options') || !defined('WP_DEBUG') || !WP_DEBUG) {
        return;
    }

    $test_email = 'test-' . time() . '@example.com';
    $result = SphereVista360_Mailchimp_API::subscribe($test_email);

    if (defined('WP_DEBUG') && WP_DEBUG) {
        error_log('[SphereVista360 Newsletter] Connection test result: ' . print_r($result, true));
    }

    return $result;
}
// spherevista360_test_mailchimp_connection(); // Uncomment to test connection