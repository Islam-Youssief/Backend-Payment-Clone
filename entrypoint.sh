#!/bin/sh

set -e

echo "Running database migrations..."
python -m flask --app run:application db upgrade

echo "Starting application..."
exec python run.py