#!/usr/bin/env bash
# Deploy site/dist/ to the Netlify project "cartouche-africa" with the official Netlify CLI.
# Needs NETLIFY_AUTH_TOKEN in the environment (a Netlify personal access token, set in the
# cloud environment's settings, never committed). Optional: NETLIFY_SITE_ID.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${NETLIFY_AUTH_TOKEN:?NETLIFY_AUTH_TOKEN is not set; cannot deploy}"
SITE_ID="${NETLIFY_SITE_ID:-cbc09739-8a6a-44e0-b425-63608d1f5431}"
test -s site/dist/index.html && test -s site/dist/plateforme.html && test -s site/dist/veille.json || { echo "site/dist is incomplete"; exit 1; }
npx -y netlify-cli@latest deploy --prod --dir site/dist --site "$SITE_ID" --no-build --message "veille $(date -u +%F)"
