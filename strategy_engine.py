from backend.feature_engine import compute_features
from backend.smc_engine import detect_bos_choch
from backend.multi_tf_gate import agree
from backend.spike_filter import is_spike
from backend.mqs import market_quality_score

class StrategyEngine:
    def __init__(self, db=None):
        self.db = db
    async def start(self): pass
    async def stop(self): pass
    async def evaluate(self, pair, candles, datafeed=None):
        # candles are raw M1 candles
        if not candles or len(candles) < 30:
            return None
        # compute main, mid, short views
        main = candles[-60:] if len(candles) >= 60 else candles
        mid = candles[-30:] if len(candles) >= 30 else candles
        short = candles[-10:] if len(candles) >= 10 else candles
        f_main = compute_features(main)
        f_mid = compute_features(mid)
        f_short = compute_features(short)
        # quality
        quality = market_quality_score(main)
        if quality < 30:
            return None
        # spike
        if is_spike(short):
            return None
        # multi-tf agreement
        if not agree(f_short, f_mid, f_main):
            return None
        struct = detect_bos_choch(main)
        direction = None; conf = 50; reasons = []
        if f_short.get('ema9') > f_short.get('ema21') and struct.get('bias') == 'bull':
            direction = 'CALL'; reasons.append('ema+struct_bull')
        if f_short.get('ema9') < f_short.get('ema21') and struct.get('bias') == 'bear':
            direction = 'PUT'; reasons.append('ema+struct_bear')
        if f_main.get('ob'):
            conf -= 10; reasons.append('order_block_present')
        # final
        if direction:
            return {'fire':True,'signal':{'pair':pair,'direction':direction,'confidence':conf,'reasons':reasons,'entry_ts':short[-1]['ts']}}
        return None
