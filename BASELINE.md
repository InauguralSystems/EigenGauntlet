# Baseline

Machine: 2007 Gateway laptop, dual Pentium class hardware.

EigenScript binary: `/home/jon/EigenScript/src/eigenscript`

Date captured: current local development state after adding parser and memory
workloads.

These numbers are not strict performance targets. They are a rough local
regression signal for this specific machine.

## Smoke Size 1

Command:

```bash
./tests/run_smoke.sh
```

Observed:

```text
tensor: ok (0.355634ms) -> rows=3 cols=3
dataflow: ok (2.03644ms) -> records=8
swarm: ok (3.64022ms) -> entities=12 steps=10
concurrent: ok (1.92414ms) -> workers=2 checksum=252
parser: ok (0.799687ms) -> generated_lines=14
memory: ok (0.556568ms) -> rounds=8 width=8
```

## Smoke Size 3

Command:

```bash
./tests/run_smoke.sh 3
```

Observed:

```text
tensor: ok (2.43468ms) -> rows=5 cols=3
dataflow: ok (1.80939ms) -> records=24
swarm: ok (21.4732ms) -> entities=36 steps=30
concurrent: ok (1.85569ms) -> workers=3 checksum=2970
parser: ok (1.53275ms) -> generated_lines=38
memory: ok (1.89075ms) -> rounds=24 width=8
```

