#!/usr/bin/env python3
"""
Generate thumbnails and metadata for photo gallery organized by date.

This script:
1. Scans photos in assets/images/photos/by-date/
2. Generates 300px wide thumbnails in assets/images/photos/thumbnails/by-date/
3. Creates metadata JSON file at data/photos/by-date.json
4. Extracts EXIF date when available, falls back to filename or current date
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from PIL import Image

# Configuration
REPO_ROOT = Path(__file__).parent.parent
PHOTOS_DIR = REPO_ROOT / "assets" / "images" / "photos" / "by-date"
THUMBNAILS_DIR = REPO_ROOT / "assets" / "images" / "photos" / "thumbnails" / "by-date"
METADATA_FILE = REPO_ROOT / "data" / "photos" / "by-date.json"
THUMBNAIL_WIDTH = 300

def get_exif_date(image_path):
    """Extract date from EXIF data if available."""
    try:
        from PIL.ExifTags import TAGS
        img = Image.open(image_path)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "DateTime":
                    # Parse EXIF datetime format: "YYYY:MM:DD HH:MM:SS"
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"  Warning: Could not extract EXIF from {image_path.name}: {e}")
    return None

def get_file_date(image_path):
    """Get file modification date as fallback."""
    try:
        timestamp = os.path.getmtime(image_path)
        return datetime.fromtimestamp(timestamp)
    except Exception:
        return datetime.now()

def generate_thumbnail(image_path, thumbnail_path, width=THUMBNAIL_WIDTH):
    """Generate a thumbnail maintaining aspect ratio."""
    try:
        # Create parent directory if it doesn't exist
        thumbnail_path.parent.mkdir(parents=True, exist_ok=True)
        
        with Image.open(image_path) as img:
            # Calculate new height maintaining aspect ratio
            aspect_ratio = img.height / img.width
            new_height = int(width * aspect_ratio)
            
            # Resize image
            img_resized = img.resize((width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary (for PNG with transparency)
            if img_resized.mode in ('RGBA', 'LA', 'P'):
                img_rgb = Image.new('RGB', img_resized.size, (255, 255, 255))
                if img_resized.mode == 'P':
                    img_resized = img_resized.convert('RGBA')
                img_rgb.paste(img_resized, mask=img_resized.split()[-1] if img_resized.mode == 'RGBA' else None)
                img_resized = img_rgb
            
            # Save as JPEG
            img_resized.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
            print(f"  Created thumbnail: {thumbnail_path.relative_to(REPO_ROOT)}")
            return True
    except Exception as e:
        print(f"  Error creating thumbnail for {image_path.name}: {e}")
        return False

def scan_and_process_photos():
    """Scan photo directory and generate thumbnails and metadata."""
    if not PHOTOS_DIR.exists():
        print(f"Error: Photos directory not found: {PHOTOS_DIR}")
        print("Please create the directory structure and add photos first.")
        return False
    
    photos_metadata = []
    
    # Scan all photos organized by date
    for year_dir in sorted(PHOTOS_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        
        for month_day_dir in sorted(year_dir.iterdir()):
            if not month_day_dir.is_dir():
                continue
            
            year = year_dir.name
            month_day = month_day_dir.name
            
            print(f"\nProcessing {year}/{month_day}...")
            
            # Process each image in the directory
            for image_path in sorted(month_day_dir.glob("*")):
                if image_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                    continue
                
                print(f"  Processing: {image_path.name}")
                
                # Try to get date from EXIF, then directory structure, then file date
                photo_date = get_exif_date(image_path)
                if not photo_date:
                    try:
                        # Parse date from directory structure: YYYY/MM-DD
                        photo_date = datetime.strptime(f"{year}-{month_day}", "%Y-%m-%d")
                    except Exception:
                        photo_date = get_file_date(image_path)
                
                # Generate thumbnail path
                thumbnail_rel_path = Path("by-date") / year / month_day / f"{image_path.stem}-th.jpg"
                thumbnail_path = THUMBNAILS_DIR / year / month_day / f"{image_path.stem}-th.jpg"
                
                # Generate thumbnail
                if generate_thumbnail(image_path, thumbnail_path):
                    # Add to metadata
                    photo_rel_path = Path("by-date") / year / month_day / image_path.name
                    
                    metadata = {
                        "title": image_path.stem.replace('-', ' ').replace('_', ' ').title(),
                        "filename": image_path.name,
                        "path": f"/assets/images/photos/{photo_rel_path}",
                        "thumbnail": f"/assets/images/photos/thumbnails/{thumbnail_rel_path}",
                        "date": photo_date.strftime("%Y-%m-%d"),
                        "year": year,
                        "month": photo_date.strftime("%m"),
                        "month_name": photo_date.strftime("%B"),
                        "day": photo_date.strftime("%d")
                    }
                    photos_metadata.append(metadata)
    
    # Sort by date (newest first)
    photos_metadata.sort(key=lambda x: x['date'], reverse=True)
    
    # Save metadata to JSON file
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "photos": photos_metadata,
            "generated_at": datetime.now().isoformat(),
            "total_count": len(photos_metadata)
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated metadata file: {METADATA_FILE.relative_to(REPO_ROOT)}")
    print(f"✓ Total photos processed: {len(photos_metadata)}")
    
    return True

def main():
    """Main entry point."""
    print("Photo Gallery Thumbnail Generator")
    print("=" * 50)
    print(f"Photos directory: {PHOTOS_DIR}")
    print(f"Thumbnails directory: {THUMBNAILS_DIR}")
    print(f"Metadata file: {METADATA_FILE}")
    print("=" * 50)
    
    success = scan_and_process_photos()
    
    if success:
        print("\n✓ Successfully generated thumbnails and metadata!")
        print("\nNext steps:")
        print("1. Review the generated thumbnails")
        print("2. Check the metadata file at data/photos/by-date.json")
        print("3. The photo gallery page will use this data to display photos")
        return 0
    else:
        print("\n✗ Failed to generate thumbnails and metadata")
        return 1

if __name__ == "__main__":
    sys.exit(main())
