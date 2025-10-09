# 🔧 Quick Usage Guide - Convenience Scripts

The SphereVista360 toolkit includes convenient bash scripts in the `bin/` directory for easy access to common operations.

## 🚀 Available Commands

### Fix Broken Links
```bash
./bin/fix-links.sh
```
Quickly identifies and fixes broken links in your WordPress content using the integrated REST API.

### Comprehensive Website Fix
```bash
./bin/comprehensive-fix.sh
```
Runs complete website validation and applies all available fixes including SEO optimization, link validation, and content quality improvements.

### Enhance Redirect Posts
```bash
./bin/enhance-redirects.sh
```
Upgrades redirect posts with professional styling, beautiful gradients, clear subheadings, and informative content explaining the page moves.

## ⚡ Easy Setup

### Option 1: Run the Setup Script
```bash
./setup.sh
```
This will add the `bin/` directory to your PATH so you can run the commands from anywhere:
```bash
fix-links.sh
comprehensive-fix.sh
enhance-redirects.sh
```

### Option 2: Manual PATH Setup
Add this line to your shell configuration file (`.bashrc`, `.zshrc`, etc.):
```bash
export PATH="/path/to/spherevista360/bin:$PATH"
```

### Option 3: Direct Usage
Run scripts directly without setup:
```bash
./bin/fix-links.sh
./bin/comprehensive-fix.sh
./bin/enhance-redirects.sh
```

## 🎯 Professional Organization

The project follows Unix conventions:
- `bin/` - Executable convenience scripts
- `master_toolkit/` - Core Python modules
- `docs/` - Documentation and reports
- `published_content/` - WordPress content files

This structure keeps the root directory clean while providing easy access to frequently used tools.

## 🔗 Related Documentation

- See `master_toolkit/README.md` for core toolkit documentation
- See `docs/` for detailed reports and guides
- Run `./setup.sh` for interactive PATH configuration