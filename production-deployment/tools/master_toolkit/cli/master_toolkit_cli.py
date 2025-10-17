#!/usr/bin/env python3
"""
Master Toolkit CLI - Main Entry Point
=====================================
Unified command-line interface for all SphereVista360 WordPress management tools.

Usage:
    python master_toolkit_cli.py <command> [options]

Commands:
    verify         - Verify site fixes and improvements
    set-images     - Set featured images from content
    seo-enhance    - Run SEO and content quality enhancements
    validate       - Run comprehensive site validation
    publish        - Publish content using master toolkit
    
    help           - Show this help message
    list           - List all available tools

Examples:
    python master_toolkit_cli.py verify
    python master_toolkit_cli.py set-images
    python master_toolkit_cli.py seo-enhance
    python master_toolkit_cli.py validate --comprehensive
"""

import sys
import os
import subprocess
from pathlib import Path

# Add master_toolkit to Python path
toolkit_path = Path(__file__).parent / 'master_toolkit'
sys.path.insert(0, str(toolkit_path))

class MasterToolkitCLI:
    def __init__(self):
        self.toolkit_dir = Path(__file__).parent / 'master_toolkit'
        self.commands = {
            'verify': {
                'script': 'cli/verify_fixes.py',
                'description': 'Verify site fixes and image improvements'
            },
            'set-images': {
                'script': 'cli/set_featured_images.py', 
                'description': 'Set featured images from content'
            },
            'seo-enhance': {
                'script': 'cli/seo_content_enhancement.py',
                'description': 'Run SEO and content quality enhancements'
            },
            'validate': {
                'script': 'cli/validate.py',
                'description': 'Run comprehensive site validation'
            },
            'publish': {
                'script': 'cli/publish.py',
                'description': 'Publish content using master toolkit'
            }
        }
    
    def show_help(self):
        """Display help information"""
        print(__doc__)
        
    def list_commands(self):
        """List all available commands"""
        print("🛠️  Available Master Toolkit Commands:")
        print("=" * 45)
        
        for cmd, info in self.commands.items():
            print(f"  {cmd:<15} - {info['description']}")
        
        print(f"\n📁 Toolkit Structure:")
        print(f"  master_toolkit/cli/        - Command-line tools")
        print(f"  master_toolkit/core/       - Core functionality")
        print(f"  master_toolkit/validation/ - Validation tools")
        print(f"  master_toolkit/utils/      - Utility functions")
        print(f"  master_toolkit/examples/   - Example scripts")
        print(f"  master_toolkit/archived/   - One-time use scripts")
        
    def run_command(self, command, args=None):
        """Execute a master toolkit command"""
        if command not in self.commands:
            print(f"❌ Unknown command: {command}")
            print(f"💡 Use 'list' to see available commands")
            return False
        
        script_path = self.toolkit_dir / self.commands[command]['script']
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        print(f"🚀 Running: {self.commands[command]['description']}")
        print(f"📝 Script: {script_path}")
        print("-" * 50)
        
        try:
            # Run the script
            cmd = [sys.executable, str(script_path)]
            if args:
                cmd.extend(args)
                
            result = subprocess.run(cmd, cwd=str(self.toolkit_dir.parent))
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False
    
    def main(self):
        """Main CLI entry point"""
        if len(sys.argv) < 2:
            self.show_help()
            return
        
        command = sys.argv[1].lower()
        args = sys.argv[2:] if len(sys.argv) > 2 else None
        
        if command in ['help', '-h', '--help']:
            self.show_help()
        elif command in ['list', 'ls']:
            self.list_commands()
        elif command in self.commands:
            self.run_command(command, args)
        else:
            print(f"❌ Unknown command: {command}")
            print(f"💡 Use 'help' for usage information")
            print(f"💡 Use 'list' to see available commands")

if __name__ == "__main__":
    cli = MasterToolkitCLI()
    cli.main()