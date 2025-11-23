import pandas as pd, numpy as np, os, math
from backend.strategy_engine import StrategyEngine

class Backtester:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.engine = StrategyEngine()

    def sliding_windows(self, window_size=60):
        rows = self.df.to_dict('records')
        for i in range(window_size, len(rows)-1):
            window = rows[i-window_size:i]
            next_candle = rows[i]
            yield window, next_candle

    def run(self, stake=1.0):
        wins=0; losses=0; total=0; pnl=0.0
        for window, next_candle in self.sliding_windows():
            res = self.engine.evaluate('BACKTEST', window)
            if not res or not res.get('fire'): continue
            s = res['signal']
            total += 1
            # naive resolution: if CALL and next close>open -> win
            if s['direction']=='CALL' and next_candle['close']>next_candle['open']:
                wins += 1; pnl += stake
            elif s['direction']=='PUT' and next_candle['close']<next_candle['open']:
                wins += 1; pnl += stake
            else:
                losses += 1; pnl -= stake
        return {'total': total, 'wins': wins, 'losses': losses, 'pnl': pnl, 'winrate': (wins/total*100) if total else None}

if __name__=='__main__':
    import sys
    path = sys.argv[1] if len(sys.argv)>1 else 'examples/historical_sample.csv'
    bt = Backtester(path)
    res = bt.run()
    print('Backtest result:', res)
