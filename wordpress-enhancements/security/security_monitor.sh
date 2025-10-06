#!/bin/bash
# WordPress Security Monitoring Script for SphereVista360
# Run this script regularly to check for security issues

echo "🔍 WordPress Security Check - $(date)"
echo "=================================="

# Check for failed login attempts in access logs
echo "📊 Recent failed login attempts:"
if [ -f "/var/log/apache2/access.log" ]; then
    grep "wp-login.php" /var/log/apache2/access.log | grep -v "200" | tail -10
elif [ -f "/var/log/nginx/access.log" ]; then
    grep "wp-login.php" /var/log/nginx/access.log | grep -v "200" | tail -10
else
    echo "   No web server logs found"
fi

echo ""

# Check WordPress core files integrity
echo "🔧 WordPress core integrity:"
if command -v wp &> /dev/null; then
    wp core verify-checksums --path=/var/www/html
else
    echo "   WP-CLI not available - manual check required"
fi

echo ""

# Check for suspicious files
echo "🚨 Suspicious file check:"
find /var/www/html -name "*.php" -type f -newer /tmp/last_check 2>/dev/null | head -10
echo "   Files modified since last check (showing first 10)"

# Update timestamp for next check
touch /tmp/last_check

echo ""

# Check disk space
echo "💾 Disk space usage:"
df -h | grep -E "(/$|/var)"

echo ""

# Check for WordPress updates
echo "🔄 Update status:"
if command -v wp &> /dev/null; then
    wp core check-update --path=/var/www/html
    wp plugin list --update=available --path=/var/www/html
    wp theme list --update=available --path=/var/www/html
else
    echo "   WP-CLI not available - check admin dashboard"
fi

echo ""
echo "✅ Security check complete"
echo "📝 Review results and take necessary actions"
