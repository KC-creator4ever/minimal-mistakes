#!/usr/bin/env python3
"""
Generate Thumbnails and Album Index

This script generates thumbnails for photo albums and creates/updates
the by-album.json index file.

Usage:
    # Generate thumbnails for fu-mountain album
    python scripts/generate_thumbnails.py --mode album --src . --dst assets/images/photos --album-id fu-mountain --thumb-width 400

Dependencies:
    pip install pillow

The script will:
1. Copy original images from source to dst/albums/{album-id}/
2. Generate thumbnails to dst/thumbnails/albums/{album-id}/
3. Create or update data/photos/by-album.json with album metadata
"""

import argparse
import json
import os
import re
import shutil
from pathlib import Path
from PIL import Image


def parse_date_from_filename(filename):
    """
    Parse date from filename in YYYYMMDD or YYMMDD format.
    Returns date string in YYYY-MM-DD format or empty string if not found.
    """
    # Try to find date patterns in filename
    # Pattern for YYMMDD (6 digits)
    match = re.search(r'_(\d{6})_', filename)
    if match:
        date_str = match.group(1)
        # Assume 20xx for YY format
        year = '20' + date_str[0:2]
        month = date_str[2:4]
        day = date_str[4:6]
        return f"{year}-{month}-{day}"
    
    # Pattern for YYYYMMDD (8 digits)
    match = re.search(r'_(\d{8})_', filename)
    if match:
        date_str = match.group(1)
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    
    return ""


def generate_thumbnail(input_path, output_path, width=400):
    """Generate a thumbnail with specified width, maintaining aspect ratio."""
    with Image.open(input_path) as img:
        # Calculate height to maintain aspect ratio
        aspect_ratio = img.height / img.width
        height = int(width * aspect_ratio)
        
        # Resize image
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Save as JPEG
        img_resized.convert('RGB').save(output_path, 'JPEG', quality=85)


def process_album(src_dir, dst_dir, album_id, thumb_width, source_pattern):
    """Process album: copy images, generate thumbnails, return photo data."""
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    
    # Create destination directories
    albums_dir = dst_path / 'albums' / album_id
    thumbnails_dir = dst_path / 'thumbnails' / 'albums' / album_id
    albums_dir.mkdir(parents=True, exist_ok=True)
    thumbnails_dir.mkdir(parents=True, exist_ok=True)
    
    # Find source images
    source_files = sorted(src_path.glob(source_pattern))
    
    if not source_files:
        print(f"Warning: No files found matching {source_pattern} in {src_dir}")
        return []
    
    photos = []
    
    for src_file in source_files:
        filename = src_file.name
        
        # Copy original to albums directory
        dst_file = albums_dir / filename
        print(f"Copying {filename} to {dst_file}")
        shutil.copy2(src_file, dst_file)
        
        # Generate thumbnail
        thumb_name = src_file.stem + '.jpg'
        thumb_file = thumbnails_dir / thumb_name
        print(f"Generating thumbnail {thumb_file}")
        generate_thumbnail(src_file, thumb_file, width=thumb_width)
        
        # Parse metadata
        title = filename
        date = parse_date_from_filename(filename)
        
        # Create photo object with relative paths (POSIX style)
        photo = {
            'filename': filename,
            'title': title,
            'date': date,
            'path': f'assets/images/photos/albums/{album_id}/{filename}',
            'thumbnail': f'assets/images/photos/thumbnails/albums/{album_id}/{thumb_name}'
        }
        photos.append(photo)
    
    return photos


def update_album_json(album_id, album_title, photos):
    """Create or update data/photos/by-album.json."""
    json_path = Path('data/photos/by-album.json')
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing data or create new
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {'albums': []}
    
    # Find or create album entry
    album = None
    for a in data['albums']:
        if a['id'] == album_id:
            album = a
            break
    
    if album is None:
        album = {
            'id': album_id,
            'title': album_title,
            'cover': '',
            'photos': []
        }
        data['albums'].append(album)
    
    # Update album data
    album['title'] = album_title
    album['photos'] = photos
    
    # Set cover to first thumbnail if photos exist
    if photos:
        album['cover'] = photos[0]['thumbnail']
    
    # Write updated data
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {json_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate thumbnails and album index')
    parser.add_argument('--mode', default='album', choices=['album'], 
                       help='Processing mode (currently only "album" is supported)')
    parser.add_argument('--src', default='.', 
                       help='Source directory containing images')
    parser.add_argument('--dst', default='assets/images/photos', 
                       help='Destination directory for organized photos')
    parser.add_argument('--album-id', required=True, 
                       help='Album identifier (e.g., "fu-mountain")')
    parser.add_argument('--album-title', 
                       help='Album title (defaults to album-id)')
    parser.add_argument('--thumb-width', type=int, default=400, 
                       help='Thumbnail width in pixels (default: 400)')
    parser.add_argument('--pattern', default='LINE_ALBUM_福山步道_251211_*.jpg',
                       help='File pattern to match (default: LINE_ALBUM_福山步道_251211_*.jpg)')
    
    args = parser.parse_args()
    
    # Default album title to album-id if not provided
    album_title = args.album_title if args.album_title else args.album_id
    
    # Process album
    photos = process_album(
        args.src, 
        args.dst, 
        args.album_id, 
        args.thumb_width,
        args.pattern
    )
    
    # Update JSON index
    update_album_json(args.album_id, album_title, photos)
    
    print(f"\nProcessed {len(photos)} photos for album '{args.album_id}'")


if __name__ == '__main__':
    main()
