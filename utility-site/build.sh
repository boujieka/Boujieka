#!/bin/sh
# Wrap landing.html (artifact-format page) into a standalone page for static hosting.
# The page's own <title>, <meta>, <link> and <style> come first in landing.html, so they stay in
# <head>; the body starts implicitly at the first page element.
# On Netlify the access form is collected by Netlify Forms (data-netlify on the form).
set -e
cd "$(dirname "$0")"
mkdir -p dist
{
  cat <<'HEAD'
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="Courant · Africa Utility Intelligence">
<meta property="og:description" content="Benchmarking et diagnostic des sociétés d’électricité africaines à partir de leurs documents publics.">
<script>window.AUI_FORM_LIVE = true;</script>
HEAD
  cat landing.html
  printf '\n</html>\n'
} > dist/index.html
cp favicon.svg dist/favicon.svg
echo "wrote dist/index.html"
