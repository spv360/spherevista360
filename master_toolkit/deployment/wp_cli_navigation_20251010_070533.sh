#!/bin/bash
# WordPress Navigation Implementation Commands
# Generated on: 2025-10-10 07:05:33

# Create main navigation menu
wp menu create 'Main Navigation (AdSense Optimized)'
wp menu item add-custom main-navigation 'Home' '/'
wp menu item add-term main-navigation category 167
wp menu item add-term main-navigation category 190
wp menu item add-term main-navigation category 3
wp menu item add-term main-navigation category 6
wp menu item add-term main-navigation category 188
wp menu item add-term main-navigation category 1
wp menu item add-term main-navigation category 7
wp menu item add-term main-navigation category 5
wp menu location assign main-navigation primary

# Create footer menu
wp menu create 'Footer Menu (Compliance)'
wp menu item add-post footer-menu 1977
wp menu item add-post footer-menu 1974
wp menu item add-post footer-menu 1971
wp menu item add-post footer-menu 1663
wp menu item add-post footer-menu 1662
wp menu location assign footer-menu footer

echo 'Navigation implementation completed!'
