import shap
import numpy as np

def shap_explain(model, X_sample, feature_names=None):
    try:
        expl = shap.Explainer(model)
        shap_values = expl(X_sample)
        # return summary
        return {'shap_values': shap_values.values.tolist(), 'base_values': shap_values.base_values.tolist()}
    except Exception as e:
        return {'error': str(e)}
