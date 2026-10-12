#!/bin/sh
# Runs once when the database volume is created: creates the non-owner application role used by the API.
set -eu
: "${APP_DB_PASSWORD:?set APP_DB_PASSWORD}"
psql -v ON_ERROR_STOP=1 -U postgres -d access360 <<SQL
CREATE ROLE access360_app LOGIN PASSWORD '${APP_DB_PASSWORD}';
GRANT CONNECT ON DATABASE access360 TO access360_app;
SQL
