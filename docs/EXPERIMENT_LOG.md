# Finance Wiki｜AGENTS.md 重複使用實驗紀錄

## 實驗目的

驗證 AI 在已存在的網站中，是否能依照同一套 `AGENTS.md` 規則，新增一篇金融文章，並且在不重新製作首頁或複製版型的情況下，使文章能進入既有的分類與搜尋系統。

## 1. 任務指令（實際使用的工作目標）

> 先閱讀 AGENTS.md 和既有六篇文章。請新增第七篇「資產配置怎麼做？建立自己的風險管理地圖」，分類為 `planning`，遵守既有 Front Matter、繁體中文、中英術語、教學假設標示、官方來源、風險說明與相關文章連結。完成後執行格式驗證並回報測試結果；不要聲稱尚未實測的 GitHub Pages 已發布。

## 2. 前後版本（本機 Git，非 GitHub 遠端 Commit）

| 階段 | 本機 Git Commit | 實際內容 |
|---|---|---|
| 第一階段 | `8bd2d7c` | 建立 Jekyll 網站架構、`AGENTS.md`、六篇金融文章及共用 UI |
| 第二階段 | `b73a888` | 新增第七篇 `_articles/asset-allocation.md`；同步更新六篇既有文章的 `related` 欄位 |

驗證指令：`git log --oneline -3`、`git diff 8bd2d7c b73a888 --stat`。

> 注意：這兩筆是**本機 Git 歷史**，必須真正推送到 GitHub 後才能算 GitHub 遠端歷史。若只透過 GitHub 網頁上傳 ZIP 解壓檔案，Git 原始歷史不會自動保留。

## 3. 新增文章實際修改內容

1. 依照既有文章格式，新增 `asset-allocation.md`，包含 `slug`、`category: planning`、摘要、關鍵字、更新日期、相關文章、來源及風險提醒。
2. 正文以「目標與期限 → 風險承受度 → 配置與再平衡」為教學順序，包含算式、比較表與教學假設 SVG 圖表。
3. 已有六篇文章的 `related` 欄位各加入 `asset-allocation`，讓讀者能從其他主題延伸閱讀。
4. **沒有手動改首頁卡片清單或搜尋 JSON**：兩者由 Jekyll 透過 `site.articles` 資料動態產生，這是規則可重複使用的主要證據。

## 4. 已實際完成的測試

| 項目 | 結果 | 證據或限制 |
|---|---|---|
| 文章數 6 → 7 | 通過 | 第二階段新增 1 篇文章 |
| 七個金融分類各至少 1 篇 | 通過 | `scripts/validate_site.py` |
| Front Matter 欄位、分類、命名、相關文章連結 | 通過 | `python scripts/validate_site.py` |
| 來源網址格式與「教學假設」標記 | 通過（**僅檢查格式**） | 規則檢查不能代替金融專業查證 |
| JavaScript 語法檢查 | 通過 | `node --check assets/js/main.js` |
| Jekyll 真正產出網站 | **未在本機 Jekyll 執行環境驗證** | 須在 GitHub Actions 或具備 Jekyll 的電腦上建置 |
| GitHub Pages 公開網站 | **尚未驗證** | 必須上傳 GitHub、啟用 Pages 並實際開啟測試 |
| WCAG 2.2 AA 完全合規 | **尚未驗證** | 基本設計包含鍵盤焦點、圖片替代文字與跳到主內容；仍須人工/輔助工具查核 |

## 5. 結果與下一步

這次實驗呈現：在一致的 `AGENTS.md`、Markdown Front Matter 與共用版型下，AI 不必複製完整網頁，就能依照欄位與命名規則新增文章，並藉由原有的自動索引設計供首頁、搜尋與分類使用。

**重要區分：** 上述是已完成的內容與規格驗證，不代表 GitHub Pages 發布、實際瀏覽器互動或全部外部連結均已測試成功。正式發布後必須補上 GitHub Actions 執行結果、上線網址和跨裝置實測紀錄。
