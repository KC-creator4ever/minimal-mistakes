# Photo Gallery System

This directory contains scripts for managing photo galleries in the minimal-mistakes Jekyll theme.

## Scripts

### generate_thumbnails.py

Generates thumbnails for albums or categories and updates the JSON data files.

**Usage for albums:**
```bash
python3 scripts/generate_thumbnails.py \
  --mode album \
  --src images \
  --dst assets/images/photos \
  --album-id fu-mountain \
  --thumb-width 400
```

**Usage for categories:**
```bash
python3 scripts/generate_thumbnails.py \
  --mode category \
  --src images \
  --dst assets/images/photos \
  --category "mountain-trails" \
  --thumb-width 400
```

**Dependencies:**
- Pillow: `pip install pillow`

### assign_categories.py

Assigns photos to categories based on a mapping file (YAML or CSV).

**Usage:**
```bash
python3 scripts/assign_categories.py \
  --mapping scripts/mapping.yaml \
  --src images \
  --dst assets/images/photos \
  --action copy
```

**Dependencies:**
- PyYAML: `pip install pyyaml`

**Actions:**
- `copy`: Copy files to category directories
- `move`: Move files to category directories
- `symlink`: Create symlinks in category directories

## Directory Structure

```
minimal-mistakes/
├── scripts/
│   ├── generate_thumbnails.py
│   ├── assign_categories.py
│   └── mapping.yaml
├── images/
│   └── [original photo files]
├── data/
│   └── photos/
│       ├── by-album.json
│       └── by-category.json
├── assets/
│   └── images/
│       └── photos/
│           ├── albums/
│           │   └── [album-id]/
│           │       └── [photo files]
│           ├── by-category/
│           │   └── [category]/
│           │       └── [photo files]
│           └── thumbnails/
│               ├── albums/
│               │   └── [album-id]/
│               │       └── [thumbnail files]
│               └── by-category/
│                   └── [category]/
│                       └── [thumbnail files]
└── photos/
    └── [album-name].md (gallery pages)
```

## Example Workflow

1. Place original photos in the `images/` directory
2. Create a mapping file (optional for category assignment)
3. Run `generate_thumbnails.py` to process photos
4. Create a markdown page in `photos/` directory with `layout: gallery`
5. The JSON files in `data/photos/` will be automatically updated

## Mapping File Format

**YAML (mapping.yaml):**
```yaml
photo1.jpg: category-name
photo2.jpg: category-name
photo3.jpg: another-category
```

**CSV (mapping.csv):**
```csv
photo1.jpg,category-name
photo2.jpg,category-name
photo3.jpg,another-category
```

## Data Format

The scripts generate JSON files with the following structure:

**by-album.json:**
```json
[
  {
    "id": "album-id",
    "title": "Album Title",
    "cover": "path/to/cover/thumbnail.jpg",
    "photos": [
      {
        "filename": "photo.jpg",
        "title": "Photo Title",
        "date": "2025-12-11",
        "path": "path/to/full/photo.jpg",
        "thumbnail": "path/to/thumbnail.jpg"
      }
    ]
  }
]
```

**by-category.json:**
```json
{
  "category-name": {
    "category": "category-name",
    "photos": [
      {
        "filename": "photo.jpg",
        "title": "Photo Title",
        "date": "2025-12-11",
        "path": "path/to/full/photo.jpg",
        "thumbnail": "path/to/thumbnail.jpg"
      }
    ]
  }
}
```

## Date Parsing

The scripts automatically parse dates from filenames in the following formats:
- YYYYMMDD (e.g., 20251211)
- YYMMDD (e.g., 251211)
- YYYY-MM-DD (e.g., 2025-12-11)
- YY-MM-DD (e.g., 25-12-11)

If no date is found in the filename, the date field will be empty.
