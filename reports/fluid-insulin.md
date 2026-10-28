# QA4 Fluids／QA5 Insulin stop 與 SC basal transition — fluid-insulin-specialist 報告

> Owner：fluid-insulin-specialist（DKA fluid insulin Opus55）｜研究日期：2026-10-28｜資料來源：只讀 `.private/case-brief.md`（去識別，Day0/1/2）
> 用途：學術討論與會診思路整理，**不是個人化醫囑**。缺 weight、vitals、I/O、urine output、mental status、MAR、最新 Cr/BOHB，以下所有劑量皆為「原則與條件」，不可直接轉成 order。

---

## 0. 一頁結論（Bottom line）

1. **目前不能宣告 DKA resolved。** 2024 consensus 的 resolution 定義是 **plasma ketone (β-hydroxybutyrate, BOHB) <0.6 mmol/L 且（venous pH ≥7.3 或 HCO3⁻ ≥18 mmol/L）**，理想上 glucose <200 mg/dL。本案最新 gas（Day2 04:25）pH 7.329、HCO3⁻ 21.6 雖已滿足 acid–base 部分，但**最後一筆 BOHB 是 Day1 05:53 的 4.2 mmol/L**，之後無 ketone 資料；Day2 glucose 211–234 mg/dL 也未達 <200 的理想值。→ **先抽 BOHB（及同時段 chemistry Na/Cl/HCO3⁻、K、Cr）再判斷。**
2. **Glucose 211–234 不是停 IV insulin 的理由。** 2024 consensus（S02 §4 Insulin）：glucose <250 mg/dL 時加 5–10% dextrose、insulin 降至 0.05 U/kg/h，之後**依 glucose（目標約 200 mg/dL）調整 insulin**，並持續到 ketoacidosis 緩解。前提是 K 安全（§6）。
3. **Weight 未知 → 不給固定速率建議。** 「3→2 U/h」在 0.05 U/kg/h 的換算下，只相當於 60 kg→40 kg 的人。這只是說明性算術（§3.3），**不代表劑量偏低或不足**；目前劑量是否足夠，要看 K、ketone、glucose 的反應，而 weight 與 MAR 都缺。
4. **K 3.2（nadir）/3.4（latest chem）是嚴重限制條件。** 優先在監測下補 K，並由臨床醫師審視 insulin 速率；2024 原文「K 升至 >3.5 前延後 insulin」（意譯）是在入院 K <3.5 的情境寫的。若 infusion 當時正在使用（無 MAR，屬假設），是否暫停或調整屬臨床判斷；但若當前 K 經確認 <3.5，臨床團隊須立即依低 K／DKA 流程處理，不能只沿用既有速率（見 §6、§8）。
5. **Fluid：** 0.9% saline 與 balanced crystalloid（Ringer's lactate、Plasma-Lyte 148）都是 2024 consensus 允許的初始液體；balanced 證據多為 biochemical（較快 acidosis/DKA resolution、較少 hyperchloremia），**無 mortality/AKI 等硬終點優勢的確證**。**現有資料不足以建立 0.45% saline 的適應症**；但 measured osmolality 318 與 osmolal gap 尚未釐清、labs 不完整，需等同時段經驗證的 direct-ISE Na／tonicity 與 fluid balance 才能判斷。「不符合 HHS」本身並不能證明所有低張液的適應症都不存在（見 §4.4）。實際給了什麼液體、多少量，**無 MAR/I/O 無法判斷**。
6. **Overlap 時間有出入：** 2024 consensus = SC basal 在停 IV 前 **1–2 h**；ADA 2026 Ch16 一般段落 = **2 h**，DKA/HHS 段落 = **2–4 h**（同一章內不一致）。
7. **Toujeo（insulin glargine U300）不能直接套「常規 1–2 h overlap」：** US PI：注射後作用約在 6 h 內逐漸出現，steady state 至少需 5 天；EU SmPC：steady state 3–4 天；2024 consensus 明言目前沒有轉換到 ultra-long-acting insulin（如 degludec、glargine U300）的研究（原句見 §5.1）。
8. **NovoRapid（insulin aspart）IV**：EU SmPC 允許在特定條件下 IV（vial、0.05–1.0 U/mL、指定稀釋液、polypropylene bag、醫護執行並監測），但它不是 regular human insulin；文件與 protocol 不應把兩者混寫（§10）。

---

## 1. 已知事實（Known facts，取自 case brief）與缺漏

| 時間 | Glucose (mg/dL) | Chem Na/K | Gas pH / HCO3⁻ / Na / K | 其他 |
|---|---|---|---|---|
| Day0 18:28 | 411 | 122 / 4.0 | 7.316 / 10.5 / 131 / 4.4（pCO2 20.3） | BOHB 5.6；measured osm 318；BUN 22；Cr 1.31；lipase 57；CRP 0.28；WBC 6.4 |
| Day0 19:46 | 380 | 123 / 3.9 | 7.278 / 11.3 / 133 / 4.3 | |
| Day1 01:58 | POC 220 | 130 / 3.4 | 7.385 / 13.4 / 138 / 3.6 | |
| Day1 05:53 | 297 | 129 / 3.6 | — | **BOHB 4.2（最後一筆 ketone）** |
| Day1 08:34 | — | — | 7.313 / 12.5 / 139 / 3.9 | HbA1c 13.6%；albumin 3.5；Mg 1.9 |
| Day1 15:03 | 281 | 133 / **3.2** | 7.357 / 15.2 / 139 / 3.4 | |
| Day1 17:31 | — | Cl 102（無同時 chem Na） | 7.401 / 17.0 / 138 / 3.7 | **TG 1950**；amylase 57；lactate 0.60 |
| Day1 22:39 | — | — | 7.386 / 17.2 / 138 / 3.8 | |
| Day2 04:25 | — | 135 / **3.4** | **7.329 / 21.6** / 139 / 3.5（pCO2 40.7） | phosphate 1.6（單位未列）；Mg 1.9 |
| Day2 POC | 181（01:00）、211、216、214、234（09:04） | | | |

**缺漏（不可補造）：** body weight/height/BMI、vitals、urine output、I/O、mental status、MAR（insulin 種類/速率、fluid 種類/速率/總量、K/P/Ca 補充）、Day2 BOHB、最新 Cr、Day2 Cl、gas 為 arterial 或 venous、Na 測定方法（direct vs indirect ISE）、C-peptide、islet autoantibodies。QA 中「IV insulin 3→2 U/h」「Toujeo 約 10 U」是**提問內容，不是已確認的給藥紀錄**。

---

## 2. QA5-A：DKA 是否已 resolved？能否停 IV insulin？

### 2.1 臨床問題
Day2 glucose 211–234 mg/dL、pH 7.329、HCO3⁻ 21.6，可以停 insulin infusion 並轉 SC 嗎？

### 2.2 證據
- **2024 consensus（Umpierrez GE et al. Diabetes Care 2024;47(8):1257–1275. DOI 10.2337/dci24-0032；PMID 39052901；PMC11272983；全文 HTML 已讀），Section 4 "Criteria for Resolution of DKA and HHS"：**
  > （意譯）DKA resolution 定義為 plasma ketone <0.6 mmol/L，且 venous pH ≥7.3 或 bicarbonate ≥18 mmol/L；理想上 glucose 也應 <200 mg/dL（11.1 mmol/L）。Anion gap 不應作為準則，因為大量 0.9% sodium chloride 造成的 hyperchloremic metabolic acidosis 會使其誤導；且隨酸中毒改善，β-hydroxybutyrate 會轉為 acetoacetate，所以應避免以 urinary ketone 判定 resolution。
- 同文 Section 3 "Diagnostic Criteria for DKA"：urine nitroprusside 主要測 acetoacetate，**不測 BOHB**；在治療後期因 BOHB→acetoacetate 轉換會高估嚴重度（意譯）；建議以 venous/capillary BOHB 做診斷與監測。
- 同文 Section 4（治療開頭段）：治療中 capillary glucose q1–2h；**electrolytes、phosphate、creatinine、BOHB、venous pH 每 4 h 抽一次，直到 DKA resolution。**
- Electrolyte-specialist 以目視讀取 2024 Fig 4（Diabetologia 同步版 CC-BY slide，DOI 10.1007/s00125-024-06183-8），回報**圖的註腳寫 pH >7.3／HCO3⁻ >18，內文寫 ≥**。這是**單一 session 目視判讀、未經獨立再現**；決策依據以 S02 正文為主。
- 註：本節意譯依據 Diabetes Care HTML 版；evidence register 以 Diabetologia 同步版（S02，§4 Criteria for resolution）為 text of record，兩版用字（單位寫法）略異，比對時應以語意為準。

### 2.3 為何 base excess、anion gap、urine ketone 都不是 resolution 標準
- **Anion gap：** 共識原文明言不用，因大量 0.9% NaCl 造成的 hyperchloremic acidosis 會讓 AG 與 HCO3⁻ 解讀脫鉤；本案又有 TG 1950 lipemia，加上 chem vs gas Na 差異（見 electrolytes 報告），**AG 的 Na 項本身就不可靠**。Day1 17:31 只有 Cl 102，沒有同時 chemistry Na/HCO3⁻，**不能算出可信的 AG**；用 gas Na 和 gas HCO3⁻ 混算屬於混方法，本報告不採用。
- **Base excess：** 是整體 acid–base 指標，同時反映 ketoacid、hyperchloremia（NAGMA）、lactate、respiratory 代償，**無法分辨酸是不是 ketone**。2024 consensus 的 resolution 定義不含 BE。SCOPE-DKA（見 §4）用 BE ≥−3 當 primary outcome，是研究終點的選擇，**不是臨床 resolution 定義**。
- **Urine ketone：** 如上，nitroprusside 不測 BOHB，且治療中後期會高估；尿液亦受 renal handling 與時間延遲影響。

### 2.4 個案應用
- **Acid–base 部分：** Day2 04:25 pH 7.329（≥7.3）且 HCO3⁻ 21.6（≥18）→ 已符合。但注意 "OR" 規則的陷阱：Day1 01:58 pH 7.385 時 HCO3⁻ 只有 13.4、Day1 17:31 pH 7.401 時 HCO3⁻ 17.0；若只看 pH，會過早「符合」acid–base 條件。gas 是 arterial 或 venous 未記載，而共識寫的是 **venous pH**。
- **Day2 pCO2 40.7、HCO3⁻ 21.6、pH 7.329：** 與 Day1 22:39（pH 7.386、HCO3⁻ 17.2；pCO2 未列，以 Henderson–Hasselbalch 推算約 30 mmHg，屬推算值）相比，**pH 下降的同時 HCO3⁻ 上升、pCO2 上升**。這不能解讀為 metabolic acidosis 惡化；較可能是呼吸成分改變，或兩次檢體的動脈／靜脈來源不同。gas 檢體類型未記載，因此 pH 單一數值的解讀要保留，應以 HCO3⁻ 加 BOHB 為主。HCO3⁻ 21.6 仍略低，可能是殘餘 ketoacid，也可能是 hyperchloremic NAGMA；**沒有 BOHB 和同時段 Cl，無法區分**，這正是 BOHB 必須補抽的原因。
- **Ketone：** 最後一筆 BOHB 4.2 是 Day1 05:53（比 Day0 5.6 只降約 25%），之後約 22 小時沒有 ketone 數據。**不能推定已 <0.6。**
- **Glucose：** 211–234 未 <200（理想值未達）；Day2 01:00 為 181，之後回升。若當時有使用 insulin infusion 與 dextrose，可能反映速率或 dextrose 量的調整、進食，或 ketosis 未清；**無 MAR，以上皆屬假設，無法判斷。**

**判定：DKA resolution 未確認（indeterminate），不是「已 resolved」。** 建議依序：
1. 立即補 BOHB（lab 或 POC；共識提到 POC 在 BOHB ≥5 mmol/L 時準確度有疑慮，本案此時應已低於此範圍）；
2. 同一管抽 chemistry Na、Cl、HCO3⁻、K、Cr、glucose，並註明採血部位；
3. BOHB <0.6 且 acid–base 達標 → 進入 §5 transition；BOHB ≥0.6 → 持續 IV insulin＋dextrose，不因 glucose 而停（前提是 K 安全，見 §6）。

---

## 3. QA5-B：Glucose <250 時的 insulin 與 dextrose；為何不給固定速率

### 3.1 證據
- 2024 consensus Section 4 "Insulin"：preferred 為 IV continuous short-acting insulin，**fixed-rate 0.1 U/kg/h** 或 nurse-driven variable-rate protocol。
  > （意譯）glucose 降到 <250 mg/dL（13.9 mmol/L）後，0.9% saline infusion 中加入 5–10% dextrose，insulin infusion 降至 0.05 units/kg/h；之後調整 IV insulin 使 glucose 維持約 200 mg/dL（11.1 mmol/L），並持續到 ketoacidosis 緩解。
- 同文 Section 4 "Fluid Therapy"：glucose 通常在 4–8 h 內降到 <250，**早於 ketoacidosis 緩解**，因此加 dextrose 是為了預防 hypoglycemia，並讓 insulin 能持續給到 ketonemia 矯正（意譯）。
- ADA 2026 Ch16（Diabetes Care 2026;49(Suppl 1):S339–S355. DOI 10.2337/dc26-S016；PMID 41358892；PMC12690180；全文 HTML 已讀），"Diabetic Ketoacidosis and Hyperglycemic Hyperosmolar State" 段：
  > （意譯）若採 nurse-driven insulin infusion protocol，速率不應低於 1 unit/h，以利 acidosis 緩解。
- 2024 Table 3（Hypoglycemia）：DKA 治療中 hypoglycemia（<70 mg/dL）發生率 16–28%；嚴重 hypoglycemia（<40 mg/dL）與 mortality 增加相關。

### 3.2 個案應用
- 本案 glucose 211–234：落在「<250 → dextrose＋減速、目標約 200」的區間。**Insulin 的目的此時是清 ketone，不是降糖**，所以不應因 glucose 接近 200 就停滴（若當時正在使用 infusion；無 MAR）。
- 實際用的是 fixed-rate 還是 variable-rate、有沒有加 dextrose、濃度多少，**MAR 缺，無法評估**。

### 3.3 Weight 未知 → 不建議固定 U/h（僅示意算術）
0.05 U/kg/h 是 weight-based 的。若把 QA 中的速率反推「隱含體重」：
- 3 U/h ÷ 0.05 = 隱含 60 kg；2 U/h ÷ 0.05 = 隱含 40 kg。
- 以上**只是說明性算術**，不能僅憑「肥胖」就推論 2–3 U/h 偏低或不足。肥胖時 weight-based 劑量該用哪一種體重，共識也沒有規範。**目前劑量是否足夠，要看對 K、ketone（BOHB）、glucose 的實際反應；weight 與 MAR（實際速率與時間）都缺，所以不做判斷，也不給數值處方。**
- 監測依據是**每 1–2 h glucose＋每 4 h BOHB/pH/HCO3⁻/K**（S02 §4 開頭段）。2024 共識**沒有禁止降低 insulin**：降到 0.05 U/kg/h 之後，正文寫的是依 glucose（約 200 mg/dL）調整 insulin，並持續到 ketoacidosis 緩解（S02 §4 Insulin）；唯一的下限是 ADA 2026 對 nurse-driven protocol 的 1 unit/h（S03 DKA/HHS 段）。
- 原則（**ketosis 未解仍需 insulin**）：依 glucose、K、ketone 的反應調整 insulin 速率，並以 dextrose 支持，避免 hypoglycemia 而能持續給 insulin。「固定 insulin 速率、只調 dextrose」是部分院內 protocol 的作法之一，**不是 2024 共識的唯一規定**。BOHB 未依預期下降時，應檢討 insulin 是否足量、IV line 是否通暢、dextrose 是否過量。
- **低 K 優先**：K <3.5 時要優先處理（§6），不能因擔心 ketosis 反彈就忽略低 K 而維持原速率。

---

## 4. QA4：Fluids — 0.9% saline vs balanced crystalloid vs 0.45% saline；NAGMA

### 4.1 臨床問題
DKA 該用 0.9% NaCl 還是 Ringer's lactate/Plasma-Lyte？什麼時候用 0.45%？hyperchloremic NAGMA 的意義為何？本案實際給液是否適當？

### 4.2 指引證據
- **2024 consensus Section 4 "Fluid Therapy"：**
  - （意譯）初始復甦液體應依當地可得性、成本與資源選擇。多數指引建議 isotonic saline；但大量使用可能伴隨 hyperchloremic normal anion gap metabolic acidosis，以及 ICU 與住院天數延長。
  - Balanced crystalloids（Ringer's lactate 或 Plasma-Lyte 148）相較 saline，共識文字描述為 DKA resolution 較快、住院天數較短、hyperchloremic metabolic acidosis 較少（意譯；引用 refs 125–129：Alghamdi 2022 MA、Self 2020、Catahay MA、Jahangir review、Bergmann pediatric）。
  - 無 renal/cardiac compromise 的成人：前 2–4 h 以 isotonic saline 或 balanced crystalloid 500–1,000 mL/h 開始（意譯）；之後依 BP、HR、I/O、Na 調整，24–48 h 內補足 deficit；老年、心臟或腎臟疾病者要謹慎（Section 4 另建議 250 mL bolus 並頻繁評估）。
  - 0.45% NaCl（HHS 段，意譯）：初期 serum Na 上升本身不是給低張液的理由；只有在已有足夠的正向液體平衡與適當 insulin、osmolality 仍未下降時，才有 0.45% sodium chloride 的適應症。
  - Glucose <250：fluid 改為含 5–10% dextrose（原文描述為加在 0.9% sodium chloride 之外）。
- **2024 Table 3 "Normal anion gap metabolic acidosis"：** 恢復期可見 hyperchloremic non–AG acidosis，機轉為 keto-anion 流失（無法再代謝回 HCO3⁻）加上含氯液體；共識描述為自限性、臨床後果少（意譯）；balanced solution 或較慢的 saline 速度可減少。
- **ADA 2026 Ch16：** DKA 管理沿用 2024 consensus 的 Fig 16.1 pathway（圖說註明改編自 Umpierrez et al.），**未新增液體種類的建議**。

### 4.3 Primary trial 與 meta-analysis（以 abstract 與 metadata 驗證；全文由 librarian 負責）
| 研究 | 設計/人數 | 主要結果 | 限制 |
|---|---|---|---|
| **Self WH et al. JAMA Netw Open 2020;3(11):e2024596**. DOI 10.1001/jamanetworkopen.2020.24596；PMID 33196806；PMC7670314 | SALT-ED＋SMART 兩個 pragmatic cluster-crossover RCT 的 **DKA 次群分析**；成人 n=172（balanced 94 vs saline 78） | DKA resolution 中位數 13.0 vs 16.9 h（採 **2009 ADA 定義**：glucose <200 加上 HCO3⁻ ≥15、pH >7.3、AG ≤12 三項中的兩項；**不是 2024 的 BOHB 定義**，且含 AG），aHR 1.68（95% CI 1.18–2.38）；insulin infusion 停止時間 9.8 vs 13.4 h，aHR 1.45（1.03–2.03） | 次群分析、單一學術中心、cluster 層級分派、非盲；未以硬終點為主；resolution 定義含 AG，與 2024 定義不同 |
| **SCOPE-DKA**：Ramanan M et al. Intensive Care Med 2021. DOI 10.1007/s00134-021-06480-5；PMID 34609547 | 7 家醫院 ICU 嚴重 DKA，cluster-crossover open-label Phase 2；mITT n=90（PL 48 vs saline 42） | Primary：48 h 時 resolution（**base excess ≥−3**）96% vs 86%，OR 3.93（0.73–21.16），p=0.111，**primary 未達標**；secondary 24 h 時 69% vs 36%，OR 4.24（1.68–10.72）。Intensive Care Med 2021;47:1248–1257 | Primary 未達標；以 BE 定義 resolution（非 ketone 定義）；open-label；樣本小。數字已由 evidence-librarian 以 PubMed abstract（efetch）核對；全文未取得 |
| **BRISK-ED**：Yan JW et al. Emerg Med J 2024. DOI 10.1136/emermed-2023-213290；PMID 38050056 | Triple-blind pilot RCT（RL vs NS），n=52 | Feasibility 達標；resolution 中位數 RL 15.7 vs NS 12.7 h（未設計做檢定） | Pilot，不能推論療效；**數字方向與 balanced 有利的假設相反** |
| Alghamdi NA et al. Crit Care Explor 2022. DOI 10.1097/CCE.0000000000000613；PMID 35018349 | MA，8 RCT，n=482 | Saline 的 resolution 時間較長 MD +3.51 h（moderate certainty）；LOS +0.89 d | 小型試驗、異質性 |
| Liu Y et al. Front Endocrinol 2024. DOI 10.3389/fendo.2024.1367916；PMID 38836222 | MA，11 RCT，n=753 | Resolution 時間**無差異** MD −1.49 h（−4.29 to 1.31）；MAKE 與 hypokalemia 無差異；Cl 較低 | 異質性 I²=65% |
| Soliman KAR et al. 2026（J Crit Care Med）. DOI 10.62838/jccm-2026-0022；PMID 42516157 | MA，11 RCT（6 個 n=491 進入定量分析） | Resolution 時間**不顯著** MD −1.50 h（−3.79 to 0.79）；12 h HCO3⁻ +2.5 | 作者結論為 clinical equipoise |

**結論：** Balanced crystalloid 在 **biochemical outcome**（chloride 較低、HCO3⁻ 較高、部分研究 resolution 較快）上一致較好；但「DKA resolution 時間」在較新的 MA 中不穩定，**目前沒有 RCT 證明 mortality、AKI/MAKE、cerebral edema 等硬終點有差異**。各研究的 resolution 定義不一（ADA 定義 vs BE），也是比較上的限制。因此 2024 consensus 的立場是「兩者皆可，依可得性選擇」，並註明 balanced 的好處。

### 4.4 個案應用
- **0.45% saline：現有資料不足以建立適應症（not established），但也不能據此斷言所有低張液的適應症都不存在。**
  (a) 本案不符合 HHS／mixed DKA/HHS 也不是 mixed DKA/HHS。HHS 需 glucose ≥600、effective osmolality >300（或 total >320）、BOHB <3.0、pH ≥7.3 且 HCO3⁻ ≥15（ADA 2026 Table 16.1）；本案 glucose 411、BOHB 5.6、HCO3⁻ 10.5。
  (b) Tonicity 不高：若採 gas Na 131（推定為 direct ISE，**方法未證實**），effective osmolality ≈ 2×131 + 411/18 ≈ 284.8；若用 chem Na 122 會更低（≈266.8）。chem Na 偏低可能是 lipemia／indirect-ISE 的假性低值，但這是**合理而未證實的推論**（TG 為 Day1 才測；詳見 electrolytes 報告）。
  (c) 2024 明言初期 serum Na 上升本身不是給低張液的理由（意譯）。
  (d) **未解決的限制：** measured osmolality 318 與計算值之間的 osmolal gap（gas Na 計約 25）尚未拆解；Na 測定方法未經 lab 確認；Day2 沒有 measured osmolality、Cl、Cr；也沒有 fluid balance、urine output、weight、vitals。「不符合 HHS」只排除了 2024 consensus 在 HHS 段落寫的 0.45% 情境，**並不證明**其他低張液情境（例如經驗證的 true hypernatremia／free-water deficit、持續的 hypertonicity）都不存在。
  (e) **條件式行動：** 若要評估低張液，需要同時段的經驗證 direct-ISE Na（或 lab 確認方法）、measured osmolality、glucose、BUN，並評估 fluid balance 與 urine output；是否改變液體張力，由臨床團隊依這些資料決定。
  (f) **兩件事不要混淆：** 以低張液（0.45% saline 或作為 free water 的 D5W）矯正 tonicity，與 glucose <250 時加 5–10% dextrose 以避免 hypoglycemia、支持 insulin 持續給予（S02 §4 Fluid therapy／Insulin），是不同目的；後者不是低張液適應症的問題。
- **Chem Na 122→135 的上升不應被當成「correction 太快」，也不應據此改用低張液：** chem 與 gas Na 的差距隨時間縮小（−9、−8、−6、−4），**可能**與干擾因素消失有關，但也可能受 glucose 下降、輸液與檢體差異影響；這只是支持性線索，不是已證實的機轉（TG 是 Day1 17:31 抽的，與 Day0 不同時）。本點已與 electrolyte-specialist 交叉確認（§8）。
- **NAGMA：** Day2 HCO3⁻ 21.6 仍偏低，可能是 ketoacid 未清，也可能是 hyperchloremic NAGMA。區分需要**同時段的 BOHB 加 chemistry Na/Cl/HCO3⁻**。只有在**已達 2024 resolution 條件**（ketone <0.6 且 venous pH ≥7.3 或 HCO3⁻ ≥18），且同時段 chemistry **證實**為 hyperchloremic NAGMA 時，才可說 isolated NAGMA 本身不應延長 DKA 的 IV insulin（S02 §3 指出恢復期 NAGMA 若被誤認為持續 DKA，可能延誤轉 SC）。**不能只憑 ketone <0.6 加 Cl 偏高就一律停滴**；停滴仍需完成 §5.3 的 transition 條件。處理方向是減少含氯液體，或改用 balanced solution。
- **Ringer's lactate 搭配 dextrose：** 共識原文描述 dextrose 是加在 0.9% sodium chloride 之外；改用 balanced 液體作為 dextrose 載體屬於院內 protocol 的選擇。RL 含 K 約 4 mmol/L，不足以作為補 K 的方案。
- **實際給液是否適當：無法判斷。** 缺 MAR（液體種類、速率、總量）、I/O、urine output、weight、BP/HR、最新 Cr、心臟功能。只能說：Day0 Cr 1.31、BUN 22 時應依 2024 監測腎功能（Table 3 "Acute kidney injury"：建議每日監測），並審視液體是否過量或不足。**不提供 mL/h 數值處方。**

---

## 5. QA5-C：IV→SC transition；overlap 1–2 h vs 2–4 h；Toujeo U300

### 5.1 證據
- **2024 consensus Section 4 "Transition to Maintenance Insulin Therapy"：**
  > （意譯）SC insulin 開始給予與 IV insulin 停止之間，應保留 1–2 h 的 overlap。
  Fig 5 圖說（意譯）：basal-bolus 是偏好方案，應在停 IV insulin 前 1–2 h 開始。
  TDD 估算：insulin-naive 為 0.5–0.6 U/kg/day；有 hypoglycemia 風險者（kidney failure、frailty）約 0.3 U/kg/day；也可參考入院前劑量與 HbA1c，或 IV 速率（需謹慎）。並寫 basal insulin 至少在停 IV 前 1–2 h 開始（意譯）。
  新診斷者（意譯）：long-acting basal insulin 以 0.15–0.3 units/kg SC 起始；infusion 期間合併低劑量 basal（0.15–0.3 U/kg）有研究顯示可縮短 infusion 時間、防止 rebound，但部分臨床醫師因 hypoglycemia/hypokalemia 風險而避免。
  **關鍵句：**「There are no current studies on transitioning to ultra-long-acting insulin (e.g., degludec, glargine U300).」
  Section 8（future research）也把 DKA/HHS 緩解後轉換到 ultra-long-acting insulin 列為研究缺口（意譯）。
- **ADA 2026 Ch16：**
  - "Transitioning From Intravenous to Subcutaneous Insulin"（一般住院段，意譯）：SC basal insulin 應在停 IV infusion 前 **2 h** 給予（ref 63 Kreider & Lien, Curr Diab Rep）。
  - "Diabetic Ketoacidosis and Hyperglycemic Hyperosmolar State" 段（意譯）：成功轉換需在停 IV insulin 前 **2–4 h** 給 basal insulin，以免 SC insulin 作用上升期間 ketoacidosis 復發與 rebound hyperglycemia（refs 63、179；179 = Harrison VS et al. Pediatr Diabetes，小兒 glargine 合併 IV insulin 研究）。
  - Recommendation 16.16（意譯）：強調及時且有橋接（bridged）地轉換到 SC maintenance insulin（Grade A）。
  - 總 TDD 可依體重、入院前劑量，或過去 6–8 h 血糖穩定達標期間的 insulin infusion 速率計算（意譯）。
  - 住院 insulin 段（S03，refs 78–81，意譯）：glargine U-300 等濃縮 insulin 在住院與圍手術期的使用資料有限、結果不一。

**差異與詮釋：** 2024 consensus 寫 1–2 h；ADA 2026 DKA 段寫 2–4 h，一般段寫 2 h，**同章內即不一致**。2–4 h 的依據是一篇 review 和一篇小兒研究，並非成人 DKA RCT。**以下屬本報告作者推論與臨床判斷，非指引原文**：這些 overlap 數字看來是以 glargine U100/detemir/NPH 等傳統 basal 的經驗為基礎（兩份指引都未明說）；較保守的作法可考慮取 overlap 範圍上限，或在 infusion 期間更早給 basal，並在停 IV 後加強 glucose 與 ketone 監測，實際依院內 protocol。

### 5.2 Toujeo（insulin glargine 300 U/mL）官方 label
| 項目 | US PI（Sanofi 原廠 label，openFDA set_id c9561d96-124d-48ca-982f-0aa1575bff36，effective 2025-05-30；§5.2/§12.2/§12.3 文字已核對） | EU SmPC（EMA EPAR product information，下載日 2026-10-28） |
|---|---|---|
| Onset | §5.2 / §12.2：注射後作用約在 6 h 內逐漸出現（意譯） | §5.1：效果比 glargine U100 更穩定、延長，>24 h（最長 36 h） |
| Steady state | §12.3：每日一次 SC 至少 5 天才達 steady-state 濃度；§5.2：完整降糖效果可能至少 5 天後才顯現（意譯） | §5.2：每日給藥 3–4 天後達治療範圍內的 steady state（意譯） |
| IV→SC transition | §5.2：對接受 IV insulin 的 type 1 diabetes 患者，停 IV 前應考量 Toujeo 較長的 onset（意譯） | — |
| DKA | — | §4.4：Toujeo 不是治療 DKA 的首選 insulin，此時建議改用 IV regular insulin（意譯） |
| 起始劑量（insulin-naive T2D） | §2.3：0.2 U/kg once daily | §4.2：0.2 units/kg |
| Unit-for-unit | §5.2/§12.2：on a unit-to-unit basis, TOUJEO has a lower glucose lowering effect than LANTUS；換藥時常需較高劑量 | §4.2：units 為 Toujeo 專屬 |
| 途徑 | 禁 IV/IM/pump | §4.2：不可 IV 給予，不可用於 pump（意譯） |

**個案應用（Toujeo「約 10 U」只是 QA 提問）：**
1. 若在停 IV 前 1–2 h 才給第一劑 Toujeo，以 6 h 的 onset 推算，停 IV 後會有數小時 basal 覆蓋不足的空窗；本案 ketosis 狀態未明，這段空窗有 **rebound ketosis** 風險。**常規 1–2 h（甚至 2–4 h）overlap 不能直接套用到 U300 的第一劑。**
2. 2024 consensus 明言 U300 轉換**缺乏研究**。可考慮的替代策略（由主治/內分泌決定，非 order）：
   (a) 初始 transition 使用 glargine U100、detemir 或 NPH 等證據較多的 basal，穩定後再換 U300（換藥時注意 unit-for-unit 效價差異）；
   (b) 若決定用 U300，在 IV infusion 期間更早給予（類似 2024/2026 所述 infusion 中合併低劑量 basal 的概念，但那些研究多用 glargine U100），延長 overlap，並在停 IV 後頭 24–72 h 密集監測 glucose 與 BOHB，配合 rapid-acting prandial/correction。
3. **10 U 的劑量合理性無法評估：** 依 weight-based 算法（basal 0.15–0.3 U/kg；label 起始 0.2 U/kg；TDD 0.5–0.6 U/kg/day），10 U 只相當於體重 33–67 kg 時的 basal 量。沒有體重就無法判斷 10 U 是否合適（肥胖與 HbA1c 13.6% 本身不足以推論劑量高低）。另需考慮 U300 單位效價較 U100 低、steady state 要 3–5 天，**前幾天的實際 basal 效果會比標示劑量更低**。
4. K、Mg：K 不是 resolution 標準，但 transition 前後應依 2024（K 維持在 4–5 mmol/L）把 K 補到目標並追蹤 Mg（Day2 Mg 1.9 mg/dL）；K <3.5 應優先處理（見 §6）。

### 5.3 Transition 條件清單（條件式，非 order）
- [ ] 同時段 BOHB <0.6 mmol/L 且 venous pH ≥7.3 或 HCO3⁻ ≥18（目前缺 BOHB）
- [ ] 理想 glucose <200 mg/dL
- [ ] 營養狀態與 SC 方案相配（**不是絕對條件**）：能進食者可用 basal-bolus（2024 Fig 5 偏好）；尚不能進食者，需有合適的 basal＋correction（必要時配合 dextrose）或續用 IV insulin 的計畫，依臨床穩定度與院內 protocol 決定
- [ ] 已知體重（計算 TDD／basal）
- [ ] K 在監測下補足（目標 4–5）、Mg 已追蹤
- [ ] Basal 在停 IV 前給予：traditional basal 依 2024 1–2 h / ADA 2026 2–4 h；**U300 需更早、更長的 overlap，且證據不足**
- [ ] 停 IV 後持續監測 glucose 與 ketone

---

## 6. K <3.5 對 insulin 的限制（與 electrolytes 報告交叉）

- 2024 Section 4 "Potassium"（意譯）：補 K 以維持 K 4–5 mmol/L 為目標；入院時 K <3.5（5–10% 患者）應以 10 mmol/h 開始補 K，並將 insulin 延後到 K 升至 >3.5 mmol/L；並建議 insulin 開始後 2 h 測 K，之後每 4 h 測至 resolution。Table 3：治療中 hypokalemia（<3.5）約 55%；≤2.5 與 mortality 增加相關。
- Electrolyte-specialist 讀取 Fig 4 後回報：K 欄位為 K⁺ <3.5 時給 10–20 mmol/h 直到 K⁺ >3.5，更快的補充需經 central venous access（意譯），**沒有「hold insulin」字樣，也沒有限定入院時**；圖與內文的速率不同（10 vs 10–20）。這是**單一 session 目視判讀、未經獨立再現**；本報告的決策依據以 S02 正文為主。
- **個案：** Day1 15:03 chem K 3.2（gas 3.4），Day2 04:25 chem K 3.4（gas 3.5，不同 analyzer/採檢；早期有 hemolysis 紀錄）。若當時正使用 IV insulin（無 MAR，屬假設），K 3.2–3.4 是 **red flag**：應優先在 ECG/腎功能/urine output 監測下補 K，並審視 insulin 速率。是否暫停或調整 infusion，要和 ketosis 未清時停 insulin 的反彈風險權衡，屬臨床判斷；但**若當前 K 經確認 <3.5，臨床團隊須立即依低 K／DKA 流程決定暫停或調整 insulin，並在監測下補 K，不能只沿用既有速率而不處理**。**IV 補 K 的速率與濃度、是否可口服，屬院規與臨床判斷，依 IV access 決定；口服並非絕對禁止；本報告不開個人化處方。**
- **無 MAR，不能宣稱已補或未補 K/insulin。**

---

## 7. 延伸：糖尿病分類與 KPD 追蹤；TG 1950 與 pancreatitis 風險

### 7.1 分類（不逕下診斷）
- 已知：42 歲男性、肥胖、HbA1c 13.6%（反映數月的慢性高血糖，不像 fulminant 型）、無明確誘因（WBC 6.4、CRP 0.28、胸片無 active lesion）、無 DM 家族史、半年前 borderline。
- 2024 consensus（S02 Section 1 epidemiology 段，意譯）：在 **Black/African American 與 Hispanic/Latino** 新診斷、unprovoked DKA 的成人中，超過一半為 T2D，文獻稱為 atypical diabetes 或 ketosis-prone T2D；特徵包括肥胖、**強烈 DM 家族史**、可測得的 insulin reserve、無自體免疫標記、追蹤中可停 insulin。這段流行病學針對特定族群，**不能直接外推到本個案**；本案也**沒有家族史**。KPD 在此只是鑑別診斷之一。
- **Aβ classification**（Balasubramanyam A et al. Endocr Rev 2008;29(3):292–302. DOI 10.1210/er.2007-0026；PMID 18292467；僅讀 abstract）：依 β-cell autoimmunity（A±）與 β-cell functional reserve（β±）分為四型，可預測日後是否依賴 insulin。
- **建議追蹤（恢復後，非急性期）：** islet autoantibodies（如 GAD65、IA-2、ZnT8）；在代謝穩定、脫離 glucotoxicity 後量 C-peptide（fasting 和/或 stimulated）。急性期的 C-peptide 受 glucotoxicity 影響，解讀需謹慎；最適檢測時點依原始文獻而定，**本報告未取得全文核對**。在分類確定前，出院時應以 insulin 為主，降階需由專科追蹤決定。（S02 Section 6 Table 4 有關 DKA 後不常規開始或繼續 SGLT2 inhibitor 的建議，位於「SGLT2 inhibitor 相關 DKA」列；本案未使用 SGLT2 inhibitor，若要用於本案屬**外推**，需由專科判斷。）

### 7.2 TG 1950 mg/dL 與 pancreatitis
- TG 1950 mg/dL（Day1 17:31）屬極高；嚴重 hypertriglyceridemia 是 acute pancreatitis 的已知病因（ACG guideline：Tenner S et al. Am J Gastroenterol 2024;119(3):419–437. DOI 10.14309/ajg.0000000000002645；**僅核對 metadata/abstract，TG 閾值等細節未核對全文，此處不引用具體數字**）。2024 consensus Section 1 也把 pancreatitis 列為 DKA 的可能誘因。
- **個案：** lipase 57 U/L（<60）、amylase 57、無腹痛記錄 → **目前資料不支持已發生 pancreatitis，但不能絕對排除**（lipemia 對酵素檢驗可能有干擾；DKA 本身可造成非特異性酵素變化；未做影像）。
- 合理追蹤：注意腹痛/嘔吐；insulin 治療與血糖控制後複查 TG（DKA 的 insulin deficiency 本身會推高 TG）；若出現症狀再查 lipase 並考慮影像；出院後做 lipid 管理與 secondary cause 評估（交由內分泌/腸胃科）。TG 也是 chem Na 假性偏低的可能原因（見 electrolytes 報告）。

---

## 8. Cross-session challenge 紀錄（native SendMessage）

| ID | 方向 | 內容摘要 | Native 送達 | ACK |
|---|---|---|---|---|
| fi-challenge-01 | fluid-insulin → electrolyte-specialist | C1：同時段 chem Na 122 用於 tonicity/osmolal gap 不一致（chem 計算 osm ≈274.7、gap ≈43；gas 計算 ≈292.7、gap ≈25）；C2：K <3.5「delay insulin」是否只限入院情境、Fig 4 措辭 | Tool 回報成功送入對方 inbox；未收到 held/refused notice | **已 ACK**（對方回覆 ACK fi-challenge-01；C1 AGREE；C2 以 Fig 4 目視確認無「hold insulin」字樣） |
| ELEC-CH1 | electrolyte-specialist → fluid-insulin | A1–A4 Na/tonicity/HHS 判定；B(i)–(iii) K 與 transition | 已收到 | 我方回覆 ACK：A1–A4 AGREE；B(i) PARTIAL AGREE（K 不是 resolution 標準，但 transition 前後要把 K 補到 4–5）；B(ii)(iii) AGREE |

**Codex 臨床審查後修訂（2026-10-28，synthesis-editor 執行）：** §0 第 2、4 點；§2.2 Fig 4 與 text-of-record 註記；§2.4 Day2 gas 解讀與 MAR 假設；§3.3 insulin 調整（2024 未禁止降低 insulin）；§4.4 (b)(f)、Na 差距與 NAGMA 條件；§5.1 ADA 2026 U-300 句與「作者推論」標示；§5.3 進食非絕對條件；§6 單一 session 判讀、條件式 insulin、確認 K <3.5 的處理；§7.1 KPD 族群範圍與 SGLT2 外推。詳見 `reports/reviews/clinical-review.md`。

**共識：** (1) Tonicity 以 measured osmolality 加 gas（推定 direct-ISE）Na 為錨，條件是 lab 確認測定方法；corrected Na 兩種數值都列出，皆為推算值而非測量值。(2) 本案是 DKA（以 HCO3⁻ 判為 moderate），不符合 HHS；現有資料不足以建立 0.45% saline 適應症，但需等經驗證的同時段 tonicity 與 fluid balance 才能定論（Codex 審稿後修訂措辭）。(3) K <3.5 → 優先在監測下補 K；若 infusion 正在使用（無 MAR），暫停或調整屬臨床判斷，但確認 K <3.5 時須立即依低 K／DKA 流程處理。
**未解決：** Na 測定方法（direct vs indirect ISE）待 lab 確認；Fig 4 只有單一 session 目視判讀、未經獨立再現；ADA 2026 Fig 16.1 雙方皆未以文字驗證。

---

## 9. 來源、工具結果與限制

| 來源 | 取得方式 | 狀態 |
|---|---|---|
| 2024 consensus DOI 10.2337/dci24-0032（PMID 39052901，PMC11272983） | PMC HTML 全文以 curl 下載轉文字後 grep 逐字引用 | **全文已讀**；Fig 2/4/5 為圖片，未以文字驗證（Fig 4 由 electrolyte-specialist 目視） |
| ADA 2026 Ch16 DOI 10.2337/dc26-S016（PMID 41358892，PMC12690180） | diabetesjournals.org 被 Cloudflare 擋（失敗）→ 改用 PMC HTML 全文 | **全文已讀**；Fig 16.1 為圖片，未驗證 |
| Toujeo EU SmPC（EMA EPAR product information PDF） | curl 下載；pdftotext；SHA256 05d36a6d50acda15612619f58c6f2b433b88d383f261fed3243417274c24906d | 全文已讀；revision date 欄位未能抽出 |
| NovoRapid EU SmPC（EMA EPAR PDF） | 同上；SHA256 596b72a285a1a6a53ef22a3d8e8f5b78afcad8d6266d30dcb5e7e2429eede7f2 | 全文已讀 |
| Toujeo US PI；NovoLog US PI | openFDA label API：Toujeo 用 Sanofi 原廠 set c9561d96（effective 2025-05-30）；NovoLog 用 Novo Nordisk set 3a1e73a2（effective 2023-02-28）。（rev 3 更正：原先引用的 257ca17b／13891e5a 是 repackager（A-S Medication Solutions）的 listing；evidence-librarian 指出後已改，引用文字內容相同） | Label 文字已讀 |
| Self 2020 | 本人只讀 abstract；evidence-librarian 有全文（LlamaParse），確認 resolution 採 2009 定義 | 全文由 librarian 持有（evidence/source-register.json） |
| Alghamdi 2022、BRISK-ED、Liu 2024、Soliman 2026、Balasubramanyam 2008 | paper-search PubMed／Europe PMC | **Abstract-only** |
| SCOPE-DKA 2021 | WebSearch 二手摘要＋Europe PMC metadata；evidence-librarian 以 PubMed efetch 核對 abstract | Abstract-only（Sci-Hub 失敗）；數字已核對 |
| ACG AP guideline 2024 | Crossref metadata | Metadata／abstract only |

- 上述 PDF 僅存於本 session 的暫存區，**未寫入 evidence/、fulltext/、parsed/**（由 librarian 負責）；未使用 LlamaParse；未上傳任何病歷。
- **台灣 TFDA 核定仿單未查核**；NovoRapid/Toujeo 台灣仿單內容可能與 EU/US 版本有細節差異。
- 本報告未讀原始病歷，只讀去識別 case brief。

## 10. NovoRapid（insulin aspart）IV vs regular insulin
- **EU SmPC §4.2 "Intravenous use"（NovoRapid vial，意譯）：** 必要時可 IV 給予，須由醫師或其他醫護人員執行；NovoRapid 100 units/mL 以 0.9% sodium chloride、5% 或 10% dextrose（含 40 mmol/L potassium chloride）稀釋至 0.05–1.0 unit/mL insulin aspart、使用 polypropylene infusion bag 的輸注系統，室溫下 24 h 穩定；初期會有部分 insulin 吸附於袋材，需監測血糖。**只有 vial 可 IV**（Penfill/FlexPen 等需 IV 時應改用 vial）。
- **US NovoLog PI §2（Novo Nordisk 原廠 label，openFDA set 3a1e73a2，effective 2023-02-28，意譯）：** IV 時稀釋至 0.05–1 unit/mL insulin aspart，使用 polypropylene infusion bag；僅能在醫療監督下、密切監測 glucose 與 K 時 IV 給予，以避免 hypoglycemia 與 hypokalemia。
- **SC PK（EU §4.2/§5.1）：** onset 10–20 min，峰效 1–3 h，作用 3–5 h。這是 **SC** 數據，不可外推為 IV 行為。
- **區分：** 2024 consensus 與 Toujeo SmPC 寫的是 IV「short-acting／regular insulin」；aspart IV 在 label 條件下可用，但**不是 regular human insulin**。若院內 IV protocol 用 aspart，order/MAR 應寫明藥名、濃度、稀釋液與袋材，不應記為「RI」；本案 MAR 缺，無法得知實際用的是哪一種。
