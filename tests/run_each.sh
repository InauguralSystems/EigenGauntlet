#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EIGS="${EIGENSCRIPT_BIN:-/home/jon/EigenScript/src/eigenscript}"
SIZE="${1:-1}"

cd "$ROOT"
for suite in tensor dataflow swarm concurrent parser memory observer io realtime; do
    "$EIGS" gauntlet.eigs --suite "$suite" --size "$SIZE"
done
