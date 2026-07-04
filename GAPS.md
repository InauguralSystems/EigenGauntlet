# EigenScript Gaps Found By EigenGauntlet

Policy: no downstream workaround is considered a fix. If a workload exposes a
missing primitive or runtime bug, record it here and fix EigenScript at the root.

## Open

(none)

## Resolved upstream — verified

- 2026-06-29 → **FIXED (verified 2026-07-03)**: the minimal repro passes
  against EigenScript main (`total=42 id=7`, keys intact) — closed by the
  v0.22.0 threading-hardening batch (EigenScript#293). The `concurrent`
  lab is unblocked. Original report:
- 2026-06-29: `concurrent` lab — a dict sent across a channel from a spawned
  thread arrives with its entry **count** intact but its string **keys
  corrupted** (garbage bytes), so `msg.total` reads null → `cannot apply '+' to
  num and null` at `concurrent_lab.eigs:31`. Cross-thread channel transfer
  doesn't deep-copy the dict's heap key strings (use-after-free on the sender
  thread's freed string memory); same-thread send/recv is fine. Minimal repro:
  worker `send of [ch, {"id": 7, "total": 42}]` → main `try_recv` yields
  `keys=["<garbage>","<garbage>"] len=2`. Filed upstream as EigenScript #293;
  to fix at the root (deep-copy/intern dict key+string contents on cross-thread
  channel transfer), not worked around here.

## Resolved

- 2026-05-30: `swarm` lab spent ~5 minutes at size 64 because the
  per-entity `nearest_in_range` call walked the entity list O(n) times per
  step, paying a dict pointer-chase per scalar on every visit. Fixed in
  EigenScript by adding `nearest_in_range_all` (SoA batch primitive). The
  new `swarm-batch` lab runs the same workload in ~9 seconds at size 64
  — a 30.6× speedup. The original `swarm` lab is preserved as a
  regression watch for the per-call path.
- 2026-05-16: `eval` used `g_global_env` even when called inside a function,
  so generated code could leak names into global scope and perturb later
  observer trajectories. Fixed in EigenScript by evaluating code strings in the
  dynamic builtin caller scope.
- 2026-05-16: `eval` returned environment-owned assignment results as builtin
  temporaries, allowing callers to release live bindings. Fixed in EigenScript
  by preserving ownership for non-owned eval results.
