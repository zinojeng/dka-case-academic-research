# Case timeline（去識別，Day0/1/2）— case-analyst

> 角色：case-analyst（bootstrap）。只提供事實、同時間點配對、單位假設與算術估算；**不做治療建議**。
> 時間標記：Day0/1/2 + 時刻；T0 = Day0 18:28（第一筆列出的 lab），**不是** insulin 開始時間（insulin 開始時間未知）。

## 0. 資料來源與取得限制（重要）
- 指定來源 `.private/case-brief.md`：本 session 讀取時被 permission settings **拒絕**（Bash 與 Read 皆 denied），未嘗試任何繞道。
- 改用 CLAUDE.md 明列的另一個允許來源：可追蹤、已去識別的 `docs/case-questions.md`（其內容自述「來源：`.private/case-brief.md`（已去識別）」）。
- 因此：本檔所有數值**未能與 case-brief 逐字比對**；若 case-brief 與 case-questions 有轉錄差異，本檔不會發現。此項列入 unresolved，建議 Codex 或有權限者比對一次。
- 未讀取任何根目錄數字開頭原始病歷 MD；也未以 `reports/` 根目錄其他（非本角色）檔案作為資料來源。

## 1. 個案背景（事實，無推定）
- 男性 42 歲；肥胖（**無** height/weight/BMI 數值）；HTN、dyslipidemia 數年。
- 約半年前 borderline glucose，只飲食控制；無 DM drug；無家族 DM 史。
- 約一週：疲倦、食慾差、polydipsia/polyuria/nocturia；含糖運動飲料攝取增加。
- 無明確感染、腹痛、胸痛；chest X-ray 無 active lesion。

## 2. 主時間軸（依時刻）
欄位「同時配對」：✔ = 同一列時刻有 chemistry 與 blood gas；✘ = 只有一方。Blood gas 一律 **arterial/venous 未知**。

| 時點 | T0 起算 | Chemistry / 其他 | Blood gas | 同時配對 |
|---|---|---|---|---|
| Day0 18:28 | T+0:00 | plasma glucose 411 mg/dL；Na 122；K 4.0；BUN 22 mg/dL；Cr 1.31 mg/dL；Ca 9.3 mg/dL；BOHB 5.6 mmol/L；measured osmolality 318 mOsm/kg；lipase 57 U/L（ref <60）；CRP 0.28（單位未列）；WBC 6.4 | pH 7.316；pCO2 20.3；HCO3 10.5；Na 131；K 4.4 | ✔ |
| Day0 19:46 | T+1:18 | glucose 380；Na 123；K 3.9 | pH 7.278；HCO3 11.3；Na 133；K 4.3（pCO2 未列） | ✔ |
| Day1 01:58 | T+7:30 | Na 130；K 3.4；**POC** glucose 220（非 plasma lab glucose） | pH 7.385；HCO3 13.4；Na 138；K 3.6（pCO2 未列） | ✔（但 glucose 為 POC） |
| Day1 05:53 | T+11:25 | glucose 297；Na 129；K 3.6；BOHB 4.2 mmol/L | — | ✘ chemistry only |
| Day1 08:34 | T+14:06 | HbA1c 13.60%；albumin 3.5 g/dL；Ca 7.8；Mg 1.9 mg/dL（**無 Na/K/glucose 列出**） | pH 7.313；HCO3 12.5；Na 139；K 3.9（pCO2 未列） | 部分（gas Na/K 無 chemistry Na/K 可對照） |
| Day1 15:03 | T+20:35 | glucose 281；Na 133；**K 3.2（全程 nadir）** | pH 7.357；HCO3 15.2；Na 139；K 3.4（pCO2 未列） | ✔ |
| Day1 17:31 | T+23:03 | TG 1950 mg/dL；total CHO 413；HDL 23；direct LDL 52（calculated LDL unavailable）；**Cl 102（無同時 chemistry Na）**；Ca 8.2；phosphate 1.3（**單位未列**）；Mg 2.2；lactate 0.60（單位未列）；amylase 57（單位未列）；troponin/CK-MB normal（數值未列）；**無 glucose 列出** | pH 7.401；HCO3 17.0；Na 138；K 3.7（pCO2 未列） | 部分（chemistry 無 Na/K/glucose） |
| Day1 22:39 | T+28:11 | — | pH 7.386；HCO3 17.2；Na 138；K 3.8（pCO2 未列） | ✘ gas only |
| Day2 01:00 | T+30:32 | POC glucose 181 | — | ✘ |
| Day2 02:50 | T+32:22 | POC glucose 211 | — | ✘ |
| Day2 04:25–04:26 | T+33:57 | Na 135；K 3.4；Ca 7.8；phosphate 1.6（**單位未列**）；Mg 1.9；**無 plasma glucose、BOHB、Cr、albumin 列出** | pH 7.329；pCO2 40.7；HCO3 21.6；Na 139；K 3.5 | ✔（相隔約 1 分鐘；brief 以區間列出，未區分哪一筆在 04:25/04:26） |
| Day2 05:00 | T+34:32 | POC glucose 216 | — | ✘ |
| Day2 07:00 | T+36:32 | POC glucose 214 | — | ✘ |
| Day2 09:04 | T+38:36 | POC glucose 234（最後一筆 glucose） | — | ✘ |

來源附註（照錄）：多筆 lipemia、早期 hemolysis（**未指明是哪幾筆 specimen**）；無 ISE 方法；無 arterial/venous 資料；原始 CBC 重複。

## 3. 同時間點配對：chemistry vs blood gas Na/K
| 時點 | chem Na | gas Na | Δ(gas−chem) | chem K | gas K | Δ(gas−chem) | 同時 glucose |
|---|---|---|---|---|---|---|---|
| Day0 18:28 | 122 | 131 | +9 | 4.0 | 4.4 | +0.4 | plasma 411 |
| Day0 19:46 | 123 | 133 | +10 | 3.9 | 4.3 | +0.4 | plasma 380 |
| Day1 01:58 | 130 | 138 | +8 | 3.4 | 3.6 | +0.2 | POC 220 |
| Day1 15:03 | 133 | 139 | +6 | 3.2 | 3.4 | +0.2 | plasma 281 |
| Day2 04:25–26 | 135 | 139 | +4 | 3.4 | 3.5 | +0.1 | 無（最近 POC 05:00 216、02:50 211） |

**非同時（不可配對）**：
- Day1 05:53：chemistry Na 129 / K 3.6，無 gas。
- Day1 08:34：gas Na 139 / K 3.9，無 chemistry Na/K。
- Day1 17:31：gas Na 138 / K 3.7；chemistry 只有 Cl 102，**無 chemistry Na**（故無法以同一 analyzer 計算 anion gap）。
- Day1 22:39：gas only。
- measured osmolality 318 只有 Day0 18:28 一筆；brief 將其列在 18:28 列，但未說明是否為同一管 specimen（原始 specimen 層級的同時性未確認）。

事實觀察（不作病因結論）：gas − chemistry Na 差距由 +9/+10（Day0）逐步縮小到 +4（Day2）；同期 TG 只有 Day1 17:31 一筆（1950），**無 Day0 TG**；ISE 方法（direct vs indirect）未知。病因判讀（indirect ISE pseudohyponatremia vs translocational hyponatremia）交由 electrolyte-specialist。

## 4. 各指標軌跡（僅列已有數值）
- **Glucose（plasma lab）**：411（D0 18:28）→ 380（D0 19:46）→ 297（D1 05:53）→ 281（D1 15:03）。Day1 17:31 及之後**無 plasma glucose**。
- **Glucose（POC）**：220（D1 01:58）；Day2 181 → 211 → 216 → 214 → 234。POC 與 plasma 方法不同，不宜直接串成同一曲線（D1 01:58 POC 220 → D1 05:53 plasma 297）。
- **glucose 482**：QA 提問者另提，**brief 中無任何對應 lab 時點/數值**；不得用於計算。
- **BOHB**：5.6（D0 18:28）→ 4.2（D1 05:53）；之後**無任何 BOHB**（Day1 05:53 後約 28 小時無 ketone 資料）。
- **pH / HCO3（gas）**：7.316/10.5 → 7.278/11.3 → 7.385/13.4 → 7.313/12.5 → 7.357/15.2 → 7.401/17.0 → 7.386/17.2 → 7.329/21.6（latest，Day2 04:25）。
- **pCO2**：只有 D0 18:28（20.3）與 D2 04:25（40.7）兩筆；其餘未列。
- **K（chemistry）**：4.0 → 3.9 → 3.4 → 3.6 → 3.2（nadir, D1 15:03）→ 3.4（latest, D2 04:25）。
- **Na（chemistry）**：122 → 123 → 130 → 129 → 133 → 135。
- **Ca**：9.3 mg/dL（D0）→ 7.8（D1 08:34）→ 8.2（D1 17:31）→ 7.8（D2 04:25）。
- **Phosphate**：1.3（D1 17:31）→ 1.6（D2 04:25），單位未列；**Day0 無 phosphate**。
- **Mg**：1.9 mg/dL（D1 08:34）→ 2.2（D1 17:31）→ 1.9（D2 04:25）。
- **Renal**：BUN 22 / Cr 1.31 只有 Day0 18:28；**之後無 Cr/BUN**。
- **Albumin**：3.5 g/dL 只有 Day1 08:34。
- **Pancreas**：lipase 57 U/L（D0 18:28，ref <60）；amylase 57（D1 17:31）；TG 1950（D1 17:31）；TG 已知後**無重複 lipase**。

## 5. 單位假設
| 項目 | brief 單位 | 假設 | 理由 / 備註 |
|---|---|---|---|
| **Phosphate 1.3 / 1.6** | **未列** | 主要假設 mg/dL | 換算 mmol/L = mg/dL × 0.3229：**1.3 → 0.42 mmol/L；1.6 → 0.52 mmol/L**（估算） |
| Phosphate（反向情境） | 未列 | 若實為 mmol/L | 反算 mg/dL = mmol/L ÷ 0.3229：1.3 → 4.03 mg/dL；1.6 → 4.96 mg/dL。兩種解讀臨床意義完全相反，**必須以原始 lab 報告單位與 reference range 確認**，下游不得只採其一而不註明。 |
| Ca 7.8 / 8.2 / 7.8 | 未列（Day0 9.3 有標 mg/dL） | mg/dL | 同院 Day0 標示 mg/dL；數值以 mmol/L 解讀生理上不可能。仍屬推定。 |
| Mg 2.2 / 1.9（Day2） | Day1 08:34 有標 mg/dL，其餘未列 | mg/dL | 同上，推定。 |
| Glucose 380/297/281、POC | 只有 411 標 mg/dL | mg/dL | 推定。 |
| Na、K、Cl、HCO3 | 未列 | mmol/L（mEq/L） | 慣例，推定。 |
| pCO2 | 未列 | mmHg | 慣例，推定。 |
| Lactate 0.60 | 未列 | mmol/L | 推定；若為 mg/dL 意義不同。 |
| CRP 0.28 | 未列 | **無法推定**（mg/dL 或 mg/L 皆常見） | 兩者解讀差 10 倍；列為缺口。 |
| Amylase 57 | 未列 | U/L | 推定。 |
| WBC 6.4 | 未列 | ×10³/µL | 推定。 |
| Troponin / CK-MB | 只寫 normal | — | 無數值與單位。 |

## 6. 算術估算（**估算值，非測量值**；供下游核對，不含臨床結論）
公式由 `docs/case-questions.md` 指定；其文獻出處由 evidence-librarian 驗證——本檔對公式出處標 `UNVERIFIED`。

### 6.1 Corrected Na（chemistry Na；Na + k × (glucose − 100)/100）
| 時點 | chem Na | glucose | k = 1.6 | k = 2.4（敏感度） | 備註 |
|---|---|---|---|---|---|
| Day0 18:28 | 122 | 411（plasma） | 127.0 | 129.5 | |
| Day0 19:46 | 123 | 380（plasma） | 127.5 | 129.7 | |
| Day1 01:58 | 130 | 220（**POC**） | 131.9 | 132.9 | glucose 為 POC，與 chemistry Na 非同法，僅參考 |
| Day1 05:53 | 129 | 297（plasma） | 132.2 | 133.7 | |
| Day1 15:03 | 133 | 281（plasma） | 135.9 | 137.3 | |
| Day2 04:25 | 135 | 無 | — | — | 無同時 glucose，**不計算** |
- 不使用 glucose 482（無對應 lab）。不使用 glucose − 180 之類替代公式。
- 若以 gas Na 代入結果不同；下游須明示用哪一個 Na。

### 6.2 Calculated osmolality（Day0 18:28；2Na + glucose/18 + BUN/2.8）
- 以 chemistry Na 122：≈ 274.7 mOsm/kg → 與 measured 318 差 ≈ 43.3（估算 osmolal gap）。
- 以 gas Na 131：≈ 292.7 mOsm/kg → 差 ≈ 25.3。
- 限制：Na 方法（ISE direct/indirect）未知；lipemia 存在；measured osmolality 與 chemistry 是否同一 specimen 未確認；無 ethanol/其他 osmole 資料。osmolal gap 判讀交 electrolyte-specialist。

### 6.3 Albumin-corrected Ca（Ca + 0.8 × (4.0 − albumin)）
- 只有 Day1 08:34 同時有 albumin：Ca 7.8、albumin 3.5 → ≈ 8.2 mg/dL（估算）。
- Day1 17:31（Ca 8.2）、Day2 04:25（Ca 7.8）**無同時 albumin**，不應套用 08:34 albumin 而不註明。
- **無 ionized Ca**；corrected Ca 不能替代 ionized Ca。

### 6.4 Anion gap
- Day0–Day1 15:03：**無 Cl**，無法計算。
- Day1 17:31：只能用 gas Na 138 − chem Cl 102 − gas HCO3 17.0 ≈ 19（**混合 analyzer、混合 specimen，僅示意**）。
- Day2 04:25：無 Cl，無法計算。

## 7. 「提問，非 MAR」項目（不得當作已執行治療）
- glucose 482：QA 作者提及，**無對應 lab**。
- IV insulin 3 → 2 U/hr：QA 作者提問內容，**非確認 MAR**；開始時間、起始劑量、中斷/調整時點皆未知。
- Toujeo（insulin glargine U300）約 10 U：提問內容，**非確認 MAR**；給藥時點、是否已給皆未知。
- NovoRapid（insulin aspart）IV：僅在 QA 題目中出現，是否使用、濃度皆未知。
- K/Ca/P 補充、fluid：**完全無資料**，不能宣稱已補或未補。

## 8. 限制
- 來源僅 `docs/case-questions.md`（case-brief 存取被拒）；未能逐字比對。
- 時刻為 lab 列出時刻，不確定是採檢、報告或 brief 彙整時刻。
- Hemolysis/lipemia 未對應到具體 specimen；任何單點 K/Na 都可能受影響。

## UNVERIFIED 清單
- Corrected Na 係數 1.6/2.4、calculated osmolality、albumin-corrected Ca 公式之文獻出處（本檔未引用 DOI/PMID）。
- Phosphate 單位（mg/dL vs mmol/L）。
- 本檔數值與 `.private/case-brief.md` 的一致性（未比對）。
