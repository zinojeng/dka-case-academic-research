# Cloudflare 教學網站 builder
使用者明確要求 website by Cloudflare 方便fellow或PGY閱讀學習；Codex統籌、Claude Opus5.5實作。Read reports/clinical-summary.zh-TW.md、docs/case-questions.md、coordination/briefs/clinical-web-update.md。臨床內容由另一session寫site/content/clinical.json（優先JSON，不改這檔）。你own site/** except site/content/**，另 docs/website.md。舊reports/evidence/scripts/.claude/git不要動。不可deploy/push，Codex做release。
建立可直接Cloudflare Workers Static Assets部署的精緻單頁教學站（HTML/CSS/vanilla JS, 少依賴）。現行官方docs確認assets-only可wrangler.jsonc只有assets.directory不需main；wrangler4.154.0，compatibility_date 2026-10-28。site/package.json devDependency pinwrangler4.154.0；site/wrangler.jsonc name dka-teaching-rounds, assets.directory ./public，workers_dev true。不要accountid/secrets。
設計：適合醫療教學的沉穩navy/teal/cream、中文字體系統、18px可讀字、長文窄欄與清楚留白，手機友善；不要巨型空hero/花俏gradient或一屏十個card。標題DKA床邊判讀，主軸「血糖下降後，還有哪些判斷不能省略」。頁首有PGY重點/Fellow深讀切換，五題章節導航、Day0–2timeline、已知/待核對重點、相關藥囑辨識、I/O部分紀錄說明、references。
互動：
- 5題以上單選quiz即時feedback/explanation/source，不只勾對錯；可reset，可access keyboard。
- 純算術insulin稀釋校驗：50U、500mL、20/30mL/h、104.5kg輸入，輸出0.1U/mL、2/3U/h、0.019/0.029U/kg/h。不是劑量建議，不自動建議調高，顯示K與BOHB未確認不能只照算術調dose。拒絕zero/negative/NaN及unrealisticoverflow，清楚單位與可及錯誤。
- search/章節錨點導航或copy-section-link；print適用、progress localStorage非必要可簡單用。
- 不需帳號、不收patientinput、不呼叫LLM、不用外部analytics，所有calculator在browser本機。
- 已知MRN/真實case日期/本機paths/內部workflowtrace不能進public/。Age用40多歲，不要rawcasefilename。Reference查核日期可以2026-10-28但不是case日期。
內容整合：Node site/build.mjs讀clinical.json並渲染主要教學文字到HTML（即使JS關閉仍能讀）。ClientJS只enhance toggles/calculator/quiz/search，建議以textContent渲染輸入以免XSS。不要將Markdown中的private/internaltrace直接複製public。可等待clinical.json或先用暫時demo資料，但最終不得帶placeholder，缺data要buildfail不是假成功。
驗證：Node原生test計算/quiz/contentshape（有意義非鏡像），build與wrangler deploy --dry-run（不要真正deploy）、本機preview建議Node或pythonserver。告訴Codexport/commands。輸出site/README.md、docs/website.md含build/deploy步驟、資料界限，不要全域npm安裝與修改別repo。留給Codex browserQA。
有需要可用boundedsubagents（同owner約束）。任務完成回報檔案、測試、待處理，不讀私密key/外部auth，不部署。
