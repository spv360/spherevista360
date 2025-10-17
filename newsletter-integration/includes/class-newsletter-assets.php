<?php
/**
 * SphereVista360 Newsletter Assets Manager
 *
 * Handles enqueuing scripts and styles
 */

class SphereVista360_Newsletter_Assets {

    /**
     * Initialize assets
     */
    public static function init() {
        add_action('wp_enqueue_scripts', array(__CLASS__, 'enqueue_assets'));
    }

    /**
     * Enqueue newsletter assets
     */
    public static function enqueue_assets() {
        // Only enqueue if we have the necessary files or if we're on a page that needs them
        if (!self::should_enqueue_assets()) {
            return;
        }

        // Enqueue jQuery as dependency
        wp_enqueue_script('jquery');

        // Enqueue newsletter script
        wp_enqueue_script(
            'spherevista360-newsletter',
            SphereVista360_Newsletter_Config::get_asset_url('js/newsletter.js'),
            array('jquery'),
            SphereVista360_Newsletter_Config::get_version(),
            true
        );

        // Localize script with AJAX data
        wp_localize_script('spherevista360_newsletter', 'spherevista360_newsletter', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('spherevista360_newsletter_nonce'),
            'current_url' => self::get_current_url(),
            'strings' => array(
                'subscribing' => __('Subscribing...', 'spherevista360'),
                'subscribe' => __('Subscribe', 'spherevista360'),
                'connection_error' => __('Connection error. Please try again.', 'spherevista360')
            )
        ));

        // Enqueue newsletter styles
        wp_enqueue_style(
            'spherevista360-newsletter',
            SphereVista360_Newsletter_Config::get_asset_url('css/newsletter.css'),
            array(),
            SphereVista360_Newsletter_Config::get_version()
        );
    }

    /**
     * Check if assets should be enqueued
     */
    private static function should_enqueue_assets() {
        // Always enqueue on single posts and pages
        if (is_single() || is_page()) {
            return true;
        }

        // Check if footer newsletter is enabled
        $show_footer = get_option('spherevista360_show_footer_newsletter', 'yes');
        if ($show_footer === 'yes' && (is_home() || is_front_page())) {
            return true;
        }

        // Allow themes/plugins to force enqueue
        return apply_filters('spherevista360_enqueue_newsletter_assets', false);
    }

    /**
     * Get current URL for tracking
     */
    private static function get_current_url() {
        if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') {
            $protocol = 'https://';
        } else {
            $protocol = 'http://';
        }

        $host = $_SERVER['HTTP_HOST'] ?? 'localhost';
        $uri = $_SERVER['REQUEST_URI'] ?? '/';

        return esc_url($protocol . $host . $uri);
    }

    /**
     * Add inline styles as fallback
     */
    public static function add_inline_styles() {
        // Only add inline styles if external CSS file doesn't exist
        $css_file = SphereVista360_Newsletter_Config::get_asset_path('css/newsletter.css');
        if (!file_exists($css_file)) {
            self::output_inline_styles();
        }
    }

    /**
     * Output inline CSS styles
     */
    private static function output_inline_styles() {
        ob_start();
        ?>
        <style>
        .newsletter-signup {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 30px;
            margin: 30px 0;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .newsletter-signup.newsletter-footer {
            margin: 40px 0 20px 0;
            padding: 25px;
        }

        .newsletter-header h3 {
            margin: 0 0 10px 0;
            font-size: 24px;
            font-weight: 600;
        }

        .newsletter-header p {
            margin: 0 0 20px 0;
            opacity: 0.9;
            font-size: 16px;
            line-height: 1.5;
        }

        .newsletter-form {
            max-width: 500px;
        }

        .form-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }

        .newsletter-email {
            flex: 1;
            padding: 12px 16px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            background: rgba(255,255,255,0.9);
            color: #333;
        }

        .newsletter-email:focus {
            outline: none;
            box-shadow: 0 0 0 2px rgba(255,255,255,0.5);
        }

        .newsletter-submit {
            padding: 12px 24px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .newsletter-submit:hover:not(:disabled) {
            background: #ff5252;
        }

        .newsletter-submit:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }

        .newsletter-message {
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .newsletter-message.success {
            background: rgba(46, 204, 113, 0.2);
            color: #27ae60;
            border: 1px solid rgba(46, 204, 113, 0.3);
        }

        .newsletter-message.error {
            background: rgba(231, 76, 60, 0.2);
            color: #e74c3c;
            border: 1px solid rgba(231, 76, 60, 0.3);
        }

        .newsletter-privacy {
            opacity: 0.8;
        }

        .newsletter-privacy small {
            font-size: 12px;
        }

        @media (max-width: 768px) {
            .newsletter-signup {
                padding: 20px;
                margin: 20px 0;
            }

            .newsletter-header h3 {
                font-size: 20px;
            }

            .form-group {
                flex-direction: column;
            }

            .newsletter-submit {
                width: 100%;
            }
        }
        </style>
        <?php
        echo ob_get_clean();
    }
}