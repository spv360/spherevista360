# SphereVista360 Image Validator - Advanced Features

## Overview

The SphereVista360 Image Validator is a sophisticated image validation system that ensures all images used in WordPress content publishing meet high standards for quality, SEO compliance, copyright verification, and content relevance.

## Key Features

### 🔍 **Quality Assurance**
- **Resolution Validation**: Ensures images meet minimum resolution requirements (1200x800 for local, 600x400 for remote)
- **Aspect Ratio Checking**: Validates proper aspect ratios (0.5 to 2.0)
- **File Size Optimization**: Checks file sizes are within optimal range (100KB - 5MB)
- **Format Support**: Validates JPEG, PNG, WebP formats

### 🏷️ **SEO Optimization**
- **Alt Text Validation**: Ensures descriptive alt text (3+ words, under 125 characters)
- **Metadata Requirements**: Validates title, caption, and description fields
- **URL-Friendly Filenames**: Checks for SEO-compliant naming (lowercase, hyphens only)
- **Descriptive Naming**: Prevents generic image names (img, photo, etc.)

### ⚖️ **Copyright Compliance**
- **Source Verification**: Validates images from known free stock sites (Unsplash, Pexels, Pixabay)
- **License Detection**: Checks for valid licenses (CC0, Public Domain, Creative Commons)
- **EXIF Analysis**: Examines embedded copyright information
- **Usage Rights**: Ensures commercial use permissions

### 🎯 **Content Relevance**
- **Category Matching**: Intelligent keyword matching for Finance, Tech, World, Travel, Politics
- **OCR Text Analysis**: Extracts and analyzes text within images (when Tesseract available)
- **Keyword Scoring**: Matches custom keywords with image content
- **Subcategory Support**: Detailed matching for specific topics within categories

### 🔄 **Duplicate Detection**
- **Perceptual Hashing**: Generates unique fingerprints for each image
- **Similarity Detection**: Prevents duplicate image usage
- **Hash Database**: Maintains registry of processed images

## Usage Examples

### Basic Validation
```python
from image_validator import ImageValidator

validator = ImageValidator()

# Validate a local image
is_valid, messages = validator.validate_image(
    image_path=Path('path/to/image.jpg'),
    category='Finance',
    keywords=['stock', 'market', 'trading'],
    metadata={
        'alt_text': 'Stock market chart showing upward trend',
        'title': 'Market Analysis Chart',
        'source_url': 'https://unsplash.com/photos/example'
    }
)

if is_valid:
    print("✅ Image validation passed!")
    for msg in messages:
        print(f"  • {msg}")
else:
    print("❌ Image validation failed:")
    for msg in messages:
        print(f"  • {msg}")
```

### Finding Best Image in Folder
```python
from image_validator import find_best_image

best_image = find_best_image(
    folder_path=Path('images/'),
    category='Tech',
    keywords=['ai', 'machine learning', 'automation']
)

if best_image:
    print(f"Best match: {best_image.name}")
```

### WordPress Integration
The validator is automatically integrated with the WordPress bulk uploader:

```bash
# Set environment variables
export WP_SITE="https://spherevista360.com"
export WP_USER="your_username"
export WP_APP_PASS="your app password"

# Upload with validation
python wp_agent_bulk.py ./content_folder --publish --top-image
```

## Validation Process

### 1. **Duplicate Check**
- Calculates perceptual hash
- Compares against existing image database
- Prevents duplicate uploads

### 2. **Copyright Verification**
- Checks source URL against known free stock sites
- Validates license information
- Examines EXIF copyright data
- Provides clear usage status

### 3. **SEO Compliance**
- Validates required metadata fields
- Checks alt text quality and length
- Ensures URL-friendly filenames
- Suggests improvements

### 4. **Quality Assessment**
- Measures resolution and aspect ratio
- Validates file size and format
- Checks technical specifications
- Provides quality scores

### 5. **Relevance Scoring**
- Matches against category keywords
- Analyzes custom keyword relevance
- Performs OCR text extraction
- Calculates relevance score

## Category Keywords

### Finance
- **Markets**: chart, graph, stock, market, trading, bull, bear, candlestick, trend
- **Banking**: bank, atm, credit, debit, card, payment, transaction, loan, mortgage
- **Investment**: investment, portfolio, dividend, mutual-fund, etf, broker, wealth

### Tech
- **Software**: software, programming, code, developer, app, application, website
- **Hardware**: computer, laptop, server, device, gadget, chip, processor
- **AI/ML**: ai, artificial-intelligence, machine-learning, robot, neural, automation

### World
- **Geography**: globe, map, world, continent, country, border, geography, terrain
- **Urban**: city, skyline, building, street, urban, downtown, metropolis
- **Culture**: culture, tradition, festival, celebration, heritage, art, music

### Travel
- **Transportation**: airplane, flight, airport, train, railway, bus, transportation
- **Accommodation**: hotel, resort, airbnb, apartment, villa, hostel, suite
- **Destinations**: beach, mountain, lake, park, monument, temple, museum

### Politics
- **Government**: government, parliament, congress, senate, court, ministry
- **Elections**: election, vote, ballot, polling, campaign, candidate, democracy
- **Leadership**: president, prime-minister, minister, governor, mayor, leader

## Configuration Options

### Quality Thresholds
```python
validator = ImageValidator()
validator.min_width = 1200          # Minimum width in pixels
validator.min_height = 800          # Minimum height in pixels
validator.min_file_size = 100 * 1024 # 100KB minimum
validator.max_file_size = 5 * 1024 * 1024 # 5MB maximum
```

### SEO Requirements
```python
validator.seo_filename_pattern = r'^[a-z0-9-]+$'  # URL-friendly pattern
validator.required_meta = {'alt_text', 'title'}   # Required metadata fields
```

### Copyright Sources
```python
validator.known_free_stock_sites = {
    'unsplash.com', 'pexels.com', 'pixabay.com',
    'freeimages.com', 'stocksnap.io'
}
```

## Validation Messages

### Success Indicators
- ✅ **"Image is unique"** - No duplicates detected
- ✅ **"Verified free stock: unsplash.com"** - Copyright verified
- ✅ **"Good resolution"** - Quality standards met
- ✅ **"Good relevance (2.5): Good aspect ratio; Matches 2 category keywords"**

### Warning Indicators
- ⚠️ **"Missing metadata: description, caption"** - SEO improvement needed
- ⚠️ **"Alt text too short"** - Needs more descriptive alt text
- ⚠️ **"Low relevance (0.5)"** - May not match content well

### Error Indicators
- ❌ **"Duplicate image detected"** - Image already used
- ❌ **"Image resolution too low"** - Below minimum requirements
- ❌ **"Copyright check failed"** - Usage rights unclear

## Integration with WordPress

The image validator seamlessly integrates with the WordPress bulk upload process:

1. **Automatic Validation**: All images are validated before upload
2. **Smart Fallbacks**: Provides intelligent defaults for missing metadata
3. **Quality Reports**: Detailed validation messages for each image
4. **Flexible Standards**: Different requirements for local vs remote images
5. **SEO Enhancement**: Automatically optimizes image attributes

## Best Practices

### For Content Creators
1. Use descriptive, keyword-rich filenames
2. Provide comprehensive alt text
3. Source images from verified free stock sites
4. Maintain consistent image quality standards
5. Choose images relevant to content topics

### For Developers
1. Configure validation thresholds based on use case
2. Monitor validation messages for quality insights
3. Implement custom keyword sets for specific domains
4. Regular database cleanup for hash storage
5. Test validation rules with sample content

## Troubleshooting

### Common Issues

**OCR Failed**: Install tesseract for text extraction
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

**Low Relevance Scores**: Add more specific keywords or choose more relevant images

**Copyright Warnings**: Ensure images are from verified free sources or provide license information

**SEO Issues**: Add comprehensive metadata including alt text, titles, and descriptions

## Performance Considerations

- **Caching**: Duplicate detection uses in-memory hash database
- **OCR**: Text extraction only when tesseract is available
- **Remote Images**: Temporary download for validation, automatic cleanup
- **Batch Processing**: Efficient handling of multiple images
- **Error Handling**: Graceful degradation on validation failures

This advanced image validation system ensures that all content published through SphereVista360 meets professional standards for quality, SEO, and legal compliance.