#!/usr/bin/env python3
"""Focused tests for scripts/workflow.py against tests/fake_claude.py. Run: python3 -m unittest discover -s tests"""
import json, os, shutil, stat, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCRIPT = REPO / "scripts" / "workflow.py"
FAKE = HERE / "fake_claude.py"


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="wf test "))
        self.root = self.tmp / "案例 DKA  root"  # spaces + CJK like the real project
        (self.root / ".claude").mkdir(parents=True)
        shutil.copytree(REPO / ".claude" / "agents", self.root / ".claude" / "agents")
        shutil.copy(REPO / ".claude" / "settings.json", self.root / ".claude" / "settings.json")
        shutil.copy(REPO / ".gitignore", self.root / ".gitignore")
        (self.root / ".private").mkdir()
        servers = {s: {"command": "/usr/bin/true", "args": [], "env": {"KEY": f"secret-{s}"}}
                   for s in ("paper-search", "research_hub", "scihub", "llamaparse", "codebase-memory-mcp")}
        (self.root / ".private" / "mcp.local.json").write_text(json.dumps({"mcpServers": servers}))
        (self.root / ".private" / "case-brief.md").write_text("# de-identified brief\n")
        self.fake_dir = self.tmp / "fake"
        self.fake_dir.mkdir()
        os.chmod(FAKE, os.stat(FAKE).st_mode | stat.S_IXUSR)
        self.env = dict(os.environ, WORKFLOW_CLAUDE_BIN=str(FAKE), FAKE_CLAUDE_DIR=str(self.fake_dir))
        self.ok("plan", "--write")
        self.ok("init")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    # helpers -------------------------------------------------------------
    def wf(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args], env=self.env, cwd=cwd,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True)

    def ok(self, *args):
        p = self.wf(*args)
        self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
        return p

    def calls(self):
        f = self.fake_dir / "calls.jsonl"
        return [json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []

    def launches(self):
        return [c for c in self.calls() if "--bg" in c["argv"]]

    def state(self):
        return json.loads((self.fake_dir / "state.json").read_text())

    def set_native(self, name, value):
        s = self.state()
        for a in s["agents"]:
            if a["name"] == name:
                a["state"] = value
        (self.fake_dir / "state.json").write_text(json.dumps(s))

    def set_mode(self, mode):
        s = self.state() if (self.fake_dir / "state.json").exists() else {"agents": [], "counter": 0}
        s["launch_mode"] = mode
        (self.fake_dir / "state.json").write_text(json.dumps(s))

    def registry(self):
        return json.loads((self.root / "runtime" / "registry.json").read_text())

    def finish(self, role, display, files):
        for f in files:
            p = self.root / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"# {f}\nDay0 de-identified\n")
        self.set_native(display, "done")
        self.ok("manifest", role, "--summary", "done", *sum((["--output", f] for f in files), []))

    def send(self, *args):
        p = self.wf("message", "send", *args)
        return p, (p.stdout.split()[1] if p.returncode == 0 else None)

    def complete_case_analyst(self):
        self.ok("dispatch", "case-analyst")
        self.finish("case-analyst", "DKA case analyst Opus55",
                    ["reports/case-analyst/case-timeline.md", "reports/case-analyst/data-gaps.md"])

    # tests -----------------------------------------------------------------
    def test_dispatch_argv_and_registry(self):
        self.ok("dispatch", "case-analyst")
        (call,) = self.launches()
        argv = call["argv"]
        self.assertEqual(argv[-2], "--", "bare -- must precede the positional prompt")
        self.assertTrue(argv[-1].startswith("你是"))
        self.assertEqual(argv[argv.index("--model") + 1], "claude-opus-5-5")
        self.assertNotIn("--fallback-model", argv)
        self.assertIn("--strict-mcp-config", argv)
        mcp = argv[argv.index("--mcp-config") + 1]
        self.assertTrue(argv[argv.index("--mcp-config") + 2].startswith("--"), "variadic --mcp-config must take one path")
        self.assertEqual(Path(mcp), (self.root / "runtime/mcp/case-analyst.json").resolve())
        self.assertEqual(json.loads(Path(mcp).read_text()), {"mcpServers": {}})
        self.assertEqual(oct(os.stat(mcp).st_mode & 0o777), "0o600")
        self.assertEqual(Path(argv[argv.index("--add-dir") + 1]), self.root.resolve())
        self.assertEqual(Path(call["cwd"]).resolve(), (self.root / "sessions/case-analyst").resolve())
        self.assertEqual(call["stdin"], "", "stdin must be DEVNULL")
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "auto")
        settings = argv[argv.index("--settings") + 1]
        self.assertEqual(Path(settings), (self.root / ".claude/settings.json").resolve(), "root settings bound explicitly")
        self.assertEqual(json.loads(Path(settings).read_text())["worktree"]["bgIsolation"], "none")
        self.assertLess(argv.index("--settings"), argv.index("--"))
        self.assertEqual(argv[argv.index("--setting-sources") + 1], "", "user/local settings must not leak into role launches")
        att = self.registry()["roles"]["case-analyst"][-1]
        self.assertEqual(att["launch_state"], "launched")
        self.assertRegex(att["session_id"], r"^[0-9a-f-]{36}$")
        self.assertNotIn("secret-", (self.root / "runtime/registry.json").read_text())
        p = self.wf("dispatch", "case-analyst")
        self.assertNotEqual(p.returncode, 0, "second dispatch of a live role must be refused")

    def test_scoped_mcp_and_per_server_rules(self):
        self.complete_case_analyst()
        p = self.ok("dispatch", "evidence-librarian")
        self.assertNotIn("secret-", p.stdout + p.stderr, "credential values must never be printed")
        argv = self.launches()[-1]["argv"]
        cfg = json.loads((self.root / "runtime/mcp/evidence-librarian.json").read_text())
        self.assertEqual(set(cfg["mcpServers"]), {"paper-search", "research_hub", "scihub", "llamaparse"})
        allowed = argv[argv.index("--allowedTools") + 1:argv.index("--disallowedTools")]
        for s in ("paper-search", "research_hub", "scihub", "llamaparse"):
            self.assertIn(f"mcp__{s}", allowed)
            self.assertIn(f"mcp__{s}__*", allowed)
        self.assertNotIn("mcp__*", allowed)
        self.assertFalse(any("codebase-memory" in t for t in allowed))
        denied = argv[argv.index("--disallowedTools") + 1:argv.index("--")]
        self.assertTrue(any(t.endswith("/[0-9]*.md)") and t.startswith("Read(") for t in denied))

    def test_dependency_and_completion_gates(self):
        p = self.wf("dispatch", "electrolyte-specialist")
        self.assertEqual(p.returncode, 4, p.stderr)
        self.ok("dispatch", "case-analyst")
        for f in ("case-timeline.md", "data-gaps.md"):  # reports existing alone are not completion
            (self.root / "reports/case-analyst" / f).write_text("x\n")
        self.assertEqual(self.wf("dispatch", "electrolyte-specialist").returncode, 4)
        files = ["reports/case-analyst/case-timeline.md", "reports/case-analyst/data-gaps.md"]
        self.ok("manifest", "case-analyst", *sum((["--output", f] for f in files), []))
        self.assertEqual(self.wf("dispatch", "electrolyte-specialist").returncode, 4, "native still working")
        self.set_native("DKA case analyst Opus55", "done")
        _, cid = self.send("--from", "red-team-reviewer", "--to", "case-analyst", "--kind", "challenge", "--topic", "unit?")
        self.assertEqual(self.wf("dispatch", "electrolyte-specialist").returncode, 4, "unanswered challenge blocks")
        self.send("--from", "case-analyst", "--to", "red-team-reviewer", "--kind", "response", "--topic", "mg/dL assumed", "--reply-to", cid)
        (self.root / "reports/case-analyst/data-gaps.md").write_text("tampered\n")
        self.assertEqual(self.wf("dispatch", "electrolyte-specialist").returncode, 4, "hash change invalidates manifest")
        self.ok("accept", "case-analyst", "--by", "codex", "--basis", "reviewed")
        self.ok("dispatch", "electrolyte-specialist")
        st = json.loads(self.ok("status", "--json").stdout)
        row = {r["role"]: r for r in st["roles"]}
        self.assertTrue(row["case-analyst"]["complete"])
        self.assertFalse(row["electrolyte-specialist"]["complete"])
        self.assertEqual(self.wf("accept", "case-analyst", "--by", "case-analyst", "--basis", "x").returncode, 2)

    def test_mailbox_reply_to_atomic(self):
        p, mid = self.send("--from", "electrolyte-specialist", "--to", "fluid-insulin-specialist", "--kind", "challenge",
                           "--topic", "Na tonicity", "--body", "chem Na vs gas Na", "--evidence", "DOI 10.2337/dci24-0032")
        self.assertEqual(p.returncode, 0, p.stderr)
        msg = json.loads((self.root / "coordination/messages" / f"{mid}.json").read_text())
        for k in ("from", "to", "topic", "evidence", "status", "reply_to", "kind", "channel"):
            self.assertIn(k, msg)
        self.assertFalse([f for f in os.listdir(self.root / "coordination/messages") if f.startswith(".tmp")])
        self.assertNotEqual(self.send("--from", "fluid-insulin-specialist", "--to", "electrolyte-specialist", "--kind", "ack",
                                      "--topic", "ack")[0].returncode, 0, "ack needs reply_to")
        self.assertNotEqual(self.send("--from", "fluid-insulin-specialist", "--to", "electrolyte-specialist", "--kind", "ack",
                                      "--topic", "ack", "--reply-to", "../../etc/passwd")[0].returncode, 0)
        self.assertIn(mid, self.ok("message", "list", "--unanswered").stdout)
        self.send("--from", "fluid-insulin-specialist", "--to", "electrolyte-specialist", "--kind", "ack", "--topic", "ack", "--reply-to", mid)
        self.assertNotIn(mid, self.ok("message", "list", "--unanswered").stdout)
        self.assertNotEqual(self.send("--from", "codex", "--to", "case-analyst", "--topic", "x",
                                      "--body", f"see {self.root}/x")[0].returncode, 0, "absolute local path refused")
        self.assertNotEqual(self.send("--from", "nobody", "--to", "codex", "--topic", "x")[0].returncode, 0)
        t = ["--from", "case-analyst", "--to", "codex", "--kind", "transport", "--channel", "native",
             "--peer", "DKA electrolytes Opus55", "--transport-result", "delivered", "--topic", "native preflight"]
        self.assertEqual(self.send(*t)[0].returncode, 0)
        self.assertEqual(self.send(*t)[0].returncode, 0)
        self.assertNotEqual(self.send(*t)[0].returncode, 0, "max 2 native exchanges per peer")

    def test_resume_rules_and_copy_detection(self):
        self.ok("dispatch", "case-analyst")
        _, mid = self.send("--from", "codex", "--to", "case-analyst", "--kind", "request", "--topic", "rework")
        n = len(self.launches())
        p = self.wf("resume", "case-analyst", "--message", mid)
        self.assertEqual(p.returncode, 5, "running session must be refused, not copied")
        self.assertEqual(len(self.launches()), n, "no launch attempted for a running session")
        self.set_native("DKA case analyst Opus55", "completed")
        self.assertNotEqual(self.wf("resume", "case-analyst").returncode, 0, "resume needs a message")
        self.ok("resume", "case-analyst", "--message", mid)
        argv = self.launches()[-1]["argv"]
        sid = self.registry()["roles"]["case-analyst"][0]["session_id"]
        self.assertEqual(argv[:5], ["--bg", "--resume", sid, "--", argv[4]], "resume argv must carry no extra flags")
        self.assertEqual(len(argv), 5)
        att = self.registry()["roles"]["case-analyst"][-1]
        self.assertEqual((att["kind"], att["launch_state"]), ("resume", "launched"), "name-less resume output parsed")
        self.set_native("DKA case analyst Opus55", "done")
        self.set_mode("copy")
        p = self.wf("resume", "case-analyst", "--message", mid)
        self.assertEqual(p.returncode, 5, p.stderr)
        self.assertIn("copy", p.stderr)
        self.assertEqual(self.registry()["roles"]["case-analyst"][-1]["launch_state"], "resume_created_copy")

    def test_path_safety(self):
        self.assertNotEqual(self.wf("dispatch", "../evil").returncode, 0)
        self.ok("dispatch", "case-analyst")
        for bad in ("../../etc/passwd", "/etc/passwd", "reports/electrolytes.md", "~/x"):
            self.assertNotEqual(self.wf("manifest", "case-analyst", "--output", bad).returncode, 0, bad)
        outside = self.tmp / "outside.md"
        outside.write_text("x")
        os.symlink(outside, self.root / "reports/case-analyst/case-timeline.md")
        (self.root / "reports/case-analyst/data-gaps.md").write_text("x")
        p = self.wf("manifest", "case-analyst", "--output", "reports/case-analyst/case-timeline.md",
                    "--output", "reports/case-analyst/data-gaps.md")
        self.assertNotEqual(p.returncode, 0, "symlink escaping owned dir refused")
        plan = json.loads((self.root / "coordination/workflow-plan.json").read_text())
        plan["roles"][0]["owned_outputs"] = ["../outside"]
        (self.root / "coordination/workflow-plan.json").write_text(json.dumps(plan))
        self.assertNotEqual(self.wf("plan").returncode, 0)
        plan["roles"][0]["owned_outputs"] = ["reports/case-analyst"]
        plan["model"] = "claude-sonnet-5-5"
        (self.root / "coordination/workflow-plan.json").write_text(json.dumps(plan))
        self.assertNotEqual(self.wf("plan").returncode, 0, "model must stay pinned")

    def test_failed_launch_no_fallback(self):
        self.set_mode("fail")
        p = self.wf("dispatch", "case-analyst")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(len(self.launches()), 1, "no retry/fallback launch")
        att = self.registry()["roles"]["case-analyst"][-1]
        self.assertEqual(att["launch_state"], "launch_failed")
        self.assertTrue((self.root / att["log"]).is_file())
        self.set_mode("garbage")
        self.assertEqual(self.wf("dispatch", "case-analyst").returncode, 2)
        self.assertEqual(self.registry()["roles"]["case-analyst"][-1]["launch_state"], "launch_unparsed")
        self.set_mode("ok")
        self.ok("dispatch", "case-analyst")
        self.env["WORKFLOW_CLAUDE_BIN"] = str(self.tmp / "missing-claude")
        self.assertEqual(self.wf("status").returncode, 0, "status degrades to closed gates")
        self.assertIn("native status unavailable", self.wf("status").stdout)

    def test_untrusted_workspace_detected_and_preserved(self):
        self.set_mode("untrusted")
        p = self.wf("dispatch", "case-analyst")
        self.assertEqual(p.returncode, 6, p.stderr)
        self.assertIn("trust", p.stderr)
        self.assertIn("sessions/case-analyst", p.stderr)
        self.assertEqual(len(self.launches()), 1, "no automatic retry or trust bypass")
        self.assertFalse(any(x in self.launches()[0]["argv"] for x in ("--dangerously-skip-permissions", "-p", "--print")))
        self.assertIn("previous launch was untrusted", self.ok("preflight").stdout)
        self.set_mode("ok")
        self.ok("dispatch", "case-analyst")
        states = [a["launch_state"] for a in self.registry()["roles"]["case-analyst"]]
        self.assertEqual(states, ["launch_untrusted", "launched"], "failed attempt kept for audit")

    def test_settings_required(self):
        (self.root / ".claude/settings.json").write_text(json.dumps({"worktree": {"bgIsolation": "worktree"}}))
        p = self.wf("dispatch", "case-analyst")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("bgIsolation", p.stderr)
        self.assertEqual(self.launches(), [], "no launch without validated settings")
        (self.root / ".claude/settings.json").unlink()
        self.assertNotEqual(self.wf("init").returncode, 0)

    def test_restart_terminal_uncompleted(self):
        self.ok("dispatch", "case-analyst")
        first = self.registry()["roles"]["case-analyst"][0]
        p = self.wf("restart", "case-analyst", "--reason", "relaunch with --settings")
        self.assertEqual(p.returncode, 5, "running/blocked must be stopped first")
        self.assertIn("claude stop", p.stderr)
        self.assertNotEqual(self.wf("restart", "case-analyst").returncode, 0, "reason required")
        self.set_native("DKA case analyst Opus55", "stopped")
        self.ok("restart", "case-analyst", "--reason", "relaunch with --settings")
        atts = self.registry()["roles"]["case-analyst"]
        self.assertEqual(atts[0], first, "prior attempt preserved unchanged")
        self.assertEqual((atts[1]["kind"], atts[1]["replaces_attempt"], atts[1]["replaced_native_state"]),
                         ("restart", first["attempt_id"], "stopped"))
        argv = self.launches()[-1]["argv"]
        self.assertIn("--settings", argv)
        self.assertNotIn("--resume", argv, "restart is a fresh launch, not a resume")
        self.finish("case-analyst", "DKA case analyst Opus55",
                    ["reports/case-analyst/case-timeline.md", "reports/case-analyst/data-gaps.md"])
        self.assertNotEqual(self.wf("restart", "case-analyst", "--reason", "x").returncode, 0, "complete role refused")

    def test_shared_cwd_mode(self):
        plan = json.loads((self.root / "coordination/workflow-plan.json").read_text())
        plan["session_cwd"] = "shared"
        (self.root / "coordination/workflow-plan.json").write_text(json.dumps(plan))
        self.ok("dispatch", "case-analyst")
        call = self.launches()[-1]
        self.assertEqual(Path(call["cwd"]).resolve(), self.root.resolve())
        self.assertIn("Bash(python3 scripts/workflow.py manifest case-analyst *)", call["argv"])
        self.assertEqual(self.registry()["roles"]["case-analyst"][-1]["cwd_rel"], ".")
        plan["session_cwd"] = "elsewhere"
        (self.root / "coordination/workflow-plan.json").write_text(json.dumps(plan))
        self.assertNotEqual(self.wf("plan").returncode, 0)

    def test_adopt_and_legacy_migration(self):
        s = {"agents": [{"id": "f99a0ad5", "sessionId": "f99a0ad5-1111-2222-3333-444455556666", "name": "DKA electrolytes Opus55",
                         "state": "done", "cwd": str(self.root)}], "counter": 0}
        (self.fake_dir / "state.json").write_text(json.dumps(s))
        self.assertNotEqual(self.wf("adopt", "fluid-insulin-specialist", "--native-id", "f99a0ad5", "--reason", "x").returncode, 0,
                            "name mismatch refused")
        self.ok("adopt", "electrolyte-specialist", "--native-id", "f99a0ad5", "--reason", "launched directly by Codex")
        self.assertEqual(self.launches(), [], "adopt never launches")
        msgs = self.root / "coordination/messages"
        (msgs / "electrolytes-ELEC-CH1-to-fluid-insulin.json").write_text(json.dumps(
            {"id": "ELEC-CH1", "from": "electrolyte-specialist (DKA electrolytes Opus55)", "to": "fluid-insulin-specialist (x)",
             "topic": "Challenge: Na", "status": "closed", "reply_to": None, "evidence": ["e"]}))
        (msgs / "fi-ack.json").write_text(json.dumps(
            {"id": "fi-ack-ELEC-CH1", "from": "fluid-insulin-specialist", "to": "electrolyte-specialist", "topic": "ACK to ELEC-CH1",
             "status": "closed", "reply_to": "ELEC-CH1", "body": "ok"}))
        (msgs / "lib-multi.json").write_text(json.dumps(
            {"id": "LIB-1", "from": "evidence-librarian", "to": ["codex", "synthesis-editor"], "topic": "completion: ledger", "status": "sent"}))
        before = {f.name: f.read_text() for f in msgs.iterdir()}
        self.assertIn("would import", self.ok("migrate-legacy").stdout)
        self.ok("migrate-legacy", "--apply")
        self.assertIn("0 legacy", self.ok("migrate-legacy").stdout, "idempotent")
        for name, text in before.items():
            self.assertEqual((msgs / name).read_text(), text, "legacy originals untouched")
        new = [json.loads(f.read_text()) for f in msgs.glob("2*.json")]
        by = {m["legacy"]["id"]: m for m in new}
        self.assertEqual(by["fi-ack-ELEC-CH1"]["reply_to"], by["ELEC-CH1"]["id"])
        self.assertEqual(by["ELEC-CH1"]["kind"], "challenge")
        self.assertEqual(sorted(m["to"] for m in new if m["legacy"]["id"] == "LIB-1"), ["codex", "synthesis-editor"])
        (self.root / "reports/electrolytes.md").write_text("legacy report\n")
        self.ok("accept", "electrolyte-specialist", "--by", "codex", "--basis", "legacy report reviewed")
        row = {r["role"]: r for r in json.loads(self.ok("status", "--json").stdout)["roles"]}
        self.assertTrue(row["electrolyte-specialist"]["complete"], row["electrolyte-specialist"])


    def test_single_file_edit_rules(self):
        self.complete_case_analyst()
        self.ok("dispatch", "electrolyte-specialist")
        argv = self.launches()[-1]["argv"]
        r = "/" + str(self.root.resolve())
        self.assertIn(f"Edit({r}/reports/electrolytes.md)", argv, "single-file output needs an exact rule")
        self.assertIn(f"Edit({r}/reports/electrolyte-specialist/**)", argv)
        self.assertFalse(any("electrolytes.md/**" in t for t in argv))
        self.assertIn("Bash(python3 ../../scripts/workflow.py message send --from electrolyte-specialist *)", argv)
        self.assertIn("Bash(python3 ../../scripts/workflow.py manifest electrolyte-specialist *)", argv)
        self.assertFalse(any(t == "Bash(python3 ../../scripts/workflow.py manifest *)" for t in argv))
        sys.path.insert(0, str(SCRIPT.parent))
        import workflow
        pr = workflow.Project(self.root)
        self.assertEqual(workflow.edit_rule(pr, "reports/reviews/clinical-review.md"), f"Edit({r}/reports/reviews/clinical-review.md)")
        self.assertEqual(workflow.edit_rule(pr, "reports/synthesis-editor"), f"Edit({r}/reports/synthesis-editor/**)")

    def test_session_identity_binding(self):
        self.ok("dispatch", "case-analyst")
        sess = self.root / "sessions" / "case-analyst"
        _, cid = self.send("--from", "red-team-reviewer", "--to", "case-analyst", "--kind", "challenge", "--topic", "q")
        def send_as(*args):
            return self.wf("message", "send", *args, cwd=sess)
        self.assertNotEqual(send_as("--from", "codex", "--to", "case-analyst", "--topic", "spoof").returncode, 0)
        self.assertNotEqual(send_as("--from", "codex", "--to", "red-team-reviewer", "--kind", "ruling", "--topic", "x",
                                    "--reply-to", cid).returncode, 0, "cannot impersonate codex")
        self.assertNotEqual(send_as("--from", "case-analyst", "--to", "red-team-reviewer", "--kind", "ruling", "--topic", "x",
                                    "--reply-to", cid).returncode, 0, "workers cannot rule")
        self.assertNotEqual(send_as("--from", "case-analyst", "--to", "codex", "--kind", "challenge", "--status", "resolved",
                                    "--topic", "x").returncode, 0, "no self-resolved challenge")
        self.assertNotEqual(self.send("--from", "fluid-insulin-specialist", "--to", "red-team-reviewer", "--kind", "response",
                                      "--topic", "x", "--reply-to", cid)[0].returncode, 0, "third party cannot answer")
        self.assertEqual(send_as("--from", "case-analyst", "--to", "red-team-reviewer", "--kind", "response", "--topic", "ok",
                                 "--reply-to", cid).returncode, 0)
        p = self.wf("manifest", "electrolyte-specialist", "--output", "reports/electrolytes.md", cwd=sess)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("bound to case-analyst", p.stderr)
        for cmd in (["dispatch", "electrolyte-specialist"], ["accept", "case-analyst", "--by", "codex", "--basis", "x"],
                    ["restart", "case-analyst", "--reason", "x"], ["plan", "--write", "--overwrite"]):
            self.assertIn("operator-only", self.wf(*cmd, cwd=sess).stderr, cmd)
        self.assertEqual(self.wf("plan", cwd=sess).returncode, 0, "read-only plan validation allowed")

    def test_unverified_and_timeout_need_abandon(self):
        self.set_mode("unlisted")
        self.assertEqual(self.wf("dispatch", "case-analyst").returncode, 3)
        self.assertEqual(self.registry()["roles"]["case-analyst"][-1]["launch_state"], "launch_unverified")
        self.set_mode("ok")
        p = self.wf("dispatch", "case-analyst")
        self.assertNotEqual(p.returncode, 0, "no silent retry that could duplicate a worker")
        self.assertIn("abandon", p.stderr)
        self.assertEqual(self.wf("restart", "case-analyst", "--reason", "x").returncode, 5)
        self.assertNotEqual(self.wf("abandon", "case-analyst").returncode, 0, "reason required")
        self.ok("abandon", "case-analyst", "--reason", "checked claude agents: no worker")
        self.ok("dispatch", "case-analyst")
        states = [a["launch_state"] for a in self.registry()["roles"]["case-analyst"]]
        self.assertEqual(states, ["launch_unverified", "abandoned", "launched"])
        self.set_native("DKA case analyst Opus55", "stopped")
        self.set_mode("hang")
        self.env["WORKFLOW_LAUNCH_TIMEOUT"] = "1"
        self.assertEqual(self.wf("restart", "case-analyst", "--reason", "timeout probe").returncode, 7)
        self.assertEqual(self.registry()["roles"]["case-analyst"][-1]["launch_state"], "launch_timeout")
        self.set_mode("ok")
        self.assertIn("abandon", self.wf("dispatch", "case-analyst").stderr)

    def test_legacy_unresolved_reply_and_repair(self):
        msgs = self.root / "coordination/messages"
        (msgs / "lib-ack.json").write_text(json.dumps(
            {"id": "LIB-ACK", "from": "evidence-librarian", "to": "codex", "topic": "ACK withheld", "reply_to": "MISSING-1",
             "status": "sent", "key_findings": ["ledger verified"], "tool_outcomes": ["llamaparse ok"]}))
        self.ok("migrate-legacy", "--apply")
        (m,) = [json.loads(f.read_text()) for f in msgs.glob("2*.json")]
        self.assertEqual((m["kind"], m["reply_to"]), ("info", None))
        self.assertTrue(any("MISSING-1" in u for u in m["unresolved"]))
        self.assertIn("key_findings: ledger verified", m["body"])
        self.assertIn("tool_outcomes: llamaparse ok", m["body"])
        broken = dict(m, id="20261028T000000000000Z-deadbeef", kind="ack", body="", unresolved=[])
        broken["legacy"] = dict(m["legacy"], id="LIB-OLD")
        (msgs / f"{broken['id']}.json").write_text(json.dumps(broken))
        self.assertIn("would repair", self.ok("migrate-legacy", "--repair").stdout)
        self.ok("migrate-legacy", "--repair", "--apply")
        fixed = json.loads((msgs / f"{broken['id']}.json").read_text())
        self.assertEqual(fixed["kind"], "info")
        self.assertTrue(fixed["body"] and fixed.get("repaired_at"))
        self.assertEqual(json.loads((msgs / "lib-ack.json").read_text())["id"], "LIB-ACK", "legacy original immutable")

    def test_ready_dry_run_wording_and_collision(self):
        p = self.ok("dispatch", "--ready", "--dry-run")
        self.assertIn("would dispatch: case-analyst", p.stdout)
        self.assertEqual(self.launches(), [])
        sys.path.insert(0, str(SCRIPT.parent))
        import workflow
        f = self.root / "coordination/messages/x.json"
        workflow.atomic_write(f, "{}", exclusive=True)
        with self.assertRaises(workflow.WFError):
            workflow.atomic_write(f, "{}", exclusive=True)


    def test_private_denies_keep_case_brief_readable(self):
        import fnmatch
        priv = self.root / ".private"
        (priv / "notes.md").write_text("canary")
        (priv / "archive").mkdir()
        (priv / "archive" / "old.md").write_text("canary")
        self.ok("dispatch", "case-analyst")
        argv = self.launches()[-1]["argv"]
        denied = argv[argv.index("--disallowedTools") + 1:argv.index("--")]
        r = "/" + str(self.root.resolve())
        self.assertIn(f"Read({r}/.private/notes.md)", denied)
        self.assertIn(f"Read({r}/.private/archive/**)", denied)
        self.assertIn(f"Read({r}/.private/mcp.local.json)", denied)
        self.assertNotIn(f"Read({r}/.private/*/**)", denied, "broad wildcard denied case-brief.md itself")
        brief = f"{r}/.private/case-brief.md"
        for rule in denied:
            if rule.startswith("Read("):
                pat = rule[5:-1].replace("/**", "/*")
                self.assertFalse(fnmatch.fnmatchcase(brief, pat) and "/.private/" in pat, f"{rule} would deny case-brief.md")

    def test_resume_refused_when_done_but_pid_live(self):
        self.ok("dispatch", "case-analyst")
        _, mid = self.send("--from", "codex", "--to", "case-analyst", "--kind", "request", "--topic", "rewrite")
        s = self.state()
        s["agents"][0].update(state="done", pid=os.getpid())  # listed live process
        (self.fake_dir / "state.json").write_text(json.dumps(s))
        n = len(self.launches())
        p = self.wf("resume", "case-analyst", "--message", mid)
        self.assertEqual(p.returncode, 5, p.stderr)
        self.assertIn("still live", p.stderr)
        self.assertIn("claude attach", p.stderr)
        self.assertEqual(len(self.launches()), n, "no CLI resume while the pid is live")
        s["agents"][0].update(pid=2 ** 22 + 12345)  # stale pid -> treated as gone
        (self.fake_dir / "state.json").write_text(json.dumps(s))
        self.ok("resume", "case-analyst", "--message", mid)

    def test_adopt_replace_copy(self):
        self.ok("dispatch", "case-analyst")
        _, mid = self.send("--from", "codex", "--to", "case-analyst", "--kind", "request", "--topic", "rewrite")
        self.set_native("DKA case analyst Opus55", "done")
        self.set_mode("copy")
        self.assertEqual(self.wf("resume", "case-analyst", "--message", mid).returncode, 5)
        self.set_mode("ok")
        atts = self.registry()["roles"]["case-analyst"]
        copy_id, src_id = atts[-1]["native_id"], atts[0]["native_id"]
        self.assertNotEqual(self.wf("adopt", "case-analyst", "--native-id", copy_id, "--reason", "x").returncode, 0,
                            "plain adopt refuses when a session is registered")
        self.assertNotEqual(self.wf("adopt", "case-analyst", "--replace", "--native-id", src_id, "--reason", "x").returncode, 0,
                            "explicit target must be the recorded copy")
        s = self.state()
        for ag in s["agents"]:
            if ag["id"] == src_id:
                ag.update(state="idle", pid=os.getpid())
        (self.fake_dir / "state.json").write_text(json.dumps(s))
        cw = ["--cwd-rel", "sessions/case-analyst"]  # the copy runs in the source session's cwd
        p = self.wf("adopt", "case-analyst", "--replace", "--native-id", copy_id, "--reason", "accept copy for rewrite", *cw)
        self.assertEqual(p.returncode, 5, "old source with live pid must be stopped first")
        self.set_native("DKA case analyst Opus55", "stopped")
        s = self.state()
        for ag in s["agents"]:
            ag.pop("pid", None)
        (self.fake_dir / "state.json").write_text(json.dumps(s))
        self.ok("adopt", "case-analyst", "--replace", "--native-id", copy_id, "--reason", "accept copy for rewrite", *cw)
        new = self.registry()["roles"]["case-analyst"]
        self.assertEqual(new[:len(atts)], atts, "history preserved")
        last = new[-1]
        self.assertEqual((last["kind"], last["native_id"], last["replaces_native_id"], last["replaced_state"]),
                         ("adopt-replace", copy_id, src_id, "resume_created_copy"))
        self.assertNotEqual(self.wf("adopt", "case-analyst", "--replace", "--native-id", copy_id, "--reason", "x").returncode, 0,
                            "no second replace once adopted")


class ShippedContractTest(unittest.TestCase):
    """The tracked plan is canonical: defaults, agents and docs must agree with it."""

    def setUp(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import workflow
        self.w = workflow
        self.pr = workflow.Project(REPO)
        self.plan = json.loads((REPO / "coordination/workflow-plan.json").read_text(encoding="utf-8"))
        self.roles = workflow.validate_plan(self.pr, self.plan)

    def test_shipped_plan_and_default_contracts_match(self):
        default = {r["name"]: r for r in self.w.default_plan()["roles"]}
        self.assertEqual(set(default), set(self.roles))
        for n, r in self.roles.items():
            for k in ("owned_outputs", "required_outputs", "depends_on", "mcp_servers"):
                self.assertEqual(r[k], default[n][k], f"{n}.{k}")
        self.assertEqual(self.plan["model"], "claude-opus-5-5")
        self.w.validate_plan(self.pr, self.w.default_plan())

    def test_shipped_tasks_reference_only_plan_outputs(self):
        import re
        outputs = {o for r in self.roles.values() for o in r["owned_outputs"] + r["required_outputs"]}
        self.assertEqual(self.plan.get("session_cwd"), "isolated")
        for n, r in self.roles.items():
            for tok in re.findall(r"(?:reports|evidence)/[A-Za-z0-9_./-]*", r.get("task", "")):
                self.assertIn(tok, outputs, f"{n} task names {tok} outside plan outputs")

    def test_peers_derived_from_roles(self):
        peers = self.w.peer_names(self.plan, self.roles)
        self.assertNotIn("peers", self.plan["native_messaging"])
        for role, name in peers.items():
            self.assertEqual(name, self.roles[role]["display_name"])
        text = self.w.preflight_text(self.plan, self.roles, "case-analyst", "x")
        self.assertIn(self.roles["evidence-librarian"]["display_name"], text)

    def test_agents_and_docs_do_not_redeclare_outputs(self):
        self.w.load_agents(self.pr, self.roles)
        outputs = {o for r in self.roles.values() for o in r["owned_outputs"] + r["required_outputs"]}
        allowed_refs = {"CLAUDE.md", ".private/case-brief.md", ".private/mcp.local.json", "coordination/workflow-plan.json"}
        import re
        for f in (REPO / ".claude/agents").glob("*.md"):
            for tok in re.findall(r"[A-Za-z0-9_./-]+\.(?:md|json)", f.read_text(encoding="utf-8")):
                self.assertTrue(tok in allowed_refs or tok.startswith("docs/") or tok in outputs, f"{f.name}: {tok}")
        for doc in ("docs/workflow.md", "docs/research-protocol.md", "README.md"):
            for tok in re.findall(r"(?:reports|evidence)/[A-Za-z0-9_./<>-]*", (REPO / doc).read_text(encoding="utf-8")):
                tok = tok.rstrip("/.")
                ok = "<" in tok or tok in outputs or any(tok.startswith(o + "/") for o in outputs) or tok in ("reports", "evidence")
                self.assertTrue(ok, f"{doc}: {tok} not in plan contracts")


class ParseLaunchTest(unittest.TestCase):
    def test_name_optional(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import workflow
        self.assertEqual(workflow.parse_launch("backgrounded · 9e500543 · DKA x Opus55\n  claude agents"), ("9e500543", "DKA x Opus55"))
        self.assertEqual(workflow.parse_launch("backgrounded · 9e500543\n  claude agents  list sessions")[0], "9e500543")
        self.assertEqual(workflow.parse_launch("backgrounded · 9e500543")[0], "9e500543")
        self.assertIsNone(workflow.parse_launch("error: nope"))


if __name__ == "__main__":
    unittest.main()
