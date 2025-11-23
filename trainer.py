import pandas as pd, numpy as np, os
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

def featurize(df):
    # simple features: returns, ema diff, rsi diff approximations
    df['ret'] = df['close'].pct_change().fillna(0)
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['ema_diff'] = df['ema9'] - df['ema21']
    df['rsi'] = (df['close'].diff().clip(lower=0).rolling(14).mean() - (-df['close'].diff().clip(upper=0).rolling(14).mean()))
    df = df.fillna(0)
    return df

if __name__=='__main__':
    import sys
    path = sys.argv[1] if len(sys.argv)>1 else 'examples/historical_sample.csv'
    df = pd.read_csv(path)
    df = featurize(df)
    # label: whether next candle close>open (CALL) else PUT
    df['label'] = (df['close'].shift(-1) > df['open'].shift(-1)).astype(int)
    df = df.dropna()
    X = df[['ret','ema_diff','rsi']]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = (preds==y_test).mean()
    print('Train acc:', acc)
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/ensemble_model.pkl')
    print('Saved model to models/ensemble_model.pkl')
