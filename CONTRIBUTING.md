# Contributing

EigenGauntlet is a stress-test application suite for
[EigenScript](https://github.com/InauguralSystems/EigenScript).
It runs small real workloads on constrained hardware, one axis per lab, plus
`cross`: the lab that crosses those axes.

## Getting Started

1. Build EigenScript:
   ```
   git clone https://github.com/InauguralSystems/EigenScript.git
   cd EigenScript && git checkout <the tag pinned in .github/workflows/ci.yml>
   make build && make install
   ```

2. Clone this repo and run the suite:
   ```
   git clone https://github.com/InauguralSystems/EigenGauntlet.git
   cd EigenGauntlet && tests/run_smoke.sh
   ```

## Workloads

The `for suite in ...` loop in `tests/run_each.sh` is the list; `README.md`
says what each one stresses.

## Adding a Workload

1. Create `src/new_lab.eigs` with a `run_new(size)` function
2. Add it to `gauntlet.eigs` (load_file + run entry)
3. Add assertions and timing metrics
4. Add the suite to `tests/run_each.sh` (the `for suite in ...` loop) and to the smoke branch in `gauntlet.eigs`

Prefer a new CROSSING in `src/cross_lab.eigs` over a new single-axis lab: the
bugs live where axes meet. Assertions pin what the runtime actually does. A
bug the pinned release still has is never pinned as expected; record it in
`GAPS.md` and route it through `known_gap` in `src/common.eigs`, which only
waives it on the one release it was observed on.

## License

MIT. See [LICENSE](LICENSE).
