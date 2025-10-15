-- WordPress Configuration SQL
-- Run these queries in phpMyAdmin or MySQL

-- Update site options
UPDATE wp_options SET option_value = 'page' WHERE option_name = 'show_on_front';
UPDATE wp_options SET option_value = '2157' WHERE option_name = 'page_on_front';
UPDATE wp_options SET option_value = '2168' WHERE option_name = 'page_for_posts';
UPDATE wp_options SET option_value = 'SphereVista360' WHERE option_name = 'blogname';
UPDATE wp_options SET option_value = 'Your 360° View on Global Insights - Finance, Technology & Innovation' WHERE option_name = 'blogdescription';
UPDATE wp_options SET option_value = '/%postname%/' WHERE option_name = 'permalink_structure';

-- Note: After running these queries, you still need to configure the menu in WordPress admin
