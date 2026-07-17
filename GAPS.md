# EigenScript Gaps Found By EigenGauntlet

Policy: no downstream workaround is considered a fix. If a workload exposes a
missing primitive or runtime bug, record it here and fix EigenScript at the root.

## Open

- 2026-07-17 — **EigenScript#642 (BLOCKER)**: a comprehension whose loop var
  shadows a local computes garbage. Inside a function, `i is 0 - 1` then
  `[i * 2 for i in [1, 2, 3]]` yields `[-2, -2, -2]` — the body reads the outer
  slot every iteration instead of its own loop var. rc=0, no diagnostic.
  Controls (one variable changed each): no outer `i` -> `[2, 4, 6]`; module
  scope -> `[2, 4, 6]`; outer named `q` -> `[2, 4, 6]`. Identical under
  `EIGS_JIT_OFF=1`. Root cause `src/compiler.c:2443` — the listcomp binder
  emits `OP_SET_NAME_LOCAL` (env) while a same-named plain assignment is
  slot-promoted, so two live bindings exist and the body reads the wrong one.
  Found by `cross_lab`'s `lib/sync` x comprehension crossing on its first run
  (the lock was incidental — isolating it produced the controls above).
  `cross_lab` parks the affected assertion rather than pinning the buggy value.

- 2026-07-17 — **EigenScript#633 (BLOCKER)**: the read AFTER such a
  comprehension is stale. Same root-cause family as #642, different symptom and
  trigger: `print of i` returns the pre-comprehension slot value while
  `eval of "i"` returns the leaked env value. Adding a never-called lambda
  mentioning the name flips which binding the read sees, so program text after a
  statement changes that statement's result. `cross_lab` re-derived this
  independently and parks its leak assertion until the fix lands.

## Resolved upstream — verified

- 2026-06-29 → **FIXED (verified 2026-07-03)**: the minimal repro passes
  against EigenScript main (`total=42 id=7`, keys intact) — fixed upstream
  in v0.21.2 (EigenScript#293, commit 1d804c1); the subsequent v0.22.0
  threading-hardening batch hardened the surrounding thread/channel paths.
  The `concurrent` lab is unblocked. Original report:
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
