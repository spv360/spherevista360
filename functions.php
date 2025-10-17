<?php
/**
 * SphereVista360 Newsletter Integration for Kadence Theme
 * Add these functions to your existing Kadence functions.php file
 * Do NOT replace the entire functions.php - just add these functions
 */

// Enqueue newsletter scripts and styles
function spherevista360_enqueue_newsletter_assets() {
    wp_enqueue_script('jquery');

    wp_enqueue_script(
        'spherevista360-newsletter',
        get_template_directory_uri() . '/js/newsletter.js',
        array('jquery'),
        '1.0.0',
        true
    );

    wp_localize_script('spherevista360-newsletter', 'spherevista360_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('spherevista360_newsletter_nonce')
    ));

    wp_enqueue_style(
        'spherevista360-newsletter',
        get_template_directory_uri() . '/css/newsletter.css',
        array(),
        '1.0.0'
    );
}
add_action('wp_enqueue_scripts', 'spherevista360_enqueue_newsletter_assets');

// AJAX handler for newsletter signup
function spherevista360_newsletter_signup_ajax() {
    // Verify nonce for security
    if (!wp_verify_nonce($_POST['nonce'], 'spherevista360_newsletter_nonce')) {
        wp_die(json_encode(array(
            'success' => false,
            'message' => 'Security check failed. Please refresh and try again.'
        )));
    }

    // Sanitize email
    $email = sanitize_email($_POST['email']);
    if (!is_email($email)) {
        wp_die(json_encode(array(
            'success' => false,
            'message' => 'Please enter a valid email address.'
        )));
    }

    // Mailchimp API configuration
    $api_key = 'YOUR_MAILCHIMP_API_KEY_HERE'; // Replace with your actual API key
    $audience_id = 'bbb4f96a8b'; // Your audience ID

    if (empty($api_key) || $api_key === 'YOUR_MAILCHIMP_API_KEY_HERE') {
        wp_die(json_encode(array(
            'success' => false,
            'message' => 'Newsletter service is not configured yet. Please contact the administrator.'
        )));
    }

    // Extract datacenter from API key
    $datacenter = substr($api_key, strpos($api_key, '-') + 1);

    // Mailchimp API URL
    $url = 'https://' . $datacenter . '.api.mailchimp.com/3.0/lists/' . $audience_id . '/members/';

    // Prepare subscriber data
    $subscriber_data = array(
        'email_address' => $email,
        'status' => 'pending', // Double opt-in
        'merge_fields' => array(
            'SIGNUP_SRC' => 'wordpress_site'
        )
    );

    // Setup cURL request
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_USERPWD, 'user:' . $api_key);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($subscriber_data));

    // Execute request
    $result = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // Handle response
    if ($http_code === 200) {
        // Success - already subscribed or newly subscribed
        wp_die(json_encode(array(
            'success' => true,
            'message' => 'Thanks! Please check your email and click the confirmation link to complete your subscription.'
        )));
    } elseif ($http_code === 400) {
        // Bad request - check for specific errors
        $response_data = json_decode($result, true);
        if (isset($response_data['title']) && $response_data['title'] === 'Member Exists') {
            wp_die(json_encode(array(
                'success' => false,
                'message' => 'This email is already subscribed to our newsletter.'
            )));
        } else {
            wp_die(json_encode(array(
                'success' => false,
                'message' => 'There was an error with your subscription. Please try again.'
            )));
        }
    } else {
        // Other errors
        wp_die(json_encode(array(
            'success' => false,
            'message' => 'Unable to process your request right now. Please try again later.'
        )));
    }
}
add_action('wp_ajax_nopriv_spherevista360_newsletter_signup', 'spherevista360_newsletter_signup_ajax');
add_action('wp_ajax_spherevista360_newsletter_signup', 'spherevista360_newsletter_signup_ajax');

// Generate newsletter signup form
function spherevista360_newsletter_signup($context = 'post') {
    $form_id = 'newsletter-' . $context . '-' . uniqid();
    $context_class = 'newsletter-' . $context;

    ob_start();
    ?>
    <div class="newsletter-signup <?php echo esc_attr($context_class); ?>">
        <div class="newsletter-header">
            <h3>Stay Updated with SphereVista360</h3>
            <p>Get the latest insights on 360° photography, virtual tours, and immersive experiences delivered to your inbox.</p>
        </div>

        <form id="<?php echo esc_attr($form_id); ?>" class="newsletter-form" method="post">
            <?php wp_nonce_field('spherevista360_newsletter_nonce', 'newsletter_nonce'); ?>
            <div class="form-group">
                <input type="email"
                       name="email"
                       placeholder="Enter your email address"
                       required
                       class="newsletter-email">
                <button type="submit" class="newsletter-submit">
                    <span class="submit-text">Subscribe</span>
                    <span class="loading-text" style="display: none;">Subscribing...</span>
                </button>
            </div>
            <div class="newsletter-message" style="display: none;"></div>
            <div class="newsletter-privacy">
                <small>We respect your privacy. Unsubscribe at any time.</small>
            </div>
        </form>
    </div>

    <script>
    jQuery(document).ready(function($) {
        $('#<?php echo esc_js($form_id); ?>').on('submit', function(e) {
            e.preventDefault();

            var $form = $(this);
            var $submitBtn = $form.find('.newsletter-submit');
            var $message = $form.find('.newsletter-message');
            var email = $form.find('input[name="email"]').val();

            // Clear previous messages
            $message.hide().removeClass('success error');

            // Show loading state
            $submitBtn.prop('disabled', true);
            $submitBtn.find('.submit-text').hide();
            $submitBtn.find('.loading-text').show();

            // Send AJAX request
            $.ajax({
                url: spherevista360_ajax.ajax_url,
                type: 'POST',
                data: {
                    action: 'spherevista360_newsletter_signup',
                    email: email,
                    nonce: spherevista360_ajax.nonce
                },
                success: function(response) {
                    var data = JSON.parse(response);

                    if (data.success) {
                        $message.addClass('success').text(data.message).show();
                        $form.find('input[name="email"]').val('');
                    } else {
                        $message.addClass('error').text(data.message).show();
                    }
                },
                error: function() {
                    $message.addClass('error').text('Connection error. Please try again.').show();
                },
                complete: function() {
                    // Reset loading state
                    $submitBtn.prop('disabled', false);
                    $submitBtn.find('.submit-text').show();
                    $submitBtn.find('.loading-text').hide();
                }
            });
        });
    });
    </script>
    <?php
    return ob_get_clean();
}

// Footer newsletter signup
function spherevista360_footer_newsletter() {
    echo spherevista360_newsletter_signup('footer');
}

// Add newsletter after post content
function spherevista360_add_newsletter_after_post($content) {
    if (is_single() && in_the_loop() && is_main_query()) {
        $content .= '<div class="post-newsletter-wrapper">';
        $content .= spherevista360_newsletter_signup('post');
        $content .= '</div>';
    }
    return $content;
}
add_filter('the_content', 'spherevista360_add_newsletter_after_post');

// Add newsletter styles
function spherevista360_newsletter_styles() {
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
}
add_action('wp_head', 'spherevista360_newsletter_styles');

/**
 * IMPORTANT: Add these functions to your existing Kadence functions.php file
 * Do NOT replace the entire file - just append these functions at the end
 * before the closing ?> tag (if it exists)
 */