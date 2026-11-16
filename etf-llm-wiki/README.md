# ETF 投資入門 LLM Wiki 與教學 HTML 簡報

**對象**：完全沒有金融基礎的一般社會大眾  
**語言**：繁體中文  
**資料**：7 份官方／可信來源的獨立摘要，7 篇 Wiki 主題，20 張 Evidence Cards，10 頁 HTML 教學簡報。  
**更新／查核日**：2026-11-16  
**提醒**：非投資建議，資訊以原始官網最新公告為準。

## 看成品（不需安裝程式）

1. 解壓縮 ZIP。
2. 開啟專案的 **`index.html`**。按「進入教學簡報」或「瀏覽 LLM Wiki」。
3. 或直接開啟 `slides/index.html`（鍵盤左右鍵換頁）與 `wiki/index.html`（可搜尋）。
4. 簡報第 7 頁有配息觀念解釋開關、第 10 頁有三題測驗。

> 若本機瀏覽器限制 `file://`，可在專案資料夾輸入 `python -m http.server 8000`，再開啟 http://localhost:8000/；此網址僅是你自己電腦的本機網址，不是 GitHub 公開網址。

## 來源與證據的完整鏈結

- `sources.md`：來源名稱、官方網址、閱讀段落、日期與摘要。
- `raw/S*.md`：7 份 ingested source notes（**獨立整理**，不擅自全文轉載）。
- `data/sources.json`：機器可讀來源註冊表。
- `cards/evidence.json`：20 張 E 事實卡，逐張關聯 S 出處。
- `wiki/topics/*.md`：7 個主題文章，附 E/S 對應。
- `data/slides.json`：逐頁內容與 E 依據，HTML 頁面會顯示 S 來源。

## 重建專案、重跑驗證

```bash
python scripts/build_content.py
python scripts/validate_draft.py
python scripts/render_site.py
python -m pytest tests/test_project.py -q
node --check slides/script.js
node --check assets/wiki.js
node tests/js_unit_test.cjs
```

瀏覽器測試另見 `tests/browser_check.py`；如瀏覽器政策阻擋，不得將其報作成功。`reports/report.md`（或根目錄 `report.md`）記錄實際測試結果與反思。

## GitHub Pages 發布（待確認站點可公開）

若採用 GitHub Pages，將專案資料上傳到 GitHub 的可發布目錄，並在 Repository → Settings → Pages 確認從正確的分支／資料夾部署。取得可開啟的網址後才能交老師。若已有 Jekyll 網站，請保留 `slides/`、`wiki/` 和 `assets/` 路徑的相對關係，避免把它們移散。

## 課程要求映射

| 項目 | 實作位置 |
|---|---|
| LLM Wiki 主題與說明 | 本 README、`wiki/index.md` |
| 至少 ingest 5 篇 | `raw/` 7 份、`reports/ingest-log.json` |
| Wiki 連結／成果 | `wiki/index.html`（靜態成果） |
| HTML 簡報 | `slides/index.html` |
| Loop / Graph | `workflow.md`、`AGENTS.md` |
| 真實執行結果 | `reports/`、`report.md` |
| 反思 | `report.md` |

專案內所有自編教學文字與程式碼為本次產出；第三方來源權利歸原網站所有，這裡不完整轉載。
