#!/usr/bin/env bash
# Deploy site/dist/ to the Netlify project "cartouche-africa" with the official Netlify CLI.
# Needs NETLIFY_AUTH_TOKEN in the environment (a Netlify personal access token, set in the
# cloud environment's settings, never committed). Optional: NETLIFY_SITE_ID.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${NETLIFY_AUTH_TOKEN:?NETLIFY_AUTH_TOKEN is not set; cannot deploy}"
SITE_ID="${NETLIFY_SITE_ID:-cbc09739-8a6a-44e0-b425-63608d1f5431}"
python3 scripts/check_dist.py ${AS_OF:+--as-of "$AS_OF"} || { echo "site/dist failed the pre-deploy checks; not deployed"; exit 1; }
npx -y netlify-cli@latest deploy --prod --dir site/dist --site "$SITE_ID" --no-build --message "veille $(date -u +%F)"
