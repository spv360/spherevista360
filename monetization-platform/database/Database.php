<?php
/**
 * SphereVista360 Database Management
 */

namespace SphereVista360\Monetization\Core;

use wpdb;

class Database {

    private static $instance = null;
    private $wpdb;
    private $table_prefix = 'spherevista360_';

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        global $wpdb;
        $this->wpdb = $wpdb;
    }

    public static function createTables() {
        $instance = self::getInstance();
        $instance->createActivityLogTable();
        $instance->createRevenueTable();
        $instance->createSitesTable();
        $instance->createSubscribersTable();
        $instance->createAutomationTable();
        $instance->createPaymentsTable();
    }

    private function createActivityLogTable() {
        $table_name = $this->getTableName('activity_log');

        $sql = "CREATE TABLE {$table_name} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id bigint(20) NOT NULL,
            action varchar(100) NOT NULL,
            data longtext,
            ip_address varchar(45),
            user_agent text,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY user_id (user_id),
            KEY action (action),
            KEY created_at (created_at)
        ) {$this->getCharsetCollate()};";

        $this->executeQuery($sql);
    }

    private function createRevenueTable() {
        $table_name = $this->getTableName('revenue');

        $sql = "CREATE TABLE {$table_name} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id bigint(20) NOT NULL,
            site_id bigint(20),
            source varchar(50) NOT NULL, -- adsense, affiliate, sponsorship, etc.
            amount decimal(10,2) NOT NULL,
            currency varchar(3) DEFAULT 'USD',
            transaction_id varchar(255),
            external_id varchar(255), -- AdSense payment ID, etc.
            status varchar(20) DEFAULT 'pending', -- pending, completed, failed, refunded
            metadata longtext,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            processed_at datetime,
            PRIMARY KEY (id),
            KEY user_id (user_id),
            KEY site_id (site_id),
            KEY source (source),
            KEY status (status),
            KEY created_at (created_at)
        ) {$this->getCharsetCollate()};";

        $this->executeQuery($sql);
    }

    private function createSitesTable() {
        $table_name = $this->getTableName('sites');

        $sql = "CREATE TABLE {$table_name} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id bigint(20) NOT NULL,
            site_url varchar(255) NOT NULL,
            site_name varchar(255),
            platform varchar(50) DEFAULT 'wordpress', -- wordpress, custom, etc.
            adsense_publisher_id varchar(100),
            analytics_tracking_id varchar(50),
            newsletter_audience_id varchar(50),
            status varchar(20) DEFAULT 'active', -- active, inactive, suspended
            tier varchar(20) DEFAULT 'free',
            settings longtext,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY site_url (site_url),
            KEY user_id (user_id),
            KEY status (status),
            KEY tier (tier)
        ) {$this->getCharsetCollate()};";

        $this->executeQuery($sql);
    }

    private function createSubscribersTable() {
        $table_name = $this->getTableName('subscribers');

        $sql = "CREATE TABLE {$table_name} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id bigint(20) NOT NULL,
            site_id bigint(20),
            email varchar(255) NOT NULL,
            first_name varchar(100),
            last_name varchar(100),
            status varchar(20) DEFAULT 'active', -- active, unsubscribed, bounced
            source varchar(50) DEFAULT 'website', -- website, import, api
            tags text,
            metadata longtext,
            subscribed_at datetime DEFAULT CURRENT_TIMESTAMP,
            unsubscribed_at datetime,
            last_activity datetime,
            PRIMARY KEY (id),
            UNIQUE KEY email_site (email, site_id),
            KEY user_id (user_id),
            KEY site_id (site_id),
            KEY status (status),
            KEY subscribed_at (subscribed_at)
        ) {$this->getCharsetCollate()};";

        $this->executeQuery($sql);
    }

    private function createAutomationTable() {
        $table_name = $this->getTableName('automation');

        $sql = "CREATE TABLE {$table_name} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id bigint(20) NOT NULL,
            site_id bigint(20),
            task_type varchar(50) NOT NULL, -- content_publish, seo_optimize, ad_refresh, etc.
            task_name varchar(255) NOT NULL,
            schedule varchar(100), -- cron expression or interval
            parameters longtext,
            status varchar(20) DEFAULT 'active', -- active, paused, completed, failed
            last_run datetime,
            next_run datetime,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY user_id (user_id),
            KEY site_id (site_id),
            KEY task_type (task_type),
            KEY status (status),
            KEY next_run (next_run)
        ) {$this->getCharsetCollate()};";

        $this->executeQuery($sql);
    }

    private function createPaymentsTable() {
        $table_name = $this->getTableName('payments');

        $sql = "CREATE TABLE {$table_name} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id bigint(20) NOT NULL,
            subscription_id varchar(255),
            payment_method varchar(50), -- stripe, paypal
            transaction_id varchar(255) NOT NULL,
            amount decimal(10,2) NOT NULL,
            currency varchar(3) DEFAULT 'USD',
            status varchar(20) DEFAULT 'pending', -- pending, completed, failed, refunded
            payment_type varchar(50), -- subscription, one_time, upgrade
            tier varchar(20),
            billing_period varchar(20), -- monthly, yearly
            metadata longtext,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            processed_at datetime,
            PRIMARY KEY (id),
            UNIQUE KEY transaction_id (transaction_id),
            KEY user_id (user_id),
            KEY subscription_id (subscription_id),
            KEY status (status),
            KEY payment_type (payment_type)
        ) {$this->getCharsetCollate()};";

        $this->executeQuery($sql);
    }

    public function getTableName($table) {
        return $this->wpdb->prefix . $this->table_prefix . $table;
    }

    public function insert($table, $data) {
        $table_name = $this->getTableName($table);
        return $this->wpdb->insert($table_name, $data);
    }

    public function update($table, $data, $where) {
        $table_name = $this->getTableName($table);
        return $this->wpdb->update($table_name, $data, $where);
    }

    public function delete($table, $where) {
        $table_name = $this->getTableName($table);
        return $this->wpdb->delete($table_name, $where);
    }

    public function getRow($table, $where = [], $output = OBJECT) {
        $table_name = $this->getTableName($table);
        return $this->wpdb->get_row(
            $this->wpdb->prepare(
                "SELECT * FROM {$table_name} WHERE " . $this->buildWhereClause($where),
                array_values($where)
            ),
            $output
        );
    }

    public function getResults($table, $where = [], $output = OBJECT) {
        $table_name = $this->getTableName($table);
        return $this->wpdb->get_results(
            $this->wpdb->prepare(
                "SELECT * FROM {$table_name} WHERE " . $this->buildWhereClause($where),
                array_values($where)
            ),
            $output
        );
    }

    public function getVar($table, $column, $where = []) {
        $table_name = $this->getTableName($table);
        return $this->wpdb->get_var(
            $this->wpdb->prepare(
                "SELECT {$column} FROM {$table_name} WHERE " . $this->buildWhereClause($where),
                array_values($where)
            )
        );
    }

    private function buildWhereClause($where) {
        if (empty($where)) {
            return '1=1';
        }

        $clauses = [];
        foreach (array_keys($where) as $column) {
            $clauses[] = "{$column} = %s";
        }

        return implode(' AND ', $clauses);
    }

    private function executeQuery($sql) {
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
    }

    private function getCharsetCollate() {
        return $this->wpdb->get_charset_collate();
    }

    public function getWpdb() {
        return $this->wpdb;
    }
}