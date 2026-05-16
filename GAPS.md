# EigenScript Gaps Found By EigenGauntlet

Policy: no downstream workaround is considered a fix. If a workload exposes a
missing primitive or runtime bug, record it here and fix EigenScript at the root.

## Open

None yet.

## Resolved

- 2026-05-16: `eval` used `g_global_env` even when called inside a function,
  so generated code could leak names into global scope and perturb later
  observer trajectories. Fixed in EigenScript by evaluating code strings in the
  dynamic builtin caller scope.
- 2026-05-16: `eval` returned environment-owned assignment results as builtin
  temporaries, allowing callers to release live bindings. Fixed in EigenScript
  by preserving ownership for non-owned eval results.
