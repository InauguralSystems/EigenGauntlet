#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EIGS="${EIGENSCRIPT_BIN:-/home/jon/EigenScript/src/eigenscript}"

cd "$ROOT"
"$EIGS" gauntlet.eigs --suite smoke --size "${1:-1}"

