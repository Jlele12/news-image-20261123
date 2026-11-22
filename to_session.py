#!/usr/bin/env python3
"""Convert the Hermes delegation live log to a make.fun hand-over session JSON.

The harness keeps sessions as an append-only delegation log without
structured per-message records, so the entry is handed over: messages carry
no timestamps and no usage (the log does not record either).
"""
import json
import re
import sys

LOG = sys.argv[1]
OUT = sys.argv[2]

LINE = re.compile(r"^(\d\d:\d\d:\d\d) (\w+)\s*\| (.*)$")
ROLE = {"user": "user", "assistant": "assistant", "tool": "tool",
        "start": "system", "goal": "user"}

messages = []
cur_role = None
cur_buf = []
def flush():
    global cur_role, cur_buf
    if cur_role and cur_buf:
        text = "\n".join(cur_buf).strip()
        if text:
            messages.append({"role": cur_role, "content": text})
    cur_role, cur_buf = None, []

for raw in open(LOG, encoding="utf-8", errors="replace"):
    line = raw.rstrip("\n")
    if not line or set(line) <= {"=", " "}:
        continue
    m = LINE.match(line)
    if not m:
        if cur_buf and not cur_buf[-1].startswith("\x00CONT"):
            cur_buf.append("    " + line)
        continue
    _t, role, text = m.groups()
    if role == "start":
        flush(); continue
    new_role = ROLE.get(role, "assistant" if role.startswith(("think", "act")) else "tool")
    flush()
    cur_role = new_role
    cur_buf = [text]

flush()

session = {
    "session_id": "deleg_98f636bb-task1",
    "harness": "Hermes Agent",
    "harness_version": "1.x",
    "provider": "anthropic",
    "model": "claude-sonnet-4-5",
    "handed_over": "Hermes subagent sessions persist only as an append-only delegation log without structured per-message records, tool results or usage; exported verbatim as hand-over.",
    "messages": messages,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(session, f, ensure_ascii=False, indent=1)
print(f"{OUT}: {len(messages)} messages")
