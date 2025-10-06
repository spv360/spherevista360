# SphereVista360 - Advanced WordPress Content Management System

![SphereVista360](https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&h=400&q=80)

> A sophisticated WordPress automation platform with advanced image validation, SEO optimization, and intelligent content publishing.

## 🚀 Features

### ✨ **Core Capabilities**
- **Bulk WordPress Publishing**: Upload multiple Markdown posts with YAML front matter
- **Advanced Image Validation**: AI-powered quality, SEO, and copyright verification
- **Smart Category Detection**: Automatic categorization based on content analysis
- **SEO Optimization**: Built-in RankMath support and metadata enhancement
- **Image Processing**: Automatic image embedding with validation and optimization

### 🔍 **Image Validation System**
- **Quality Assurance**: Resolution, aspect ratio, and file size validation
- **Copyright Compliance**: Automatic verification of usage rights and licenses
- **SEO Optimization**: Alt text, metadata, and filename validation
- **Content Relevance**: Intelligent keyword matching and OCR text analysis
- **Duplicate Detection**: Perceptual hashing to prevent duplicate uploads

### 📝 **Content Management**
- **Markdown Support**: Full Markdown to HTML conversion with extensions
- **YAML Front Matter**: Complete metadata support including SEO fields
- **Category Management**: Automatic folder-based categorization
- **Image Embedding**: Smart image selection and embedding after H2 or at top
- **Link Enhancement**: UTM parameter injection for tracking

## 🛠️ Installation

### Prerequisites
```bash
# Python 3.8+
python --version

# Virtual environment (recommended)
python -m venv wpagent-venv
source wpagent-venv/bin/activate  # Linux/Mac
# or
wpagent-venv\Scripts\activate     # Windows
```

### Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- `requests` - WordPress API communication
- `markdown` - Markdown to HTML conversion
- `pyyaml` - YAML front matter parsing
- `python-slugify` - URL-friendly slug generation
- `Pillow` - Image processing and validation
- `pytesseract` - OCR text extraction (optional)

### Optional: Tesseract OCR
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

## ⚙️ Configuration

### WordPress Setup
1. **Generate Application Password**:
   - Go to WordPress Admin → Users → Profile
   - Scroll to "Application Passwords"
   - Add new password with name "Bulk Uploader"
   - Copy the generated password (keep spaces)

2. **Environment Variables**:
```bash
export WP_SITE="https://your-site.com"
export WP_USER="your_username"
export WP_APP_PASS="your application password with spaces"
```

3. **Create .env file** (optional):
```env
WP_SITE=https://spherevista360.com
WP_USER=your_username
WP_APP_PASS=your application password
```

## 📖 Usage

### Basic Upload
```bash
python wp_agent_bulk.py ./content_folder
```

### Advanced Options
```bash
# Publish immediately (default: drafts)
python wp_agent_bulk.py ./content_folder --publish

# Place images at top instead of after H2
python wp_agent_bulk.py ./content_folder --top-image

# Skip image embedding
python wp_agent_bulk.py ./content_folder --no-image

# Force specific category
python wp_agent_bulk.py ./content_folder --category "Tech"

# Add UTM tracking
python wp_agent_bulk.py ./content_folder --utm "?utm_source=spherevista360"
```

### Content Structure
```
content_folder/
├── Finance/
│   ├── investing-tips-2025.md
│   └── market-analysis.md
├── Tech/
│   ├── ai-trends.md
│   └── cloud-computing.md
└── images/
    ├── finance-chart.jpg
    └── tech-innovation.png
```

### Markdown Format
```markdown
---
title: "How AI Is Transforming Finance in 2025"
excerpt: "Discover the latest AI applications in financial services"
category: "Finance"
tags: ["AI", "Finance", "Technology"]
publish: true
slug: "ai-finance-2025"
seo_title: "AI in Finance 2025: Complete Guide"
seo_description: "Learn how AI is revolutionizing finance in 2025"
image: "https://example.com/image.jpg"
alt: "AI technology in finance illustration"
---

Your content here in **Markdown** format.

## Key Points
- AI automation
- Risk assessment
- Customer service
```

## 🖼️ Image Validation

### Automatic Validation
Every image is automatically validated for:
- **Quality**: Resolution, aspect ratio, file size
- **SEO**: Alt text, metadata, filename optimization
- **Copyright**: Usage rights and license verification
- **Relevance**: Content matching and keyword analysis
- **Duplicates**: Perceptual hash comparison

### Validation Results
```bash
✅ Remote image validated successfully:
  • Image is unique
  • Verified free stock: unsplash.com
  • Good relevance (2.5): Good aspect ratio; Matches 2 category keywords

⚠️ Remote image validation warnings:
  • Missing metadata: description, caption
  • Consider adding more descriptive alt text
```

### Category Keywords
The system includes intelligent keyword matching for:
- **Finance**: stock, market, trading, investment, banking
- **Tech**: software, AI, cloud, programming, automation
- **World**: geography, culture, politics, global events
- **Travel**: destinations, transportation, accommodation
- **Politics**: government, elections, policy, leadership

## 📊 Content Generation

### Built-in Content Creator
```bash
# Generate week's content
python build_week1_zip_v3.py

# Creates structured content with:
# - 12 posts across 6 categories
# - SEO-optimized titles and descriptions
# - Relevant Unsplash images
# - Cross-linking between related posts
```

### Content Categories
- **Finance** (3 posts): AI investing, inflation trends, digital banking
- **Tech** (3 posts): Cloud wars, AI tools, cybersecurity
- **World** (2 posts): Trade relations, global elections
- **Travel** (2 posts): Visa-free destinations, digital nomad visas
- **Politics** (1 post): AI influence in politics
- **Business** (1 post): Startup funding trends

## 🔧 Advanced Features

### Image Validation Configuration
```python
from image_validator import ImageValidator

validator = ImageValidator()

# Custom quality thresholds
validator.min_width = 1200
validator.min_height = 800
validator.min_file_size = 100 * 1024  # 100KB

# SEO requirements
validator.required_meta = {'alt_text', 'title', 'description'}

# Copyright sources
validator.known_free_stock_sites.add('your-stock-site.com')
```

### Custom Category Mapping
```python
CATEGORY_MAP = {
    "Finance": ["stock", "market", "invest", "fund"],
    "Tech": ["ai", "cloud", "saas", "startup"],
    "Custom": ["your", "keywords", "here"]
}
```

### Batch Processing
```python
# Process multiple folders
folders = ["content1", "content2", "content3"]
for folder in folders:
    process(Path(folder), publish=True)
```

## 📈 SEO Optimization

### Built-in SEO Features
- **Meta Title & Description**: Automatic generation and validation
- **Alt Text Optimization**: Descriptive, keyword-rich alt attributes
- **URL-Friendly Slugs**: Clean, SEO-friendly post URLs
- **Image Optimization**: Proper sizing, lazy loading, compression
- **Schema Markup**: Structured data for better search visibility

### RankMath Integration
```yaml
seo_title: "Your SEO Title (under 60 chars)"
seo_description: "Your meta description (under 160 chars)"
```

## 🚀 Performance

### Optimization Features
- **Lazy Loading**: Images load only when needed
- **Responsive Images**: Automatic sizing for different devices
- **Duplicate Detection**: Prevents redundant uploads
- **Batch Processing**: Efficient handling of multiple posts
- **Smart Caching**: Image validation result caching

### Performance Metrics
- **Upload Speed**: ~2-3 posts per second
- **Image Processing**: <1 second per image validation
- **Memory Usage**: Minimal footprint with cleanup
- **Error Recovery**: Graceful handling of network issues

## 🛡️ Security & Compliance

### Security Features
- **Application Passwords**: Secure WordPress authentication
- **HTTPS Required**: Encrypted communication only
- **Input Validation**: Sanitized content processing
- **Error Handling**: Safe failure modes

### Copyright Compliance
- **Source Verification**: Automatic license checking
- **Usage Rights**: Clear attribution requirements
- **EXIF Analysis**: Embedded copyright detection
- **Safe Defaults**: Conservative approval process

## 📚 Documentation

### Additional Resources
- [Image Validator Documentation](IMAGE_VALIDATOR_DOCS.md)
- [WordPress Setup Guide](WORDPRESS_SETUP.md)
- [Content Creation Guide](CONTENT_CREATION.md)
- [API Reference](API_REFERENCE.md)

### Example Projects
- [Week 1 Content Pack](spherevista360_week1_final/)
- [Sample Templates](templates/)
- [Configuration Examples](examples/)

## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/spv360/spherevista360.git
cd spherevista360
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Testing
```bash
# Run image validator tests
python -m pytest tests/test_image_validator.py

# Test WordPress connection
python wp_agent_bulk.py --test-connection
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Unsplash**: High-quality stock photography
- **WordPress REST API**: Powerful content management
- **Python Community**: Amazing libraries and tools
- **Contributors**: Everyone who helped improve this project

---

**SphereVista360** - Elevating WordPress content management with intelligent automation and advanced validation systems.

For support, feature requests, or contributions, please visit our [GitHub repository](https://github.com/spv360/spherevista360).