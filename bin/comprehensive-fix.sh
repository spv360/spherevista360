#!/bin/bash
# Comprehensive Website Fix
# Convenience script to run comprehensive validation and fixing

cd "$(dirname "$0")/.."
python3 master_toolkit/utils/comprehensive_fix.py "$@"
