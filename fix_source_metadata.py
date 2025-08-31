#!/usr/bin/env python3
"""Fix metadata in source distribution by removing problematic license fields."""

import tarfile
import tempfile
import os
import shutil

def fix_source_metadata():
    """Fix the metadata in the source distribution."""
    tar_file = 'dist/epub_pinyin-0.2.0.tar.gz'
    
    if not os.path.exists(tar_file):
        print(f"Source distribution {tar_file} not found!")
        return
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Extract the tar.gz
        with tarfile.open(tar_file, 'r:gz') as tar:
            tar.extractall(temp_dir)
        
        # Find and fix PKG-INFO
        pkg_info_path = os.path.join(temp_dir, 'epub_pinyin-0.2.0', 'PKG-INFO')
        if os.path.exists(pkg_info_path):
            with open(pkg_info_path, 'r', encoding='utf-8') as f:
                metadata = f.read()
            
            # Remove problematic license fields
            lines = metadata.split('\n')
            filtered_lines = []
            for line in lines:
                if not line.startswith('License-File:') and not line.startswith('License-Expression:'):
                    filtered_lines.append(line)
            
            new_metadata = '\n'.join(filtered_lines)
            
            # Write fixed metadata
            with open(pkg_info_path, 'w', encoding='utf-8') as f:
                f.write(new_metadata)
            
            # Create new tar.gz
            new_tar = tar_file.replace('.tar.gz', '_fixed.tar.gz')
            with tarfile.open(new_tar, 'w:gz') as tar:
                tar.add(os.path.join(temp_dir, 'epub_pinyin-0.2.0'), arcname='epub_pinyin-0.2.0')
            
            # Replace original
            os.remove(tar_file)
            os.rename(new_tar, tar_file)
            
            print("Source distribution metadata fixed successfully!")
        else:
            print("PKG-INFO not found in source distribution!")
            
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    fix_source_metadata()
