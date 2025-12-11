#!/bin/bash
# generate_thumbnails.sh - Shell script alternative for thumbnail generation
# Note: This is a simplified version. For full functionality, use generate_thumbnails.py

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PHOTOS_DIR="$REPO_ROOT/assets/images/photos/by-date"
THUMBNAILS_DIR="$REPO_ROOT/assets/images/photos/thumbnails/by-date"
METADATA_FILE="$REPO_ROOT/data/photos/by-date.json"

echo "Photo Gallery Thumbnail Generator (Shell Script)"
echo "=================================================="
echo ""
echo "Note: This script requires ImageMagick (convert command) to be installed."
echo "For full functionality including EXIF data extraction and metadata generation,"
echo "please use: python3 scripts/generate_thumbnails.py"
echo ""

# Check if convert command is available
if ! command -v convert &> /dev/null; then
    echo "Error: ImageMagick 'convert' command not found."
    echo "Please install ImageMagick or use the Python script instead:"
    echo "  sudo apt-get install imagemagick  # On Ubuntu/Debian"
    echo "  brew install imagemagick          # On macOS"
    echo ""
    echo "Or run the Python script:"
    echo "  python3 scripts/generate_thumbnails.py"
    exit 1
fi

if [ ! -d "$PHOTOS_DIR" ]; then
    echo "Error: Photos directory not found: $PHOTOS_DIR"
    echo "Please create the directory structure and add photos first."
    exit 1
fi

echo "Photos directory: $PHOTOS_DIR"
echo "Thumbnails directory: $THUMBNAILS_DIR"
echo ""

# Generate thumbnails
find "$PHOTOS_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r photo; do
    # Get relative path
    rel_path="${photo#$PHOTOS_DIR/}"
    year_month_day="$(dirname "$rel_path")"
    filename="$(basename "$photo")"
    name="${filename%.*}"
    
    # Create thumbnail directory
    thumb_dir="$THUMBNAILS_DIR/$year_month_day"
    mkdir -p "$thumb_dir"
    
    # Generate thumbnail (300px wide, maintain aspect ratio)
    thumb_file="$thumb_dir/${name}-th.jpg"
    echo "Processing: $year_month_day/$filename"
    convert "$photo" -resize 300x -quality 85 "$thumb_file"
    echo "  Created: $thumb_file"
done

echo ""
echo "✓ Thumbnails generated successfully!"
echo ""
echo "Note: Metadata file (data/photos/by-date.json) was NOT updated."
echo "To generate/update metadata with photo information, please run:"
echo "  python3 scripts/generate_thumbnails.py"
