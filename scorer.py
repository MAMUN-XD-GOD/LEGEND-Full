def finalize(signal):
    if not signal: return None
    s = signal.copy()
    s['confidence'] = max(0,min(100, s.get('confidence',50)))
    return s
