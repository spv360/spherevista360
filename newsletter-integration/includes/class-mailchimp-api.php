<?php
/**
 * SphereVista360 Mailchimp API Handler
 *
 * Handles all Mailchimp API interactions
 */

class SphereVista360_Mailchimp_API {

    /**
     * Subscribe user to newsletter
     */
    public static function subscribe($email, $merge_fields = array()) {
        // Validate configuration
        if (!SphereVista360_Newsletter_Config::is_configured()) {
            return new WP_Error('config_error', 'Newsletter service is not configured yet.');
        }

        // Validate email
        if (!is_email($email)) {
            return new WP_Error('invalid_email', 'Please enter a valid email address.');
        }

        $api_key = SphereVista360_Newsletter_Config::get_mailchimp_api_key();
        $audience_id = SphereVista360_Newsletter_Config::get_mailchimp_audience_id();

        // Extract datacenter from API key
        $datacenter = substr($api_key, strpos($api_key, '-') + 1);
        $url = 'https://' . $datacenter . '.api.mailchimp.com/3.0/lists/' . $audience_id . '/members/';

        // Prepare subscriber data
        $subscriber_data = array(
            'email_address' => $email,
            'status' => 'pending', // Double opt-in
            'merge_fields' => array_merge(array(
                'SIGNUP_SRC' => 'wordpress_site',
                'SIGNUP_DATE' => date('Y-m-d H:i:s')
            ), $merge_fields)
        );

        // Setup cURL request
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_USERPWD, 'user:' . $api_key);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 15);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($subscriber_data));

        // Execute request
        $result = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);

        // Handle cURL errors
        if ($curl_error) {
            self::log_error('cURL Error: ' . $curl_error);
            return new WP_Error('connection_error', 'Unable to connect to newsletter service. Please try again later.');
        }

        // Handle HTTP response
        return self::handle_api_response($http_code, $result);
    }

    /**
     * Handle Mailchimp API response
     */
    private static function handle_api_response($http_code, $result) {
        $response_data = json_decode($result, true);

        switch ($http_code) {
            case 200:
                // Success - already subscribed or newly subscribed
                return array(
                    'success' => true,
                    'message' => 'Thanks! Please check your email and click the confirmation link to complete your subscription.',
                    'data' => $response_data
                );

            case 400:
                // Bad request - check for specific errors
                if (isset($response_data['title']) && $response_data['title'] === 'Member Exists') {
                    return array(
                        'success' => false,
                        'message' => 'This email is already subscribed to our newsletter.',
                        'code' => 'already_subscribed'
                    );
                } elseif (isset($response_data['title']) && $response_data['title'] === 'Invalid Resource') {
                    self::log_error('Mailchimp API Error: Invalid Resource - ' . json_encode($response_data));
                    return array(
                        'success' => false,
                        'message' => 'There was an error with your subscription. Please try again.',
                        'code' => 'invalid_resource'
                    );
                } else {
                    self::log_error('Mailchimp API Error (400): ' . json_encode($response_data));
                    return array(
                        'success' => false,
                        'message' => 'There was an error with your subscription. Please try again.',
                        'code' => 'bad_request'
                    );
                }

            case 401:
                self::log_error('Mailchimp API Error (401): Unauthorized - Check API key');
                return new WP_Error('auth_error', 'Newsletter service configuration error. Please contact the administrator.');

            case 404:
                self::log_error('Mailchimp API Error (404): List not found - Check Audience ID');
                return new WP_Error('list_error', 'Newsletter service configuration error. Please contact the administrator.');

            default:
                self::log_error('Mailchimp API Error (' . $http_code . '): ' . $result);
                return array(
                    'success' => false,
                    'message' => 'Unable to process your request right now. Please try again later.',
                    'code' => 'server_error'
                );
        }
    }

    /**
     * Log errors for debugging
     */
    private static function log_error($message) {
        if (defined('WP_DEBUG') && WP_DEBUG) {
            error_log('[SphereVista360 Newsletter] ' . $message);
        }
    }
}