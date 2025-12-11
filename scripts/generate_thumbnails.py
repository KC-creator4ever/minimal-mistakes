#!/usr/bin/env python3
"""
generate_thumbnails.py
- 針對 album 或 category 產生縮圖並更新 data/photos/*.json
- 預設縮圖寬度 400px
用法:
  python3 scripts/generate_thumbnails.py --mode album --src images --dst assets/images/photos --album-id fu-mountain --thumb-width 400
依賴: Pillow (pip install pillow)
"""
import os
import sys
import json
import shutil
from PIL import Image
from pathlib import Path
import argparse
import re
from datetime import datetime

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower())

def parse_date_from_filename(name):
    # Try explicit date formats first
    for fmt in ("%Y%m%d", "%y%m%d", "%Y-%m-%d", "%y-%m-%d"):
        try:
            return datetime.strptime(name, fmt).date().isoformat()
        except Exception:
            pass
    # Look for 8-digit date (YYYYMMDD)
    m = re.search(r'(\d{8})', name)
    if m:
        try:
            date = datetime.strptime(m.group(1), "%Y%m%d").date()
            # Validate reasonable year range (1900-2100)
            if 1900 <= date.year <= 2100:
                return date.isoformat()
        except Exception:
            pass
    # Look for 6-digit date (YYMMDD) - be more careful
    m2 = re.search(r'(\d{6})', name)
    if m2:
        try:
            date = datetime.strptime(m2.group(1), "%y%m%d").date()
            # Validate the date is reasonable (month 1-12, day 1-31)
            if 1 <= date.month <= 12 and 1 <= date.day <= 31:
                return date.isoformat()
        except Exception:
            pass
    return ""

def safe_make_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def make_thumbnail(in_path, out_path, width):
    try:
        img = Image.open(in_path)
        img = img.convert("RGB")
        w, h = img.size
        if w <= width:
            img.save(out_path, "JPEG", quality=85)
        else:
            ratio = width / float(w)
            img = img.resize((width, int(h * ratio)), Image.LANCZOS)
            img.save(out_path, "JPEG", quality=85)
        return True
    except Exception as e:
        print(f"Error creating thumbnail for {in_path}: {e}", file=sys.stderr)
        return False

def build_album_index(dst_base, album_id, files, album_title=None):
    album = {
        "id": album_id,
        "title": album_title if album_title else album_id,
        "cover": "",
        "photos": []
    }
    for i, fname in enumerate(files):
        title = Path(fname).stem
        date = parse_date_from_filename(title)
        rel_full = str(Path(dst_base) / "albums" / album_id / fname).replace("\\","/")
        rel_thumb = str(Path(dst_base) / "thumbnails" / "albums" / album_id / (Path(fname).stem + ".jpg")).replace("\\","/")
        if i == 0:
            album["cover"] = rel_thumb
        album["photos"].append({
            "filename": fname,
            "title": title,
            "date": date,
            "path": rel_full,
            "thumbnail": rel_thumb
        })
    return album

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("album","category"), required=True)
    parser.add_argument("--src", required=True, help="source directory containing original images (e.g. images)")
    parser.add_argument("--dst", required=True, help="destination base (e.g. assets/images/photos)")
    parser.add_argument("--thumb-width", type=int, default=400)
    parser.add_argument("--album-id", help="album id for mode=album")
    parser.add_argument("--album-title", help="album title for mode=album (defaults to album-id)")
    parser.add_argument("--category", help="category for mode=category")
    args = parser.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    safe_make_dir(dst)
    thumbs_base = dst / "thumbnails"
    safe_make_dir(thumbs_base)

    img_exts = {".jpg",".jpeg",".png",".webp"}
    files = sorted([p for p in src.iterdir() if p.is_file() and p.suffix.lower() in img_exts])

    if args.mode == "album":
        if not args.album_id:
            print("album_id required for album mode", file=sys.stderr)
            sys.exit(1)
        album_id = args.album_id
        target_dir = dst / "albums" / album_id
        thumb_dir = thumbs_base / "albums" / album_id
        safe_make_dir(target_dir)
        safe_make_dir(thumb_dir)
        copied = []
        for f in files:
            dest = target_dir / f.name
            shutil.copy2(f, dest)
            thumb_out = thumb_dir / (f.stem + ".jpg")
            make_thumbnail(dest, thumb_out, args.thumb_width)
            copied.append(str(dest.name))
        album = build_album_index(dst, album_id, copied, args.album_title)
        out_data_dir = Path("data/photos")
        safe_make_dir(out_data_dir)
        by_album = []
        if (out_data_dir / "by-album.json").exists():
            try:
                by_album = json.loads((out_data_dir / "by-album.json").read_text(encoding="utf-8"))
            except Exception:
                by_album = []
        replaced = False
        for i, a in enumerate(by_album):
            if a.get("id") == album_id:
                by_album[i] = album
                replaced = True
                break
        if not replaced:
            by_album.append(album)
        (out_data_dir / "by-album.json").write_text(json.dumps(by_album, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote album {album_id} with {len(album['photos'])} photos to data/photos/by-album.json")
    else:
        if not args.category:
            print("category required for category mode", file=sys.stderr)
            sys.exit(1)
        category = slugify(args.category)
        target_dir = dst / "by-category" / category
        thumb_dir = thumbs_base / "by-category" / category
        safe_make_dir(target_dir)
        safe_make_dir(thumb_dir)
        copied = []
        for f in files:
            dest = target_dir / f.name
            shutil.copy2(f, dest)
            thumb_out = thumb_dir / (f.stem + ".jpg")
            make_thumbnail(dest, thumb_out, args.thumb_width)
            copied.append(str(dest.name))
        # build simple category index
        cat = {"category": category, "photos": []}
        for fname in copied:
            title = Path(fname).stem
            date = parse_date_from_filename(title)
            rel_full = str(Path(dst) / "by-category" / category / fname).replace("\\","/")
            rel_thumb = str(Path(dst) / "thumbnails" / "by-category" / category / (Path(fname).stem + ".jpg")).replace("\\","/")
            cat["photos"].append({
                "filename": fname,
                "title": title,
                "date": date,
                "path": rel_full,
                "thumbnail": rel_thumb
            })
        out_data_dir = Path("data/photos")
        safe_make_dir(out_data_dir)
        by_cat = {}
        if (out_data_dir / "by-category.json").exists():
            try:
                by_cat = json.loads((out_data_dir / "by-category.json").read_text(encoding="utf-8"))
            except Exception:
                by_cat = {}
        by_cat[category] = cat
        (out_data_dir / "by-category.json").write_text(json.dumps(by_cat, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote category {category} with {len(cat['photos'])} photos to data/photos/by-category.json")

if __name__ == "__main__":
    main()
