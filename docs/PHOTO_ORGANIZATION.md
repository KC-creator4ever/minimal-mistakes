# 相簿組織系統說明

此文檔說明如何使用相簿模式組織和管理網站上的照片。

## 目錄結構

相簿系統使用以下目錄結構：

```
assets/images/photos/
├── albums/
│   └── {album-id}/           # 原始照片檔案
│       └── *.jpg
└── thumbnails/
    └── albums/
        └── {album-id}/       # 縮圖檔案 (400px 寬)
            └── *.jpg

data/photos/
└── by-album.json             # 相簿索引資料

photos/
└── {album-id}.md             # 相簿頁面

scripts/
├── generate_thumbnails.py    # 生成縮圖和更新索引
├── assign_categories.py      # 按類別分配照片
└── mapping.yaml              # 照片到類別的映射
```

## 安裝依賴

在本地運行腳本之前，需要安裝 Python 依賴：

```bash
pip install pillow
```

對於 `assign_categories.py` 腳本，還需要：

```bash
pip install pyyaml
```

## 使用方法

### 1. 生成縮圖和相簿索引

使用 `generate_thumbnails.py` 腳本來處理照片、生成縮圖並更新相簿索引：

```bash
# 基本用法：為 fu-mountain 相簿生成縮圖
python scripts/generate_thumbnails.py \
  --mode album \
  --src . \
  --dst assets/images/photos \
  --album-id fu-mountain \
  --album-title "福山步道" \
  --thumb-width 400
```

**參數說明：**

- `--mode album`: 處理模式（目前僅支援 album）
- `--src`: 源照片目錄
- `--dst`: 目標目錄（照片將被複製到此處）
- `--album-id`: 相簿標識符（用於 URL 和目錄名稱，使用 ASCII 字符）
- `--album-title`: 相簿標題（可選，默認使用 album-id）
- `--thumb-width`: 縮圖寬度（像素，默認 400）
- `--pattern`: 檔案匹配模式（可選）

**腳本執行的操作：**

1. 將原始照片從源目錄複製到 `dst/albums/{album-id}/`
2. 生成縮圖到 `dst/thumbnails/albums/{album-id}/`
3. 從檔名解析日期（支援 YYYYMMDD 或 YYMMDD 格式）
4. 創建或更新 `data/photos/by-album.json` 檔案

### 2. 按類別分配照片

使用 `assign_categories.py` 腳本根據映射檔案將照片分配到類別：

```bash
python scripts/assign_categories.py \
  --mapping scripts/mapping.yaml \
  --src . \
  --dst organized \
  --action copy
```

**參數說明：**

- `--mapping`: YAML 映射檔案路徑
- `--src`: 源照片目錄
- `--dst`: 目標基礎目錄
- `--action`: 操作類型（copy、move 或 symlink）

**映射檔案格式 (mapping.yaml)：**

```yaml
photo1.jpg: category-name
photo2.jpg: category-name
photo3.jpg: another-category
```

### 3. 創建相簿頁面

為每個相簿創建一個 Markdown 頁面，例如 `photos/fu-mountain.md`：

```markdown
---
layout: gallery
title: "福山步道"
permalink: /photos/fu-mountain/
lang: "zh-TW"
album_id: fu-mountain
---

相簿描述文字
```

**前置資料欄位：**

- `layout: gallery`: 使用相簿佈局
- `title`: 頁面標題
- `permalink`: 頁面 URL
- `lang`: 語言代碼
- `album_id`: 對應 by-album.json 中的相簿 ID

## 檔案格式

### by-album.json 結構

```json
{
  "albums": [
    {
      "id": "album-id",
      "title": "相簿標題",
      "cover": "assets/images/photos/thumbnails/albums/album-id/cover.jpg",
      "photos": [
        {
          "filename": "photo.jpg",
          "title": "照片標題",
          "date": "2025-12-11",
          "path": "assets/images/photos/albums/album-id/photo.jpg",
          "thumbnail": "assets/images/photos/thumbnails/albums/album-id/photo.jpg"
        }
      ]
    }
  ]
}
```

## 日期解析

腳本會自動從檔名中解析日期：

- **YYMMDD 格式**: `file_251211_1.jpg` → `2025-12-11`
- **YYYYMMDD 格式**: `file_20251211_1.jpg` → `2025-12-11`

如果檔名中沒有找到日期模式，`date` 欄位將為空字串。

## 本地測試

在提交更改之前，可以在本地測試相簿頁面：

```bash
# 安裝 Jekyll 依賴（如果尚未安裝）
bundle install

# 在本地啟動 Jekyll 服務器
bundle exec jekyll serve

# 訪問 http://localhost:4000/photos/fu-mountain/
```

## 注意事項

### 關於提交照片

此分支中已提交原始照片和縮圖檔案。這是根據用戶許可執行的操作。

- **原始照片**: `assets/images/photos/albums/`
- **縮圖**: `assets/images/photos/thumbnails/albums/`

### 目錄命名

- 使用 ASCII 字符作為目錄名稱（例如 `fu-mountain`）
- 使用短橫線分隔單詞
- 避免在目錄名稱中使用非 ASCII 字符，以確保跨平台兼容性

### 相對路徑

所有照片路徑都使用 POSIX 風格的正斜杠（`/`）和相對路徑，以確保在 GitHub Pages 上正常工作。

## 新增相簿範例

要新增新相簿，請遵循以下步驟：

1. 將照片放在一個目錄中
2. 更新 `scripts/mapping.yaml`（如果使用類別分配）
3. 運行 `generate_thumbnails.py` 腳本
4. 創建相簿頁面 Markdown 檔案
5. 提交所有更改

```bash
# 範例：新增名為 "sunset-beach" 的相簿
python scripts/generate_thumbnails.py \
  --mode album \
  --src photos/raw \
  --dst assets/images/photos \
  --album-id sunset-beach \
  --album-title "日落海灘" \
  --pattern "beach_*.jpg"
```

## 疑難排解

### 縮圖品質

縮圖使用 JPEG 格式，品質設置為 85。如需調整品質，請編輯 `scripts/generate_thumbnails.py` 中的 `quality` 參數。

### 檔名中的特殊字符

腳本支援 UTF-8 檔名（包括中文字符）。確保您的終端和編輯器都設置為使用 UTF-8 編碼。

## 未來改進

可能的增強功能：

- 支援從 EXIF 資料中提取日期和元資料
- 支援多種圖片格式（PNG、WebP 等）
- 自動化的圖片優化
- 批量處理工具
- Web 介面用於上傳和組織照片
