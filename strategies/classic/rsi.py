NAME = "rsi_contextual_ema"
from utils.indicators import ema, rsi

class Strategy:
    def __init__(self, symbol="EURUSD", tf="M15"):
        self.symbol = symbol
        self.tf = tf
        self.name = f"{NAME}:{symbol}:{tf}"

    def run(self, context):
        closes = context.get("closes", [1.001,1.002,1.003,1.006,1.004,1.008,1.007,1.006,1.009,1.013,1.012,1.015])
        highs  = context.get("highs",  [c*1.0015 for c in closes])
        lows   = context.get("lows",   [c*0.9985 for c in closes])
        sym = context.get("symbol", self.symbol)

        e9 = ema(closes, 9)
        e21 = ema(closes, 21)
        rs = rsi(closes, 14)

        direction = None
        if e9[-1] > e21[-1] and rs[-1] > 55:
            direction = "buy"
        elif e9[-1] < e21[-1] and rs[-1] < 45:
            direction = "sell"
        if not direction:
            return {}

        entry = closes[-1]
        atr_like = max(highs[-5:]) - min(lows[-5:])
        risk = max(atr_like * 0.5, entry*0.001)
        if direction == "buy":
            sl = entry - risk; tp = entry + risk*2.2
        else:
            sl = entry + risk; tp = entry - risk*2.2

        return {
            "symbol": sym,
            "direction": direction,
            "entry": round(entry, 6),
            "sl": round(sl, 6),
            "tp": round(tp, 6),
            "tags": ["rsi","ema_trend","contextual"],
        }

def run(context):
    return Strategy().run(context)
