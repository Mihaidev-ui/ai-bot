def ema(values, period):
    k = 2/(period+1)
    ema_vals = []
    prev = None
    for v in values:
        prev = v if prev is None else (v - prev)*k + prev
        ema_vals.append(prev)
    return ema_vals

def rsi(values, period=14):
    if len(values) < period+1:
        return [50.0]*len(values)
    gains = []; losses = []
    for i in range(1, len(values)):
        ch = values[i] - values[i-1]
        gains.append(max(ch, 0.0)); losses.append(max(-ch, 0.0))
    avg_gain = sum(gains[:period])/period
    avg_loss = sum(losses[:period])/period
    rsis = [50.0]*(period)
    for i in range(period, len(gains)):
        avg_gain = (avg_gain*(period-1) + gains[i]) / period
        avg_loss = (avg_loss*(period-1) + losses[i]) / period
        rs = (avg_gain / avg_loss) if avg_loss != 0 else 999999.0
        r = 100 - (100/(1+rs))
        rsis.append(r)
    while len(rsis) < len(values):
        rsis.insert(0, 50.0)
    return rsis
