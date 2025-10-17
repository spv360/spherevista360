<?php
/**
 * SphereVista360 Newsletter Form Handler
 *
 * Handles form generation and AJAX processing
 */

class SphereVista360_Newsletter_Form {

    /**
     * Initialize the form handler
     */
    public static function init() {
        add_action('wp_ajax_nopriv_spherevista360_newsletter_signup', array(__CLASS__, 'handle_ajax_signup'));
        add_action('wp_ajax_spherevista360_newsletter_signup', array(__CLASS__, 'handle_ajax_signup'));
    }

    /**
     * Handle AJAX newsletter signup
     */
    public static function handle_ajax_signup() {
        try {
            // Verify nonce for security
            if (!wp_verify_nonce($_POST['nonce'], 'spherevista360_newsletter_nonce')) {
                wp_die(json_encode(array(
                    'success' => false,
                    'message' => 'Security check failed. Please refresh and try again.'
                )));
            }

            // Get and validate email
            $email = sanitize_email($_POST['email']);
            if (!is_email($email)) {
                wp_die(json_encode(array(
                    'success' => false,
                    'message' => 'Please enter a valid email address.'
                )));
            }

            // Get additional data
            $context = isset($_POST['context']) ? sanitize_text_field($_POST['context']) : 'unknown';
            $merge_fields = array(
                'SIGNUP_PAGE' => isset($_POST['current_url']) ? esc_url_raw($_POST['current_url']) : '',
                'USER_AGENT' => isset($_SERVER['HTTP_USER_AGENT']) ? sanitize_text_field($_SERVER['HTTP_USER_AGENT']) : '',
                'SIGNUP_CONTEXT' => $context
            );

            // Attempt subscription
            $result = SphereVista360_Mailchimp_API::subscribe($email, $merge_fields);

            if (is_wp_error($result)) {
                wp_die(json_encode(array(
                    'success' => false,
                    'message' => $result->get_error_message()
                )));
            }

            wp_die(json_encode($result));

        } catch (Exception $e) {
            if (defined('WP_DEBUG') && WP_DEBUG) {
                error_log('[SphereVista360 Newsletter] AJAX Error: ' . $e->getMessage());
            }

            wp_die(json_encode(array(
                'success' => false,
                'message' => 'An unexpected error occurred. Please try again later.'
            )));
        }
    }

    /**
     * Generate newsletter signup form
     */
    public static function generate_form($context = 'post', $args = array()) {
        $defaults = array(
            'title' => 'Stay Updated with SphereVista360',
            'description' => 'Get the latest insights on 360° photography, virtual tours, and immersive experiences delivered to your inbox.',
            'button_text' => 'Subscribe',
            'placeholder' => 'Enter your email address',
            'show_privacy' => true,
            'classes' => array()
        );

        $args = wp_parse_args($args, $defaults);
        $form_id = 'newsletter-' . $context . '-' . uniqid();
        $context_class = 'newsletter-' . $context;
        $custom_classes = implode(' ', array_map('esc_attr', $args['classes']));

        ob_start();
        ?>
        <div class="newsletter-signup <?php echo esc_attr($context_class . ' ' . $custom_classes); ?>">
            <div class="newsletter-header">
                <h3><?php echo esc_html($args['title']); ?></h3>
                <p><?php echo esc_html($args['description']); ?></p>
            </div>

            <form id="<?php echo esc_attr($form_id); ?>" class="newsletter-form" method="post" data-context="<?php echo esc_attr($context); ?>">
                <?php wp_nonce_field('spherevista360_newsletter_nonce', 'newsletter_nonce'); ?>
                <div class="form-group">
                    <input type="email"
                           name="email"
                           placeholder="<?php echo esc_attr($args['placeholder']); ?>"
                           required
                           class="newsletter-email"
                           autocomplete="email">
                    <button type="submit" class="newsletter-submit">
                        <span class="submit-text"><?php echo esc_html($args['button_text']); ?></span>
                        <span class="loading-text" style="display: none;">Subscribing...</span>
                    </button>
                </div>
                <div class="newsletter-message" style="display: none;"></div>
                <?php if ($args['show_privacy']) : ?>
                <div class="newsletter-privacy">
                    <small>We respect your privacy. Unsubscribe at any time.</small>
                </div>
                <?php endif; ?>
            </form>
        </div>
        <?php

        return ob_get_clean();
    }

    /**
     * Generate footer newsletter
     */
    public static function footer_newsletter() {
        echo self::generate_form('footer', array(
            'classes' => array('newsletter-footer')
        ));
    }

    /**
     * Add newsletter after post content
     */
    public static function add_after_post($content) {
        if (is_single() && in_the_loop() && is_main_query()) {
            $newsletter = '<div class="post-newsletter-wrapper">' .
                self::generate_form('post') .
                '</div>';
            $content .= $newsletter;
        }
        return $content;
    }
}