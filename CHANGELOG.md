# Changelog

## [0.1.0] — 2026-07-01

### Workloads (10)
- **tensor**: batched neural-layer math (matmul, relu, softmax)
- **dataflow**: JSON round-trips, file I/O, EigenStore persistence
- **swarm**: entity simulation with spatial queries
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
