## Done when

> **Pre-registration status: BLOCKED (inputs not frozen).** The authoritative augmented file is fetchable only as an 804,978,618-byte object. The mandated “never download a file over 200 MB whole” rule prevents the canonical-order scan required to select records uniformly. No sample IDs or results are invented. The bar below is the frozen replacement specification, but no experiment may be graded until the three missing ID files and their digests are produced by `sample.py` from an independently supplied, digest-matching local copy. See `evidence/bar-rewrite-50/facts.txt`.

### Frozen protocol

Every graded command is a future builder command with this common contract: it writes canonical JSON to `results/50/<item>.json`, writes no other stdout, and exits 0 exactly when the stated gate passes (2 for malformed/missing inputs and 1 for a failed gate). Each record contains `machine`, oracle class, verdict (`none|cycler|translated_cycler`), and first-claim transition. Counts are integers; rates also include their raw numerator and denominator. The report names the **closest call** for every boundary: false-positive boundary (latest halting machine to escape a claim, or earliest false claim), recall boundary (the missed/claimed machine whose ordered first-claim margin to 1,050,000 is smallest), exact champion counts (signed transition/ones margins), Antihydra (earliest claim or `none` with 100,000,000-step margin), collision plant (earliest false claim or `none`), and parity/median boundaries (symmetric-difference machine and raw median step margin).

1. **Soundness.** Population: all 10,000 frozen halting IDs (the union of the two nonoverlapping strata). Oracle: `status=halt` and `steps` in Coq-BB5 augmented v1.0.0. Threshold: zero `cycler` or `translated_cycler` claims through transition 1,050,000. Command: `python prereg/50/run_bar.py soundness --manifest prereg/50/manifest.json`.
2. **Loops recall.** Population: 10,000 frozen `LOOP1_*`, `nonhalt` IDs. Oracle: Coq-BB5 augmented v1.0.0. Threshold: at least 9,500/10,000 receive either claim by transition 1,050,000. This is observer recall, not the published aggregate Loops coverage. Command: `python prereg/50/run_bar.py recall --manifest prereg/50/manifest.json`.
3. **Champion and replay.** Population: the single total machine `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA`, blank all-0 tape, A, head 0. Oracle: independent simulator recorded in facts. Threshold: VM (`EIGS_JIT=0`) and default JIT each execute exactly 47,176,870 transitions and finish with exactly 4,098 ones; `EIGS_TRACE` output and tape SHA-256 must equal the `EIGS_REPLAY` output and tape SHA-256 byte-for-byte. AOT is explicitly `WAITING_ON_OUROBOROS_PIN`: this repository pins none, so it is reported but is not a gate. Command: `python prereg/50/run_bar.py champion --manifest prereg/50/manifest.json`.
4. **Antihydra abstention.** Population/oracle: the one cited bbchallenge machine `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA`, blank all-0 tape, A, head 0. Threshold: zero claims of **any** class during 100,000,000 transitions. The JSON also reports (but does not grade) every observer predicate state on the head-extent binding. Command: `python prereg/50/run_bar.py antihydra --manifest prereg/50/manifest.json`.
5. **Collision plant.** Population: the 10,000 frozen halting IDs. Oracle: Coq-BB5 halting status. Threshold: with only the signature hash masked to its low 4 bits, at least 1/10,000 false nonhalting claim by transition 1,050,000. Command: `python prereg/50/run_bar.py collision --manifest prereg/50/manifest.json`.
6. **Pinned baseline.** Population: the same frozen halting and Loops samples. Oracle/baseline: `bbchallenge/bbchallenge-deciders` at `abcf5375c06b9706a3a8e4752c5fd834dd9c47af`, `decider-cyclers` plus `decider-translated-cyclers`, capped at 1,050,000 transitions. **Parity** requires identical claimed-machine sets separately on both populations. **Beats** requires parity and observer median first-claim transition strictly below baseline median on the 10,000 Loops machines; both raw medians are printed. Command: `python prereg/50/run_bar.py baseline --manifest prereg/50/manifest.json`.
7. **NGramCPS specificity report.** Population: 1,000 frozen `NGRAM_CPS_*`, `nonhalt` IDs. Oracle: Coq-BB5 augmented v1.0.0. Threshold: zero false class labels (only `none`, `cycler`, or `translated_cycler` are legal); claim rate has no pass threshold and is printed as a raw fraction. Command: `python prereg/50/run_bar.py ngramcps --manifest prereg/50/manifest.json`.

`run_bar.py` is deliberately not part of this pre-registration: implementing it would be the forbidden simulator/decider/harness workload.

### Settings

| Setting | Frozen value |
|---|---|
| Release / record format | Coq-BB5 v1.0.0 augmented CSV: ASCII header `machine,status,decider,sigma,space,steps,machine_with_halt_transition`; standard bbchallenge text machines |
| Release object | GitHub asset URL and SHA-256 in manifest; 804,978,618-byte zstd file; only bytes 0–8,388,607 were read |
| Sampling | canonical CSV order; one `numpy.random.default_rng(50)`; draws in order uniform halt 5,000, long halt 5,000 excluding the first stratum, Loops 10,000, NGramCPS 1,000; all without replacement |
| Eligibility | exact `halt`; long has integer `steps >= 1000`; Loops is `nonhalt` and `decider.startswith("LOOP1_")`; NGramCPS likewise `NGRAM_CPS_` |
| Category overlap | status separates halters; the proof pipeline assigns one deciding method per row, so method categories are disjoint; second halt stratum explicitly excludes first |
| Budget | 1,050,000 transitions, the largest Loops step bound used by the pinned proof (`loop1_decider 1050000`); the generic passes use 130 and 4,100. |
| Signature | `(state ASCII A..F/Z, signed head-left offset, FNV-1a-64(window bytes))`; window is every cell from minimum through maximum position ever visited, inclusive; cells serialize left-to-right as one byte `0x00`/`0x01`; offset is mathematical signed integer, not hashed |
| Hash | FNV-1a 64: offset basis `14695981039346656037`, multiply `1099511628211` modulo 2^64; plant masks `hash & 0x0f` |
| Observation/read | after each executed transition, after write/move/state update; assign the unsigned hash as an exactly represented hexadecimal string binding and assign offset to a numeric binding; first claim wins |
| Claim mapping | `cycler` iff `converged of signature_hash` or `stable of signature_hash`; `translated_cycler` iff neither fired and `oscillating of head_offset`; no other predicate claims. This uses named predicates and default constants, with no setters or experiment constants in the claim path. |
| EigenScript before | tag v0.46.0, commit `4a3a5c1941568e9bc562c7c8221cff22dc8ba697`; window 10, min/max 4/64, `dh_zero=.001`, `dh_small=.01`, `h_low=.1`, scale `.001` |
| After sequencing | EigenScript#1758 round 3 is follow-up only, outside this Done-when |
| Champion convention | total `1RZ`; 47,176,870 executed transitions; 4,098 final ones. Partial `---` executes 47,176,869 defined transitions, then looks up undefined E0 with 4,097 ones. |
| Antihydra | `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA`; 100,000,000 transitions |
| Trace tolerance | none: `cmp` equality plus identical SHA-256 |
| Count/rate tolerance | exact integer comparisons; recall inclusive `>= 9500`; beat strictly `<`; medians are ordinary average of the two center order statistics |
| VM/JIT/AOT | VM `EIGS_JIT=0`; JIT default; AOT waiting because no ouroboros commit is pinned here |
| Compute lane | local measured probe: observer off 11.14M iterations/s, on 6.05M/s. Champion ≈7.80 s observed / 4.24 s off; Antihydra ≈16.52 s observed; 21,000 sampled machines × 1,050,000 = 22,050,000,000 transitions ≈60.74 observed minutes before baseline, so samples require an off-box lane. |

### Blocking condition

The sample freeze is blocked as stated above. No before/after workload SHAs exist because implementation is expressly out of scope.
