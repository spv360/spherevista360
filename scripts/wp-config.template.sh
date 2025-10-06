#!/bin/bash
# WordPress Configuration Template
# Copy this file to wp-config.local.sh and fill in your credentials
# IMPORTANT: wp-config.local.sh is ignored by Git and will not be committed

export WP_SITE="https://spherevista360.com"
export WP_USER="your_wordpress_username"
export WP_APP_PASS="your_wordpress_application_password"

# To get your WordPress Application Password:
# 1. Go to WordPress Admin → Users → Profile
# 2. Scroll down to "Application Passwords"
# 3. Enter application name (e.g., "SphereVista360 Automation")
# 4. Click "Add New Application Password"
# 5. Copy the generated password (it will look like: "xxxx xxxx xxxx xxxx xxxx xxxx")
