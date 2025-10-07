#!/usr/bin/env python3
"""
Complete Content Republishing and Validation Workflow
====================================================
Systematically republish content and run all validation tests.
"""

import os
import sys
import time
from pathlib import Path

# Add wp_tools to path
sys.path.append(str(Path(__file__).parent / 'wp_tools'))

from wp_client import WordPressClient, print_header, print_section


def run_command(command, description):
    """Run a command and report results."""
    print(f"\n🔧 {description}")
    print(f"Command: {command}")
    print("-" * 50)
    
    result = os.system(command)
    
    if result == 0:
        print(f"✅ {description} - SUCCESS")
        return True
    else:
        print(f"❌ {description} - FAILED (Exit code: {result})")
        return False


def main():
    """Main workflow function."""
    
    print_header("COMPLETE CONTENT REPUBLISHING & VALIDATION")
    print("🎯 This workflow will:")
    print("   1. Test publishing with dry-run")
    print("   2. Republish content systematically") 
    print("   3. Run duplicate detection")
    print("   4. Validate and fix images")
    print("   5. Run SEO validation")
    print("   6. Generate comprehensive reports")
    print()
    
    # Get authentication
    print("🔐 Authentication required for all operations")
    wp_client = WordPressClient()
    
    # Test authentication
    if not wp_client.authenticate():
        print("❌ Authentication failed. Cannot proceed.")
        return 1
    
    print("✅ Authentication successful! Proceeding with workflow...")
    
    # Phase 1: Dry run test
    print_section("PHASE 1: DRY RUN TEST")
    print("Testing publishing workflow without actually publishing...")
    
    success = run_command(
        "python wp_tools/content_publisher.py content_to_publish/Entertainment --dry-run",
        "Dry run test on Entertainment category"
    )
    
    if not success:
        print("❌ Dry run failed. Check publishing tool setup.")
        return 1
    
    # Ask for confirmation
    print("\n" + "="*60)
    proceed = input("🤔 Dry run successful. Proceed with actual publishing? (y/N): ").lower()
    
    if proceed != 'y':
        print("⏹️ Workflow stopped by user.")
        return 0
    
    # Phase 2: Systematic republishing
    print_section("PHASE 2: SYSTEMATIC REPUBLISHING")
    
    categories = [
        'Entertainment',  # Start with already optimized category
        'Technology',
        'Finance', 
        'Travel',
        'World',
        'Politics',
        'Business'
    ]
    
    published_categories = []
    
    for category in categories:
        category_dir = f"content_to_publish/{category}"
        
        if not os.path.exists(category_dir):
            print(f"⚠️ Skipping {category} - directory not found")
            continue
        
        print(f"\n📂 Publishing {category} category...")
        
        success = run_command(
            f"python wp_tools/content_publisher.py {category_dir} --category {category} --auto-optimize",
            f"Publishing {category} category with auto-optimization"
        )
        
        if success:
            published_categories.append(category)
            print(f"✅ {category} published successfully")
            
            # Brief pause between categories
            time.sleep(2)
        else:
            print(f"❌ Failed to publish {category}")
            
            # Ask whether to continue
            continue_choice = input(f"Continue with remaining categories? (y/N): ").lower()
            if continue_choice != 'y':
                break
    
    print(f"\n📊 PUBLISHING SUMMARY:")
    print(f"   ✅ Successfully published: {len(published_categories)} categories")
    print(f"   📋 Categories: {', '.join(published_categories)}")
    
    # Phase 3: Duplicate detection
    print_section("PHASE 3: DUPLICATE DETECTION")
    
    run_command(
        "python wp_tools/duplicate_checker.py --all",
        "Checking for duplicate posts and pages"
    )
    
    # Phase 4: Image validation
    print_section("PHASE 4: IMAGE VALIDATION & OPTIMIZATION")
    
    for category in published_categories:
        run_command(
            f"python wp_tools/image_tool.py --category {category} --fix --add-images --report {category.lower()}_images.txt",
            f"Image validation and optimization for {category}"
        )
    
    # Phase 5: SEO validation
    print_section("PHASE 5: SEO VALIDATION")
    
    for category in published_categories:
        run_command(
            f"python wp_tools/seo_tool.py --category {category} --report {category.lower()}_seo.txt",
            f"SEO validation for {category}"
        )
    
    # Overall SEO check
    run_command(
        "python wp_tools/seo_tool.py --report overall_seo_report.txt",
        "Overall SEO validation for all content"
    )
    
    # Phase 6: Link validation
    print_section("PHASE 6: LINK VALIDATION")
    
    run_command(
        "python wp_tools/link_tool.py --site-scan --max-pages 30 --report site_links.txt",
        "Site-wide link validation"
    )
    
    run_command(
        "python wp_tools/link_tool.py --menu --report menu_validation.txt",
        "Menu structure validation"
    )
    
    # Phase 7: Final verification
    print_section("PHASE 7: FINAL VERIFICATION")
    
    run_command(
        "python wp_tools/duplicate_checker.py --all --cleanup-commands",
        "Final duplicate check with cleanup recommendations"
    )
    
    # Generate summary report
    print_section("WORKFLOW COMPLETE - SUMMARY")
    
    print("📊 REPUBLISHING RESULTS:")
    print(f"   ✅ Categories published: {len(published_categories)}")
    print(f"   📋 Published categories: {', '.join(published_categories)}")
    
    print("\n📁 GENERATED REPORTS:")
    report_files = []
    
    # Check for generated reports
    for category in published_categories:
        seo_report = f"{category.lower()}_seo.txt"
        img_report = f"{category.lower()}_images.txt"
        
        if os.path.exists(seo_report):
            report_files.append(seo_report)
        if os.path.exists(img_report):
            report_files.append(img_report)
    
    # Overall reports
    overall_reports = [
        "overall_seo_report.txt",
        "site_links.txt", 
        "menu_validation.txt"
    ]
    
    for report in overall_reports:
        if os.path.exists(report):
            report_files.append(report)
    
    if report_files:
        for report in report_files:
            print(f"   📄 {report}")
    else:
        print("   ⚠️ No reports generated (check for errors)")
    
    print("\n🎉 WORKFLOW COMPLETE!")
    print("📋 Next steps:")
    print("   1. Review all generated reports")
    print("   2. Check website functionality")
    print("   3. Verify SEO scores improved")
    print("   4. Test site navigation and links")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())