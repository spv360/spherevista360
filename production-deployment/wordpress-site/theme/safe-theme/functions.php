<?php
/**
 * Functions and definitions
 */

function spherevista360_safe_setup() {
    // Add theme support
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'automatic-feed-links' );
    add_theme_support( 'html5', array( 'comment-list', 'comment-form', 'search-form' ) );
}
add_action( 'after_setup_theme', 'spherevista360_safe_setup' );

function spherevista360_safe_scripts() {
    wp_enqueue_style( 'spherevista360-safe-style', get_stylesheet_uri(), array(), '1.0' );
}
add_action( 'wp_enqueue_scripts', 'spherevista360_safe_scripts' );

// AdSense Ad Units
function spherevista360_header_ad() {
    if ( ! is_single() ) return; // Only show on single posts for now
    ?>
    <div class="adsense-header-ad" style="text-align: center; margin: 20px 0; min-height: 90px;">
        <!-- SphereVista360 Header Leaderboard Ad -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-1542284739923981"
             data-ad-slot="1234567890"
             data-ad-format="horizontal"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    <?php
}

function spherevista360_content_top_ad() {
    if ( ! is_single() ) return;
    ?>
    <div class="adsense-content-top-ad" style="text-align: center; margin: 20px 0; min-height: 250px;">
        <!-- SphereVista360 Content Top Rectangle -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-1542284739923981"
             data-ad-slot="1234567891"
             data-ad-format="rectangle"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    <?php
}

function spherevista360_in_content_ad() {
    if ( ! is_single() ) return;
    ?>
    <div class="adsense-in-content-ad" style="text-align: center; margin: 20px 0; min-height: 250px;">
        <!-- SphereVista360 In-Content Medium Rectangle -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-1542284739923981"
             data-ad-slot="1234567892"
             data-ad-format="rectangle"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    <?php
}

function spherevista360_footer_ad() {
    if ( ! is_single() ) return;
    ?>
    <div class="adsense-footer-ad" style="text-align: center; margin: 20px 0; min-height: 90px;">
        <!-- SphereVista360 Footer Banner -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-1542284739923981"
             data-ad-slot="1234567893"
             data-ad-format="horizontal"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    <?php
}

// Insert in-content ad after first paragraph
function spherevista360_insert_in_content_ad( $content ) {
    if ( ! is_single() ) return $content;

    // Find first paragraph
    $paragraph_pos = strpos( $content, '<p>' );

    if ( $paragraph_pos !== false ) {
        // Find end of first paragraph
        $end_paragraph_pos = strpos( $content, '</p>', $paragraph_pos );

        if ( $end_paragraph_pos !== false ) {
            $end_paragraph_pos += 4; // Include </p>

            // Insert ad after first paragraph
            $ad_code = '<div class="adsense-in-content-ad" style="text-align: center; margin: 20px 0; min-height: 250px;">
                <!-- SphereVista360 In-Content Medium Rectangle -->
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-1542284739923981"
                     data-ad-slot="1234567892"
                     data-ad-format="rectangle"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({});
                </script>
            </div>';

            $content = substr_replace( $content, $ad_code, $end_paragraph_pos, 0 );
        }
    }

    return $content;
}
add_filter( 'the_content', 'spherevista360_insert_in_content_ad' );

// Newsletter signup form for posts
function spherevista360_newsletter_signup() {
    if ( ! is_single() ) return;

    ob_start();
    ?>
    <div class="newsletter-signup-post" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin: 30px 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h3 style="margin-top: 0; font-size: 1.5rem; font-weight: 600;">🚀 Stay Ahead of Tech Trends</h3>
        <p style="margin: 15px 0 25px 0; font-size: 1.1rem; opacity: 0.9;">Get weekly insights on AI, finance, and innovation delivered to your inbox. Join 500+ tech professionals!</p>

        <form id="post-newsletter-form" method="post" style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; max-width: 500px; margin: 0 auto;">
            <input type="email" name="email" id="post-email" placeholder="Enter your email address" required
                   style="flex: 1; min-width: 250px; padding: 12px 16px; border: none; border-radius: 6px; font-size: 16px;">
            <input type="submit" value="Subscribe Now"
                   style="background: #ff6b6b; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.3s;">
        </form>
        <div id="post-newsletter-message" style="margin-top: 15px; font-size: 14px;"></div>
        <p style="font-size: 0.9rem; margin-top: 15px; opacity: 0.8;">No spam, unsubscribe anytime. View our <a href="/privacy-policy" style="color: #ff6b6b; text-decoration: underline;">Privacy Policy</a>.</p>
    </div>

    <script>
    jQuery(document).ready(function($) {
        $('#post-newsletter-form').on('submit', function(e) {
            e.preventDefault();

            var email = $('#post-email').val();
            var submitBtn = $(this).find('input[type="submit"]');
            var messageDiv = $('#post-newsletter-message');

            // Disable button and show loading
            submitBtn.prop('disabled', true).val('Subscribing...');
            messageDiv.html('<span style="color: #ffffff;">Sending confirmation email...</span>');

            // AJAX request
            $.ajax({
                url: '<?php echo admin_url('admin-ajax.php'); ?>',
                type: 'POST',
                data: {
                    action: 'spherevista360_newsletter_signup',
                    email: email,
                    nonce: '<?php echo wp_create_nonce('newsletter_signup_nonce'); ?>'
                },
                success: function(response) {
                    if (response.success) {
                        messageDiv.html('<span style="color: #ffffff;">' + response.data.message + '</span>');
                        $('#post-email').val('');
                    } else {
                        messageDiv.html('<span style="color: #ff6b6b;">' + response.data.message + '</span>');
                    }
                },
                error: function() {
                    messageDiv.html('<span style="color: #ff6b6b;">Connection error. Please try again.</span>');
                },
                complete: function() {
                    submitBtn.prop('disabled', false).val('Subscribe Now');
                }
            });
        });
    });
    </script>
    <?php
    return ob_get_clean();
}

// Newsletter signup for footer
function spherevista360_footer_newsletter() {
    ob_start();
    ?>
    <div class="newsletter-signup-footer" style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; border: 1px solid #e9ecef;">
        <h4 style="margin-top: 0; color: #333; font-size: 1.2rem;">📧 Weekly Tech Digest</h4>
        <p style="margin: 10px 0 15px 0; color: #666; font-size: 0.95rem;">Get the latest in AI, finance, and innovation</p>

        <form id="footer-newsletter-form" method="post" style="display: flex; gap: 8px; max-width: 400px; margin: 0 auto; flex-wrap: wrap;">
            <input type="email" name="email" id="footer-email" placeholder="Your email" required
                   style="flex: 1; min-width: 200px; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;">
            <input type="submit" value="Subscribe"
                   style="background: #0073aa; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: 500; cursor: pointer;">
        </form>
        <div id="footer-newsletter-message" style="margin-top: 10px; font-size: 14px;"></div>
    </div>

    <script>
    jQuery(document).ready(function($) {
        $('#footer-newsletter-form').on('submit', function(e) {
            e.preventDefault();

            var email = $('#footer-email').val();
            var submitBtn = $(this).find('input[type="submit"]');
            var messageDiv = $('#footer-newsletter-message');

            // Disable button and show loading
            submitBtn.prop('disabled', true).val('Subscribing...');
            messageDiv.html('<span style="color: #0073aa;">Sending confirmation email...</span>');

            // AJAX request
            $.ajax({
                url: '<?php echo admin_url('admin-ajax.php'); ?>',
                type: 'POST',
                data: {
                    action: 'spherevista360_newsletter_signup',
                    email: email,
                    nonce: '<?php echo wp_create_nonce('newsletter_signup_nonce'); ?>'
                },
                success: function(response) {
                    if (response.success) {
                        messageDiv.html('<span style="color: #28a745;">' + response.data.message + '</span>');
                        $('#footer-email').val('');
                    } else {
                        messageDiv.html('<span style="color: #dc3545;">' + response.data.message + '</span>');
                    }
                },
                error: function() {
                    messageDiv.html('<span style="color: #dc3545;">Connection error. Please try again.</span>');
                },
                complete: function() {
                    submitBtn.prop('disabled', false).val('Subscribe');
                }
            });
        });
    });
    </script>
    <?php
    return ob_get_clean();
}

// AJAX handler for newsletter signup
function spherevista360_newsletter_signup_ajax() {
    // Verify nonce for security
    if (!wp_verify_nonce($_POST['nonce'], 'newsletter_signup_nonce')) {
        wp_send_json_error(array('message' => 'Security check failed.'));
        return;
    }

    $email = sanitize_email($_POST['email']);

    // Validate email
    if (!is_email($email)) {
        wp_send_json_error(array('message' => 'Please enter a valid email address.'));
        return;
    }

    // Mailchimp API integration
    $api_key = 'YOUR_MAILCHIMP_API_KEY_HERE'; // 🔴 REPLACE WITH YOUR ACTUAL API KEY
    $list_id = 'bbb4f96a8b'; // Your audience ID

    // Extract datacenter from API key (part after last dash)
    $api_key_parts = explode('-', $api_key);
    $datacenter = end($api_key_parts);

    if (empty($api_key) || $api_key === 'YOUR_MAILCHIMP_API_KEY_HERE') {
        wp_send_json_error(array('message' => 'Newsletter signup is not configured yet. Please contact site administrator.'));
        return;
    }

    // Prepare Mailchimp API call
    $url = "https://{$datacenter}.api.mailchimp.com/3.0/lists/{$list_id}/members/";

    $data = array(
        'email_address' => $email,
        'status' => 'pending', // Double opt-in: sends confirmation email
        'merge_fields' => array(
            'FNAME' => '',
            'LNAME' => ''
        )
    );

    $json_data = json_encode($data);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json',
        'Authorization: Bearer ' . $api_key
    ));
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code == 200) {
        // Success - subscriber added (pending confirmation)
        wp_send_json_success(array('message' => 'Thanks! Please check your email to confirm your subscription.'));
    } else {
        $response_data = json_decode($response, true);
        if (isset($response_data['title']) && $response_data['title'] == 'Member Exists') {
            wp_send_json_error(array('message' => 'This email is already subscribed to our newsletter.'));
        } else {
            wp_send_json_error(array('message' => 'Something went wrong. Please try again later.'));
        }
    }
}
add_action('wp_ajax_spherevista360_newsletter_signup', 'spherevista360_newsletter_signup_ajax');
add_action('wp_ajax_nopriv_spherevista360_newsletter_signup', 'spherevista360_newsletter_signup_ajax');
