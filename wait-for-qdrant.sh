#!/bin/bash

host="$1"
port="$2"
shift 2  # Drop host and port so $@ becomes the real command

echo "⏳ Waiting for Qdrant at $host:$port..."

until curl -s "http://$host:$port/collections" > /dev/null; do
  echo "🔁 Still waiting for Qdrant..."
  sleep 2
done

echo "✅ Qdrant is up!"
exec "$@"
