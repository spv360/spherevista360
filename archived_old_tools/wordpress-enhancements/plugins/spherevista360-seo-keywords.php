<?php
/**
 * Plugin Name: SphereVista360 SEO Keywords
 * Description: Adds targeted keywords meta tags to improve SEO
 * Version: 1.0
 * Author: SphereVista360
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class SphereVista360_Keywords {
    
    public function __construct() {
        add_action('wp_head', array($this, 'add_keywords_meta'));
    }
    
    public function add_keywords_meta() {
        $default_keywords = 'finance news, technology insights, political analysis, travel guides, world affairs, entertainment news, SphereVista360, global perspectives, breaking news, expert analysis';
        
        $keywords = $default_keywords;
        
        if (is_home() || is_front_page()) {
            $keywords = 'finance news, technology insights, political analysis, travel guides, world affairs, entertainment news, SphereVista360, global perspectives, breaking news, expert analysis, comprehensive coverage';
        } elseif (is_category()) {
            $category = get_queried_object();
            switch($category->slug) {
                case 'finance':
                    $keywords = 'finance, investment, market analysis, economic trends, stock market, financial planning, cryptocurrency, banking, economic indicators, portfolio management';
                    break;
                case 'technology':
                    $keywords = 'technology, artificial intelligence, cybersecurity, digital transformation, AI developments, tech news, innovation, software, cloud computing, machine learning';
                    break;
                case 'politics':
                    $keywords = 'politics, government, elections, policy analysis, political news, governance, public policy, democracy, political trends, voting';
                    break;
                case 'travel':
                    $keywords = 'travel, tourism, destination guides, visa information, travel tips, vacation planning, travel trends, hotels, flights, travel insurance';
                    break;
                case 'world':
                    $keywords = 'world news, international relations, global affairs, diplomacy, international politics, global economy, world events, foreign policy, global trends';
                    break;
                case 'entertainment':
                    $keywords = 'entertainment, movies, TV shows, celebrity news, pop culture, music, Hollywood, streaming, entertainment industry, film reviews';
                    break;
            }
        } elseif (is_single()) {
            global $post;
            $post_categories = get_the_category($post->ID);
            if (!empty($post_categories)) {
                $category_slug = $post_categories[0]->slug;
                // Use category-specific keywords
                $keywords = $this->get_category_keywords($category_slug);
            }
        }
        
        echo '<meta name="keywords" content="' . esc_attr($keywords) . '">' . "\n";
    }
    
    private function get_category_keywords($category_slug) {
        $category_keywords = array(
            'finance' => 'finance, investment, market analysis, economic trends, stock market, financial planning, cryptocurrency, banking, economic indicators, portfolio management',
            'technology' => 'technology, artificial intelligence, cybersecurity, digital transformation, AI developments, tech news, innovation, software, cloud computing, machine learning',
            'politics' => 'politics, government, elections, policy analysis, political news, governance, public policy, democracy, political trends, voting',
            'travel' => 'travel, tourism, destination guides, visa information, travel tips, vacation planning, travel trends, hotels, flights, travel insurance',
            'world' => 'world news, international relations, global affairs, diplomacy, international politics, global economy, world events, foreign policy, global trends',
            'entertainment' => 'entertainment, movies, TV shows, celebrity news, pop culture, music, Hollywood, streaming, entertainment industry, film reviews'
        );
        
        return isset($category_keywords[$category_slug]) ? $category_keywords[$category_slug] : 'finance news, technology insights, political analysis, travel guides, world affairs, entertainment news, SphereVista360';
    }
}

// Initialize the plugin
new SphereVista360_Keywords();
?>