#!/usr/bin/env bash
# Build the in-browser demo into landing/app/ (then deploy landing/ to Netlify).
set -euo pipefail
cd "$(dirname "$0")/../.."
(cd backend && .venv/bin/python ../tools/web_demo/build_assets.py)
(cd frontend && npx vite build --mode demo --base /app/)
rm -rf landing/app && cp -r frontend/dist-demo landing/app
echo "landing/app ready"
