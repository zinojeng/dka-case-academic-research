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
| 11 | 中 | 最新 pH 下降但 HCO₃ 與 pCO₂ 上升，不是代謝性酸中毒惡化；檢體類型未知 | 採納 | fluid-insulin §2.4（改寫 Winter's 段）；summary §5；timeline | case brief 數值；Day1 22:39 pCO₂ 實測 28.4 mmHg（Codex 原始紀錄核對；原推算約 30 的敘述已於 final QA 移除） |
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

## Supplement v2 更動紀錄（2026-10-28）
執行：clinical-update（Claude Code Opus 5.5；Codex 授權本輪為 reports/ 醫學內容、`site/content/clinical.json`、`docs/case-questions.md` 的唯一內容 owner）。依據：使用者新增的去識別 supplement v2（體重、vitals、部分 I/O、單位、醫囑）與 Codex precision notes。歷史 mailbox 未修改。

| # | 臨床必修項 | 舊敘述 | 新敘述 | 修改位置 | Locator |
|---|---|---|---|---|---|
| V1 | Phosphate 單位 | 單位未列，mg/dL 為假設 | 已確認 mg/dL：1.3 → 1.6 = 0.42 → 0.52 mmol/L，中度低磷；是否補磷依肌力／呼吸／心臟評估 | electrolytes §S、§1.1、§1.2、§1.4(3)、§1.5、§5；summary §一；timeline；docs/case-questions；clinical.json | S02 §4 Phosphate（<1.0 mmol/L 且有症狀） |
| V2 | 補充醫囑 | 無補 K/Ca/P 醫囑 | 有 CaCl₂ 400 mg/20 mL × 2 STAT IV、KCl in NS 20 mEq/500 mL STAT drip、K-gluconate 20 mEq QID＋STAT。Order ≠ 已給；CaCl₂ 800 mg 為製劑量，不等於元素鈣 800 mg（元素鈣含量待商品仿單確認）；QID 80＋STAT 20＋IV 20 不能無 MAR 稱 120 mEq/day；片段中未見含磷製劑（不代表完整醫囑沒有） | electrolytes §S、§1.2、§1.4(2)(4)(5)、§3.2、§3.4(4)、§3.5、§5；fluid-insulin §6；summary §一、§三；timeline 醫囑段 | S02 §4 Potassium；S09（補磷與 iCa） |
| V3 | 體重與 insulin 算術 | weight 未知，以隱含體重示意 | 104.5 kg；50 U/500 mL = 0.1 U/mL；20–30 mL/h = 2–3 U/h；目前 2 U/h = 0.019 U/kg/h（3 U/h = 0.029）；低於 0.05 U/kg/h 參考（5.225 U/h）不直接建議上調，K 3.4 與最新 BOHB 為限制；vehicle 480–720 mL/day 納入總輸液 | fluid-insulin §S、§0(3)(9)、§3.3、§4.4、§5.2(3)、§5.3；summary §四、§五 | S02 §4 Insulin；S03 DKA/HHS 段（nurse protocol ≥1 U/h） |
| V4 | NovoRapid 產品與穩定性 | 只泛論 aspart IV 條件 | 醫囑顯示 FlexPen；SmPC IV 用 vial，需核對實際製劑與藥局配製，不由顯示名稱判錯誤；0.05–1.0 U/mL、指定輸液與 polypropylene 袋、室溫 24 h、起始吸附；500 mL 以 20 mL/h 需 25 h → 核對 hang time，不宣告超時 | fluid-insulin §0(8)、§10.1；summary §五；clinical.json insulin | S18 §4.2 Intravenous use、各 pen 段（本機 pdftotext 核對 EMA PDF，未上傳） |
| V5 | I/O 與 vitals | 無 vitals、無 I/O、無進食 | 條件式片段：液體 2946（IV 2386＋口服 560）、尿 2050、差 +896 mL；不稱 24 h、不算 mL/kg/h、固體不計入；IV 1000 mL 是輸入容量非 mL/h；RI 177／IV 209 不換算 U、不逕對應 insulin 袋；最新 BP 149/86、HR 85、RR 18；有進食 | timeline（vitals、I/O 表）；fluid-insulin §S、§4.4；summary §四；clinical.json io | — |
| V6 | 血酮分析物 | 直接稱 BOHB | 檢驗名稱與參考 0–0.6 mmol/L 支持很可能為 BOHB，但分析物待檢驗科確認；最後一筆仍為 Day1 05:53 的 4.2 | timeline；fluid-insulin §S；summary §五；clinical.json | S02 §3（建議以 BOHB 監測） |
| V7 | 醫囑時間 | — | 醫囑未附開立時間，不放進任何特定 Day | timeline「醫囑（無時間）」；clinical.json timeline | Codex precision note |
| V8 | 英文原句 | 部分段落引用 label／共識英文原句 | 改為繁中意譯並保留 locator（S02 §4 Transition；S17 §5.2/§12.2） | fluid-insulin §5.1、§5.2 | S02、S17 |

### 維持不變
DKA resolution 判定（indeterminate，缺最新 BOHB）；Na／pseudohyponatremia 為合理但未證實的推論與所有 Na／osmolality 算術；K <3.5 的入院語境與治療中優先補 K、由團隊依流程調整 insulin；0.45% saline 未建立適應症但不逕排除；overlap 1–2 h vs 2 h／2–4 h；Toujeo U300 onset／steady state 與「無轉換研究」限制；KPD 與 pancreatitis 延伸。未新增文獻，也未引用 register 以外的研究。

### 公開網站內容界限
`site/content/clinical.json`：年齡寫 40 多歲；不含病歷號、真實個案日期、醫師、機構、地點、本機路徑或 workflow 紀錄；`updated` 為文獻查核日期，公開 HTML 僅顯示年月。慢性藥只以類別列出與 DKA 判讀相關者（β-blocker、含 ARB 複方、fibrate）。References 7 筆（S02、S03、S09、S11、S17、S18、S20），所有 topic／quiz 的 sourceIds 與 evidence register 均可對應。S20 為原廠藥品成分來源，公開此文獻連結不代表個案所在機構或地點。

### 仍未解決
完整 MAR（insulin 起訖與 hang time、K／Ca 實際給量、dextrose）、最新 BOHB 與分析物確認、最新 Cr、ionized Ca、ECG、意識狀態、Na ISE 方法與 lipemia index、gas 檢體類型、insulin 實際製劑／vehicle／袋材、I/O 是否完整與各筆區間。

### Codex v2 QA 修正（2026-10-28，完成前）
- **Q1 元素鈣範圍移除**：所有白話、公開與報告內容刪除未經商品仿單驗證的 218–289 mg 化學計量換算；只保留「醫囑標示 800 mg calcium chloride 製劑 ≠ 800 mg 元素鈣，實際水合物與元素鈣含量須由商品仿單確認」。位置：clinical.json（calcium-phosphate body/fellow、medications）、summary §一、electrolytes §S、§1.4(5)、§5、本檔 V2。
- **Q2 Na 差距段弱化**：chem−gas Na 差距縮小不能主要歸因於 glucose 或干擾減少；沒有同時段 ISE 方法與 TG，也可能是實際水與鈉平衡變化；單憑 chem Na 上升不能診斷（也不能排除）rapid correction。位置：clinical.json sodium body/fellow、summary §二、electrolytes §2.4(e)、fluid-insulin §4.4、timeline 判讀重點。
- **Q3 K-Glu 成分**：Codex 以原廠產品頁獨立核對（每 15 mL 含 K⁺ 20 mEq，potassium gluconate）：https://www.sintong.com.tw/tw/products_view/216 。clinical.json 與 evidence/source-register.json 均登錄 S20，potassium topic sourceIds 加入 S20；網站 references 共 7 筆。Summary 與 electrolytes §S 加註。原臨床更新 session 未自行開啟該網頁，來源由 Codex 驗證並登錄。
- I/O 條件式與來源未知事項維持不變。

### Final medical QA 小修（2026-10-28）
1. Day1 01:58：pH 7.385 已符合 2024 OR 規則的 pH 條件；改寫為「acid–base 條件成立，但 HCO₃ 13.4 且無同時血酮，不能判定 resolution」（clinical.json timeline；fluid-insulin §2.4）。
2. clinical.json insulin takeaway 與 quiz 選項改用「血酮」，不預設分析物已確認為 BOHB。
3. clinical.json 公開內文：NovoRapid 室溫 24 h 穩定性明示以指定輸液、0.05–1.0 U/mL 濃度與 polypropylene 袋為前提（insulin body 與 hang-time quiz）。
4. Day1 22:39 pCO₂：Codex 依原始紀錄核對為 28.4 mmHg（去識別 brief 原未列；本 session 未讀原始病歷）。移除所有「pCO₂ 未列／推算約 30」敘述，改引 28.4 → 40.7（clinical.json insulin fellow；timeline；fluid-insulin §2.4；case-analyst/case-timeline Day1 22:39 列；docs/case-questions；本檔 #11）。其他時點的「pCO2 未列」為 brief 實況，未改。
5. 公開內容的「目前／現在」改為「該次紀錄」「Day2 紀錄」「現有資料」，避免進行中個案的語氣，臨床意義不變。
