# EigenGauntlet

[![CI](https://github.com/InauguralSystems/EigenGauntlet/actions/workflows/ci.yml/badge.svg)](https://github.com/InauguralSystems/EigenGauntlet/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/InauguralSystems/EigenGauntlet/badge)](https://securityscorecards.dev/viewer/?uri=github.com/InauguralSystems/EigenGauntlet)
[![tag](https://img.shields.io/github/v/tag/InauguralSystems/EigenGauntlet?label=version)](https://github.com/InauguralSystems/EigenGauntlet/tags)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

EigenGauntlet is an EigenScript stress application suite for constrained
hardware. It is intentionally built as a set of small real workloads rather
than synthetic microbenchmarks.

The goal is to expose EigenScript language, runtime, standard library, and
tooling gaps without hiding them behind downstream workarounds. When a workload
needs a primitive EigenScript should own, the issue goes in `GAPS.md` and gets
fixed at the root.

## Requirements

- EigenScript built from source. CI builds and tests against the release
  pinned in `.github/workflows/ci.yml` (the `git clone --branch` line);
  that line is the only place the version is written down.
- No external runtime dependencies for the default smoke suite (the
  `cross-tape` suite also needs `env` on `PATH`)

Use the local development binary directly:

```bash
../EigenScript/src/eigenscript gauntlet.eigs --suite smoke
```

Or use an installed binary:

```bash
eigenscript gauntlet.eigs --suite smoke
```

## Workloads

- `tensor` - batched neural-layer math, matrix/vector broadcasting, softmax
- `dataflow` - JSON, strings, dictionaries, file I/O, EigenStore
- `swarm` - real-time style entity simulation and spatial queries
- `swarm-batch` - batched spatial queries via `nearest_in_range_all`
- `concurrent` - threads, channels, non-blocking receive
- `parser` - `try_parse`, `eval`, generated source, functions, match, f-strings
- `memory` - list/dict/tensor churn, closures
- `observer` - interrogatives, predicates, report states, unobserved blocks
- `io` - stream tensor I/O, buffers, byte reads, tensor save/load
- `realtime` - frame-budget style fixed-step loop with monotonic timing
- `module-scope` - `eval`, `load_file`, import isolation, module closures
- `cross` - the crossings: combinations of the axes above that nobody has a
  reason to write (observer x tasks, errors inside `unobserved:` x tasks,
  null/bool singletons x builtins x a JIT-hot observed loop, numbers in
  container slots x tasks x comprehensions, bools x JSON x comparison errors)
- `cross-tape` - tape x tasks x containers: a child run under `EIGS_TRACE`,
  replayed under `EIGS_REPLAY`, must print the same line (two child
  interpreters, so it is its own suite; CI runs it as a separate step)
- `soak` - not a workload: `cross` and `cross-tape` at 1000x the size, for
  off-box fuzz runs

## Hardware Discipline

Defaults must stay small enough to run quickly on constrained hardware: the
recording machine is an ASUS X540NA (Celeron N3350, 4 GB), and `BASELINE.md`
holds its numbers. Larger modes exist, but they are opt-in and named clearly
(`--size N`, `--suite soak`).

## Commands

```bash
# Run all smoke workloads
./tests/run_smoke.sh

# Run each workload separately with timings
./tests/run_each.sh

# Run one workload
../EigenScript/src/eigenscript gauntlet.eigs --suite tensor

# Run a bigger local pass
../EigenScript/src/eigenscript gauntlet.eigs --suite smoke --size 3

# The crossings at 1000x, for off-box fuzz runs (~5 s on the X540NA)
../EigenScript/src/eigenscript gauntlet.eigs --suite soak

# Fail on a known upstream gap instead of printing KNOWN-GAP (see GAPS.md)
../EigenScript/src/eigenscript gauntlet.eigs --suite cross --strict-gaps
```
