# Photo Gallery System - Complete Implementation Guide

## 概述 (Overview)
這個實作包含了一個完整的照片畫廊系統，分為兩個 PR：
1. **photos-by-FuMountain**: 基礎系統和福山步道相簿
2. **photos-by-trails**: 分類系統示範（山徑步道分類）

This implementation includes a complete photo gallery system, split into two PRs:
1. **photos-by-FuMountain**: Foundation system with Fu Mountain Trail album
2. **photos-by-trails**: Category system demonstration (trails category)

## 已完成的檔案 (Completed Files)

### PR #1: photos-by-FuMountain ✅

#### Scripts (`scripts/`)
- ✅ `generate_thumbnails.py` - 縮圖產生器 (Thumbnail generator)
- ✅ `assign_categories.py` - 分類指派工具 (Category assignment tool)
- ✅ `mapping.yaml` - 福山步道照片對應 (Fu Mountain photo mapping)
- ✅ `README.md` - 完整文件 (Complete documentation)

#### Layout (`_layouts/`)
- ✅ `gallery.html` - 畫廊版型 (Gallery layout template)

#### Data (`data/photos/`)
- ✅ `by-album.json` - 相簿資料 (Album data)
  - fu-mountain 相簿：8 張照片
  - 完整的 metadata（檔名、標題、日期、路徑）

#### Photos (`photos/`)
- ✅ `fu-mountain.md` - 福山步道畫廊頁面 (Fu Mountain gallery page)

#### Images
- ✅ `images/` - 原始照片 (Original photos): 8 張
- ✅ `assets/images/photos/albums/fu-mountain/` - 完整照片 (Full-size): 8 張
- ✅ `assets/images/photos/thumbnails/albums/fu-mountain/` - 縮圖 (Thumbnails): 8 張

#### Documentation
- ✅ `PR_DESCRIPTION_photos-by-FuMountain.md` - 第一個 PR 的描述

### PR #2: photos-by-trails (準備就緒 - Ready to implement)

#### 需要建立的檔案 (Files to create)
- [ ] `scripts/mapping-trails.yaml` - 山徑分類對應檔
- [ ] `data/photos/by-category.json` - 分類資料檔
- [ ] `photos/trails.md` - 山徑畫廊頁面
- [ ] 執行腳本產生分類照片和縮圖

#### Documentation
- ✅ `PR_DESCRIPTION_photos-by-trails.md` - 第二個 PR 的描述（已準備）

## 系統架構 (System Architecture)

### 資料夾結構 (Directory Structure)
```
minimal-mistakes/
├── scripts/                      # 工具腳本 (Utility scripts)
│   ├── generate_thumbnails.py   # 縮圖產生器
│   ├── assign_categories.py     # 分類指派
│   ├── mapping.yaml             # 福山步道對應
│   ├── mapping-trails.yaml      # 山徑分類對應 (for PR #2)
│   └── README.md                # 文件
├── _layouts/
│   └── gallery.html             # 畫廊版型
├── images/                       # 原始照片來源
├── data/
│   └── photos/
│       ├── by-album.json        # 相簿索引
│       └── by-category.json     # 分類索引 (for PR #2)
├── assets/
│   └── images/
│       └── photos/
│           ├── albums/           # 相簿照片
│           │   └── fu-mountain/
│           ├── by-category/      # 分類照片 (for PR #2)
│           │   └── trails/
│           └── thumbnails/       # 縮圖
│               ├── albums/
│               │   └── fu-mountain/
│               └── by-category/  # 分類縮圖 (for PR #2)
│                   └── trails/
└── photos/                       # 畫廊頁面
    ├── fu-mountain.md
    └── trails.md                 # (for PR #2)
```

## 使用方式 (Usage)

### 建立新相簿 (Create New Album)
```bash
# 1. 將照片放到 images/ 目錄
# 2. 執行縮圖產生器
python3 scripts/generate_thumbnails.py \
  --mode album \
  --src images \
  --dst assets/images/photos \
  --album-id your-album-id \
  --thumb-width 400

# 3. 建立畫廊頁面
# 在 photos/your-album.md 建立新檔案
```

### 建立新分類 (Create New Category)
```bash
# 1. 建立對應檔 (mapping file)
# scripts/mapping-your-category.yaml

# 2. 指派照片到分類
python3 scripts/assign_categories.py \
  --mapping scripts/mapping-your-category.yaml \
  --src images \
  --dst assets/images/photos \
  --action copy

# 3. 產生分類縮圖
python3 scripts/generate_thumbnails.py \
  --mode category \
  --src assets/images/photos/by-category/your-category \
  --dst assets/images/photos \
  --category your-category \
  --thumb-width 400

# 4. 建立分類畫廊頁面
# 在 photos/your-category.md 建立新檔案
```

## 技術細節 (Technical Details)

### 依賴套件 (Dependencies)
- Python 3.12+
- Pillow: `pip install pillow`
- PyYAML: `pip install pyyaml`

### 縮圖規格 (Thumbnail Specifications)
- 預設寬度：400px
- 格式：JPEG
- 品質：85%
- 保持長寬比 (Maintains aspect ratio)

### 日期解析 (Date Parsing)
支援的檔名格式：
- YYYYMMDD (20251211)
- YYMMDD (251211)
- YYYY-MM-DD (2025-12-11)
- YY-MM-DD (25-12-11)

### JSON 資料格式 (JSON Data Format)

**by-album.json:**
```json
[
  {
    "id": "album-id",
    "title": "Album Title",
    "cover": "path/to/cover.jpg",
    "photos": [
      {
        "filename": "photo.jpg",
        "title": "Photo Title",
        "date": "2025-12-11",
        "path": "path/to/photo.jpg",
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
        "path": "path/to/photo.jpg",
        "thumbnail": "path/to/thumbnail.jpg"
      }
    ]
  }
}
```

## 測試檢查清單 (Testing Checklist)

### PR #1: photos-by-FuMountain
- [x] Python 腳本可執行 (Scripts executable)
- [x] 依賴套件已安裝 (Dependencies installed)
- [x] 8 張照片成功複製 (8 photos copied)
- [x] 8 張縮圖成功產生 (8 thumbnails generated)
- [x] by-album.json 正確建立 (JSON created correctly)
- [x] 畫廊頁面已建立 (Gallery page created)
- [x] 版型檔案已建立 (Layout file created)

### PR #2: photos-by-trails (待執行 - To be done)
- [ ] mapping-trails.yaml 已建立
- [ ] 照片已複製到分類目錄
- [ ] 分類縮圖已產生
- [ ] by-category.json 已建立
- [ ] trails.md 畫廊頁面已建立

## PR 提交順序 (PR Submission Order)

### 1. photos-by-FuMountain (已完成 - Completed) ✅
- 包含所有基礎檔案和腳本
- 福山步道相簿（8 張照片）
- 完整的文件說明

### 2. photos-by-trails (準備中 - Ready)
- 依賴 PR #1
- 展示分類系統功能
- 可以使用相同的腳本

## 下一步 (Next Steps)

### 完成 PR #2
1. 建立 `scripts/mapping-trails.yaml`
2. 執行 `assign_categories.py`
3. 執行 `generate_thumbnails.py` (category mode)
4. 建立 `photos/trails.md`
5. 提交 PR

### 未來擴充 (Future Enhancements)
- 增加更多相簿
- 建立相簿索引頁
- 建立分類索引頁
- 增加搜尋功能
- 增加標籤系統
- EXIF 資料讀取
- 自動化部署腳本

## 維護指南 (Maintenance Guide)

### 新增照片到現有相簿
```bash
# 將新照片放到 images/
# 重新執行 generate_thumbnails.py
python3 scripts/generate_thumbnails.py --mode album --src images --dst assets/images/photos --album-id existing-album-id
```

### 新增照片到現有分類
```bash
# 更新 mapping file
# 執行 assign_categories.py
# 重新執行 generate_thumbnails.py (category mode)
```

### 更新縮圖大小
修改 `--thumb-width` 參數並重新執行腳本

## 問題排解 (Troubleshooting)

### 腳本執行錯誤
- 檢查 Python 版本（需要 3.x）
- 確認依賴套件已安裝
- 檢查檔案路徑是否正確

### 縮圖品質問題
- 調整 `--thumb-width` 參數
- 修改腳本中的 quality 參數（目前 85%）

### JSON 格式錯誤
- 使用 JSON validator 檢查
- 確認 UTF-8 編碼

## 授權與貢獻 (License & Contributing)
- 遵循 minimal-mistakes 主題授權
- 歡迎提交 issue 和 PR
- 請遵循現有的程式碼風格

## 作者 (Authors)
- GitHub Copilot
- KC-creator4ever

## 版本歷史 (Version History)
- v1.0 (2025-12-11): 初始版本，包含 fu-mountain 相簿和完整腳本系統
