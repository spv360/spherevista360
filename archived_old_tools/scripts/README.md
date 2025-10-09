# 📜 Scripts Directory

Organized collection of Python scripts for WordPress content management.

## 📁 Directory Structure

### 🚀 Active Scripts (`active/`)
Scripts currently in use and maintained:

#### **`content_manager.py`** - Content Inventory & Analysis
- **Purpose**: Analyze content directories and generate publishing plans
- **Usage**: `python3 scripts/active/content_manager.py analyze`
- **Status**: ✅ Active - provides content inventory and publishing insights
- **Features**:
  - Content directory analysis
  - Publishing plan generation
  - File size and count statistics
  - Category organization overview

### 📦 Archive Scripts
**All archived scripts have been moved to the consolidated archive directory:**
**`../archive_consolidated/`** - Single, organized archive with categorized structure

#### **Migration Information:**
- **Old Location**: `scripts/archive/` (removed)
- **New Location**: `../archive_consolidated/` (categorized by purpose)
- **Access**: See `../archive_consolidated/README.md` for navigation guide

#### **Script Categories in Consolidated Archive:**
- **Content Management** - Content tools and utilities
- **Workflows** - Process automation scripts  
- **Validation** - Quality assurance tools
- **Utilities** - General purpose utilities
- **Project Setup** - Build and deployment tools
- **Historical** - Complete backup of all scripts

## 🔄 Migration Guide

### **From Old Scripts to Enhanced Tools:**

```bash
# OLD: Basic republishing (archived)
# python3 republish_and_validate.py

# NEW: Enhanced workflow
python3 wp_tools/blog_workflow.py publish content_to_publish/Technology --category Technology
```

```bash
# OLD: Basic validation (archived)
# python3 test_republishing_readiness.py

# NEW: Comprehensive validation
python3 wp_tools/comprehensive_validator.py --category Entertainment
```

```bash
# OLD: Content verification (archived)
# python3 verify_content.py

# NEW: Enhanced publisher with verification
python3 wp_tools/enhanced_content_publisher.py content.md --category Technology --dry-run
```

## 📊 Script Status Summary

| Category | Active | Archived | Total |
|----------|--------|----------|-------|
| **Content Management** | 1 | 0* | 1 |
| **Archived Tools** | 0 | 0* | 0 |
| **Historical Tools** | 0 | 0* | 0 |
| **TOTAL** | **1** | **0** | **1** |

*All archived scripts moved to `../archive_consolidated/` with organized categorization

## 🎯 Recommended Usage

### **For Content Operations:**
- **Content Analysis**: `python3 scripts/active/content_manager.py analyze`
- **Publishing**: `python3 wp_tools/blog_workflow.py publish [directory] --category [category]`
- **Validation**: `python3 wp_tools/comprehensive_validator.py --category [category]`

### **For Development:**
- All active development should use the enhanced `wp_tools/` directory
- Archive scripts are kept for reference but not recommended for use
- See `docs/tools/TOOLS_DOCUMENTATION.md` for current tool usage

---

**Clean, organized, and production-ready! 🚀**