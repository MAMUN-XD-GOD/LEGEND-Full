def agree(short_feat, mid_feat, long_feat):
    # require majority agree on ema direction
    votes = []
    for f in (short_feat, mid_feat, long_feat):
        if not f: continue
        votes.append('bull' if f.get('ema9',0) > f.get('ema21',0) else 'bear')
    if not votes:
        return False
    return votes.count(votes[0]) >= 2
