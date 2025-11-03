<?php
/**
 * Quick Tools Setup Script
 * Upload this to your WordPress root and run it once, then delete it
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    die('Direct access not allowed');
}

require_once('wp-load.php');

// Check if user is admin
if (!current_user_can('administrator')) {
    die('Admin access required');
}

echo "<h1>SIP Calculator Tools Setup</h1>";

// Create Tools page
$tools_content = file_get_contents('tools_page_content.html');
if ($tools_content === false) {
    $tools_content = '<!-- Add tools content here -->';
}

$tools_page = array(
    'post_title' => 'Tools',
    'post_content' => $tools_content,
    'post_status' => 'publish',
    'post_type' => 'page',
);

$tools_page_id = wp_insert_post($tools_page);

if ($tools_page_id) {
    echo "<p>✓ Tools page created (ID: $tools_page_id)</p>";
} else {
    echo "<p>✗ Failed to create Tools page</p>";
}

// Create SIP Calculator page
$sip_page = array(
    'post_title' => 'SIP Calculator',
    'post_content' => '[sip_calculator]',
    'post_status' => 'publish',
    'post_type' => 'page',
);

$sip_page_id = wp_insert_post($sip_page);

if ($sip_page_id) {
    echo "<p>✓ SIP Calculator page created (ID: $sip_page_id)</p>";
} else {
    echo "<p>✗ Failed to create SIP Calculator page</p>";
}

// Update menu
if ($tools_page_id && $sip_page_id) {
    $menu_name = 'primary';
    $menu = wp_get_nav_menu_object($menu_name);

    if (!$menu) {
        $menus = wp_get_nav_menus();
        if (!empty($menus)) {
            $menu = $menus[0];
        }
    }

    if ($menu) {
        wp_update_nav_menu_item($menu->term_id, 0, array(
            'menu-item-title' => 'Tools',
            'menu-item-url' => get_permalink($tools_page_id),
            'menu-item-status' => 'publish',
            'menu-item-type' => 'post_type',
            'menu-item-object' => 'page',
            'menu-item-object-id' => $tools_page_id,
        ));

        wp_update_nav_menu_item($menu->term_id, 0, array(
            'menu-item-title' => 'SIP Calculator',
            'menu-item-url' => get_permalink($sip_page_id),
            'menu-item-status' => 'publish',
            'menu-item-type' => 'post_type',
            'menu-item-object' => 'page',
            'menu-item-object-id' => $sip_page_id,
        ));

        echo "<p>✓ Menu items added</p>";
    } else {
        echo "<p>⚠ Could not update menu automatically</p>";
    }
}

echo "<h2>Setup Complete!</h2>";
echo "<p><strong>Next steps:</strong></p>";
echo "<ul>";
echo "<li>Check your site's navigation menu</li>";
echo "<li>Visit the Tools page: <a href='" . get_permalink($tools_page_id) . "' target='_blank'>View Tools</a></li>";
echo "<li>Visit the SIP Calculator: <a href='" . get_permalink($sip_page_id) . "' target='_blank'>View Calculator</a></li>";
echo "<li>Delete this file for security</li>";
echo "</ul>";
?>
