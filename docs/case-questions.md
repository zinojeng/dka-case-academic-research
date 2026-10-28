# 個案問題與去識別時間軸（portable case example）

> 來源：`.private/case-brief.md`（已去識別）。只用 Day0/1/2 + 時刻；無病歷號、真實日期、醫師、地點。可公開重現。

## 個案摘要
男性 42 歲，肥胖（無 height/weight/BMI），HTN/dyslipidemia 數年；半年前 borderline glucose 只飲食控制，無 DM drug，無家族 DM。約一週疲倦、食慾差、polydipsia/polyuria/nocturia、含糖運動飲料增加；無明確感染、腹痛、胸痛。胸片無 active lesion。

## 時間軸
| 時點 | Chemistry / 其他 | Blood gas（arterial/venous 未知） |
|---|---|---|
| Day0 18:28 | plasma glucose 411 mg/dL, Na 122, K 4.0, BUN 22 mg/dL, Cr 1.31 mg/dL, Ca 9.3 mg/dL; BOHB 5.6 mmol/L; measured osmolality 318 mOsm/kg; lipase 57 U/L (<60), CRP 0.28, WBC 6.4 | pH 7.316, pCO2 20.3, HCO3 10.5, Na 131, K 4.4 |
| Day0 19:46 | glucose 380, Na 123, K 3.9 | pH 7.278, HCO3 11.3, Na 133, K 4.3 |
| Day1 01:58 | Na 130, K 3.4; POC glucose 220 | pH 7.385, HCO3 13.4, Na 138, K 3.6 |
| Day1 05:53 | glucose 297, Na 129, K 3.6, BOHB 4.2 | — |
| Day1 08:34 | HbA1c 13.60%, albumin 3.5 g/dL, Ca 7.8, Mg 1.9 mg/dL | pH 7.313, HCO3 12.5, Na 139, K 3.9 |
| Day1 15:03 | glucose 281, Na 133, K 3.2 | pH 7.357, HCO3 15.2, Na 139, K 3.4 |
| Day1 17:31 | TG 1950 mg/dL, total CHO 413, HDL 23, direct LDL 52（calculated LDL unavailable）; Cl 102（無同時 chemistry Na）; Ca 8.2, phosphate 1.3（**單位未列**）, Mg 2.2; lactate 0.60, amylase 57; troponin/CK-MB normal | pH 7.401, HCO3 17.0, Na 138, K 3.7 |
| Day1 22:39 | — | pH 7.386, HCO3 17.2, Na 138, K 3.8 |
| Day2 04:25–04:26 | Na 135, K 3.4, Ca 7.8, phosphate 1.6（**單位未列**）, Mg 1.9 | pH 7.329, pCO2 40.7, HCO3 21.6, Na 139, K 3.5 |
| Day2 POC glucose | 01:00 181; 02:50 211; 05:00 216; 07:00 214; 09:04 234 | — |

備註：多筆 lipemia，早期 hemolysis；無 ISE 方法、arterial/venous 資料；原始 CBC 重複。
QA 作者另提 glucose 482 但**無對應 lab**；IV insulin 3→2 U/hr 與 Toujeo 約 10 U 是**提問，非確認 MAR**。

**資料缺口（不可補造）**：MAR、補 K/Ca/P 醫囑、fluid 種類/速率/總量、weight/vitals/UO/mental status、ionized Ca、latest Cr/BOHB、C-peptide/autoantibodies。

## 必須回答
### QA1 Calcium / Phosphate
Ca 7.8、albumin 3.5；phosphate 1.3→1.6 未列單位 → 明示 mg/dL 假設與 mmol/L 換算（mg/dL × 0.3229）。沒有 MAR 不能宣稱已補或沒補。討論 ionized Ca、症狀、DKA phosphate RCT、補磷引起 hypocalcemia。

### QA2 Sodium
同時 chemistry Na 122 vs gas Na 131、glucose 411（482 無對應 lab）、TG 1950。分開 indirect ISE pseudohyponatremia 與 hyperglycemic translocational hyponatremia。corrected Na = Na + 1.6 × (glucose − 100)/100，並給 2.4 敏感度；不可用 glucose − 180。measured osmolality 318、BUN 22：釐清 osmolal gap、方法與 same-time 限制；corrected Na 不是測量真值。cerebral edema vs osmotic demyelination。

### QA3 Potassium
nadir 3.2、latest 3.4；核對 2024 consensus 原文：K < 3.5 先補 K 並延後/暫停 insulin until > 3.5。ECG、renal、urine output、IV access 的 rate/concentration 院規；oral 並非永遠禁用；勿在無資料下開個人化處方。

### QA4 Fluids
0.9% saline vs balanced/Ringer lactate 證據、0.45% 的情境、hyperchloremic NAGMA；缺 I/O、weight、vitals、renal/heart 資料不判實際量；比較 trial 硬終點的限制。

### QA5 Insulin / resolution / transition
glucose 211–234 不能單獨作為停滴依據；latest ketone 4.2 是較早的 Day1；latest pH 7.329 / HCO3 21.6；無 latest BOHB 不能宣稱 resolved。2024 resolution：BOHB < 0.6 mmol/L AND (pH ≥ 7.3 OR HCO3 ≥ 18)，glucose ideally < 200；不用 BE/anion gap/urine ketone 判 resolution。glucose < 250 加 dextrose 續 insulin 直到 ketosis 解除；劑量依體重情境而非固定 2–3 U/hr。2024 overlap 1–2 h vs 2026 2–4 h 需並列原文說清楚；Toujeo U300 onset/steady-state 依 label，不能直接套常規 overlap；NovoRapid（aspart）IV 依 label 與濃度核對，不自動當 regular。

### 延伸
- HbA1c 13.6% 代表 chronic hyperglycemia；肥胖 DKA 首發可考慮 KPD，需恢復後 C-peptide/autoantibodies，不逕診。
- TG 1950 的 pancreatitis 風險；lipase 57 且無腹痛不支持已發生，但不能絕對排除。

## 必查文獻
- 2024 hyperglycemic crises consensus — DOI 10.2337/dci24-0032
- ADA Standards of Care 2026, Section 16 — DOI 10.2337/dc26-s016
- 以及當前 literature 與 drug label（需記錄 query/date/DOI/PMID/取得方式/locator/限制）
