# Research protocol

## 原則
1. **不捏造**：每個 citation 必須有可解析的 DOI 或 PMID；數字、引號字串必須能在本地 parsed MD 或 abstract 找回（grep-able）。
2. **來源分級**：guideline/consensus 原文 > RCT/meta-analysis > cohort > review/expert opinion > label。標明 fulltext vs abstract-only。
3. **個案優先**：先寫本例數據與時間點（同時/非同時），再寫證據，最後寫限制與資料缺口。
4. **不補資料**：沒有 MAR、fluid、vitals、UO、weight 就寫「資料缺口」，不推定治療已做或未做。
5. **不開個人化處方**：說明 guideline 條件、閾值、需核對的院規（濃度、速率、IV access、監測）。

## Source register 欄位
實際檔名由 plan 中 evidence-librarian 的 `required_outputs` 決定（`coordination/workflow-plan.json`）。
| key | citation | DOI | PMID | 取得 | 下載/parse 結果 | locator | 用於 | 限制 |
|---|---|---|---|---|---|---|---|---|

- 取得：`fulltext` / `abstract-only` / `failed`（照實記錄失敗原因與嘗試過的工具）。
- 下載/parse：paper-search `download_with_fallback` → scihub → 使用者提供；PDF 存 `fulltext/`（ignored），LlamaParse → `parsed/`（ignored）；檢查 parse 內容確為該論文。
- locator：頁碼/表/圖/段落標題。

## Search log（檔名見 plan）
每筆：date（UTC）、tool/source、query 字串、結果數、選入/排除理由。

## 寫作
- 繁體中文為主；medical/drug names English；單位明示（mg/dL、mmol/L、mOsm/kg）。
- 估算值（corrected Na、calculated osmolality）明確標「估算」，不得當測量值。
- 2024 consensus 與 2026 ADA 不一致處並列原文與 locator，不自行調和。
- 每檔末附「限制與資料缺口」與「UNVERIFIED 清單」。

## 爭點處理
challenge（具名、附 evidence）→ response → ack 或 ruling（裁決依據）；未解決項寫入 `unresolved` 並由 synthesis-editor 保留。
