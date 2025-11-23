import joblib, os

def save_model(model, path='models/ensemble_model.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(path='models/ensemble_model.pkl'):
    return joblib.load(path)
