#!/usr/bin/env python3
"""
assign_categories.py
- 根據 mapping (YAML 或 CSV) 將檔案 copy/move/symlink 到 assets/images/photos/by-category/<category>/
用法:
  python3 scripts/assign_categories.py --mapping scripts/mapping.yaml --src images --dst assets/images/photos --action copy
依賴: pyyaml (pip install pyyaml)

注意事項 / Notes:
- symlink action 使用絕對路徑，可能導致 repository 移動時失效
- symlink action uses absolute paths which may break when repository is moved
- 建議使用 copy action 以確保可攜性 / Use copy action for better portability
"""
import argparse
import yaml
import csv
from pathlib import Path
import shutil
import sys

def load_mapping(path):
    p = Path(path)
    if p.suffix in (".yaml",".yml"):
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    elif p.suffix == ".csv":
        out = {}
        with p.open(encoding="utf-8") as f:
            r = csv.reader(f)
            for row in r:
                if len(row) >= 2:
                    out[row[0].strip()] = row[1].strip()
        return out
    else:
        raise SystemExit("mapping must be yaml or csv")

def safe_mkdir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", required=True, help="mapping file (yaml or csv)")
    parser.add_argument("--src", required=True, help="source folder of original images")
    parser.add_argument("--dst", required=True, help="destination base (assets/images/photos)")
    parser.add_argument("--action", choices=("copy","move","symlink"), default="copy")
    args = parser.parse_args()

    mapping = load_mapping(args.mapping)
    src = Path(args.src)
    dst = Path(args.dst)

    for filename, category in mapping.items():
        src_path = src / filename
        if not src_path.exists():
            print(f"source missing: {src_path}", file=sys.stderr)
            continue
        target_dir = dst / "by-category" / category
        safe_mkdir(target_dir)
        target_path = target_dir / src_path.name
        if args.action == "copy":
            shutil.copy2(src_path, target_path)
            print(f"copied {src_path} -> {target_path}")
        elif args.action == "move":
            shutil.move(src_path, target_path)
            print(f"moved {src_path} -> {target_path}")
        else:
            try:
                if target_path.exists():
                    target_path.unlink()
                target_path.symlink_to(src_path.resolve())
                print(f"symlinked {target_path} -> {src_path}")
            except Exception as e:
                print(f"symlink failed: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
