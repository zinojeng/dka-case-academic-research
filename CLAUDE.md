# DKA 個案 academic deep research — project protocol (portable)

本檔適用於本專案任何 Claude Code session（含 `sessions/<role>/` 下的 native `--bg` session，CLAUDE.md 由上層目錄自動載入）。

## 資料與隱私
- 根目錄數字開頭的原始病歷 MD 為 **read-only、gitignored、禁止讀取**；個案資料只來自 `.private/case-brief.md`（去識別）或可追蹤的 `docs/case-questions.md`。
- 可追蹤檔案（reports/、docs/、coordination/）必須去識別：用 Day0/1/2 + 時刻，不寫病歷號、真實日期、醫師、居住/工作地、本機絕對路徑。
- 憑證只存在 `.private/` key file 與 ignored `runtime/mcp/`；**絕不讀出、印出、引用或寫入訊息**。
- 只有已發表 literature PDF 可送 LlamaParse；病歷/case brief 絕不上傳任何服務。

## 擁有權（ownership）
- 每個角色只寫入 `coordination/workflow-plan.json` 中自己的 `owned_outputs`；其他人的檔案一律 read-only。
- `.claude/agents/*.md`、`.claude/commands/`、`.claude/settings.json`、`scripts/`、`docs/`、`CLAUDE.md` 由 workflow 維護者（Codex/workflow-builder）擁有；研究角色不得修改。
- `.claude/settings.local.json` 由 Codex 管理（ignored），其他人不改。
- `coordination/messages/`、`coordination/manifests/`、`coordination/acceptance/` 只透過 `scripts/workflow.py` 寫入（原子、不可覆寫訊息）。
- `.claude/settings.json` 設 `worktree.bgIsolation: "none"`：報告以 owner 路徑分隔，不靠 worktree；需要改 code 時再明確開 worktree。

## 研究與寫作
- 繁體中文為主；medical/drug names 用 English。
- 每個論斷附 DOI/PMID 與 locator；標明 fulltext vs abstract；未驗證者標 `UNVERIFIED`；禁止捏造 citation、數據、MAR、醫囑或缺失的 vitals。
- 不給個人化處方；說明 guideline 條件、本例缺哪些資料、需核對的院規。
- 詳見 `docs/research-protocol.md`、`docs/case-questions.md`。

## 協作
- 完成定義：native session state 為 done/completed/idle **且**（當前 attempt 的 manifest 無未回覆 challenge，或 Codex/human acceptance）。檔案存在不算完成。
- 爭點：具名 challenge → response → ack/ruling（`--reply-to`），記錄裁決依據與 unresolved。
- Native SendMessage 只是 transport；file mailbox 是 durable audit。每 peer 最多 2 次 native exchange。見 `docs/native-transport.md`。
- 只有 Codex 處理 git / PR / release；其他 session 不執行 git/gh。
