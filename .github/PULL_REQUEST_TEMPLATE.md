## What does this PR do?

<!-- Brief description of the change -->

## Checklist

- [ ] Every changed/added workload **runs** (`eigenscript gauntlet.eigs --suite <name>`)
- [ ] The smoke suite passes locally (`./tests/run_smoke.sh`)
- [ ] Defaults stay small enough for constrained hardware; any larger mode is
      **opt-in and named** (e.g. `--size 3`, not a bigger default)
- [ ] Any runtime/language/stdlib gap surfaced is logged in
      [GAPS.md](../GAPS.md) (and, if it's an EigenScript bug, filed upstream)
- [ ] `BASELINE.md` updated only if a workload's number genuinely moved (n=5, same host)
