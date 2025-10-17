<?php
/**
 * SphereVista360 Newsletter Configuration
 *
 * Centralized configuration for newsletter functionality
 */

class SphereVista360_Newsletter_Config {

    /**
     * Get Mailchimp API key
     */
    public static function get_mailchimp_api_key() {
        // First check for constant, then option, then filter
        $api_key = defined('SPHEREVISTA360_MAILCHIMP_API_KEY') ?
            SPHEREVISTA360_MAILCHIMP_API_KEY :
            get_option('spherevista360_mailchimp_api_key', '');

        // Allow override via filter
        return apply_filters('spherevista360_mailchimp_api_key', $api_key);
    }

    /**
     * Get Mailchimp audience ID
     */
    public static function get_mailchimp_audience_id() {
        $audience_id = defined('SPHEREVISTA360_MAILCHIMP_AUDIENCE_ID') ?
            SPHEREVISTA360_MAILCHIMP_AUDIENCE_ID :
            get_option('spherevista360_mailchimp_audience_id', 'bbb4f96a8b');

        return apply_filters('spherevista360_mailchimp_audience_id', $audience_id);
    }

    /**
     * Get plugin version
     */
    public static function get_version() {
        return '1.0.0';
    }

    /**
     * Check if newsletter is properly configured
     */
    public static function is_configured() {
        $api_key = self::get_mailchimp_api_key();
        return !empty($api_key) && $api_key !== 'YOUR_MAILCHIMP_API_KEY_HERE';
    }

    /**
     * Get asset URLs
     */
    public static function get_asset_url($file) {
        return get_template_directory_uri() . '/newsletter/' . $file;
    }

    /**
     * Get asset paths
     */
    public static function get_asset_path($file) {
        return get_template_directory() . '/newsletter/' . $file;
    }
}