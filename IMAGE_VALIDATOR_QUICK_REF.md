# Image Validator Quick Reference

## 🔍 Validation Checklist

### ✅ Quality Standards
- **Resolution**: ≥1200x800 (local), ≥600x400 (remote)
- **Aspect Ratio**: 0.5 to 2.0
- **File Size**: 100KB to 5MB
- **Format**: JPEG, PNG, WebP

### ✅ SEO Requirements
- **Alt Text**: 3+ words, <125 characters
- **Title**: Descriptive and relevant
- **Filename**: lowercase-with-hyphens
- **Metadata**: Complete attribution

### ✅ Copyright Compliance
- **Source**: Verified free stock sites
- **License**: CC0, Public Domain, Commercial use
- **Attribution**: Proper credit when required
- **Usage Rights**: Clear commercial permissions

### ✅ Content Relevance
- **Category Match**: Keywords align with content
- **OCR Analysis**: Text within image relevant
- **Context**: Image supports article topic
- **Quality**: Professional appearance

## 🏷️ Category Keywords

| Category | Primary Keywords |
|----------|------------------|
| **Finance** | stock, market, trading, investment, banking, money, chart |
| **Tech** | software, AI, cloud, programming, automation, digital |
| **World** | geography, culture, politics, global, international |
| **Travel** | destination, tourism, vacation, hotel, transportation |
| **Politics** | government, election, policy, leadership, democracy |

## 📊 Validation Messages

### 🟢 Success Indicators
```
✅ Image is unique
✅ Verified free stock: unsplash.com
✅ Good resolution
✅ Good relevance (2.5): Good aspect ratio; Matches 2 category keywords
```

### 🟡 Warnings
```
⚠️ Missing metadata: description, caption
⚠️ Alt text too short
⚠️ Low relevance (0.5): Consider more relevant image
```

### 🔴 Errors
```
❌ Duplicate image detected
❌ Image resolution too low: 400x300
❌ Copyright check failed: Usage rights unclear
```

## 🛠️ Quick Commands

```bash
# Basic validation test
python -c "
from image_validator import ImageValidator
validator = ImageValidator()
result = validator.validate_image(Path('image.jpg'), 'Tech', ['ai'])
print(result)
"

# Find best image in folder
python -c "
from image_validator import find_best_image
best = find_best_image(Path('images/'), 'Finance', ['stock'])
print(f'Best match: {best}')
"

# Test with WordPress upload
python wp_agent_bulk.py ./content --publish --top-image
```

## 🎯 Best Practices

### For Images
1. **Use descriptive filenames**: `ai-finance-chart-2025.jpg` not `img1.jpg`
2. **Choose relevant stock photos**: Match content topic and tone
3. **Optimize file size**: Balance quality and loading speed
4. **Include alt text**: Descriptive, keyword-rich, accessible

### For Content
1. **Match categories**: Align images with article categories
2. **Add metadata**: Complete title, caption, description fields
3. **Source responsibly**: Use verified free stock sites
4. **Check relevance**: Ensure images support content message

## 🔧 Configuration

### Customize Validation
```python
# In image_validator.py
self.min_width = 800          # Lower for blogs
self.min_height = 600         # Lower for blogs
self.required_meta = {'alt_text', 'title'}  # Minimal requirements
```

### Add Custom Keywords
```python
self.category_keywords['Custom'] = [
    'your', 'specific', 'keywords', 'here'
]
```

### Adjust Scoring
```python
# In get_image_score method
score += 2.0 if high_priority_match else 0.5
```

## 🚨 Troubleshooting

### Common Issues

**"OCR failed"** → Install tesseract: `sudo apt-get install tesseract-ocr`

**"Low relevance score"** → Use more specific keywords or better matching images

**"Missing metadata"** → Add alt text and title to image metadata

**"Copyright unclear"** → Source from verified free stock sites

**"Duplicate detected"** → Use different image or check hash database

### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test specific validation
validator = ImageValidator()
score, reasons = validator.get_image_score(path, category, keywords)
print(f"Score: {score}, Reasons: {reasons}")
```

## 📈 Performance Tips

1. **Batch Processing**: Process multiple images together
2. **Cache Results**: Store validation results to avoid re-processing
3. **Optimize Images**: Use appropriate resolution and compression
4. **Smart Defaults**: Provide fallback metadata for faster processing
5. **Monitor Logs**: Watch for patterns in validation failures

This quick reference covers the essential aspects of the SphereVista360 Image Validator for efficient content publishing.