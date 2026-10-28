#!/usr/bin/env python3
"""Turn complete issue-50 logs into deterministic, canonical JSON."""
import hashlib
import json
import pathlib
import re
import sys

logdir, destination = map(pathlib.Path, sys.argv[1:3])

def text(name):
    return (logdir / name).read_text()

def stats(name):
    match = re.search(r"\[jit\] scanned=(\d+) compiled=(\d+) cache_used=(\d+) cache_full_rejects=(\d+)", text(name))
    if not match:
        raise SystemExit(f"missing JIT statistics in {name}")
    return dict(zip(("scanned", "compiled", "cache_used", "cache_full_rejects"), map(int, match.groups())))

line = text("vm.record.stdout").strip()
m = re.fullmatch(r"transitions=(\d+) ones=(\d+) tape_sha256=([0-9a-f]{64})", line)
if not m:
    raise SystemExit("malformed champion output")
if (int(m.group(1)), int(m.group(2))) != (47176870, 4098):
    raise SystemExit("champion result does not meet the frozen bar")
for arm in ("vm", "jit"):
    if text(f"{arm}.record.stdout") != text(f"{arm}.replay.stdout"):
        raise SystemExit(f"{arm} record/replay output differs")
if text("vm.record.stdout") != text("jit.record.stdout"):
    raise SystemExit("VM/JIT champion output differs")

anti_lines = text("antihydra.stdout").splitlines()
if len(anti_lines) != 3 or anti_lines[0] != "transitions=100000000 claim=null":
    raise SystemExit("Antihydra made a claim or did not reach the frozen bound")

def predicates(line, binding):
    prefix = binding + " "
    if not line.startswith(prefix):
        raise SystemExit(f"missing {binding} observer report")
    pairs = re.findall(r"(converged|stable|improving|oscillating|diverging|equilibrium)=(true|false)", line[len(prefix):])
    if len(pairs) != 6:
        raise SystemExit(f"incomplete {binding} observer report")
    return {key: value == "true" for key, value in pairs}

def digest(name):
    return hashlib.sha256((logdir / name).read_bytes()).hexdigest()

vm_trace_sha = text("vm.tape.sha256").split()[0]
jit_trace_sha = text("jit.tape.sha256").split()[0]
if vm_trace_sha != jit_trace_sha:
    raise SystemExit("VM/JIT trace tapes differ")
vm_stats = stats("vm.record.stderr")
jit_stats = stats("jit.record.stderr")
if vm_stats["compiled"] != 0 or jit_stats["compiled"] <= 0:
    raise SystemExit("VM/JIT tier evidence does not meet the frozen bar")

result = {
    "schema": "eigengauntlet.issue-50.v1",
    "eigenscript": "0.46.0",
    "champion": {
        "machine": "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA",
        "transitions": int(m.group(1)), "ones": int(m.group(2)),
        "final_tape_sha256": m.group(3),
        "stdout_sha256": digest("vm.record.stdout"),
        "trace_tape_sha256": vm_trace_sha,
        "record_replay_byte_identical": True,
        "vm_jit_output_byte_identical": True,
        "vm_jit_trace_tape_byte_identical": True,
        "vm_jit_stats": {"vm": vm_stats, "jit": jit_stats},
    },
    "antihydra": {
        "machine": "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA",
        "transitions": 100000000, "claim": None,
        "predicates_ungraded": {
            "signature_hash": predicates(anti_lines[1], "signature_hash"),
            "head_offset": predicates(anti_lines[2], "head_offset"),
        },
    },
}
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
