#!/usr/bin/env python3
"""
Generate photo thumbnails and update album JSON data.

Usage:
    python scripts/generate_thumbnails.py --mode album --src images --dst assets/images/photos --album-id fu-mountain --thumb-width 400

This script:
1. Copies original images from src to dst/albums/<album-id>/
2. Generates thumbnails at specified width (maintaining aspect ratio)
3. Creates or updates data/photos/by-album.json with album metadata

Dependencies:
    pip install pillow
"""

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image


def parse_date_from_filename(filename):
    """
    Parse date from filename in YYYYMMDD or YYMMDD format.
    Returns ISO date string or None if not found.
    """
    # Try to find YYMMDD pattern (e.g., 251211 for 2025-12-11)
    match = re.search(r'_(\d{6})_', filename)
    if match:
        date_str = match.group(1)
        try:
            # Assume 20xx for YY
            year = 2000 + int(date_str[0:2])
            month = int(date_str[2:4])
            day = int(date_str[4:6])
            return f"{year:04d}-{month:02d}-{day:02d}"
        except (ValueError, IndexError):
            pass
    
    # Try to find YYYYMMDD pattern
    match = re.search(r'_(\d{8})_', filename)
    if match:
        date_str = match.group(1)
        try:
            year = int(date_str[0:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            return f"{year:04d}-{month:02d}-{day:02d}"
        except (ValueError, IndexError):
            pass
    
    return None


def generate_thumbnail(image_path, thumbnail_path, width):
    """Generate a thumbnail with specified width, maintaining aspect ratio."""
    with Image.open(image_path) as img:
        # Calculate height to maintain aspect ratio
        aspect_ratio = img.height / img.width
        height = int(width * aspect_ratio)
        
        # Resize image
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Save as JPEG
        img_resized.convert('RGB').save(thumbnail_path, 'JPEG', quality=85, optimize=True)


def process_album(src_dir, dst_dir, album_id, thumb_width):
    """
    Process an album: copy images, generate thumbnails, and create metadata.
    
    Returns album data structure.
    """
    src_path = Path(src_dir)
    album_dst = Path(dst_dir) / 'albums' / album_id
    thumb_dst = Path(dst_dir) / 'thumbnails' / 'albums' / album_id
    
    # Create destination directories
    album_dst.mkdir(parents=True, exist_ok=True)
    thumb_dst.mkdir(parents=True, exist_ok=True)
    
    # Find all image files in source directory
    image_files = []
    for ext in ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG']:
        image_files.extend(src_path.glob(ext))
    
    # Sort files by name
    image_files.sort(key=lambda x: x.name)
    
    photos = []
    
    for img_file in image_files:
        # Copy original to album folder
        dst_image = album_dst / img_file.name
        print(f"Copying {img_file.name} to {dst_image}")
        shutil.copy2(img_file, dst_image)
        
        # Generate thumbnail filename (change extension to .jpg)
        thumb_filename = img_file.stem + '.jpg'
        thumb_path = thumb_dst / thumb_filename
        
        print(f"Generating thumbnail: {thumb_path}")
        generate_thumbnail(dst_image, thumb_path, thumb_width)
        
        # Parse date from filename
        date_str = parse_date_from_filename(img_file.name)
        
        # Create photo entry with relative paths
        photo_data = {
            'filename': img_file.name,
            'title': img_file.stem,
            'path': f'assets/images/photos/albums/{album_id}/{img_file.name}',
            'thumbnail': f'assets/images/photos/thumbnails/albums/{album_id}/{thumb_filename}'
        }
        
        if date_str:
            photo_data['date'] = date_str
        
        photos.append(photo_data)
    
    # Create album data structure
    album_data = {
        'id': album_id,
        'title': album_id.replace('-', ' ').title(),  # Default title
        'cover': photos[0]['thumbnail'] if photos else '',
        'photos': photos
    }
    
    return album_data


def update_album_json(album_data, json_path='data/photos/by-album.json'):
    """Update or create by-album.json with the album data."""
    json_file = Path(json_path)
    json_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing data or create new
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {'albums': []}
    
    # Find and update or append album
    album_id = album_data['id']
    updated = False
    for i, album in enumerate(data['albums']):
        if album['id'] == album_id:
            data['albums'][i] = album_data
            updated = True
            break
    
    if not updated:
        data['albums'].append(album_data)
    
    # Write updated data
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {json_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate photo thumbnails and update album JSON')
    parser.add_argument('--mode', required=True, choices=['album'], 
                        help='Processing mode (currently only "album" is supported)')
    parser.add_argument('--src', required=True, help='Source directory containing images')
    parser.add_argument('--dst', required=True, help='Destination base directory for processed images')
    parser.add_argument('--album-id', required=True, help='Album identifier (slug)')
    parser.add_argument('--thumb-width', type=int, default=400, help='Thumbnail width in pixels (default: 400)')
    
    args = parser.parse_args()
    
    if args.mode == 'album':
        print(f"Processing album: {args.album_id}")
        print(f"Source: {args.src}")
        print(f"Destination: {args.dst}")
        print(f"Thumbnail width: {args.thumb_width}px")
        print()
        
        album_data = process_album(args.src, args.dst, args.album_id, args.thumb_width)
        update_album_json(album_data)
        
        print()
        print(f"Successfully processed {len(album_data['photos'])} photos")
        print(f"Album ID: {album_data['id']}")


if __name__ == '__main__':
    main()
