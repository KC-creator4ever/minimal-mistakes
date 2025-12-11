# 建立兩個 PR 的步驟指南

## 目標
根據先前的對話,需要為兩款自訂皮膚分別建立 Pull Request:
1. **Beach Skin PR** - 海邊沙灘主題
2. **Forest Skin PR** - 空靈清新森林浴主題

## 當前狀態

### 已存在的分支
- `copilot/add-beach-skin` - 目前包含 **beach** 和 **forest** 兩款皮膚
- `copilot/add-forest-skin` - 本地分支,僅包含 **forest** 皮膚 (未推送)
- `master` - 包含所有皮膚的基礎分支

## 方案一:修改現有分支 (推薦)

### 步驟 1: 為 Beach Skin 準備純淨的分支

```bash
# 切換到 beach 分支
git checkout copilot/add-beach-skin

# 移除 forest skin 檔案
git rm _sass/minimal-mistakes/skins/_forest.scss

# 提交變更
git commit -m "Remove forest skin - keep beach skin only"

# 推送到遠端
git push origin copilot/add-beach-skin
```

完成後,`copilot/add-beach-skin` 分支將只包含 Beach 皮膚,可直接用於建立 PR。

### 步驟 2: 為 Forest Skin 建立新分支

```bash
# 從相同的基礎點建立 forest 分支
git checkout -b copilot/add-forest-skin f048a102

# 僅添加 forest skin 檔案
cat > _sass/minimal-mistakes/skins/_forest.scss << 'EOF'
/* ==========================================================================
   Forest skin (空靈清新森林浴)
   ========================================================================== */

/* Colors */
$forest-green: #52b788 !default;
$moss-green: #74c69d !default;
$light-sage: #d8f3dc !default;
$misty-white: #f7fff7 !default;
$deep-forest: #2d6a4f !default;
$sky-mist: #95d5b2 !default;
$earth-brown: #6c584c !default;

$background-color: $misty-white !default;
$text-color: #1b4332 !default;
$muted-text-color: mix(#000, $forest-green, 50%) !default;
$primary-color: $forest-green !default;
$border-color: mix(#fff, $moss-green, 80%) !default;
$code-background-color: $light-sage !default;
$code-background-color-dark: mix(#000, $light-sage, 15%) !default;
$form-background-color: mix(#fff, $light-sage, 50%) !default;
$footer-background-color: $moss-green !default;
$link-color: $deep-forest !default;
$link-color-hover: $forest-green !default;
$link-color-visited: mix(#000, $forest-green, 40%) !default;
$masthead-link-color: $text-color !default;
$masthead-link-color-hover: $forest-green !default;
$navicon-link-color-hover: mix(#000, $misty-white, 20%) !default;

/* Accent colors */
$success-color: $forest-green !default;
$warning-color: #f4a261 !default;
$danger-color: #e76f51 !default;
$info-color: $sky-mist !default;

/* notices */
$notice-background-mix: 85% !default;

.page__footer {
  color: #fff !important; // override
}

.page__footer-follow .social-icons i,
.page__footer-follow .social-icons .svg-inline--fa {
  color: inherit;
}

.author__urls.social-icons i,
.author__urls.social-icons .svg-inline--fa {
  color: inherit;
}
EOF

# 更新配置檔使用 forest 皮膚
# 編輯 _config.yml 的第 15 行,將 "default" 改為 "forest"

# 提交變更
git add _sass/minimal-mistakes/skins/_forest.scss _config.yml
git commit -m "Add forest skin with misty forest theme"

# 推送到遠端
git push -u origin copilot/add-forest-skin
```

## 方案二:使用 GitHub Web UI (如果無法使用命令列)

### Beach Skin PR:
1. 前往 GitHub repository
2. 切換到 `copilot/add-beach-skin` 分支
3. 手動刪除 `_sass/minimal-mistakes/skins/_forest.scss` 檔案
4. 提交變更並建立 PR

### Forest Skin PR:
1. 從 `copilot/add-beach-skin` 分支建立新分支 `copilot/add-forest-skin`
2. 刪除 `_sass/minimal-mistakes/skins/_beach.scss`
3. 將 _config.yml 中的皮膚設定從 "beach" 改為 "forest"
4. 提交變更並建立 PR

## PR 描述建議

### Beach Skin PR 描述:
```markdown
# Add Beach Skin 🏖️

添加海邊沙灘主題皮膚,帶來溫暖悠閒的海濱氛圍。

## 特色
- 溫暖的沙色調背景 (#f4e4c1)
- 海洋藍色調的鏈接和強調元素 (#4a90a4)
- 適合旅遊、生活分享等內容風格

## 檔案變更
- 新增 `_sass/minimal-mistakes/skins/_beach.scss`
- 更新 `_config.yml` 使用 beach 皮膚

## 預覽
適合呈現輕鬆、海濱風格的內容。
```

### Forest Skin PR 描述:
```markdown
# Add Forest Skin 🌲

添加空靈清新森林浴主題皮膚,營造寧靜的森林氛圍。

## 特色
- 清新的森林綠色調 (#52b788)
- 薄霧白背景,營造空靈寧靜感 (#f7fff7)
- 適合自然、環保、靜心等主題內容

## 檔案變更
- 新增 `_sass/minimal-mistakes/skins/_forest.scss`
- 更新 `_config.yml` 使用 forest 皮膚

## 預覽
適合呈現自然、寧靜風格的內容。
```

## 驗證步驟

建立 PR 前,請確保:
1. 每個分支只包含一個皮膚檔案
2. _config.yml 正確配置對應的皮膚
3. 可以本地建置並預覽:
   ```bash
   bundle exec jekyll build
   bundle exec jekyll serve
   ```
4. 訪問 http://localhost:4000 確認皮膚正常運作

## 注意事項

- Beach 和 Forest 兩個分支應該從相同的基礎點 (commit f048a102) 分岔
- 確保兩個 PR 互不衝突
- 建議先建立 Beach PR,測試通過後再建立 Forest PR
