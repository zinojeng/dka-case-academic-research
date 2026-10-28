# Data gaps（資料缺口）— case-analyst 工作檔（當前狀態）

> 原則：缺資料就寫缺口，**不推定治療已做或未做**；醫囑不等於已給；本檔不做治療建議。時間以 Day0/1/2 + 時刻表示。
> 來源：去識別 case brief（含 Day1 22:39 pCO₂ 28.4 addendum）與使用者 supplement v2；依 supplement v2 更新。啟動時讀取權限問題的歷史見 [input-validation.md](input-validation.md)；原 bootstrap 版本保留在 Git 歷史。事實與算術見 [case-timeline.md](case-timeline.md)。

## A. 已補充（不再列為完全未知）
| 項目 | 目前狀態 | 仍需注意 |
|---|---|---|
| 體重 | 175 cm、104.5 kg、BMI 34.1（Day1 17:00） | 肥胖時用哪一種體重算劑量，共識未規範 |
| Vitals | Day1 17:00–Day2 09:01 BP/HR/RR/T 九筆；最新 149/86、85、18、35.7 | 無 SpO₂；不能據此判定意識狀態或 resolution |
| 進食 | Day1 18:00 乾飯、Day2 07:24 稀飯（單位未列） | 實際攝取量與碳水化合物量未知 |
| 尿量／I/O | 片段：液體 2946、尿 2050、差 +896 mL（條件式） | 非完整 24 h；需確認獨立區間；不換算 mL/kg/h |
| 電解質單位 | Na/K/Cl = mEq/L；Ca/P = mg/dL（使用者確認） | P 1.3 → 1.6 mg/dL = 0.42 → 0.52 mmol/L |
| IV insulin | 使用者確認 50 U／500 mL（0.1 U/mL）、曾 20–30 mL/h、該次紀錄當下 2 U/h | 實際產品（醫囑顯示 NovoRapid FlexPen）、藥局配製、vehicle、袋材、起訖與 hang time 待核對 |
| K 醫囑 | KCl in NS 20 mEq/500 mL ST；K-Glu 20 mEq/15 mL QID＋ST | 無 MAR，不能加總為已給 120 mEq/day |
| Ca 醫囑 | Calcium Chloride 400 mg/20 mL 2 amp ST IV | 800 mg 是製劑量，不是元素鈣；是否已給待 MAR |
| 輸液醫囑 | LR 500 mL × 4 QD、NS 500 mL QD、NS 500 mL ST | 實際給量、速率與起訖待 MAR；insulin vehicle 480–720 mL/day 需一併考慮 |
| pCO₂ | Day0 20.3、Day1 22:39 28.4、Day2 04:25 40.7 | 其他時點未列；檢體類型未知 |

## B. 治療紀錄仍缺
| # | 缺口 | 影響 |
|---|---|---|
| B1 | **完整 MAR**（所有醫囑的實際給藥時間與量；醫囑本身也無開立時間） | QA1–QA5 全部 |
| B2 | Insulin 實際產品（vial 或 pen）、配製方式、vehicle 液體與袋材、掛上與換袋時間、速率調整與是否曾暫停 | QA3、QA5 |
| B3 | Basal insulin：Toujeo（glargine U300）是否給、劑量、時點——「約 10 U」仍只是**提問** | QA5 transition |
| B4 | Dextrose 是否給、濃度、時間（貼出片段未見） | QA5 |
| B5 | K 實際給量（KCl drip、K-Glu 各次是否服用） | QA3 |
| B6 | CaCl₂ 是否已給、時間與開立理由；phosphate、Mg 是否有其他醫囑（片段未見） | QA1 |
| B7 | Bicarbonate 是否使用 | QA4、QA5 |

## C. 臨床狀態仍缺
| # | 缺口 | 影響 |
|---|---|---|
| C1 | **Mental status / GCS**、神經學變化 | QA2 cerebral edema/ODS、嚴重度 |
| C2 | 症狀：腹痛、肌無力、呼吸肌力、tetany/paresthesia、心悸（Day1 21:01 一次 RR 30 的情境） | QA1 補磷條件、QA3、pancreatitis |
| C3 | **ECG**（K、Ca 相關變化；QTc） | QA1、QA3 |
| C4 | IV access 類型（peripheral vs central） | QA3 K 濃度/速率、CaCl₂ 給法 |
| C5 | Monitoring 等級與院內 DKA protocol 版本 | QA3–QA5 院規核對 |
| C6 | 完整 I/O（起訖、是否累計、其他輸出、insensible loss）、SpO₂ | QA4 |

## D. 檢驗仍缺
| # | 缺口 | 現有資料 | 影響 |
|---|---|---|---|
| D1 | **最新血酮**與分析物確認 | 最後一筆 4.2（Day1 05:53）；檢驗名稱與參考值支持很可能是 BOHB，但未確認 | QA5 resolution 無法判定 |
| D2 | **最新 Cr/BUN** | 只有 Day0（Cr 1.31、BUN 22） | QA3 renal、AKI 恢復 |
| D3 | **Ionized Ca**（含採檢 pH） | 只有 total Ca 與一筆 albumin | QA1 |
| D4 | Baseline phosphate（Day0） | 無 | QA1 趨勢 |
| D5 | **ISE 方法**（chemistry direct/indirect；gas analyzer）、lipemia/hemolysis index 對應 specimen | 未知 | QA2 pseudohyponatremia、QA3 單點可信度 |
| D6 | **Arterial vs venous gas** | 全部未知 | pH/pCO₂ 判讀 |
| D7 | 其他時點 pCO₂ | 只有三筆（見 A） | 酸鹼判讀 |
| D8 | **Cl** 與同時 chemistry Na/HCO₃ | 只有 Day1 17:31 Cl 102，無同時 chemistry Na | NAGMA 判讀（QA4） |
| D9 | Day1 15:03 後 plasma glucose；Day2 04:25 同時 glucose | 只有 POC | QA2 corrected Na |
| D10 | Day0 TG | 只有 Day1 17:31 TG 1950 | QA2 lipemia 時序 |
| D11 | TG 已知後 lipase 複查、影像 | lipase 57（Day0）、amylase 57 | pancreatitis 延伸題 |
| D12 | 其他時點 measured osmolality；是否同一 specimen | 只有 Day0 318 | QA2 osmolal gap |
| D13 | 其他時點 albumin | 只有 Day1 08:34 3.5 | QA1 |
| D14 | **C-peptide、islet autoantibodies** | 無 | KPD（恢復後檢測） |
| D15 | Cultures 等感染性 precipitant 評估 | 只有 CXR 無 active lesion、無明確感染症狀 | precipitant |
| D16 | CRP 單位、troponin/CK-MB 數值、lactate 單位、完整 CBC | 只有部分數值或 normal | 背景 |
| D17 | glucose 482 的出處 | **無對應 lab** | 不得使用 |
| D18 | **誘因相關用藥史**（SGLT2 inhibitor、steroid、antipsychotic 等） | 只知「無 DM drug」與部分長期口服醫囑；其他用藥史未完整確認 | 不能從「無 DM drug」推論這些誘因用藥皆已排除 |
| D19 | **血酮檢測方法**（lab 或 POC、儀器／方法）與 **urine ketone／urinalysis** | 只有檢驗名稱與參考 0–0.6 mmol/L；方法與尿液檢查未提供 | 方法未知與分析物未確認是兩件事，需分別向檢驗科確認；resolution 不以 urine ketone 判定 |

## E. 時間解析度
- 每筆時刻為採檢、報告或彙整時刻不明；醫囑沒有開立時間。
- Day2 04:25–04:26 chemistry 與 gas 視為同時（相差 ≤ 1 分鐘）。
- T0（Day0 18:28）與到院、insulin 開始的相對時間未知。
- Day1 15:03 → Day2 01:00 之間無 plasma 或 POC glucose（約 10 h）。

## F. 給續讀 session 的注意事項（事實層面，非建議）
- 不要再寫「完全沒有體重、vitals、進食、尿量、醫囑」或「phosphate 單位未知」；改用 A 表的已知狀態與 B–D 表的仍缺項目。
- 醫囑 ≠ 已給；不可把 QID＋ST＋IV K 加總為已給 120 mEq/day；CaCl₂ 800 mg ≠ 800 mg 元素鈣。
- Day0 血酮 5.6 不是最新值；最後一筆是 Day1 05:53 的 4.2。
- 低於 0.05 U/kg/h 參考的 insulin 速率不等於應增速；K 3.4 與最新血酮是限制。
- I/O 只用條件式片段差 +896 mL；IV 1000 是容量；RI 177／IV 209 不是 insulin 單位。
