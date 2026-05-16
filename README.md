# EigenGauntlet

EigenGauntlet is an EigenScript stress application suite for constrained
hardware. It is intentionally built as a set of small real workloads rather
than synthetic microbenchmarks.

The goal is to expose EigenScript language, runtime, standard library, and
tooling gaps without hiding them behind downstream workarounds. When a workload
needs a primitive EigenScript should own, the issue goes in `GAPS.md` and gets
fixed at the root.

## Requirements

- EigenScript v0.9.3.4 or later
- No external runtime dependencies for the default smoke suite

Use the local development binary directly:

```bash
/home/jon/EigenScript/src/eigenscript gauntlet.eigs --suite smoke
```

Or use an installed binary:

```bash
eigenscript gauntlet.eigs --suite smoke
```

## Workloads

- `tensor` - batched neural-layer math, matrix/vector broadcasting, softmax
- `dataflow` - JSON, strings, dictionaries, file I/O, EigenStore
- `swarm` - real-time style entity simulation and spatial queries
- `concurrent` - threads, channels, non-blocking receive
- `parser` - `try_parse`, `eval`, generated source, functions, match, f-strings
- `memory` - list/dict/tensor churn, closures, arena mark/reset

## Hardware Discipline

This repo is designed for a 2007 dual-Pentium laptop. Defaults must stay small
enough to run quickly on that hardware. Larger modes can exist, but they should
be opt-in and named clearly.

## Commands

```bash
# Run all smoke workloads
./tests/run_smoke.sh

# Run each workload separately with timings
./tests/run_each.sh

# Run one workload
/home/jon/EigenScript/src/eigenscript gauntlet.eigs --suite tensor

# Run a bigger local pass
/home/jon/EigenScript/src/eigenscript gauntlet.eigs --suite smoke --size 3
```
