#!/usr/bin/env python3
"""Native `claude --bg` workflow for the de-identified DKA case study (stdlib only).

Commands: plan, init, preflight, dispatch, restart, abandon, adopt, resume, status,
message, manifest, accept, migrate-legacy.  The plan (coordination/workflow-plan.json)
is the single output contract.  Trust model: local trusted operator (project-root
cwd); a cwd under sessions/<role>/ is bound to that role.  Not a security boundary.
Rules (docs/workflow.md): pinned claude-opus-5-5, no fallback, stdin=DEVNULL,
dispatch binds --settings <root>/.claude/settings.json and --setting-sources "",
bare `--` before every positional prompt (variadic --mcp-config/--add-dir/
--allowedTools), resume = `--bg --resume <full sessionId> -- <prompt>` with no
other flags and only for non-running sessions (else the CLI starts a copy),
completion = native completed/idle + (current-attempt manifest with no
unanswered challenge, or Codex/human acceptance). Registry/logs/MCP copies
live in ignored runtime/; credential values are never printed.
"""
from __future__ import annotations

import argparse, datetime as dt, fcntl, hashlib, json, os, re, secrets, shutil, subprocess, sys, tempfile
from contextlib import contextmanager
from pathlib import Path

PINNED_MODEL = "claude-opus-5-5"
PLAN_REL, MSG_REL, ACC_REL, MAN_REL, AGENTS_REL = ("coordination/workflow-plan.json", "coordination/messages", "coordination/acceptance",
                                                   "coordination/manifests", ".claude/agents")
REQUIRED_IGNORES = ("runtime/", "sessions/", ".private/", "fulltext/", "parsed/", "/[0-9]*.md")
ROLE_RE = re.compile(r"^[a-z][a-z0-9-]{1,47}$")
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._-]{0,79}$")
SERVER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
MSG_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{12}Z-[0-9a-f]{8}$")
SHORT_ID_RE = re.compile(r"^[0-9a-f]{8}$")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
LAUNCH_RE = re.compile(r"backgrounded\s*·\s*([0-9a-f]{8})\b(?:[ \t]*·[ \t]*([^\n]*?))?[ \t]*$", re.M)  # name optional (resume output)
COPY_RE = re.compile(r"\bcop(y|ied)\b", re.I)
UNTRUSTED_RE = re.compile(r"workspace not trusted", re.I)
FAILED_LAUNCH = {"launch_failed", "launch_unparsed", "launch_untrusted", "abandoned"}  # safe to relaunch
NEEDS_RECONCILE = {"launch_unverified", "launch_timeout", "resume_created_copy"}  # a worker may exist: operator must abandon
LOCAL_PATH_RE = re.compile(r"(?<![\w.])/(Users|home|private|var/folders|Volumes|tmp)/")
RUNNING, SUCCESS = {"working", "blocked"}, {"done", "completed", "idle"}
TERMINAL = SUCCESS | {"failed", "stopped"}
LAUNCHED = {"launched", "adopted"}
EXTERNAL, ACCEPTORS = ("codex", "human", "workflow-builder"), ("codex", "human")
KINDS = ("info", "request", "challenge", "response", "ack", "ruling", "completion", "transport")
ANSWERS = ("response", "ack", "ruling")
STATUSES = ("open", "answered", "acknowledged", "resolved", "unresolved")
TRANSPORT_RESULTS = ("delivered", "failed", "peer-not-found")
MAX_NATIVE_EXCHANGES, QUERY_TIMEOUT = 2, 60
LAUNCH_TIMEOUT = int(os.environ.get("WORKFLOW_LAUNCH_TIMEOUT", "180"))
PEER_ROLES = ["evidence-librarian", "electrolyte-specialist", "fluid-insulin-specialist"]
OPERATOR_ONLY = {"plan", "init", "dispatch", "restart", "abandon", "adopt", "resume", "accept", "migrate-legacy"}
WEB = ["WebSearch", "WebFetch"]
TIMEOUT_CODE = 7
PRIVATE_BRIEF = "case-brief.md"  # the only readable file under .private/
REPLACEABLE = {"resume_created_copy", "abandoned"}  # adopt --replace may take over these


class WFError(Exception):
    def __init__(self, msg, code=2):
        super().__init__(msg)
        self.code = code


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso():
    return now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(o):
    return json.dumps(o, ensure_ascii=False, indent=2) + "\n"


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise WFError(f"cannot read JSON {Path(p).name}: {e.__class__.__name__}")


def atomic_write(path, text, mode=0o644, exclusive=False):
    """Same-dir temp + fsync + rename; exclusive=True links and never overwrites."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, mode)
        if exclusive:
            try:
                os.link(tmp, str(path))
            except FileExistsError:
                raise WFError(f"refusing to overwrite existing {path.name}")
            os.unlink(tmp)
        else:
            os.replace(tmp, str(path))
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


class Project:
    def __init__(self, root):
        self.root = Path(root).resolve()
        if any(c in str(self.root) for c in "*?[]{}"):
            raise WFError("project root contains glob metacharacters")
        self.runtime, self.sessions = self.root / "runtime", self.root / "sessions"
        self.registry, self.logs, self.mcp = self.runtime / "registry.json", self.runtime / "logs", self.runtime / "mcp"
        self.messages, self.acceptance, self.manifests = self.root / MSG_REL, self.root / ACC_REL, self.root / MAN_REL

    def safe(self, rel, within=None):
        """Project-relative path; refuses absolute, '~', '..' and symlink escapes."""
        if not isinstance(rel, str) or not rel or "\x00" in rel or rel.startswith("~") or Path(rel).is_absolute():
            raise WFError(f"unsafe path: {rel!r}")
        if ".." in Path(rel).parts:
            raise WFError(f"'..' not allowed: {rel!r}")
        base = (within or self.root).resolve()
        full = (self.root / rel).resolve()
        if full != base and base not in full.parents:
            raise WFError(f"path escapes allowed area: {rel!r}")
        return full

    def rel(self, p):
        return Path(p).resolve().relative_to(self.root).as_posix()

    def session_caller(self):
        """Role bound to a cwd under sessions/<role>/; None for the trusted operator (any other cwd)."""
        try:
            cwd = Path.cwd().resolve()
        except OSError:
            raise WFError("cannot determine the current directory; run from the project root or sessions/<role>/")
        if cwd != self.sessions and self.sessions not in cwd.parents:
            return None
        parts = cwd.relative_to(self.sessions).parts
        if not parts or not ROLE_RE.match(parts[0]):
            raise WFError("unrecognised session cwd")
        return parts[0]

    def guard(self, *texts):
        home = os.path.expanduser("~")
        for t in texts:
            if t and (str(self.root) in t or (len(home) > 1 and home in t) or LOCAL_PATH_RE.search(t)):
                raise WFError("tracked text must not contain local absolute paths")


@contextmanager
def locked(pr):
    pr.runtime.mkdir(parents=True, exist_ok=True)
    with open(pr.runtime / ".lock", "a+") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        yield


# ------------------------------------------------------------------ plan
def _role(name, display, deps, owned, required, mcp, tools, task):
    return {"name": name, "display_name": display, "depends_on": deps, "owned_outputs": owned,
            "required_outputs": required, "mcp_servers": mcp, "extra_tools": tools, "task": task}


def default_plan():
    """Template for new installs; mirrors the shipped plan's output contracts (tests compare them)."""
    return {
        "schema_version": 1, "model": PINNED_MODEL, "effort": "high", "permission_mode": "auto", "session_cwd": "isolated",
        "mcp_source": ".private/mcp.local.json", "external_participants": list(EXTERNAL),
        "native_messaging": {"max_exchanges_per_peer": MAX_NATIVE_EXCHANGES, "peer_roles": list(PEER_ROLES)},
        "roles": [
            _role("case-analyst", "DKA case analyst Opus55", [], ["reports/case-analyst"],
                  ["reports/case-analyst/case-timeline.md", "reports/case-analyst/data-gaps.md"], [], [],
                  "Bootstrap：只讀 .private/case-brief.md，建立去識別 Day0/1/2 時間軸、同時間點配對、單位假設與資料缺口。"),
            _role("evidence-librarian", "evidence-librarian-fulltext-parsing", ["case-analyst"],
                  ["evidence", "reports/evidence-librarian", "fulltext", "parsed"],
                  ["evidence/search-log.md", "evidence/source-register.json", "evidence/fulltext-manifest.json"],
                  ["paper-search", "research_hub", "scihub", "llamaparse"], WEB,
                  "查證 DOI 10.2337/dci24-0032、10.2337/dc26-s016 與當前 literature/label；全文下載，只把已發表 literature PDF 送 LlamaParse；記錄 query/date/DOI/PMID/fulltext vs abstract/locator/限制。"),
            _role("electrolyte-specialist", "DKA electrolytes Opus55", ["case-analyst"], ["reports/electrolyte-specialist", "reports/electrolytes.md"],
                  ["reports/electrolytes.md"], ["paper-search"], WEB, "回答 docs/case-questions.md QA1–QA3。"),
            _role("fluid-insulin-specialist", "DKA fluid insulin Opus55", ["case-analyst"], ["reports/fluid-insulin-specialist", "reports/fluid-insulin.md"],
                  ["reports/fluid-insulin.md"], ["paper-search"], WEB, "回答 docs/case-questions.md QA4–QA5 與延伸題。"),
            _role("synthesis-editor", "DKA synthesis editor Opus55", ["evidence-librarian", "electrolyte-specialist", "fluid-insulin-specialist"],
                  ["reports/clinical-summary.zh-TW.md", "reports/case-timeline.md", "reports/synthesis-editor", "reports/reviews/clinical-review.md"],
                  ["reports/clinical-summary.zh-TW.md", "reports/case-timeline.md", "reports/reviews/clinical-review.md"], [], [],
                  "整合已完成報告為繁體中文個案研究報告；只用 source register 已驗證引用；保留爭點、裁決依據與未解決項。"),
            _role("red-team-reviewer", "DKA independent reviewer Opus55", ["synthesis-editor"], ["reports/red-team-reviewer"],
                  ["reports/red-team-reviewer/review.md"], ["paper-search"], WEB,
                  "獨立審查：引用真實性、數字/單位、guideline 原文、是否補造缺失資料；以具名 challenge 送 mailbox。"),
        ],
    }


def peer_names(plan, roles):
    """Native peer display names derived from plan roles (no duplicate name map)."""
    return {r: roles[r]["display_name"] for r in plan.get("native_messaging", {}).get("peer_roles", []) if r in roles}


def validate_plan(pr, plan):
    if plan.get("model") != PINNED_MODEL:
        raise WFError(f"plan model must be {PINNED_MODEL}")
    if plan.get("permission_mode") not in ("auto", "dontAsk", "acceptEdits", "plan"):
        raise WFError("plan permission_mode not accepted (bypassPermissions is refused)")
    if plan.get("session_cwd", "isolated") not in ("isolated", "shared"):
        raise WFError("plan session_cwd must be 'isolated' or 'shared'")
    pr.safe(plan.get("mcp_source", ""))
    roles, names, owned_all = {}, set(), []
    for r in plan.get("roles") or []:
        n = r.get("name", "")
        if not ROLE_RE.match(n) or n in roles or n in EXTERNAL:
            raise WFError(f"invalid/duplicate role: {n!r}")
        if not NAME_RE.match(r.get("display_name", "")) or r["display_name"] in names:
            raise WFError(f"invalid/duplicate display name for {n}")
        names.add(r["display_name"])
        if not all(SERVER_RE.match(s) for s in r.get("mcp_servers", [])):
            raise WFError(f"invalid MCP server name in {n}")
        if not r.get("owned_outputs"):
            raise WFError(f"{n} owns nothing")
        for o in r["owned_outputs"]:
            p = pr.safe(o)
            for other, q in owned_all:
                if p == q or p in q.parents or q in p.parents:
                    raise WFError(f"owned outputs overlap: {other} / {n}")
            owned_all.append((n, p))
        roles[n] = r
        for q in r.get("required_outputs", []):
            if not owns(pr, r, q):
                raise WFError(f"{n} required output {q} not owned")
    for n, r in roles.items():
        for d in r.get("depends_on", []):
            if d not in roles:
                raise WFError(f"{n} depends on unknown {d}")
    if len(sum(stages(roles), [])) != len(roles):
        raise WFError("dependency cycle")
    nm = plan.get("native_messaging", {})
    if "peers" in nm:
        raise WFError("native_messaging.peers is obsolete; list role names in native_messaging.peer_roles (names come from roles)")
    if any(r not in roles for r in nm.get("peer_roles", [])):
        raise WFError("native_messaging.peer_roles lists an unknown role")
    return roles


def stages(roles):
    done, out = set(), []
    while True:
        lvl = [n for n, r in roles.items() if n not in done and all(d in done for d in r.get("depends_on", []))]
        if not lvl:
            return out
        out.append(lvl)
        done.update(lvl)


def load_plan(pr):
    p = pr.root / PLAN_REL
    if not p.is_file():
        raise WFError("plan missing; for a NEW install run: python3 scripts/workflow.py plan --write")
    plan = load(p)
    return plan, validate_plan(pr, plan)


def get_role(roles, name):
    if not ROLE_RE.match(name or "") or name not in roles:
        raise WFError(f"unknown role: {name!r}")
    return roles[name]


def owns(pr, role, rel):
    p = pr.safe(rel)
    return any(p == (pr.root / o).resolve() or (pr.root / o).resolve() in p.parents for o in role["owned_outputs"])


def load_agents(pr, roles):
    out = {}
    for n in roles:
        f = pr.root / AGENTS_REL / f"{n}.md"
        if not f.is_file():
            raise WFError(f"missing {AGENTS_REL}/{n}.md")
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            raise WFError(f"{n}.md frontmatter malformed")
        meta = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        if meta.get("name") != n or meta.get("model") != "inherit" or not meta.get("description"):
            raise WFError(f"{n}.md needs name={n}, model: inherit, description")
        out[n] = {"description": meta["description"], "prompt": m.group(2).strip(), "model": "inherit"}
    return out


# ------------------------------------------------------------------ registry / native CLI
def load_reg(pr):
    if not pr.registry.is_file():
        raise WFError("runtime registry missing; run: python3 scripts/workflow.py init")
    return load(pr.registry)


def save_reg(pr, reg):
    atomic_write(pr.registry, dump(reg), mode=0o600)


def current(reg, role):
    a = reg["roles"].get(role, [])
    return a[-1] if a else None


def last_session(reg, role):
    return next((a for a in reversed(reg["roles"].get(role, [])) if a.get("session_id") and a.get("launch_state") in LAUNCHED), None)


def record(pr, reg, role, rec):
    reg["roles"].setdefault(role, []).append(rec)
    save_reg(pr, reg)


def claude_bin():
    b = os.environ.get("WORKFLOW_CLAUDE_BIN") or shutil.which("claude")
    if not b or not os.access(b, os.X_OK):
        raise WFError("claude CLI not found / not executable")
    return b


def run(argv, cwd, timeout):
    try:
        return subprocess.run(argv, cwd=str(cwd), stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise WFError(f"claude CLI timed out after {timeout}s", TIMEOUT_CODE)
    except OSError as e:
        raise WFError(f"claude CLI could not start: {e.strerror}")


def native(pr):
    p = run([claude_bin(), "agents", "--json", "--all"], pr.root, QUERY_TIMEOUT)
    if p.returncode != 0:
        raise WFError(f"`claude agents --json --all` failed rc={p.returncode}")
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise WFError("`claude agents --json` returned non-JSON")
    return {e["id"]: e for e in data if isinstance(e, dict) and isinstance(e.get("id"), str)}


def nstate(nat, att):
    if nat is None:
        return "native-unavailable"
    if not att or not att.get("native_id"):
        return "not-launched"
    e = nat.get(att["native_id"])
    if not e:
        return "not-listed"
    if att.get("session_id") and e.get("sessionId") != att["session_id"]:
        return "session-mismatch"
    return str(e.get("state", "unknown"))


def pid_live(e):
    pid = e.get("pid") if isinstance(e, dict) else None
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def write_log(pr, role, label, payload):
    p = pr.logs / f"{now():%Y%m%dT%H%M%S%f}Z-{role}-{label}.json"
    atomic_write(p, dump(payload), mode=0o600, exclusive=True)
    return pr.rel(p)


def parse_launch(out):
    m = LAUNCH_RE.search(out or "")
    return (m.group(1), m.group(2)) if m else None


# ------------------------------------------------------------------ MCP + argv
def scoped_mcp(pr, plan, role):
    """runtime/mcp/<role>.json containing only the role's servers; values never printed."""
    sel = {}
    if role.get("mcp_servers"):
        src = pr.safe(plan["mcp_source"])
        if not src.is_file():
            raise WFError(f"MCP source missing: {plan['mcp_source']}")
        pool = load(src).get("mcpServers")
        if not isinstance(pool, dict):
            raise WFError("MCP source lacks mcpServers")
        missing = [s for s in role["mcp_servers"] if s not in pool]
        if missing:
            raise WFError(f"MCP servers not configured: {', '.join(missing)}")
        for s in role["mcp_servers"]:
            vals = [pool[s].get("command", "")] + list(pool[s].get("args") or [])
            if any(isinstance(v, str) and v.startswith(("./", "../")) for v in vals):
                raise WFError(f"MCP server {s} uses cwd-relative paths; sessions run in their own cwd")
            sel[s] = pool[s]
    pr.mcp.mkdir(parents=True, exist_ok=True)
    os.chmod(pr.mcp, 0o700)
    out = pr.mcp / f"{role['name']}.json"
    atomic_write(out, json.dumps({"mcpServers": sel}) + "\n", mode=0o600)
    return out


def rule_path(p):
    return "/" + str(p)  # permission-rule absolute form: //abs/path


def session_cwd(pr, plan, name):
    """isolated: sessions/<role>/ (each dir must be trusted once natively); shared: the trusted project root."""
    return pr.root if plan.get("session_cwd", "isolated") == "shared" else pr.sessions / name


def script_ref(pr, cwd):
    return "scripts/workflow.py" if cwd == pr.root else "../../scripts/workflow.py"


def edit_rule(pr, rel):
    """Exact rule for a single-file output, '/**' for a directory output."""
    p = pr.root / rel
    return f"Edit({rule_path(p)})" if p.is_file() or Path(rel).suffix else f"Edit({rule_path(p)}/**)"


def allowed(pr, role, cwd):
    s, n = script_ref(pr, cwd), role["name"]
    t = ["Read", "Glob", "Grep", "Agent", "TodoWrite", "ListAgents", "SendMessage",  # helpers scoped to the owned role
         f"Bash(python3 {s} message send --from {n} *)", f"Bash(python3 {s} message list *)", f"Bash(python3 {s} manifest {n} *)"]
    t += [edit_rule(pr, o) for o in role["owned_outputs"]]
    t += [f"Edit({rule_path(pr.sessions / role['name'])}/**)"] + list(role.get("extra_tools", []))
    for s in role.get("mcp_servers", []):
        t += [f"mcp__{s}", f"mcp__{s}__*"]  # per-server rules; generic mcp__* did not approve tools
    return t


def denied(pr):
    r = rule_path(pr.root)
    priv = [f"Read({r}/.private/*.{x})" for x in ("json", "key", "pem", "env", "txt", "yaml", "yml", "toml")]
    pdir = pr.root / ".private"
    for e in sorted(pdir.iterdir()) if pdir.is_dir() else []:  # names only; contents never read
        if e.is_dir():
            priv.append(f"Read({r}/.private/{e.name}/**)")
        elif e.name != PRIVATE_BRIEF:
            priv.append(f"Read({r}/.private/{e.name})")
    return [f"Read({r}/[0-9]*.md)", *priv, f"Read({r}/.env)",
            f"Read({r}/.env.*)", f"Read({r}/runtime/**)", f"Edit({r}/[0-9]*.md)", f"Edit({r}/.private/**)", f"Edit({r}/scripts/**)",
            f"Edit({r}/.claude/**)", f"Edit({r}/coordination/**)", f"Edit({r}/docs/**)", f"Edit({r}/CLAUDE.md)",
            "Bash(git *)", "Bash(gh *)"]


def project_settings(pr):
    """Root .claude/settings.json, bound explicitly with --settings: an isolated cwd does not load the root project settings."""
    f = pr.root / ".claude" / "settings.json"
    if not f.is_file() or f.is_symlink():
        raise WFError(".claude/settings.json missing; it must set worktree.bgIsolation to \"none\"")
    d = load(f)
    if not isinstance(d, dict) or (d.get("worktree") or {}).get("bgIsolation") != "none":
        raise WFError(".claude/settings.json must set worktree.bgIsolation to \"none\" (shared report ownership)")
    return f


def dispatch_argv(pr, plan, role, agents, mcp_path, prompt, cwd):
    return [claude_bin(), "--bg", "--name", role["display_name"], "--model", PINNED_MODEL, "--effort", plan["effort"],
            "--settings", str(project_settings(pr)), "--setting-sources", "",
            "--permission-mode", plan["permission_mode"], "--strict-mcp-config", "--mcp-config", str(mcp_path),
            "--add-dir", str(pr.root), "--agents", json.dumps(agents, ensure_ascii=False), "--agent", role["name"],
            "--allowedTools", *allowed(pr, role, cwd), "--disallowedTools", *denied(pr), "--", prompt]


def resume_argv(session_id, prompt):
    if not UUID_RE.match(session_id or ""):
        raise WFError("resume needs the full native sessionId UUID")
    return [claude_bin(), "--bg", "--resume", session_id, "--", prompt]  # no other flags: extra flags start a copy


def preflight_text(plan, roles, me, script):
    nm = plan.get("native_messaging", {})
    peers = "、".join(f"`{v}`" for k, v in peer_names(plan, roles).items() if k != me) or "（無）"
    lim = nm.get("max_exchanges_per_peer", MAX_NATIVE_EXCHANGES)
    return (f"Native preflight（file mailbox 為 durable fallback/audit）：ListAgents 只找本專案 peers {peers}；對其中一個 SendMessage 送一則 scoped ping 請求 ACK"
            f"（不含 PHI/路徑/憑證）。transport 結果與 application ACK 分開記錄：python3 {script} message send --from {me} --to codex --kind transport "
            f"--channel native --peer '<peer>' --transport-result delivered|failed|peer-not-found --topic 'native preflight'；收到回覆另記 --kind ack "
            f"--channel native --reply-to <transport id>。每 peer 最多 {lim} 次 exchange，超過改用 file mailbox；不得改全域 inbound policy。\n")


def role_prompt(pr, plan, roles, role, attempt_id, preflight, cwd):
    n = role["name"]
    deps = "\n".join(f"  - {d}: {', '.join(roles[d]['required_outputs'])}" for d in role.get("depends_on", [])) or "  - （無）"
    s = script_ref(pr, cwd)
    p = (f"你是 DKA 個案研究 workflow 的 `{n}`（attempt {attempt_id}）。專案根目錄（--add-dir）：{pr.root}；你的 cwd：{pr.rel(cwd) if cwd != pr.root else '專案根目錄（shared）'}。\n"
         "先讀（絕對路徑）：" + "、".join(str(pr.root / f) for f in ("CLAUDE.md", "docs/research-protocol.md", "docs/case-questions.md",
                                                                  ".private/case-brief.md", f".claude/agents/{n}.md")) + "。\n"
         "輸出契約以本 prompt（來自 coordination/workflow-plan.json）為準；agent 定義不列檔名。\n"
         "禁止讀根目錄數字開頭原始病歷 MD、.private/mcp.local.json、key/env、runtime/；不得 git/gh/release；不得修改 read-only 來源；不得印出憑證或 PHI。\n"
         f"任務：{role.get('task', '')}\n只可寫入：{', '.join(role['owned_outputs'])}\n必須產出：{', '.join(role['required_outputs'])}\n上游（已過 gate）：\n{deps}\n"
         f"Mailbox：python3 {s} message list --to {n} --unanswered；python3 {s} message send --from {n} --to <participant> --kind <kind> --topic '...' --body '...' [--reply-to <id>] [--evidence '...']。"
         "重要爭點用具名 challenge → response → ack/ruling，記錄裁決依據與 unresolved。\n"
         f"完成：python3 {s} manifest {n} --summary '...' " + " ".join(f"--output {o}" for o in role["required_outputs"]) +
         f" [--unresolved '...']，再 message send --kind completion --to codex。檔案存在不等於完成。\n")
    return p + (preflight_text(plan, roles, n, s) if preflight else "")


# ------------------------------------------------------------------ gates
def check_outputs(pr, role, outs):
    bad = []
    for o in outs:
        try:
            p = pr.safe(o.get("path", ""))
            if not owns(pr, role, o["path"]):
                bad.append(f"{o['path']}: not owned")
            elif p.is_symlink() or not p.is_file() or sha256(p) != o.get("sha256"):
                bad.append(f"{o['path']}: missing or changed")
        except WFError as e:
            bad.append(str(e))
    return bad


def evidence(pr, role, att, kind):
    p = (pr.manifests if kind == "manifest" else pr.acceptance) / f"{role['name']}.json"
    if not p.is_file():
        return False, "missing"
    try:
        d = load(p)
    except WFError:
        return False, "invalid"
    if d.get("role") != role["name"] or (kind == "manifest" and d.get("status") != "complete") or \
            (kind == "acceptance" and (d.get("by") not in ACCEPTORS or d.get("decision") != "accepted")):
        return False, "invalid"
    if not att or d.get("attempt_id") != att.get("attempt_id"):
        return False, "stale attempt"
    listed = {o.get("path") for o in d.get("outputs", [])}
    miss = [r for r in role["required_outputs"] if r not in listed]
    bad = ([f"unlisted {', '.join(miss)}"] if miss else []) + check_outputs(pr, role, d.get("outputs", []))
    return (False, "; ".join(bad)) if bad else (True, "ok")


def completion(pr, reg, role, nat):
    att = current(reg, role["name"])
    st = nstate(nat, att)
    m_ok, m = evidence(pr, role, att, "manifest")
    a_ok, a = evidence(pr, role, att, "acceptance")
    ch = [x["id"] for x in unanswered(pr, role["name"], ("challenge",))]
    launched = bool(att and att.get("launch_state") in LAUNCHED)
    ev = a_ok or (m_ok and not ch)
    why = ([] if launched else ["not launched"]) + ([] if st in SUCCESS else [f"native {st}"]) + \
          ([] if ev else [f"open challenges {ch}" if m_ok else f"manifest {m}; acceptance {a}"])
    return {"role": role["name"], "native_id": att and att.get("native_id"), "attempt_id": att and att.get("attempt_id"),
            "launch_state": att and att.get("launch_state"), "native_state": st, "manifest": m, "acceptance": a,
            "open_challenges": ch, "complete": not why, "reasons": why}


def gate(pr, reg, roles, role, nat):
    return [f"{d}: {'; '.join(c['reasons'])}" for d in role.get("depends_on", [])
            for c in [completion(pr, reg, roles[d], nat)] if not c["complete"]]


# ------------------------------------------------------------------ mailbox
def messages(pr):
    out = []
    for p in sorted(pr.messages.glob("*.json")) if pr.messages.is_dir() else []:
        if MSG_ID_RE.match(p.stem) and not p.is_symlink():
            try:
                m = load(p)
            except WFError:
                continue
            if isinstance(m, dict) and m.get("id") == p.stem:
                out.append(m)
    return out


def unanswered(pr, to=None, kinds=("request", "challenge")):
    ms = messages(pr)
    done = {m.get("reply_to") for m in ms if m.get("kind") in ANSWERS}
    return [m for m in ms if m.get("kind") in kinds and m["id"] not in done and m.get("status") != "resolved"
            and (to is None or m.get("to") == to)]


def send(pr, plan, roles, a):
    people = list(roles) + list(plan.get("external_participants", EXTERNAL))
    if a.sender not in people or a.to not in people or a.sender == a.to:
        raise WFError("unknown or identical sender/recipient")
    caller = pr.session_caller()
    if caller and a.sender != caller:
        raise WFError(f"session cwd is bound to {caller}; --from {a.sender} refused")
    if a.kind in ("request", "challenge") and a.status != "open":
        raise WFError(f"{a.kind} must start with status open; close it with a reply")
    topic, body = (a.topic or "").strip(), a.body or ""
    if not topic or len(topic) > 200 or len(body) > 20000:
        raise WFError("topic required (<=200), body <=20000")
    pr.guard(topic, body, *(a.evidence or []), *(a.unresolved or []), a.peer or "")
    ms = {m["id"]: m for m in messages(pr)}
    if a.reply_to:
        if not MSG_ID_RE.match(a.reply_to) or a.reply_to not in ms:
            raise WFError(f"reply_to not found: {a.reply_to!r}")
    elif a.kind in ANSWERS:
        raise WFError(f"kind {a.kind} requires --reply-to")
    if a.kind in ANSWERS:
        o = ms[a.reply_to]
        own_transport = a.kind == "ack" and o.get("kind") == "transport" and o["from"] == a.sender
        if a.kind == "ruling" and a.sender not in ACCEPTORS:
            raise WFError("only codex/human may issue a ruling")
        if a.sender not in ACCEPTORS and not own_transport and (a.sender != o["to"] or a.to != o["from"]):
            raise WFError(f"{a.kind} must come from the original recipient ({o['to']}) and go to the original sender ({o['from']})")
    msg = {"schema_version": 1, "id": f"{now():%Y%m%dT%H%M%S%f}Z-{secrets.token_hex(4)}", "created_at": iso(), "from": a.sender,
           "to": a.to, "kind": a.kind, "channel": a.channel, "topic": topic, "status": a.status, "reply_to": a.reply_to or None,
           "evidence": a.evidence or [], "unresolved": a.unresolved or [], "body": body}
    if a.kind == "transport":
        if a.channel != "native" or not a.peer or not a.transport_result:
            raise WFError("transport needs --channel native --peer --transport-result")
        lim = int(plan.get("native_messaging", {}).get("max_exchanges_per_peer", MAX_NATIVE_EXCHANGES))
        if sum(1 for m in ms.values() if m.get("kind") == "transport" and m["from"] == a.sender and m.get("transport", {}).get("peer") == a.peer) >= lim:
            raise WFError(f"native exchange limit {lim} reached for {a.sender} -> {a.peer}; use the file mailbox")
        msg["transport"] = {"peer": a.peer, "result": a.transport_result}
    elif a.peer or a.transport_result:
        raise WFError("--peer/--transport-result only with --kind transport")
    atomic_write(pr.messages / f"{msg['id']}.json", dump(msg), exclusive=True)
    return msg


# ------------------------------------------------------------------ commands
def cmd_plan(pr, a):
    if a.write:
        if (pr.root / PLAN_REL).exists() and not a.overwrite:
            raise WFError(f"{PLAN_REL} exists; use --overwrite")
        validate_plan(pr, default_plan())
        atomic_write(pr.root / PLAN_REL, dump(default_plan()))
    plan, roles = load_plan(pr)
    print(f"model={plan['model']} permission_mode={plan['permission_mode']} effort={plan['effort']}")
    for i, lvl in enumerate(stages(roles)):
        print(f"stage {i}: {', '.join(lvl)}")
    return 0


def cmd_init(pr, a):
    plan, roles = load_plan(pr)
    load_agents(pr, roles)
    project_settings(pr)
    gi = (pr.root / ".gitignore").read_text(encoding="utf-8").splitlines() if (pr.root / ".gitignore").is_file() else []
    if [p for p in REQUIRED_IGNORES if p not in gi]:
        raise WFError(f".gitignore lacks: {', '.join(p for p in REQUIRED_IGNORES if p not in gi)}")
    owned_dirs = [pr.safe(o) for r in roles.values() for o in r["owned_outputs"] if not Path(o).suffix]
    for d in [pr.logs, pr.mcp] + [pr.sessions / n for n in roles] + owned_dirs:
        d.mkdir(parents=True, exist_ok=True)
    pr.manifests.mkdir(parents=True, exist_ok=True)
    for d in (pr.runtime, pr.mcp):
        os.chmod(d, 0o700)
    pr.messages.mkdir(parents=True, exist_ok=True)
    pr.acceptance.mkdir(parents=True, exist_ok=True)
    with locked(pr):
        if not pr.registry.is_file():
            save_reg(pr, {"schema_version": 1, "roles": {}})
    print(f"init ok; mcp_source {'present' if pr.safe(plan['mcp_source']).is_file() else 'MISSING'} (not read)")
    return 0


def launch(pr, reg, role_name, rec, argv, cwd, label):
    """Run one native launch; records every outcome; raises on any failure (no fallback)."""
    try:
        p = run(argv, cwd, LAUNCH_TIMEOUT)
    except WFError as e:
        state = "launch_timeout" if e.code == TIMEOUT_CODE else "launch_failed"  # a timed-out CLI may have started a worker
        record(pr, reg, role_name, dict(rec, launch_state=state, error=str(e)))
        raise
    rec.update(returncode=p.returncode, log=write_log(pr, role_name, label, {"argv": argv, "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}))
    parsed = parse_launch(p.stdout)
    if UNTRUSTED_RE.search(p.stderr + p.stdout):
        record(pr, reg, role_name, dict(rec, launch_state="launch_untrusted"))
        where = pr.rel(cwd) if cwd != pr.root else "."
        raise WFError(f"{role_name}: native workspace trust missing for {where}. A person must run `claude` once in that directory, "
                      f"accept the trust dialog and exit, then retry (see docs/workflow.md#workspace-trust). "
                      f"Trust is never bypassed or written by this tool. Log: {rec['log']}", 6)
    if p.returncode != 0 or not parsed:
        record(pr, reg, role_name, dict(rec, launch_state="launch_failed" if p.returncode else "launch_unparsed"))
        raise WFError(f"{role_name}: {label} failed rc={p.returncode}; see {rec['log']}")
    rec["native_id"] = parsed[0]
    return p


def dispatch_one(pr, plan, roles, agents, reg, nat, name, a, restart=None):
    role, att = roles[name], current(reg, name)
    if att and not restart and not (att.get("launch_state") in FAILED_LAUNCH or nstate(nat, att) == "failed"):
        raise WFError(f"{name} already has attempt {att['attempt_id']} ({att.get('launch_state')}, native {nstate(nat, att)})"
                      + ("; a worker may exist: verify with `claude agents`, then abandon --reason" if att.get("launch_state") in NEEDS_RECONCILE
                         else "; use resume, or restart --reason after it stops"))
    blockers = gate(pr, reg, roles, role, nat)
    if blockers:
        raise WFError(f"{name} gate closed:\n  " + "\n  ".join(blockers), 4)
    aid, cwd = secrets.token_hex(6), session_cwd(pr, plan, name)
    prompt = role_prompt(pr, plan, roles, role, aid, a.native_preflight, cwd)
    if a.dry_run:
        print(dump({"role": name, "cwd": str(cwd), "argv": dispatch_argv(pr, plan, role, agents, pr.mcp / f"{name}.json", prompt, cwd)}), end="")
        return 0
    cwd.mkdir(parents=True, exist_ok=True)
    argv = dispatch_argv(pr, plan, role, agents, scoped_mcp(pr, plan, role), prompt, cwd)
    rec = {"attempt_id": aid, "kind": "restart" if restart else "dispatch", "started_at": iso(), **(restart or {}), "name": role["display_name"], "cwd_rel": "." if cwd == pr.root else pr.rel(cwd),
           "model": PINNED_MODEL, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()}
    launch(pr, reg, name, rec, argv, cwd, "dispatch")
    e = native(pr).get(rec["native_id"])
    if not e or not UUID_RE.match(str(e.get("sessionId", ""))) or e.get("name") != role["display_name"]:
        record(pr, reg, name, dict(rec, launch_state="launch_unverified"))
        raise WFError(f"{name}: {rec['native_id']} not confirmed by `claude agents`", 3)
    record(pr, reg, name, dict(rec, launch_state="launched", session_id=e["sessionId"]))
    print(f"dispatched {name}: native {rec['native_id']} attempt {aid}")
    return 0


def cmd_restart(pr, a):
    """Fresh native session (current launch flags) for a terminal, uncompleted attempt. Prior attempts are kept."""
    plan, roles = load_plan(pr)
    agents = load_agents(pr, roles)
    role = get_role(roles, a.role)
    if not (a.reason or "").strip():
        raise WFError("--reason is required")
    pr.guard(a.reason)
    with locked(pr):
        reg, nat = load_reg(pr), native(pr)
        att = current(reg, a.role)
        if not att:
            raise WFError(f"{a.role} has no attempt; use dispatch")
        st = nstate(nat, att)
        if att.get("launch_state") in NEEDS_RECONCILE:
            raise WFError(f"{a.role} last attempt is {att['launch_state']}; reconcile with `claude agents` and run abandon --reason first", 5)
        if st in RUNNING:
            raise WFError(f"{a.role} native {att.get('native_id')} is {st}; stop it first (`claude stop {att.get('native_id')}`), then restart", 5)
        if att.get("launch_state") not in FAILED_LAUNCH and st not in TERMINAL:
            raise WFError(f"{a.role} native state {st!r} is not terminal; refused", 5)
        if completion(pr, reg, role, nat)["complete"]:
            raise WFError(f"{a.role} is already complete; use resume for rework")
        return dispatch_one(pr, plan, roles, agents, reg, nat, a.role, a, restart={
            "restart_reason": a.reason, "replaces_attempt": att.get("attempt_id"), "replaces_native_id": att.get("native_id"),
            "replaced_native_state": st})


def cmd_abandon(pr, a):
    """Operator reconciliation for launch_unverified/launch_timeout/resume_created_copy; never stops or deletes sessions itself."""
    plan, roles = load_plan(pr)
    get_role(roles, a.role)
    if not (a.reason or "").strip():
        raise WFError("--reason is required")
    pr.guard(a.reason)
    with locked(pr):
        reg, nat = load_reg(pr), native(pr)
        att = current(reg, a.role)
        if not att or att.get("launch_state") not in NEEDS_RECONCILE:
            raise WFError(f"{a.role}: abandon only applies to {sorted(NEEDS_RECONCILE)}")
        nid = att.get("native_id")
        if nid and nat.get(nid, {}).get("state") in RUNNING:
            raise WFError(f"native {nid} is still {nat[nid]['state']}; `claude stop {nid}` first", 5)
        record(pr, reg, a.role, {"attempt_id": secrets.token_hex(6), "kind": "abandon", "started_at": iso(), "launch_state": "abandoned",
                                 "abandons_attempt": att.get("attempt_id"), "abandoned_state": att.get("launch_state"),
                                 "native_id_seen": nid, "reason": a.reason})
    print(f"abandoned {a.role} attempt {att.get('attempt_id')} ({att.get('launch_state')}); dispatch/restart may now relaunch")
    return 0


def cmd_preflight(pr, a):
    """Read-only launch readiness: CLI, plan, agents, MCP source presence, session cwd per role. Never reads trust/credential JSON."""
    plan, roles = load_plan(pr)
    load_agents(pr, roles)
    print(f"claude CLI: {claude_bin()}")
    print(f"settings: {pr.rel(project_settings(pr))} (worktree.bgIsolation=none, passed via --settings)")
    print(f"session_cwd mode: {plan.get('session_cwd', 'isolated')}; mcp_source {'present' if pr.safe(plan['mcp_source']).is_file() else 'MISSING'}")
    reg = load_reg(pr)
    for n in roles:
        cwd = session_cwd(pr, plan, n)
        att = current(reg, n)
        hint = "previous launch was untrusted" if att and att.get("launch_state") == "launch_untrusted" else ""
        where = "." if cwd == pr.root else pr.rel(cwd)
        print(f"  {n:<26} cwd={where:<32} exists={cwd.is_dir()} {hint}")
    if plan.get("session_cwd", "isolated") == "isolated":
        print("Isolated mode: each sessions/<role>/ must be trusted once natively by a person (run `claude` there, accept, exit).")
    return 0


def cmd_dispatch(pr, a):
    plan, roles = load_plan(pr)
    agents = load_agents(pr, roles)
    if bool(a.role) == bool(a.ready):
        raise WFError("give exactly one of <role> or --ready")
    with locked(pr):
        reg, nat = load_reg(pr), native(pr)
        if a.role:
            return dispatch_one(pr, plan, roles, agents, reg, nat, get_role(roles, a.role)["name"], a)
        todo = [n for n in roles if not current(reg, n) and not gate(pr, reg, roles, roles[n], nat)]
        for n in todo:  # stops at first failure
            dispatch_one(pr, plan, roles, agents, reg, nat, n, a)
        print(("would dispatch: " if a.dry_run else "dispatched: ") + (", ".join(todo) or "nothing ready"))
        return 0


def cmd_adopt(pr, a):
    plan, roles = load_plan(pr)
    role = get_role(roles, a.role)
    if not SHORT_ID_RE.match(a.native_id or "") or not a.reason.strip():
        raise WFError("need 8-hex --native-id and --reason")
    pr.guard(a.reason)
    cwd = pr.root if a.cwd_rel in (None, ".") else pr.safe(a.cwd_rel)
    with locked(pr):
        reg, nat = load_reg(pr), native(pr)
        lineage = {}
        if a.replace:
            att, old = current(reg, a.role), last_session(reg, a.role)
            if not att or att.get("launch_state") not in REPLACEABLE:
                raise WFError(f"{a.role}: adopt --replace only applies when the current attempt is one of {sorted(REPLACEABLE)}")
            seen = att.get("native_id") or att.get("native_id_seen")
            if att["launch_state"] == "resume_created_copy" and a.native_id != seen:
                raise WFError(f"{a.role}: the recorded copy is {seen}; --native-id {a.native_id} does not match")
            if old and old.get("native_id") == a.native_id:
                raise WFError("--native-id is the old source session; use resume, not adopt --replace")
            src = nat.get(old["native_id"]) if old else None
            if src and (src.get("state") in RUNNING or pid_live(src)):
                raise WFError(f"old source {old['native_id']} is still {src.get('state')}"
                              f"{' with a live pid' if pid_live(src) else ''}; `claude stop {old['native_id']}` first", 5)
            lineage = {"replaces_attempt": att.get("attempt_id"), "replaced_state": att["launch_state"],
                       "replaces_native_id": old and old.get("native_id"), "replaces_session_id": old and old.get("session_id")}
        elif last_session(reg, a.role):
            raise WFError(f"{a.role} already has a registered session (use adopt --replace for a copy/abandoned attempt)")
        e = nat.get(a.native_id)
        if not e or e.get("name") != role["display_name"] or not UUID_RE.match(str(e.get("sessionId", ""))):
            raise WFError(f"native {a.native_id} not listed with name {role['display_name']!r} and full sessionId")
        if e.get("cwd") and Path(e["cwd"]).resolve() != cwd:
            raise WFError("native session cwd differs from --cwd-rel")
        record(pr, reg, a.role, {"attempt_id": secrets.token_hex(6), "kind": "adopt-replace" if a.replace else "adopt", "started_at": iso(),
                                 "name": e["name"], "cwd_rel": "." if cwd == pr.root else pr.rel(cwd), "model": PINNED_MODEL,
                                 "native_id": a.native_id, "session_id": e["sessionId"], "launch_state": "adopted", "gate_bypassed": True,
                                 "reason": a.reason, **lineage})
    print(f"adopted {a.role}: {a.native_id} (native {e.get('state')}){' replacing ' + str(lineage.get('replaces_native_id')) if a.replace else ''}; "
          "dependency gate NOT checked")
    return 0


def cmd_resume(pr, a):
    plan, roles = load_plan(pr)
    get_role(roles, a.role)
    ms = {m["id"]: m for m in messages(pr)}
    if not a.message or any(ms.get(i, {}).get("to") != a.role for i in a.message):
        raise WFError(f"resume needs existing --message ids addressed to {a.role}")
    with locked(pr):
        reg = load_reg(pr)
        prev = last_session(reg, a.role)
        if not prev:
            raise WFError(f"{a.role} has no registered native session")
        e = native(pr).get(prev["native_id"])
        if not e or e.get("sessionId") != prev["session_id"]:
            raise WFError("native session not listed or sessionId mismatch; refusing to guess")
        st = e.get("state")
        if pid_live(e):
            raise WFError(f"{a.role} native {prev['native_id']} is {st!r} but its process (pid {e['pid']}) is still live; CLI resume "
                          f"would clone it. Talk to it with `claude attach {prev['native_id']}` or SendMessage, or `claude stop "
                          f"{prev['native_id']}` and wait until `claude agents` lists no pid, then resume", 5)
        if st in RUNNING or st not in TERMINAL:
            raise WFError(f"{a.role} native state {st!r}: resuming a running/unknown session starts a copy — refused", 5)
        aid = secrets.token_hex(6)
        cwd = pr.root if prev.get("cwd_rel", ".") == "." else pr.safe(prev["cwd_rel"])
        s = script_ref(pr, cwd)
        pr.guard(a.note or "")
        prompt = (f"Resume（attempt {aid}）：處理 mailbox {', '.join(a.message)}。先 python3 {s} message list --to {a.role} --unanswered；"
                  f"逐則 --reply-to 回覆，更新你擁有的輸出，重跑 manifest（新 attempt 使舊 manifest 失效）並送 completion。\n"
                  + (f"Codex 附註：{a.note}\n" if a.note else "") + (preflight_text(plan, roles, a.role, s) if a.native_preflight else ""))
        argv = resume_argv(prev["session_id"], prompt)
        if a.dry_run:
            print(dump({"role": a.role, "cwd": str(cwd), "argv": argv}), end="")
            return 0
        rec = {"attempt_id": aid, "kind": "resume", "started_at": iso(), "name": prev["name"], "cwd_rel": prev.get("cwd_rel", "."),
               "model": PINNED_MODEL, "messages": a.message, "native_state_before": st}
        p = launch(pr, reg, a.role, rec, argv, cwd, "resume")
        if rec["native_id"] != prev["native_id"] or COPY_RE.search(p.stdout + p.stderr):
            record(pr, reg, a.role, dict(rec, launch_state="resume_created_copy"))
            raise WFError(f"{a.role}: CLI started a copy {rec['native_id']} instead of resuming {prev['native_id']}; stop it manually if unwanted", 5)
        record(pr, reg, a.role, dict(rec, launch_state="launched", session_id=prev["session_id"]))
    print(f"resumed {a.role}: native {rec['native_id']} attempt {aid}")
    return 0


def cmd_status(pr, a):
    plan, roles = load_plan(pr)
    reg = load_reg(pr)
    try:
        nat, err = native(pr), None
    except WFError as e:
        nat, err = None, str(e)
    rows = [dict(completion(pr, reg, r, nat), gate=gate(pr, reg, roles, r, nat), unanswered=[m["id"] for m in unanswered(pr, n)])
            for n, r in roles.items()]
    if a.json:
        print(dump({"native_error": err, "roles": rows, "unanswered_to_codex": [m["id"] for m in unanswered(pr, "codex")]}), end="")
        return 0
    if err:
        print(f"WARNING native status unavailable ({err}); all gates closed")
    for c in rows:
        tag = "COMPLETE" if c["complete"] else ("ready" if not c["gate"] and not c["launch_state"] else "-")
        print(f"{c['role']:<26} {tag:<8} native={c['native_id'] or '-'}:{c['native_state']} launch={c['launch_state'] or '-'} "
              f"manifest={c['manifest']} acceptance={c['acceptance']}")
        for g in c["gate"]:
            print(f"    gate: {g}")
        if c["unanswered"]:
            print(f"    unanswered: {', '.join(c['unanswered'])}")
    return 0


def cmd_message(pr, a):
    plan, roles = load_plan(pr)
    if a.action == "send":
        with locked(pr):
            m = send(pr, plan, roles, a)
        print(f"sent {m['id']} -> {MSG_REL}/{m['id']}.json")
        return 0
    ms = unanswered(pr, a.to) if a.unanswered else [m for m in messages(pr) if not a.to or m["to"] == a.to]
    for m in ms:
        print(f"{m['id']} {m['from']}->{m['to']} [{m['kind']}/{m['status']}/{m.get('channel')}]" +
              (f" re:{m['reply_to']}" if m.get("reply_to") else "") + f" {m['topic']}")
    return 0


def _legacy_who(v, people):
    who = re.sub(r"\s*\(.*\)\s*$", "", str(v or "")).strip()
    if who not in people:
        raise WFError(f"legacy participant not in plan: {who!r}")
    return who


def _legacy_kind(d):
    tag = f"{d.get('id', '')} {d.get('topic', '')}".lower()
    if "challenge" in tag:
        return "challenge"
    if re.search(r"\back\b", tag) and d.get("reply_to"):
        return "ack"
    return "completion" if "complet" in tag else "info"


LEGACY_SUMMARY_KEYS = ("summary", "resolution", "deliverable", "key_findings", "tool_outcomes", "limitations", "not_done")


def _legacy_body(d):
    if isinstance(d.get("body"), str) and d["body"].strip():
        return d["body"]
    lines = []
    for k in LEGACY_SUMMARY_KEYS:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            lines.append(f"{k}: {v.strip()}")
        elif isinstance(v, list):
            lines += [f"{k}: {x}" for x in v if isinstance(x, str) and x.strip()]
    return "\n".join(lines)[:20000] or "(legacy message had no body; see legacy.original)"


def _legacy_normalise(msg, rt_found):
    """Unresolvable reply_to never yields an answer kind with a null reply_to."""
    if msg["kind"] in ANSWERS and not rt_found:
        msg["kind"] = "info"
        msg["reply_to"] = None
        rt = msg["legacy"].get("reply_to")
        marker = f"legacy reply_to {rt!r} not found; downgraded from answer to info"
        if marker not in msg["unresolved"]:
            msg["unresolved"] = list(msg["unresolved"]) + [marker]
    if not (msg.get("body") or "").strip():
        msg["body"] = _legacy_body(msg["legacy"].get("original", {}))
    return msg


def cmd_migrate_legacy(pr, a):
    """Wrap non-schema mailbox JSON into schema messages (one per recipient); originals never modified. Dry-run unless --apply."""
    plan, roles = load_plan(pr)
    people = list(roles) + list(plan.get("external_participants", EXTERNAL))
    existing = [m for m in messages(pr) if m.get("legacy")]
    done = {(m["legacy"]["id"], m["to"]) for m in existing}
    known = {m["legacy"]["id"]: m["id"] for m in existing}
    todo, seq = [], 0
    for f in sorted(pr.messages.glob("*.json")):
        if MSG_ID_RE.match(f.stem) or f.is_symlink():
            continue
        d = load(f)
        if not isinstance(d, dict) or not d.get("id"):
            raise WFError(f"legacy file without id: {f.name}")
        pr.guard(json.dumps(d, ensure_ascii=False))
        for to in (d.get("to") if isinstance(d.get("to"), list) else [d.get("to")]):
            to = _legacy_who(to, people)
            if (d["id"], to) in done:
                continue
            mid = f"{now():%Y%m%dT%H%M%S}{seq:06d}Z-{secrets.token_hex(4)}"
            seq += 1
            known.setdefault(d["id"], mid)
            todo.append((f, d, to, mid))
    out = []
    for f, d, to, mid in todo:
        rt, st = d.get("reply_to"), str(d.get("status", ""))
        msg = {"schema_version": 1, "id": mid, "created_at": iso(), "from": _legacy_who(d.get("from"), people), "to": to,
               "kind": _legacy_kind(d), "channel": "file", "topic": str(d.get("topic", d["id"]))[:200],
               "status": "resolved" if st in ("closed", "resolved") else "open", "reply_to": known.get(rt) if rt else None,
               "evidence": d.get("evidence") if isinstance(d.get("evidence"), list) else [], "unresolved": d.get("unresolved") or [],
               "body": _legacy_body(d),
               "legacy": {"id": d["id"], "file": f.name, "status": st, "reply_to": rt, "kind_inferred": True,
                          "reply_to_unresolved": bool(rt and rt not in known), "original": d}}
        out.append(_legacy_normalise(msg, bool(not rt or rt in known)))
        print(f"{'import' if a.apply else 'would import'} {f.name} -> {mid} [{msg['kind']}/{msg['status']}] {msg['from']}->{to}"
              + (" (reply_to unresolved)" if msg["legacy"]["reply_to_unresolved"] else ""))
    repairs = []
    if a.repair:  # imported copies are operational (legacy files stay immutable provenance); fix schema violations in place
        ids = {m["id"] for m in messages(pr)}
        for m in existing:
            before = json.dumps(m, sort_keys=True)
            fixed = _legacy_normalise(json.loads(before), bool(m.get("reply_to") in ids))
            if json.dumps(fixed, sort_keys=True) != before:
                fixed["repaired_at"] = iso()
                repairs.append(fixed)
                print(f"{'repair' if a.apply else 'would repair'} {m['id']} -> kind {fixed['kind']}, body {'filled' if not m.get('body') else 'kept'}")
    if a.apply:
        with locked(pr):
            for m in out:
                atomic_write(pr.messages / f"{m['id']}.json", dump(m), exclusive=True)
            for m in repairs:
                atomic_write(pr.messages / f"{m['id']}.json", dump(m))
    print(f"{len(out)} legacy message(s), {len(repairs)} repair(s) {'applied' if a.apply else 'pending; rerun with --apply'}")
    return 0


def cmd_manifest(pr, a):
    plan, roles = load_plan(pr)
    role = get_role(roles, a.role)
    caller = pr.session_caller()
    if caller and caller != a.role:
        raise WFError(f"session cwd is bound to {caller}; manifest for {a.role} refused")
    mpath = pr.manifests / f"{a.role}.json"
    outs = []
    for rel in a.output:
        p = pr.safe(rel)
        if not owns(pr, role, rel) or p.is_symlink() or not p.is_file():
            raise WFError(f"{rel}: not an owned regular output file")
        outs.append({"path": rel, "sha256": sha256(p), "bytes": p.stat().st_size})
    miss = [r for r in role["required_outputs"] if r not in a.output]
    if miss:
        raise WFError(f"required outputs missing: {', '.join(miss)}")
    pr.guard(a.summary, *(a.unresolved or []))
    with locked(pr):
        att = current(load_reg(pr), a.role)
        if not att or att.get("launch_state") not in LAUNCHED:
            raise WFError(f"{a.role} has no launched attempt")
        atomic_write(mpath, dump({"schema_version": 1, "role": a.role, "status": "complete", "attempt_id": att["attempt_id"],
                                  "created_at": iso(), "summary": a.summary, "outputs": outs, "unresolved": a.unresolved or []}))
    print(f"manifest written for {a.role}; completion still requires native completed/idle")
    return 0


def cmd_accept(pr, a):
    plan, roles = load_plan(pr)
    role = get_role(roles, a.role)
    if a.by not in ACCEPTORS or not a.basis.strip():
        raise WFError(f"--by must be one of {ACCEPTORS} and --basis is required")
    pr.guard(a.basis)
    with locked(pr):
        att = current(load_reg(pr), a.role)
        st = nstate(native(pr), att)
        if not att or att.get("launch_state") not in LAUNCHED or st not in SUCCESS:
            raise WFError(f"{a.role}: acceptance needs a launched attempt with native completed/idle (now {st})")
        outs = []
        for r in role["required_outputs"]:
            p = pr.safe(r)
            if p.is_symlink() or not p.is_file():
                raise WFError(f"required output missing: {r}")
            outs.append({"path": r, "sha256": sha256(p)})
        atomic_write(pr.acceptance / f"{a.role}.json", dump({
            "schema_version": 1, "role": a.role, "decision": "accepted", "by": a.by, "attempt_id": att["attempt_id"], "created_at": iso(),
            "basis": a.basis, "open_challenges": [m["id"] for m in unanswered(pr, a.role, ("challenge",))], "outputs": outs}))
    print(f"accepted {a.role} attempt {att['attempt_id']} by {a.by}")
    return 0


def parser():
    ap = argparse.ArgumentParser(prog="workflow.py")
    ap.add_argument("--root")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--write", action="store_true"); p.add_argument("--overwrite", action="store_true")
    sub.add_parser("init")
    sub.add_parser("preflight")
    p = sub.add_parser("abandon"); p.add_argument("role"); p.add_argument("--reason", required=True)
    p = sub.add_parser("restart"); p.add_argument("role"); p.add_argument("--reason", required=True)
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--native-preflight", action="store_true")
    for name in ("dispatch", "resume"):
        p = sub.add_parser(name)
        p.add_argument("role", nargs="?" if name == "dispatch" else None)
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--native-preflight", action="store_true")
        if name == "dispatch":
            p.add_argument("--ready", action="store_true")
        else:
            p.add_argument("--message", action="append"); p.add_argument("--note")
    p = sub.add_parser("adopt"); p.add_argument("role"); p.add_argument("--native-id", required=True)
    p.add_argument("--reason", required=True); p.add_argument("--cwd-rel"); p.add_argument("--replace", action="store_true")
    p = sub.add_parser("status"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("message"); ms = p.add_subparsers(dest="action", required=True)
    s = ms.add_parser("send")
    s.add_argument("--from", dest="sender", required=True); s.add_argument("--to", required=True); s.add_argument("--topic", required=True)
    s.add_argument("--kind", default="info", choices=KINDS); s.add_argument("--status", default="open", choices=STATUSES)
    s.add_argument("--channel", default="file", choices=("file", "native")); s.add_argument("--body", default="")
    s.add_argument("--reply-to"); s.add_argument("--evidence", action="append"); s.add_argument("--unresolved", action="append")
    s.add_argument("--peer"); s.add_argument("--transport-result", choices=TRANSPORT_RESULTS)
    l = ms.add_parser("list"); l.add_argument("--to"); l.add_argument("--unanswered", action="store_true")
    p = sub.add_parser("manifest"); p.add_argument("role"); p.add_argument("--output", action="append", required=True)
    p.add_argument("--summary", default=""); p.add_argument("--unresolved", action="append")
    p = sub.add_parser("migrate-legacy"); p.add_argument("--apply", action="store_true"); p.add_argument("--repair", action="store_true")
    p = sub.add_parser("accept"); p.add_argument("role"); p.add_argument("--by", required=True); p.add_argument("--basis", required=True)
    return ap


def main(argv=None):
    a = parser().parse_args(argv)
    try:
        pr = Project(a.root or Path(__file__).resolve().parent.parent)
        if a.cmd in OPERATOR_ONLY and (a.cmd != "plan" or a.write) and pr.session_caller():
            raise WFError(f"`{a.cmd}` is operator-only; refused from a session cwd")
        return globals()[f"cmd_{a.cmd.replace('-', '_')}"](pr, a)
    except WFError as e:
        print(f"error: {e}", file=sys.stderr)
        return e.code


if __name__ == "__main__":
    sys.exit(main())
