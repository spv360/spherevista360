/**
 * SphereVista360 Newsletter Frontend JavaScript
 *
 * Handles form submission and user interactions
 */

(function($) {
    'use strict';

    class NewsletterForm {
        constructor(form) {
            this.form = $(form);
            this.submitBtn = this.form.find('.newsletter-submit');
            this.messageDiv = this.form.find('.newsletter-message');
            this.emailInput = this.form.find('input[name="email"]');
            this.context = this.form.data('context') || 'unknown';

            this.bindEvents();
        }

        bindEvents() {
            this.form.on('submit', (e) => this.handleSubmit(e));
            this.emailInput.on('input', () => this.clearMessages());
        }

        handleSubmit(e) {
            e.preventDefault();

            const email = this.emailInput.val().trim();

            if (!this.validateEmail(email)) {
                this.showMessage('Please enter a valid email address.', 'error');
                return;
            }

            this.setLoadingState(true);
            this.clearMessages();

            this.submitForm(email)
                .done((response) => this.handleSuccess(response))
                .fail(() => this.handleError())
                .always(() => this.setLoadingState(false));
        }

        submitForm(email) {
            return $.ajax({
                url: spherevista360_newsletter.ajax_url,
                type: 'POST',
                data: {
                    action: 'spherevista360_newsletter_signup',
                    email: email,
                    context: this.context,
                    current_url: window.location.href,
                    nonce: spherevista360_newsletter.nonce
                }
            });
        }

        handleSuccess(response) {
            try {
                const data = typeof response === 'string' ? JSON.parse(response) : response;

                if (data.success) {
                    this.showMessage(data.message, 'success');
                    this.emailInput.val('');
                    this.trackConversion(data);
                } else {
                    this.showMessage(data.message, 'error');
                }
            } catch (e) {
                this.showMessage('An unexpected error occurred. Please try again.', 'error');
            }
        }

        handleError() {
            this.showMessage(spherevista360_newsletter.strings.connection_error, 'error');
        }

        validateEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        showMessage(message, type) {
            this.messageDiv
                .removeClass('success error')
                .addClass(type)
                .text(message)
                .show();

            // Auto-hide success messages after 5 seconds
            if (type === 'success') {
                setTimeout(() => {
                    this.messageDiv.fadeOut();
                }, 5000);
            }
        }

        clearMessages() {
            this.messageDiv.hide().removeClass('success error');
        }

        setLoadingState(loading) {
            this.submitBtn.prop('disabled', loading);

            const submitText = this.submitBtn.find('.submit-text');
            const loadingText = this.submitBtn.find('.loading-text');

            if (loading) {
                submitText.hide();
                loadingText.show();
            } else {
                loadingText.hide();
                submitText.show();
            }
        }

        trackConversion(data) {
            // Track conversion if Google Analytics is available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'newsletter_signup', {
                    event_category: 'engagement',
                    event_label: this.context,
                    value: 1
                });
            }

            // Track with Facebook Pixel if available
            if (typeof fbq !== 'undefined') {
                fbq('track', 'Lead', {
                    content_name: 'Newsletter Signup',
                    content_category: this.context
                });
            }
        }
    }

    // Initialize forms when DOM is ready
    $(document).ready(function() {
        $('.newsletter-form').each(function() {
            new NewsletterForm(this);
        });
    });

    // Re-initialize forms after AJAX content loads (for infinite scroll, etc.)
    $(document).on('newsletter_forms_loaded', function() {
        $('.newsletter-form').each(function() {
            if (!$(this).data('newsletter-initialized')) {
                new NewsletterForm(this);
                $(this).data('newsletter-initialized', true);
            }
        });
    });

})(jQuery);