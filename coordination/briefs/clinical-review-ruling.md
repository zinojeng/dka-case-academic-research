# Codex 臨床審查裁決與修訂清單
獨立 Claude read-only reviewer 已核對 S02/S03/S09/S11/S16/S17/S18，沒有發現捏造 citation 或算術錯誤。原始 review 留在 ignored runtime/clinical-review-original.md。以下是 Codex 採納的修訂；請 synthesis-editor 完成 reports 中的修訂與簡短 reports/reviews/clinical-review.md disposition（繁中、不要複製原始英文長引文），完成後停止 peer loops。
1. MUST FIX fluid-insulin §3.3：2024 不是禁止減 insulin。保留 ketosis 未解需 insulin 的原則，應依 glucose、K、ketone 反應調整 insulin 並搭配 dextrose；固定速率加 dextrose 是 protocol 選項，不能寫成共識唯一規定。低 K 優先處理，不能因怕 ketosis 反彈而忽略。
2. MUST FIX 三份報告統一：現有資料未建立 0.45% saline 適應症；Na 方法、gap 與 I/O 未知，不能排除所有低張液情境。避免把用 D5W 矯正 tonicity 與 glucose<250 時加 dextrose 支持 insulin 混為一談。
3. Sodium：禁止說 measured osm318「不可能」與 true Na122 並存；高 osmolal gap 也可能來自未量測溶質，不能憑 gap 單獨判定假性低 Na。lipemia/ISE discrepancy 是合理但未證實推論，TG 是次日；不要將化學Na上升主要歸因於干擾清除當成事實。Chopra S15 abstract multivariable model 的 protein 比 TG 更重要，勿選擇性引用。
4. 稀疏 gas-based effective-osm 測值不能排除中間曾快速下降，也不能估算短時下降率。改為離散測值未顯示持續下降、無法排除短時變化；沒有意識記錄也不能排除神經事件。
5. 正文與 Fig4 不同數字：以 S02 正文為主要決策依據，圖像是單一 session 目視，尚未獨立再現。2009 S19 由一個 session 讀 XML，但 librarian 只有metadata。可寫 single-session verified / not independently reproduced，不把它當兩個獨立來源都確認。不可推定2024單位寫錯。
6. Fisher S09：兩組 total Ca 都下降、組間 total Ca 無顯著差；ionized Ca 分析僅可測的13人，補磷組較低且無tetany。不能用Ca下降反推給過磷。
7. 未提供 MAR，所以某時刻 insulin 正在跑、正在補液、glucose 因 insulin 下降均屬假設；寫成「若當時使用 infusion」。
8. KPD 只是鑑別；S02相關流行病學段落特定族群，無法直接外推此個案。SGLT2i-associatedDKA table建議不能直接套用未使用 SGLT2i 的個案，刪除不必要外推或清楚標為外推。
9. Oral vsIV K門檻、1–2h更密K抽血、選overlap上界都需標臨床判斷/院規，而非宣稱2024原文。若當前K確認<3.5，需由臨床團隊立即依低K/DKA流程決定暫停/調整insulin與監測補K，不能只沿用既有速率不處理。
10. heparinized sample偏差方向取決於heparin型態與稀釋，不能籠統說都降低Na。
11. 最新pH下降同時HCO3上升且pCO2上升，不能解讀為代謝酸中毒惡化；sampletype未知需保留。
12. Summary的NAGMA段：需證實NAGMA並已達ketone與pH/HCO3 resolution條件，才可說不應因isolatedNAGMA延長DKAinsulin；不能單用ketone<0.6+Cl高就一律停滴。
13. SC transition不是一律必須能進食：能進食可basal-bolus；未能進食須有合適basal/correction/dextrose或續IV計畫，依臨床穩定與protocol，不把能吃當絕對條件。
14. 引用用 paraphrase 與 source locators，維持現有去識別。不要把未取得的MAR/劑量變成已確認事實。加五篇可點擊DOI連結與指向兩份專題報告、source register的相對Markdown連結。
