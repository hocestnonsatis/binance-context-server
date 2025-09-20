#!/usr/bin/env python3
"""
Script to build and upload package to PyPI
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main function"""
    print("🚀 Starting PyPI upload process...")
    
    # Check if .pypirc exists
    if not os.path.exists('.pypirc'):
        print("❌ .pypirc file not found. Please create it with your PyPI token.")
        sys.exit(1)
    
    # Build package
    if not run_command("python -m build", "Building package"):
        sys.exit(1)
    
    # Upload to PyPI
    if not run_command("python -m twine upload dist/*", "Uploading to PyPI"):
        sys.exit(1)
    
    print("\n🎉 Package successfully uploaded to PyPI!")
    print("📦 Check: https://pypi.org/project/binance-context-server/")

if __name__ == "__main__":
    main()
