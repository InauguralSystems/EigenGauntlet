#!/usr/bin/env bash
set -euo pipefail

EIGS=${EIGENSCRIPT_BIN:-eigenscript}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
OUT=${BB50_OUT:-"$ROOT/results/50/run"}
mkdir -p "$OUT"

"$EIGS" --version | tee "$OUT/version.log"

run_champion_arm() {
  local arm=$1 off=$2
  env EIGS_JIT_OFF="$off" EIGS_JIT_STATS=1 EIGS_TRACE="$OUT/$arm.tape" \
    "$EIGS" "$ROOT/evidence/50/champion.eigs" \
    >"$OUT/$arm.record.stdout" 2>"$OUT/$arm.record.stderr"
  env EIGS_JIT_OFF="$off" EIGS_JIT_STATS=1 EIGS_REPLAY="$OUT/$arm.tape" \
    "$EIGS" "$ROOT/evidence/50/champion.eigs" \
    >"$OUT/$arm.replay.stdout" 2>"$OUT/$arm.replay.stderr"
  cmp "$OUT/$arm.record.stdout" "$OUT/$arm.replay.stdout"
  sha256sum "$OUT/$arm.tape" >"$OUT/$arm.tape.sha256"
}

run_champion_arm vm 1
# A full trace is several GiB.  Retain its digest, then reclaim it before the
# JIT arm so GitHub's runner does not need space for two identical tapes.
vm_tape_sha=$(cut -d' ' -f1 "$OUT/vm.tape.sha256")
rm -f "$OUT/vm.tape"
run_champion_arm jit ""
cmp "$OUT/vm.record.stdout" "$OUT/jit.record.stdout"
jit_tape_sha=$(cut -d' ' -f1 "$OUT/jit.tape.sha256")
test "$vm_tape_sha" = "$jit_tape_sha"

env EIGS_JIT_STATS=1 "$EIGS" "$ROOT/evidence/50/antihydra.eigs" \
  >"$OUT/antihydra.stdout" 2>"$OUT/antihydra.stderr"

python3 "$ROOT/evidence/50/summarize.py" "$OUT" "$ROOT/results/50/graded.json"
