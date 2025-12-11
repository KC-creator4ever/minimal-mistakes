# 快速建立兩個 PR 的指令

## 現況說明
- 本地已建立 `copilot/add-forest-skin` 分支 (commit: ee8cd978)
- 遠端存在 `copilot/add-beach-skin` 分支但包含兩個皮膚

## 快速執行步驟

### 步驟 1: 推送 Forest Skin 分支
```bash
# 切換到本地的 forest 分支
git checkout copilot/add-forest-skin

# 推送到遠端
git push -u origin copilot/add-forest-skin

# 然後在 GitHub 建立 PR
```

### 步驟 2: 清理 Beach Skin 分支
```bash
# 切換到 beach 分支
git checkout copilot/add-beach-skin

# 移除 forest skin
git rm _sass/minimal-mistakes/skins/_forest.scss

# 提交
git commit -m "Remove forest skin from beach branch"

# 推送
git push origin copilot/add-beach-skin --force-with-lease

# 然後在 GitHub 建立或更新 PR
```

### 步驟 3: 在 GitHub 建立 PR

#### For Forest Skin:
- 前往: https://github.com/KC-creator4ever/minimal-mistakes/compare/master...copilot/add-forest-skin
- 點擊 "Create pull request"
- 標題: "Add Forest Skin 🌲"
- 描述請參考 PR_SETUP_GUIDE.md

#### For Beach Skin:
- 前往: https://github.com/KC-creator4ever/minimal-mistakes/compare/master...copilot/add-beach-skin  
- 點擊 "Create pull request" 
- 標題: "Add Beach Skin 🏖️"
- 描述請參考 PR_SETUP_GUIDE.md

## 分支資訊

| 分支名稱 | Commit ID | 狀態 | 包含內容 |
|---------|-----------|------|---------|
| copilot/add-forest-skin | ee8cd978 | 本地,未推送 | 僅 Forest skin |
| copilot/add-beach-skin | 13c23cc4 | 已推送 | Beach + Forest (需清理) |

## 如果無法使用命令列

由於工具限制,您可能需要手動執行以下操作:

1. **推送 Forest 分支**: 需要有寫入權限的帳號手動推送本地的 copilot/add-forest-skin 分支
2. **修改 Beach 分支**: 可以直接在 GitHub Web UI 上編輯 copilot/add-beach-skin 分支,刪除 _forest.scss 檔案

##備選方案: 重建兩個分支

如果上述步驟遇到困難,可以考慮重新建立兩個乾淨的分支:

```bash
# 刪除舊的 beach 分支 (如果需要)
git push origin --delete copilot/add-beach-skin

# 從基礎點重建 Beach 分支
git checkout -b beach-skin-only f048a102
# 添加 beach skin
# 提交並推送

# 從基礎點重建 Forest 分支  
git checkout -b forest-skin-only f048a102
# 添加 forest skin
# 提交並推送
```
