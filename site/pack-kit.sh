#!/usr/bin/env bash
# Rebuild the buyer zip from BYOA-Resume-Factory/ (files at zip root).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KIT="$ROOT/BYOA-Resume-Factory"
OUT="$ROOT/BYOA-Resume-Factory.zip"

if [[ ! -f "$KIT/AGENTS.md" ]]; then
  echo "Missing $KIT/AGENTS.md" >&2
  exit 1
fi

rm -f "$OUT"
(
  cd "$KIT"
  zip -r "$OUT" . \
    -x '*/__pycache__/*' \
    -x '*.pyc' \
    -x '*/.DS_Store' \
    -x '.DS_Store'
)

echo "wrote $OUT ($(wc -c < "$OUT") bytes)"
