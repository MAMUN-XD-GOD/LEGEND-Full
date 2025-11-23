def combine_models(ensemble_prob, adv_prob, weights=(0.6,0.4)):
    """Combine two model probabilities into final probability.
    weights: tuple for (ensemble, adv)
    ""
    e,w = ensemble_prob, adv_prob
    return float(weights[0]*e + weights[1]*w)

def final_decision(prob, threshold=0.55):
    if prob >= threshold:
        return 'CALL'
    if prob <= (1-threshold):
        return 'PUT'
    return 'HOLD'
