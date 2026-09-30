#!/bin/bash
# Build the KDP paperback interior (6 x 9 in, no bleed) of "Bankable Is Not Enough".
# usage: ./build_paperback.sh manuscript.docx fonts_dir [out.pdf]
#   fonts_dir: Charis SIL 6.200 TTFs (https://github.com/silnrsi/font-charis/releases)
# needs pandoc >= 3, and Python with weasyprint and pypdf.
set -e
DIR=$(cd "$(dirname "$0")" && pwd)
IN=$1; FONTS=$2; OUT=${3:-Bankable_Is_Not_Enough_paperback_6x9.pdf}
TMP=$(mktemp -d)
BOOK_ISBN=${BOOK_ISBN:-9798178190425} pandoc "$IN" -f docx -t html5 --wrap=none --section-divs \
  --lua-filter="$DIR/kindle.lua" --lua-filter="$DIR/print_notes.lua" -o "$TMP/body.html"
python "$DIR/build_print.py" "$TMP/body.html" "$FONTS" "$OUT"
