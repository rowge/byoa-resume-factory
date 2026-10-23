#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 build_pdfs.py "$@"
fi
if command -v python >/dev/null 2>&1; then
  exec python build_pdfs.py "$@"
fi
echo "Python 3.10+ not found. Install it, then: python3 -m pip install -r requirements.txt" >&2
exit 1
