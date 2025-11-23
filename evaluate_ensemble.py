import pandas as pd
from backend.ensemble import predict_proba, load_model

if __name__=='__main__':
    df = pd.read_csv('examples/historical_sample.csv')
    # featurize similar to trainer
    df['ret'] = df['close'].pct_change().fillna(0)
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['ema_diff'] = df['ema9'] - df['ema21']
    df['rsi'] = (df['close'].diff().clip(lower=0).rolling(14).mean() - (-df['close'].diff().clip(upper=0).rolling(14).mean())).fillna(0)
    load_model()
    probs = []
    for i,row in df.iterrows():
        fv = {'ret':row['ret'],'ema_diff':row['ema_diff'],'rsi':row['rsi']}
        try:
            p = predict_proba(fv)
        except Exception:
            p = None
        probs.append(p)
    df['prob_call'] = probs
    print(df[['ts','close','prob_call']].tail())
