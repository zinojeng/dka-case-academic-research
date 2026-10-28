# Data gaps（資料缺口）— case-analyst

> 原則：缺資料就寫缺口，**不推定治療已做或未做**；本檔不做治療建議。時間以 Day0/1/2 + 時刻表示。
> 來源：`docs/case-questions.md`（`.private/case-brief.md` 讀取被 permission settings 拒絕，見 case-timeline.md §0）。

## A. 治療紀錄（最關鍵）
| # | 缺口 | 影響的下游問題 | 備註 |
|---|---|---|---|
| A1 | **MAR**（任何藥物實際給藥紀錄） | QA1–QA5 全部 | 目前所有 insulin 資訊都只是提問 |
| A2 | IV insulin：製劑（regular vs NovoRapid/aspart）、濃度、開始時間、起始速率、調整紀錄、是否曾暫停 | QA3、QA5 | 「3 → 2 U/hr」為**提問，非 MAR** |
| A3 | Basal insulin：Toujeo（glargine U300）是否給、劑量、時點 | QA5 transition/overlap | 「約 10 U」為**提問，非 MAR** |
| A4 | Dextrose 是否加入、何時、濃度 | QA5 | glucose < 250 後處理無資料 |
| A5 | **補 K 醫囑/給藥**（途徑、濃度、速率、總量） | QA3 | K nadir 3.2（D1 15:03）、latest 3.4（D2 04:25）；不得宣稱已補或未補 |
| A6 | **補 Ca / phosphate 醫囑/給藥** | QA1 | 不得宣稱已補或未補 |
| A7 | 補 Mg 醫囑/給藥 | QA1、QA3 | |
| A8 | **Fluid 種類**（0.9% saline / balanced / 0.45%）、速率、各時段與累計總量 | QA2、QA4 | |
| A9 | Bicarbonate 是否使用 | QA4、QA5 | |
| A10 | Oral intake / diet 恢復時間（transition 前提） | QA5 | |

## B. 生命徵象與臨床狀態
| # | 缺口 | 影響 |
|---|---|---|
| B1 | **Weight**（及 height/BMI；只知「肥胖」） | QA4 fluid、QA5 weight-based insulin |
| B2 | **Vitals**（BP、HR、RR、BT、SpO2）各時點 | QA4 volume status、嚴重度 |
| B3 | **Urine output / I/O** | QA3（補 K 前提）、QA4 |
| B4 | **Mental status / GCS**、神經學變化 | QA2 cerebral edema/ODS、DKA 嚴重度分級 |
| B5 | 症狀：腹痛（後續是否出現）、肌無力、tetany/paresthesia、心悸 | QA1、QA3、pancreatitis 延伸題 |
| B6 | **ECG**（K、Ca 相關變化；QTc） | QA1、QA3 |
| B7 | IV access 類型（peripheral vs central） | QA3 K 濃度/速率院規 |
| B8 | Monitoring 等級（ICU / ward）與院內 DKA protocol 版本 | QA3–QA5 院規核對 |

## C. 檢驗缺口
| # | 缺口 | 現有資料 | 影響 |
|---|---|---|---|
| C1 | **Latest BOHB** | 最後一筆 4.2 mmol/L（D1 05:53），之後約 28 h 無 | QA5 resolution 無法判定 |
| C2 | **Latest Cr/BUN** | 只有 Day0 18:28（Cr 1.31、BUN 22） | QA3 renal function、AKI 恢復 |
| C3 | **Ionized Ca** | 無；只有 total Ca 與一筆 albumin | QA1 |
| C4 | **Phosphate 單位**與 reference range | 1.3 / 1.6 單位未列 | QA1：mg/dL（0.42/0.52 mmol/L）vs mmol/L（4.03/4.96 mg/dL）意義相反 |
| C5 | Baseline phosphate（Day0） | 無 | QA1 趨勢 |
| C6 | **ISE 方法**（chemistry 為 direct 或 indirect ISE；gas analyzer 為 direct） | 未知 | QA2 pseudohyponatremia 判讀 |
| C7 | **Arterial vs venous gas** | 未知（全部 8 筆） | pCO2/pH 判讀、respiratory compensation |
| C8 | pCO2 其餘時點 | 只有 D0 18:28、D2 04:25 | 酸鹼判讀 |
| C9 | **Cl** 其餘時點 | 只有 D1 17:31 一筆，且無同時 chemistry Na | anion gap、hyperchloremic NAGMA 判讀（QA4） |
| C10 | Plasma glucose（Day1 17:31 之後） | 只剩 POC | QA2 corrected Na、QA5 |
| C11 | Day2 04:25 同時 glucose | 無 | Day2 corrected Na 無法計算 |
| C12 | glucose 482 的出處 | **無對應 lab** | 不得使用 |
| C13 | Day0 TG（入院時） | 只有 D1 17:31 TG 1950 | QA2 lipemia/pseudohyponatremia 時序 |
| C14 | TG 已知後的 lipase 複查、影像 | lipase 57（D0）、amylase 57（D1） | pancreatitis 延伸題 |
| C15 | Measured osmolality 與 chemistry 是否同一 specimen；其他時點 osmolality | 只 D0 18:28 一筆 318 | QA2 osmolal gap |
| C16 | Albumin 其他時點 | 只 D1 08:34 3.5 | QA1 corrected Ca |
| C17 | Hemolysis / lipemia 對應哪幾筆 specimen（index 值） | 只寫「多筆 lipemia、早期 hemolysis」 | QA2、QA3 單點可信度 |
| C18 | **C-peptide、islet autoantibodies**（GAD65 等） | 無 | KPD 延伸題（需恢復後檢測） |
| C19 | Urine ketone / urinalysis、serum ketone 方法 | 無 | 背景（resolution 不以 urine ketone 判定） |
| C20 | CRP 單位 | 0.28 單位未列 | 感染評估 |
| C21 | Troponin、CK-MB 數值 | 只寫 normal | |
| C22 | Lactate 單位 | 0.60 未列 | |
| C23 | CBC 完整數值 | 只有 WBC 6.4；原始 CBC 重複 | |
| C24 | 感染評估（cultures、UA）、其他 precipitant 評估 | 只有 CXR 無 active lesion、無明確感染症狀 | precipitant 判斷 |
| C25 | Lipid 之外的家族史/藥物史細節（e.g., SGLT2i、steroid、antipsychotic 使用與否） | 只寫「無 DM drug」 | 不能推定其他藥物 |

## D. 時間解析度缺口
- D1：每筆時刻為採檢、報告或彙整時刻不明。
- D2：Day2 04:25–04:26 chemistry 與 gas 的分屬時刻不明（相差 ≤ 1 分鐘，視為同時）。
- D3：T0（Day0 18:28）與到院/insulin 開始的相對時間未知；所有「T+」只相對於第一筆 lab。
- D4：Day1 15:03 → Day2 01:00 之間無任何 glucose（約 10 h）。

## E. 交給下游的注意事項（事實層面，非建議）
- electrolyte-specialist：phosphate 單位兩種解讀都要並列；Na 有 chemistry/gas 兩套，配對表見 case-timeline.md §3；Day1 17:31 Cl 無同時 chemistry Na。
- fluid-insulin-specialist：insulin 速率、Toujeo 劑量為提問非 MAR；latest BOHB 為 Day1 05:53；latest pH 7.329 / HCO3 21.6（D2 04:25，arterial/venous 未知）；Day2 glucose 只有 POC。
- 所有角色：無 weight/vitals/UO/mental status/MAR/fluid 資料，不得推定。

## 限制
- 來源僅 `docs/case-questions.md`；與 `.private/case-brief.md` 未比對。若 case-brief 含 case-questions 未轉錄的資料，本缺口清單可能高估缺口。

## UNVERIFIED 清單
- 本檔無文獻引用；所有缺口均以 `docs/case-questions.md` 內容為準，未與 case-brief 驗證。
