#!/bin/bash
set -e

echo "Starting IP Geolocation Service..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
