# 獨立審查與實際執行驗證

審查執行：Claude Code Opus 5.5；統籌、採納與交付：Codex。研究與執行日期：2026-10-28。

## 臨床內容

獨立 read-only reviewer 核對 2024 consensus、ADA 2026、Fisher／Hillier 全文與 Toujeo／NovoRapid label。原始審查發現的 14 項修訂均已處理，複查未發現剩餘的重大臨床阻擋項。完整逐項處理見 [clinical review](../reviews/clinical-review.md)。使用者要求後，整合摘要另改為白話連貫內文；公式與完整文獻比較保留在專題報告。

## Workflow 驗證

- 所有角色均以使用者指定的 `claude-opus-5-5` 執行；六個研究角色定義使用 `model: inherit`。
- 實際 case analyst 從獨立 session 目錄啟動、產出兩份必要檔案並建立綁定當次 attempt 的 manifest，native state 為 done。
- 初次 bootstrap 的文獻與臨床 sessions 由 Codex 直接啟動，之後明確 adopt；紀錄保留 `gate_bypassed`，未假稱最初已完全由 dispatcher 自動依序啟動。
- 兩個臨床 session 使用原生 ListAgents／SendMessage 交換具名 challenge 與 ACK；transport 與內容回覆分開保存。
- 新目錄的 trust prompt、背景寫入 guard、private-brief Read deny 與 live-PID resume 產生副本的行為均經真實操作發現。支援的修復包括明確綁定 root settings、角色權限快照、restart 及 operator 明確採納副本；不以 Bash 繞過 Write guard。
- 原生 Write smoke 成功；Read smoke 確認去識別 case brief 可讀，兩個無敏感內容的私密 canary 均遭拒。未測試讀取真實密鑰。
- 三篇 PDF 的 LlamaParse 輸出與全文來源均核對 manifest hash；20 筆來源區分全文、摘要與未取得部分。解析器估算的圖表數值不當作原文數據。

## 交付 gate

測試涵蓋 argv、settings、完整／單檔 ownership、角色身分、相依 gate、mailbox、legacy repair、失敗與不確定啟動、restart／adopt recovery。已完成獨立 staged 與網站 worktree diff 審查。網站審查未發現 critical 問題；三項主要發現為引用審查紀錄過時、文件誤稱自動檢查 evidence register、臨時角色 completion 未關閉。Codex 已核對並修正引用與 hash、改正文件為發布時人工核對、以明確 operator acceptance 關閉補充角色紀錄。

原始病歷、密鑰、fulltext／parsed 檔案、session logs 與 runtime registry 均不進 Git。去識別摘要由使用者授權的 Claude Code 處理；病歷不送至文獻下載或 LlamaParse。

## Supplement v2 與教學網站的最終核對（Codex 補記）

新 clinical-update session 與網站 session 為 Codex 明確授權的本輪額外分工，沒有假冒六角色 plan 的 sender。補充內容經另一個 Claude Opus 5.5 read-only session（3c90cb01）核對，未發現高信心的重大阻擋項。後續已修正 pH 的 OR 條件敘述、血酮分析物措辭、NovoRapid 穩定性前提與 pCO₂ 原始實測值；公開頁只顯示文獻查核年月。

網站修正手機放大至桌面時目錄無法展開的問題，瀏覽器確認 390→1440→360px 切換正常且無水平溢出。建置替換加入備份還原；index 與 404 皆執行輸出掃描。39 項網站測試與 26 項流程測試通過，含換版失敗還原、無 JavaScript 可讀內容、惡意文字跳脫、無效計算輸入及來源完整性。

所有七筆網站 reference IDs 均由 Codex 核對存在於 20 筆 source register。K-Glu 原廠來源用於核對成分，不推定個案所在機構或地點；原廠連結公開屬於可重現引用的一部分。
