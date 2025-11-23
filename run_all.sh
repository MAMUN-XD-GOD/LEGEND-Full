#!/bin/bash
# Start bridge, frontend, main runner, broadcaster in background for local dev
uvicorn backend.bridge_server:app --host 127.0.0.1 --port 8765 &
uvicorn backend.frontend_server:app --host 127.0.0.1 --port 8000 &
python backend/main_runner.py &
uvicorn backend.pro_broadcaster:app --host 127.0.0.1 --port 8777 &
echo 'Started all services (check logs)'
