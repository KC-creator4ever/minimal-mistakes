# Pull Request: Add Fu Mountain Album and Organize Photos

## Branch Information
- **Branch Name**: photos-by-FuMountain
- **Base Branch**: master
- **PR Title**: Add Fu Mountain album and organize photos (photos-by-FuMountain)

## Summary

This PR adds album-based photo organization for the Fu Mountain (福山步道) hiking trail photos. It includes:

- **8 original photos** organized in `assets/images/photos/albums/fu-mountain/`
- **8 web-optimized thumbnails** (400px width) in `assets/images/photos/thumbnails/albums/fu-mountain/`
- **Gallery page** at `/photos/fu-mountain/` with Traditional Chinese UI
- **JSON-based metadata** in `data/photos/by-album.json`
- **Python scripts** for automation
- **Comprehensive documentation** in Traditional Chinese

## Files Added

### Directory Structure
```
_layouts/
  └── gallery.html                              # Custom gallery layout for albums

assets/images/photos/
  ├── albums/fu-mountain/                       # Original photos (8 files)
  │   └── LINE_ALBUM_福山步道_251211_*.jpg
  └── thumbnails/albums/fu-mountain/            # Thumbnails (8 files, ~400px width)
      └── LINE_ALBUM_福山步道_251211_*.jpg

data/photos/
  └── by-album.json                             # Album index with metadata

photos/
  ├── fu-mountain.md                            # Gallery page
  └── README.md                                 # Photos directory README

scripts/
  ├── generate_thumbnails.py                    # Generate thumbnails and update index
  ├── assign_categories.py                      # Assign photos to categories
  ├── mapping.yaml                              # Photo-to-category mapping
  └── README.md                                 # Scripts documentation

docs/
  └── PHOTO_ORGANIZATION.md                     # Complete documentation (Traditional Chinese)
```

### Total Changes
- **25 files added**
- **728 insertions**
- Original photos: ~4.2MB
- Thumbnails: ~537KB

## Features

### 1. Album Organization
- Photos organized by album ID (fu-mountain)
- Original images preserved at full resolution
- Thumbnails automatically generated at 400px width
- All paths use POSIX-style forward slashes for GitHub Pages compatibility

### 2. Gallery Page
- URL: `/photos/fu-mountain/`
- Traditional Chinese title: "福山步道"
- Responsive grid layout (auto-fills based on screen size)
- Thumbnail images link to full-size originals
- Displays filename and parsed date for each photo

### 3. Metadata System
- JSON-based album index at `data/photos/by-album.json`
- Each photo includes:
  - filename
  - title (from filename)
  - date (parsed from filename: YYMMDD → YYYY-MM-DD)
  - path to original
  - path to thumbnail
- Dates parsed from filename: `251211` → `2025-12-11`

### 4. Automation Scripts

#### generate_thumbnails.py
```bash
python scripts/generate_thumbnails.py \
  --mode album \
  --src . \
  --dst assets/images/photos \
  --album-id fu-mountain \
  --album-title "福山步道" \
  --thumb-width 400
```

Features:
- Copies originals to albums directory
- Generates JPEG thumbnails with aspect ratio preserved
- Parses dates from filenames (YYMMDD or YYYYMMDD formats)
- Creates/updates by-album.json automatically
- Uses Pillow (PIL) for high-quality image processing

#### assign_categories.py
```bash
python scripts/assign_categories.py \
  --mapping scripts/mapping.yaml \
  --src . \
  --dst organized \
  --action copy
```

Features:
- Maps photos to categories using YAML file
- Supports copy, move, or symlink actions
- Useful for organizing photos before album processing

### 5. Documentation
- Complete usage guide in Traditional Chinese
- Installation instructions for dependencies
- Example commands for common tasks
- Troubleshooting section
- Directory structure explanation

## Technical Details

### Dependencies
```bash
pip install pillow      # For generate_thumbnails.py
pip install pyyaml      # For assign_categories.py (optional)
```

### Filename Date Parsing
The system automatically parses dates from filenames:
- Pattern: `_YYMMDD_` or `_YYYYMMDD_`
- Example: `LINE_ALBUM_福山步道_251211_1.jpg` → date: `2025-12-11`

### Image Processing
- Thumbnails: 400px width, height calculated to maintain aspect ratio
- Format: JPEG with 85% quality
- Resampling: Lanczos (high quality)

### Gallery Layout
- Responsive CSS Grid
- Minimum column width: 300px
- Auto-fill layout adapts to screen size
- Hover effects on thumbnails
- Border and shadow for visual appeal

## How to Test Locally

1. **Install dependencies**:
   ```bash
   pip install pillow
   ```

2. **Start Jekyll**:
   ```bash
   bundle install
   bundle exec jekyll serve
   ```

3. **View gallery**:
   - Navigate to `http://localhost:4000/photos/fu-mountain/`
   - Click thumbnails to view full-size images
   - Verify all 8 photos display correctly

4. **Regenerate thumbnails** (if needed):
   ```bash
   python scripts/generate_thumbnails.py \
     --mode album \
     --src . \
     --dst assets/images/photos \
     --album-id fu-mountain \
     --album-title "福山步道"
   ```

## Design Decisions

### Why Filename-Based Dates?
- No EXIF dependency in this PR (per requirements)
- Simple and predictable
- Can be enhanced with EXIF in future PR

### Why Commit Images?
- User permission granted to commit originals and thumbnails
- Ensures images are always available with the code
- Simplifies deployment to GitHub Pages

### Why ASCII Directory Names?
- `fu-mountain` instead of `福山步道` for directories
- Ensures cross-platform compatibility
- Avoids URL encoding issues
- Traditional Chinese used in UI/titles where appropriate

### Why Relative Paths?
- All paths use relative URLs (no leading `/`)
- Compatible with GitHub Pages subdirectory deployments
- Example: `assets/images/photos/albums/...`

## Files Not Modified

As requested, the following files were **NOT** modified:
- `_data/navigation.yml` - Navigation unchanged
- `_config.yml` - Site configuration unchanged

## Future Enhancements

Potential improvements for future PRs:
- EXIF metadata extraction for dates and camera info
- WebP format support for better compression
- Automatic image optimization
- Multi-album index page
- Category-based browsing
- Search functionality
- Bulk upload tools

## Validation

All changes have been validated:
- ✅ All 8 photos copied to albums directory
- ✅ All 8 thumbnails generated at 400px width
- ✅ by-album.json created with correct structure
- ✅ Gallery page created with Traditional Chinese metadata
- ✅ Scripts are executable and documented
- ✅ Documentation is comprehensive and in Traditional Chinese
- ✅ All paths use POSIX-style forward slashes
- ✅ Directory names use ASCII slugs
- ✅ No modifications to navigation.yml or _config.yml

## Notes

- This PR introduces a new photo organization system that can be extended for additional albums
- The gallery layout is reusable for future albums
- The scripts are designed to be run manually as needed
- All Chinese text uses Traditional Chinese (zh-TW) as specified
- Images are committed to the repository per user permission

## Related Documentation

- See `docs/PHOTO_ORGANIZATION.md` for complete usage guide
- See `scripts/README.md` for scripts overview
