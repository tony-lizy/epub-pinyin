#!/usr/bin/env python3
"""Fix metadata by removing problematic license fields."""

import zipfile
import tempfile
import os
import shutil

def fix_metadata():
    """Fix the metadata in the wheel file."""
    wheel_file = 'dist/epub_pinyin-0.2.0-py3-none-any.whl'
    
    if not os.path.exists(wheel_file):
        print(f"Wheel file {wheel_file} not found!")
        return
    
    # Read the original wheel
    with zipfile.ZipFile(wheel_file, 'r') as z:
        # Extract metadata
        metadata = z.read('epub_pinyin-0.2.0.dist-info/METADATA').decode()
        
        # Remove problematic license fields
        lines = metadata.split('\n')
        filtered_lines = []
        for line in lines:
            if not line.startswith('License-File:') and not line.startswith('License-Expression:'):
                filtered_lines.append(line)
        
        new_metadata = '\n'.join(filtered_lines)
        
        # Create a new wheel with fixed metadata
        temp_dir = tempfile.mkdtemp()
        try:
            # Extract all files to temp directory
            z.extractall(temp_dir)
            
            # Write fixed metadata
            metadata_path = os.path.join(temp_dir, 'epub_pinyin-0.2.0.dist-info', 'METADATA')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                f.write(new_metadata)
            
            # Create new wheel
            new_wheel = wheel_file.replace('.whl', '_fixed.whl')
            with zipfile.ZipFile(new_wheel, 'w', zipfile.ZIP_DEFLATED) as new_z:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, temp_dir)
                        new_z.write(file_path, arc_name)
            
            # Replace original wheel
            os.remove(wheel_file)
            os.rename(new_wheel, wheel_file)
            
            print("Metadata fixed successfully!")
            
        finally:
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    fix_metadata()
