## Done when

> **Pre-registration status: FROZEN — PILOT FAILED SEPARATION.** The release and four samples are frozen below. The only workload run was the pre-named, disjoint mechanism pilot. It rejected the claim mapping, so **needing explicit cycle detection is the finding** and the 22,050,000,000-transition sample runs must not be run.

### Frozen graded scope after the pilot

A future harness may run only these graded items. It writes canonical JSON under `results/50/`; no simulator, decider, or graded result is included here.

1. **Champion and replay.** Run total machine `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA` on a blank tape with the **plain simulator: no signature and no observer**. Both VM (`EIGS_JIT_OFF=1`) and default JIT must execute exactly 47,176,870 transitions, finish with 4,098 ones, and produce byte-identical trace/replay output and tape SHA-256. Each arm must also set `EIGS_JIT_STATS=1`: the VM arm must report `compiled=0`, and the JIT arm must report `compiled>0`. v0.46.0 reads the switch at `src/jit.c:4487-4495` and prints those counters at `src/jit.c:310-314`; the verbatim source and demonstrated 0/1 tier output are in `prereg/50/evidence/bar-rewrite-50-fix/`.
2. **Antihydra abstention.** Machine `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA`, blank tape, must receive no claim of any class through 100,000,000 transitions. Report every observer predicate on both signature bindings, without grading those states.
3. **Mechanism pilot table.** Preserve the already-run checkpoint table and the rejection decision byte-for-byte. This is evidence, not a rerunnable graded sample.

AOT remains `WAITING_ON_OUROBOROS_PIN`. The former soundness, recall, collision, baseline, and NGramCPS sample items are removed from the graded scope by the pre-registered pilot branch; the frozen lists remain artifacts and must not be executed.

### Source and frozen samples

| Setting | Frozen value |
|---|---|
| Release | Coq-BB5 augmented v1.0.0, 804,978,618-byte zstd object at the manifest URL |
| Integrity | Full SHA-256 `2be2101b18b80a458bf85814ee361aa4f4e8d0d45a719cccda9756a65cd0685a`; computed locally over the complete object and equal to the digest already published in the first-round manifest (whose provenance was the GitHub release metadata) |
| Scan | `sample.py` makes exactly two `zstd -dc` streaming passes and never stores the decompressed CSV. Pass 1 counts eligibility; pass 2 selects rows at ascending sampled indices. |
| RNG | One `numpy.random.default_rng(50)`; `choice(..., replace=False)` in order: 5,000 uniform halters, requested 5,000 `steps >= 1000` halters after excluding the first draw; the eligible population is only 503, so the frozen stratum is its complete census, 10,000 `LOOP1_*` nonhalters, 1,000 `NGRAM_CPS_*` nonhalters |
| Lists | `halting-uniform.txt`, `halting-ge-1000.txt`, `loop1-nonhalt.txt`, `ngram-cps-nonhalt.txt`; counts (5,000 / 503 / 10,000 / 1,000), eligible-population counts, distributions, and SHA-256 values are in the manifest and streaming-pass evidence |
| Ordering | Canonical CSV order; sampled indices sorted ascending before records are written |

### Signature and observation

Let `p = 2^61 - 1` and base `b = 1815673109382999696`, drawn once as `default_rng(50).integers(2, p-1)`. For visited interval `[left,right]`, the hash is

`H = sum(cell[pos] * b^(pos-left), pos=left..right) mod p`.

A write updates it in O(1) with `(new-old)*b^(pos-left)`. Extending left re-bases in O(1) as `H := b*H + new_left_cell`; extending right only grows the cached power table (amortized O(1)). The collision plant, if retained as an ungraded diagnostic, masks `H & 0x0f`. The other signature fields remain state and signed `head-left`. Read after write/move/state update; bind the hash as fixed 16-digit hexadecimal text and the offset as a number.

The original mapping was `cycler` iff `converged(signature_hash) OR stable(signature_hash)`, otherwise `translated_cycler` iff `oscillating(head_offset)`. It is now frozen **as rejected**, not as a graded classifier. At v0.46.0, `observer_slot_update` sends only numeric values to the value trajectory and nonnumeric values fall back to entropy (`src/eigenscript.c:769-793`); strings use character Shannon entropy (`src/eigenscript.c:388-440`). Thus random hex identities have similar entropy even when configurations differ. Likewise, head-offset oscillation detects ordinary sweeps, including halting sweeps.

### Pre-named pilot and decision rule

Before it ran, the pilot named 11 entries in `prereg/50/evidence/bar-rewrite-50-fix/pilot-classes.txt`: three explicit period-2 cyclers, three explicit one-cell translated cyclers, three totalized terminal variants sharing the champion's >1,000-step sweeping prefix, the champion's first 1,000,000 transitions, and Antihydra's first 1,000,000. The constructed machines are absent from all frozen IDs. Classes come from direct transition-table proofs, the Coq-BB5 champion record, and the cited bbchallenge Antihydra page as detailed there.

At 10^3, 10^4, 10^5, and 10^6 the pilot recorded all six predicates (`converged`, `stable`, `improving`, `oscillating`, `diverging`, `equilibrium`) on both bindings. It failed separation: every sweeping halter already had `stable(signature_hash)=true` at 10^3, while translated-2 had no mapped predicate at any checkpoint. No better observer-only mapping is proposed. Therefore the mapping is rejected and no sample workload may run.

### Compute lanes

The real probe executes the champion's first 1,000,000 TM transitions, O(1) polynomial update, hexadecimal string-entropy assignment, and numeric offset assignment. Its measured rate and all derived seconds are verbatim in `real-compute-probe.txt`. The sample lane is `22,050,000,000 / measured_rate`; Antihydra is `100,000,000 / measured_rate`; and an observed champion would be `47,176,870 / measured_rate`. The actual champion lane is separately priced from a plain 1,000,000-transition probe because its frozen command has no signature/observer. These are single-process wall-clock estimates with no unmeasured numeric-update proxy.
