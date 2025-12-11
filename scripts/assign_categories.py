#!/usr/bin/env python3
"""
Assign Categories to Photos

This script assigns photos to categories based on a mapping file.
It supports copy, move, or symlink actions.

Usage:
    python scripts/assign_categories.py --mapping scripts/mapping.yaml --src . --dst organized --action copy

Dependencies:
    pip install pyyaml
"""

import argparse
import os
import shutil
import yaml
from pathlib import Path


def load_mapping(mapping_file):
    """Load the YAML mapping file."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def process_files(mapping, src_dir, dst_dir, action):
    """
    Process files according to mapping.
    
    Args:
        mapping: Dictionary mapping filenames to categories
        src_dir: Source directory containing images
        dst_dir: Destination base directory
        action: One of 'copy', 'move', or 'symlink'
    """
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    
    for filename, category in mapping.items():
        src_file = src_path / filename
        
        if not src_file.exists():
            print(f"Warning: Source file not found: {src_file}")
            continue
        
        # Create category directory
        category_dir = dst_path / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        dst_file = category_dir / filename
        
        # Perform the action
        if action == 'copy':
            print(f"Copying {filename} to {category}/")
            shutil.copy2(src_file, dst_file)
        elif action == 'move':
            print(f"Moving {filename} to {category}/")
            shutil.move(str(src_file), str(dst_file))
        elif action == 'symlink':
            print(f"Symlinking {filename} to {category}/")
            if dst_file.exists() or dst_file.is_symlink():
                dst_file.unlink()
            dst_file.symlink_to(src_file.absolute())
        else:
            raise ValueError(f"Unknown action: {action}")


def main():
    parser = argparse.ArgumentParser(description='Assign photos to categories')
    parser.add_argument('--mapping', required=True,
                       help='Path to YAML mapping file')
    parser.add_argument('--src', required=True,
                       help='Source directory containing images')
    parser.add_argument('--dst', required=True,
                       help='Destination base directory')
    parser.add_argument('--action', choices=['copy', 'move', 'symlink'], 
                       default='copy',
                       help='Action to perform (default: copy)')
    
    args = parser.parse_args()
    
    # Load mapping
    mapping = load_mapping(args.mapping)
    
    if not mapping:
        print("Warning: Empty mapping file")
        return
    
    # Process files
    process_files(mapping, args.src, args.dst, args.action)
    
    print(f"\nProcessed {len(mapping)} files with action '{args.action}'")


if __name__ == '__main__':
    main()
