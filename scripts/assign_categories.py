#!/usr/bin/env python3
"""
Assign photos to categories based on a mapping file.

Usage:
    python scripts/assign_categories.py --mapping scripts/mapping.yaml --src source_dir --dst dest_dir --action copy

Actions:
    copy    - Copy files to destination
    move    - Move files to destination
    symlink - Create symbolic links to destination
"""

import argparse
import shutil
import yaml
from pathlib import Path


def load_mapping(mapping_file):
    """Load the mapping YAML file."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def assign_categories(mapping, src_dir, dst_dir, action):
    """
    Assign photos to categories based on mapping.
    
    Args:
        mapping: Dictionary mapping filenames to categories
        src_dir: Source directory containing images
        dst_dir: Destination base directory
        action: 'copy', 'move', or 'symlink'
    """
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    
    for filename, category in mapping.items():
        src_file = src_path / filename
        
        if not src_file.exists():
            print(f"Warning: {filename} not found in {src_dir}")
            continue
        
        # Create category directory
        category_dir = dst_path / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        dst_file = category_dir / filename
        
        if action == 'copy':
            print(f"Copying {filename} to {category}/")
            shutil.copy2(src_file, dst_file)
        elif action == 'move':
            print(f"Moving {filename} to {category}/")
            shutil.move(str(src_file), str(dst_file))
        elif action == 'symlink':
            print(f"Symlinking {filename} to {category}/")
            if dst_file.exists():
                dst_file.unlink()
            dst_file.symlink_to(src_file.absolute())
        else:
            raise ValueError(f"Unknown action: {action}")


def main():
    parser = argparse.ArgumentParser(description='Assign photos to categories based on mapping file')
    parser.add_argument('--mapping', required=True, help='Path to mapping YAML file')
    parser.add_argument('--src', required=True, help='Source directory containing images')
    parser.add_argument('--dst', required=True, help='Destination base directory')
    parser.add_argument('--action', required=True, choices=['copy', 'move', 'symlink'],
                        help='Action to perform: copy, move, or symlink')
    
    args = parser.parse_args()
    
    mapping_data = load_mapping(args.mapping)
    
    if 'mapping' in mapping_data:
        mapping = mapping_data['mapping']
    else:
        mapping = mapping_data
    
    print(f"Processing {len(mapping)} files")
    print(f"Action: {args.action}")
    print()
    
    assign_categories(mapping, args.src, args.dst, args.action)
    
    print()
    print("Done!")


if __name__ == '__main__':
    main()
