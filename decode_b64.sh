#!/usr/bin/env bash
# Restore binary artifacts stored as base64 sidecars (GitHub MCP transport can't carry raw binary).
# The SQLite sidecars (cropcircles.sqlite.b64) are stored as base64(gzip(data)) — the raw
# database is mostly empty pages whose plain base64 is tens of KB of repeated 'A' runs that
# cannot transit a text-only API intact. This script auto-detects the gzip magic (1f 8b).
# Usage: bash decode_b64.sh
set -e
find . -name '*.b64' | while read f; do
  out="${f%.b64}"
  tmp="$(mktemp)"
  base64 -d "$f" > "$tmp"
  if [ "$(od -An -tx1 -N2 "$tmp" | tr -d ' \n')" = "1f8b" ]; then
    gzip -dc "$tmp" > "$out"
    rm -f "$tmp"
  else
    mv "$tmp" "$out"
  fi
  echo "restored $out"
done
echo "Done. Serve the site: cd website && python -m http.server 8000"
