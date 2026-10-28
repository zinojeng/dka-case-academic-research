# 電解質專題報告：Calcium/Phosphate、Sodium/Tonicity/Cerebral effects、Potassium（QA1–QA3）

- 作者角色：electrolyte-specialist（Claude Code Opus 5.5 session「DKA electrolytes Opus55」）
- 依據：僅 `.private/case-brief.md`（去識別摘要）＋公開文獻；未讀原始病歷。時間以 Day0/1/2 表示。
- 格式：每題依「臨床問題 → 已知事實 → 證據 → 個案應用 → 缺漏資料」。
- 重要前提：**病歷中沒有 medication administration record（MAR）、補 K/Ca/P 醫囑、輸液種類/速率/總量、體重、vital signs、urine output（UO）、意識狀態**。因此本報告：
  1. 不宣稱任何電解質「已補」或「未補」——「沒有記錄」≠「沒有給」；
  2. 不給個人化劑量／速率處方，只提供決策框架與需先確認的資料。
- QA 原文提到 glucose 482 mg/dL：case brief 中**無對應 lab**，本報告不採用。

---

## 0. 文獻來源與定位（已核對）

| # | 文獻 | 識別碼 | 取得狀態（本 session） | 本報告使用的 locator |
|---|---|---|---|---|
| [1] | Umpierrez GE, et al. Hyperglycemic Crises in Adults With Diabetes: A Consensus Report. *Diabetes Care* 2024;47(8):1257–1275 | DOI 10.2337/dci24-0032；PMID 39052901；PMC11272983 | PMC HTML 以 WebFetch 讀取（摘錄性回答，非全文下載）；diabetesjournals.org 403 | Section 4 "Potassium"、"Phosphate"、"Fluid therapy"、"Criteria for resolution"；phosphate 閾值文字確認為 "<1.0 mmol/L" |
| [1b] | 同上共同出版：*Diabetologia* 2024;67(8):1455–1479 | DOI 10.1007/s00125-024-06183-8；PMID 38907161；PMC11343900（CC BY 4.0） | Europe PMC fullTextXML 下載成功（scratch，非 evidence/）；出版社 ESM slideset（pptx）取得並**目視**判讀 Fig 4 | Section 3（Table 2）、Section 4 各小節、Section 5 Table 3、Fig 4（slideset slide 4，影像無文字層） |
| [2] | Kitabchi AE, et al. Hyperglycemic crises in adult patients with diabetes. *Diabetes Care* 2009;32:1335–1343 | DOI 10.2337/dc09-9032；PMC2699725 | Europe PMC fullTextXML 全文（**僅本 session 讀取**；evidence-librarian 登錄為 S19 metadata-only → single-session verified、未經獨立再現） | "Potassium"、"Phosphate"、"Diagnosis/Laboratory findings"、Fig 2 註腳 |
| [3] | ADA. 16. Diabetes Care in the Hospital: Standards of Care in Diabetes—2026. *Diabetes Care* 2026;49(Suppl 1):S339–S355 | DOI 10.2337/dc26-S016；PMC12690180 | PMC HTML WebFetch（前 100k 字元）；Europe PMC XML 500 | Rec 16.16–16.17；DKA/HHS 段落；Fig 16.1 僅 alt text 可得，K 閾值數值**未能核對** |
| [4] | Fisher JN, Kitabchi AE. A randomized study of phosphate therapy in the treatment of DKA. *J Clin Endocrinol Metab* 1983;57:177–180 | PMID 6406531；DOI 10.1210/jcem-57-1-177 | 本 session abstract-only；evidence-librarian 已取得全文並 parse（register S09） | Abstract；全文 Results p178–179、Table 1–2（librarian 回報） |
| [5] | Wilson HK, et al. Phosphate therapy in diabetic ketoacidosis. *Arch Intern Med* 1982;142:517–520 | PMID 6802095 | abstract-only | Abstract |
| [6] | Katz MA. Hyperglycemia-induced hyponatremia—calculation of expected serum sodium depression. *N Engl J Med* 1973;289:843–844 | PMID 4763428 | 書目資料（無 abstract） | — |
| [7] | Hillier TA, Abbott RD, Barrett EJ. Hyponatremia: evaluating the correction factor for hyperglycemia. *Am J Med* 1999;106:399–403 | PMID 10225241 | 本 session abstract-only；evidence-librarian 已取得全文並 parse（register S11） | Abstract；全文 Results（librarian 回報） |
| [8] | Davidson DF. Excess osmolal gap in diabetic ketoacidosis explained. *Clin Chem* 1992;38:755–757 | PMID 1582030 | abstract-only | Abstract |
| [9] | Fortgens P, Pillay TS. Pseudohyponatremia revisited: a modern-day pitfall. *Arch Pathol Lab Med* 2011;135:516–519 | PMID 21466372；DOI 10.5858/2010-0018-RS.1 | 書目資料（未讀全文） | 僅作背景 |
| [10] | Dimeski G, et al. Disagreement between ion selective electrode direct and indirect sodium measurements. *J Crit Care* 2012;27:326.e9–16 | PMID 22227082；DOI 10.1016/j.jcrc.2011.11.003 | 書目資料（未讀全文） | 僅作背景 |
| [11] | Chopra P, et al. Impact of total protein and triglycerides on the comparability of Na and K measurements by direct and indirect ISE（實驗分析研究）. *EJIFCC* 2026;37(4):696–709 | PMID 42729988 | abstract-only | Abstract |
| [12] | Arora S, et al. Prevalence of hypokalemia in ED patients with DKA. *Am J Emerg Med* 2012;30:481–484 | PMID 21316179；DOI 10.1016/j.ajem.2011.01.002 | abstract-only | Abstract |
| [13] | Desgagnés N, et al. Use of albumin-adjusted calcium measurements in clinical practice. *JAMA Netw Open* 2025;8:e2455251 | PMID 39836424；DOI 10.1001/jamanetworkopen.2024.55251 | abstract-only | Abstract |
| [14] | Pasquel FJ, et al. Clinical outcomes in patients with isolated or combined DKA and HHS. *Diabetes Care* 2020;43:349–357 | PMID 31704689；PMC6971788 | 經 [1b] 引用（未獨立讀全文） | 作為 [1b] 的引文 |

> 全文下載／LlamaParse／evidence register 由 evidence-librarian 負責；本 session 只把來源 locator 傳給 librarian，未寫入 `evidence/`、`fulltext/`、`parsed/`。
> JBDS 2022 DKA guideline（DOI 10.1111/dme.14788）非 OA，本 session 未讀全文，**不引用其 K 表格數值**。

### 0.1 2024 共識：本文 vs Fig 4 vs 2009 的差異（只記錄，不以猜測統一）

| 項目 | 2024 本文（[1]/[1b] §Potassium、§Phosphate、§Resolution；**主要決策依據**） | 2024 Fig 4（[1b] slideset slide 4，**單一 session 目視、未經獨立再現**） | 2009 共識 [2]（**single-session verified**） |
|---|---|---|---|
| K <3.5 時 K 補充速率 | 以 **10 mmol/h** 開始補 K（意譯） | K⁺ <3.5 時給 **10–20**（圖上單位印成 mmol·L⁻¹·h⁻¹，語意應為 mmol/h，但原圖如此）直到 K⁺ >3.5；更快的補充需經 central venous access（意譯） | 補 K 應與輸液治療同時開始（意譯） |
| K <3.5 時 insulin | insulin 應**延後到 K 升至 >3.5 mmol/L**（語境：入院時 K 即低，約占 DKA 的 5–10%）（意譯） | **圖中無「hold insulin」字樣**；只有 K⁺ >5.0 分支註明開始 insulin 但不給 K⁺；K 欄最上方先要求確認腎功能足夠（urine output 約 0.5 mL/kg/h）（意譯） | insulin 應延後到 K 回升至 **>3.3 mEq/L**（意譯） |
| K 3.5–5.0 維持量 | 每公升 IV fluid 加 **20–30 mmol** K 通常足夠；目標 4–5 mmol/L（意譯） | 每公升 IV fluid 視需要加 **10–20 mmol** K⁺，使 serum K⁺ 維持在 4–5 mmol/L（意譯） | 20–30 mEq/L；目標 4–5 |
| K 監測 | 開始 insulin 後 2 h 測 serum K，之後每 4 h 測一次直到 DKA resolution；Table 3 亦為每 4 h（意譯） | K⁺ >5.0 分支每 2 h 測 K；圖底部註明電解質每 2–4 h 測至穩定（意譯） | — |
| Phosphate 給予閾值 | 除非有 muscle weakness（如呼吸或心臟受損）且 phosphate **<1.0 mmol/L**，否則不常規補磷（意譯） | 除非同時有 muscle weakness、respiratory compromise 且 phosphate **<1.0 mmol/L**，否則不給（意譯） | serum phosphate **<1.0 mg/dL**（另列 cardiac dysfunction、anemia、respiratory depression）（意譯） |
| DKA resolution | ketone <0.6 且 venous pH **≥**7.3 或 HCO₃ **≥**18 | 註腳 b：pH **>**7.3 或 bicarbonate **>**18 | pH >7.30；HCO₃ >18 |

**解讀註記**：
- 2024 phosphate 閾值 1.0 **mmol/L ≈ 3.1 mg/dL**，比 2009 的 1.0 **mg/dL ≈ 0.32 mmol/L** 寬鬆約 3 倍。S02 正文即寫 mmol/L（Diabetes Care 版與 Fig 4 亦同），**不可推定 2024 單位寫錯**；兩版差異的原因無法判定。建議在院內 protocol 中明文寫出採用的閾值與單位。
- K 補充速率在本文寫 10 mmol/h、Fig 4 寫 10–20；維持量在本文寫 20–30 mmol/L、Fig 4 寫 10–20 mmol/L。**以 S02 正文為主要決策依據**；Fig 4 只是單一 session 的影像目視判讀，尚未獨立再現。實際速率與濃度應依院內 IV potassium policy（周邊／中心靜脈、輸注幫浦、ECG monitoring）。
- 2009 共識 [2] 的引述由本 session 讀 XML 取得，evidence-librarian 只有 metadata（S19），因此屬 single-session verified，**不視為兩個獨立來源都確認**。
- ADA 2026 [3] 的 Fig 16.1 含 "potassium supplementation thresholds"（依 alt text），但數值本 session **未能文字核對**，不引用其數字。

---

## QA1. Calcium / Phosphate

### 1.1 臨床問題
1. Ca 7.8 mg/dL、albumin 3.5 g/dL 算低血鈣嗎？corrected Ca 可信嗎？
2. Phosphate 1.3 → 1.6（未列單位）代表什麼？要補嗎？
3. 能否說「已補磷所以 Ca 下降」或「沒有補」？
4. 補磷相關 RCT 與 hypocalcemia 風險為何？

### 1.2 已知事實（case brief）
| 時間 | Total Ca (mg/dL) | Albumin (g/dL) | Phosphate（單位未列） | Mg (mg/dL) |
|---|---|---|---|---|
| Day0 18:28 | 9.3 | — | — | — |
| Day1 08:34 | 7.8 | 3.5 | — | 1.9 |
| Day1 17:31 | 8.2 | — | 1.3 | 2.2 |
| Day2 04:25 | 7.8 | — | 1.6 | 1.9 |

- 無 ionized Ca、PTH、25-OH vitamin D、症狀（paresthesia、Chvostek/Trousseau、tetany）、ECG QTc、呼吸肌力等資料。
- 無補 Ca/P/Mg 的醫囑或 MAR；無輸液內容（例如是否含 potassium phosphate）。
- 多筆 lipemia（TG 1950 mg/dL, Day1 17:31）；lipemia 可能干擾比色法分析，實際干擾程度依檢驗系統而定（本 session 未取得該院方法資料）。

### 1.3 證據
- **補磷不常規**：2024 共識 §Phosphate [1][1b]（意譯）：除非有 muscle weakness（如呼吸或心臟受損）且 phosphate <1.0 mmol/L，否則不建議常規補磷；補磷過快可能誘發 hypocalcaemia；確有需要時，可在補充液中加入 20–30 mmol potassium phosphate。
- **RCT**：
  - Fisher & Kitabchi 1983 [4]：n=30（15 vs 15），phosphate 8.5 mmol/h（約 6 g/24 h）vs 無。到達 glucose 250、HCO₃ >15、pH >7.3 與意識恢復的時間無差異；**補磷組 plasma ionized calcium 顯著較低**。作者結論是需謹慎使用。依 evidence-librarian 的全文核對（S09）：對照組給 KCl；baseline Pi 以 mg/dL 報告（Table 1）；recovery 指標無差異（Table 2）。全文 Results（p178）指出**兩組在治療過程中 total Ca 都下降、組間 total Ca 無顯著差異**；ionized Ca 只在 hyperlipidemia 不干擾、可測得的 **13 人（7+6）** 中分析，補磷組 24 h 時較低，無 tetany。因此 **total Ca 下降本身不能用來反推曾經補磷**。此外，全文圖表的 parsed 數字是 LlamaParse 從圖估計的，不可引用。
  - Wilson 1982 [5]：n=44，三組（無補、第 4 h 15 mmol、2/6/10 h 共 45 mmol sodium phosphate）。45 mmol 可防止嚴重低磷（1 例例外），但 DKA 持續時間、insulin 需求、muscle enzyme、morbidity/mortality 均無差異。
  - 兩者樣本小、年代早、非現代 protocol；屬「無證據顯示有益」而非「證明無害或有害」。
- **2009 共識 [2] §Phosphate**（意譯；single-session verified）：閾值 <1.0 mg/dL，並列 cardiac dysfunction、anemia、respiratory depression；提醒過度積極補磷可導致嚴重 hypocalcemia；一般認為安全的最大補充速率為 4.5 mmol/h。
- **Corrected Ca 的限制**：Desgagnés 2025 [13]（n=22,658，同時測 total 與 ionized Ca）中，**未校正 total Ca 與 ionized Ca 的相關性反而高於 simplified Payne**（R² 71.7% vs 68.9%）；分類一致率 74.5% vs 58.7–63.0%；低白蛋白時誤分類更嚴重。此研究非 DKA/ICU 族群，但足以支持「albumin-corrected Ca 不能單獨作為判讀依據」。
- **生理（教科書層級，非單一文獻）**：酸血症時 albumin 結合 Ca 減少、ionized fraction 上升；酸中毒矯正後 ionized Ca 會下降。補 bicarbonate 或磷、大量輸液稀釋、hypomagnesemia 都會影響 Ca。

### 1.4 個案應用
1. **Corrected Ca（Payne，僅供參考）**：Day1 08:34 為 7.8 + 0.8×(4.0−3.5) = **8.2 mg/dL**。若沿用同一 albumin 套到 Day1 17:31（8.2 → 8.6）或 Day2（7.8 → 8.2），等於假設 albumin 不變，屬**未驗證假設**。
   → 結論：數值落在「輕度偏低或臨界」，**不足以診斷或排除真正 hypocalcemia**；需 **ionized Ca**（最好 blood gas analyzer 同時測，並註明 pH 校正與否）。
2. **Ca 9.3 → 7.8 的可能解釋**（無法排序，缺資料）：輸液稀釋與 albumin 變化（Day0 無 albumin）、酸中毒矯正後蛋白結合改變（影響 ionized，不直接改變 total）、若曾補磷則可能 Ca-P 結合（[4] 補磷組 iCa 較低，但兩組 total Ca 都下降且無差異）、lipemia 干擾、真實 hypocalcemia（Mg 正常，Mg 缺乏不像主因）。**無 MAR，不能用 Ca 下降反推給過磷。**
3. **Phosphate 單位的條件式解讀**（換算：mg/dL × 0.3229 = mmol/L；1.0 mmol/L ≈ 3.10 mg/dL）：

   | 假設單位 | 1.3 | 1.6 | 意義 |
   |---|---|---|---|
   | **mg/dL**（台灣多數實驗室慣用，但**需檢驗科確認**） | 0.42 mmol/L | 0.52 mmol/L | 中度低磷（一般成人參考約 2.5–4.5 mg/dL）。低於 2024 閾值 1.0 mmol/L，但**高於** 2009 閾值 1.0 mg/dL |
   | mmol/L | 4.03 mg/dL | 4.96 mg/dL | 正常至偏高，則無低磷問題 |

   - 在 mg/dL 假設下，依 2024 文字，是否補磷取決於**是否有 muscle weakness / respiratory or cardiac compromise**。case brief **沒有**這些評估資料，所以無法判定「需要補」或「不需要補」。依 2009 的 <1.0 mg/dL 標準則未達門檻。
   - 1.3 → 1.6 的上升可能是自發恢復（insulin 早期磷進入細胞，之後再分布或飲食恢復）、曾給含磷製劑，或檢驗變異。**沒有 MAR，不能推論「已補」或「沒補」**。
4. **補磷時的 Ca 風險**：此個案 total Ca 已偏低、iCa 未知，若臨床決定補磷（例如出現無力或呼吸問題），應先取得 iCa，並注意速率（[2] 提及 4.5 mmol/h 為一般認為安全之上限、[4] 顯示補磷組 iCa 下降）。具體劑量依院規與體重，**本報告不給個人化處方**。

### 1.5 缺漏資料（需補）
- **Ionized Ca**（含採檢時 pH）、重複 albumin、Mg 趨勢、PTH／25-OH D（若 iCa 持續低）。
- Phosphate **單位與參考區間**（向檢驗科確認）。
- 症狀與徵象：肌力、呼吸（呼吸次數、潮氣量）、心衰竭徵象、溶血或橫紋肌溶解（CK）、ECG QTc。
- MAR：是否曾給 potassium phosphate、calcium gluconate、Mg、bicarbonate；輸液種類與量。
- 腎功能趨勢（只有 Day0 Cr 1.31 mg/dL）。

---

## QA2. Sodium / Tonicity / Cerebral effects

### 2.1 臨床問題
1. Day0 18:28 同時採檢的 chemistry Na 122 與 gas Na 131 相差 9 mmol/L，是哪一種 hyponatremia？
2. 如何計算 corrected Na（1.6 與 2.4）、calculated／effective osmolality 與 osmolal gap，而不混用不同時間、不做兩次校正？
3. 是否符合 HHS？是否需擔心 cerebral edema 或 osmotic demyelination syndrome（ODS）？

### 2.2 已知事實
| 時間 | Lab glucose (mg/dL) | Chem Na | Gas Na | Chem−Gas | 其他 |
|---|---|---|---|---|---|
| Day0 18:28 | 411 | 122 | 131 | −9 | BUN 22、measured osmolality 318 mOsm/kg、BOHB 5.6、pH 7.316、HCO₃ 10.5 |
| Day0 19:46 | 380 | 123 | 133 | −10 | pH 7.278、HCO₃ 11.3 |
| Day1 01:58 | （僅 POC 220） | 130 | 138 | −8 | — |
| Day1 05:53 | 297 | 129 | — | — | BOHB 4.2 |
| Day1 15:03 | 281 | 133 | 139 | −6 | — |
| Day2 04:25 | （無同時 lab glucose） | 135 | 139 | −4 | — |

- TG 1950 mg/dL 是 **Day1 17:31**（非 Day0 同時）；brief 註明「多筆 lipemia」。Albumin 3.5（不支持高蛋白造成的 pseudohyponatremia）。
- **無 ISE 方法資料**（中央 chemistry 是否 indirect ISE、blood gas 是否 direct ISE），也無 gas 為動脈或靜脈的資料。
- QA 所提 glucose 482 無對應 lab，不納入計算。

### 2.3 證據
- **Pseudohyponatremia（假性低血鈉）**：indirect ISE 先稀釋檢體，並假設 plasma water 約 93%。若 lipid 或蛋白占體積增加（water fraction 降低），會**低估** Na；direct ISE 測 plasma water 中的活性，不受此影響 [9][10]。2009 共識 [2]（single-session verified）指出：嚴重 chylomicronemia 時，DKA 可能出現 pseudonormoglycemia 與 pseudohyponatremia（意譯）。
  - Chopra 2026 [11]（S15，abstract-only；實驗加入 Intralipid）：TG **>2000 mg/dL** 時 indirect ISE 的 Na 顯著低估；但在 multivariable model 中，**total protein 是最強的預測因子，TG 的貢獻很小**；K 幾乎不受影響。本例只有 albumin 3.5，沒有 total protein；TG 是 Day1 才測。因此本研究**不能**用來量化本例 lipemia 對 Na 的影響。
- **Translocational（hypertonic）hyponatremia**：高血糖把細胞內水拉到細胞外而稀釋 Na，屬「真的低 Na 但不是低張」。
  - Katz 1973 [6]：每 100 mg/dL glucose 上升，Na 下降 1.6 mmol/L（理論推導）。
  - Hillier 1999 [7]（n=6 健康人，somatostatin + dextrose 至 >600 mg/dL）：平均 **2.4**；關係非線性，≤400 mg/dL 時 1.6 適用，>400 mg/dL 時 4.0 較佳。樣本極小、非 DKA 病人，因此 2.4 只能當**敏感度分析**。全文核對（evidence-librarian S11）：線性斜率 −2.4±0.3（vs 1.6，p=0.02）；Results 的分段斜率轉折點約在 **~440 mg/dL**，abstract 寫 400（登錄為差異 D6）。Na 以 **flame photometry** 測定；限制包括 somatostatin 可能影響 ADH，且受試者無脫水。
  - Na 測定方法的其他文獻（librarian 回報，abstract-only，見 evidence/source-register.json）：Vera 2022 Lab Med（無 lipemia 時 direct 與 indirect ISE 一致）；Evenepoel 2022（direct ISE 不受 TG 影響；某實驗室的工作閾值為 TG 1500 mg/dL）。
  - 2024 共識 [1b] §Fluid therapy（HHS 語境，意譯）：glucose 每下降 5.6 mmol/L（100 mg/dL），Na 約上升 1.6 mmol/L；並強調初期 serum Na 上升本身不是給低張液的理由。2009 [2] 亦採 1.6。
  - **公式基準為 (glucose − 100)/100**；不使用 glucose − 180 的版本（director brief 規定，且 [2] 與 [1b] 皆以 100 為基準）。
- **DKA 的 osmolal gap**：Davidson 1992 [8]：DKA 常見大 osmolal gap，約 20 h 治療後消失；主要來自 **acetone 上升、plasma water fraction 下降**，以及 amino acids、glycerol。作者指出在 DKA 中 calculated osmolality 可能嚴重低估實際值（意譯）。
- **HHS 定義**：2024 [1b] Section 3 / Fig 2b 要求四項全部符合（glucose ≥600 mg/dL、effective osmolality >300 mOsm/kg、無顯著 ketonemia、無顯著酸中毒）；HHS 的 resolution 定義才用 osmolality <300。
- **Cerebral edema / ODS**：2024 [1b] Section 5 Table 3（意譯）：成人 cerebral edema 罕見（估計 <0.1% 的事件），與 osmolarity 快速變化有關，建議對腦部影像檢查採低門檻。ODS：可發生於 hyponatraemia 快速矯正時，成人 HHS 治療中可能出現。HHS 段：Na 在 24 h 內下降不應超過 10 mmol/L，osmolality 下降 3.0–8.0 mOsm/kg/h。

### 2.4 個案應用

#### (a) Day0 18:28 的鑑別：兩種機轉並存，不是二選一
1. **Gas Na 131 可用 translocation 解釋**：1.6 校正 → **136.0**；2.4 校正 → **138.5**，即推算的 corrected Na 大致正常（推估值，不是測量的 true Na；條件是 gas Na 經確認為 direct ISE）。
2. **Chem Na 122 比 gas 低 9 mmol/L**：**lipemia 造成的 indirect-ISE pseudohyponatremia**（疊加在 translocation 之上）是**合理但未證實的推論**。考量點：
   - **Measured osmolality 318 與 Na 122 不一致，但並非不可能並存**：若 true Na 為 122，calculated osmolality 為 274.7，osmolal gap 達 **43.3**。高 gap 也可能來自未量測的溶質（如 acetone、其他 ketone 相關溶質、lipemia 降低 water fraction，或需另外排除的外來 osmole），**不能單憑 gap 判定 pseudohyponatremia**。反推：若 gap 為 0／10，與 318 相容的 Na 約 **143.7／138.7**，較接近 gas Na，但這只是算術對照。
   - Chem−gas 差距隨時間縮小（−9/−10 → −8 → −6 → −4），**可能**與干擾物減少有關（例如若有使用 insulin，chylomicron 可能下降），也可能受其他因素影響；TG 只在 Day1 測一次，**僅屬支持性線索，不是已證實的機轉**。
   - Albumin 3.5 不支持高蛋白造成；但 total protein 未測（Chopra [11] 顯示 protein 是 indirect-ISE 偏差的主要預測因子）。
3. **但不能「假設」方法**：必須向檢驗科確認 chemistry 是否為 indirect ISE、blood gas 是否為 direct ISE。Gas 分析也可能受 heparin 稀釋、檢體延遲、氣泡、hemolysis（早期有 hemolysis 紀錄）影響；動脈或靜脈來源未知（對 Na 影響小）。**確認方法**：同一檢體在 direct ISE 上重測，或經 ultracentrifugation／lipid clearing 後重測。

#### (b) 計算（只用同一時間點；只做一次校正）
| Day0 18:28 | 使用 gas Na 131（建議主值，待方法確認） | 使用 chem Na 122（方法混淆，僅供對照） |
|---|---|---|
| Corrected Na（1.6） | 136.0 | 127.0 |
| Corrected Na（2.4，敏感度） | 138.5 | 129.5 |
| Calculated osmolality = 2Na + Glu/18 + BUN/2.8 | 292.7 | 274.7 |
| Osmolal gap（vs measured 318） | **25.3** | 43.3（可能部分來自方法差異，未證實） |
| Effective osmolality（tonicity）= 2Na + Glu/18 | **284.8** | 266.8 |

- **不重複校正**：corrected Na 只對 glucose 校正一次；**不對 lipemia 再「加回」一個 Na**。lipemia 的正確處理方式是換用 direct ISE 的測量值，而不是用公式補。Corrected Na 是推估值（construct），**不是測量的真值**。
- **Osmolal gap 約 25**（用 gas Na）：依 [8]，DKA 本身（acetone、water fraction 下降、amino acids、glycerol）即可造成大 gap；本例另有嚴重 lipemia 可降低 water fraction。殘餘的 Na 方法誤差無法與上述來源分開，因此 **gap 的組成無法拆解**，也不能據此單獨診斷 toxic alcohol（若臨床有疑慮，應另行檢驗）。
- **Measured osmolality 318** 包含 urea 與其他 ineffective osmoles，**不能直接等同 effective tonicity**。以 measured 318 − BUN/2.8（7.9）≈ 310 當作 tonicity 上限估計，仍含 acetone 等未必有 effective 作用的溶質，屬不確定區間。
- **Anion gap（不建議計算）**：Day1 17:31 有 Cl 102，但沒有同時的 chemistry Na；若混用 gas Na 138 與 gas HCO₃ 17.0 得 AG ≈ 19，屬**跨方法混用**，且 2024 [1b] 明言 AG 不作 resolution 準則。

#### (c) HHS？→ 不符合；屬 DKA
- Glucose 411（<600）、effective osmolality ≈285（<300，即使用 chem Na 也只有 267）、BOHB 5.6（≥3.0）、HCO₃ 10.5（<18）→ **DKA，非 HHS，也非 mixed DKA/HHS**。
- 嚴重度：依 2024 Table 2，HCO₃ 10.5（10 至 <15）→ moderate；Day0 18:28 pH 7.316 本身不屬於 Table 2 的 moderate pH 區間，19:46 pH 7.278 落在 mild 區間。Table 2 註明不需所有變數都符合。

#### (d) 時間序列（同一時間點配對）
| 時間 | Glucose | Gas Na → corrected 1.6／2.4 | Chem Na → corrected 1.6／2.4 | Effective osm（gas／chem） |
|---|---|---|---|---|
| Day0 18:28 | 411 | 131 → 136.0／138.5 | 122 → 127.0／129.5 | 284.8／266.8 |
| Day0 19:46 | 380 | 133 → 137.5／139.7 | 123 → 127.5／129.7 | 287.1／267.1 |
| Day1 05:53 | 297 | — | 129 → 132.2／133.7 | —／274.5 |
| Day1 15:03 | 281 | 139 → 141.9／143.3 | 133 → 135.9／137.3 | 293.6／281.6 |

- Day1 01:58 只有 POC glucose（220），Day2 04:25 沒有同時的 lab glucose（POC 05:00 為 216），**不計算**，避免混用時間與方法。
- **離散測值未顯示 effective osmolality 持續下降**（gas 284.8 → 287.1 → 293.6，只有三個時點）：glucose 下降被 Na 上升抵銷。但取樣稀疏，**不能排除兩次採檢之間曾有短時快速變化，也不能據此估算短時下降速率**；沒有意識狀態紀錄，也**不能排除神經事件**。
- Gas-based corrected Na 從 136.0 升到 141.9（兩點相差約 20.5 h，+5.9；2.4 版 +4.8；只是兩點差值）→ 提示相對 free water 狀態需追蹤（輸液張力的選擇屬 fluid-insulin 報告範圍）。

#### (e) Cerebral edema vs ODS
- **Cerebral edema**：成人罕見；機轉與 tonicity 快速下降、低灌流、發炎相關 [1b Table 3]。本例離散測值未顯示 effective tonicity 持續下降，但無法排除短時變化；若出現頭痛、意識改變、bradycardia 或高血壓，應依 [1b] 對腦部影像檢查採低門檻。
- **ODS**：風險來自**慢性、真正低張**的 hyponatremia 被快速矯正。本例的「低 Na」**推論上**較可能是 **translocational（非低張）**，加上**可能的** pseudohyponatremia（未證實）；gas Na 131 → 139 與 chem Na 122 → 135 的上升，**推論上**可能主要反映 glucose 下降（水回到細胞內），以及可能的干擾減少，而不是 true hypotonic hyponatremia 的矯正——這是推論，不是已證實的事實。因此不宜直接把 chem Na 從 122 升到 135 解讀為「Na 矯正過快（13 mmol/L）、有 ODS 風險」。
  - **低張液**：現有資料**未建立** 0.45% saline 的適應症（[1b] §Fluid therapy 只在 HHS 中 osmolality 未下降時提到）；但 Na 方法、osmolal gap 與 I/O 都未確認，**不能排除所有低張液情境**。以低張液（0.45% saline 或作為 free water 的 D5W）矯正 tonicity，和 glucose <250 時加 5–10% dextrose 以支持 insulin 持續給予（[1b] §Fluid therapy／Insulin）是**兩件不同的事**，不應混為一談。
  - 例外：若檢驗科確認 chemistry 其實是 direct ISE，此推論必須重做。

### 2.5 自我挑戰（sodium/tonicity 不確定性）
1. **若 gas Na 才是錯的呢？** 肝素化 syringe 檢體量不足時，Na 偏差方向**取決於 heparin 型態與稀釋程度**：液態稀釋或 lithium heparin 可能使 Na 偏低，液態 sodium heparin 則可能使 Na 偏高；本例 heparin 型態未知，無法判斷方向。溶血或檢體延遲對 Na 影響小。Measured osmolality 318 與 gas Na 的一致性（gap 25，DKA 溶質可能部分解釋 [8]）高於 chem Na（gap 43），但這不構成證明。但 measured osmolality 本身也可能有誤差（檢體處理、蒸發會升高 osmolality）。→ 結論維持為「合理但未證實的推論」，**不寫成確診**。
2. **若中央檢驗用的是 direct ISE？** 那麼 lipemia 不應造成 9 mmol/L 差異，需改考慮 gas analyzer 校正問題、不同時間採檢（brief 寫同時）、標本混淆。此時 measured osmolality 318 仍是最客觀的錨點。
3. **TG 不是同一時間測**：Day0 的實際 lipemia 程度未知（brief 只寫多筆 lipemia）。Chopra [11] 顯示 TG >2000 才有明顯偏差，但其 multivariable model 中 protein 的影響大於 TG；本例 Day1 TG 1950，Day0 可能不同，但沒有數據。因此 lipemia 機轉在測得 lipemia index 並確認方法前，**只是合理但未量化的推論**。
4. **1.6 vs 2.4 vs 4.0**：Hillier [7] 的 n=6 且為健康人急性高血糖模型（Na 以 flame photometry 測，非 ISE），轉折點 400（abstract）或約 440（Results），本例 glucose 411 剛好落在兩者之間；DKA 合併 osmotic diuresis 與 ketone，結果可能不同。本報告兩者並列，不宣稱哪一個是 true Na。
5. **Osmolal gap 不能拿來證明或排除方法誤差**：gap 25 可能全部來自 DKA 溶質 [8]，也可能部分來自 gas Na 偏差；資料不足以拆解。

### 2.6 缺漏資料
- **檢驗方法**：中央 chemistry 與 blood gas 的 Na 測定方式（indirect vs direct ISE）、gas 檢體類型（arterial/venous）、lipemia index／hemolysis index。
- 同一檢體以 direct ISE 或 ultracentrifugation 後重測的 Na；Day0 的 TG。
- 意識狀態（GCS）、神經學症狀、vital signs。
- 輸液種類、速率、總量與 I/O（判斷 free water 與 Na 走勢）。

---

## QA3. Potassium

### 3.1 臨床問題
1. K nadir 3.2（Day1 15:03 chem）、latest 3.4（Day2 04:25 chem）vs gas 3.5，哪一個可信？
2. 2024 共識「K <3.5 延後／暫停 insulin」是否適用於治療中途、已在跑的 insulin？
3. IV 或 oral？速率與濃度如何決定？

### 3.2 已知事實
| 時間 | Chem K | Gas K | 同時其他 |
|---|---|---|---|
| Day0 18:28 | 4.0 | 4.4 | 早期 hemolysis 紀錄、pH 7.316 |
| Day0 19:46 | 3.9 | 4.3 | pH 7.278 |
| Day1 01:58 | **3.4** | 3.6 | pH 7.385 |
| Day1 05:53 | 3.6 | — | — |
| Day1 08:34 | — | 3.9 | Mg 1.9 |
| Day1 15:03 | **3.2（nadir）** | 3.4 | — |
| Day1 17:31 | — | 3.7 | Mg 2.2 |
| Day1 22:39 | — | 3.8 | — |
| Day2 04:25 | **3.4（latest）** | 3.5 | Mg 1.9 |

- Insulin 使用狀況（QA 提及 3→2 U/h、Toujeo 約 10 U）**只是提問內容，不是 MAR**；是否、何時、多少 K 已補，**完全沒有紀錄**。
- 無 ECG、UO、最近 Cr（只有 Day0 Cr 1.31）、IV access 類型（周邊／中心）。

### 3.3 證據
- **2024 共識 §Potassium [1][1b]**：
  - 總體 K 缺乏 3–6 mmol/kg；治療 48 h 內 K 通常下降 1–2 mmol/L。
  - （意譯）serum K 降到 <5.0 mmol/L 後開始補 K，目標維持 4–5 mmol/L；每公升 IV fluid 加 20–30 mmol K 通常足夠。
  - （意譯）入院時 K 偏低或低正常（<3.5 mmol/L）約見於 5–10% 的 DKA；此時應以 10 mmol/h 開始補 K，並**將 insulin 延後到 K 升至 >3.5 mmol/L**，以避免致命性心律不整與呼吸肌無力。
  - （意譯）開始 insulin 後 2 h 測 serum K，之後每 4 h 測一次直到 DKA resolution；補充過多或過少都與住院天數延長相關。
- **2024 Fig 4**（單一 session 目視、未經獨立再現；決策以正文為主，見 §0.1）：K <3.5 → 10–20 mmol/h until >3.5，更快需要 central venous access；K 欄的第一步是確認腎功能足夠（urine output 約 0.5 mL/kg/h）；圖中**沒有** K <3.5 時 hold insulin 的文字。
- **2024 Table 3**：K <3.5 發生於約 55% 的 DKA；≤2.5 與住院死亡相關（adjusted OR 4.9；本文另述約三倍死亡率 [14]）。
- **2009 共識 [2]**（single-session verified）：門檻為 >3.3 mEq/L（2024 提高到 >3.5）。
- **入院即低 K 的頻率**：Arora 2012 [12]：54 例 DKA 中 3 例（5.6%）治療前 K <3.5（3.0、3.0、2.8）。
- **ADA 2026 [3]**：Rec 16.16 僅寫以 IV fluids、insulin、electrolytes 處理；Fig 16.1 的 K 閾值本 session 未能文字核對。

### 3.4 個案應用
1. **哪個 K 可信？** Chem（serum）與 gas（whole blood）來源不同：serum K 通常因血小板在凝血時釋出 K 而略高於 plasma/whole blood；hemolysis 會使 K 假性升高（Day0 有 hemolysis 紀錄 → 早期 chem K 4.0 可能**高估**）。本例卻是 gas K 常比 chem K **高 0.1–0.4**，方向與一般預期相反，可能與分析儀校正、檢體處理或時間差有關，**原因無法確定**。Lipemia 對 K 影響小 [11]。
   → 實務上應以**同一方法的趨勢**判讀；nadir 3.2（chem）與 3.4（gas）**兩種方法都 <3.5**，因此 Day1 15:03 的 hypokalemia 是真實訊號，不能用 gas 值 3.5 否定 Day2 的 chem 3.4。
2. **K <3.5 與 insulin（紅旗）**：
   - 2024 本文「K >3.5 前延後 insulin」（意譯）的語境是**入院時** K 低（尚未開始 insulin）。本例 K 在治療過程中降到 3.2；**若當時正使用 IV insulin（無 MAR，屬假設）**，文字並未直接說「中途停掉已在跑的 insulin」，Fig 4（單一 session 目視）也沒有 hold insulin 字樣。
   - 但同一機轉（insulin 讓 K 進入細胞）在治療中途同樣存在。因此本報告的立場是：**K <3.5 是嚴重限制**，應以**監測下的 K 補充為優先**（ECG／monitor、確認 UO 與腎功能、檢查 Mg；複查間隔屬**臨床判斷**，2024 正文為開始 insulin 後 2 h、之後每 4 h），**同時由主治醫師重新評估 insulin 速率**。若仍在持續 ketosis（Day1 BOHB 4.2，之後沒有 BOHB），完全停掉 insulin 有 ketoacidosis 反彈的風險。降低 insulin 速率並配合 dextrose、全速補 K、或短暫暫停，屬**臨床判斷**，不是可以機械套用的規則；但**若當前 K 經確認 <3.5，臨床團隊須立即依低 K／DKA 流程決定暫停或調整 insulin，並在監測下補 K，不能只沿用既有速率而不處理**。這一點與 fluid-insulin-specialist 一致（見 §4）。
   - 入院時 K 為 4.0／4.4（≥3.5），依 2024 文字開始 insulin 時**不需延後**。
3. **Transition 與 K**：轉換 SC basal（例如 glargine U300／Toujeo）期間，insulin 作用仍會讓 K 往細胞內移。DKA resolution 本身不以 K 為準則，但**轉換前後 K 應補到目標 4–5 mmol/L 並持續監測**（2024：K 每 4 h，直到 resolution）。Overlap 時間（2024 的 1–2 h vs ADA 2026 的 2–4 h）不改變 K 監測頻率。
4. **IV vs oral**：
   - 2024 文字與 Fig 4 都只描述 IV 補充，**沒有禁止 oral**。
   - （**臨床判斷／院規，非 2024 原文**）IV 的優點是可滴定，一般用於 K 較低、有症狀或 ECG 變化、不能口服、腸胃功能不佳、正在用 IV insulin 等情況；oral KCl 吸收可靠但較慢，在可進食、無嘔吐、K 輕度偏低且穩定時可作為**合併或接續**手段。具體 K 門檻（例如以 3.0 為分界）依院內 protocol。
   - 周邊或中心靜脈的最大濃度與速率、是否需要 ECG monitor，依**院內 IV potassium policy**。Fig 4 指出「更快的補充需要 central venous access」。
   - **在沒有體重、UO、Cr、ECG、IV access、MAR 的情況下，本報告不提供個人化劑量或速率。**
5. **Mg**：1.9／2.2／1.9 mg/dL，大致在一般參考範圍內；hypomagnesemia 會造成 refractory hypokalemia，目前資料不支持此為主因，但補 K 期間應持續追蹤。
6. **Phosphate 與 K 的交互**：若臨床決定補磷，potassium phosphate 會同時提供 K（[1b] §Phosphate：需要時可加 20–30 mmol potassium phosphate），計算總 K 負荷時要納入。

### 3.5 缺漏資料
- **MAR**：insulin 實際速率與時間、K 製劑（KCl／K phosphate）、途徑與總量、oral K。
- ECG（U wave、QT）、cardiac monitor、心律不整症狀、肌無力或呼吸症狀。
- UO、最近 Cr／eGFR（Day0 Cr 1.31 之後無資料）、IV access 類型。
- Day1 15:03 之後的 chem K 趨勢（只有 gas）、最近一次 BOHB（判斷 insulin 必要性）。
- 院內 K 補充 protocol（周邊最大濃度與速率）。

---

## 4. 跨 session 交換紀錄（native SendMessage，最多 2 次）

- **對象**：DKA fluid insulin Opus55（fluid-insulin-specialist）。未聯絡本專案以外的 session。
- **Exchange 1**（electrolyte → fluid-insulin，ELEC-CH1）：挑戰 Na/tonicity 解讀、HHS 是否成立、K <3.5 與 transition 的關係。Transport：SendMessage 回傳 success（已送達對方 inbox）；未收到 held/refused notice。
- **對方同時來訊 fi-challenge-01**：要求確認 tonicity 以 measured osmolality ＋ direct-ISE Na 為錨點，並詢問 Fig 4 / ADA 2026 Fig 16.1 是否有不分時機的「hold insulin if K<3.5」。
- **對方 ACK ELEC-CH1（其 exchange 2/2）**：A1–A4 全部同意。補充三點：chem−gas Na 差距逐漸縮小僅屬支持性證據；TG 不是同時測；gas 動脈或靜脈未知但影響小。B(i) 部分同意：K 不是 resolution 準則，但轉換前後要補到 4–5 並複查 Mg；持續 K <3.5 需要優先補充並由主治醫師檢視 insulin 速率，**但不構成單獨不給 SC basal 的理由**。B(ii)、B(iii) 同意。另提出 ADA 2026 內部不一致：Transition 段寫 2 h、DKA/HHS 段寫 2–4 h（本 session 只核到 DKA/HHS 段的 "2–4 h"）。
- **Exchange 2**（electrolyte → fluid-insulin，ACK fi-challenge-01）：回報 Fig 4 目視結果（**無 hold-insulin 字樣、無 admission 限定語**；本文與圖的速率、濃度、≥/> 差異），同意 C1。說明 ADA 2026 Fig 16.1 數值本 session 未核對。Thread closed。
- **共識與未解項**：
  - 共識：DKA 非 HHS；tonicity 以 gas Na（待方法確認）＋ measured osmolality 為錨點；chem Na 不用於 tonicity 或 gap；corrected Na 兩值並列且皆為推估值；現有資料未建立 0.45% saline 的適應症，但 Na 方法、gap 與 I/O 未知，不能排除所有低張液情境（Codex 臨床審查後統一措辭）；K <3.5 屬紅旗，優先監測下補 K，若 insulin 正在使用（無 MAR），暫停或調整屬臨床判斷，但確認 K <3.5 時須立即依低 K／DKA 流程處理；沒有 MAR 不宣稱給或沒給。
  - 未解：ISE 方法（需檢驗科確認）；ADA 2026 Fig 16.1 的 K 閾值數值；2024 本文與 Fig 4 的 K 速率／濃度差異；2024 與 2009 的 phosphate 閾值單位差異。

---

## 5. 一頁摘要（給臨床團隊）
1. **Ca**：total Ca 7.8、albumin 3.5 → Payne 校正約 8.2，但**校正公式不可靠**[13] → **請測 ionized Ca**。不能推論曾補磷導致 Ca 下降（無 MAR）。
2. **Phosphate**：單位未列。若為 mg/dL → 0.42 → 0.52 mmol/L（中度低磷），是否補磷取決於肌無力、呼吸或心臟受損（2024 閾值 <1.0 mmol/L 並需有症狀）。RCT [4][5] 未顯示補磷改善結局；[4] 兩組 total Ca 都下降且無差異，補磷組 iCa 較低（僅 13 人可測）。2024（mmol/L）與 2009（mg/dL）閾值不一致，不可推定 2024 單位寫錯。
3. **Na**：chem 122 vs gas 131 同時 → **lipemia／indirect-ISE pseudohyponatremia 是合理但未證實的推論**，疊加 translocational hyponatremia。Measured osmolality 318 與 Na 122 不一致但並非不可能並存；高 gap 也可能來自未量測溶質。Gas-based corrected Na 136.0（1.6）／138.5（2.4）；effective osmolality ≈285；osmolal gap ≈25（無法拆解）。**非 HHS**。離散測值未顯示 effective tonicity 持續下降，但不能排除短時變化。現有資料未建立 0.45% saline 適應症，也不能排除所有低張液情境。**需檢驗科確認 ISE 方法。**
4. **K**：nadir 3.2、latest 3.4（gas 3.5），兩種方法都曾 <3.5 → **紅旗**。2024 正文（入院語境）為 K <3.5 延後 insulin 至 >3.5；Fig 4（單一 session 目視）寫 10–20 mmol/h（正文寫 10 mmol/h），且需先確認腎功能／UO。若當時正使用 insulin（無 MAR），應優先監測下補 K，並重新評估 insulin 速率；當前 K 若確認 <3.5，須立即依低 K／DKA 流程處理。IV 依院規，oral 不是絕對禁忌。**沒有體重、UO、Cr、ECG、MAR → 不給個人化處方。**
5. 本報告已依 Codex 臨床審查修訂（2026-10-28，synthesis-editor 執行），見 `reports/reviews/clinical-review.md`。
