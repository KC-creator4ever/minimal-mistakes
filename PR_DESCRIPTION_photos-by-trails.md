# PR: Add Photo Gallery System - Trails Category (photos-by-trails)

## Overview
This PR extends the photo gallery system by adding a trails category organization feature. It demonstrates how to use the category-based organization alongside the existing album-based system.

## What's Included

### 1. Trails Category
- New category: `trails` for trail-related photos
- Uses the existing `assign_categories.py` and `generate_thumbnails.py` scripts
- Demonstrates category-based photo organization

### 2. Updated Mapping File
- **`scripts/mapping-trails.yaml`**: New mapping file for trails category
  - Maps photos to the `trails` category
  - Can include photos from multiple albums

### 3. Category Data
- **`data/photos/by-category.json`**: JSON file containing category metadata
  - Category: `trails`
  - Photos with metadata (filename, title, date, paths)

### 4. Category Gallery Page
- **`photos/trails.md`**: Markdown page for the trails category gallery
  - Permalink: `/photos/trails/`
  - Layout: `gallery`
  - Language: `zh-TW` (or as needed)

## Directory Structure
```
minimal-mistakes/
├── scripts/
│   └── mapping-trails.yaml              # Mapping file for trails category
├── data/
│   └── photos/
│       ├── by-album.json                # Existing album data
│       └── by-category.json             # New category data
├── assets/
│   └── images/
│       └── photos/
│           ├── albums/                  # Existing albums
│           ├── by-category/
│           │   └── trails/              # Category photos
│           └── thumbnails/
│               ├── albums/              # Existing album thumbnails
│               └── by-category/
│                   └── trails/          # Category thumbnails
└── photos/
    ├── fu-mountain.md                   # Existing gallery
    └── trails.md                        # New category gallery
```

## Usage Example

### Step 1: Create Mapping File
Create `scripts/mapping-trails.yaml`:
```yaml
# Example: Assign some photos to trails category
LINE_ALBUM_福山步道_251211_1.jpg: trails
LINE_ALBUM_福山步道_251211_2.jpg: trails
LINE_ALBUM_福山步道_251211_3.jpg: trails
# Add more photos as needed
```

### Step 2: Assign Photos to Category
```bash
python3 scripts/assign_categories.py \
  --mapping scripts/mapping-trails.yaml \
  --src images \
  --dst assets/images/photos \
  --action copy
```

### Step 3: Generate Thumbnails for Category
```bash
python3 scripts/generate_thumbnails.py \
  --mode category \
  --src assets/images/photos/by-category/trails \
  --dst assets/images/photos \
  --category trails \
  --thumb-width 400
```

### Step 4: Create Gallery Page
Create `photos/trails.md`:
```markdown
---
layout: gallery
title: "山徑步道"
permalink: /photos/trails/
lang: "zh-TW"
---

Trail photos from various hiking adventures.
```

## Technical Details

### Category vs. Album Organization
- **Albums**: Grouping of photos from a single event/location (e.g., Fu Mountain Trail)
- **Categories**: Topical grouping across multiple albums (e.g., all trail photos)
- Photos can belong to both an album AND categories
- Same photo can appear in multiple categories

### Data Structure
**by-category.json format:**
```json
{
  "trails": {
    "category": "trails",
    "photos": [
      {
        "filename": "photo.jpg",
        "title": "Photo Title",
        "date": "2025-12-11",
        "path": "assets/images/photos/by-category/trails/photo.jpg",
        "thumbnail": "assets/images/photos/thumbnails/by-category/trails/photo.jpg"
      }
    ]
  }
}
```

## Workflow
1. **Source photos**: Start with photos in `images/` directory
2. **Create mapping**: Define which photos belong to which categories
3. **Assign categories**: Run `assign_categories.py` to copy/move/symlink photos
4. **Generate thumbnails**: Run `generate_thumbnails.py` in category mode
5. **Create gallery page**: Add markdown file in `photos/` directory
6. **View gallery**: Navigate to `/photos/trails/` on the site

## Features Demonstrated
- ✅ Category-based organization
- ✅ Cross-album photo grouping
- ✅ Reusable scripts from first PR
- ✅ Flexible photo organization
- ✅ Multi-dimensional photo browsing (by album AND by category)

## Testing
Before submitting this PR, verify:
- [ ] Mapping file created
- [ ] Photos copied to category directory
- [ ] Thumbnails generated successfully
- [ ] by-category.json created/updated correctly
- [ ] Gallery page created with proper front matter
- [ ] No conflicts with existing album data

## Dependencies
- Requires PR #1 (photos-by-FuMountain) to be merged first
- Uses the same scripts and layout from PR #1

## Example Use Cases
- **Trails category**: All trail photos from multiple albums
- **Seasons category**: Photos organized by season
- **Wildlife category**: Animal photos from various trips
- **Landscape category**: Scenic landscape photos
- **Activity category**: Hiking, camping, climbing, etc.

## Benefits
- **Flexible organization**: Browse photos by album OR by topic
- **Reusable content**: Same photo appears in multiple contexts
- **Easy maintenance**: Update categories without affecting albums
- **Scalable**: Add new categories without restructuring existing albums

## Related
- Depends on PR #1: `photos-by-FuMountain`
- Demonstrates advanced usage of the photo gallery system
