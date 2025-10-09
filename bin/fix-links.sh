#!/bin/bash
# Quick Fix Broken Links
# Convenience script to run the broken links fixer

cd "$(dirname "$0")/.."
python3 master_toolkit/utils/fix_broken_links.py "$@"
