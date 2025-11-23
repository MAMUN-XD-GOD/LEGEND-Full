from backend.feature_engineering import compute_basic_features, normalize_features
from backend.market_regime_detector import regime_from_candles
from backend.ensembler import combine_models, final_decision
from backend.risk_engine_pro import kelly_fraction, position_size, stop_loss_from_atr
from backend.advanced_predictor import Predictor
from backend.ensemble import predict_proba

predictor = Predictor()

def pipeline_decide(pair, candles, account_balance=1000):
    # compute features
    feats = compute_basic_features(candles)
    norm = normalize_features(feats)
    regime = regime_from_candles(candles)
    # model probs
    try:
        eprob = predict_proba({'ret':feats.get('ret',0),'ema_diff':feats.get('ema_diff',0),'rsi':feats.get('rsi',50)})
    except Exception:
        eprob = 0.5
    aprob = predictor.predict_proba([feats.get('ret',0), feats.get('ema_diff',0), feats.get('rsi',50)])
    finalp = combine_models(eprob, aprob)
    decision = final_decision(finalp)
    # risk sizing
    win_rate_est = 0.6
    wr = win_rate_est
    wlr = 1.2
    kf = kelly_fraction(wr, wlr)
    size = position_size(account_balance, kf)
    sl = stop_loss_from_atr(feats.get('close',0), feats.get('atr',0), multiplier=1.0, direction=decision)
    return {'pair':pair,'decision':decision,'prob':finalp,'size':size,'stop_loss':sl,'regime':regime}
