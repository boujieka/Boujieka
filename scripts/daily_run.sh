#!/usr/bin/env bash
# Daily veille: rebuild data for today, watch official sources, build site/dist/.
# Deployment to Netlify is a separate step (see docs/DAILY_WATCH.md).
# Safe to run in a fresh container: database setup and migrations are idempotent.
set -euo pipefail
cd "$(dirname "$0")/.."

AS_OF="${AS_OF:-$(date -u +%F)}"
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

python3 -m pip install -q -e "backend[dev]" 2>/dev/null || python3 -m pip install -q -e "backend[dev]" --break-system-packages
cd backend
alembic upgrade head
python3 -m app.watch.daily --as-of "$AS_OF" --previous "$PREVIOUS" --out ../site/dist
echo "OK: site/dist built for $AS_OF"
