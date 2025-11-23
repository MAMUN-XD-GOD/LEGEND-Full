import numpy as np
import matplotlib.pyplot as plt

def compute_heatmap(candles, precision=0.0001, window=200):
    if not candles:
        return {}
    recent = candles[-window:]
    levels = {}
    for c in recent:
        p = round(c['close'] / precision) * precision
        levels[p] = levels.get(p, 0) + 1
    return levels

def plot_heatmap(levels, out='heatmap.png'):
    if not levels:
        return None
    xs = sorted(levels.keys())
    ys = [levels[x] for x in xs]
    plt.figure(figsize=(8,4))
    plt.bar(xs, ys, width=(xs[1]-xs[0]) if len(xs)>1 else 0.0001)
    plt.title('Liquidity heatmap (price level counts)')
    plt.savefig(out)
    return out
