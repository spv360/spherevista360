# SphereVista360 Monetization Platform Dockerfile

FROM php:8.1-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    nodejs \
    npm \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy composer files
COPY composer.json composer.lock ./

# Install PHP dependencies
RUN composer install --no-dev --optimize-autoloader

# Copy application code
COPY . .

# Install Node.js dependencies and build assets
RUN npm install && npm run build

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 775 /var/www/html/wp-content

# Configure Apache
RUN a2enmod rewrite headers ssl
COPY docker/apache-config.conf /etc/apache2/sites-available/000-default.conf

# Create necessary directories
RUN mkdir -p wp-content/uploads \
    && mkdir -p wp-content/cache \
    && mkdir -p wp-content/logs \
    && chown -R www-data:www-data wp-content

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/wp-admin/install.php || exit 1

EXPOSE 80

CMD ["apache2-foreground"]