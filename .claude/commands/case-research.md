---
description: 查看/推進 DKA 個案研究 workflow（native claude --bg sessions、gate、mailbox）
argument-hint: "[status|plan|messages|dry-run <role>]"
---

你在 DKA 個案研究專案根目錄。遵守 `CLAUDE.md`。不要讀根目錄數字開頭的原始病歷 MD 或 `.private/mcp.local.json`。

依 `$ARGUMENTS` 執行（預設 `status`）：

- `status`：`python3 scripts/workflow.py status`，摘要每個角色的 native state、manifest、acceptance、gate blockers、未回覆訊息。
- `plan`：`python3 scripts/workflow.py plan`，說明 stage 順序（bootstrap → evidence + clinical → synthesis → independent review）。
- `messages`：`python3 scripts/workflow.py message list --unanswered`，列出待處理 challenge/request。
- `dry-run <role>`：`python3 scripts/workflow.py dispatch <role> --dry-run`，只印 argv，不派發。

**不要**自行執行實際 `dispatch`、`resume`、`accept` 或 git——這些由 Codex（或使用者明確指示）決定。回報時引用訊息 id 與報告路徑，不印出憑證或 PHI。
