#!/usr/bin/env bash
# Restore binary artifacts stored as base64 sidecars (GitHub MCP transport can't carry raw binary).
# Usage: bash decode_b64.sh
set -e
find . -name '*.b64' | while read f; do
  out="${f%.b64}"
  base64 -d "$f" > "$out"
  echo "restored $out"
done
echo "Done. Serve the site: cd website && python -m http.server 8000"
