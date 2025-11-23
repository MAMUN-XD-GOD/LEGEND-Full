import pandas as pd
import numpy as np

def regime_from_candles(candles, window=50):
    """Return regime: 'trending' or 'ranging' and volatility metric.
    candles: list of dict with keys ts, open, high, low, close, volume
    """
    if not candles or len(candles) < window:
        return {'regime':'unknown','vol':0.0,'trend_strength':0.0}
    df = pd.DataFrame(candles[-window:])
    df['hl'] = df['high'] - df['low']
    df['oc'] = (df['close'] - df['open']).abs()
    vol = df['hl'].mean()
    # momentum proxy: rolling mean of close diff
    momentum = df['close'].diff().abs().rolling(10).mean().iloc[-1]
    # ADX-like proxy: ratio of directional movement strength
    dm = (df['high'] - df['high'].shift()).fillna(0).clip(lower=0)
    dm2 = (df['low'].shift() - df['low']).fillna(0).clip(lower=0)
    dm_sum = dm.rolling(14).sum().iloc[-1]
    dm2_sum = dm2.rolling(14).sum().iloc[-1]
    trend_strength = (dm_sum - dm2_sum) / (dm_sum + dm2_sum + 1e-9)
    trend_strength = float(np.abs(trend_strength))
    regime = 'trending' if (momentum > vol*0.6 and trend_strength > 0.1) else 'ranging'
    return {'regime':regime, 'vol':float(vol), 'trend_strength':float(trend_strength), 'momentum':float(momentum)}
