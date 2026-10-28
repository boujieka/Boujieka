#!/usr/bin/env bash
# Rebuild the illustrator album (Markdown, Word, PDF) for Courant Continental — Cameroun.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
D="$HERE/../../docs/courant-continental-cameroun"
TMP="$(mktemp -d)"
python3 "$HERE/../assemble_courant_continental.py" "$D"
TITLE="Courant Continental — Cameroun · Saison 1 (illustrateur)"
pandoc "$D/album-saison-1-illustrateur.md" -f markdown-yaml_metadata_block -t docx -o "$D/album-saison-1-illustrateur.docx" --toc --toc-depth=3 --metadata title="$TITLE"
pandoc "$D/album-saison-1-illustrateur.md" -f markdown-yaml_metadata_block -t html5 -s --toc --toc-depth=3 --metadata title="$TITLE" --metadata lang=fr -c "$HERE/album.css" --embed-resources -o "$TMP/album.html"
python3 - "$TMP/album.html" <<'PY'
import re, sys
p = sys.argv[1]; h = open(p, encoding='utf-8').read()
def fix(m):
    t = m.group(0)
    if re.search(r'<th[^>]*>\s*Case\s*</th>', t):
        t = re.sub(r'<colgroup>.*?</colgroup>', '', t, flags=re.S).replace('<table', '<table class="cases"', 1)
    return t
h = re.sub(r'<table.*?</table>', fix, h, flags=re.S)
h = h.replace('</head>', '<style>td:first-child{width:auto;text-align:left;font-weight:normal}table.cases{table-layout:fixed}table.cases td:first-child,table.cases th:first-child{width:4%;text-align:center;font-weight:bold}table.cases td:nth-child(2),table.cases th:nth-child(2){width:46%}table.cases td:nth-child(3),table.cases th:nth-child(3){width:50%}</style></head>', 1)
open(p, 'w', encoding='utf-8').write(h)
PY
node "$HERE/pdf.js" "$TMP/album.html" "$D/album-saison-1-illustrateur.pdf"
echo "OK: $D/album-saison-1-illustrateur.{md,docx,pdf}"
