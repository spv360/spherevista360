# WordPress Tools Package

A comprehensive suite of reusable tools for WordPress site optimization, validation, and maintenance.

## Features

### 🔧 WordPress REST API Client (`wp_client.py`)
- Full WordPress REST API integration
- Authentication with application passwords
- CRUD operations for posts, pages, categories
- Built-in error handling and utilities

### 📊 SEO Validator (`seo_validator.py`)
- Comprehensive SEO scoring (H2 headings, images, titles, internal links)
- Category-based validation
- Detailed reports and recommendations
- Command-line tool (`seo_tool.py`)

### 🖼️ Image Validator (`image_validator.py`)
- Image presence and alt text validation
- Automatic image addition with responsive styling
- Broken image detection
- Command-line tool (`image_tool.py`)

### 🔗 Link Validator (`link_validator.py`)
- Broken link detection
- Menu structure validation
- Site-wide link scanning
- Internal/external link classification
- Command-line tool (`link_tool.py`)

## Quick Start

### Installation
```bash
# Install dependencies
pip install requests beautifulsoup4

# Make tools executable
chmod +x wp_tools/*.py
```

### Basic Usage

#### SEO Validation
```python
from wp_tools import WordPressClient, SEOValidator

# Initialize client
wp_client = WordPressClient()
wp_client.authenticate('username', 'app_password')

# Validate SEO for Entertainment category
validator = SEOValidator()
results = validate_all_posts(wp_client, 'Entertainment')

# Generate report
report = validator.generate_report(results)
print(report)
```

#### Command Line Tools
```bash
# SEO validation for Entertainment category
python wp_tools/seo_tool.py --category Entertainment --report seo_report.txt

# Image validation with auto-fix
python wp_tools/image_tool.py --category Entertainment --fix --add-images

# Link validation for entire site
python wp_tools/link_tool.py --site-scan --max-pages 20 --report link_report.txt

# Menu validation
python wp_tools/link_tool.py --menu
```

## Tool Reference

### SEO Tool (`seo_tool.py`)
```bash
# Validate specific post
python wp_tools/seo_tool.py --post-id 123

# Validate by category
python wp_tools/seo_tool.py --category "Entertainment"

# Validate all pages
python wp_tools/seo_tool.py --pages

# Save report
python wp_tools/seo_tool.py --category "Entertainment" --report seo_report.txt
```

### Image Tool (`image_tool.py`)
```bash
# Validate images in specific post
python wp_tools/image_tool.py --post-id 123

# Fix images automatically
python wp_tools/image_tool.py --post-id 123 --fix --add-images

# Validate by category with fixes
python wp_tools/image_tool.py --category "Entertainment" --fix --add-images
```

### Link Tool (`link_tool.py`)
```bash
# Validate links in specific post
python wp_tools/link_tool.py --post-id 123

# Validate menu structure
python wp_tools/link_tool.py --menu

# Scan entire site for broken links
python wp_tools/link_tool.py --site-scan --max-pages 20

# Save detailed report
python wp_tools/link_tool.py --site-scan --report broken_links.txt
```

## SEO Scoring Criteria

### Core Requirements (100% scoring)
- **H2 Headings**: 2+ structured headings (25 points)
- **Images**: 1+ images with alt text (25 points)  
- **Title Length**: Under 60 characters (25 points)
- **Internal Links**: 2+ internal links (25 points)

### Bonus Points
- **Meta Description**: Present and optimized (bonus)

### Grading Scale
- A+: 100% (Perfect SEO)
- A: 75-99% (Excellent)
- B: 50-74% (Good)
- C: 25-49% (Needs Work)
- F: 0-24% (Poor)

## Common Workflows

### Complete Site Optimization
```bash
# 1. SEO validation and report
python wp_tools/seo_tool.py --report initial_seo.txt

# 2. Fix images site-wide
python wp_tools/image_tool.py --fix --add-images --report image_fixes.txt

# 3. Validate links and menu
python wp_tools/link_tool.py --menu --report menu_validation.txt
python wp_tools/link_tool.py --site-scan --report broken_links.txt

# 4. Final SEO validation
python wp_tools/seo_tool.py --report final_seo.txt
```

### Category-Specific Optimization
```bash
# Focus on Entertainment category
python wp_tools/seo_tool.py --category "Entertainment"
python wp_tools/image_tool.py --category "Entertainment" --fix --add-images
```

## Authentication

All tools require WordPress authentication:

1. **Create Application Password** in WordPress Admin:
   - Users → Profile → Application Passwords
   - Generate new password

2. **Provide Credentials**:
   - Interactive prompts (default)
   - Command line: `--username USER --password PASS`
   - Environment variables: `WP_USERNAME`, `WP_PASSWORD`

## Output Examples

### SEO Validation Output
```
📊 SEO VALIDATION TOOL
===============================================

📊 VALIDATION SUMMARY:
   📄 Posts analyzed: 5
   📈 Average score: 100.0%
   🎯 Perfect scores: 5/5

📋 INDIVIDUAL RESULTS:
   1. YouTube Automation Channels Scaling...
      📊 100.0% (4/4 core + 0/1 bonus)
   
   2. Streaming Wars Update...
      📊 100.0% (4/4 core + 0/1 bonus)
```

### Image Validation Output
```
🖼️ IMAGE VALIDATION TOOL
===============================================

📄 Title: Newsletter Page
🖼️ Total Images: 3
📊 Image Score: 100.0% (Grade: A+)
✅ Images with alt text: 3/3
🌐 Accessible images: 3/3
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- WordPress with REST API enabled
- Application passwords configured

## Error Handling

Tools include comprehensive error handling:
- Network timeouts and connection errors
- Authentication failures
- Missing content or invalid IDs
- API rate limiting
- Graceful degradation for partial failures

## Contributing

When adding new tools:
1. Follow the modular structure pattern
2. Include comprehensive error handling
3. Add command-line interface
4. Update this README
5. Add examples and documentation