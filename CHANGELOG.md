# Changelog

## [Unreleased]

### Crossings (2026-10)
- `cross`: an error inside `unobserved:` in an eval'd chunk and in a task
  that dies uncaught, then a predicate (EigenScript#1735, a KNOWN-GAP on the
  v0.46.0 pin); null/bool singletons through builtins and slots in a JIT-hot
  observed loop (#1729); numbers in list/dict slots x tasks x comprehension x
  dict iteration; bools x containers x JSON x comparison errors
- `cross-tape` suite: a task-mutated container recorded under `EIGS_TRACE`
  must replay identically, and every counted nondet call must be an N record
- `soak` suite: the crossings at 1000x size (the singleton crossing makes
  3.3M builtin calls); `--strict-gaps` fails on any known gap
- BASELINE re-captured on the ASUS X540NA; front-door docs no longer name a
  version (the CI pin is the one place it is written)

## [0.1.0] — 2026-07-01

### Workloads (11)
- **tensor**: batched neural-layer math (matmul, relu, softmax)
- **dataflow**: JSON round-trips, file I/O, EigenStore persistence
- **swarm**: entity simulation with spatial queries
- **swarm-batch**: batched spatial queries via `nearest_in_range_all`
- **concurrent**: threads, channels, non-blocking receive
- **parser**: try_parse validation, eval, generated source
- **memory**: list/dict/tensor allocation churn, closures, arena
- **observer**: interrogatives, predicates, state tracking
- **io**: tensor streaming, buffers, binary reads
- **realtime**: frame budgets, monotonic timing
- **module-scope**: eval, load_file, import, closure factories

### Infrastructure
- Smoke test runner (`tests/run_smoke.sh`)
- Per-workload runner (`tests/run_each.sh`)
- Hardware baseline captured (2007 Gateway laptop)
- 2 eval bugs found and fixed upstream in EigenScript
