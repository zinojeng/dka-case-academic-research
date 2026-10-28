# DKA 個案 academic deep research workflow

教學網站：**[DKA 床邊判讀](https://dka-teaching-rounds.zinojeng.workers.dev)**。免登入，支援手機閱讀；可切換 PGY 重點與 Fellow 深讀，包含個案時間軸、Insulin 算術核對、九題練習及來源連結。

以單一去識別 DKA 個案（40 多歲男性，Day0–Day2）為核心的文獻研究：五大 QA（Ca/P、Na、K、fluids、insulin transition）＋延伸（KPD、TG/pancreatitis），由多個 native Claude Code background sessions（pinned `claude-opus-5-5`）分工完成，Codex 統籌與 git release。

網站原始碼與部署說明見 [site](site/README.md) 和 [網站文件](docs/website.md)。研究紀錄保留於 private repository；公開教學頁僅提供去識別內容。

## 結構
```
CLAUDE.md                     專案 protocol（隱私、ownership、完成定義）
scripts/workflow.py           plan/init/dispatch/adopt/resume/status/message/manifest/accept/migrate-legacy
tests/                        fake claude + unittest（argv、registry、mailbox、gate、path safety、失敗啟動、resume copy）
.claude/agents/*.md           六個角色定義（model: inherit）
.claude/commands/case-research.md   /case-research 斜線指令
.claude/settings.json         worktree.bgIsolation = none
docs/case-questions.md        去識別時間軸 + 必答問題（可重現的 case example）
docs/research-protocol.md     引用、source register、寫作規則
docs/workflow.md              session、gate、resume、legacy takeover
docs/native-transport.md      ListAgents/SendMessage 與 file mailbox
coordination/                 workflow-plan.json、messages/、manifests/、acceptance/（追蹤、去識別）
reports/<role>/               各角色 owned outputs
runtime/ sessions/ fulltext/ parsed/ .private/   ignored
```

## 本輪報告
- [臨床摘要（繁中）](reports/clinical-summary.zh-TW.md)
- [電解質 QA1–QA3：Ca/P、Na、K](reports/electrolytes.md)
- [輸液與胰島素 QA4–QA5](reports/fluid-insulin.md)
- [去識別時間軸](reports/case-timeline.md)
- Evidence：[search log](evidence/search-log.md)、[source register](evidence/source-register.json)、[fulltext manifest](evidence/fulltext-manifest.json)（PDF/parsed MD 在 ignored `fulltext/`、`parsed/`）

## 快速開始
```bash
python3 scripts/workflow.py plan            # 驗證 shipped plan（勿 --write/--overwrite）
python3 scripts/workflow.py init
python3 scripts/workflow.py preflight      # 各角色 cwd；isolated 模式每個 sessions/<role>/ 需信任一次
python3 scripts/workflow.py status
python3 scripts/workflow.py dispatch case-analyst --dry-run   # 只印 argv
python3 scripts/workflow.py dispatch case-analyst             # 由 Codex 決定何時執行
python3 -m unittest discover -s tests
```
新安裝：plan 不存在時才 `plan --write`；先依 `docs/case-questions.md` 的去識別範例（或自己的去識別個案）建立 `.private/case-brief.md`，不得放入可識別資料。

MCP：複製 `.mcp.example.json` 為 `.private/mcp.local.json` 並填入本機路徑；key 放 `.env`（見 `.env.example`）或 key file，不得追蹤。

## 規則摘要
- 原始病歷 MD read-only/ignored，不讀；只用 `.private/case-brief.md`。可追蹤內容去識別。
- 檔案存在不算完成：需 native state done/completed/idle + manifest 或 Codex acceptance。
- 無 fallback：失敗就記錄並停止。只有 Codex 做 git/PR/release。
