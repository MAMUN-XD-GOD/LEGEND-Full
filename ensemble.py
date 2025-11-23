import joblib, os
_model = None

def load_model(path='models/ensemble_model.pkl'):
    global _model
    if _model is None:
        _model = joblib.load(path)
    return _model

def predict_proba(feature_vector):
    model = load_model()
    # feature_vector is dict-like with keys ['ret','ema_diff','rsi']
    import numpy as np
    X = np.array([[feature_vector.get('ret',0), feature_vector.get('ema_diff',0), feature_vector.get('rsi',0)]])
    p = model.predict_proba(X)[0]
    # return probability of CALL
    return float(p[1])
