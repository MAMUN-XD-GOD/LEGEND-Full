import pandas as pd
import numpy as np

def compute_basic_features(candles):
    df = pd.DataFrame(candles)
    if df.empty:
        return {}
    df['ts'] = pd.to_datetime(df['ts'], unit='s')
    df.set_index('ts', inplace=True)
    df['ret'] = df['close'].pct_change().fillna(0)
    df['ema9'] = df['close'].ewm(span=9,adjust=False).mean()
    df['ema21'] = df['close'].ewm(span=21,adjust=False).mean()
    df['ema_diff'] = df['ema9'] - df['ema21']
    df['atr'] = (df['high'] - df['low']).rolling(14).mean().fillna(0)
    df['rsi'] = compute_rsi(df['close'], period=14)
    df['volatility'] = df['ret'].rolling(20).std().fillna(0)
    # last row features
    last = df.iloc[-1]
    return {
        'close': float(last['close']),
        'ret': float(last['ret']),
        'ema9': float(last['ema9']),
        'ema21': float(last['ema21']),
        'ema_diff': float(last['ema_diff']),
        'atr': float(last['atr']),
        'rsi': float(last['rsi']),
        'volatility': float(last['volatility'])
    }

def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0).rolling(period).mean()
    down = -delta.clip(upper=0).rolling(period).mean()
    rs = up / (down + 1e-9)
    rsi = 100 - 100 / (1 + rs)
    return rsi.fillna(50)

def normalize_features(feat_dict):
    # simple scaling
    scaled = {}
    scaled['ema_diff_s'] = feat_dict.get('ema_diff',0) / max(1e-6, abs(feat_dict.get('close',1))*0.001)
    scaled['rsi_s'] = (feat_dict.get('rsi',50)-50)/50
    scaled['vol_s'] = feat_dict.get('volatility',0)
    scaled['atr_s'] = feat_dict.get('atr',0)
    return scaled
