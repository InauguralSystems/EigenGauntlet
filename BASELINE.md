# Baseline

Machine: 2007 Gateway laptop, dual Pentium class hardware.

EigenScript binary: `/home/jon/EigenScript/src/eigenscript`

Date captured: 2026-05-16 local development state after adding observer, I/O,
realtime, and module/scope workloads.

These numbers are not strict performance targets. They are a rough local
regression signal for this specific machine.

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
