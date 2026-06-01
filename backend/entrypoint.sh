#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-eventflow}" > /dev/null 2>&1; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is up"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting application: $*"
exec "$@"
