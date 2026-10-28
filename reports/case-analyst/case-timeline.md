# Case timeline（去識別，Day0/1/2）— case-analyst 工作檔（當前狀態）

> 只提供事實、同時間點配對、單位與算術估算；**不做治療建議**。時間標記：Day0/1/2 + 時刻；T0 = Day0 18:28（第一筆列出的 lab），**不是** insulin 開始時間（insulin 開始時間未知）。
> 來源：去識別 case brief（含 Codex 對 Day1 22:39 pCO₂ 的精確化 addendum）與使用者 supplement v2（依 supplement v2 更新）。啟動時 case brief 讀取被拒、改用 `docs/case-questions.md` 的歷史已修正，見 [input-validation.md](input-validation.md)；原 bootstrap 版本保留在 Git 歷史。
> 教學用整理版見 [reports/case-timeline.md](../case-timeline.md)；缺口清單見 [data-gaps.md](data-gaps.md)。

## 1. 個案背景
- 男性 40 多歲；肥胖：身高 175 cm、體重 104.5 kg、BMI 34.1（Day1 17:00）；HTN、dyslipidemia 數年。
- 約半年前 borderline glucose，只飲食控制；無 DM drug；無家族 DM 史。
- 約一週：疲倦、食慾差、polydipsia/polyuria/nocturia；含糖運動飲料攝取增加。
- 無明確感染、腹痛、胸痛；chest X-ray 無 active lesion。

## 2. 檢驗主時間軸
「同時配對」：✔ = 同一列時刻有 chemistry 與 blood gas；✘ = 只有一方。Blood gas 一律 **arterial/venous 未知**。血酮為 Blood Ketone Quantitative Test（參考 0–0.6 mmol/L），**很可能是 BOHB，分析物待檢驗科確認**。

| 時點 | T0 起算 | Chemistry / 其他 | Blood gas | 同時配對 |
|---|---|---|---|---|
| Day0 18:28 | T+0:00 | plasma glucose 411；Na 122；K 4.0；BUN 22；Cr 1.31；Ca 9.3；血酮 5.6；measured osmolality 318 mOsm/kg；lipase 57 U/L（ref <60）；CRP 0.28（單位未列）；WBC 6.4 | pH 7.316；pCO₂ 20.3；HCO₃ 10.5；Na 131；K 4.4 | ✔ |
| Day0 19:46 | T+1:18 | glucose 380；Na 123；K 3.9 | pH 7.278；HCO₃ 11.3；Na 133；K 4.3 | ✔ |
| Day1 01:58 | T+7:30 | Na 130；K 3.4；**POC** glucose 220 | pH 7.385；HCO₃ 13.4；Na 138；K 3.6 | ✔（glucose 為 POC） |
| Day1 05:53 | T+11:25 | glucose 297；Na 129；K 3.6；**血酮 4.2（最後一筆）** | — | ✘ chemistry only |
| Day1 08:34 | T+14:06 | HbA1c 13.60%；albumin 3.5 g/dL；Ca 7.8；Mg 1.9 | pH 7.313；HCO₃ 12.5；Na 139；K 3.9 | 部分（無 chemistry Na/K） |
| Day1 15:03 | T+20:35 | glucose 281；Na 133；**K 3.2（nadir）** | pH 7.357；HCO₃ 15.2；Na 139；K 3.4 | ✔ |
| Day1 17:31 | T+23:03 | TG 1950；total CHO 413；HDL 23；direct LDL 52；**Cl 102（無同時 chemistry Na）**；Ca 8.2；**phosphate 1.3 mg/dL（0.42 mmol/L）**；Mg 2.2；lactate 0.60（單位未列）；amylase 57；troponin/CK-MB normal（數值未列） | pH 7.401；HCO₃ 17.0；Na 138；K 3.7 | 部分 |
| Day1 22:39 | T+28:11 | — | pH 7.386；**pCO₂ 28.4**；HCO₃ 17.2；Na 138；K 3.8 | ✘ gas only |
| Day2 01:00–09:04 | T+30:32–38:36 | POC glucose 181（01:00）、211（02:50）、216（05:00）、214（07:00）、234（09:04） | — | ✘ |
| Day2 04:25–04:26 | T+33:57 | Na 135；**K 3.4（latest）**；Ca 7.8；**phosphate 1.6 mg/dL（0.52 mmol/L）**；Mg 1.9；無 plasma glucose、血酮、Cr、albumin | pH 7.329；pCO₂ 40.7；HCO₃ 21.6；Na 139；K 3.5 | ✔（相隔約 1 分鐘） |

來源附註：多筆 lipemia、早期 hemolysis（未指明 specimen）；無 ISE 方法；無 arterial/venous 資料；原始 CBC 重複。glucose 482 為 QA 提問者另提，**無對應 lab**，不得使用。

## 3. 同時間點配對：chemistry vs blood gas Na/K
| 時點 | chem Na | gas Na | Δ(gas−chem) | chem K | gas K | Δ(gas−chem) | 同時 glucose |
|---|---|---|---|---|---|---|---|
| Day0 18:28 | 122 | 131 | +9 | 4.0 | 4.4 | +0.4 | plasma 411 |
| Day0 19:46 | 123 | 133 | +10 | 3.9 | 4.3 | +0.4 | plasma 380 |
| Day1 01:58 | 130 | 138 | +8 | 3.4 | 3.6 | +0.2 | POC 220 |
| Day1 15:03 | 133 | 139 | +6 | 3.2 | 3.4 | +0.2 | plasma 281 |
| Day2 04:25–26 | 135 | 139 | +4 | 3.4 | 3.5 | +0.1 | 無（最近 POC 05:00 216） |

- 非同時：Day1 05:53（chem only）、Day1 08:34 與 22:39（gas only）、Day1 17:31（chemistry 只有 Cl，無 Na）。Measured osmolality 只有 Day0 18:28 一筆，是否同一管 specimen 未確認。
- 事實觀察：gas − chem Na 差距由 +9/+10 縮小到 +4；TG 只有 Day1 17:31 一筆；ISE 方法未知。（判讀見 §10）

## 4. 各指標軌跡
- **Glucose（plasma）**：411 → 380 → 297 → 281（Day1 15:03）；之後只有 POC。POC 與 plasma 方法不同，不宜直接串成同一曲線。
- **血酮**：5.6（Day0）→ 4.2（Day1 05:53）；之後**沒有任何血酮**，Day0 的 5.6 不是最新值。
- **pH / HCO₃**：7.316/10.5 → 7.278/11.3 → 7.385/13.4 → 7.313/12.5 → 7.357/15.2 → 7.401/17.0 → 7.386/17.2 → 7.329/21.6（latest）。
- **pCO₂**：20.3（Day0 18:28）→ 28.4（Day1 22:39）→ 40.7（Day2 04:25）；其他時點 brief 未列；檢體類型未知。
- **K（chemistry）**：4.0 → 3.9 → 3.4 → 3.6 → 3.2（nadir）→ 3.4（latest）。
- **Na（chemistry）**：122 → 123 → 130 → 129 → 133 → 135。
- **Ca**：9.3 → 7.8 → 8.2 → 7.8 mg/dL；albumin 只有 Day1 08:34 的 3.5；無 ionized Ca。
- **Phosphate**：1.3 → 1.6 mg/dL（換算 0.42 → 0.52 mmol/L）；Day0 無 phosphate。
- **Mg**：1.9 → 2.2 → 1.9 mg/dL。
- **Renal**：BUN 22 / Cr 1.31 只有 Day0；之後無 Cr/BUN。
- **Pancreas**：lipase 57（Day0）；amylase 57、TG 1950（Day1 17:31）；TG 已知後無重複 lipase。

## 5. 體型、生命徵象、進食與部分 I/O（supplement v2）
| 時點 | BP | HR | RR | T (°C) |
|---|---|---|---|---|
| Day1 17:00 | 137/81 | 84 | 14 | 36.2 |
| Day1 19:01 | 131/67 | 79 | 17 | 35.5 |
| Day1 21:01 | 103/70 | 94 | 30 | 36.0 |
| Day1 23:01 | 134/72 | 85 | 20 | 36.1 |
| Day2 01:01 | 133/62 | 83 | 17 | 36.7 |
| Day2 03:01 | 117/53 | 83 | 19 | 36.5 |
| Day2 05:01 | 135/83 | 84 | 16 | 36.6 |
| Day2 07:01 | 150/80 | 90 | 17 | 36.3 |
| Day2 09:01 | 149/86 | 85 | 18 | 35.7 |

- 進食：Day1 18:00 乾飯 243、Day2 07:24 稀飯 270（固體，單位未列）。
- 部分 I/O（非完整 24 h；需確認各筆為獨立區間量而非累計）：Day1 21:00 口服 60 mL、21:44 尿 1100、22:43 口服 450、22:46 IV 177（欄位標 RI）、22:47 IV 1000；Day2 06:06 IV 1000、尿 950、06:07 IV 209、07:40 口服 50。
- 條件式算術（若無重複）：IV 2386 + 口服液體 560 = 2946 mL；尿 2050 mL；片段差 +896 mL。固體不計入；不是 24 h net；不換算 mL/kg/h 尿量。IV 1000 是容量不是 mL/h；RI 177、IV 209 不是 insulin 單位，也不確定來自 insulin 點滴袋。

## 6. 單位
| 項目 | 狀態 | 備註 |
|---|---|---|
| Na、K、Cl | **使用者確認** mEq/L | 單價離子數值同 mmol/L |
| Ca、phosphate | **使用者確認** mg/dL | P mmol/L = mg/dL × 0.3229 |
| HCO₃ | 推定 mmol/L | 慣例 |
| Glucose（含 POC） | 411 有標 mg/dL，其餘推定 mg/dL | |
| Mg | Day1 08:34 有標 mg/dL，其餘推定 | |
| pCO₂ | 推定 mmHg | 慣例 |
| 血酮 | mmol/L（參考 0–0.6） | 分析物待確認 |
| Lactate 0.60 | 未列，推定 mmol/L | |
| CRP 0.28 | **無法推定**（mg/dL 或 mg/L） | 差 10 倍，列為缺口 |
| Amylase | 推定 U/L | |
| Troponin / CK-MB | 只寫 normal | 無數值與單位 |

## 7. 算術估算（**估算值，非測量值**；不含臨床結論）
- **Corrected Na**（Na + k × (glucose − 100)/100；k = 1.6，2.4 為敏感度；不用 glucose − 180、不用 482）：

  | 時點 | Na | glucose | k = 1.6 | k = 2.4 |
  |---|---|---|---|---|
  | Day0 18:28 gas | 131 | 411 | 136.0 | 138.5 |
  | Day0 18:28 chem | 122 | 411 | 127.0 | 129.5 |
  | Day0 19:46 chem | 123 | 380 | 127.5 | 129.7 |
  | Day1 05:53 chem | 129 | 297 | 132.2 | 133.7 |
  | Day1 15:03 chem | 133 | 281 | 135.9 | 137.3 |

  Day1 01:58 只有 POC glucose、Day2 04:25 無同時 glucose，不計算。
- **Calculated osmolality**（Day0 18:28；2Na + glucose/18 + BUN/2.8）：gas Na 131 → 292.7（gap 25.3）；chem Na 122 → 274.7（gap 43.3）。Effective osmolality：284.8 / 266.8。
- **Albumin-corrected Ca**：只有 Day1 08:34 可算（7.8 → 8.2）；其他時點無同時 albumin；無 ionized Ca。
- **Anion gap**：只有 Day1 17:31 能混用 gas Na 138 − Cl 102 − gas HCO₃ 17.0 ≈ 19（跨 analyzer，僅示意）。
- **Insulin**：50 U ÷ 500 mL = 0.1 U/mL；20 / 30 mL/h = 2 / 3 U/h = 0.0191 / 0.0287 U/kg/h（104.5 kg）。

## 8. 醫囑與給藥狀態（醫囑**無開立時間、無 MAR**；order ≠ 已給）
- **Insulin**：使用者確認 50 U／500 mL、曾 20–30 mL/h、該次紀錄當下 2 U/h。醫囑顯示 NovoRapid FlexPen 300 IU 商品名、50 IU ST 加入點滴瓶；實際產品與藥局配製待核對，不直接判定給藥錯誤。
- **K**：KCl in NS 20 mEq/500 mL 1 btl ST；K-Glu（potassium gluconate）20 mEq/15 mL，15 mL QID（order 面 80 mEq/day）＋15 mL ST。QID、口服 ST 20 與 IV 20 不可在沒有 MAR 時加總為實際已給 120 mEq/day。
- **Ca**：Calcium Chloride 400 mg/20 mL 2 amp ST IV；800 mg 是製劑量，不等於 800 mg 元素鈣。
- **輸液**：LR 500 mL × 4 btl QD；NS 500 mL QD；NS 500 mL ST。
- **長期口服**：β-blocker、含 ARB 降壓複方、fibrate、另一項非 DKA 相關口服藥。
- 貼出的醫囑片段**未見** phosphate、Mg、dextrose、bicarbonate 製劑（片段不代表完整醫囑沒有）。
- **Toujeo 約 10 U**：仍只是 QA 提問，**不是醫囑或 MAR**。

## 9. 限制
- 時刻為 lab 列出時刻，不確定是採檢、報告或彙整時刻。
- Hemolysis/lipemia 未對應到具體 specimen；任何單點 K/Na 都可能受影響。
- 醫囑沒有時間，不放進任何特定 Day。
- 本檔不引用文獻；公式出處見 electrolytes／fluid-insulin 報告與 evidence register。

## 10. 衍生判讀（非事實紀錄；依據與來源詳見 [電解質報告](../electrolytes.md)、[輸液與 insulin 報告](../fluid-insulin.md)）
以下為兩份有來源報告中的判讀摘要，放在此處只為方便續讀；不新增臨床建議。
- **Na 差距縮小**：可能與血糖下降、干擾減少或實際水與鈉平衡變化有關；沒有同時段 direct-ISE Na 與 TG，無法歸因（[電解質報告 §2.4](../electrolytes.md)）。
- **pCO₂ 與酸鹼**：Day1 22:39 → Day2 04:25 pH 下降但 HCO₃ 與 pCO₂ 上升，不是代謝性酸中毒惡化；檢體類型未知（[輸液與 insulin 報告 §2.4](../fluid-insulin.md)）。
- **Phosphate**：0.42 → 0.52 mmol/L 屬中度低磷；是否補充依症狀條件（[電解質報告 §1.4](../electrolytes.md)）。
- **Corrected Ca**：不能替代 ionized Ca（[電解質報告 §1.4](../electrolytes.md)）。
- **Anion gap**：2024 共識不以 AG 判定 resolution（[輸液與 insulin 報告 §2.3](../fluid-insulin.md)）。
- **Insulin 速率**：0.05 U/kg/h 參考換算 5.225 U/h；低於參考不能單獨作為增速理由，K 3.4 與最新血酮未知是限制（[輸液與 insulin 報告 §3.3](../fluid-insulin.md)）。
- **生命徵象與進食**：不能據此確定意識狀態或 DKA 緩解（[輸液與 insulin 報告 §2](../fluid-insulin.md)）。
