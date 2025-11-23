def emulate_orderflow(candles):
    if not candles:
        return {'buys':0,'sells':0,'imbalance':0}
    buys = 0; sells = 0
    for c in candles:
        if c['close'] > c['open']:
            buys += c.get('volume',1)
        else:
            sells += c.get('volume',1)
    imbalance = buys - sells
    return {'buys':buys,'sells':sells,'imbalance':imbalance}

def rolling_imbalance(candles, window=20):
    out = []
    for i in range(window, len(candles)+1):
        s = emulate_orderflow(candles[i-window:i])
        out.append(s['imbalance'])
    return out
