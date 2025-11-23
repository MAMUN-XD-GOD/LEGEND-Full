def pre_signal_checks(signal, market_state):
    # market_state contains 'spread','session','recent_news'
    # returns (bool, reasons)
    reasons = []
    if market_state.get('spread', 0) > 0.001: # arbitrary spread threshold
        reasons.append('wide_spread')
    if market_state.get('session') == 'off':
        reasons.append('session_off')
    if market_state.get('recent_news'):
        reasons.append('high_impact_news')
    return (len(reasons)==0, reasons)
