// SphereVista360 Newsletter JavaScript
// Handles AJAX form submissions and user interactions

jQuery(document).ready(function($) {
    'use strict';

    // Newsletter form submission handler
    $('.newsletter-form').on('submit', function(e) {
        e.preventDefault();

        var $form = $(this);
        var $submitBtn = $form.find('.newsletter-submit');
        var $message = $form.find('.newsletter-message');
        var $emailInput = $form.find('input[name="email"]');
        var email = $emailInput.val().trim();

        // Clear previous messages
        $message.hide().removeClass('success error');

        // Basic email validation
        if (!email || !isValidEmail(email)) {
            $message.addClass('error').text('Please enter a valid email address.').show();
            $emailInput.focus();
            return;
        }

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
                try {
                    var data = JSON.parse(response);

                    if (data.success) {
                        $message.addClass('success').text(data.message).show();
                        $emailInput.val(''); // Clear the form

                        // Optional: Hide form after successful submission
                        setTimeout(function() {
                            $form.slideUp();
                        }, 3000);
                    } else {
                        $message.addClass('error').text(data.message).show();
                    }
                } catch (error) {
                    $message.addClass('error').text('An unexpected error occurred. Please try again.').show();
                }
            },
            error: function(xhr, status, error) {
                var errorMessage = 'Connection error. Please check your internet and try again.';

                if (xhr.status === 403) {
                    errorMessage = 'Security check failed. Please refresh the page and try again.';
                } else if (xhr.status === 500) {
                    errorMessage = 'Server error. Please try again in a few minutes.';
                }

                $message.addClass('error').text(errorMessage).show();
            },
            complete: function() {
                // Reset loading state
                $submitBtn.prop('disabled', false);
                $submitBtn.find('.submit-text').show();
                $submitBtn.find('.loading-text').hide();
            }
        });
    });

    // Email validation helper
    function isValidEmail(email) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Add smooth scrolling for anchor links (optional enhancement)
    $('a[href^="#"]').on('click', function(e) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 500);
        }
    });

    // Add focus/blur effects for better UX
    $('.newsletter-email').on('focus', function() {
        $(this).parent().addClass('focused');
    }).on('blur', function() {
        $(this).parent().removeClass('focused');
    });
});