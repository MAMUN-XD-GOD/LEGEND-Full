def detect_bos_choch(candles):
    if len(candles) < 6:
        return {'bias':'neutral','type':None}
    closes = [c['close'] for c in candles[-6:]]
    # simple detection
    if closes[-1] > max(closes[:-1]):
        return {'bias':'bull','type':'BOS'}
    if closes[-1] < min(closes[:-1]):
        return {'bias':'bear','type':'BOS'}
    return {'bias':'neutral','type':None}
