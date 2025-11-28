#!/bin/sh
# wait-for-db.sh

set -e

# Host and Port are passed from docker-compose env
host="db"
port="5432"
cmd="$@"

>&2 echo "Waiting for PostgreSQL ($host:$port)..."

# Use a loop to check if the database is ready every second
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -p "$port" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command: $cmd"
exec $cmd