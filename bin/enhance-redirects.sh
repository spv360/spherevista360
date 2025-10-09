#!/bin/bash
# Enhance Redirect Posts
# Convenience script to enhance redirect posts with professional styling

cd "$(dirname "$0")/.."
python3 master_toolkit/utils/simple_redirect_enhancer.py "$@"