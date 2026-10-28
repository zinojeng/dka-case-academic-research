# DKA 床邊判讀：教學網站

PGY / Fellow 用的單頁教學站，主軸「血糖下降後，還有哪些判斷不能省略」。純靜態 HTML/CSS/vanilla JS，部署為 Cloudflare Workers **assets-only**（沒有 Worker script）。完整說明（資料界限、部署流程、驗收清單）見 [`../docs/website.md`](../docs/website.md)。

## 指令（在 `site/` 內執行，需要 Node ≥ 22）

```bash
npm install              # 只安裝本地 devDependency wrangler@4.154.0（不做全域安裝）
npm run build            # content/clinical.json → public/；資料缺漏或不合規就失敗
npm test                 # Node 原生 test：計算機、測驗、內容契約、build 輸出
npm run preview          # http://127.0.0.1:8788/ （PORT=xxxx 或 --port 可改）
npm run deploy:dry-run   # wrangler deploy --dry-run，不會真的部署
npm run check            # build + test + dry-run
npm run deploy           # 由 Codex release 時執行（build 後 wrangler deploy）
```

`public/` 是 build 產物（已 gitignore）。每次部署前都要重新 build，才會讀到最新的 `content/clinical.json`。

## 結構

```
build.mjs              讀 JSON → 驗證 → 渲染 → 備份舊 public/ 後替換（失敗時還原）
lib/validate.mjs       clinical.json 契約、placeholder 與隱私掃描
lib/render.mjs         HTML 模板（所有內容先 escape）
src/assets/            styles.css、app.js（漸進增強）、calc.js、quiz.js、icon.svg
src/static/            _headers（CSP 等）、robots.txt、.assetsignore
scripts/serve.mjs      本機預覽（套用 _headers 的 "/*" 規則）
tests/                 *.test.mjs 與 fixtures/
content/clinical.json  臨床內容；由 clinical partner 擁有，本站程式不修改
wrangler.jsonc         name dka-teaching-rounds、assets.directory ./public、workers_dev true
```
