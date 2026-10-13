# Baseline

Machine: ASUS X540NA, Intel Celeron N3350 (2 cores), 4 GB RAM, Linux 6.8.

EigenScript: v0.46.0 (tag commit `4a3a5c19`), built with `make build` — the
release CI pins. Gauntlet tree: the commit that added this capture (parent
`a55383c`).

Date captured: 2026-10-12.

These numbers are not performance targets. They are a rough local regression
signal for this machine; don't compare them across hosts, and a one-shot line
is noise on this hardware (see CLAUDE.md, "Perf claims are n=5"). The
`KNOWN-GAP` line is EigenScript#1735 on the v0.46.0 pin (see `GAPS.md`); a
build carrying the fix prints the same output without it.

## Smoke size 1

Command: `./tests/run_smoke.sh`. Whole-run wall time (bash runner, process
start to exit), 9 paired runs: median **58 ms** (range 56-66). The same runner
over the tree before the five 2026-10 crossings: median **48 ms** (45-54), so
the crossings cost 1.21x.

```text
EigenGauntlet suite=smoke size=1
tensor: ok (0.198351ms) -> rows=3 cols=3
dataflow: ok (0.781852ms) -> records=8
swarm: ok (0.926421ms) -> entities=12 steps=10
swarm-batch: ok (0.633646ms) -> entities=12 steps=10
concurrent: ok (1.719616ms) -> workers=2 checksum=252
parser: ok (0.859872ms) -> generated_lines=14
memory: ok (0.737857ms) -> rounds=8 width=8
observer: ok (0.139978ms) -> age=21 hot=191
io: ok (1.473263ms) -> stream_values=4
realtime: ok (0.726668ms) -> frames=20 entities=10 slow=0
module-scope: ok (1.811997ms) -> size=1 global=7
KNOWN-GAP EigenScript#1735 (waived on v0.46.0 only): cross: predicate after a task died inside unobserved:
cross: ok (15.162688ms) -> singleton_calls=3300 slots=8 bools=4
EigenGauntlet complete
```

`cross-tape` is its own suite (it spawns two child interpreters, which alone
would cost the smoke run more than its budget); CI runs it as a separate step:

```text
EigenGauntlet suite=cross-tape size=1
cross-tape: ok (18.392267ms) -> tape_nondet=14
EigenGauntlet complete
```

## Smoke size 3

Command: `./tests/run_smoke.sh 3`

```text
EigenGauntlet suite=smoke size=3
tensor: ok (0.192408ms) -> rows=5 cols=3
dataflow: ok (1.332297ms) -> records=24
swarm: ok (9.050967ms) -> entities=36 steps=30
swarm-batch: ok (5.556988ms) -> entities=36 steps=30
concurrent: ok (3.512916ms) -> workers=3 checksum=2970
parser: ok (1.219139ms) -> generated_lines=38
memory: ok (1.345976ms) -> rounds=24 width=8
observer: ok (0.226679ms) -> age=61 hot=1771
io: ok (1.953167ms) -> stream_values=12
realtime: ok (2.168866ms) -> frames=60 entities=30 slow=0
module-scope: ok (1.261441ms) -> size=3 global=7
KNOWN-GAP EigenScript#1735 (waived on v0.46.0 only): cross: predicate after a task died inside unobserved:
cross: ok (24.38914ms) -> singleton_calls=9900 slots=24 bools=12
EigenGauntlet complete
```

## Soak

Command: `eigenscript gauntlet.eigs --suite soak` (the crossings at 1000x).
Whole run 5 s wall. The singleton crossing makes 3,300,000 builtin calls,
1,100,000 on each of `null`, `true` and `false` — past the singletons'
1,000,000 refcount margin, which is the point (EigenScript#1729).

```text
EigenGauntlet suite=soak size=1
soak: crossings at size=1000
KNOWN-GAP EigenScript#1735 (waived on v0.46.0 only): cross: predicate after a task died inside unobserved:
cross: ok (3837.177593ms) -> singleton_calls=3300000 slots=8000 bools=4000
cross-tape: ok (488.666522ms) -> tape_nondet=12002
EigenGauntlet complete
```
