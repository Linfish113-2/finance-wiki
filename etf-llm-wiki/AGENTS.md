# AGENTS.md — ETF 投資入門 LLM Wiki 工作手冊

> 本規格經過 10 題需求訪談後確認；本專案未使用真實交易帳號或機密文件。

## 1. 任務及讀者

- 任務：依知識庫生成讓零金融背景大眾理解 ETF 的繁體中文教學 HTML 簡報。
- 必交：至少 5 篇 ingest、Wiki、可瀏覽的 HTML、Graph / Loop 說明、實際執行紀錄與反思。
- 內容範圍：ETF 定義、主動與被動、種類、個股比較、NAV 與市價、配息、費用、風險與選擇檢查表。
- 簡報：預計 10 頁，允許 8–15 頁，手機／電腦有清晰字體；不得指定個人買賣標的。

## 2. 來源邊界

1. 只採用 `sources.md` 和 `raw/S*.md` 記錄且已確認的公開可信資料；不得自行補造 ETF 商品數字、獲利或報酬。
2. 已 ingest 的 `raw/` 是**來源閱讀後獨立整理的摘要**，不是侵犯著作權的網站全文副本。原始網站以 URL 可查。
3. 每一重要事實須有 `cards/evidence.json` 內的 E 編號，並指向一個以上 S 編號。
4. 配息除息、折溢價的數字都是**明確標示為假設**的教學算例，不是即時市場行情。
5. 最新法令、稅費與產品規定可能變動，必須提醒查閱現行公開說明書和官方公告。
6. 注意**主動式 ETF**：不應把每檔 ETF 都定義為被動追蹤指數。
7. 不得把配息直接寫成獲利，更不能宣稱 ETF 保本。

## 3. 節點、輸入與輸出

| 節點 | 只能讀 | 產物 | 檢查及可退回 |
|---|---|---|---|
| A 資料蒐集 | 官網資料 | URL / metadata | 找不到來源即停；補來源再做 |
| B Ingest | A | `raw/`, `sources.md` | 來源編號唯一、至少 5 篇 |
| C Wiki / 證據卡 | B | `wiki/topics`, `cards/evidence.json` | 所有重要事實有 S 編號；不通過回 B |
| D 大綱及逐頁稿 | C | `data/slides.json` | 執行 `scripts/validate_draft.py`；不通過回 D 或 C |
| E HTML 渲染 | D | `slides/`, `wiki/index.html` | 不允許渲染時更改投資事實 |
| F 程式驗收 | E + C | `reports/` | 靜態 lint／JS 測試，失敗回對應節點 |
| G 人工審查 | 所有通過之文件 | 人工審查紀錄 | 超出 3 輪或資料不足停止 |

## 4. Loop 限制

- 每個缺陷最多局部修正 3 輪；其他未受影響的節點不得整份重做。
- 完成條件：資料數、來源對應、關鍵定義、頁數、連結、鍵盤／按鈕、互動測驗與報告均達標。
- 停止條件：來源不足、無法確認重要資訊、3 輪後仍失敗、工具或政策阻擋驗證。留下真實問題紀錄，不說謊報通過。
- 審查內容應在獨立上下文比對成品與來源（若無此條件，標註尚待人工內容審查）。

## 5. 可重現操作

```bash
python scripts/build_content.py
python scripts/validate_draft.py
python scripts/render_site.py
python -m pytest tests/test_project.py -q
node --check slides/script.js
node tests/js_unit_test.cjs
# 選做：電腦可啟動瀏覽器時再執行
python tests/browser_check.py
```

- 不准虛構執行過的檢查。`reports/` 只能填寫真實執行資訊。
- 若需變更來源、圖文、流程，先修改資料／證據，再重產並檢查；保留 Git commit。
