# Baseline

Machine: 2007 Gateway laptop, dual Pentium class hardware.

EigenScript binary: `/home/jon/EigenScript/src/eigenscript`

Date captured: 2026-05-16 local development state after adding observer, I/O,
and realtime workloads.

These numbers are not strict performance targets. They are a rough local
regression signal for this specific machine.

## Smoke Size 1

Command:

```bash
./tests/run_smoke.sh
```

Observed:

```text
tensor: ok (0.335171ms) -> rows=3 cols=3
dataflow: ok (1.10043ms) -> records=8
swarm: ok (1.4877ms) -> entities=12 steps=10
concurrent: ok (2.2188ms) -> workers=2 checksum=252
parser: ok (0.970312ms) -> generated_lines=14
memory: ok (0.669084ms) -> rounds=8 width=8
observer: ok (0.11056ms) -> age=1 hot=191
io: ok (29.7353ms) -> stream_values=4
realtime: ok (0.756595ms) -> frames=20 entities=10 slow=0
```

## Smoke Size 3

Command:

```bash
./tests/run_smoke.sh 3
```

Observed:

```text
tensor: ok (0.399913ms) -> rows=5 cols=3
dataflow: ok (2.93342ms) -> records=24
swarm: ok (17.8853ms) -> entities=36 steps=30
concurrent: ok (2.52729ms) -> workers=3 checksum=2970
parser: ok (1.20435ms) -> generated_lines=38
memory: ok (1.61935ms) -> rounds=24 width=8
observer: ok (0.116915ms) -> age=1 hot=1771
io: ok (181.797ms) -> stream_values=12
realtime: ok (6.54697ms) -> frames=60 entities=30 slow=0
```
