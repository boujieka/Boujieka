#!/usr/bin/env bash
# Construit les documents Word avec un sommaire paginé (deux passes).
# Usage : tools/build.sh bible|scenario
set -euo pipefail
WHICH="${1:-bible}"
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
rm -f "$HERE/pages_${WHICH}.json"
DOCX_OUT="$TMP/pass1.docx" node "$HERE/build_docx.js" "$WHICH"
soffice --headless --convert-to pdf --outdir "$TMP" "$TMP/pass1.docx" >/dev/null 2>&1
python3 "$HERE/paginate.py" "$TMP/pass1.pdf" "$HERE/toc_${WHICH}.json" "$HERE/pages_${WHICH}.json"
node "$HERE/build_docx.js" "$WHICH"
rm -rf "$TMP"
