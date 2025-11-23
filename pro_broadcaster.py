from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio, json, logging
app = FastAPI()
LOG = logging.getLogger('pro_broadcaster')
clients = set()

@app.websocket('/ws/signals')
async def ws_signals(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            data = await ws.receive_text()
            # this endpoint is intended for read-only (clients subscribe). Keep alive.
    except WebSocketDisconnect:
        clients.discard(ws)

async def broadcast(obj):
    text = json.dumps(obj)
    for c in list(clients):
        try:
            await c.send_text(text)
        except Exception:
            clients.discard(c)

# Usage: import pro_broadcaster and call broadcast({'type':'signal','signal':{...}})
