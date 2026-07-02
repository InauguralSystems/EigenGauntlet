# CLAUDE.md

Guidance for working in this repository.

## What this is

EigenGauntlet is an **EigenScript stress harness**. It runs small but
real workloads — neural math, JSON/file I/O, swarm simulation, threads,
parsers, observers, realtime loops — and the **point is to surface
runtime/language/stdlib gaps in EigenScript itself**, not to optimize
the workloads.

Rule of thumb: if a workload needs a primitive EigenScript should own,
the gap goes in `GAPS.md` and gets fixed upstream rather than worked
around locally. EigenGauntlet is a forcing function for EigenScript,
sibling to EigenRegex, EigenMiniSat, and Tidepool.

## Toolchain

EigenScript is **not** vendored — point at a built binary:

```bash
# Default path (matches tests/run_smoke.sh):
../EigenScript/src/eigenscript gauntlet.eigs --suite smoke

# Or use an installed binary:
eigenscript gauntlet.eigs --suite smoke

# Or override:
EIGENSCRIPT_BIN=/path/to/eigenscript ./tests/run_smoke.sh
```

CI builds and tests against EigenScript **v0.23.0**, pinned in
`.github/workflows/ci.yml`.

## Run / test

```bash
EIGS=../EigenScript/src/eigenscript

# All smoke workloads at default size
./tests/run_smoke.sh

# All workloads, each separately, with per-suite timings
./tests/run_each.sh

# One workload
$EIGS gauntlet.eigs --suite tensor

# Bigger pass (size scales workload, NOT a new suite)
$EIGS gauntlet.eigs --suite smoke --size 3
```

`BASELINE.md` records timing snapshots; update it when you've
genuinely moved a workload's number (see `feedback_perf_measurement` —
one-shot comparisons are noise on this hardware).

## Workloads

| Suite | What it stresses |
|---|---|
| `tensor` | batched neural-layer math, matrix/vector broadcasting, softmax |
| `dataflow` | JSON, strings, dicts, file I/O, EigenStore |
| `swarm` | real-time-style entity simulation + spatial queries |
| `swarm-batch` | batched spatial queries via `nearest_in_range_all` |
| `concurrent` | threads, channels, `try_recv`/`recv_timeout` |
| `parser` | `try_parse`, `eval`, generated source, `match`, f-strings |
| `memory` | list/dict/tensor churn, closures, arena mark/reset |
| `observer` | interrogatives, predicates, `unobserved` blocks |
| `io` | stream tensor I/O, buffers, byte reads, tensor save/load |
| `realtime` | frame-budget fixed-step loop, monotonic timing |
| `module-scope` | `eval`, `load_file`, import isolation, module closures |

## Layout

| Path | Role |
|---|---|
| `gauntlet.eigs` | CLI entry — dispatches `--suite` to a lab |
| `src/*_lab.eigs` | One file per workload (the suite implementations) |
| `src/common.eigs` | Shared helpers (timing, output format) |
| `lib/gauntlet_scope.eigs` | Module-scope harness for the `module-scope` suite |
| `fixtures/` | Static input data (JSON, etc.) |
| `tests/run_smoke.sh`, `tests/run_each.sh` | Runners |
| `GAPS.md` | The forcing-function ledger — every friction logged here |
| `BASELINE.md` | Recorded timings per workload |
| `docs/` | Notes on specific stress paths |

## Hardware discipline

Defaults must run quickly on the target — a **2007 dual-Pentium laptop
(T3200)**. Larger modes can exist but **must be opt-in and named
clearly** (e.g. `--size 3`, not changing the default). When in doubt,
ship the smaller default and document the larger mode.

## Hard-won rules

- **No local workarounds for upstream gaps.** If a workload would be
  easier with a builtin EigenScript should own, log it in `GAPS.md`
  and write the awkward version — the friction is the signal.
- **Perf claims are n=5.** Don't compare a single one-shot to a single
  one-shot on this hardware; variance dominates.
- **Match historical methodology when bisecting regressions.** Comparing
  a 500K canary to a 225M aggregate has burned us before.
- **Hoist module globals to function locals** in hot paths so the JIT's
  inline caches fire (the same pattern EigenMiniSat's
  `Inline tiny accessors in CDCL hot path` commit captures).

## Current state

10 workloads, smoke green at default size. Latest addition:
`swarm-batch` lab exercising `nearest_in_range_all` (the batched
spatial-query primitive that landed in EigenScript). Pinned to
v0.23.0-line semantics; `--pkg` integration is available but the suite
runs without packages.

## Gotchas

- Don't compare timings across hosts; record the machine in any
  baseline you update.
- `tmp/` is scratch — don't commit it.
- The `concurrent` workload spawns threads; if you've patched the
  closure-cycle collector, run under `make asan` from the EigenScript
  side to verify no new leaks are introduced.
