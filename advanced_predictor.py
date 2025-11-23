import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib, os
MODEL_PATH='models/adv_predictor.pkl'

class Predictor:
    def __init__(self):
        self.model = None
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
    def train_dummy(self, X, y):
        m = RandomForestClassifier(n_estimators=50)
        m.fit(X,y)
        os.makedirs('models', exist_ok=True); joblib.dump(m, MODEL_PATH); self.model = m
    def predict_proba(self, features):
        if self.model is None:
            return 0.5
        import numpy as np
        X = np.array([features])
        p = self.model.predict_proba(X)[0]
        return float(p[1])
