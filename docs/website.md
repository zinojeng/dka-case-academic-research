# 教學網站（Cloudflare Workers Static Assets）

正式網址：[DKA 床邊判讀](https://dka-teaching-rounds.zinojeng.workers.dev)。首版由 Codex 部署，Cloudflare version：`2c54829d-477f-45be-9d95-fc1ed3280e6a`。

`site/` 是給 PGY / Fellow 閱讀的單頁教學站「DKA 床邊判讀」。臨床內容來自 `site/content/clinical.json`（由 clinical partner 擁有），站台程式只負責驗證與呈現，不改寫醫學內容。

## 擁有權
| 路徑 | owner |
|---|---|
| `site/content/**` | clinical partner（本站程式唯讀） |
| `site/**`（content 以外）、`docs/website.md` | site builder |
| git、PR、Cloudflare deploy | Codex |

## 架構
- **Assets-only Worker**：`wrangler.jsonc` 只有 `name`、`compatibility_date`（2026-10-28）、`workers_dev: true`、`assets.directory: ./public`、`not_found_handling: 404-page`。依 Cloudflare 文件，assets-only Worker 可以沒有 `main`。沒有 account_id、routes、bindings 或 secrets。
- **Build**：`node build.mjs` 讀 JSON → `lib/validate.mjs` 檢查 → `lib/render.mjs` 產生完整 HTML → 先寫到暫存目錄 `public.tmp-*`，再把舊 `public/` 改名為備份 `public.bak-*`，然後把暫存目錄改名為 `public/`，成功後刪除備份。驗證或渲染失敗時 exit 1，舊 `public/` 不會被動到。若替換時 rename 失敗，會把備份改回 `public/` 並清掉暫存目錄。這不是完全原子的操作：兩次 rename 之間有極短的空窗，可能讓正在讀取的本機預覽回 404。
- **No-JS 可讀**：概覽、關鍵數字、時間軸、已知/待核對、五題（含 Fellow 深讀的 `<details>`）、藥囑、I/O、測驗解析與 references 都在靜態 HTML 中。計算機的本例結果在 build 時算好。
- **漸進增強**（`src/assets/app.js`）：PGY/Fellow 切換、本頁搜尋、複製章節連結、目前章節標示、計算機、即時回饋測驗、列印前展開所有段落。動態文字一律用 `textContent`。
- **安全標頭**（`src/static/_headers`）：CSP `default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'none'; form-action 'none'; frame-ancestors 'none'`，加上 nosniff、`Referrer-Policy: no-referrer`、Permissions-Policy、`X-Robots-Tag: noindex`。頁面沒有 inline script/style，也沒有外部資源（只有 reference 連結）。
- **索引**：預設 `noindex`（meta、header 與 robots.txt）。這是個案教學站，若要公開索引，請 Codex 決定後移除這三處。

## 資料界限（build 會強制檢查）
Build 會檢查 JSON 的每個字串，並再掃一次產出 HTML 的可見文字。下列任一項出現就失敗：
- placeholder：`TODO`、`TBD`、`FIXME`、`XXX`、`lorem ipsum`、`placeholder`、`demo`、`待填`、`佔位`、`???`。
- 隱私：6 位以上連續數字（references 標題除外）、「病歷號」/`MRN`、精確年齡（例如 `42 歲`、`42M`；公開版寫 40 多歲）、本機絕對路徑、`.private`、`runtime/`、`sessions/`、`coordination/` 等內部路徑、`*.md` 檔名、workflow/manifest/mailbox 字樣。
- 完整日期：`content.updated` 仍以 `YYYY-MM-DD` 輸入，但公開頁只顯示年月，標示為「文獻查核月份」（`<time datetime="YYYY-MM">`）。其他 JSON 欄位不可寫完整日期，產出的 HTML（含屬性，外部 href 除外）也不可出現 `YYYY-MM-DD`；任何完整日期都視為可能的真實個案日期。
- 契約：五個 topic id 都要有（calcium-phosphate、sodium、potassium、fluids、insulin），不可多也不可少；quiz ≥ 5 題、answer 在範圍內、選項不重複；reference id 一律為 `S` 加 2–3 位數字（原廠產品頁等非文獻來源也一樣）；`sourceIds` 與內文的 `S02`/`[S02]` 都要對到同一份 JSON 的 references；references 必須是 https；timeline 要有 Day 0/1/2；metric status 與 medication evidence 要是規定的 enum；`io.differenceMl` 必須等於 `inputMl − urineMl`。
- 來源代號的自動檢查與人工核對：build 會自動檢查 id 格式，以及每個引用是否對到 JSON 內的 references。這些 id 是否真的存在於 `evidence/source-register.json`、內容是否一致，build **不檢查**（刻意不讓網站依賴 repo 外層的 register）。這一步由 Codex 在 release 前人工核對。
- 計算機預設體重（104.5 kg，在 `lib/render.mjs` 的 `CALC_DEFAULTS`）必須仍出現在 JSON 中，避免兩邊數字不同步。

本站不需帳號、不收集病人輸入、不呼叫 LLM、不使用 analytics。計算與測驗都在瀏覽器本機進行；localStorage 只存閱讀模式與測驗作答，沒有也能正常使用。

## Insulin 稀釋算術校驗
`src/assets/calc.js` 是純函式，瀏覽器、build 與 test 共用：
- 濃度 = U ÷ mL；U/h = mL/h × 濃度；U/kg/h = U/h ÷ kg；整袋需時 = mL ÷ mL/h；vehicle mL/day = mL/h × 24。
- 本例：50 U / 500 mL、20 / 30 mL/h、104.5 kg → 0.1 U/mL、2 / 3 U/h、0.019 / 0.029 U/kg/h、25 / 16.7 h、480 / 720 mL/day。
- 只接受一般十進位正數；0、負數、NaN、Infinity、`1e3`、`0x10`、千分位，以及超出範圍的值都會被拒絕（U 1–1000、mL 1–5000、mL/h 0.1–1000、kg 20–400）。錯誤訊息用 `aria-invalid` 與 `aria-describedby` 綁定欄位。
- 不給劑量建議、不建議調速；頁面固定提示「K 與最新 BOHB 未確認前，不能只依算術調整 dose」。濃度不在 EMA IV 配製範圍（0.05–1 U/mL）時，只提示需要核對。

## 驗證與發布（Codex）
```bash
cd site
npm install                 # 本地 wrangler 4.154.0
npm run build               # 必須在 clinical partner 完成最後修改後重跑
npm test
npm run deploy:dry-run
npm run preview             # http://127.0.0.1:8788/  給 browser QA
npm run deploy              # 正式部署（只由 Codex 執行）
```
`npm run preview` 只綁 127.0.0.1，並套用 `_headers` 的 `/*` 規則，CSP 行為接近正式環境。也可以用 `npx wrangler dev`（workerd 本機模擬）。

Browser QA 建議檢查：
- 手機寬度（360px）沒有水平捲動，表格會堆疊成卡片。
- PGY/Fellow 切換會收合或展開所有深讀段落，重新整理後保留。
- 測驗可以只用鍵盤作答（Tab 與方向鍵），每題回饋包含正確答案、解析與來源；重設後全部清空。
- 計算機輸入 0、-1、abc、9999999 都顯示對應欄位的錯誤，且不顯示結果。
- 搜尋「phosphate」或「K」會列出結果，點擊後跳到該段並展開收合內容。
- 複製連結可用；列印預覽會展開深讀段落與測驗解析，並隱藏互動元件。
- 關閉 JS 後主要內容仍可閱讀；console 沒有 CSP 錯誤。
