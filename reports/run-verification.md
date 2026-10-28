# 本輪交付驗證

- Codex 統籌，Claude Code Opus 5.5 執行研究、白話整合、臨床複查與網站製作。六個基礎角色有 native sessions 與驗收；supplement v2 與網站為明確額外授權，完成紀錄由 Codex 接受。初始 bootstrap 為直接啟動並 adopt，保留實際執行歷程。
- 26 項流程 unittest、39 項網站測試通過；原生 Write／Read 權限 canary 通過。新版成果由 Codex 重新核對 hash。
- 20 筆來源登錄，三篇文獻 PDF 經 LlamaParse 成功解析，原文與解析檔 hash 核對一致。Consensus／ADA 2026 無 PDF 時使用 XML／HTML，取得層級如實記錄；全文與 parsed MD 不進 Git。
- 原 14 項臨床修訂已處理。Supplement v2 經獨立 read-only QA，未發現重大阻擋項。Insulin 濃度、體重換算、磷單位、藥囑與 MAR、部分 I/O 的限制均保留。
- 獨立程式 diff 審查的具體發現已處理：重複 sender 參數、審查紀錄與來源 ID 不一致、文件自動檢查範圍、臨時角色完成紀錄、目錄 resize、建置失敗還原及 404 掃描。詳見 [審查紀錄](red-team-reviewer/review.md)。
- 瀏覽器實測桌面、390px 及 360px；無水平溢出。閱讀模式、搜尋、計算機錯誤處理、還原、測驗解析、方向鍵作答與重設均可用。主要內容靜態呈現，不依賴 JavaScript。
- 公開站只顯示文獻查核月份；無個案完整日期、病歷號、本機路徑與精確年齡。全 repo 只有隱私測試中的查核日期字串命中日期 denylist，屬於測試拒絕輸入，未進公開 HTML。原始病歷 hash 保持不變；Git 候選內容未含原始識別資料或密鑰。
- 報告與文件本機連結可解析。七筆網站 reference IDs 全部存在於 evidence/source-register.json，這項由 Codex 發布時人工核對。
- 已部署：[DKA 床邊判讀](https://dka-teaching-rounds.zinojeng.workers.dev)。Cloudflare version：2c54829d-477f-45be-9d95-fc1ed3280e6a。
