#!/usr/bin/env bash

set -e

source ./config.bash.priv

echo "Connecting as user '$DB_USER' to $DB_NAME at $DB_HOST..."
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"