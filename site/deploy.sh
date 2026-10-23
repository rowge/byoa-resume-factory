#!/usr/bin/env bash
# Deploy the store to Cloudflare Pages (resumefactory project).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TOKEN_FILE="${CLOUDFLARE_API_TOKEN_FILE:-$HOME/.config/cloudflare/api_token}"
if [[ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  echo "Set CLOUDFLARE_ACCOUNT_ID" >&2
  exit 1
fi

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  if [[ ! -f "$TOKEN_FILE" ]]; then
    echo "Missing Cloudflare token at $TOKEN_FILE" >&2
    exit 1
  fi
  export CLOUDFLARE_API_TOKEN
  CLOUDFLARE_API_TOKEN="$(cat "$TOKEN_FILE")"
fi

"$ROOT/pack-kit.sh"

DIST="$(mktemp -d)"
trap 'rm -rf "$DIST"' EXIT
cp -a "$ROOT/index.html" "$ROOT/pricing.html" "$ROOT/privacy.html" "$ROOT/refund.html" \
  "$ROOT/terms.html" "$ROOT/requirements.html" "$ROOT/style.css" \
  "$ROOT/favicon.svg" "$ROOT/thanks.html" "$ROOT/robots.txt" "$DIST/"
mkdir -p "$DIST/kit"
cp -a "$(cd "$ROOT/.." && pwd)/BYOA-Resume-Factory.zip" "$DIST/kit/BYOA-Resume-Factory.zip"

exec deno run -A npm:wrangler@4 pages deploy "$DIST" \
  --project-name=resumefactory \
  --branch=main \
  --commit-dirty=true
