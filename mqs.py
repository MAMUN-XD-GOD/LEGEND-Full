def market_quality_score(candles):
    if not candles:
        return 0
    vols = [abs(c['high']-c['low']) for c in candles]
    vol = sum(vols)/len(vols)
    spikes = sum(1 for i in range(1,len(candles)) if abs(candles[i]['close']-candles[i-1]['close'])/max(1,abs(candles[i-1]['close']))>0.005)
    score = max(0, 100 - spikes*20 - vol*1000)
    return score
