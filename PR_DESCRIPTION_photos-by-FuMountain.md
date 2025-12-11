# PR: Add Photo Gallery System - Fu Mountain Trail (photos-by-FuMountain)

## Overview
This PR implements a complete photo gallery system for the minimal-mistakes Jekyll theme, featuring the Fu Mountain Trail (福山步道) album with 8 photos.

## What's Included

### 1. Photo Gallery Scripts (`scripts/`)
- **`generate_thumbnails.py`**: Python script to generate thumbnails and update JSON data
  - Supports both album and category modes
  - Automatically parses dates from filenames
  - Creates 400px wide thumbnails by default
  - Updates `data/photos/by-album.json` or `data/photos/by-category.json`
  
- **`assign_categories.py`**: Python script to assign photos to categories
  - Supports YAML and CSV mapping files
  - Supports copy/move/symlink operations
  
- **`mapping.yaml`**: Example mapping file for the 8 Fu Mountain photos
  
- **`README.md`**: Comprehensive documentation for the photo gallery system

### 2. Gallery Layout (`_layouts/gallery.html`)
- New Jekyll layout for photo gallery pages
- Based on the existing `single.html` layout
- Includes gallery include support
- Breadcrumbs and sidebar support

### 3. Fu Mountain Photo Album
- **8 high-quality photos** from LINE ALBUM 福山步道
- **Original photos**: stored in `images/` directory
- **Full-size photos**: `assets/images/photos/albums/fu-mountain/`
- **Thumbnails**: `assets/images/photos/thumbnails/albums/fu-mountain/`

### 4. Data Files
- **`data/photos/by-album.json`**: JSON file containing album metadata
  - Album ID: `fu-mountain`
  - Album Title: 福山步道
  - 8 photos with metadata (filename, title, date, paths)
  - Date: 2025-12-11 (parsed from filename)

### 5. Gallery Page
- **`photos/fu-mountain.md`**: Markdown page for the Fu Mountain gallery
  - Permalink: `/photos/fu-mountain/`
  - Layout: `gallery`
  - Language: `zh-TW`

## Directory Structure
```
minimal-mistakes/
├── scripts/
│   ├── generate_thumbnails.py          # Thumbnail generator script
│   ├── assign_categories.py            # Category assignment script
│   ├── mapping.yaml                    # Mapping file for fu-mountain
│   └── README.md                       # Documentation
├── images/
│   └── LINE_ALBUM_福山步道_251211_*.jpg # Original source images (8 files)
├── data/
│   └── photos/
│       └── by-album.json               # Album metadata JSON
├── assets/
│   └── images/
│       └── photos/
│           ├── albums/
│           │   └── fu-mountain/        # Full-size album photos (8 files)
│           └── thumbnails/
│               └── albums/
│                   └── fu-mountain/    # Thumbnails (8 files)
├── photos/
│   └── fu-mountain.md                  # Gallery page
└── _layouts/
    └── gallery.html                    # Gallery layout template
```

## Technical Details

### Dependencies
- **Python 3**: For running the scripts
- **Pillow**: Image processing library (`pip install pillow`)
- **PyYAML**: YAML file processing (`pip install pyyaml`)

### Features
- **Automatic thumbnail generation**: Resizes images to 400px width while maintaining aspect ratio
- **Date parsing**: Automatically extracts dates from filenames (supports multiple formats)
- **JSON data management**: Automatically updates JSON files with photo metadata
- **Flexible organization**: Supports both album-based and category-based organization
- **Multiple file operations**: Copy, move, or symlink photos to category directories

### Photo Metadata
Each photo includes:
- Filename
- Title (derived from filename)
- Date (parsed from filename: 2025-12-11)
- Full-size image path
- Thumbnail path

## Usage

### Generate Thumbnails for an Album
```bash
python3 scripts/generate_thumbnails.py \
  --mode album \
  --src images \
  --dst assets/images/photos \
  --album-id fu-mountain \
  --thumb-width 400
```

### Assign Photos to Categories
```bash
python3 scripts/assign_categories.py \
  --mapping scripts/mapping.yaml \
  --src images \
  --dst assets/images/photos \
  --action copy
```

## Testing
- ✅ Scripts execute without errors
- ✅ All 8 thumbnails generated successfully
- ✅ JSON data file created with correct structure
- ✅ Photos organized in correct directory structure
- ✅ Gallery page created with proper front matter

## Next Steps
This PR establishes the foundation for the photo gallery system. Future PRs can:
- Add more albums (e.g., photos-by-trails)
- Implement category-based organization
- Add gallery display functionality in Jekyll templates
- Create index pages for browsing all albums/categories

## Related
- This is the first of two PRs for the photo gallery system
- Second PR: `photos-by-trails` (to be created)
