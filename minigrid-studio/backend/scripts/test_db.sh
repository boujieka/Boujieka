#!/usr/bin/env bash
# Start a throwaway PostgreSQL 16 cluster for the API tests (port 55432).
# Usage: sudo scripts/test_db.sh   then
#   MGS_TEST_DATABASE_URL=postgresql+psycopg://mgs:mgs@127.0.0.1:55432/mgs_test pytest
set -euo pipefail
BIN=${PG_BIN:-/usr/lib/postgresql/16/bin}
DATA=${PG_DATA:-/var/lib/postgresql/mgs-test}
runuser -u postgres -- bash -c "rm -rf '$DATA' && '$BIN/initdb' -D '$DATA' -A trust -U postgres -E UTF8 --locale=C.UTF-8 >/dev/null \
  && '$BIN/pg_ctl' -D '$DATA' -o '-p 55432 -k /tmp' -l '$DATA/log.txt' start"
sleep 2
psql -h /tmp -p 55432 -U postgres -c "create user mgs password 'mgs'" -c "create database mgs owner mgs" \
     -c "create database mgs_test owner mgs"
