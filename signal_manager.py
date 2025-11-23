import sqlite3, json
DB='quantumapex.db'

class SignalManager:
    def __init__(self):
        pass
    def save(self, signal):
        conn = sqlite3.connect(DB); cur = conn.cursor()
        cur.execute('INSERT INTO signals(pair,direction,confidence,reasons,entry_ts,result,resolved_ts) VALUES(?,?,?,?,?,?,?)', (signal['pair'], signal['direction'], float(signal['confidence']), ','.join(signal.get('reasons',[])), int(signal.get('entry_ts',0)), None, None))
        conn.commit(); conn.close()
    def resolve_recent(self, pair):
        # simplistic: mark last unresolved signal result based on next candle direction
        conn = sqlite3.connect(DB); cur = conn.cursor()
        cur.execute('SELECT id,entry_ts FROM signals WHERE pair=? AND result IS NULL ORDER BY id DESC LIMIT 1', (pair,))
        row=cur.fetchone()
        if not row:
            conn.close(); return
        sid, entry_ts = row
        # find candle after entry_ts
        cur.execute('SELECT ts,open,high,low,close FROM candles WHERE pair=? AND ts>? ORDER BY ts ASC LIMIT 1', (pair, entry_ts))
        nextc = cur.fetchone()
        if not nextc:
            conn.close(); return
        ts,o,h,l,c = nextc
        # naive resolution: if signal was CALL and close>open => win
        cur.execute('SELECT direction FROM signals WHERE id=?',(sid,))
        dir = cur.fetchone()[0]
        res = 'loss'
        if dir=='CALL' and c>o: res='win'
        if dir=='PUT' and c<o: res='win'
        cur.execute('UPDATE signals SET result=?, resolved_ts=? WHERE id=?', (res, ts, sid))
        conn.commit(); conn.close()
