# SphereVista360 Tools

This directory contains all the essential, reusable tools for managing the WordPress publishing workflow.

## Directory Structure

```
tools/
├── validation/          # Link and image validation tools
│   ├── links.py        # Link validation and fixing utilities
│   └── images.py       # Image validation and optimization
├── publishing/         # Content publishing tools
│   ├── publish_individual.py    # Individual post publishing
│   ├── individual_publisher.py  # Publisher class
│   └── publisher.py             # Main publisher utilities
├── seo/                # SEO optimization tools
│   └── comprehensive_seo_validator.py  # SEO auditing
├── maintenance/        # Core maintenance tools
│   ├── auth.py         # Authentication utilities
│   ├── client.py       # WordPress API client
│   └── config.py       # Configuration management
└── master_website_tester.py  # Complete site validation tool
```

## Key Tools

### Master Website Tester (`master_website_tester.py`)
Comprehensive website validation tool that checks:
- All internal and external links for broken URLs
- All images for accessibility and loading issues
- SEO optimization (titles, meta descriptions, etc.)
- Generates detailed reports with recommendations

**Usage:**
```bash
cd tools
python3 master_website_tester.py
```

### Publishing Tools
- `publish_individual.py`: CLI tool for publishing individual posts with validation
- `individual_publisher.py`: Publisher class with SEO checks and image handling
- `publisher.py`: Core publishing utilities

### Validation Tools
- `links.py`: Link validation and broken link fixing
- `images.py`: Image validation and optimization
- `comprehensive_seo_validator.py`: Complete SEO auditing

### Maintenance Tools
- `auth.py`: WordPress authentication
- `client.py`: WordPress REST API client
- `config.py`: Configuration management

## Quick Start

1. Run the master website tester to check site health:
   ```bash
   python3 tools/master_website_tester.py
   ```

2. Use the publishing tools for new content:
   ```bash
   python3 tools/publishing/publish_individual.py
   ```

3. Validate links and images:
   ```bash
   # Use the validation tools in your scripts
   from tools.validation.links import LinkValidator
   ```

## Dependencies

- requests
- python-dotenv
- PIL (Pillow) for image processing
- All tools are designed to work with the existing master_toolkit infrastructure