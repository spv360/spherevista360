#!/bin/bash

# WordPress Content Setup Script
# This script creates instructions and tools to set up your theme properly

echo "🔧 WordPress Theme Content Setup Guide"
echo "======================================"

# Create a comprehensive setup guide
cat > "/tmp/wordpress_setup_guide.md" << 'EOF'
# SphereVista360 Theme Setup Guide

Your theme is working but needs content and configuration! Here's how to set everything up:

## 🏠 STEP 1: Create Homepage Content

### Option A: Static Homepage (Recommended)
1. **Go to**: WordPress Admin > Pages > Add New
2. **Create a page called**: "Homepage" or "Home"
3. **Add content** like:
   ```
   Welcome to SphereVista360
   
   Your trusted source for finance and technology insights.
   
   Explore our latest articles and discover cutting-edge solutions for your business.
   ```
4. **Publish the page**
5. **Go to**: Settings > Reading
6. **Set**: "Your homepage displays" to "A static page"
7. **Choose**: Your new homepage

### Option B: Blog Homepage
1. **Go to**: Settings > Reading  
2. **Set**: "Your homepage displays" to "Your latest posts"
3. **Make sure you have some blog posts published**

## 📋 STEP 2: Create Main Menu

### Create Primary Navigation:
1. **Go to**: Appearance > Menus
2. **Click**: "Create a new menu"
3. **Name it**: "Primary Navigation"
4. **Add pages**:
   - Home
   - About
   - Services  
   - Blog
   - Contact
5. **Assign to**: "Primary" location
6. **Save Menu**

### Quick Pages to Create:
- **About**: Tell your story
- **Services**: What you offer
- **Blog**: For your articles (if not using homepage)
- **Contact**: Contact information
- **Privacy Policy**: Required for most sites

## 🖼️ STEP 3: Add Images and Logo

### Site Logo:
1. **Go to**: Appearance > Customize > Site Identity
2. **Upload**: Your logo
3. **Set**: Site title and tagline
4. **Save**

### Featured Images for Posts:
1. **Edit each blog post**
2. **Set Featured Image** (appears in cards)
3. **Use professional images** related to finance/tech

### Header Images:
- The theme supports header images
- Go to: Appearance > Customize > Header Image

## 🎨 STEP 4: Configure Theme Colors

1. **Go to**: Appearance > Customize > Colors
2. **Adjust**:
   - Primary color (currently blue #667eea)
   - Secondary color (currently purple #764ba2)
   - Text colors
3. **Preview** changes
4. **Publish** when satisfied

## 📱 STEP 5: Set Up Widgets

1. **Go to**: Appearance > Widgets
2. **Add widgets to**:
   - **Footer Widget Area 1**: About text, contact info
   - **Footer Widget Area 2**: Recent posts or categories
   - **Footer Widget Area 3**: Social media links

### Recommended Widgets:
- **Text Widget**: For about/contact info
- **Recent Posts**: Show latest articles
- **Categories**: Help navigation
- **Social Icons**: If you have social accounts

## 📝 STEP 6: Create Sample Content

### Blog Posts:
Create a few sample posts about:
- "Future of Financial Technology"
- "Digital Transformation in Finance"
- "AI in Investment Management"

### Pages:
- **About**: Your expertise and mission
- **Services**: What you offer clients
- **Contact**: Contact form and information

## 🔧 STEP 7: Enable Theme Features

### Dark Mode:
- Should automatically appear in header
- Test by clicking the dark mode toggle

### Search:
- Use the search form in the header
- Test with keywords from your content

### Social Sharing:
- Will appear automatically on blog posts
- Customize in theme settings if available

## ⚡ STEP 8: Performance Optimization

1. **Install recommended plugins**:
   - Yoast SEO (for search optimization)
   - Contact Form 7 (for contact forms)
   - WP Super Cache (for speed)

2. **Set up caching**:
   - Install a caching plugin
   - Enable compression

## 🎯 IMMEDIATE TODO LIST:

□ Create homepage content
□ Set up main menu (5-7 items)
□ Upload site logo
□ Create About and Contact pages
□ Add 2-3 sample blog posts with featured images
□ Configure footer widgets
□ Test all theme features

## 🚨 TROUBLESHOOTING:

**No menu showing?**
- Check Appearance > Menus > Menu Settings
- Ensure menu is assigned to "Primary" location

**No images?**
- Add featured images to posts
- Upload logo in Customizer
- Check image file sizes (optimize if needed)

**Plain appearance?**
- Verify SphereVista360 theme is active
- Check Appearance > Customize for options
- Ensure posts have content and images

**Missing content?**
- Create pages and posts
- Set up homepage in Settings > Reading
- Add content to widgets
EOF

# Create a quick content creation script
cat > "/tmp/sample_content.txt" << 'EOF'
SAMPLE CONTENT FOR YOUR WEBSITE:

=== HOMEPAGE CONTENT ===
Title: Welcome to SphereVista360

Content:
Welcome to SphereVista360 - Your Gateway to Financial Innovation

At SphereVista360, we provide cutting-edge insights into the intersection of finance and technology. Our expert analysis helps businesses navigate the rapidly evolving financial landscape.

🔹 Financial Technology Insights
🔹 Investment Strategy Analysis  
🔹 Digital Transformation Guidance
🔹 Market Intelligence Reports

Explore our latest articles and discover how technology is reshaping the future of finance.

=== ABOUT PAGE ===
Title: About SphereVista360

Content:
SphereVista360 is a leading source of financial technology insights and analysis. Our team of experts combines deep industry knowledge with cutting-edge technology understanding to deliver actionable intelligence.

Our Mission:
To empower businesses and individuals with the knowledge they need to thrive in the digital financial ecosystem.

Our Expertise:
- Financial Technology (FinTech)
- Digital Banking Solutions
- Investment Management
- Regulatory Technology (RegTech)
- Blockchain and Cryptocurrency
- AI in Finance

=== SERVICES PAGE ===
Title: Our Services

Content:
SphereVista360 offers comprehensive financial technology consulting and analysis services:

✅ Market Research & Analysis
In-depth research on emerging financial technologies and market trends.

✅ Technology Strategy Consulting
Strategic guidance for financial institutions adopting new technologies.

✅ Investment Intelligence
Data-driven insights for informed investment decisions.

✅ Regulatory Compliance
Navigate complex regulatory requirements in the digital age.

Contact us to learn how we can help your organization succeed.

=== CONTACT PAGE ===
Title: Contact Us

Content:
Get in Touch with SphereVista360

We'd love to hear from you. Contact us for inquiries about our services, partnership opportunities, or media requests.

📧 Email: contact@spherevista360.com
📞 Phone: [Your Phone Number]
🌐 Web: www.spherevista360.com

Business Hours:
Monday - Friday: 9:00 AM - 6:00 PM
Saturday: 10:00 AM - 2:00 PM
Sunday: Closed

=== SAMPLE BLOG POSTS ===

Post 1:
Title: "The Future of Digital Banking: Trends to Watch in 2025"
Excerpt: Explore the latest innovations reshaping the banking industry, from AI-powered customer service to blockchain-based transactions.

Post 2: 
Title: "AI in Investment Management: Opportunities and Challenges"
Excerpt: How artificial intelligence is transforming investment strategies and what it means for portfolio management.

Post 3:
Title: "Regulatory Technology: Streamlining Compliance in Finance"
Excerpt: Discover how RegTech solutions are helping financial institutions navigate complex regulatory landscapes more efficiently.
EOF

echo "✅ Setup guide created: /tmp/wordpress_setup_guide.md"
echo "✅ Sample content created: /tmp/sample_content.txt"

# Copy to downloads
cp /tmp/wordpress_setup_guide.md ~/downloads/
cp /tmp/sample_content.txt ~/downloads/

echo
echo "📋 IMMEDIATE ACTION PLAN:"
echo "========================"
echo
echo "Your theme is working but needs content! Here's what to do RIGHT NOW:"
echo
echo "1. 🏠 CREATE HOMEPAGE:"
echo "   • Go to: WordPress Admin > Pages > Add New"
echo "   • Title: 'Homepage' or 'Home'"  
echo "   • Add welcome content (see sample_content.txt)"
echo "   • Publish"
echo
echo "2. 📋 SET UP MENU:"
echo "   • Go to: Appearance > Menus"
echo "   • Create menu: 'Primary Navigation'"
echo "   • Add pages: Home, About, Services, Blog, Contact"
echo "   • Assign to: 'Primary' location"
echo
echo "3. 🖼️ ADD LOGO:"
echo "   • Go to: Appearance > Customize > Site Identity"
echo "   • Upload your logo"
echo "   • Set site title and tagline"
echo
echo "4. 📝 CREATE CONTENT:"
echo "   • Create About, Services, Contact pages"
echo "   • Add 2-3 blog posts with featured images"
echo "   • Use the sample content provided"
echo
echo "5. ⚙️ SET HOMEPAGE:"
echo "   • Go to: Settings > Reading"
echo "   • Set 'A static page' as homepage"
echo "   • Choose your Homepage"
echo
echo "📁 Files created in ~/downloads/:"
echo "   • wordpress_setup_guide.md (detailed instructions)"
echo "   • sample_content.txt (ready-to-use content)"
echo
echo "🚀 Once you add content, your theme will look amazing!"
echo "   Your professional design is there - it just needs content to display!"