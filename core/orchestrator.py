import importlib
from utils.logger import log

class StrategyWrapper:
    def __init__(self, name, module):
        self.name = name
        self._module = module

    def generate_signal(self, context:dict):
        if hasattr(self._module, "Strategy"):
            s = self._module.Strategy()
            self.name = getattr(s, "name", self.name)
            return s.run(context)
        elif hasattr(self._module, "run"):
            return self._module.run(context)
        else:
            raise RuntimeError(f"Strategy {self.name} has no Strategy class or run()")

class Orchestrator:
    def __init__(self, memory, config=None):
        self.memory = memory
        self.config = config or {}
        self._cache = []

    def load_strategies(self):
        if self._cache:
            return self._cache
        pkgs = self.config.get("strategy_packages") if self.config else None
        if not pkgs:
            pkgs = ["strategies.classic.rsi"]
        loaded = []
        for path in pkgs:
            try:
                mod = importlib.import_module(path)
                name = getattr(mod, "NAME", path.split(".")[-1])
                loaded.append(StrategyWrapper(name, mod))
                log(f"Loaded strategy: {name}")
            except Exception as e:
                log(f"Failed loading {path}: {e}", "ERROR")
        self._cache = loaded
        return loaded

    def evolve(self):
        for sym in (self.config.get("symbols") or []):
            best = self.memory.get_best_for(sym)
            if best:
                log(f"[EVOLVE] Best for {sym}: {best['strategy']} score={best['score']} winrate={best['winrate']:.2f} rr={best['avg_rr']:.2f}")
