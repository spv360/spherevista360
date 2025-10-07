
<?php
/**
 * SphereVista360 Theme Enhancements
 * Complete SEO optimization with keywords meta tags and image support
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Add Keywords Meta Tags to Pages and Posts
 */
function spherevista360_add_keywords_meta() {
    // Category-specific keywords mapping
    $category_keywords = array(
        'finance' => 'finance news, investment analysis, market trends, stock market, cryptocurrency, economic outlook, financial planning, wealth management, trading strategies, business finance',
        'technology' => 'technology news, artificial intelligence, cybersecurity, software development, digital innovation, tech trends, startup ecosystem, mobile technology, cloud computing, data science',
        'politics' => 'political news, government policy, election coverage, political analysis, international relations, democracy, political campaigns, legislative updates, political commentary, governance',
        'travel' => 'travel guides, destination reviews, travel tips, tourism trends, vacation planning, cultural experiences, adventure travel, budget travel, travel safety, hospitality industry',
        'world' => 'world news, international affairs, global events, breaking news, diplomatic relations, cross-border issues, international trade, global politics, humanitarian issues, world economy',
        'entertainment' => 'entertainment news, celebrity updates, movie reviews, TV shows, music industry, pop culture, streaming services, entertainment trends, awards shows, celebrity interviews'
    );
    
    // Homepage keywords
    $homepage_keywords = 'SphereVista360, global news, finance technology politics travel world entertainment, breaking news, expert analysis, comprehensive coverage, international perspectives, daily insights';
    
    // Get current page/post information
    $keywords = '';
    
    if (is_home() || is_front_page()) {
        $keywords = $homepage_keywords;
    } elseif (is_category()) {
        $category = get_queried_object();
        $category_slug = $category->slug;
        
        if (isset($category_keywords[$category_slug])) {
            $keywords = $category_keywords[$category_slug];
        }
    } elseif (is_single() || is_page()) {
        $post_categories = get_the_category();
        
        if (!empty($post_categories)) {
            $primary_category = $post_categories[0]->slug;
            
            if (isset($category_keywords[$primary_category])) {
                $keywords = $category_keywords[$primary_category];
            }
        }
        
        // Add post-specific keywords if available
        $post_keywords = get_post_meta(get_the_ID(), '_yoast_wpseo_focuskw', true);
        if (!empty($post_keywords)) {
            $keywords = $post_keywords . ', ' . $keywords;
        }
    }
    
    // Output keywords meta tag if we have keywords
    if (!empty($keywords)) {
        echo '<meta name="keywords" content="' . esc_attr($keywords) . '">' . "\n";
    }
}

// Hook into wp_head to add keywords meta tags
add_action('wp_head', 'spherevista360_add_keywords_meta', 1);

/**
 * Enhance Homepage with Featured Images
 */
function spherevista360_homepage_featured_content() {
    if (is_home() || is_front_page()) {
        // Add structured data for better SEO
        ?>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "SphereVista360",
            "url": "<?php echo esc_url(home_url('/')); ?>",
            "description": "Your comprehensive source for global insights on finance, technology, politics, travel, world affairs, and entertainment.",
            "publisher": {
                "@type": "Organization",
                "name": "SphereVista360",
                "url": "<?php echo esc_url(home_url('/')); ?>"
            },
            "potentialAction": {
                "@type": "SearchAction",
                "target": "<?php echo esc_url(home_url('/')); ?>?s={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        }
        </script>
        
        <!-- Open Graph Meta Tags -->
        <meta property="og:title" content="SphereVista360 - Global Perspectives on Finance, Technology, Politics & More">
        <meta property="og:description" content="Your comprehensive source for global insights on finance, technology, politics, travel, world affairs, and entertainment.">
        <meta property="og:type" content="website">
        <meta property="og:url" content="<?php echo esc_url(home_url('/')); ?>">
        <meta property="og:image" content="https://via.placeholder.com/1200x630/667eea/FFFFFF?text=SphereVista360+Global+Perspectives">
        <meta property="og:site_name" content="SphereVista360">
        
        <!-- Twitter Card Meta Tags -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="SphereVista360 - Global Perspectives">
        <meta name="twitter:description" content="Your comprehensive source for global insights on finance, technology, politics, travel, world affairs, and entertainment.">
        <meta name="twitter:image" content="https://via.placeholder.com/1200x630/667eea/FFFFFF?text=SphereVista360+Global+Perspectives">
        <?php
    }
}

// Hook into wp_head for homepage enhancements
add_action('wp_head', 'spherevista360_homepage_featured_content', 2);

/**
 * Add custom CSS for better image display
 */
function spherevista360_custom_styles() {
    ?>
    <style>
        /* SphereVista360 Custom Styles */
        .spherevista-hero img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .spherevista-category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .spherevista-category-card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        
        .spherevista-category-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .spherevista-category-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        @media (max-width: 768px) {
            .spherevista-category-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    <?php
}

// Add custom styles to wp_head
add_action('wp_head', 'spherevista360_custom_styles', 10);

/**
 * Enhance category pages with featured images
 */
function spherevista360_category_featured_images() {
    if (is_category()) {
        $category = get_queried_object();
        $category_slug = $category->slug;
        
        // Category-specific featured images
        $category_images = array(
            'finance' => 'https://via.placeholder.com/1200x400/38A169/FFFFFF?text=Finance+%26+Investment+News',
            'technology' => 'https://via.placeholder.com/1200x400/4C51BF/FFFFFF?text=Technology+%26+Innovation',
            'politics' => 'https://via.placeholder.com/1200x400/9F7AEA/FFFFFF?text=Politics+%26+Governance',
            'travel' => 'https://via.placeholder.com/1200x400/D53F8C/FFFFFF?text=Travel+%26+Tourism',
            'world' => 'https://via.placeholder.com/1200x400/2B6CB0/FFFFFF?text=World+Affairs',
            'entertainment' => 'https://via.placeholder.com/1200x400/E53E3E/FFFFFF?text=Entertainment+News'
        );
        
        if (isset($category_images[$category_slug])) {
            ?>
            <div class="category-featured-image" style="text-align: center; margin: 20px 0;">
                <img src="<?php echo esc_url($category_images[$category_slug]); ?>" 
                     alt="<?php echo esc_attr($category->name); ?> News and Updates" 
                     style="width: 100%; max-width: 1200px; height: auto; border-radius: 8px;" />
            </div>
            <?php
        }
    }
}

// Hook to display category images
add_action('wp_head', 'spherevista360_category_featured_images', 15);

/**
 * Optimize images for better SEO
 */
function spherevista360_optimize_images($attr, $attachment, $size) {
    // Add alt text if missing
    if (empty($attr['alt'])) {
        $attr['alt'] = get_post_meta($attachment->ID, '_wp_attachment_image_alt', true);
        
        if (empty($attr['alt'])) {
            $attr['alt'] = $attachment->post_title;
        }
    }
    
    // Add loading attribute for performance
    if (!isset($attr['loading'])) {
        $attr['loading'] = 'lazy';
    }
    
    return $attr;
}

// Hook to optimize image attributes
add_filter('wp_get_attachment_image_attributes', 'spherevista360_optimize_images', 10, 3);

/**
 * Add breadcrumb schema for better SEO
 */
function spherevista360_breadcrumb_schema() {
    if (!is_home() && !is_front_page()) {
        ?>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "<?php echo esc_url(home_url('/')); ?>"
                }
                <?php if (is_category()) : ?>
                ,{
                    "@type": "ListItem",
                    "position": 2,
                    "name": "<?php echo esc_js(single_cat_title('', false)); ?>",
                    "item": "<?php echo esc_url(get_category_link(get_queried_object_id())); ?>"
                }
                <?php endif; ?>
            ]
        }
        </script>
        <?php
    }
}

// Add breadcrumb schema
add_action('wp_head', 'spherevista360_breadcrumb_schema', 20);

/**
 * Log SEO enhancements for debugging
 */
function spherevista360_log_seo_enhancements() {
    if (WP_DEBUG && WP_DEBUG_LOG) {
        error_log('SphereVista360 SEO Enhancements Active: ' . date('Y-m-d H:i:s'));
    }
}

// Initialize logging
add_action('init', 'spherevista360_log_seo_enhancements');

?>
