#!/usr/bin/env bash
# Reassemble files that were split into <path>.parts/part_NNN for transport.
# Usage: bash assemble_parts.sh   (run BEFORE decode_b64.sh)
set -e
find . -type d -name '*.parts' | while read d; do
  target="${d%.parts}"
  mkdir -p "$(dirname "$target")"
  cat "$d"/part_* > "$target"
  echo "assembled $target"
done
