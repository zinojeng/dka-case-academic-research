#!/usr/bin/env python3
"""Fake `claude` CLI for tests. State lives in $FAKE_CLAUDE_DIR/state.json; every call is logged to calls.jsonl.

Mimics observed native behaviour:
  * `--bg ... --name N -- prompt`  -> "backgrounded · <id> · <name>"
  * `--bg --resume <uuid> -- p`    -> "backgrounded · <id>"  (no name)
  * resume of a running session, or resume with extra launch flags -> starts a COPY with a new id
"""
import json, os, sys, uuid
from pathlib import Path

d = Path(os.environ["FAKE_CLAUDE_DIR"])
sp = d / "state.json"
state = json.loads(sp.read_text()) if sp.exists() else {"agents": [], "counter": 0}
argv = sys.argv[1:]
stdin_data = sys.stdin.read() if not sys.stdin.isatty() else "<tty>"
with open(d / "calls.jsonl", "a") as fh:
    fh.write(json.dumps({"argv": argv, "cwd": os.getcwd(), "stdin": stdin_data}) + "\n")


def save():
    sp.write_text(json.dumps(state))


def new_agent(name):
    state["counter"] += 1
    a = {"id": f"{state['counter']:08x}", "sessionId": str(uuid.uuid4()), "name": name, "state": "working",
         "kind": "background", "cwd": os.getcwd()}
    state["agents"].append(a)
    return a


if argv[:1] == ["agents"]:
    print(json.dumps(state["agents"]))
    sys.exit(0)
if argv[:1] == ["logs"]:
    print(f"log of {argv[1]}")
    sys.exit(0)
if "--bg" not in argv:
    sys.exit(f"fake: unsupported {argv}")
mode = state.get("launch_mode", "ok")
if mode == "fail":
    sys.stderr.write("fake: launch refused\n")
    sys.exit(1)
if mode == "untrusted":  # observed native message for a never-trusted cwd
    sys.stderr.write(f"Workspace not trusted. Run `claude` in {os.getcwd()} once and accept the trust prompt, then retry.\n")
    sys.exit(1)
if mode == "hang":  # CLI that never returns (timeout path)
    import time
    time.sleep(30)
if mode == "unlisted":  # prints an id but `claude agents` never lists it
    state["counter"] += 1
    save()
    print(f"backgrounded · {state['counter']:08x} · {argv[argv.index('--name') + 1]}")
    sys.exit(0)
if mode == "garbage":
    print("something unexpected")
    sys.exit(0)
if "--resume" in argv:
    sid = argv[argv.index("--resume") + 1]
    target = next((a for a in state["agents"] if a["sessionId"] == sid), None)
    extra = [x for x in argv if x.startswith("--") and x not in ("--bg", "--resume", "--")]
    if target is None:
        sys.exit("fake: no such session")
    if target["state"] in ("working", "blocked") or extra or mode == "copy":
        c = new_agent(target["name"])
        c["sessionId"] = str(uuid.uuid4())
        save()
        print(f"backgrounded · {c['id']}\n  session is already running; started a copy")
        sys.exit(0)
    target["state"] = "working"
    save()
    print(f"backgrounded · {target['id']}\n  claude agents             list sessions")
    sys.exit(0)
name = argv[argv.index("--name") + 1]
a = new_agent(name)
save()
print(f"backgrounded · {a['id']} · {name}\n  claude agents             list sessions\n  claude attach {a['id']}    open in this terminal")
