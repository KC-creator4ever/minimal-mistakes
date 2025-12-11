#!/usr/bin/env python3
"""
Generate thumbnails for photo albums and update metadata.

This script:
1. Scans assets/images/photos/albums/ for album directories
2. Generates thumbnails (default 400px wide) for each photo
3. Updates data/photos/by-album.json with album metadata

Usage:
    python scripts/generate_thumbnails.py [--width WIDTH] [--album ALBUM_NAME]

Dependencies:
    pip install Pillow
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is not installed. Install it with: pip install Pillow")
    sys.exit(1)


def extract_date_from_filename(filename: str) -> Optional[str]:
    """
    Extract date from filename pattern like LINE_ALBUM_*_YYMMDD_N.jpg
    Returns date in ISO format (YYYY-MM-DD) or None if not found.
    """
    # Pattern: LINE_ALBUM_*_YYMMDD_N.jpg where YYMMDD is the date
    match = re.search(r'_(\d{6})_\d+\.jpg$', filename, re.IGNORECASE)
    if match:
        date_str = match.group(1)
        # Assume YY format, convert to 20YY
        year = '20' + date_str[:2]
        month = date_str[2:4]
        day = date_str[4:6]
        try:
            # Validate date
            datetime(int(year), int(month), int(day))
            return f"{year}-{month}-{day}"
        except ValueError:
            pass
    return None


def get_title_from_filename(filename: str) -> str:
    """Extract title from filename (without extension)."""
    return Path(filename).stem


def generate_thumbnail(
    input_path: Path,
    output_path: Path,
    width: int = 400
) -> bool:
    """
    Generate a thumbnail for an image.
    
    Args:
        input_path: Path to original image
        output_path: Path to save thumbnail
        width: Target width in pixels (height will be proportional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with Image.open(input_path) as img:
            # Calculate height maintaining aspect ratio
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio)
            
            # Resize image
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Save as JPEG
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img_resized.save(output_path, 'JPEG', quality=85, optimize=True)
            
            print(f"  ✓ Generated thumbnail: {output_path.name}")
            return True
    except Exception as e:
        print(f"  ✗ Error generating thumbnail for {input_path.name}: {e}")
        return False


def process_album(
    album_name: str,
    album_path: Path,
    thumbnail_base_path: Path,
    width: int = 400
) -> Optional[Dict]:
    """
    Process a single album: generate thumbnails and collect metadata.
    
    Args:
        album_name: Name of the album
        album_path: Path to album directory
        thumbnail_base_path: Base path for thumbnails
        width: Thumbnail width in pixels
    
    Returns:
        Album metadata dictionary or None if no photos
    """
    print(f"\nProcessing album: {album_name}")
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    image_files = sorted([
        f for f in album_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ])
    
    if not image_files:
        print(f"  No images found in {album_name}")
        return None
    
    photos = []
    thumbnail_dir = thumbnail_base_path / 'albums' / album_name
    
    for img_file in image_files:
        # Generate thumbnail
        thumbnail_path = thumbnail_dir / img_file.name
        success = generate_thumbnail(img_file, thumbnail_path, width)
        
        if success:
            # Create photo metadata
            photo_data = {
                'path': f'/assets/images/photos/albums/{album_name}/{img_file.name}',
                'thumbnail': f'/assets/images/photos/thumbnails/albums/{album_name}/{img_file.name}',
                'title': get_title_from_filename(img_file.name)
            }
            
            # Try to extract date from filename
            date = extract_date_from_filename(img_file.name)
            if date:
                photo_data['date'] = date
            
            photos.append(photo_data)
    
    if not photos:
        return None
    
    # Create album metadata
    album_data = {
        'id': album_name,
        'title': album_name.replace('-', ' ').title(),  # Default title
        'cover': photos[0]['thumbnail'],  # First photo as cover
        'photos': photos
    }
    
    print(f"  Processed {len(photos)} photos")
    return album_data


def update_album_metadata(
    albums_data: List[Dict],
    output_path: Path
) -> None:
    """
    Update the by-album.json file with album metadata.
    
    Args:
        albums_data: List of album metadata dictionaries
        output_path: Path to by-album.json
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'albums': albums_data,
            'generated': datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Updated metadata: {output_path}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate thumbnails for photo albums'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=400,
        help='Thumbnail width in pixels (default: 400)'
    )
    parser.add_argument(
        '--album',
        type=str,
        help='Process only this album (default: all albums)'
    )
    
    args = parser.parse_args()
    
    # Define paths
    repo_root = Path(__file__).parent.parent
    albums_base = repo_root / 'assets' / 'images' / 'photos' / 'albums'
    thumbnails_base = repo_root / 'assets' / 'images' / 'photos' / 'thumbnails'
    metadata_path = repo_root / 'data' / 'photos' / 'by-album.json'
    
    if not albums_base.exists():
        print(f"Error: Albums directory not found: {albums_base}")
        sys.exit(1)
    
    # Get list of albums to process
    if args.album:
        album_dirs = [albums_base / args.album]
        if not album_dirs[0].exists():
            print(f"Error: Album not found: {args.album}")
            sys.exit(1)
    else:
        album_dirs = [d for d in albums_base.iterdir() if d.is_dir()]
    
    if not album_dirs:
        print("No albums found to process")
        sys.exit(0)
    
    # Process each album
    albums_data = []
    for album_dir in sorted(album_dirs):
        album_name = album_dir.name
        album_data = process_album(
            album_name,
            album_dir,
            thumbnails_base,
            args.width
        )
        if album_data:
            albums_data.append(album_data)
    
    # Update metadata
    if albums_data:
        update_album_metadata(albums_data, metadata_path)
        print(f"\n✓ Successfully processed {len(albums_data)} album(s)")
    else:
        print("\nNo albums with photos were processed")


if __name__ == '__main__':
    main()
