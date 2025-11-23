def choose_model(market_regime):
    # simple rules
    if market_regime=='trending':
        return 'adv_predictor'
    if market_regime=='ranging':
        return 'ensemble'
    return 'ensemble'
