#!/usr/bin/env python3
"""
Build and deployment script for epub-pinyin package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', 'epub_pinyin.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")

def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")

def check_package():
    """Check the built package."""
    print("Checking package...")
    
    # Fix metadata issues
    print("Fixing metadata...")
    import subprocess
    subprocess.run(["python", "fix_metadata.py"], check=True)
    subprocess.run(["python", "fix_source_metadata.py"], check=True)
    
    # Check package
    run_command("twine check dist/*")

def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("Uploading to TestPyPI...")
    run_command("twine upload --repository testpypi dist/*")

def upload_to_pypi():
    """Upload to PyPI."""
    print("Uploading to PyPI...")
    run_command("twine upload dist/*")

def main():
    """Main deployment function."""
    print("=== EPUB-Pinyin Package Deployment ===")
    
    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print("Error: pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build package
    build_package()
    
    # Check package
    check_package()
    
    print("\n=== Build completed successfully! ===")
    print("\nTo upload to TestPyPI (recommended first):")
    print("  python build_and_deploy.py --test")
    print("\nTo upload to PyPI:")
    print("  python build_and_deploy.py --upload")
    print("\nTo install from TestPyPI:")
    print("  pip install --index-url https://test.pypi.org/simple/ epub-pinyin")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            main()
            upload_to_testpypi()
            print("Uploaded to TestPyPI successfully!")
        elif sys.argv[1] == "--upload":
            main()
            upload_to_pypi()
            print("Uploaded to PyPI successfully!")
        else:
            print("Usage: python build_and_deploy.py [--test|--upload]")
    else:
        main()
