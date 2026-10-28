# Workflow: native `claude --bg` sessions

`scripts/workflow.py`（Python stdlib）把每個研究角色跑成**真正的 native background session**：具名、可續接、pinned `claude-opus-5-5`、自己的 cwd、自己的 owned outputs、strict scoped MCP。

**輸出契約只有一個來源：`coordination/workflow-plan.json`。** 每個角色的 `owned_outputs`、`required_outputs`、`display_name` 都只在 plan 定義；dispatch prompt 由 plan 生成；`.claude/agents/*.md` 與本文件不列各角色檔名。`default_plan()` 只是新安裝的範本，測試確保它與 shipped plan 的契約一致。

## Stages（由 plan 的 `depends_on` 推導）
```
stage 0  case-analyst                                   (bootstrap)
stage 1  evidence-librarian | electrolyte-specialist | fluid-insulin-specialist
stage 2  synthesis-editor
stage 3  red-team-reviewer                              (independent review)
```

## Commands
| command | 作用 |
|---|---|
| `plan` | 驗證既有 plan（model pin、owner 不重疊、無循環、`peer_roles`）。`plan --write` 只用於**新安裝**（plan 已存在時會拒絕；`--overwrite` 會丟掉本地 plan 編輯） |
| `init` | 建 `runtime/`(0700)、`sessions/<role>/`、owned dirs、`coordination/{messages,manifests,acceptance}`、ignored registry；檢查 `.gitignore` 與 `.claude/settings.json` |
| `preflight` | 唯讀檢查：CLI、settings、plan、agents、MCP source 是否存在、各角色 cwd 與上次是否 untrusted（不讀 trust/憑證 JSON） |
| `dispatch <role>\|--ready [--dry-run] [--native-preflight]` | gate 檢查後啟動 native session；`--dry-run` 只印 argv |
| `restart <role> --reason ... [--dry-run]` | 對 stopped/failed/done 但**未完成**的 attempt 開新 native session（目前的 launch flags）；running/blocked 需先 `claude stop <id>`；已完成者拒絕 |
| `abandon <role> --reason ...` | 對 `launch_unverified` / `launch_timeout` / `resume_created_copy`（可能已有 worker）做人工 reconcile 記錄；之後才可 dispatch/restart |
| `adopt <role> --native-id <8hex> --reason ... [--replace] [--cwd-rel ...]` | 登記 Codex 已直接啟動的 session（不啟動、不檢查 gate，記錄 `gate_bypassed`）。`--replace`：當前 attempt 為 `resume_created_copy`/`abandoned` 時接管指定 session（copy 時 id 必須等於記錄的 copy id；name/cwd 必須相符；舊 source 必須已停止且無 live pid；記錄 `replaces_*` lineage，歷史不改） |
| `resume <role> --message <id>... [--note] [--dry-run]` | 讓已結束的 session 處理 mailbox 訊息 |
| `status [--json]` | native state + manifest + acceptance + gate blockers + 未回覆訊息 |
| `message send\|list` | 原子 file mailbox |
| `migrate-legacy [--repair] [--apply]` | 匯入/修復舊格式訊息（預設 dry-run） |
| `manifest <role> --output ...` | session 自己寫 explicit completion manifest（綁定當前 attempt + sha256） |
| `accept <role> --by codex\|human --basis ...` | Codex/human acceptance（需 native 已結束） |

Operator-only（從 `sessions/<role>/` cwd 呼叫會被拒絕）：`plan --write`、`init`、`dispatch`、`restart`、`abandon`、`adopt`、`resume`、`accept`、`migrate-legacy`。

## Launch argv（dispatch / restart）
```
claude --bg --name "<display_name>" --model claude-opus-5-5 --effort high \
  --settings <root>/.claude/settings.json --setting-sources "" --permission-mode auto \
  --strict-mcp-config --mcp-config runtime/mcp/<role>.json --add-dir <root> \
  --agents '<json from .claude/agents>' --agent <role> \
  --allowedTools Read Glob Grep Agent TodoWrite ListAgents SendMessage \
     'Bash(python3 ../../scripts/workflow.py message send --from <role> *)' \
     'Bash(python3 ../../scripts/workflow.py message list *)' \
     'Bash(python3 ../../scripts/workflow.py manifest <role> *)' \
     'Edit(//<root>/<owned-dir>/**)' 'Edit(//<root>/<owned-file.md>)' ... mcp__<server> 'mcp__<server>__*' ... \
  --disallowedTools 'Read(//<root>/[0-9]*.md)' 'Read(//<root>/.private/*.json)' ... 'Bash(git *)' \
  -- "<prompt>"
```
- **`--settings <root>/.claude/settings.json` + `--setting-sources ""`**：isolated cwd 不會載入專案根的 `.claude/settings.json`，`worktree.bgIsolation: none` 因此未生效，session 被 EnterWorktree guard 擋住。dispatch 明確綁定該檔（缺檔、symlink 或 `bgIsolation` ≠ `none` 時拒絕啟動），並以 `--setting-sources ""` 防止 operator 的 user/local 寬權限滲入角色 session。**不得**以 Bash 寫檔繞過 Write/EnterWorktree guard。
- `cwd = sessions/<role>/`（`session_cwd: isolated`，預設）或專案根目錄（`session_cwd: shared`）；`stdin = DEVNULL`（否則 heredoc/管線內容會被附加到 native prompt）；`shell=False`。
- **永遠用 bare `--`**：`--mcp-config`、`--add-dir`、`--allowedTools`、`--disallowedTools` 都是 variadic。
- **Edit rule**：owned 目錄 → `Edit(//abs/dir/**)`；owned 單一檔案 → 精確 `Edit(//abs/file.md)`（`file.md/**` 不會匹配檔案本身）。
- MCP：從 `.private/mcp.local.json` 只複製該角色的 server 到 `runtime/mcp/<role>.json`（0600），值絕不印出；缺 server 直接失敗。Allow rule 以 server 為單位（`mcp__<s>` 與 `mcp__<s>__*`）；generic `mcp__*` 觀察到不會核准工具。
- `.private/`：常見敏感副檔名 `*.json/*.key/*.pem/*.env/*.txt/*.yaml/*.yml/*.toml` deny；啟動時列出 `.private/` 內實際的子目錄（`<sub>/**`）與檔案（精確路徑）逐一 deny，**唯獨 `case-brief.md` 可讀**（只讀名稱，不讀內容）。不用 `.private/*/**` 這類寬 wildcard —— 實測它會擋住 case-brief.md 本身。此清單是**啟動當下的快照**：launch 之後才新增到 `.private/` 的檔案只受副檔名 pattern 約束；這是協作 guardrail，不是安全邊界。
- Prompt 內所有要先讀的檔案都以專案根絕對路徑給出（isolated cwd 下相對路徑會錯）。
- 啟動後以 `claude agents --json --all` 確認 id、name、完整 sessionId（UUID）才記為 `launched`。

## No fallback / failure handling
| 狀態 | 意義 | 下一步 |
|---|---|---|
| `launch_untrusted` | stderr 含 `Workspace not trusted`（exit 6） | 人工信任該目錄後 dispatch |
| `launch_failed` / `launch_unparsed` | CLI rc≠0 / 輸出無法解析 | 修正後 dispatch（新 attempt） |
| `launch_timeout` | CLI 逾時，**可能已啟動 worker** | `claude agents` 核對 → 必要時 `claude stop` → `abandon --reason` |
| `launch_unverified` | 有 id 但 `claude agents` 未確認（exit 3） | 同上 |
| `resume_created_copy` | resume 產生 copy（exit 5） | 同上 |
| `abandoned` | operator 已 reconcile | dispatch / restart |

不用 `--fallback-model`、不換 flag 自動重試、不退回非背景執行、不猜 session id；`dispatch --ready` 遇第一個失敗即停止；`claude agents` 無法使用 → 所有 gate 關閉。所有 attempt（含失敗）永久保留在 registry。

## Restart vs resume
- **resume**：同一 session 續接。argv **只能**是 `claude --bg --resume <full sessionId UUID> -- <prompt>`。觀察：對仍在執行的 session resume，或多帶任何 launch flag，CLI 會另開 copy。因此 `working`/`blocked`/未知 → 拒絕（exit 5，不呼叫 CLI）；**即使 state 為 `done`/`idle`，只要 `claude agents` 列出的 pid 仍存活也拒絕**（實測：done + live pid 的 session 以無 flag resume 仍被 clone）——改用 `claude attach <id>` 或 SendMessage 與它對話，或 `claude stop <id>` 並等到不再列出 pid 後再 resume；輸出可能只有 `backgrounded · <id>`（無名稱），名稱與 sessionId 由 registry/`claude agents` 對照；回傳 id ≠ 原 id 或輸出提到 copy → `resume_created_copy`。
- **restart**：新 session、新 attempt id，套用**目前**的 launch flags（例如補上 `--settings`）。舊 attempt 原樣保留，新 attempt 記 `replaces_attempt`、`replaces_native_id`、`replaced_native_state`、`restart_reason`。舊 manifest/acceptance 綁定舊 attempt id，自動失效。

## Completion gate
角色完成 ⇔
1. 當前 attempt 為 `launched`/`adopted`，且
2. native state ∈ {`done`, `completed`, `idle`}，且
3. `coordination/manifests/<role>.json` 屬於當前 attempt、列出所有 plan `required_outputs`、sha256 未變、且沒有未回覆的 challenge；**或** `coordination/acceptance/<role>.json`（by codex/human，同 attempt，hash 未變）。

報告檔存在本身永遠不算完成。下游 dispatch 前所有 `depends_on` 都必須完成。

## Mailbox 與身分（local trusted-operator model）
`coordination/messages/<UTC-ts>-<8hex>.json`，以 same-dir temp + fsync + `os.link`（不覆寫；碰撞回報錯誤而非 traceback）原子寫入。欄位：`id, created_at, from, to, kind, channel, topic, status, reply_to, evidence, unresolved, body`（transport 另有 `transport.peer/result`）。

身分規則（**本機協作約定，不是密碼學或安全邊界**）：
- 從專案根目錄（或任何非 `sessions/` cwd）呼叫 = trusted operator（Codex/人）。
- `--from`/`--to` 只能出現一次（含 `--from=x` 與縮寫形式），否則 argparse 會取最後一個值、繞過 Bash prefix rule 的身分（shared cwd 模式尤其依賴此點）。
- 從 `sessions/<role>/` 呼叫 → `message send --from` 必須是該 role；`manifest` 只能寫該 role；operator-only 指令拒絕。launch 的 Bash allow rule 也只允許該 role 的 helper 形式。
- `request`/`challenge` 一律以 `open` 開始，不能自行標 resolved；關閉只能靠回覆。
- `response`/`ack` 必須由原收件者回給原寄件者；`ruling` 只能由 codex/human；例外：session 可對自己送出的 `transport` 記錄補記 native `ack`。
- 「未回覆」= request/challenge 沒有 response/ack/ruling 指向它，且自身 status ≠ resolved（只有 operator 匯入的 legacy 訊息可能帶 resolved）。
- shared cwd 模式下 cwd 無法區分角色，只剩 Bash allow rule 的 `--from <role>`/`manifest <role>` 限制。

file polling 不是 native realtime messaging；native 傳輸見 `docs/native-transport.md`。

## Runtime（ignored，不追蹤）
`runtime/registry.json`（0600：attempt、native id、sessionId、cwd_rel、prompt sha256）、`runtime/logs/`、`runtime/mcp/`、`sessions/`、`fulltext/`、`parsed/`。

## Workspace trust（troubleshooting）
Native `claude --bg` 只在**已信任**的目錄啟動；信任**不會**從上層目錄繼承。新建的 `sessions/<role>/` 第一次 dispatch 會失敗：
```
Workspace not trusted. Run `claude` in <root>/sessions/<role> once and accept the trust prompt, then retry.
```
workflow 偵測此 stderr → `launch_untrusted`（exit 6）並印出需信任的相對目錄；**不**自動重試、**不**讀寫全域 trust JSON、**不**用 `--dangerously-skip-permissions` 或 `-p` 繞過。修復（有權限的人執行，屬授權 setup）：
```bash
python3 scripts/workflow.py preflight
cd sessions/<role> && claude          # 接受 trust dialog 後 /exit
python3 scripts/workflow.py dispatch <role>
```
Clone 到其他路徑：每個 isolated `sessions/<role>/` 都要信任一次；或在 plan 設 `"session_cwd": "shared"`（cwd = 已信任專案根；代價見上方身分規則）。

## Live verification（實測紀錄）
- 首次 dispatch case-analyst：`Workspace not trusted`（rc 1）→ 記為失敗 attempt，保留於 registry。
- 信任後 dispatch：session 啟動，但被 EnterWorktree guard 擋住 —— 專案根 `.claude/settings.json` 的 `bgIsolation: none` 在 isolated cwd 未生效。
- Codex 正向實證：native session 從**同一** `sessions/case-analyst` cwd 以 `--settings <ABS_ROOT>/.claude/settings.json --setting-sources ''` 且只允許 Write/Read 啟動，Write 成功建立 ignored `sessions/case-analyst/smoke.md`，native state `done`。結論：明確 settings 綁定修正了 guard 問題，無需 Bash workaround。
- 已完成：Codex 以修正後 flags 對 case-analyst 執行 `restart`；case/data-gap 輸出與 manifest 成功。
- resume 實測：state `done` 但 pid 仍存活的 session，以無 flag resume 仍被 clone（回報 exit 5）→ 現在 live pid 一律拒絕 resume。

## Legacy takeover（本輪）
本輪 clinical sessions 由 Codex 直接啟動，輸出為扁平檔案，訊息為手寫 JSON（任意 id/schema）。shipped plan 已記錄實際 owner 與輸出；**不要**為了開始而 `plan --write --overwrite`。
1. `python3 scripts/workflow.py plan`（驗證 shipped plan）→ `init`。
2. `claude agents --json --all` 查 short id 後 `adopt <role> --native-id <id> --reason "..."`（名稱必須等於 plan `display_name`；cwd 為專案根；記錄 `gate_bypassed: true`）。
3. `migrate-legacy`（dry-run）→ `--apply`：
   - from/to 去掉 `(display name)` 後綴；list 收件者逐一展開；kind 由 id/topic 推斷（`kind_inferred: true`）；`closed` → `resolved`；reply_to 依 legacy id 對映。
   - legacy reply_to 找不到 → 降為 `info` 並在 `unresolved` 加標記（不會產生 reply_to 為 null 的 ack/response）。
   - body 缺少時由原檔 `summary/resolution/deliverable/key_findings/tool_outcomes/limitations/not_done` 組成摘要；完整原物件保留在 `legacy.original`。
   - `--repair --apply` 修復先前匯入的副本（同上規則，記 `repaired_at`）。
   - **Supersession**：legacy 原檔是不可變的 provenance，永不修改；匯入的 schema 副本是 operational mailbox（status/gate 只看副本）。兩者並存是刻意的。
4. 完成判定：adopted session 沒有 workflow manifest → Codex 檢閱後 `accept <role> --by codex --basis "..."`（需 native done）；或 `resume` 讓它自己跑 `manifest`。
5. 之後的角色走正常 gate。
