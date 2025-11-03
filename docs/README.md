# SphereVista360 Website Management Toolkit

## Structure

- **content/**: Website content files and assets
- **tools/**: Automation tools and utilities
- **scripts/**: Reusable scripts
- **assets/**: Static assets and media files
- **docs/**: Documentation and guides
- **config.json**: Site configuration and WordPress credentials
- **.env**: Environment variables (create from .env.example)

## Usage

The toolkit provides automated tools for managing the SphereVista360 WordPress site:

```bash
# Publish content
python3 content_publisher.py

# Run SEO validation
python3 tools/seo/comprehensive_seo_validator.py

# Check site status
python3 check_site_status.py
```

## Configuration

1. Copy `.env.example` to `.env` and fill in your credentials
2. Update `config.json` with your WordPress site details
3. Ensure WordPress REST API is enabled with application passwords

## Tools Overview

- **content_publisher.py**: Publish HTML content to WordPress
- **tools/seo/**: SEO validation and optimization tools
- **tools/core/**: Core utilities and helpers
- **scripts/**: Various automation scripts for site management

## Safety Features

- **Config Validation**: Verifies credentials before making changes
- **Dry Run Mode**: Test operations without publishing
- **Backup Integration**: Creates backups before major changes


