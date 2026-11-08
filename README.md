# Finance Wiki｜金融知識庫

**用可靠來源與實用範例，讓金融知識變得容易理解。** 此專案為國立臺北大學 AI 課程第九週作業，重點在於使用 [AGENTS.md](AGENTS.md) 指定 AI 的標準作業規則，讓未來新增文章仍維持一致內容、設計與品質。

- 目標讀者：想開始投資理財的社會大眾
- 分類：股票、ETF、基金、債券、銀行與存款、保險、風險與理財
- 第一版：七篇實用教學文章，包含公式、圖表、比較、風險提醒和來源
- 技術：Jekyll 4.4、Markdown、Liquid、共用 CSS、原生 JavaScript（無後端、無付費 AI API）
- 特色：Jekyll 自動產生首頁列表與 `search.json` 搜尋資料，文章獨立網址，手機／平板／電腦適配
- GitHub 公開網站：**部署成功後再將此處改成實際確認的網站網址；未部署前不得填虛假連結。**

## 目錄

| 路徑 | 用途 |
|---|---|
| `AGENTS.md` | AI「員工手冊」，規範任務、權限、驗收 |
| `_articles/` | Markdown 文章、Front Matter |
| `_data/categories.yml` | 分類單一資料來源 |
| `_layouts/`、`_includes/` | Jekyll 共用版型與文章卡片 |
| `index.html`、`about.md` | 首頁、關於本站 |
| `search.json` | Jekyll 自動生成的 JSON 搜尋索引 |
| `assets/` | 共用樣式、原生 JS、SVG 教學圖表 |
| `scripts/validate_site.py` | 文章格式、引用與連結規範自動檢查 |
| `docs/EXPERIMENT_LOG.md` | 先六篇，再依 AGENTS.md 新增第七篇的實驗紀錄 |
| `.github/workflows/deploy.yml` | 部署 GitHub Pages 的 Action |

## 如何在本機預覽

先安裝 Ruby、Bundler 與 Jekyll 所需套件，於專案根目錄執行：

```bash
bundle install
python -m pip install pyyaml
python scripts/validate_site.py
bundle exec jekyll serve --baseurl=""
```

在瀏覽器打開 `http://127.0.0.1:4000/`。Windows 可使用 WSL 或 GitHub Actions 建置環境。

## 新增一篇文章（可重複流程）

1. 交辦 AI：「**請先閱讀 AGENTS.md，在 ETF 類別新增一篇 ETF 配息教學，並回報測試結果，發布前先給我審核。**」
2. AI 讀取規則、現有 Markdown 與分類檔，查證來源、建立 `_articles/etf-dividends.md`。
3. 依照既有 Front Matter 填 `slug`、`category`、`description`、`tags`、`related`、`sources`、`risk_note` 等欄位。
4. Jekyll 重新建置後，自動更新首頁文章卡片和搜尋索引；按需更新內部延伸閱讀。
5. AI 執行檢查並交付檔案異動、來源、測試通過／失敗／未測與待確認事項；取得核准後才發布。

### 常見問題

- **文章沒有出現在首頁？** 檢查是否存於 `_articles/`，YAML Front Matter 是否有效、`category` 是否符合分類 ID、Jekyll 是否成功建置。
- **搜尋找不到文章？** 開啟產出的 `/search.json`，確認標題、摘要、關鍵字有寫入且 JSON 格式正確；檢查網站部署後的 `baseurl`。
- **圖片顯示失敗？** 本站站內圖片一律使用 `{{ '/assets/.../' | relative_url }}` 的 Jekyll 路徑寫法，避免子網站相對路徑錯誤。
- **表格在手機上過寬？** 網站 JS 會替文章表格增加可水平捲動的容器；仍須做實際裝置檢查。
- **網站無法部署？** 到 GitHub Actions 檢查錯誤日誌、Ruby/Jekyll 依賴、Pages 設定，並確認 Repo 的 `Settings → Pages → Build and deployment → GitHub Actions`。

## GitHub Pages 發布步驟

1. 在自己的 GitHub 帳號建立一個新的 **public** repository，建議名稱 `finance-wiki`。
2. 將**專案根目錄內**所有檔案上傳至該 repository 根目錄（包含 `.github` 隱藏資料夾）。不要多包一層 `finance-wiki/`。
3. 如果 repository 名稱不是 `finance-wiki`，請同步修改 `_config.yml` 的 `baseurl`；若 GitHub 帳號不同，同步修改 `url` 與 `README` 的作者連結。
4. GitHub 的 `Settings → Pages → Build and deployment` 選擇 `GitHub Actions`。
5. 成功部署後瀏覽 `https://<username>.github.io/<repository>/`，實測首頁、7 篇文章、搜尋與手機版。
6. 依照你在需求訪談中選擇的流程，往後修改須先經製作者確認再發布。

## 資料與風險聲明

所有內容僅供教育，不構成個人化投資建議。參考來源以證交所、金管會、中央存款保險公司、美國 SEC Investor.gov 等為主；需要區分臺灣與美國制度的差異。資料可能更新，請以主管機關、發行機構及保險契約最新正式文件為準。

## 作者與專案

國立臺北大學經濟學系 · 林姵妤。專案使用 `AGENTS.md` 讓 AI 可重複執行工作，將「一次做出網站」提升為「可持續擴充與維護的網站規範」。詳見 [實驗紀錄](docs/EXPERIMENT_LOG.md)。
