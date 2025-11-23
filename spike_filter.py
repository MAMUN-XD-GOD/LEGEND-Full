def is_spike(candles, rel_thresh=0.005):
    if len(candles) < 3:
        return False
    last = candles[-1]['close']
    prev = candles[-2]['close']
    if prev == 0:
        return False
    return abs(last - prev)/abs(prev) > rel_thresh
