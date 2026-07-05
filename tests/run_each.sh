#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EIGS="${EIGENSCRIPT_BIN:-eigenscript}"
SIZE="${1:-1}"

cd "$ROOT"
for suite in tensor dataflow swarm swarm-batch concurrent parser memory observer io realtime module-scope; do
    "$EIGS" gauntlet.eigs --suite "$suite" --size "$SIZE"
done
