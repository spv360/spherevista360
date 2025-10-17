<?php
/**
 * SphereVista360 Payments Module
 * Handles subscription payments and revenue processing
 */

namespace SphereVista360\Monetization\Modules\Payments;

use SphereVista360\Monetization\Core\Config;
use SphereVista360\Monetization\Database;

class PaymentsModule {

    private $config;
    private $db;

    public function __construct() {
        $this->config = Config::getInstance();
        $this->db = Database::getInstance();

        if ($this->isStripeEnabled()) {
            $this->initializeStripe();
        }
    }

    public function isActive() {
        return $this->config->get('modules.payments.enabled', false);
    }

    private function isStripeEnabled() {
        return $this->config->get('apis.stripe.secret_key') && $this->config->get('apis.stripe.publishable_key');
    }

    private function initializeStripe() {
        \Stripe\Stripe::setApiKey($this->config->get('apis.stripe.secret_key'));
    }

    /**
     * Create a subscription for a user
     */
    public function createSubscription($user_id, $tier, $payment_method_id) {
        if (!$this->isStripeEnabled()) {
            return new \WP_Error('stripe_not_configured', 'Stripe is not configured');
        }

        try {
            $prices = $this->getTierPrices();
            $price_id = $prices[$tier] ?? null;

            if (!$price_id) {
                return new \WP_Error('invalid_tier', 'Invalid subscription tier');
            }

            // Get or create customer
            $customer = $this->getOrCreateCustomer($user_id);

            // Create subscription
            $subscription = \Stripe\Subscription::create([
                'customer' => $customer->id,
                'items' => [
                    [
                        'price' => $price_id,
                    ],
                ],
                'default_payment_method' => $payment_method_id,
                'expand' => ['latest_invoice.payment_intent'],
            ]);

            // Store subscription data
            $this->storeSubscription($user_id, $subscription, $tier);

            return [
                'subscription_id' => $subscription->id,
                'client_secret' => $subscription->latest_invoice->payment_intent->client_secret,
                'status' => $subscription->status
            ];

        } catch (\Stripe\Exception\ApiErrorException $e) {
            return new \WP_Error('stripe_error', $e->getMessage());
        }
    }

    /**
     * Process Stripe webhook
     */
    public function processWebhook($event) {
        switch ($event->type) {
            case 'invoice.payment_succeeded':
                return $this->handlePaymentSucceeded($event->data->object);
            case 'invoice.payment_failed':
                return $this->handlePaymentFailed($event->data->object);
            case 'customer.subscription.deleted':
                return $this->handleSubscriptionCancelled($event->data->object);
            default:
                return true; // Unhandled event, but not an error
        }
    }

    private function handlePaymentSucceeded($invoice) {
        $subscription_id = $invoice->subscription;
        $amount = $invoice->amount_paid / 100; // Convert from cents

        // Update subscription status
        $this->db->update(
            'payments',
            [
                'status' => 'completed',
                'processed_at' => current_time('mysql')
            ],
            ['subscription_id' => $subscription_id]
        );

        // Update user tier
        $this->updateUserTier($subscription_id);

        // Log revenue
        do_action('spherevista_revenue_generated', [
            'source' => 'subscription',
            'amount' => $amount,
            'currency' => strtoupper($invoice->currency),
            'transaction_id' => $invoice->id,
            'subscription_id' => $subscription_id
        ]);

        return true;
    }

    private function handlePaymentFailed($invoice) {
        $subscription_id = $invoice->subscription;

        $this->db->update(
            'payments',
            ['status' => 'failed'],
            ['subscription_id' => $subscription_id]
        );

        // Notify user of payment failure
        $this->notifyPaymentFailure($subscription_id);

        return true;
    }

    private function handleSubscriptionCancelled($subscription) {
        // Update user tier to free
        $user_id = $this->getUserIdFromSubscription($subscription->id);
        if ($user_id) {
            update_user_meta($user_id, 'spherevista360_tier', 'free');
        }

        return true;
    }

    /**
     * Get pricing for different tiers
     */
    private function getTierPrices() {
        return [
            'free' => null, // No payment required
            'pro' => $this->config->get('pricing.pro.price_id'),
            'enterprise' => $this->config->get('pricing.enterprise.price_id')
        ];
    }

    /**
     * Get or create Stripe customer
     */
    private function getOrCreateCustomer($user_id) {
        $user = get_userdata($user_id);
        $customer_id = get_user_meta($user_id, 'stripe_customer_id', true);

        if ($customer_id) {
            return \Stripe\Customer::retrieve($customer_id);
        }

        $customer = \Stripe\Customer::create([
            'email' => $user->user_email,
            'name' => $user->display_name,
            'metadata' => [
                'user_id' => $user_id,
                'platform' => 'spherevista360'
            ]
        ]);

        update_user_meta($user_id, 'stripe_customer_id', $customer->id);

        return $customer;
    }

    /**
     * Store subscription data in database
     */
    private function storeSubscription($user_id, $subscription, $tier) {
        $this->db->insert('payments', [
            'user_id' => $user_id,
            'subscription_id' => $subscription->id,
            'payment_method' => 'stripe',
            'transaction_id' => $subscription->latest_invoice->id,
            'amount' => $subscription->latest_invoice->amount_paid / 100,
            'currency' => strtoupper($subscription->latest_invoice->currency),
            'status' => 'pending',
            'payment_type' => 'subscription',
            'tier' => $tier,
            'billing_period' => 'monthly'
        ]);
    }

    /**
     * Update user tier based on active subscription
     */
    private function updateUserTier($subscription_id) {
        $payment = $this->db->getRow('payments', ['subscription_id' => $subscription_id]);

        if ($payment) {
            update_user_meta($payment->user_id, 'spherevista360_tier', $payment->tier);
        }
    }

    /**
     * Get user ID from subscription ID
     */
    private function getUserIdFromSubscription($subscription_id) {
        $payment = $this->db->getRow('payments', ['subscription_id' => $subscription_id]);
        return $payment ? $payment->user_id : null;
    }

    /**
     * Send payment failure notification
     */
    private function notifyPaymentFailure($subscription_id) {
        $user_id = $this->getUserIdFromSubscription($subscription_id);

        if ($user_id) {
            $user = get_userdata($user_id);

            wp_mail(
                $user->user_email,
                'Payment Failed - SphereVista360',
                "Your recent payment for SphereVista360 subscription failed. Please update your payment method to continue using premium features."
            );
        }
    }

    /**
     * Get subscription details for user
     */
    public function getUserSubscription($user_id) {
        return $this->db->getRow('payments', [
            'user_id' => $user_id,
            'payment_type' => 'subscription',
            'status' => 'completed'
        ], ARRAY_A);
    }

    /**
     * Cancel user subscription
     */
    public function cancelSubscription($user_id) {
        $subscription = $this->getUserSubscription($user_id);

        if (!$subscription) {
            return new \WP_Error('no_subscription', 'No active subscription found');
        }

        try {
            $stripe_subscription = \Stripe\Subscription::retrieve($subscription['subscription_id']);
            $stripe_subscription->cancel();

            return true;
        } catch (\Stripe\Exception\ApiErrorException $e) {
            return new \WP_Error('stripe_error', $e->getMessage());
        }
    }
}