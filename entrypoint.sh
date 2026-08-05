#!/bin/bash
set -e

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running database migrations..."
    flask db upgrade
fi

exec "$@"
