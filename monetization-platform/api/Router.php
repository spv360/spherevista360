<?php
/**
 * SphereVista360 REST API Router
 */

namespace SphereVista360\Monetization\API;

use WP_REST_Controller;
use WP_REST_Server;
use WP_Error;

class Router extends WP_REST_Controller {

    public function __construct() {
        $this->namespace = 'spherevista360/v1';
    }

    public function registerRoutes() {
        add_action('rest_api_init', [$this, 'registerApiRoutes']);
    }

    public function registerApiRoutes() {
        // Analytics endpoints
        register_rest_route($this->namespace, '/analytics/revenue', [
            'methods' => WP_REST_Server::READABLE,
            'callback' => [$this, 'getRevenueAnalytics'],
            'permission_callback' => [$this, 'checkAnalyticsPermission'],
            'args' => $this->getAnalyticsArgs()
        ]);

        // Sites management
        register_rest_route($this->namespace, '/sites', [
            'methods' => WP_REST_Server::READABLE,
            'callback' => [$this, 'getSites'],
            'permission_callback' => [$this, 'checkSitesPermission']
        ]);

        register_rest_route($this->namespace, '/sites', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'createSite'],
            'permission_callback' => [$this, 'checkSitesPermission'],
            'args' => $this->getSiteArgs()
        ]);

        // Subscribers management
        register_rest_route($this->namespace, '/subscribers', [
            'methods' => WP_REST_Server::READABLE,
            'callback' => [$this, 'getSubscribers'],
            'permission_callback' => [$this, 'checkSubscribersPermission'],
            'args' => $this->getSubscribersArgs()
        ]);

        register_rest_route($this->namespace, '/subscribers/(?P<id>\d+)', [
            'methods' => WP_REST_Server::EDITABLE,
            'callback' => [$this, 'updateSubscriber'],
            'permission_callback' => [$this, 'checkSubscribersPermission'],
            'args' => $this->getSubscriberUpdateArgs()
        ]);

        // Automation endpoints
        register_rest_route($this->namespace, '/automation/tasks', [
            'methods' => WP_REST_Server::READABLE,
            'callback' => [$this, 'getAutomationTasks'],
            'permission_callback' => [$this, 'checkAutomationPermission']
        ]);

        register_rest_route($this->namespace, '/automation/tasks', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'createAutomationTask'],
            'permission_callback' => [$this, 'checkAutomationPermission'],
            'args' => $this->getAutomationArgs()
        ]);

        // Webhook endpoints for external services
        register_rest_route($this->namespace, '/webhooks/stripe', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handleStripeWebhook'],
            'permission_callback' => '__return_true' // Webhooks need public access
        ]);

        register_rest_route($this->namespace, '/webhooks/mailchimp', [
            'methods' => WP_REST_Server::CREATABLE,
            'callback' => [$this, 'handleMailchimpWebhook'],
            'permission_callback' => '__return_true'
        ]);
    }

    // Analytics endpoints
    public function getRevenueAnalytics($request) {
        $user_id = get_current_user_id();
        $period = $request->get_param('period') ?: '30d';
        $source = $request->get_param('source');

        $analytics = new \SphereVista360\Modules\Analytics\AnalyticsModule();
        $data = $analytics->getRevenueData($user_id, $period, $source);

        return new \WP_REST_Response($data, 200);
    }

    // Sites management
    public function getSites($request) {
        $user_id = get_current_user_id();
        $status = $request->get_param('status') ?: 'active';

        $sites = \SphereVista360\Monetization\Database::getInstance()->getResults(
            'sites',
            ['user_id' => $user_id, 'status' => $status]
        );

        return new \WP_REST_Response($sites, 200);
    }

    public function createSite($request) {
        $user_id = get_current_user_id();
        $site_data = [
            'user_id' => $user_id,
            'site_url' => $request->get_param('site_url'),
            'site_name' => $request->get_param('site_name'),
            'platform' => $request->get_param('platform') ?: 'wordpress',
            'adsense_publisher_id' => $request->get_param('adsense_publisher_id'),
            'analytics_tracking_id' => $request->get_param('analytics_tracking_id'),
            'tier' => $request->get_param('tier') ?: 'free'
        ];

        $db = \SphereVista360\Monetization\Database::getInstance();
        $result = $db->insert('sites', $site_data);

        if ($result) {
            $site_data['id'] = $db->getWpdb()->insert_id;
            return new \WP_REST_Response($site_data, 201);
        }

        return new WP_Error('site_creation_failed', 'Failed to create site', ['status' => 500]);
    }

    // Subscribers management
    public function getSubscribers($request) {
        $user_id = get_current_user_id();
        $site_id = $request->get_param('site_id');
        $status = $request->get_param('status') ?: 'active';
        $limit = min($request->get_param('limit') ?: 50, 1000);

        $where = ['user_id' => $user_id, 'status' => $status];
        if ($site_id) {
            $where['site_id'] = $site_id;
        }

        $subscribers = \SphereVista360\Monetization\Database::getInstance()->getResults('subscribers', $where);

        return new \WP_REST_Response(array_slice($subscribers, 0, $limit), 200);
    }

    public function updateSubscriber($request) {
        $subscriber_id = $request->get_param('id');
        $user_id = get_current_user_id();

        // Verify ownership
        $subscriber = \SphereVista360\Monetization\Database::getInstance()->getRow(
            'subscribers',
            ['id' => $subscriber_id, 'user_id' => $user_id]
        );

        if (!$subscriber) {
            return new WP_Error('subscriber_not_found', 'Subscriber not found', ['status' => 404]);
        }

        $update_data = [];
        $allowed_fields = ['first_name', 'last_name', 'status', 'tags'];

        foreach ($allowed_fields as $field) {
            if ($request->has_param($field)) {
                $update_data[$field] = $request->get_param($field);
            }
        }

        if (!empty($update_data)) {
            $result = \SphereVista360\Monetization\Database::getInstance()->update(
                'subscribers',
                $update_data,
                ['id' => $subscriber_id]
            );

            if ($result !== false) {
                return new \WP_REST_Response(['success' => true], 200);
            }
        }

        return new WP_Error('update_failed', 'Failed to update subscriber', ['status' => 500]);
    }

    // Automation endpoints
    public function getAutomationTasks($request) {
        $user_id = get_current_user_id();
        $status = $request->get_param('status') ?: 'active';

        $tasks = \SphereVista360\Monetization\Database::getInstance()->getResults(
            'automation',
            ['user_id' => $user_id, 'status' => $status]
        );

        return new \WP_REST_Response($tasks, 200);
    }

    public function createAutomationTask($request) {
        $user_id = get_current_user_id();
        $task_data = [
            'user_id' => $user_id,
            'site_id' => $request->get_param('site_id'),
            'task_type' => $request->get_param('task_type'),
            'task_name' => $request->get_param('task_name'),
            'schedule' => $request->get_param('schedule'),
            'parameters' => json_encode($request->get_param('parameters') ?: [])
        ];

        $db = \SphereVista360\Monetization\Database::getInstance();
        $result = $db->insert('automation', $task_data);

        if ($result) {
            $task_data['id'] = $db->getWpdb()->insert_id;
            return new \WP_REST_Response($task_data, 201);
        }

        return new WP_Error('task_creation_failed', 'Failed to create automation task', ['status' => 500]);
    }

    // Webhook handlers
    public function handleStripeWebhook($request) {
        $payload = $request->get_body();
        $sig_header = $request->get_header('stripe-signature');

        $webhook_secret = \SphereVista360\Monetization\Core\Config::getInstance()->get('apis.stripe.webhook_secret');

        try {
            $event = \Stripe\Webhook::constructEvent($payload, $sig_header, $webhook_secret);

            $payments_module = new \SphereVista360\Modules\Payments\PaymentsModule();
            $result = $payments_module->processWebhook($event);

            return new \WP_REST_Response(['success' => $result], 200);

        } catch (\Exception $e) {
            return new WP_Error('webhook_error', $e->getMessage(), ['status' => 400]);
        }
    }

    public function handleMailchimpWebhook($request) {
        // Verify webhook signature if configured
        $newsletter_module = new \SphereVista360\Modules\Newsletter\NewsletterModule();
        $result = $newsletter_module->processWebhook($request->get_params());

        return new \WP_REST_Response(['success' => $result], 200);
    }

    // Permission callbacks
    public function checkAnalyticsPermission() {
        return current_user_can('manage_options');
    }

    public function checkSitesPermission() {
        return current_user_can('manage_options');
    }

    public function checkSubscribersPermission() {
        return current_user_can('manage_options');
    }

    public function checkAutomationPermission() {
        return current_user_can('manage_options');
    }

    // Argument definitions
    private function getAnalyticsArgs() {
        return [
            'period' => [
                'type' => 'string',
                'enum' => ['7d', '30d', '90d', '1y'],
                'default' => '30d'
            ],
            'source' => [
                'type' => 'string',
                'enum' => ['adsense', 'affiliate', 'sponsorship', 'all'],
                'default' => 'all'
            ]
        ];
    }

    private function getSiteArgs() {
        return [
            'site_url' => [
                'type' => 'string',
                'format' => 'uri',
                'required' => true
            ],
            'site_name' => [
                'type' => 'string',
                'required' => true
            ],
            'platform' => [
                'type' => 'string',
                'enum' => ['wordpress', 'custom'],
                'default' => 'wordpress'
            ],
            'adsense_publisher_id' => [
                'type' => 'string'
            ],
            'analytics_tracking_id' => [
                'type' => 'string'
            ],
            'tier' => [
                'type' => 'string',
                'enum' => ['free', 'pro', 'enterprise'],
                'default' => 'free'
            ]
        ];
    }

    private function getSubscribersArgs() {
        return [
            'site_id' => [
                'type' => 'integer'
            ],
            'status' => [
                'type' => 'string',
                'enum' => ['active', 'unsubscribed', 'bounced'],
                'default' => 'active'
            ],
            'limit' => [
                'type' => 'integer',
                'minimum' => 1,
                'maximum' => 1000,
                'default' => 50
            ]
        ];
    }

    private function getSubscriberUpdateArgs() {
        return [
            'first_name' => ['type' => 'string'],
            'last_name' => ['type' => 'string'],
            'status' => [
                'type' => 'string',
                'enum' => ['active', 'unsubscribed', 'bounced']
            ],
            'tags' => ['type' => 'string']
        ];
    }

    private function getAutomationArgs() {
        return [
            'site_id' => ['type' => 'integer'],
            'task_type' => [
                'type' => 'string',
                'enum' => ['content_publish', 'seo_optimize', 'ad_refresh', 'newsletter_send'],
                'required' => true
            ],
            'task_name' => [
                'type' => 'string',
                'required' => true
            ],
            'schedule' => [
                'type' => 'string',
                'required' => true
            ],
            'parameters' => [
                'type' => 'object',
                'default' => []
            ]
        ];
    }
}