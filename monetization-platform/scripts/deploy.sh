#!/bin/bash

# SphereVista360 Monetization Platform Deployment Script

set -e

echo "🚀 Starting SphereVista360 Monetization Platform Deployment"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_ENV=${1:-production}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."

    if ! command -v php &> /dev/null; then
        log_error "PHP is not installed"
        exit 1
    fi

    if ! command -v composer &> /dev/null; then
        log_error "Composer is not installed"
        exit 1
    fi

    if ! command -v npm &> /dev/null; then
        log_error "Node.js/npm is not installed"
        exit 1
    fi

    log_info "All dependencies are available"
}

install_php_dependencies() {
    log_info "Installing PHP dependencies..."
    cd "$PROJECT_ROOT"
    composer install --no-dev --optimize-autoloader
}

install_node_dependencies() {
    log_info "Installing Node.js dependencies..."
    cd "$PROJECT_ROOT"
    npm install
    npm run build
}

setup_database() {
    log_info "Setting up database..."

    if [ "$DEPLOY_ENV" = "docker" ]; then
        log_info "Using Docker database setup"
        return
    fi

    # For production deployment, you would configure database here
    # This is a placeholder for actual database setup
    log_warn "Please configure your database manually for $DEPLOY_ENV environment"
}

configure_environment() {
    log_info "Configuring environment for $DEPLOY_ENV..."

    if [ ! -f ".env.$DEPLOY_ENV" ]; then
        log_error "Environment file .env.$DEPLOY_ENV not found"
        log_info "Please create .env.$DEPLOY_ENV with your configuration"
        exit 1
    fi

    cp ".env.$DEPLOY_ENV" .env
    log_info "Environment configured"
}

run_migrations() {
    log_info "Running database migrations..."
    php core/migrate.php
}

build_assets() {
    log_info "Building assets..."
    npm run build
}

setup_permissions() {
    log_info "Setting up file permissions..."

    # Set proper permissions for WordPress
    find . -type f -name "*.php" -exec chmod 644 {} \;
    find . -type d -exec chmod 755 {} \;

    # Special permissions for wp-content
    chmod -R 775 wp-content/
    chown -R www-data:www-data wp-content/ 2>/dev/null || true
}

run_tests() {
    if [ "$DEPLOY_ENV" = "development" ]; then
        log_info "Running tests..."
        ./vendor/bin/phpunit
    fi
}

cleanup() {
    log_info "Cleaning up temporary files..."

    # Remove development files
    rm -rf node_modules/
    rm -rf tests/
    rm -f composer.lock
    rm -f package-lock.json

    # Remove hidden files that shouldn't be in production
    find . -name ".git*" -type f -delete
    find . -name "*.log" -type f -delete
}

create_backup() {
    if [ -d "wp-content" ]; then
        log_info "Creating backup..."
        BACKUP_DIR="backup-$(date +%Y%m%d-%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        cp -r wp-content/uploads "$BACKUP_DIR/" 2>/dev/null || true
        log_info "Backup created in $BACKUP_DIR"
    fi
}

# Main deployment process
main() {
    log_info "Starting deployment for environment: $DEPLOY_ENV"

    check_dependencies
    create_backup
    install_php_dependencies
    install_node_dependencies
    configure_environment
    setup_database
    run_migrations
    build_assets
    setup_permissions
    run_tests
    cleanup

    log_info "🎉 Deployment completed successfully!"
    log_info "Your SphereVista360 Monetization Platform is ready at: http://your-domain.com"

    if [ "$DEPLOY_ENV" = "docker" ]; then
        log_info "To start with Docker: docker-compose up -d"
    fi
}

# Run main function
main "$@"