<?php
/**
 * SphereVista360 Monetization Manager
 * Coordinates all monetization modules
 */

namespace SphereVista360\Monetization\Modules;

use SphereVista360\Monetization\Core\Application;

class MonetizationManager {

    private static $instance = null;
    private $modules = [];
    private $app;

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->app = Application::getInstance();
        $this->initializeModules();
    }

    private function initializeModules() {
        // Core modules are loaded in Bootstrap
        // This method can be used for dynamic module loading
    }

    public static function registerModule($name, $module) {
        $instance = self::getInstance();
        $instance->modules[$name] = $module;
    }

    public static function getModule($name) {
        $instance = self::getInstance();
        return isset($instance->modules[$name]) ? $instance->modules[$name] : null;
    }

    public function getAllModules() {
        return $this->modules;
    }

    public function getActiveModules() {
        return array_filter($this->modules, function($module) {
            return $module->isActive();
        });
    }

    /**
     * Process revenue event across all relevant modules
     */
    public function processRevenueEvent($event) {
        $event_type = $event['type'] ?? 'unknown';

        // Route to appropriate modules
        switch ($event_type) {
            case 'adsense_impression':
            case 'adsense_click':
                $this->getModule('adsense')?->processAdEvent($event);
                break;

            case 'newsletter_signup':
                $this->getModule('newsletter')?->processSignupEvent($event);
                break;

            case 'subscription_payment':
                $this->getModule('payments')?->processPaymentEvent($event);
                break;

            case 'content_view':
            case 'content_engagement':
                $this->getModule('analytics')?->processContentEvent($event);
                break;
        }

        // Always send to analytics for tracking
        $this->getModule('analytics')?->trackEvent($event);
    }

    /**
     * Get combined revenue data from all modules
     */
    public function getRevenueReport($user_id, $period = '30d') {
        $report = [
            'total_revenue' => 0,
            'breakdown' => [],
            'period' => $period,
            'generated_at' => current_time('mysql')
        ];

        $modules_with_revenue = ['adsense', 'payments', 'analytics'];

        foreach ($modules_with_revenue as $module_name) {
            $module = $this->getModule($module_name);
            if ($module && $module->isActive()) {
                $module_revenue = $module->getRevenueData($user_id, $period);

                if ($module_revenue) {
                    $report['total_revenue'] += $module_revenue['amount'];
                    $report['breakdown'][$module_name] = $module_revenue;
                }
            }
        }

        return $report;
    }

    /**
     * Check if user can perform action based on tier limits
     */
    public function canUserPerformAction($user_id, $action, $context = []) {
        $tier = $this->app->getUserTier();
        $tier_limits = $this->app->getConfig()->get('tier_limits');

        if (!isset($tier_limits[$tier])) {
            return false;
        }

        $limits = $tier_limits[$tier];

        switch ($action) {
            case 'create_site':
                $current_sites = $this->getUserSiteCount($user_id);
                return $current_sites < ($limits['adsense_sites'] ?? 0);

            case 'send_newsletter':
                $current_subscribers = $this->getUserSubscriberCount($user_id);
                return $current_subscribers <= ($limits['newsletter_subscribers'] ?? 0);

            case 'api_call':
                return $this->checkApiRateLimit($user_id, $limits['api_calls'] ?? 1000);

            case 'automation_task':
                $current_tasks = $this->getUserAutomationTaskCount($user_id);
                return $current_tasks < ($limits['automation_tasks'] ?? 5);

            default:
                return isset($limits[$action]) ? $limits[$action] : false;
        }
    }

    /**
     * Get optimization recommendations for user
     */
    public function getOptimizationRecommendations($user_id) {
        $recommendations = [];

        // Check each module for recommendations
        foreach ($this->getActiveModules() as $name => $module) {
            if (method_exists($module, 'getOptimizationRecommendations')) {
                $module_recs = $module->getOptimizationRecommendations($user_id);
                if (!empty($module_recs)) {
                    $recommendations[$name] = $module_recs;
                }
            }
        }

        return $recommendations;
    }

    /**
     * Run automated optimization tasks
     */
    public function runOptimizationTasks($user_id) {
        $results = [];

        foreach ($this->getActiveModules() as $name => $module) {
            if (method_exists($module, 'runOptimization')) {
                $results[$name] = $module->runOptimization($user_id);
            }
        }

        return $results;
    }

    /**
     * Helper methods for user limits
     */
    private function getUserSiteCount($user_id) {
        return $this->app->getDatabase()->getVar(
            'sites',
            'COUNT(*)',
            ['user_id' => $user_id, 'status' => 'active']
        );
    }

    private function getUserSubscriberCount($user_id) {
        return $this->app->getDatabase()->getVar(
            'subscribers',
            'COUNT(*)',
            ['user_id' => $user_id, 'status' => 'active']
        );
    }

    private function getUserAutomationTaskCount($user_id) {
        return $this->app->getDatabase()->getVar(
            'automation',
            'COUNT(*)',
            ['user_id' => $user_id, 'status' => 'active']
        );
    }

    private function checkApiRateLimit($user_id, $limit) {
        $today = date('Y-m-d');
        $calls_today = $this->app->getDatabase()->getVar(
            'activity_log',
            'COUNT(*)',
            [
                'user_id' => $user_id,
                'action' => 'api_call',
                'DATE(created_at)' => $today
            ]
        );

        return $calls_today < $limit;
    }

    /**
     * Export user data for GDPR compliance
     */
    public function exportUserData($user_id) {
        $export_data = [
            'user_info' => get_userdata($user_id)->to_array(),
            'sites' => [],
            'subscribers' => [],
            'revenue' => [],
            'activity' => [],
            'exported_at' => current_time('mysql')
        ];

        // Get data from each table
        $export_data['sites'] = $this->app->getDatabase()->getResults('sites', ['user_id' => $user_id]);
        $export_data['subscribers'] = $this->app->getDatabase()->getResults('subscribers', ['user_id' => $user_id]);
        $export_data['revenue'] = $this->app->getDatabase()->getResults('revenue', ['user_id' => $user_id]);
        $export_data['activity'] = $this->app->getDatabase()->getResults('activity_log', ['user_id' => $user_id]);

        return $export_data;
    }

    /**
     * Delete user data for GDPR compliance
     */
    public function deleteUserData($user_id) {
        $tables = ['sites', 'subscribers', 'revenue', 'activity_log', 'payments', 'automation'];

        foreach ($tables as $table) {
            $this->app->getDatabase()->delete($table, ['user_id' => $user_id]);
        }

        // Cancel any active subscriptions
        $payments_module = $this->getModule('payments');
        if ($payments_module) {
            $payments_module->cancelSubscription($user_id);
        }

        return true;
    }
}