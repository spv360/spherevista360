#!/usr/bin/env python3
"""
Website Navigation Optimizer for AdSense
========================================
Optimize WordPress navigation structure for better Google AdSense performance.
- Categories in top navigation for content discovery
- Info pages in footer for compliance
- Clean structure for optimal ad placement
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add the master_toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from master_toolkit.core import WordPressClient
from master_toolkit.core.config import config
from master_toolkit.utils import print_success, print_error, print_warning, print_info


class NavigationOptimizer:
    """Optimize website navigation for AdSense performance."""
    
    def __init__(self):
        """Initialize the navigation optimizer."""
        self.wp = None
        self.categories = []
        self.pages = []
        
    def setup_client(self):
        """Setup WordPress client."""
        print_info("🔧 Setting up WordPress client...")
        
        try:
            self.wp = WordPressClient()
            self.wp.authenticate()
            print_success("✅ WordPress connected successfully")
            return True
        except Exception as e:
            print_error(f"❌ WordPress setup failed: {str(e)}")
            return False
    
    def analyze_current_structure(self):
        """Analyze current website structure."""
        print_info("\n📊 Analyzing current website structure...")
        
        try:
            # Get all categories
            self.categories = self.wp.get_categories()
            print_success(f"✅ Found {len(self.categories)} categories")
            
            # Get all pages  
            self.pages = self.wp.get_pages(per_page=50)
            print_success(f"✅ Found {len(self.pages)} pages")
            
            # Analyze categories
            content_categories = []
            empty_categories = []
            
            for cat in self.categories:
                if cat.get('count', 0) > 0 and cat.get('name') != 'Uncategorized':
                    content_categories.append(cat)
                elif cat.get('name') != 'Uncategorized':
                    empty_categories.append(cat)
            
            print_info(f"\n🎯 Category Analysis:")
            print_info(f"   Categories with content: {len(content_categories)}")
            print_info(f"   Empty categories: {len(empty_categories)}")
            
            # Show top categories by content
            content_categories.sort(key=lambda x: x.get('count', 0), reverse=True)
            print_info(f"\n📈 Top Categories by Content:")
            for cat in content_categories[:8]:
                print_info(f"   - {cat.get('name')}: {cat.get('count')} posts")
            
            # Analyze pages for footer placement
            info_pages = []
            functional_pages = []
            
            for page in self.pages:
                title = page.get('title', {}).get('rendered', '').lower()
                if any(keyword in title for keyword in ['privacy', 'terms', 'disclaimer', 'about', 'contact']):
                    info_pages.append(page)
                else:
                    functional_pages.append(page)
            
            print_info(f"\n📄 Page Analysis:")
            print_info(f"   Info pages (for footer): {len(info_pages)}")
            print_info(f"   Functional pages: {len(functional_pages)}")
            
            return {
                'content_categories': content_categories,
                'empty_categories': empty_categories,
                'info_pages': info_pages,
                'functional_pages': functional_pages
            }
            
        except Exception as e:
            print_error(f"❌ Analysis failed: {str(e)}")
            return None
    
    def generate_navigation_structure(self, analysis):
        """Generate optimal navigation structure for AdSense."""
        print_info("\n🎯 Generating optimal navigation structure...")
        
        # Top navigation categories (main content categories)
        top_nav_categories = []
        content_categories = analysis['content_categories']
        
        # Priority categories for AdSense (high traffic potential)
        priority_keywords = [
            'technology', 'tech', 'finance', 'business', 'travel', 
            'entertainment', 'politics', 'economy', 'investment', 'ai',
            'cryptocurrency', 'startup', 'market', 'global'
        ]
        
        # Sort categories by priority and content count
        def category_priority(cat):
            name = cat.get('name', '').lower()
            count = cat.get('count', 0)
            
            # Boost priority for AdSense-friendly categories
            priority_boost = 0
            for keyword in priority_keywords:
                if keyword in name:
                    priority_boost = 100
                    break
            
            return count + priority_boost
        
        sorted_categories = sorted(content_categories, key=category_priority, reverse=True)
        
        # Select top 8-10 categories for navigation
        top_nav_categories = sorted_categories[:8]
        
        print_info(f"🔝 Recommended Top Navigation Categories:")
        for i, cat in enumerate(top_nav_categories, 1):
            print_info(f"   {i}. {cat.get('name')} ({cat.get('count')} posts)")
        
        # Footer pages (compliance and info)
        footer_pages = analysis['info_pages']
        
        print_info(f"\n🦶 Recommended Footer Pages:")
        for page in footer_pages:
            title = page.get('title', {}).get('rendered', '')
            print_info(f"   - {title}")
        
        # Additional recommendations
        recommendations = self.generate_adsense_recommendations(analysis)
        
        return {
            'top_navigation': top_nav_categories,
            'footer_pages': footer_pages,
            'functional_pages': analysis['functional_pages'],
            'recommendations': recommendations
        }
    
    def generate_adsense_recommendations(self, analysis):
        """Generate specific AdSense optimization recommendations."""
        recommendations = []
        
        content_categories = analysis['content_categories']
        
        # Check for AdSense-friendly categories
        adsense_friendly = ['Technology', 'Finance', 'Business', 'Travel', 'Health', 'Education']
        missing_categories = []
        
        existing_names = [cat.get('name', '') for cat in content_categories]
        for friendly_cat in adsense_friendly:
            if not any(friendly_cat.lower() in name.lower() for name in existing_names):
                missing_categories.append(friendly_cat)
        
        if missing_categories:
            recommendations.append({
                'type': 'category_expansion',
                'title': 'Create High-Value Categories',
                'description': f"Consider adding these AdSense-friendly categories: {', '.join(missing_categories)}",
                'priority': 'high'
            })
        
        # Check for empty categories cleanup
        empty_cats = analysis['empty_categories']
        if len(empty_cats) > 3:
            recommendations.append({
                'type': 'cleanup',
                'title': 'Remove Empty Categories',
                'description': f"Remove {len(empty_cats)} empty categories to clean up navigation",
                'priority': 'medium'
            })
        
        # Navigation depth recommendation
        if len(content_categories) > 10:
            recommendations.append({
                'type': 'navigation',
                'title': 'Optimize Navigation Depth',
                'description': "Consider grouping categories into parent/child relationships for better UX",
                'priority': 'medium'
            })
        
        # Page structure recommendations
        info_pages = analysis['info_pages']
        required_pages = ['Privacy Policy', 'Terms of Service', 'About Us', 'Contact Us']
        
        existing_page_titles = [p.get('title', {}).get('rendered', '').lower() for p in info_pages]
        missing_pages = []
        
        for required in required_pages:
            if not any(required.lower() in title for title in existing_page_titles):
                missing_pages.append(required)
        
        if missing_pages:
            recommendations.append({
                'type': 'compliance',
                'title': 'Add Required Pages for AdSense',
                'description': f"Missing pages: {', '.join(missing_pages)}",
                'priority': 'high'
            })
        
        return recommendations
    
    def generate_navigation_code(self, structure):
        """Generate navigation code for WordPress theme."""
        print_info("\n💻 Generating navigation code...")
        
        # Generate top navigation HTML
        top_nav_html = self.generate_top_navigation_html(structure['top_navigation'])
        
        # Generate footer HTML
        footer_html = self.generate_footer_html(structure['footer_pages'])
        
        # Generate CSS for AdSense optimization
        adsense_css = self.generate_adsense_css()
        
        return {
            'top_navigation_html': top_nav_html,
            'footer_html': footer_html,
            'adsense_css': adsense_css,
            'php_functions': self.generate_php_functions()
        }
    
    def generate_top_navigation_html(self, categories):
        """Generate HTML for top navigation."""
        base_url = config.get('base_url')
        
        html = """
<!-- Optimized Top Navigation for AdSense -->
<nav class="main-navigation adsense-optimized" role="navigation">
    <div class="nav-container">
        <ul class="nav-menu" id="primary-menu">
            <li class="nav-item">
                <a href="{base_url}" class="nav-link">Home</a>
            </li>
""".format(base_url=base_url)
        
        for cat in categories:
            cat_name = cat.get('name', '')
            cat_slug = cat.get('slug', '')
            cat_url = f"{base_url}/category/{cat_slug}/"
            
            html += f"""            <li class="nav-item">
                <a href="{cat_url}" class="nav-link">{cat_name}</a>
            </li>
"""
        
        html += """        </ul>
    </div>
</nav>
"""
        return html
    
    def generate_footer_html(self, pages):
        """Generate HTML for footer with info pages."""
        base_url = config.get('base_url')
        
        html = """
<!-- AdSense Compliant Footer -->
<footer class="site-footer adsense-footer">
    <div class="footer-container">
        <div class="footer-section footer-links">
            <h4>Information</h4>
            <ul class="footer-menu">
"""
        
        for page in pages:
            title = page.get('title', {}).get('rendered', '')
            page_url = page.get('link', '')
            
            html += f"""                <li><a href="{page_url}">{title}</a></li>
"""
        
        html += f"""            </ul>
        </div>
        
        <div class="footer-section footer-about">
            <h4>SphereVista360</h4>
            <p>Global insights on finance, technology, and business trends.</p>
        </div>
        
        <div class="footer-section footer-contact">
            <h4>Stay Connected</h4>
            <p>Follow us for the latest updates and insights.</p>
        </div>
    </div>
    
    <div class="footer-bottom">
        <div class="footer-container">
            <p>&copy; 2025 SphereVista360. All rights reserved.</p>
        </div>
    </div>
</footer>
"""
        return html
    
    def generate_adsense_css(self):
        """Generate CSS optimized for AdSense placement."""
        css = """
/* AdSense Optimized CSS */

/* Main Navigation */
.main-navigation.adsense-optimized {
    background: #ffffff;
    border-bottom: 1px solid #e1e5e9;
    padding: 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.nav-menu {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    align-items: center;
}

.nav-item {
    margin: 0;
}

.nav-link {
    display: block;
    padding: 15px 20px;
    color: #333;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.nav-link:hover {
    background-color: #f8f9fa;
    color: #007cba;
}

/* AdSense Ad Placement Zones */
.ad-zone {
    margin: 20px 0;
    text-align: center;
    min-height: 250px;
    background: #f8f9fa;
    border: 1px dashed #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ad-zone-top {
    margin-bottom: 30px;
}

.ad-zone-sidebar {
    margin: 20px 0;
    min-height: 600px;
}

.ad-zone-content {
    margin: 30px 0;
}

.ad-zone-footer {
    margin-top: 30px;
}

/* Footer Optimization */
.site-footer.adsense-footer {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 40px 0 20px;
    margin-top: 50px;
}

.footer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
}

.footer-section h4 {
    color: #3498db;
    margin-bottom: 15px;
    font-size: 18px;
}

.footer-menu {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-menu li {
    margin-bottom: 8px;
}

.footer-menu a {
    color: #bdc3c7;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-menu a:hover {
    color: #3498db;
}

.footer-bottom {
    background: #34495e;
    padding: 15px 0;
    margin-top: 30px;
    text-align: center;
    border-top: 1px solid #4a5f7a;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .nav-menu {
        flex-direction: column;
        background: white;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        display: none;
    }
    
    .nav-menu.active {
        display: flex;
    }
    
    .nav-link {
        padding: 12px 20px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .footer-container {
        grid-template-columns: 1fr;
        text-align: center;
    }
}

/* Content Layout for Better Ad Performance */
.content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 30px;
}

.main-content {
    min-width: 0;
}

.sidebar {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
}

@media (max-width: 968px) {
    .content-wrapper {
        grid-template-columns: 1fr;
    }
}
"""
        return css
    
    def generate_php_functions(self):
        """Generate PHP functions for WordPress theme."""
        php = """<?php
/**
 * AdSense Optimized Navigation Functions
 */

// Register navigation menus
function adsense_register_menus() {
    register_nav_menus(array(
        'primary' => 'Primary Navigation',
        'footer' => 'Footer Menu'
    ));
}
add_action('after_setup_theme', 'adsense_register_menus');

// Add AdSense ad zones
function insert_ad_zone($position = 'content') {
    $ad_zones = array(
        'top' => '<div class="ad-zone ad-zone-top"><!-- AdSense Top Ad --></div>',
        'content' => '<div class="ad-zone ad-zone-content"><!-- AdSense Content Ad --></div>',
        'sidebar' => '<div class="ad-zone ad-zone-sidebar"><!-- AdSense Sidebar Ad --></div>',
        'footer' => '<div class="ad-zone ad-zone-footer"><!-- AdSense Footer Ad --></div>'
    );
    
    return isset($ad_zones[$position]) ? $ad_zones[$position] : '';
}

// Optimize category display for AdSense
function get_adsense_categories($limit = 8) {
    $categories = get_categories(array(
        'orderby' => 'count',
        'order' => 'DESC',
        'number' => $limit,
        'hide_empty' => true,
        'exclude' => array(1) // Exclude 'Uncategorized'
    ));
    
    return $categories;
}

// Add AdSense-friendly meta tags
function adsense_meta_tags() {
    echo '<meta name="google-adsense-account" content="ca-pub-XXXXXXXXXX">' . "\\n";
    echo '<meta name="google-adsense-platform-account" content="ca-host-pub-XXXXXXXXXX">' . "\\n";
    echo '<meta name="ads.txt" content="/ads.txt">' . "\\n";
}
add_action('wp_head', 'adsense_meta_tags');

// Enqueue optimized styles
function adsense_styles() {
    wp_enqueue_style('adsense-nav', get_template_directory_uri() . '/css/adsense-navigation.css', array(), '1.0.0');
}
add_action('wp_enqueue_scripts', 'adsense_styles');
?>"""
        return php
    
    def save_optimization_files(self, navigation_code, structure):
        """Save all optimization files."""
        print_info("\n💾 Saving optimization files...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save HTML templates
        with open(f'navigation_html_{timestamp}.html', 'w') as f:
            f.write("<!-- Top Navigation HTML -->\n")
            f.write(navigation_code['top_navigation_html'])
            f.write("\n\n<!-- Footer HTML -->\n")
            f.write(navigation_code['footer_html'])
        
        # Save CSS
        with open(f'adsense_styles_{timestamp}.css', 'w') as f:
            f.write(navigation_code['adsense_css'])
        
        # Save PHP functions
        with open(f'adsense_functions_{timestamp}.php', 'w') as f:
            f.write(navigation_code['php_functions'])
        
        # Save complete report
        report = {
            'timestamp': datetime.now().isoformat(),
            'site_url': config.get('base_url'),
            'navigation_structure': {
                'top_categories': [
                    {
                        'name': cat.get('name'),
                        'slug': cat.get('slug'), 
                        'count': cat.get('count'),
                        'url': f"{config.get('base_url')}/category/{cat.get('slug')}/"
                    }
                    for cat in structure['top_navigation']
                ],
                'footer_pages': [
                    {
                        'title': page.get('title', {}).get('rendered'),
                        'url': page.get('link'),
                        'id': page.get('id')
                    }
                    for page in structure['footer_pages']
                ]
            },
            'recommendations': structure['recommendations'],
            'adsense_optimization': {
                'category_count': len(structure['top_navigation']),
                'footer_pages_count': len(structure['footer_pages']),
                'compliance_status': 'ready' if len(structure['footer_pages']) >= 4 else 'needs_work'
            }
        }
        
        with open(f'adsense_optimization_report_{timestamp}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print_success("✅ All optimization files saved!")
        print_info(f"📁 Files created:")
        print_info(f"   - navigation_html_{timestamp}.html")
        print_info(f"   - adsense_styles_{timestamp}.css") 
        print_info(f"   - adsense_functions_{timestamp}.php")
        print_info(f"   - adsense_optimization_report_{timestamp}.json")
        
        return f'adsense_optimization_report_{timestamp}.json'


def main():
    """Main optimization execution."""
    print_info("🚀 WEBSITE NAVIGATION OPTIMIZER FOR ADSENSE")
    print_info("=" * 60)
    
    optimizer = NavigationOptimizer()
    
    # Setup WordPress connection
    if not optimizer.setup_client():
        return False
    
    # Analyze current structure
    analysis = optimizer.analyze_current_structure()
    if not analysis:
        return False
    
    # Generate optimal structure
    structure = optimizer.generate_navigation_structure(analysis)
    
    # Generate code
    navigation_code = optimizer.generate_navigation_code(structure)
    
    # Save files
    report_file = optimizer.save_optimization_files(navigation_code, structure)
    
    # Display summary
    print_info("\n" + "="*70)
    print_info("📊 ADSENSE OPTIMIZATION SUMMARY")
    print_info("="*70)
    
    print_info(f"🔝 Top Navigation Categories ({len(structure['top_navigation'])}):")
    for cat in structure['top_navigation']:
        print_info(f"   - {cat.get('name')} ({cat.get('count')} posts)")
    
    print_info(f"\n🦶 Footer Pages ({len(structure['footer_pages'])}):")
    for page in structure['footer_pages']:
        print_info(f"   - {page.get('title', {}).get('rendered')}")
    
    print_info(f"\n💡 Recommendations ({len(structure['recommendations'])}):")
    for rec in structure['recommendations']:
        priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
        print_info(f"   {priority_icon} {rec['title']}: {rec['description']}")
    
    print_success("\n🎉 Website optimization for AdSense completed!")
    print_info(f"📄 Full report: {report_file}")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)