---
name: Bug Report
about: Report a workload that fails/crashes or a suite that regresses
title: ""
labels: bug
assignees: ""
---

**Describe the bug**
What went wrong — e.g. a workload fails to parse/run, a suite crashes, or the
smoke suite regresses (a previously-green workload now errors or asserts).

**To reproduce**
Which suite and how you ran it:
```sh
eigenscript gauntlet.eigs --suite smoke        # or a single workload, e.g. --suite tensor
./tests/run_smoke.sh                            # or tests/run_each.sh
```

**Expected vs actual**
What you expected (which workload/assertion) vs what happened (include output).

**Environment**
- OS: [e.g., Ubuntu 24.04]
- EigenScript version: [output of `eigenscript --version`]
- EigenGauntlet version/tag: [e.g. v0.1.0]
- Hardware: [EigenGauntlet targets constrained hardware — note if relevant]

> If the root cause is the EigenScript language, runtime, or standard library
> itself, it belongs in the
> [EigenScript repo](https://github.com/InauguralSystems/EigenScript/issues) —
> and it's likely worth a note in [GAPS.md](../../GAPS.md).
