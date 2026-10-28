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
- 三篇 PDF 的 LlamaParse 輸出與全文來源均核對 manifest hash；19 筆文獻區分全文、摘要與未取得部分。解析器估算的圖表數值不當作原文數據。

## 交付 gate

測試涵蓋 argv、settings、完整／單檔 ownership、角色身分、相依 gate、mailbox、legacy repair、失敗與不確定啟動、restart／adopt recovery。已進行兩輪獨立 staged diff 審查並修正具體問題；最後修訂的程式 diff 複查結果在交付前由 Codex補記。本檔不把尚未回來的審查推定為通過。

原始病歷、密鑰、fulltext／parsed 檔案、session logs 與 runtime registry 均不進 Git。去識別摘要由使用者授權的 Claude Code 處理；病歷不送至文獻下載或 LlamaParse。
