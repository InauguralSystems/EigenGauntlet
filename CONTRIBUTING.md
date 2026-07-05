# Contributing

EigenGauntlet is a stress-test application suite for
[EigenScript](https://github.com/InauguralSystems/EigenScript).
It exercises 11 workloads covering language breadth on constrained hardware.

## Getting Started

1. Build EigenScript:
   ```
   git clone https://github.com/InauguralSystems/EigenScript.git
   cd EigenScript && make build && make install
   ```

2. Clone this repo and run the suite:
   ```
   git clone https://github.com/InauguralSystems/EigenGauntlet.git
   cd EigenGauntlet && tests/run_smoke.sh
   ```

## Workloads

tensor, dataflow, swarm, swarm-batch, concurrent, parser, memory, observer, io, realtime, module-scope

## Adding a Workload

1. Create `src/new_lab.eigs` with a `run_new(size)` function
2. Add it to `gauntlet.eigs` (load_file + run entry)
3. Add assertions and timing metrics
4. Add the suite to `tests/run_each.sh` (the `for suite in ...` loop) and to the smoke branch in `gauntlet.eigs`

## License

MIT. See [LICENSE](LICENSE).
