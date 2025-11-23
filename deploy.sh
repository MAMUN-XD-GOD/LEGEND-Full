#!/bin/bash
pip install -r requirements.txt
uvicorn backend.bridge_server:app --host 0.0.0.0 --port 8765 &
uvicorn backend.frontend_server:app --host 0.0.0.0 --port 8000 &
