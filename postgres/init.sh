#!/bin/bash
set -e

echo "$0 start"
psql -v ON_ERROR_STOP=1 --username postgres --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $PG_USER WITH ENCRYPTED PASSWORD '$PG_PASSWORD';
    CREATE DATABASE $PG_DATABASE;
    ALTER DATABASE $PG_DATABASE OWNER TO $PG_USER;
EOSQL
echo "$0 end"

