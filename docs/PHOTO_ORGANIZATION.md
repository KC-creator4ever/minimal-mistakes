# 相片組織說明文件

本文件說明如何使用相簿模式來組織和展示照片。

## 目錄結構

相片按相簿組織，使用以下目錄結構：

```
assets/images/photos/
├── albums/
│   └── {相簿ID}/
│       └── {原始圖檔}
└── thumbnails/
    └── albums/
        └── {相簿ID}/
            └── {縮圖檔案}

data/photos/
└── by-album.json          # 相簿元數據

photos/
└── {相簿ID}.md            # 相簿展示頁面

scripts/
├── generate_thumbnails.py # 縮圖生成腳本
├── assign_categories.py   # 分類指派腳本
└── mapping.yaml           # 檔案與分類對應表
```

## 在本地執行腳本

### 安裝依賴套件

```bash
pip install pillow
```

如需使用分類指派功能，還需安裝：

```bash
pip install pyyaml
```

### 生成相簿縮圖

使用 `generate_thumbnails.py` 腳本來處理相簿：

```bash
python scripts/generate_thumbnails.py \
  --mode album \
  --src {來源目錄} \
  --dst assets/images/photos \
  --album-id {相簿ID} \
  --thumb-width 400
```

**參數說明：**
- `--mode`：處理模式（目前僅支援 `album`）
- `--src`：包含原始圖檔的來源目錄
- `--dst`：處理後圖檔的目標基礎目錄
- `--album-id`：相簿識別碼（使用 ASCII slug，例如：`fu-mountain`）
- `--thumb-width`：縮圖寬度（像素），預設值為 400

**範例：**

```bash
# 為福山步道相簿生成縮圖
python scripts/generate_thumbnails.py \
  --mode album \
  --src /tmp/fu-mountain-images \
  --dst assets/images/photos \
  --album-id fu-mountain \
  --thumb-width 400
```

此腳本會：
1. 複製原始圖檔到 `assets/images/photos/albums/{相簿ID}/`
2. 生成指定寬度的縮圖（保持長寬比）
3. 將縮圖儲存至 `assets/images/photos/thumbnails/albums/{相簿ID}/`
4. 建立或更新 `data/photos/by-album.json` 檔案

### 使用分類指派腳本

`assign_categories.py` 腳本可根據對應表將照片指派到不同分類：

```bash
python scripts/assign_categories.py \
  --mapping scripts/mapping.yaml \
  --src {來源目錄} \
  --dst {目標目錄} \
  --action {copy|move|symlink}
```

**參數說明：**
- `--mapping`：對應表 YAML 檔案路徑
- `--src`：包含圖檔的來源目錄
- `--dst`：目標基礎目錄
- `--action`：執行動作
  - `copy`：複製檔案
  - `move`：移動檔案
  - `symlink`：建立符號連結

**mapping.yaml 格式：**

```yaml
mapping:
  檔案名稱1.jpg: 分類名稱
  檔案名稱2.jpg: 分類名稱
```

## 檔案配置

### 相簿資料 (data/photos/by-album.json)

此 JSON 檔案包含所有相簿的元數據：

```json
{
  "albums": [
    {
      "id": "相簿ID",
      "title": "相簿標題",
      "cover": "封面圖檔路徑",
      "photos": [
        {
          "filename": "原始檔名",
          "title": "照片標題",
          "date": "日期（YYYY-MM-DD）",
          "path": "原始圖檔相對路徑",
          "thumbnail": "縮圖相對路徑"
        }
      ]
    }
  ]
}
```

### 相簿頁面

每個相簿都有對應的 Markdown 頁面（例如：`photos/fu-mountain.md`），包含：

**Front Matter：**
```yaml
---
layout: gallery
title: "相簿標題"
permalink: /photos/{相簿ID}/
lang: "zh-TW"
---
```

頁面內容會從 `data/photos/by-album.json` 讀取資料並渲染縮圖畫廊。

## 日期和標題處理

腳本會自動從檔案名稱解析日期和標題：

- **日期格式：** YYYYMMDD 或 YYMMDD
  - 範例：`LINE_ALBUM_福山步道_251211_1.jpg` → 日期：`2025-12-11`
- **標題：** 使用檔案名稱（不含副檔名）

若無法從檔名解析日期，則該欄位留空。

## 相對路徑

所有路徑都使用 POSIX 風格斜線（`/`）的相對路徑，確保在 GitHub Pages 上正常運作。

## 提交圖檔

在此分支中，根據使用者許可，原始圖檔和縮圖都會提交到版本庫。這可確保：
- 圖檔立即可用於展示
- 無需額外的建置步驟
- 可在 GitHub Pages 上直接運作

## 福山步道相簿範例

福山步道相簿使用以下設定：
- **相簿ID：** `fu-mountain`
- **標題：** 福山步道
- **圖檔數量：** 8 張
- **縮圖寬度：** 400px
- **頁面：** `/photos/fu-mountain/`

## 注意事項

1. 使用 ASCII slug 作為目錄名稱（例如：`fu-mountain`），避免路徑問題
2. 縮圖自動轉換為 JPEG 格式以最佳化檔案大小
3. 所有路徑都相對於網站根目錄，以 `/` 開頭
4. 此實作不使用 EXIF 資料，僅從檔名解析日期和標題
