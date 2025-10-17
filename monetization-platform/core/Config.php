<?php
/**
 * SphereVista360 Configuration Management
 */

namespace SphereVista360\Monetization\Core;

class Config {

    private static $instance = null;
    private $config = [];

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->load();
    }

    public static function load() {
        $instance = self::getInstance();
        $instance->config = $instance->loadConfiguration();
    }

    private function loadConfiguration() {
        $defaults = $this->getDefaults();
        $stored = get_option('spherevista360_config', []);

        return array_merge($defaults, $stored);
    }

    public function get($key, $default = null) {
        $keys = explode('.', $key);
        $value = $this->config;

        foreach ($keys as $key_part) {
            if (!isset($value[$key_part])) {
                return $default;
            }
            $value = $value[$key_part];
        }

        return $value;
    }

    public function set($key, $value) {
        $keys = explode('.', $key);
        $config = &$this->config;

        foreach ($keys as $i => $key_part) {
            if ($i === count($keys) - 1) {
                $config[$key_part] = $value;
            } else {
                if (!isset($config[$key_part]) || !is_array($config[$key_part])) {
                    $config[$key_part] = [];
                }
                $config = &$config[$key_part];
            }
        }

        $this->save();
    }

    public function save() {
        update_option('spherevista360_config', $this->config);
    }

    public static function setDefaults() {
        $instance = self::getInstance();
        $defaults = $instance->getDefaults();

        foreach ($defaults as $key => $value) {
            if (!isset($instance->config[$key])) {
                $instance->config[$key] = $value;
            }
        }

        $instance->save();
    }

    private function getDefaults() {
        return [
            'platform' => [
                'name' => 'SphereVista360 Monetization',
                'version' => '1.0.0',
                'description' => 'Complete WordPress monetization toolkit'
            ],

            'modules' => [
                'adsense' => ['enabled' => true, 'auto_optimize' => true],
                'newsletter' => ['enabled' => true, 'double_optin' => true],
                'analytics' => ['enabled' => true, 'track_revenue' => true],
                'seo' => ['enabled' => true, 'auto_optimize' => true],
                'payments' => ['enabled' => true, 'stripe_enabled' => false],
                'automation' => ['enabled' => true, 'scheduled_tasks' => true]
            ],

            'tier_limits' => [
                'free' => [
                    'adsense_sites' => 1,
                    'newsletter_subscribers' => 1000,
                    'monthly_revenue' => 100,
                    'automation_tasks' => 5,
                    'api_calls' => 1000
                ],
                'pro' => [
                    'adsense_sites' => 5,
                    'newsletter_subscribers' => 10000,
                    'monthly_revenue' => 1000,
                    'automation_tasks' => 25,
                    'api_calls' => 10000
                ],
                'enterprise' => [
                    'adsense_sites' => -1, // unlimited
                    'newsletter_subscribers' => -1,
                    'monthly_revenue' => -1,
                    'automation_tasks' => -1,
                    'api_calls' => -1
                ]
            ],

            'apis' => [
                'mailchimp' => [
                    'api_key' => '',
                    'audience_id' => '',
                    'double_optin' => true
                ],
                'stripe' => [
                    'publishable_key' => '',
                    'secret_key' => '',
                    'webhook_secret' => ''
                ],
                'google' => [
                    'adsense_publisher_id' => '',
                    'analytics_tracking_id' => '',
                    'search_console_verification' => ''
                ]
            ],

            'features' => [
                'auto_ad_placement' => true,
                'revenue_tracking' => true,
                'ab_testing' => false,
                'custom_analytics' => true,
                'email_automation' => true,
                'performance_monitoring' => true
            ],

            'security' => [
                'rate_limiting' => true,
                'ip_whitelist' => [],
                'api_key_rotation' => 30, // days
                'audit_log_retention' => 90 // days
            ],

            'performance' => [
                'cache_enabled' => true,
                'cdn_integration' => false,
                'lazy_loading' => true,
                'image_optimization' => true
            ]
        ];
    }

    public function getAll() {
        return $this->config;
    }

    public function reset() {
        $this->config = $this->getDefaults();
        $this->save();
    }
}