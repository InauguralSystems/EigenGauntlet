# Issue 50 frozen-scope evidence report

The pre-registration prices the observed Antihydra lane at 755.037609 seconds
and the trace files produced while validating replay are multi-GiB.  Therefore
the exact run is delegated to the push-triggered `bb50.yml` job (340-minute
timeout); the local run below is the required reduced smoke.  No frozen sample
list was read or executed.

## Release build check

```text
$ make -C /tmp/eigenscript build
make: Entering directory '/tmp/eigenscript'
EigenScript 0.46.0 built. Binary: 1.2M
make: Leaving directory '/tmp/eigenscript'
exit=0
```

## Release and champion (plain simulator)

```text
$ /tmp/eigenscript/src/eigenscript --version
0.46.0
exit=0
$ env EIGS_JIT_OFF=1 EIGS_JIT_STATS=1 /tmp/eigenscript/src/eigenscript evidence/50/champion.eigs
transitions=47176870 ones=4098 tape_sha256=2ef0e5dca6b00adf3cf1dc75e0d40a6408ac9799c778ac71961484a292f436df
[jit] scanned=0 compiled=0 cache_used=0 cache_full_rejects=0
exit=0
$ env EIGS_JIT_STATS=1 /tmp/eigenscript/src/eigenscript evidence/50/champion.eigs
transitions=47176870 ones=4098 tape_sha256=2ef0e5dca6b00adf3cf1dc75e0d40a6408ac9799c778ac71961484a292f436df
[jit] scanned=2 compiled=2 cache_used=65628 cache_full_rejects=0
exit=0
```

## Antihydra reduced smoke

The million-transition checkpoint is pre-named pilot evidence, not a frozen
sample-list workload.  All predicates are deliberately reported without using
them to make a claim.

```text
$ env EIGS_JIT_STATS=1 /tmp/eigenscript/src/eigenscript evidence/50/antihydra.eigs 1000000
transitions=1000000 claim=null
signature_hash converged=false stable=true improving=false oscillating=false diverging=false equilibrium=true
head_offset converged=false stable=false improving=false oscillating=false diverging=true equilibrium=false
[jit] scanned=8 compiled=6 cache_used=104512 cache_full_rejects=0
exit=0
```

## Pilot preservation

```text
$ sha256sum prereg/50/evidence/bar-rewrite-50-fix/pilot-table.json results/50/pilot-table.json prereg/50/evidence/bar-rewrite-50-fix/mapping-decision.txt results/50/mapping-decision.txt
e07eced2d60b2f2c2d855b571b0290899459a2327b2bfcca4869d4cd83baeb6b  prereg/50/evidence/bar-rewrite-50-fix/pilot-table.json
e07eced2d60b2f2c2d855b571b0290899459a2327b2bfcca4869d4cd83baeb6b  results/50/pilot-table.json
f91532fa2b9104ca6363159564e9df8e2b1dfcb48cc97bb3e81e24955a51fac7  prereg/50/evidence/bar-rewrite-50-fix/mapping-decision.txt
f91532fa2b9104ca6363159564e9df8e2b1dfcb48cc97bb3e81e24955a51fac7  results/50/mapping-decision.txt
exit=0
$ cmp prereg/50/evidence/bar-rewrite-50-fix/pilot-table.json results/50/pilot-table.json
exit=0
$ cmp prereg/50/evidence/bar-rewrite-50-fix/mapping-decision.txt results/50/mapping-decision.txt
exit=0
```

## Harness checks

```text
$ python3 -m py_compile evidence/50/summarize.py
exit=0
$ bash -n evidence/50/run.sh
exit=0
```

## Exact off-box command

The workflow runs this command after building the pinned release.  Its complete
stdout/stderr logs, trace digests, and canonical `results/50/graded.json` are
uploaded even if a later step fails.

```text
$ EIGENSCRIPT_BIN=/tmp/eigenscript/src/eigenscript BB50_OUT=/tmp/bb50 evidence/50/run.sh
not run locally (long lane; see push-triggered workflow)
exit=not-run
```
