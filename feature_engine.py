import pandas as pd

def to_df(candles):
    if not candles:
        return pd.DataFrame()
    df = pd.DataFrame(candles)
    if 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'], unit='s')
        df.set_index('ts', inplace=True)
    return df

def add_indicators(df):
    if df.empty:
        return df
    df['ema9'] = df['close'].ewm(span=9,adjust=False).mean()
    df['ema21'] = df['close'].ewm(span=21,adjust=False).mean()
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = tr.rolling(14).mean()
    delta = df['close'].diff()
    up = delta.clip(lower=0).rolling(14).mean()
    down = -delta.clip(upper=0).rolling(14).mean()
    rs = up/down
    df['rsi'] = 100 - 100/(1+rs)
    df['wick'] = df['high'] - df['low']
    return df

def compute_features(candles):
    df = to_df(candles)
    if df.empty:
        return {}
    df = add_indicators(df)
    last = df.iloc[-1]
    # simple order-block: large wick relative to ATR in previous 5 candles
    prev = df.iloc[-6:-1]
    ob = False
    if not prev.empty and last['wick'] > prev['atr'].mean()*1.5:
        ob = True
    return {'ema9':float(last['ema9']),'ema21':float(last['ema21']),'atr':float(last['atr']),'rsi':float(last['rsi']),'ob':ob,'close':float(last['close'])}
