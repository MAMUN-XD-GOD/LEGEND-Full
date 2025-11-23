from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json, sqlite3, asyncio, logging
app = FastAPI()
LOG = logging.getLogger('bridge_server')
DB_PATH = 'quantumapex.db'

def insert_candles(pair, candles):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for c in candles:
        cur.execute('INSERT INTO candles(pair,ts,open,high,low,close,volume) VALUES(?,?,?,?,?,?,?)', (pair, int(c['ts']), float(c['open']), float(c['high']), float(c['low']), float(c['close']), float(c.get('volume',0))))
    conn.commit(); conn.close()

@app.websocket('/ws/bridge')
async def bridge_ws(ws: WebSocket):
    await ws.accept()
    LOG.info('bridge client connected')
    try:
        while True:
            text = await ws.receive_text()
            try:
                payload = json.loads(text)
            except Exception:
                await ws.send_text(json.dumps({'error':'invalid_json'})); continue
            token = payload.get('token')
            if not token:
                await ws.send_text(json.dumps({'error':'no_token'})); continue
            pair = payload.get('pair')
            candles = payload.get('candles')
            if not pair or not candles:
                await ws.send_text(json.dumps({'error':'missing_fields'})); continue
            # insert into sqlite
            try:
                insert_candles(pair, candles)
            except Exception:
                LOG.exception('db insert failed')
                await ws.send_text(json.dumps({'error':'db_insert'})); continue
            await ws.send_text(json.dumps({'status':'ok'}))
    except WebSocketDisconnect:
        LOG.info('bridge disconnected')
