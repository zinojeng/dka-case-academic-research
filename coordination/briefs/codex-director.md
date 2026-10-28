# Codex director brief — 2026-10-28
使用者授權 Codex 統籌、Claude Code Opus 5.5 執行多個獨立可續接 cross sessions，依需求建立 subagents。以個案為核心 academic deep research；繁體中文為主，medical/drug names English；實際完成五大QA與文獻研究、全文下載/LlamaParse PDF→MD、workflow、private GitHub repo PR merge main。只有 Codex 處理 git release。
## 規則
- 原始根目錄數字開頭病歷 MD read-only / gitignored。只讀 .private/case-brief.md。可追蹤內容去識別：用 Day0/1/2，不能記載病歷號、真實入院日期、醫師、居住工作地、本機絕對路徑。
- .private/mcp.local.json 有 research_hub,paper-search,scihub,llamaparse,codebase-memory-mcp。key 只存在 key file，絕不讀出或印出。只有已發表 literature PDF 能送 LlamaParse，病歷不能上傳。
- 真正 native claude --bg --model claude-opus-5-5，每個session有own output path，可由 claude agents --cwd "$PWD" 看見。依賴順序bootstrap→evidence及clinical→synthesis→independent review。不必為純報告各自開git worktree；用各自cwd與owner檔。可依需要使用subagents。
- 可用 file mailbox：coordination/messages/*.json 原子訊息，有 from/to/topic/evidence/status/reply_to，透過resume處理。不能宣稱 file polling 是 native realtime messaging。重要爭點需具名 challenge/response/ACK，記錄裁決依據和未解決項。
- 檔案存在不代表session成功；需native status及explicit completion manifest/human gate。session registry/實際logs放ignored runtime，不得track本機cwd或PHI。
- 2024共識DOI10.2337/dci24-0032、2026 ADA ch16 DOI10.2337/dc26-s016，需查當前literature。記錄query/date/DOI/PMID/fulltext vs abstract/download及parse真正結果、locator與限制，禁止捏造citation。
## 必須回答
1. Calcium/Phosphate：Ca7.8,albumin3.5；phosphate1.3→1.6未列單位，明示mg/dL假設與mmol/L換算。沒有MAR不能宣稱已補或沒補。ionizedCa、症狀、RCT與補磷引起hypocalcemia。
2. Sodium：同時chemistryNa122 vs gasNa131、glucose411（QA482無對應lab）、TG1950。indirectISE pseudohyponatremia與hyperglycemic translocational hyponatremia分開。correctedNa=Na+1.6*(glucose-100)/100，2.4敏感度，不能用glucose-180。Measuredosmolality318 BUN22，釐清osmolgap與method、same-time限制，不可將correctedNa當測量真值。cerebral edema vs osmotic demyelination。
3. Potassium：nadir3.2 latest3.4；2024 K<3.5先補K並延後/暫停insulin until>3.5，核對原文。ECG、renal、urineoutput、IV access rate/concentration院規；oral並非永遠禁用，勿無資料開個人化處方。
4. fluids：0.9%saline vs balanced/Ringer lactate證據、0.45%情境、hyperchloremicNAGMA；缺I/O weight vitals renal/heart不判實際量。比較trial硬終點限制。
5. insulin：glucose211–234不能單獨停滴；latestketone4.2是較早Day1，latestpH7.329/HCO3 21.6，無latestBOHB不能宣稱resolved。2024 BOHB<0.6 AND(pH>=7.3 OR HCO3>=18)，glucose ideally<200；不用BE/aniongap/urineketone判resolution。<250加dextrose續insulin tillketosis解；依體重情境而非固定2–3U/hr。2024overlap1–2h vs2026 2–4h需說清楚；ToujeoU300 onset/steady-state核對label不能直接套常規overlap。NovoRapidaspart IV核對label與濃度，不自動當regular。
延伸：HbA1c13.6代表chronic；肥胖DKA首發可考慮KPD需恢復後C-peptide/autoantibodies，不逕診。TG1950 pancreatitis風險，lipase57無腹痛不支持已發生但不能絕對排除。
