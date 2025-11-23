#!/bin/bash
# Simple canary: start new version on different port, health check, switch traffic (manual step)
set -e
NEW_PORT=${1:-8766}
uvicorn backend.bridge_server:app --host 0.0.0.0 --port $NEW_PORT &
PID=$!
echo "Started new instance on port $NEW_PORT (PID $PID)"
# health check
sleep 2
if curl -sSf http://127.0.0.1:$NEW_PORT/ >/dev/null; then
  echo 'Health OK; you can switch reverse-proxy to new port'
else
  echo 'Health failed; killing new instance'
  kill $PID
fi
