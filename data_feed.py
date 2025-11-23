import asyncio, sqlite3, time
from collections import defaultdict, deque
import pandas as pd

DB_PATH = 'quantumapex.db'

class DataFeed:
    def __init__(self, pairs=None, maxlen=5000):
        self.pairs = pairs or ['EURUSD']
        self.buffers = defaultdict(lambda: deque(maxlen=maxlen))
        self._running = False
        self._last_id = 0

    async def start(self):
        self._running = True
        asyncio.create_task(self._loop())

    async def stop(self):
        self._running = False

    async def _loop(self):
        while self._running:
            try:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute('SELECT id,pair,ts,open,high,low,close,volume FROM candles WHERE id>? ORDER BY id ASC', (self._last_id,))
                rows = cur.fetchall()
                for r in rows:
                    _id,pair,ts,o,h,l,c,vol = r
                    self._last_id = _id
                    self.buffers[pair].append({'ts':ts,'open':o,'high':h,'low':l,'close':c,'volume':vol})
                conn.close()
            except Exception:
                pass
            await asyncio.sleep(0.5)

    def get_candles(self, pair, limit=200):
        arr = list(self.buffers.get(pair, []))
        return arr[-limit:]

    def get_all(self):
        return {p:list(dq) for p,dq in self.buffers.items()}

    # helper: resample to minutes using pandas
    def resample(self, pair, rule='1T'):
        arr = self.get_candles(pair, limit=1000)
        if not arr:
            return []
        df = pd.DataFrame(arr)
        df['ts'] = pd.to_datetime(df['ts'], unit='s')
        df.set_index('ts', inplace=True)
        agg = df.resample(rule).agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna()
        out = []
        for idx,row in agg.iterrows():
            out.append({'ts':int(idx.timestamp()),'open':float(row['open']),'high':float(row['high']),'low':float(row['low']),'close':float(row['close']),'volume':float(row['volume'])})
        return out
