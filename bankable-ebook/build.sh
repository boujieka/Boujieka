#!/bin/bash
# Build the Kindle ebook (EPUB 3) of "Bankable Is Not Enough" from the Word manuscript.
# usage: ./build.sh manuscript.docx cover.jpg [out.epub]
# needs pandoc >= 3 (e.g. pip install pypandoc_binary); optional: epubcheck.jar for validation.
set -e
DIR=$(cd "$(dirname "$0")" && pwd)
IN=$1; COVER=$2; OUT=${3:-Bankable_Is_Not_Enough.epub}
pandoc "$IN" --metadata-file="$DIR/meta.yaml" -f docx -t epub3 \
  --lua-filter="$DIR/kindle.lua" --css="$DIR/kindle.css" --epub-cover-image="$COVER" \
  --toc --toc-depth=2 --split-level=2 --epub-title-page=false -o "$OUT"
echo "built $OUT"
[ -n "$EPUBCHECK" ] && java -jar "$EPUBCHECK" "$OUT" || true
