#!/usr/bin/env bash
# Daily veille: rebuild data for today, watch official sources, build site/dist/.
# Deployment to Netlify is a separate step (see docs/DAILY_WATCH.md).
# Safe to run in a fresh container: database setup and migrations are idempotent.
set -euo pipefail
cd "$(dirname "$0")/.."

AS_OF="${AS_OF:-$(date -u +%F)}"
INGEST="${INGEST:-1}"  # 1: collect UMOA-Titres, BEAC and BVMAC results and strictly auto-approve (owner's instructions, 2026-10-04/08)
PREVIOUS="${PREVIOUS:-https://cartouche-africa.netlify.app/veille.json}"
export ABI_DATABASE_URL="${ABI_DATABASE_URL:-postgresql+psycopg://abi:abi@localhost:5432/abi}"

if command -v service >/dev/null && ! pg_isready -q 2>/dev/null; then
  service postgresql start >/dev/null
  sleep 2
fi
psql_admin() { su postgres -c "psql -tAc \"$1\""; }
psql_admin "select 1 from pg_roles where rolname='abi'" | grep -q 1 \
  || psql_admin "create role abi login password 'abi' createdb"
psql_admin "select 1 from pg_database where datname='abi'" | grep -q 1 \
  || su postgres -c "createdb -O abi abi"

# The UMOA-Titres extractor and checker need pdftotext (poppler).
if ! command -v pdftotext >/dev/null; then
  (apt-get install -y -qq poppler-utils >/dev/null 2>&1 || (apt-get update -qq >/dev/null && apt-get install -y -qq poppler-utils >/dev/null)) \
    || echo "WARNING: pdftotext unavailable; new results will be held, not approved"
fi
# CEMAC: BEAC result notices are scanned PDFs and need OCR (tesseract, French) and pdftoppm.
if ! command -v tesseract >/dev/null || ! tesseract --list-langs 2>/dev/null | grep -qx fra; then
  (apt-get install -y -qq tesseract-ocr tesseract-ocr-fra poppler-utils >/dev/null 2>&1 \
    || (apt-get update -qq >/dev/null && apt-get install -y -qq tesseract-ocr tesseract-ocr-fra poppler-utils >/dev/null)) \
    || echo "WARNING: tesseract unavailable; BEAC notices are skipped today (BVMAC and UMOA continue)"
fi
python3 -m pip install -q -e "backend[dev]" 2>/dev/null || python3 -m pip install -q -e "backend[dev]" --break-system-packages
cd backend
alembic upgrade head
INGEST_FLAG=""
[ "$INGEST" = "1" ] && INGEST_FLAG="--ingest"
python3 -m app.watch.daily --as-of "$AS_OF" --previous "$PREVIOUS" --out ../site/dist $INGEST_FLAG
cd ..
python3 scripts/check_dist.py --as-of "$AS_OF"  # refuse a partial or mixed build before any deploy
echo "OK: site/dist built for $AS_OF"
