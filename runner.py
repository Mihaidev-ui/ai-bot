from core.orchestrator import Orchestrator
from core.execution_flow import ExecutionFlow
from core.config import CONFIG
from ai.memory import Memory
from utils.logger import log

if __name__ == "__main__":
    mem = Memory()
    orch = Orchestrator(mem, CONFIG)
    execf = ExecutionFlow(mem)
    for strat in orch.load_strategies():
        result = execf.execute(strat)
        if result.get("valid", True):
            mem.save_result(strat.name, result)
    orch.evolve()
    log("Done initial run.")
