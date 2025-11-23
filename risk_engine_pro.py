import math

def kelly_fraction(win_rate, win_loss_ratio):
    # Avoid division by zero
    if win_loss_ratio <= 0:
        return 0.0
    return max(0.0, (win_rate - (1 - win_rate) / win_loss_ratio))

def position_size(account_balance, kelly_frac, max_risk_percent=0.02):
    # conservative fraction of Kelly and cap by max risk
    frac = 0.5 * kelly_frac
    frac = min(frac, max_risk_percent)
    return max(0.0, account_balance * frac)

def stop_loss_from_atr(entry_price, atr, multiplier=1.0, direction='CALL'):
    if atr <= 0:
        return entry_price * 0.995 if direction=='CALL' else entry_price * 1.005
    if direction == 'CALL':
        return entry_price - atr * multiplier
    else:
        return entry_price + atr * multiplier
