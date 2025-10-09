# Tool Refactoring Plan

## Current State Analysis

### Directory Structure
```
tools/           - 50 specialized scripts (mostly one-off fixes)
wp_tools/        - 14 well-structured modules 
wordpress-enhancements/ - 3 experimental scripts
```

### Key Issues
- **Redundancy**: Multiple tools doing similar things
- **Scattered functionality**: Authentication, validation, and publishing spread across directories
- **One-off solutions**: Many tools solve specific problems but aren't reusable
- **Inconsistent patterns**: Different auth methods, API approaches, error handling

## Target Architecture

### Core Structure
```
wordpress_toolkit/
├── core/
│   ├── __init__.py
│   ├── client.py          # Unified WordPress API client
│   ├── auth.py           # Authentication management
│   └── config.py         # Configuration management
├── content/
│   ├── __init__.py
│   ├── publisher.py      # Content publishing
│   ├── validator.py      # Content validation
│   └── workflow.py       # Publishing workflows
├── validation/
│   ├── __init__.py
│   ├── links.py          # Link validation & fixing
│   ├── images.py         # Image validation & fixing
│   ├── seo.py           # SEO validation & optimization
│   └── comprehensive.py # Combined validation suite
├── utils/
│   ├── __init__.py
│   ├── helpers.py        # Common utilities
│   └── formatters.py     # Output formatting
└── cli/
    ├── __init__.py
    ├── publish.py        # Publishing commands
    ├── validate.py       # Validation commands
    └── fix.py           # Fixing commands
```

## Key Features to Preserve

### Working Authentication
- JK user credentials with basic auth (from editor_fix_cmd.py)
- Application password support
- Proper error handling

### Core Functionality
- Content publishing with markdown support
- Comprehensive validation (links, images, SEO)
- Broken link detection and fixing
- SEO optimization
- Image validation and replacement

### Proven Patterns
- wp_tools modular architecture
- Comprehensive error handling and reporting
- Progress tracking and user feedback

## Migration Strategy

1. **Create Core Infrastructure** - WordPress client, authentication, config
2. **Build Content Management** - Publishing, validation, workflows
3. **Consolidate Validation Tools** - Links, images, SEO in unified modules
4. **Preserve Working Solutions** - Ensure JK auth and proven fixes work
5. **Clean Up** - Remove duplicates, organize utilities, update docs

## Benefits

- **Maintainability**: Clear module boundaries and responsibilities
- **Reusability**: Common patterns abstracted into reusable components
- **Consistency**: Unified authentication, error handling, and reporting
- **Extensibility**: Easy to add new features without duplication
- **Reliability**: Preserve all working solutions while improving structure