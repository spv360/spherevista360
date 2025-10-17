<?php
/**
 * SphereVista360 Monetization Platform Bootstrap
 *
 * SaaS platform for WordPress monetization with multi-tenant support
 */

namespace SphereVista360\Monetization;

require_once __DIR__ . '/../vendor/autoload.php';

use SphereVista360\Monetization\Core\Application;
use SphereVista360\Monetization\Core\Config;
use SphereVista360\Monetization\Core\Database;
use SphereVista360\Monetization\Modules\MonetizationManager;
use SphereVista360\Monetization\API\Router;
use SphereVista360\Monetization\Dashboard\AdminDashboard;

class Bootstrap {

    private static $instance = null;
    private $app;

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->initialize();
    }

    private function initialize() {
        // Load configuration
        Config::load();

        // Initialize database
        Database::getInstance();

        // Initialize core application
        $this->app = new Application();

        // Register modules
        $this->registerModules();

        // Initialize API
        $this->initializeAPI();

        // Initialize dashboard
        $this->initializeDashboard();

        // Setup hooks and integrations
        $this->setupHooks();
    }

    private function registerModules() {
        $modules = [
            'adsense' => new \SphereVista360\Modules\AdSense\AdSenseModule(),
            'newsletter' => new \SphereVista360\Modules\Newsletter\NewsletterModule(),
            'analytics' => new \SphereVista360\Modules\Analytics\AnalyticsModule(),
            'seo' => new \SphereVista360\Modules\SEO\SEOModule(),
            'payments' => new \SphereVista360\Modules\Payments\PaymentsModule(),
            'automation' => new \SphereVista360\Modules\Automation\AutomationModule()
        ];

        foreach ($modules as $name => $module) {
            MonetizationManager::registerModule($name, $module);
        }
    }

    private function initializeAPI() {
        $router = new Router();
        $router->registerRoutes();
    }

    private function initializeDashboard() {
        if (is_admin()) {
            new AdminDashboard();
        }
    }

    private function setupHooks() {
        // WordPress integration hooks
        add_action('init', [$this, 'wordpressInit']);
        add_action('admin_menu', [$this, 'registerAdminMenus']);
        add_action('wp_enqueue_scripts', [$this, 'enqueueFrontendAssets']);
        add_action('admin_enqueue_scripts', [$this, 'enqueueAdminAssets']);

        // Monetization hooks
        add_action('spherevista_revenue_generated', [$this, 'handleRevenueEvent']);
        add_filter('spherevista_ad_placement', [$this, 'optimizeAdPlacement']);
    }

    public function wordpressInit() {
        // Initialize user session tracking
        MonetizationManager::getModule('analytics')->trackUserSession();

        // Check for monetization opportunities
        MonetizationManager::getModule('adsense')->checkAdOptimization();
    }

    public function registerAdminMenus() {
        add_menu_page(
            'SphereVista360 Monetization',
            'Monetization',
            'manage_options',
            'spherevista360-monitization',
            [$this, 'renderMainDashboard'],
            'dashicons-money-alt',
            30
        );

        // Submenus for different modules
        $submenus = [
            ['adsense', 'AdSense Manager', 'adsense'],
            ['newsletter', 'Newsletter', 'newsletter'],
            ['analytics', 'Analytics', 'analytics'],
            ['payments', 'Payments', 'payments'],
            ['automation', 'Automation', 'automation']
        ];

        foreach ($submenus as $submenu) {
            add_submenu_page(
                'spherevista360-monitization',
                $submenu[1],
                $submenu[1],
                'manage_options',
                'spherevista360-' . $submenu[0],
                [$this, 'renderModulePage']
            );
        }
    }

    public function renderMainDashboard() {
        include __DIR__ . '/../dashboard/templates/main-dashboard.php';
    }

    public function renderModulePage() {
        $module = str_replace('spherevista360-', '', $_GET['page']);
        $template = __DIR__ . "/../dashboard/templates/{$module}.php";

        if (file_exists($template)) {
            include $template;
        } else {
            echo '<div class="wrap"><h1>Module Not Found</h1></div>';
        }
    }

    public function enqueueFrontendAssets() {
        wp_enqueue_style('spherevista360-frontend', plugins_url('assets/css/frontend.css', __FILE__));
        wp_enqueue_script('spherevista360-frontend', plugins_url('assets/js/frontend.js', __FILE__), ['jquery'], '1.0.0', true);

        wp_localize_script('spherevista360-frontend', 'spherevista360', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('spherevista360_nonce'),
            'user_id' => get_current_user_id()
        ]);
    }

    public function enqueueAdminAssets() {
        wp_enqueue_style('spherevista360-admin', plugins_url('assets/css/admin.css', __FILE__));
        wp_enqueue_script('spherevista360-admin', plugins_url('assets/js/admin.js', __FILE__), ['jquery'], '1.0.0', true);
    }

    public function handleRevenueEvent($data) {
        // Log revenue events
        MonetizationManager::getModule('analytics')->logRevenue($data);

        // Process payments if applicable
        if (isset($data['payment_required'])) {
            MonetizationManager::getModule('payments')->processPayment($data);
        }
    }

    public function optimizeAdPlacement($placement) {
        return MonetizationManager::getModule('adsense')->optimizePlacement($placement);
    }

    public function getApp() {
        return $this->app;
    }

    public static function activate() {
        // Plugin activation hook
        Database::createTables();
        Config::setDefaults();

        // Create necessary directories
        self::createDirectories();

        // Set activation flag
        update_option('spherevista360_activated', time());
    }

    public static function deactivate() {
        // Plugin deactivation cleanup
        wp_clear_scheduled_hook('spherevista360_daily_maintenance');
        wp_clear_scheduled_hook('spherevista360_revenue_sync');

        // Note: We don't delete data on deactivation for safety
    }

    private static function createDirectories() {
        $dirs = [
            WP_CONTENT_DIR . '/spherevista360/cache',
            WP_CONTENT_DIR . '/spherevista360/logs',
            WP_CONTENT_DIR . '/spherevista360/temp'
        ];

        foreach ($dirs as $dir) {
            if (!file_exists($dir)) {
                wp_mkdir_p($dir);
            }
        }
    }
}

// Initialize the platform
if (!defined('ABSPATH')) {
    exit;
}

// Register activation/deactivation hooks
register_activation_hook(__FILE__, ['SphereVista360\Monetization\Bootstrap', 'activate']);
register_deactivation_hook(__FILE__, ['SphereVista360\Monetization\Bootstrap', 'deactivate']);

// Start the platform
Bootstrap::getInstance();