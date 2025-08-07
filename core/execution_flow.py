from datetime import datetime
from utils.logger import log

class ExecutionFlow:
    def __init__(self, memory):
        self.memory = memory

    def _validate(self, signal:dict):
        required = ["symbol","direction","entry","sl","tp"]
        if not signal:
            return False, "empty"
        for k in required:
            if signal.get(k) is None:
                return False, f"missing_{k}"
        if signal["sl"] == signal["entry"]:
            return False, "sl_equals_entry"
        if signal["direction"] not in ("buy","sell"):
            return False, "bad_direction"
        return True, "ok"

    def _compute_rr(self, signal:dict):
        entry = float(signal["entry"]); sl = float(signal["sl"]); tp = float(signal["tp"])
        risk = abs(entry - sl); reward = abs(tp - entry)
        rr = 0.0 if risk == 0 else round(reward / risk, 4)
        return rr

    def execute(self, strategy_obj):
        context = {"now": datetime.utcnow().isoformat()+"Z"}
        signal = strategy_obj.generate_signal(context=context)
        ok, reason = self._validate(signal)
        if not ok:
            log(f"{strategy_obj.name}: invalid signal -> {reason}", "WARN")
            return {"strategy": strategy_obj.name, "valid": False, "reason": reason}

        rr = self._compute_rr(signal)
        enriched = {
            **signal,
            "strategy": strategy_obj.name,
            "rr": rr,
            "timestamp": context["now"],
            "win": True if rr >= 1.5 else False
        }
        log(f"Executed {strategy_obj.name} on {signal['symbol']} | dir={signal['direction']} rr={rr}")
        return enriched
