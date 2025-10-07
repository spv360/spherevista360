#!/usr/bin/env python3
"""
Content Title Fixer
Adds proper H1 titles to articles that are missing them and improves content structure
"""

import os
import re
from typing import Dict, List

class ContentTitleFixer:
    def __init__(self):
        self.content_path = "/home/kddevops/projects/spherevista360/spherevista360_week1_final"
        self.backup_path = "/home/kddevops/projects/spherevista360/spherevista360_week1_final_backup"
        
        # Files that need title fixes (identified from verification)
        self.files_to_fix = [
            "Finance/01-ai-transforming-investing-2025.md",
            "Finance/02-global-inflation-trends-2025.md", 
            "Finance/03-digital-banking-future-fintech.md",
            "Finance/business_01-startup-funding-trends-2025.md",
            "Technology/01-cloud-wars-2025-aws-azure-gcp.md",
            "Technology/02-generative-ai-tools-2025.md",
            "Technology/03-ai-cybersecurity-automation.md",
            "Politics/01-ai-influencing-politics.md",
            "Travel/01-visa-free-destinations-2025.md",
            "Travel/02-digital-nomad-visas-2025.md",
            "World/01-us-india-trade-2025.md",
            "World/02-global-elections-2025.md"
        ]
    
    def extract_title_from_frontmatter(self, content: str) -> str:
        """Extract title from YAML frontmatter"""
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()
        return ""
    
    def has_h1_title(self, content: str) -> bool:
        """Check if content has H1 markdown title after frontmatter"""
        # Remove frontmatter first
        content_without_frontmatter = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        return bool(re.search(r'^#\s+', content_without_frontmatter, re.MULTILINE))
    
    def add_h1_title(self, content: str, title: str) -> str:
        """Add H1 title after frontmatter"""
        frontmatter_match = re.search(r'^(---\s*\n.*?\n---\s*\n)', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            rest_content = content[len(frontmatter):].strip()
            
            # Add H1 title
            return f"{frontmatter}\n# {title}\n\n{rest_content}"
        else:
            # No frontmatter, just add title at the beginning
            return f"# {title}\n\n{content.strip()}"
    
    def create_backup(self) -> bool:
        """Create backup of content before fixing"""
        try:
            import shutil
            if os.path.exists(self.backup_path):
                shutil.rmtree(self.backup_path)
            shutil.copytree(self.content_path, self.backup_path)
            print(f"✅ Backup created: {self.backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def fix_file_titles(self) -> Dict:
        """Fix titles in files that are missing them"""
        results = {
            'fixed': [],
            'skipped': [],
            'errors': []
        }
        
        for file_path in self.files_to_fix:
            full_path = os.path.join(self.content_path, file_path)
            
            try:
                # Read current content
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if already has H1 title
                if self.has_h1_title(content):
                    results['skipped'].append(file_path)
                    continue
                
                # Extract title from frontmatter
                title = self.extract_title_from_frontmatter(content)
                if not title:
                    results['errors'].append(f"{file_path}: No title found in frontmatter")
                    continue
                
                # Add H1 title
                fixed_content = self.add_h1_title(content, title)
                
                # Write back to file
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                results['fixed'].append(file_path)
                print(f"✅ Fixed: {file_path} - Added title: '{title}'")
                
            except Exception as e:
                results['errors'].append(f"{file_path}: {str(e)}")
                print(f"❌ Error fixing {file_path}: {e}")
        
        return results
    
    def verify_fixes(self) -> Dict:
        """Verify that fixes were applied correctly"""
        verification = {
            'success': [],
            'still_missing': [],
            'errors': []
        }
        
        for file_path in self.files_to_fix:
            full_path = os.path.join(self.content_path, file_path)
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if self.has_h1_title(content):
                    verification['success'].append(file_path)
                else:
                    verification['still_missing'].append(file_path)
                    
            except Exception as e:
                verification['errors'].append(f"{file_path}: {str(e)}")
        
        return verification
    
    def run_title_fixes(self) -> bool:
        """Run the complete title fixing process"""
        print("🔧 Content Title Fixer")
        print("=" * 40)
        
        # Create backup
        print("💾 Creating backup...")
        if not self.create_backup():
            print("❌ Backup failed - aborting fixes")
            return False
        
        # Fix titles
        print(f"\n🔧 Fixing {len(self.files_to_fix)} files...")
        results = self.fix_file_titles()
        
        # Verify fixes
        print(f"\n🔍 Verifying fixes...")
        verification = self.verify_fixes()
        
        # Report results
        print(f"\n📊 TITLE FIX RESULTS")
        print("=" * 40)
        print(f"✅ Successfully Fixed: {len(results['fixed'])}")
        print(f"⏭️ Already Had Titles: {len(results['skipped'])}")
        print(f"❌ Errors: {len(results['errors'])}")
        
        if results['errors']:
            print(f"\n❌ Errors encountered:")
            for error in results['errors']:
                print(f"   • {error}")
        
        print(f"\n🔍 VERIFICATION RESULTS")
        print("=" * 40)
        print(f"✅ Titles Now Present: {len(verification['success'])}")
        print(f"❌ Still Missing Titles: {len(verification['still_missing'])}")
        
        if verification['still_missing']:
            print(f"\n⚠️ Files still missing titles:")
            for file in verification['still_missing']:
                print(f"   • {file}")
        
        success = len(verification['still_missing']) == 0 and len(results['errors']) == 0
        
        if success:
            print(f"\n🎉 All title fixes completed successfully!")
        else:
            print(f"\n⚠️ Some issues remain that need manual attention")
        
        print(f"\n💾 Backup available at: {self.backup_path}")
        
        return success

def main():
    """Main function"""
    try:
        fixer = ContentTitleFixer()
        success = fixer.run_title_fixes()
        
        if success:
            print(f"\n✅ Title fixing completed successfully!")
            print(f"\n📋 Next Steps:")
            print("1. Run content verification again to confirm fixes")
            print("2. Review the updated content structure")
            print("3. Proceed with WordPress publishing")
        else:
            print(f"\n⚠️ Title fixing completed with some issues")
            print("Review the errors above and fix manually if needed")
            
    except Exception as e:
        print(f"❌ Title fixing failed: {e}")

if __name__ == "__main__":
    main()