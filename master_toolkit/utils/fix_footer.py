#!/usr/bin/env python3
"""
Fix footer issues by creating a clean minimal footer
"""

import os

# Path to theme footer
THEME_PATH = '/home/kddevops/projects/spherevista360/spherevista-safe'
FOOTER_FILE = os.path.join(THEME_PATH, 'footer.php')

def create_minimal_footer():
    """Create a clean minimal footer"""
    
    minimal_footer = '''<?php
/**
 * Footer template - Minimal clean version
 * 
 * @package SphereVista Safe
 */
?>

</main><!-- #main -->
</div><!-- #content -->

<footer id="colophon" class="site-footer">
    <div class="site-info">
        <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.</p>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
'''
    
    print("=" * 80)
    print("🔧 FIXING FOOTER")
    print("=" * 80)
    print()
    
    # Backup existing footer
    if os.path.exists(FOOTER_FILE):
        backup_file = FOOTER_FILE + '.backup'
        with open(FOOTER_FILE, 'r') as f:
            content = f.read()
        with open(backup_file, 'w') as f:
            f.write(content)
        print(f"💾 Backed up existing footer to: {backup_file}")
    
    # Write new minimal footer
    with open(FOOTER_FILE, 'w') as f:
        f.write(minimal_footer)
    
    print(f"✅ Created minimal footer: {FOOTER_FILE}")
    print()
    print("Footer now contains:")
    print("  • Clean closing tags")
    print("  • Simple copyright line")
    print("  • No widgets or complex content")
    print()
    print("⚠️  You need to re-upload the theme:")
    print("   1. Zip the spherevista-safe folder")
    print("   2. Upload to WordPress")
    print("   3. Activate the theme")
    print()

if __name__ == '__main__':
    create_minimal_footer()
