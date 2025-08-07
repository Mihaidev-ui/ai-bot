import json, os, threading
from datetime import datetime

class Memory:
    def __init__(self, path:str="/mnt/data/BOT_AI_REBUILD/history.json"):
        self.path = path
        self._lock = threading.Lock()
        self.state = {"runs": [], "perf": {}, "best_by_symbol": {}}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            except Exception:
                pass

    def _save(self):
        tmp = self.path + ".tmp"
        with self._lock:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
            os.replace(tmp, self.path)

    def save_result(self, strategy_name:str, result:dict):
        symbol = result.get("symbol","?")
        ts = result.get("timestamp") or datetime.utcnow().isoformat()+"Z"
        rr = float(result.get("rr", 0.0))
        win = bool(result.get("win", False))
        # append run
        self.state["runs"].append({"strategy":strategy_name, **result, "timestamp":ts})
        # perf aggregate
        perf_sym = self.state["perf"].setdefault(symbol, {})
        perf = perf_sym.setdefault(strategy_name, {"wins":0,"losses":0,"avg_rr":0.0,"trades":0})
        perf["trades"] += 1
        if win: perf["wins"] += 1
        else:   perf["losses"] += 1
        n = perf["trades"]
        perf["avg_rr"] = round(((perf["avg_rr"]*(n-1)) + rr)/n, 4)
        # best update
        winrate = perf["wins"]/max(1, perf["trades"])
        score = round(winrate * max(0.1, perf["avg_rr"]), 4)
        best = self.state["best_by_symbol"].get(symbol)
        if best is None or score > best.get("score", 0):
            self.state["best_by_symbol"][symbol] = {"strategy": strategy_name, "score": score, "winrate": winrate, "avg_rr": perf["avg_rr"]}
        self._save()

    def get_best_for(self, symbol:str):
        return self.state["best_by_symbol"].get(symbol)

    def get_perf(self, symbol:str, strategy:str):
        return self.state["perf"].get(symbol, {}).get(strategy, {"wins":0,"losses":0,"avg_rr":0.0,"trades":0})
