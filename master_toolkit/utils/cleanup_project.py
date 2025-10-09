#!/usr/bin/env python3
"""
Project Cleanup Script
=====================
Clean up unnecessary scripts and organize the project structure.
"""

import os
import shutil
from pathlib import Path


def cleanup_project():
    """Clean up the project structure."""
    print("🧹 STARTING PROJECT CLEANUP")
    print("=" * 50)
    
    # Files and directories to archive
    dirs_to_archive = [
        'tools',
        'wp_tools', 
        'wordpress-enhancements',
        'scripts',
        'spherevista360_week1_final_backup',
        'spherevista360_week2_final'
    ]
    
    files_to_archive = [
        'debug_auth.py',
        'test_core_client.py',
        'merge_content_by_category.py',
        'build_week2_zip.py',
        'setup_tools.sh',
        'basic',
        'spherevista360_week2_final.zip'
    ]
    
    # Create archive directory
    archive_dir = Path('archived_old_tools')
    archive_dir.mkdir(exist_ok=True)
    
    print(f"📦 Archiving old tools to {archive_dir}/")
    
    # Archive directories
    for dir_name in dirs_to_archive:
        dir_path = Path(dir_name)
        if dir_path.exists():
            archive_path = archive_dir / dir_name
            if archive_path.exists():
                shutil.rmtree(archive_path)
            shutil.move(str(dir_path), str(archive_path))
            print(f"  ✅ Archived {dir_name}/")
    
    # Archive files
    for file_name in files_to_archive:
        file_path = Path(file_name)
        if file_path.exists():
            archive_path = archive_dir / file_name
            if archive_path.exists():
                os.remove(archive_path)
            shutil.move(str(file_path), str(archive_path))
            print(f"  ✅ Archived {file_name}")
    
    # Clean up content directories
    print("\n📁 ORGANIZING CONTENT")
    print("-" * 30)
    
    # Ensure published_content exists
    published_dir = Path('published_content')
    if not published_dir.exists():
        published_dir.mkdir()
        
        # Move content_to_publish to published_content
        content_to_publish = Path('content_to_publish')
        if content_to_publish.exists():
            for item in content_to_publish.iterdir():
                shutil.move(str(item), str(published_dir / item.name))
            content_to_publish.rmdir()
            print("  ✅ Moved content_to_publish to published_content")
    
    # Clean up docs
    docs_dir = Path('docs')
    if docs_dir.exists():
        # Keep only essential docs
        essential_docs = ['README.md', 'reports']
        archive_docs = archive_dir / 'docs'
        archive_docs.mkdir(exist_ok=True)
        
        for item in docs_dir.iterdir():
            if item.name not in essential_docs:
                archive_path = archive_docs / item.name
                if archive_path.exists():
                    if archive_path.is_dir():
                        shutil.rmtree(archive_path)
                    else:
                        os.remove(archive_path)
                shutil.move(str(item), str(archive_path))
                print(f"  ✅ Archived docs/{item.name}")
    
    print("\n📊 CLEANUP SUMMARY")
    print("-" * 30)
    print(f"✅ Archived {len(dirs_to_archive)} directories")
    print(f"✅ Archived {len(files_to_archive)} files")
    print("✅ Organized content structure")
    print("✅ Cleaned up documentation")
    
    # Show current clean structure
    print("\n📂 CLEAN PROJECT STRUCTURE")
    print("-" * 30)
    current_items = []
    for item in Path('.').iterdir():
        if item.name.startswith('.'):
            continue
        if item.is_dir():
            current_items.append(f"📁 {item.name}/")
        else:
            current_items.append(f"📄 {item.name}")
    
    for item in sorted(current_items)[:15]:  # Show first 15 items
        print(f"  {item}")
    
    print("\n🎯 ACTIVE TOOLS STRUCTURE")
    print("-" * 30)
    print("📁 master_toolkit/")
    print("  ├── core/           # Authentication, API client")
    print("  ├── content/        # Publishing, workflows")
    print("  ├── validation/     # Links, images, SEO")
    print("  ├── utils/          # Common utilities")
    print("  └── cli/            # Command-line tools")
    print("")
    print("📁 published_content/")
    print("  ├── Business/")
    print("  ├── Entertainment/")
    print("  ├── Finance/")
    print("  ├── Politics/")
    print("  ├── Technology/")
    print("  ├── Travel/")
    print("  └── World/")


if __name__ == "__main__":
    cleanup_project()
    print("\n🎉 CLEANUP COMPLETED!")
    print("The project is now clean and organized.")
    print("\nNext steps:")
    print("1. Test the website: python3 comprehensive_website_tester.py")
    print("2. Use master toolkit: python3 master_toolkit/cli/validate.py --help")
    print("3. Review content: ls published_content/")