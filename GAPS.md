# EigenScript Gaps Found By EigenGauntlet

Policy: no downstream workaround is considered a fix. If a workload exposes a
missing primitive or runtime bug, record it here and fix EigenScript at the root.

## Open

None yet.

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
