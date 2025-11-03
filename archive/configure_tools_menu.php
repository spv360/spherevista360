<?php
/**
 * WordPress Tools Menu Configuration Script
 * Run this in your theme's functions.php or as a standalone script
 */

// Add Tools menu item programmatically
function add_tools_menu_item() {
    // Only run this once
    if (get_option('tools_menu_configured')) {
        return;
    }

    // Get primary menu
    $menu_name = 'primary'; // Change this to match your menu location
    $menu = wp_get_nav_menu_object($menu_name);

    if (!$menu) {
        // Try to get the first available menu
        $menus = wp_get_nav_menus();
        if (!empty($menus)) {
            $menu = $menus[0];
        }
    }

    if ($menu) {
        // Check if Tools page exists
        $tools_page = get_page_by_title('Tools');
        if (!$tools_page) {
            // Create Tools page
            $tools_content = '<!-- Content from tools_page_content.html -->';
            $tools_page_id = wp_insert_post(array(
                'post_title' => 'Tools',
                'post_content' => $tools_content,
                'post_status' => 'publish',
                'post_type' => 'page',
            ));
        } else {
            $tools_page_id = $tools_page->ID;
        }

        // Check if SIP Calculator page exists
        $sip_page = get_page_by_title('SIP Calculator');
        if (!$sip_page) {
            // Create SIP Calculator page
            $sip_page_id = wp_insert_post(array(
                'post_title' => 'SIP Calculator',
                'post_content' => '[sip_calculator]',
                'post_status' => 'publish',
                'post_type' => 'page',
            ));
        } else {
            $sip_page_id = $sip_page->ID;
        }

        // Add items to menu
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
            'menu-item-parent-id' => $tools_page_id, // Make it a submenu
        ));

        // Mark as configured
        update_option('tools_menu_configured', true);

        echo "Tools menu configured successfully!";
    } else {
        echo "Could not find a menu to update. Please create a menu first.";
    }
}

// Uncomment the line below to run the configuration
// add_tools_menu_config();

// Alternative: Add this to your theme's functions.php
/*
add_action('init', 'add_tools_menu_item');
*/
?>
