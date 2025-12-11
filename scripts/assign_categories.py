#!/usr/bin/env python3
"""
Categorize and move photos based on a mapping file.

This script allows you to organize photos into album categories by providing
a simple YAML or CSV mapping file.

Usage:
    python scripts/assign_categories.py --mapping mapping.yml
    python scripts/assign_categories.py --mapping mapping.csv

The mapping file should contain photo-to-album assignments.

YAML format example:
    fu-mountain:
      - LINE_ALBUM_福山步道_251211_1.jpg
      - LINE_ALBUM_福山步道_251211_2.jpg
    another-album:
      - photo1.jpg
      - photo2.jpg

CSV format example:
    photo,album
    LINE_ALBUM_福山步道_251211_1.jpg,fu-mountain
    LINE_ALBUM_福山步道_251211_2.jpg,fu-mountain
    photo1.jpg,another-album

For this Fu Mountain album, a sample mapping is provided below.
"""

import csv
import os
import sys
from pathlib import Path
from typing import Dict, List

# Try to import YAML support
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def load_yaml_mapping(filepath: Path) -> Dict[str, List[str]]:
    """Load photo-to-album mapping from YAML file."""
    if not YAML_AVAILABLE:
        print("Error: PyYAML is not installed. Install it with: pip install PyYAML")
        print("Or use CSV format instead.")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        mapping = yaml.safe_load(f)
    
    return mapping


def load_csv_mapping(filepath: Path) -> Dict[str, List[str]]:
    """Load photo-to-album mapping from CSV file."""
    mapping = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            photo = row['photo']
            album = row['album']
            
            if album not in mapping:
                mapping[album] = []
            mapping[album].append(photo)
    
    return mapping


def load_mapping(filepath: Path) -> Dict[str, List[str]]:
    """Load mapping from YAML or CSV file."""
    suffix = filepath.suffix.lower()
    
    if suffix in ['.yml', '.yaml']:
        return load_yaml_mapping(filepath)
    elif suffix == '.csv':
        return load_csv_mapping(filepath)
    else:
        print(f"Error: Unsupported file format: {suffix}")
        print("Supported formats: .yml, .yaml, .csv")
        sys.exit(1)


def move_photos(
    mapping: Dict[str, List[str]],
    source_dir: Path,
    albums_base: Path,
    dry_run: bool = False
) -> None:
    """
    Move or copy photos to album directories based on mapping.
    
    Args:
        mapping: Dictionary of album_name -> list of photo filenames
        source_dir: Directory containing source photos
        albums_base: Base directory for albums
        dry_run: If True, only print what would be done
    """
    for album_name, photos in mapping.items():
        album_dir = albums_base / album_name
        
        if not dry_run:
            album_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nAlbum: {album_name}")
        
        for photo_name in photos:
            source_path = source_dir / photo_name
            dest_path = album_dir / photo_name
            
            if not source_path.exists():
                print(f"  ⚠ Warning: Source file not found: {photo_name}")
                continue
            
            if dry_run:
                print(f"  Would move: {photo_name} -> {album_name}/")
            else:
                # Copy instead of move to preserve originals
                import shutil
                shutil.copy2(source_path, dest_path)
                print(f"  ✓ Copied: {photo_name} -> {album_name}/")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Categorize and organize photos into albums'
    )
    parser.add_argument(
        '--mapping',
        type=str,
        required=True,
        help='Path to mapping file (YAML or CSV)'
    )
    parser.add_argument(
        '--source',
        type=str,
        help='Source directory containing photos (default: repo root)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print what would be done without actually moving files'
    )
    
    args = parser.parse_args()
    
    # Define paths
    repo_root = Path(__file__).parent.parent
    mapping_path = Path(args.mapping)
    
    if not mapping_path.exists():
        print(f"Error: Mapping file not found: {mapping_path}")
        sys.exit(1)
    
    # Load mapping
    print(f"Loading mapping from: {mapping_path}")
    mapping = load_mapping(mapping_path)
    print(f"Loaded mappings for {len(mapping)} album(s)")
    
    # Determine source directory
    if args.source:
        source_dir = Path(args.source)
    else:
        source_dir = repo_root
    
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        sys.exit(1)
    
    # Define albums base
    albums_base = repo_root / 'assets' / 'images' / 'photos' / 'albums'
    
    # Move photos
    move_photos(mapping, source_dir, albums_base, args.dry_run)
    
    if not args.dry_run:
        print("\n✓ Photo organization complete")
        print("\nNext steps:")
        print("1. Run: python scripts/generate_thumbnails.py")
        print("2. Create album pages in photos/ directory")
        print("3. Update data/photos/by-album.json if needed")
    else:
        print("\n(Dry run complete - no files were moved)")


# Sample mapping for Fu Mountain album
SAMPLE_MAPPING_YAML = """# Sample mapping for Fu Mountain photos
fu-mountain:
  - LINE_ALBUM_福山步道_251211_1.jpg
  - LINE_ALBUM_福山步道_251211_2.jpg
  - LINE_ALBUM_福山步道_251211_3.jpg
  - LINE_ALBUM_福山步道_251211_4.jpg
  - LINE_ALBUM_福山步道_251211_5.jpg
  - LINE_ALBUM_福山步道_251211_6.jpg
  - LINE_ALBUM_福山步道_251211_7.jpg
  - LINE_ALBUM_福山步道_251211_8.jpg
"""

SAMPLE_MAPPING_CSV = """photo,album
LINE_ALBUM_福山步道_251211_1.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_2.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_3.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_4.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_5.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_6.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_7.jpg,fu-mountain
LINE_ALBUM_福山步道_251211_8.jpg,fu-mountain
"""


if __name__ == '__main__':
    # If no arguments provided, print sample mappings
    if len(sys.argv) == 1:
        print(__doc__)
        print("\n--- Sample YAML Mapping ---")
        print(SAMPLE_MAPPING_YAML)
        print("\n--- Sample CSV Mapping ---")
        print(SAMPLE_MAPPING_CSV)
        print("\nTo use this script, save one of the sample mappings to a file")
        print("and run: python scripts/assign_categories.py --mapping <file>")
    else:
        main()
