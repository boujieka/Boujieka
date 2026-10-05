#!/bin/sh
# Wrap landing.html (artifact-format body) into a standalone page for static hosting.
# On Netlify the access form is collected by Netlify Forms (data-netlify on the form).
set -e
cd "$(dirname "$0")"
mkdir -p dist
{
  printf '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  printf '<script>window.AUI_FORM_LIVE = true;</script>\n</head>\n<body>\n'
  cat landing.html
  printf '\n</body>\n</html>\n'
} > dist/index.html
echo "wrote dist/index.html"
