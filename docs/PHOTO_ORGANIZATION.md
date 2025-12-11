# 照片組織說明文件

本文件說明如何使用相簿模式來組織和管理網站上的照片。

## 目錄結構

照片組織採用以下目錄結構：

```
assets/images/photos/
├── albums/              # 原始照片存放位置
│   └── fu-mountain/     # 相簿目錄（以相簿 ID 命名）
│       ├── LINE_ALBUM_福山步道_251211_1.jpg
│       └── ...
└── thumbnails/          # 縮圖存放位置
    └── albums/
        └── fu-mountain/ # 對應的縮圖目錄
            ├── LINE_ALBUM_福山步道_251211_1.jpg
            └── ...

data/photos/
└── by-album.json        # 相簿元資料索引

photos/
└── fu-mountain.md       # 相簿展示頁面

scripts/
├── generate_thumbnails.py  # 縮圖生成工具
├── assign_categories.py    # 照片分類工具
└── fu-mountain-mapping.csv # 照片分類對應表範例
```

## 相簿模式說明

相簿模式是一種以主題或事件為單位來組織照片的方式。每個相簿：

- 有唯一的 ID（使用 ASCII 字元，如 `fu-mountain`）
- 包含一組相關的照片
- 擁有自己的展示頁面
- 在元資料檔案中記錄詳細資訊

## 如何新增照片

### 步驟 1：準備照片

1. 將照片檔案放在儲存庫的根目錄或任何臨時位置
2. 確保照片檔名有意義（建議包含日期資訊）

### 步驟 2：建立相簿目錄

```bash
# 建立新相簿目錄（將 album-name 替換為您的相簿 ID）
mkdir -p assets/images/photos/albums/album-name
mkdir -p assets/images/photos/thumbnails/albums/album-name
```

### 步驟 3：複製照片到相簿目錄

```bash
# 手動複製
cp 照片檔案.jpg assets/images/photos/albums/album-name/

# 或使用分類工具（見下方說明）
```

### 步驟 4：生成縮圖

使用縮圖生成工具自動建立縮圖並更新元資料：

```bash
# 為所有相簿生成縮圖
python3 scripts/generate_thumbnails.py

# 只為特定相簿生成縮圖
python3 scripts/generate_thumbnails.py --album album-name

# 自訂縮圖寬度（預設 400 像素）
python3 scripts/generate_thumbnails.py --width 500
```

**依賴套件**：執行前需先安裝 Pillow

```bash
pip install Pillow
```

### 步驟 5：建立相簿頁面

在 `photos/` 目錄下建立相簿展示頁面（如 `album-name.md`）：

```markdown
---
layout: single
title: "相簿標題"
permalink: /photos/album-name/
author_profile: true
gallery:
  - url: /assets/images/photos/albums/album-name/photo1.jpg
    image_path: /assets/images/photos/thumbnails/albums/album-name/photo1.jpg
    alt: "照片 1"
    title: "照片 1"
  - url: /assets/images/photos/albums/album-name/photo2.jpg
    image_path: /assets/images/photos/thumbnails/albums/album-name/photo2.jpg
    alt: "照片 2"
    title: "照片 2"
---

# 相簿標題

相簿說明文字。

{% include gallery caption="照片集" %}
```

### 步驟 6：更新元資料（可選）

縮圖生成工具會自動建立和更新 `data/photos/by-album.json`，但您可以手動編輯以：

- 修改相簿標題
- 調整照片順序
- 更新日期資訊
- 修改照片標題

## 如何重新生成縮圖

如果原始照片有變更，或需要調整縮圖大小：

```bash
# 重新生成所有縮圖
python3 scripts/generate_thumbnails.py

# 只重新生成特定相簿的縮圖
python3 scripts/generate_thumbnails.py --album album-name

# 使用不同的縮圖寬度
python3 scripts/generate_thumbnails.py --width 600
```

縮圖生成工具會：
1. 掃描 `assets/images/photos/albums/` 下的所有相簿
2. 為每張照片生成等比例縮放的縮圖（預設寬度 400 像素）
3. 將縮圖儲存在對應的縮圖目錄
4. 更新 `data/photos/by-album.json` 元資料檔案
5. 嘗試從檔名擷取日期（格式：`_YYMMDD_`）

## 如何編輯 by-album.json

`data/photos/by-album.json` 包含所有相簿的元資料：

```json
{
  "albums": [
    {
      "id": "album-id",
      "title": "相簿標題",
      "cover": "/assets/images/photos/thumbnails/albums/album-id/cover.jpg",
      "photos": [
        {
          "path": "/assets/images/photos/albums/album-id/photo1.jpg",
          "thumbnail": "/assets/images/photos/thumbnails/albums/album-id/photo1.jpg",
          "title": "照片標題",
          "date": "2025-12-11"
        }
      ]
    }
  ],
  "generated": "2025-12-11T16:00:00.000000"
}
```

### 可編輯的欄位

- **id**: 相簿的唯一識別碼（建議使用 ASCII 字元和連字號）
- **title**: 相簿的顯示標題（可使用中文）
- **cover**: 封面圖片路徑（通常是第一張照片的縮圖）
- **photos**: 照片陣列
  - **path**: 原始照片的路徑
  - **thumbnail**: 縮圖的路徑
  - **title**: 照片標題（預設使用檔名，可自行修改）
  - **date**: 照片日期（ISO 格式：YYYY-MM-DD，可選）

### 編輯建議

1. 使用文字編輯器開啟 `data/photos/by-album.json`
2. 確保 JSON 格式正確（可使用 JSON 驗證工具）
3. 所有路徑使用絕對路徑（從網站根目錄開始，以 `/` 開頭）
4. 修改後可執行縮圖生成工具以驗證格式

## 使用照片分類工具

`scripts/assign_categories.py` 提供了批次整理照片的功能。

### 建立對應表

有兩種格式可選：

**CSV 格式** (`mapping.csv`)：
```csv
photo,album
photo1.jpg,album-name
photo2.jpg,album-name
photo3.jpg,another-album
```

**YAML 格式** (`mapping.yml`)：
```yaml
album-name:
  - photo1.jpg
  - photo2.jpg
another-album:
  - photo3.jpg
```

### 執行分類

```bash
# 預覽將會執行的動作（不實際移動檔案）
python3 scripts/assign_categories.py --mapping mapping.csv --dry-run

# 實際執行照片分類
python3 scripts/assign_categories.py --mapping mapping.csv

# 指定來源目錄
python3 scripts/assign_categories.py --mapping mapping.csv --source /path/to/photos
```

**注意**：此工具會**複製**照片而非移動，以保留原始檔案。

### 範例對應表

儲存庫中已包含福山步道相簿的範例對應表：
- `scripts/fu-mountain-mapping.csv`

## 路徑規範

為確保在 GitHub Pages 上正常運作，所有照片和縮圖的路徑都應該：

1. **使用絕對路徑**：從網站根目錄開始，以 `/` 開頭
   - 正確：`/assets/images/photos/albums/fu-mountain/photo.jpg`
   - 錯誤：`assets/images/photos/albums/fu-mountain/photo.jpg`
   - 錯誤：`../assets/images/photos/albums/fu-mountain/photo.jpg`

2. **使用相對 URL 過濾器**（在 Jekyll 模板中）：
   ```liquid
   {{ img.path | relative_url }}
   ```

3. **保持一致性**：所有元資料檔案、頁面和工具都使用相同的路徑格式

## 福山步道相簿範例

本儲存庫已包含完整的福山步道相簿範例：

- 原始照片：`assets/images/photos/albums/fu-mountain/`
- 縮圖：`assets/images/photos/thumbnails/albums/fu-mountain/`
- 相簿頁面：`photos/fu-mountain.md`
- 元資料：`data/photos/by-album.json`
- 對應表範例：`scripts/fu-mountain-mapping.csv`

可以參考這個範例來建立新的相簿。

## 常見問題

### Q: 為什麼要生成縮圖？

A: 縮圖可以加快頁面載入速度，改善使用者體驗。原始照片通常較大（數 MB），而縮圖只有數十 KB。

### Q: 可以修改縮圖的大小嗎？

A: 可以。使用 `--width` 參數指定縮圖寬度，例如：
```bash
python3 scripts/generate_thumbnails.py --width 600
```

### Q: 如果檔名中沒有日期怎麼辦？

A: 縮圖生成工具會嘗試從檔名中擷取日期（格式 `_YYMMDD_`）。如果找不到，日期欄位會被省略。您可以在 `by-album.json` 中手動新增日期。

### Q: 可以在元資料中新增更多欄位嗎？

A: 可以，但需要相應地修改相簿頁面模板來顯示這些額外欄位。

### Q: 照片的標題可以使用中文嗎？

A: 可以。標題欄位支援 UTF-8 編碼，可以使用任何語言。

## 技術細節

### 縮圖生成

- 使用 Pillow（PIL）函式庫
- 保持原始照片的長寬比
- 使用 LANCZOS 重新取樣演算法確保品質
- JPEG 品質設定為 85，並啟用最佳化

### 日期擷取

工具會從檔名中尋找 `_YYMMDD_` 格式的日期：
- 範例：`LINE_ALBUM_福山步道_251211_1.jpg` → `2025-12-11`
- 假設年份為 20YY（21 世紀）

### 路徑處理

所有路徑都使用 Python 的 `pathlib.Path` 處理，確保跨平台相容性。

## 維護建議

1. **定期備份**：原始照片檔案應該在本地保留備份
2. **版本控制**：使用 Git 追蹤 `by-album.json` 的變更
3. **一致性**：保持命名規範一致（相簿 ID 使用小寫和連字號）
4. **文件更新**：新增相簿時更新此文件

## 相關資源

- [Minimal Mistakes 文件](https://mmistakes.github.io/minimal-mistakes/)
- [Jekyll 文件](https://jekyllrb.com/docs/)
- [Pillow 文件](https://pillow.readthedocs.io/)
- [GitHub Pages 文件](https://docs.github.com/pages)
