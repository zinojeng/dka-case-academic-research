# 臨床審查處理紀錄（Codex ruling disposition）

> 日期：2026-10-28｜執行：synthesis-editor（Claude Code Opus 5.5）｜依據：`coordination/briefs/clinical-review-ruling.md`（Codex 採納的 14 項修訂）
> 獨立 reviewer 以 parsed 全文核對 S02/S03/S09/S11/S16/S17/S18，**未發現捏造 citation 或算術錯誤**。原始 review 留在 ignored runtime，本檔不複製其英文原文。
> 修訂範圍：[electrolytes.md](../electrolytes.md)、[fluid-insulin.md](../fluid-insulin.md)、[clinical-summary.zh-TW.md](../clinical-summary.zh-TW.md)、[case-timeline.md](../case-timeline.md)。來源 ID 見 [source register](../../evidence/source-register.json)。

## 處理總表

| # | 嚴重度 | 審查要點 | 處理 | 修改位置 | Primary-source locator |
|---|---|---|---|---|---|
| 1 | MUST FIX | 2024 共識沒有禁止降低 insulin；固定速率加 dextrose 只是 protocol 選項；低 K 優先 | 採納 | fluid-insulin §0 第 2 點、§3.3（改寫最後一段並新增兩點）；summary §5 | S02 §4 Insulin（降至 0.05 U/kg/h 後依 glucose 約 200 調整，持續到 ketoacidosis 緩解）；S03 DKA/HHS 段（nurse-driven protocol 下限 1 unit/h） |
| 2 | MUST FIX | 三份報告統一 0.45% 措辭；區分以 D5W 矯正 tonicity 與 glucose <250 加 dextrose | 採納 | electrolytes §2.4(e)、§4 共識、§5 第 3 點；fluid-insulin §4.4 新增 (f)；summary §4、§9 | S02 §4 Fluid therapy（HHS 段 0.45% 條件；glucose <250 加 dextrose） |
| 3 | 高 | 不可說 measured 318 與 Na 122「不可能」並存；高 gap 可能來自未量測溶質；lipemia/ISE 為合理但未證實推論；TG 為次日；Chopra 中 protein 比 TG 重要 | 採納（以 Codex 裁決為準，覆蓋原 reviewer「不能並存」的寫法） | electrolytes §2.3 Chopra、§2.4(a)(2)、§2.4(b) 表、§2.4(e)、§2.5(1)(3)、§5；fluid-insulin §4.4(b) 與 Na 差距段；summary §2；timeline | S15 abstract（multivariable model）；Davidson 1992（abstract）；S11 |
| 4 | 高 | 稀疏 effective-osm 測值不能排除短時快速下降或估算下降率；無意識紀錄不能排除神經事件 | 採納 | electrolytes §2.4(d)(e)、§5；summary §2；timeline | S02 Section 5 Table 3（cerebral oedema：腦部影像低門檻） |
| 5 | 高 | 以 S02 正文為主；Fig 4 為單一 session 目視；2009（S19）為 single-session verified、未獨立再現；不可推定 2024 單位寫錯 | 採納 | electrolytes §0 表 [2]、§0.1 表頭與解讀註記、§1.3、§2.3、§3.3、§3.4、§5；fluid-insulin §2.2、§6、§8；summary §1、§3、§9 | S02 §4 Potassium、§4 Phosphate（正文寫 mmol/L）；S19 register 為 metadata-only |
| 6 | 中 | Fisher：兩組 total Ca 都下降且無差；iCa 只在可測的 13 人中分析；不能用 Ca 下降反推補磷 | 採納 | electrolytes §1.3、§1.4 第 2 點、§5；summary §1 | S09 p178 Results；Table 1–2 |
| 7 | 中 | 無 MAR → insulin 正在跑、正在補液、glucose 因 insulin 下降皆為假設，寫成「若當時使用」 | 採納 | electrolytes §2.4(a)、§3.4 第 2 點、§4、§5；fluid-insulin §0 第 4 點、§2.4、§3.2、§6、§8；summary §0、§3；timeline | case brief（MAR 缺） |
| 8 | 中 | KPD 只是鑑別；S02 該段針對特定族群；SGLT2i 相關 DKA 列的建議不能直接套用 | 採納 | fluid-insulin §7.1（加族群範圍、標為外推）；summary §6 | S02 Section 1 epidemiology 段；S02 Section 6 Table 4（SGLT2 inhibitor 列） |
| 9 | 中 | oral vs IV 門檻、更密 K 複查、選 overlap 上限屬臨床判斷／院規；確認 K <3.5 須立即依流程處理 | 採納 | electrolytes §3.4 第 2、4 點；fluid-insulin §0 第 4 點、§5.1 差異與詮釋、§6；summary §3、§5 | S02 §4 Potassium（2 h 後、之後每 4 h）；S02 §4 Transition（1–2 h）；S03（2 h／2–4 h） |
| 10 | 低 | heparin 檢體偏差方向取決於 heparin 型態與稀釋 | 採納 | electrolytes §2.5(1) | 一般檢驗醫學知識（非單一來源） |
| 11 | 中 | 最新 pH 下降但 HCO₃ 與 pCO₂ 上升，不是代謝性酸中毒惡化；檢體類型未知 | 採納 | fluid-insulin §2.4（改寫 Winter's 段）；summary §5；timeline | case brief 數值；Day1 22:39 pCO₂ 以 Henderson–Hasselbalch 推算約 30 mmHg（推算值，已標示） |
| 12 | 中 | NAGMA：需證實 NAGMA 且已達 resolution 條件，才可說不應延長 insulin；不能單憑 ketone <0.6＋Cl 高就停滴 | 採納 | fluid-insulin §4.4 NAGMA 段；summary §4 | S02 Section 3（恢復期 NAGMA 若誤認為持續 DKA 可能延誤轉 SC）；S02 §4 Criteria for resolution |
| 13 | 中 | SC transition 不以能進食為絕對條件 | 採納 | fluid-insulin §5.3 清單；summary §5 | S02 §4 Transition、Fig 5（basal-bolus 為偏好方案） |
| 14 | 中 | 改用 paraphrase 與 locator；維持去識別；不把 MAR/劑量變成事實；加五篇可點擊 DOI 與相對 Markdown 連結 | 採納 | summary §8（5 個 doi.org 連結）、頁首連結；timeline 連結；本檔連結 | S02、S03、S04、S09、S11 |

## 原始 review 中的其他建議（一併處理）
- **ADA 2026 U-300 句（漏引）**：已以意譯加入 fluid-insulin §5.1 與 summary §5（S03 住院 insulin 段，refs 78–81：住院使用 U-300 等濃縮 insulin 的資料有限、結果不一）。
- **Diabetes Care HTML 與 S02 用字差異**：fluid-insulin §2.2 已加註，比對應以語意為準，text of record 為 S02。
- **Hillier 轉折點（abstract 400 vs Results 約 440）**：electrolytes §2.3 已由 electrolyte-specialist 在先前版本記錄（register D6），本次未變更。

## 保留不變（reviewer 確認正確）
- Resolution 判定為 indeterminate（Day1 05:53 之後無 BOHB）。
- 「K <3.5 延後 insulin」為入院語境；入院 K 4.0／4.4 不需延後。
- Overlap：2024 為 1–2 h；ADA 2026 為 2 h 與 2–4 h；本輪未找到直接比較這些 overlap 時長的成人 DKA RCT，也不直接適用於 U300。
- 所有 Na／osmolality 算術、phosphate 換算、Payne 校正 Ca、Table 2 嚴重度判定。

## 未解決（需實際資料或檢驗科）
- Na 測定法（direct vs indirect ISE）、lipemia index、total protein、gas 檢體類型。
- 2024 Fig 4 與 2009 共識只有單一 session 讀取；ADA 2026 Fig 16.1 未讀。
- MAR、體重、I/O、意識狀態、當前 BOHB 與 K。

## 白話改寫紀錄（2026-10-28）
依使用者最新指示（Codex 轉達，訊息 20261028T025952162151Z-e4b69bc0），synthesis-editor 把 clinical-summary.zh-TW.md 改寫成白話、連貫的段落版本，約 2000 中文字，以五個小標對應鈣磷、鈉、鉀、輸液與 insulin，去掉事實／推論標籤、公式與密集條列。上述 14 項審查修訂的內容全部保留，只是改用自然句子表達：沒有給藥紀錄不能推論有無補充；磷單位不明、需測游離鈣；兩種鈉的測量方法未證實、三酸甘油酯是次日測、實測滲透壓差距未解；低鉀優先處理並依團隊流程調整或暫停 insulin；兩種輸液皆可但無硬終點優勢，0.45% 未建立適應症也不逕排除；缺最新血酮，血糖不能單獨作為停滴依據，緩解定義以文字說明；dextrose 支持 insulin 但速率可調、鉀安全優先；basal 需銜接、Toujeo 起效慢且證據有限；能否進食不是轉皮下注射的絕對條件。公式與詳細 locator 留在兩份專題報告，本次未改動專題報告、時間軸與 evidence。
