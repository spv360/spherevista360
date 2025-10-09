#!/usr/bin/env python3
"""
Merge spherevista360_week2_final to content_to_publish by categories
Preserves existing content and adds new content from week2
"""

import os
import shutil
from pathlib import Path

def merge_content_by_category():
    """Merge content from week2_final to content_to_publish by categories"""
    
    source_dir = Path("spherevista360_week2_final")
    target_dir = Path("content_to_publish")
    
    print("🔄 MERGING CONTENT BY CATEGORIES")
    print("=" * 50)
    print(f"Source: {source_dir}")
    print(f"Target: {target_dir}")
    print()
    
    # Categories to process
    categories = ["Business", "Entertainment", "Finance", "Politics", "Technology", "Travel", "World"]
    
    # Track merge statistics
    stats = {
        "total_files_copied": 0,
        "categories_processed": 0,
        "files_by_category": {}
    }
    
    for category in categories:
        source_category_dir = source_dir / category
        target_category_dir = target_dir / category
        
        print(f"📁 Processing {category}...")
        
        # Ensure target category directory exists
        target_category_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if source category has files
        if not source_category_dir.exists():
            print(f"   ⚠️ Source category {category} does not exist")
            continue
            
        source_files = list(source_category_dir.glob("*.md"))
        
        if not source_files:
            print(f"   ℹ️ No markdown files in source {category}")
            continue
        
        # List existing files in target
        existing_files = list(target_category_dir.glob("*.md"))
        print(f"   📋 Existing files in target: {len(existing_files)}")
        
        # Copy new files from source
        files_copied = 0
        for source_file in source_files:
            target_file = target_category_dir / source_file.name
            
            if target_file.exists():
                # Handle duplicate names by adding suffix
                base_name = source_file.stem
                extension = source_file.suffix
                counter = 1
                
                while target_file.exists():
                    new_name = f"{base_name}_week2_{counter}{extension}"
                    target_file = target_category_dir / new_name
                    counter += 1
                
                print(f"   📝 Copying (renamed): {source_file.name} → {target_file.name}")
            else:
                print(f"   📝 Copying: {source_file.name}")
            
            # Copy the file
            shutil.copy2(source_file, target_file)
            files_copied += 1
        
        stats["files_by_category"][category] = files_copied
        stats["total_files_copied"] += files_copied
        stats["categories_processed"] += 1
        
        print(f"   ✅ Copied {files_copied} files to {category}")
        print()
    
    # Final statistics
    print("📊 MERGE COMPLETE - STATISTICS")
    print("=" * 40)
    print(f"Categories processed: {stats['categories_processed']}")
    print(f"Total files copied: {stats['total_files_copied']}")
    print()
    
    print("Files copied by category:")
    for category, count in stats["files_by_category"].items():
        print(f"  {category}: {count} files")
    
    # Show final directory structure
    print(f"\n📁 FINAL CONTENT STRUCTURE:")
    print("-" * 30)
    
    for category in categories:
        category_dir = target_dir / category
        if category_dir.exists():
            files = list(category_dir.glob("*.md"))
            print(f"{category}: {len(files)} files")
            for file in sorted(files):
                print(f"  - {file.name}")
        print()
    
    return stats

def verify_merge():
    """Verify the merge was successful"""
    print("\n🔍 VERIFYING MERGE")
    print("=" * 30)
    
    source_dir = Path("spherevista360_week2_final")
    target_dir = Path("content_to_publish")
    
    # Count total files in both directories
    source_total = sum(len(list(category_dir.glob("*.md"))) 
                      for category_dir in source_dir.iterdir() 
                      if category_dir.is_dir())
    
    target_total = sum(len(list(category_dir.glob("*.md"))) 
                      for category_dir in target_dir.iterdir() 
                      if category_dir.is_dir())
    
    print(f"Source files (week2_final): {source_total}")
    print(f"Target files (content_to_publish): {target_total}")
    
    # Check if content was properly merged
    categories = ["Business", "Entertainment", "Finance", "Politics", "Technology", "Travel", "World"]
    
    print(f"\nCategory breakdown:")
    for category in categories:
        target_category_dir = target_dir / category
        if target_category_dir.exists():
            files = list(target_category_dir.glob("*.md"))
            print(f"  {category}: {len(files)} files")
    
    print(f"\n✅ Merge verification complete!")

if __name__ == "__main__":
    try:
        # Perform the merge
        stats = merge_content_by_category()
        
        # Verify the merge
        verify_merge()
        
        print(f"\n🎉 SUCCESS! Content merged successfully!")
        print(f"📝 {stats['total_files_copied']} files from week2_final added to content_to_publish")
        print(f"📁 All content organized by categories and ready for publishing")
        
    except Exception as e:
        print(f"\n❌ ERROR during merge: {e}")
        import traceback
        traceback.print_exc()