# Baseline

Machine: 2007 Gateway laptop, dual Pentium class hardware.

> **STALE — needs re-capture (2026-07-17).** That machine was retired (the
> T3200 went to EigenOS); the current dev box is an ASUS X540NA (Celeron
> N3350, 4 GB). The numbers below are therefore not comparable to a current
> run. The constrained-hardware *regime* is unchanged — this is not modern
> hardware either — so the baseline's purpose stands and only the capture is
> out of date. Re-run `tests/run_smoke.sh` on the X540NA and replace the table
> (the `swarm-batch` and `cross` workloads also post-date the 2026-05-16
> capture; a current run emits 12 workload lines).

EigenScript binary: `../EigenScript/src/eigenscript`

Date captured: 2026-05-16 local development state after adding observer, I/O,
realtime, and module/scope workloads.

These numbers are not strict performance targets. They are a rough local
regression signal for this specific machine.

Note: the `swarm-batch` workload was added after this 2026-05-16 capture, so
it has no line below; a current `run_smoke.sh` emits 11 workload lines. Re-run
`run_smoke.sh` to re-capture on the recording machine before comparing.

## Smoke Size 1

Command:

```bash
./tests/run_smoke.sh
```

Observed:

```text
tensor: ok (0.954248ms) -> rows=3 cols=3
dataflow: ok (1.50048ms) -> records=8
swarm: ok (2.89787ms) -> entities=12 steps=10
concurrent: ok (4.0363ms) -> workers=2 checksum=252
parser: ok (1.21343ms) -> generated_lines=14
memory: ok (0.586112ms) -> rounds=8 width=8
observer: ok (0.13263ms) -> age=1 hot=191
io: ok (5.16068ms) -> stream_values=4
realtime: ok (0.806044ms) -> frames=20 entities=10 slow=0
module-scope: ok (1.77922ms) -> size=1 global=7
```

## Smoke Size 3

Command:

```bash
./tests/run_smoke.sh 3
```

Observed:

```text
tensor: ok (0.350466ms) -> rows=5 cols=3
dataflow: ok (1.7855ms) -> records=24
swarm: ok (16.8637ms) -> entities=36 steps=30
concurrent: ok (2.53742ms) -> workers=3 checksum=2970
parser: ok (2.17515ms) -> generated_lines=38
memory: ok (2.1301ms) -> rounds=24 width=8
observer: ok (0.254224ms) -> age=1 hot=1771
io: ok (3.00571ms) -> stream_values=12
realtime: ok (9.87619ms) -> frames=60 entities=30 slow=0
module-scope: ok (1.04078ms) -> size=3 global=7
```
