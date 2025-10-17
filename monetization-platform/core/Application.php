<?php
/**
 * SphereVista360 Core Application Class
 */

namespace SphereVista360\Monetization\Core;

class Application {

    private $config;
    private $database;
    private $modules = [];

    public function __construct() {
        $this->config = Config::getInstance();
        $this->database = Database::getInstance();
    }

    public function getConfig() {
        return $this->config;
    }

    public function getDatabase() {
        return $this->database;
    }

    public function registerModule($name, $module) {
        $this->modules[$name] = $module;
    }

    public function getModule($name) {
        return isset($this->modules[$name]) ? $this->modules[$name] : null;
    }

    public function getAllModules() {
        return $this->modules;
    }

    public function isModuleActive($name) {
        $module = $this->getModule($name);
        return $module && $module->isActive();
    }

    public function getVersion() {
        return '1.0.0';
    }

    public function getUserTier() {
        $user_id = get_current_user_id();
        return get_user_meta($user_id, 'spherevista360_tier', true) ?: 'free';
    }

    public function canAccessFeature($feature) {
        $tier = $this->getUserTier();
        $tier_limits = $this->config->get('tier_limits');

        return isset($tier_limits[$tier][$feature]) && $tier_limits[$tier][$feature];
    }

    public function logActivity($action, $data = []) {
        $log_data = array_merge($data, [
            'user_id' => get_current_user_id(),
            'timestamp' => current_time('mysql'),
            'action' => $action,
            'ip' => $this->getClientIP()
        ]);

        $this->database->insert('spherevista360_activity_log', $log_data);
    }

    private function getClientIP() {
        $ip_headers = ['HTTP_CF_CONNECTING_IP', 'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'];

        foreach ($ip_headers as $header) {
            if (!empty($_SERVER[$header])) {
                $ip = $_SERVER[$header];
                if ($header === 'HTTP_X_FORWARDED_FOR') {
                    $ip = explode(',', $ip)[0];
                }
                return filter_var($ip, FILTER_VALIDATE_IP) ? $ip : 'unknown';
            }
        }

        return 'unknown';
    }
}